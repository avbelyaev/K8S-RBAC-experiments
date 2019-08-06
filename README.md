# Kubernetes RBAC/ABAC experiments

Basic K8S info - at `/kube` dir

Launching minikube and configuring RBAC/ABAC - at `kube/config/{abac|rbac}` dir


### Flask notes

- connect via Mongo Explorer (Intellij Idea plugin) with the following creds:
  - uri: `localhost:27017`
  - creds: `admin/admin`
  - auth database: `kube`
  - mechanism: `scram`

- example request to save json from body:
```bash
curl -X POST http://18.209.211.193:8080/any -H 'content-type: application/json' -d '{"hello": "world"}'
```
