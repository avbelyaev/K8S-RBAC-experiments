# RBAC

Start up
```bash
# minikube version <= 0.25
minikube start --extra-config=apiserver.Authorization.Mode=RBAC 
```


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

# generate keys
```bash
# create key
openssl genrsa -out dev.key 2048

# create certificate sign request (csr)
# CN = username, O = group
openssl req -new -key dev.key -out dev.csr  -subj "/CN=dev-user/O=dev-group"

# generate final certificate
openssl x509 -req -in dev.csr -CA ~/.minikube/ca.crt -CAkey ~/.minikube/ca.key -CAcreateserial -out dev.crt -days 500
```

Note: this dev.crt is created manually by accessing minikube's local CA file. The preffered way is 
to use [k8s cert management system](https://v1-9.docs.kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)

# create users, namespaces, contexts, roles, rolebindings
```bash
# credentials name "dev-user" must be equal to CN from certificate from above
kubectl config set-credentials dev-user --client-certificate=dev.crt --client-key=dev.key

# create namespaces (dev/prod)
kubectl create -f ns-stage.yaml
kubectl create -f ns-prod.yaml

# create context == (cluster,user,ns)
kubectl config set-context dev-context --cluster=minikube --namespace=stage-ns --user=dev-user
```

# grant roles to user with rolebindings
```bash
# create roles (reader/admin)
kubectl create -f role-reader.yaml 
kubectl create -f role-admin.yaml

# bind user "dev-user" to role "admin-role" at namespace "dev-ns" (developer is and admin in his namespace)
# same as create -f rolebinding-dev-user-dev-ns.yaml
kubectl create rolebinding dev-user-stage-ns-binding --user=dev-user --role=admin-role --namespace=stage-ns
 
# bind "dev-user" to "reader-role" at namespace "prod-ns" (dev can only read at production)
# same as create -f rolebinding-dev-user-prod-ns.yaml
kubectl create rolebinding dev-user-prod-ns-binding --user=dev-user --role=reader-role --namespace=prod-ns
```


# check privileges
```bash
kubectl auth can-i get pods --namespace=dev-ns --as dev-user
yes
kubectl auth can-i get pods --namespace=prod-ns --as dev-user
yes
kubectl auth can-i create pods --namespace=dev-ns --as dev-user
yes
kubectl auth can-i create pods --namespace=prod-ns --as dev-user
no
```


# configure admin
```bash
# generate admin key & cert
openssl genrsa -out admin.key 2048
openssl req -new -key admin.key -out admin.csr  -subj "/CN=admin-user/O=admin-group"
openssl x509 -req -in admin.csr -CA ~/.minikube/ca.crt -CAkey ~/.minikube/ca.key -CAcreateserial -out admin.crt -days 500

#

```

# Links
- [k8s auth docs](https://kubernetes.io/docs/admin/authentication/)
- [EBay k8s auth overview (deprecated)](https://github.com/eBay/Kubernetes/blob/master/docs/user-guide/kubeconfig-file.md)
- [RBAC configuration](https://docs.bitnami.com/kubernetes/how-to/configure-rbac-in-your-kubernetes-cluster/#step-5-test-the-rbac-rule)

# TODO
- [certificate signing request](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)
