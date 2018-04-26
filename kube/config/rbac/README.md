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
minikube start --extra-config=apiserver.Authorization.Mode=RBAC 
```

### generate keys
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

### create users, namespaces, contexts
```bash
# name "frodo" for credentials must be equal to CN from certificate
user=frodo
kubectl config set-credentials ${user} --client-certificate=certs/${user}.crt --client-key=certs/${user}.key 

# create namespaces (stage/prod)
kubectl create -f ns-stage.yaml
kubectl create -f ns-prod.yaml

# create context == (cluster,user,ns)
kubectl config set-context minikube-${user}-stage --cluster=minikube --user=${user} --namespace=stage-ns
```

### create roles and grant roles to user via rolebindings
```bash
# create roles and rolebindings on stage
kubectl create -f view-stage-role-rb.yaml
kubectl create -f edit-stage-role-rb.yaml 
# crete roles and rolebindings on prod
kubectl create -f view-prod-role-rb.yaml 
kubectl create -f edit-prod-role-rb.yaml 


# OR create rolebindings manually
# bind user "frodo" to role "view-stage-role" at namespace "stage-ns" (frodo can view-only on stage)
# and do same to grant another roles (edit-stage-role) to somebody
user=frodo
kubectl create rolebinding view-stage-rb --user=${user} --role=view-stage-role --namespace=stage-ns
```


### check privileges
```bash
kubectl auth can-i get pods --namespace=stage-ns --as frodo
yes
kubectl auth can-i get pods --namespace=prod-ns --as frodo
yes
kubectl auth can-i create pods --namespace=stage-ns --as frodo
yes
kubectl auth can-i create pods --namespace=prod-ns --as frodo
no
```


### Links
- [k8s auth docs](https://kubernetes.io/docs/admin/authentication/)
- [EBay k8s auth overview (deprecated)](https://github.com/eBay/Kubernetes/blob/master/docs/user-guide/kubeconfig-file.md)
- [RBAC configuration](https://docs.bitnami.com/kubernetes/how-to/configure-rbac-in-your-kubernetes-cluster/#step-5-test-the-rbac-rule)

### TODO
- [certificate signing request](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)
