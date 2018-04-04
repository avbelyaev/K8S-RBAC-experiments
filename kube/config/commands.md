
# Namaspaces
A "context" defines a named (cluster,user,namespace) tuple


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
```
