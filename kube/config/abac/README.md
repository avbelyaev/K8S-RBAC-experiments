# ABAC

Start up
```bash
minikube start --extra-config=apiserver.Authorization.Mode=RBAC --extra-config=apiserver.AuthorizationPolicyFile=auth_policy.jsonl
```

# generate keys



# Links
- [k8s ABAC](https://kubernetes.io/docs/admin/authorization/abac/)
- [example config](https://github.com/kubernetes/kubernetes/blob/master/pkg/auth/authorizer/abac/example_policy_file.jsonl)
- [cert revoke](https://stackoverflow.com/questions/36919323/how-to-revoke-signed-certificate-in-kubernetes-cluster)

- [setting up certs](https://stackoverflow.com/questions/37786244/what-username-does-the-kubernetes-kubelet-use-when-contacting-the-kubernetes-api)
- [accessing api server](http://k8s.uk/accessing-kubernetes-apiserver.html)


# TODO
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
