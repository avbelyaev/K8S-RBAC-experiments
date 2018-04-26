# ABAC

Start up
```bash
minikube start \
        --extra-config=apiserver.Authorization.Mode=ABAC \
        --extra-config=apiserver.Authentication.TokenFile.TokenFile=auth_tokens.csv \
        --extra-config=apiserver.AuthorizationPolicyFile=auth_policy.jsonl

```

### generate keys
```bash
# create key
openssl genrsa -out dev.key 2048

# create certificate sign request (csr)
# CN = username, O = group
openssl req -new -key dev.key -out dev.csr  -subj "/CN=dev-user"

# generate final certificate
openssl x509 -req -in dev.csr -CA ~/.minikube/ca.crt -CAkey ~/.minikube/ca.key -CAcreateserial -out dev.crt -days 500
```

Note: this dev.crt is created manually by accessing minikube's local CA file. The preffered way is 
to use [k8s cert management system](https://v1-9.docs.kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)

### create users, namespaces, contexts
```bash
# credentials name "dev-user" must be equal to CN from certificate from above
kubectl config set-credentials dev-user --client-certificate=dev.crt --client-key=dev.key

# create namespaces (dev/prod)
kubectl create -f ns-stage.yaml
kubectl create -f ns-prod.yaml

# create context == (cluster,user,ns)
kubectl config set-context dev-context --cluster=minikube --namespace=stage-ns --user=dev-user
```



### Links
- [k8s ABAC](https://kubernetes.io/docs/admin/authorization/abac/)
- [example config](https://github.com/kubernetes/kubernetes/blob/master/pkg/auth/authorizer/abac/example_policy_file.jsonl)
- [cert revoke](https://stackoverflow.com/questions/36919323/how-to-revoke-signed-certificate-in-kubernetes-cluster)

- [setting up certs](https://stackoverflow.com/questions/37786244/what-username-does-the-kubernetes-kubelet-use-when-contacting-the-kubernetes-api)
- [accessing api server](http://k8s.uk/accessing-kubernetes-apiserver.html)
- [--extra-config=apiserver.XXX options](https://godoc.org/k8s.io/kubernetes/cmd/kube-apiserver/app/options#APIServer)


### TODO

{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"dev-user",    "namespace": "dev-ns",      "resource": "pods",             "readonly": false }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"dev-user",    "namespace": "dev-ns",      "resource": "deployments",      "readonly": false }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"dev-user",    "namespace": "dev-ns",      "resource": "services",         "readonly": false }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"dev-user",    "namespace": "dev-ns",      "resource": "secrets",          "readonly": true  }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"dev-user",    "namespace": "dev-ns",      "resource": "configmaps",       "readonly": true  }}

{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"dev-user",    "namespace": "prod-ns",      "resource": "pods",            "readonly": true }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"dev-user",    "namespace": "prod-ns",      "resource": "deployments",     "readonly": true }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"dev-user",    "namespace": "prod-ns",      "resource": "services",        "readonly": true }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"dev-user",    "namespace": "prod-ns",      "resource": "secrets",         "readonly": true }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"dev-user",    "namespace": "prod-ns",      "resource": "configmaps",      "readonly": true }}




{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"devops-user", "namespace": "dev-ns",      "resource": "pods",             "readonly": true }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"devops-user", "namespace": "dev-ns",      "resource": "deployments",      "readonly": true }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"devops-user", "namespace": "dev-ns",      "resource": "services",         "readonly": true }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"devops-user", "namespace": "dev-ns",      "resource": "secrets",          "readonly": true }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"devops-user", "namespace": "dev-ns",      "resource": "configmaps",       "readonly": true }}

{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"devops-user", "namespace": "prod-ns",      "resource": "pods",             "readonly": true }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"devops-user", "namespace": "prod-ns",      "resource": "deployments",      "readonly": true }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"devops-user", "namespace": "prod-ns",      "resource": "services",         "readonly": true }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"devops-user", "namespace": "prod-ns",      "resource": "secrets",          "readonly": true }}
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"devops-user", "namespace": "prod-ns",      "resource": "configmaps",       "readonly": true }}
