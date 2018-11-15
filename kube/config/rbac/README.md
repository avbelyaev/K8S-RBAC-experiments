# RBAC

RBAC:
- Roles and ClusterRoles: Consist of rules. The difference is the scope: 
in a Role, the rules are applicable to a single namespace, whereas a ClusterRole is cluster-wide
- Subjects:
  - User Accounts: These are global, and meant for humans or processes living outside the cluster.
  - Service Accounts: This kind of account is namespaced and meant for intra-cluster processes running inside pods, which want to authenticate against the API
  - Groups: This is used for referring to multiple accounts.
- RoleBindings and ClusterRoleBindings: Just as the names imply, these bind subjects to roles (i.e. the operations a given user can perform).
As for Roles and ClusterRoles, the difference lies in the scope

A "context" defines a named (cluster,user,namespace) tuple

Start up
```bash
# minikube version <= 0.25
minikube --extra-config=apiserver.Authorization.Mode=RBAC start  

# !! looks like v0.30.0 does not start with this arg 
# or hangs on 'Starting cluster components...' 
```

## Tokens

#### on behalf of admin:
```bash
# create service account for alice at stage namespace
kubectl -n stage create sa alice

# create cluster-role (not namespace-scoped)
kubectl create -f roles/stage-reader-role.yaml

# bind role to sa via rolebinding (alice-staging-rb)
kubectl create -f rb-alice.yaml

# alice's service account has been created
kubectl -n stage get sa alice -o json
```

Suppose alice's sa looks like this:
```json
{
    "kind": "ServiceAccount",
    "metadata": {
        "name": "alice",
        "namespace": "stage"
    },
    "secrets": [{ "name": "alice-token-nt8wm" }]
}
```

Now we need to get alice's secret and token and debase64 them:
```bash
# secret name from above
kubectl get secret alice-token-nt8wm -o json

# put ca.crt into 'ca.crt', token into 'token'
# decode them from base64:
base64 --decode ca.crt > alice-ca.crt
base64 --decode token > alice.token
```

Also we should tell alice where is cluster's master:
```bash
kubectl cluster-info
```

Now we should give alice's credentials (`alice-ca.crt` and `alice.token`) and master's address to user (alice)

Since now cluster know that Alice exists

#### on behalf of user:

Let's configure kubectl to interact with cluster. We should have `alice-ca.crt` and `alice.token`

```bash
# install kubectl
# check configuration
kubectl config view

# ==============================
# >>> CREATE CLUSTER
# --embed-certs: save certs for the cluster entry in kubeconfig
# --server: where cluster's master is running
# --certificate-authority: cert for talking with master
kubectl config set-cluster mini-cluster --embed-certs=true --server=https://192.168.99.100:8443 --certificate-authority=alice-ca.crt

# =============================
# >>> CREATE USER
# --token: contents of alice.token
kubectl config set-credentials alice --token=$(cat alice.token)
    
# =============================
# >>> BIND ALICE WITH CLUSTER AND NAMESPACE
# context = (user,cluster,namespace)
kubectl config set-context alice-stage --user=alice --cluster=mini-cluster --namespace=stage
    
# make sure everything has been created
kubectl config view
```

Switch to context to interact with cluster
```bash
kubectl config use-context alice-ctx

# check permissions
kubectl auth can-i get pods -n stage
# yes
kubectl auth can-i get pods -n prod
# nope
```


## X509 Certs
```bash
# let Frodo be a user
user=frodo

# create key
openssl genrsa -out certs/${user}.key 2048

# create certificate sign request (csr)
# CN = username, O = group (*group can be used as subject in rolebinding later)
openssl req -new -key certs/${user}.key -out certs/${user}.csr  -subj "/CN=${user}"

# generate final certificate
openssl x509 -req -in certs/${user}.csr -CA ~/.minikube/ca.crt -CAkey ~/.minikube/ca.key -CAcreateserial -out certs/${user}.crt -days 500
```

Note: this dev.crt is created manually by accessing minikube's local CA file. The preffered way is 
to use [k8s cert management system](https://v1-9.docs.kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)

### check privileges
```bash
# check rolebindings created
kubectl get rolebinding --all-namespaces

# check privileges
kubectl auth can-i get pods --namespace=stage --as frodo
yes
kubectl auth can-i get pods --namespace=prod --as frodo
yes
kubectl auth can-i create pods --namespace=stage --as frodo
yes
kubectl auth can-i create pods --namespace=prod --as frodo
no
```

## grant and deny
```bash
# create user
user=frodo
# create rb frodo.view.stage
kubectl create rolebinding ${user}.view.stage --user=${user} --role=view-stage-role --namespace=stage
# create rb frodo.edit.stage
kubectl create rolebinding ${user}.edit.stage --user=${user} --role=edit-stage-role --namespace=stage
# create rb frodo.view.prod
kubectl create rolebinding ${user}.view.prod --user=${user} --role=view-prod-role --namespace=prod

# find out namespaces where frodo's rolebindings exist
kubectl get rolebinding --all-namespaces | grep frodo
# delete them
kubectl delete $(kubectl get rolebinding --all-namespaces -o name | grep frodo) --namespace=stage
kubectl delete $(kubectl get rolebinding --all-namespaces -o name | grep frodo) --namespace=prod
```


## CSR
- [TLS bootstrapping @medium](https://medium.com/@toddrosner/kubernetes-tls-bootstrapping-cf203776abc7)
- [yet another TLS article](https://jenciso.github.io/personal/manage-tls-certificates-for-kubernetes-users)


### Links
- [k8s auth docs](https://kubernetes.io/docs/admin/authentication/)
- [EBay k8s auth overview (deprecated)](https://github.com/eBay/Kubernetes/blob/master/docs/user-guide/kubeconfig-file.md)
- [RBAC configuration](https://docs.bitnami.com/kubernetes/how-to/configure-rbac-in-your-kubernetes-cluster/#step-5-test-the-rbac-rule)

### TODO
- [certificate signing request](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)
