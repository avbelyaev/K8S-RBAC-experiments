
# Namespaces
A "context" defines a named (cluster,user,namespace) tuple

RBAC:
- Roles and ClusterRoles: Consist of rules. The difference is the scope: 
in a Role, the rules are applicable to a single namespace, whereas a ClusterRole is cluster-wide
- Subjects:
  - User Accounts: These are global, and meant for humans or processes living outside the cluster.
  - Service Accounts: This kind of account is namespaced and meant for intra-cluster processes running inside pods, which want to authenticate against the API
  - Groups: This is used for referring to multiple accounts.
- RoleBindings and ClusterRoleBindings: Just as the names imply, these bind subjects to roles (i.e. the operations a given user can perform).
As for Roles and ClusterRoles, the difference lies in the scope



# generate keys
```bash
# create key
openssl genrsa -out dev.key 2048

# create certificate sign request (csr)
# CN = username, O = group
openssl req -new -key dev.key -out dev.csr  -subj "/CN=developer/O=dev-group"

# generate final certificate
openssl x509 -req -in dev.csr -CA ~/.minikube/ca.crt -CAkey ~/.minikube/ca.key -CAcreateserial -out dev.crt -days 500
```

# create users and contexts in k8s api server
```bash
kubectl config set-credentials dev-user --client-certificate=dev.crt --client-key=dev.key

# create namespaces and then
# create context == (cluster,user,ns)
kubectl config set-context dev-context --cluster=minikube --namespace=dev-ns --user=dev-user

# create role
# create
```
