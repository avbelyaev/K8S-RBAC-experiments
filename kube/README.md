### start up
```bash
minikube --vm-driver=virtualbox start
    
minikube stop
```


### append local docker
```bash
eval $(minikube docker-env)
```


### cluster info
```bash
kubectl cluster-info === minikube ip
```


## Basics
### run end expose
```bash
# create new deployment
kubectl run hello-minikube --image=k8s.gcr.io/echoserver:1.4 --port=8080

#image from local
docker build -t flask:1 .
kubectl run hello-flask --image=flask:1 --port=5000 --image-pull-policy=Never

#expose deployment as service (aka create new service)
kubectl expose deployment hello-flask --type=NodePort

#get service ip:port and check it
curl $(minikube service hello-flask --url)/hello
```


### run from file
```bash
kubectl create -f file.yaml

#update changes in file
kubectl apply -f file.yml
```


### info
```bash
kubectl get {pod/service/deployment}
kubectl get pods -l app=flask
kubectl describe pods hello-minikube-6bd65c5cb7-676hf
kubectl describe {deployment/service} hello-world

# logs
kubectl logs flask-pod-1337
# logs of all pods
kubectl logs -l app=flask

# port-forwarding to localhost:9000
kubectl port-forward flask-pod-1337 9000:8080
```


### stop/remove resource
```bash
kubectl delete pod hello-minikube-6bd65c5cb7-676hf
kubectl delete service,pod,deployment hello-minikube
```


### namespaces and context
```bash
kubectl get namespace
kubectl create -f namespace-prod.yaml

kubectl config view
# define a context for the kubectl client to work in each namespace
kubectl config set-context dev --namespace=dev --cluster=minikube --user=minikube

#switch to dev namespace (current-context should be "dev")
kubectl config use-context dev

# open service that lays in a namespace prod
minikube --namespace=prod service flask-service --url
```

### ConfigMaps and Secrets

Config-map is a map that hold k-v pairs 

Config map example:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: conf-map
data:
  my-name: anthony
```

Secret is a 'config-map' for sensitive data, where value is a base64ed string

```bash
echo -n 'victoria' | base64
# paste base64ed string into secret.yaml

# or even easier:
kubectl create secret generic victoria-secret \
    --from-literal=name=anthony
    --from-literal=password=qwerty 
    --namespace my-namespace
```

In k8s resource descriptors they can be referenced in, for example, `env` section:
```yaml
env:
- name: MY_NAME
  valueFrom:
    configMapKeyRef:
      name: conf-map
      key: my-name
- name: MY_SECURED_PASSWORD
  valueFrom:
    secretKeyRef:
      name: victoria-secret
      key: my-pwd
```

### Port-forwarding

We can connect our machine directly to port of certain pod/svc/etc! Its very convenient for debugging 

Remember! Local->Remote

```bash
# connect localhost:8080 to remote pod's :5000
kubectl port-forward pod/my-flask 8080:5000
```

we can also connect to deployment/svc the same way

# Helm

- Package manager aka "brew for k8s"
- Deploy unit - __chart__ - set of params interpolated into k8s resource descriptor 
    - Search for charts with tag "postgres": `helm search postgres`
- Deploying a chart creates a __release__
- With Helm 2.x to deploy into cluster, you need "sudo-server" Tiller :) which deploys interpolated templates.
    - Tiller has been removed in Helm 3
- "Helm'ed" apps should only be managed by helm - touching them with kubectl may cause errors!!
   
- Installation:
```bash
mkdir ~/helm
tar -zxvf helm-v2.0.0-linux-amd64.tgz -C helm 

Error: release failed: namespaces "default" is forbidden: User "system:serviceaccount:kube-system:default" cannot get namespaces in the namespace "default"

kubectl create sa --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy -n kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
```

### List releases

- When using helm, you always talk to particular Tiller instance, thus in multi-ns clusters use flag `--tiller-namespace`
    - Tiller sits in `kube-system` ns by default
    - In case of deploying into `stage` ns, Tiller would sit in `stage-system` ns 
```bash
# list current releases in "stage" ns by connecting to Tiller at "stage-system" ns
helm ls --tiller-namespace stage-system

# list current state of components deployed in release "my-mongo"
helm status my-mongo --tiller-namespace stage-system
```

### Install, Upgrade & Rollback

- Find chart you want to install at <https://github.com/helm/charts>
- Override default values from chart
    - via `--set` flag: `$ helm ... --set "fullnameOverride=monga" ...`
    - via `values.yaml` file `helm install ... -f values.yaml ...`
    - the rightmost value wins
- Mutating commands (those that change smth) should be run with `--dry-run --debug` flags. In this case, Helm will 
interpolate templates, but wont apply them to cluster, so they can be reviewed one more time and only then be deployed
    - like this: `helm install --name my-mongo stable/mongodb --dry-run --debug`  

__Installing__:
```bash
helm install --name my-mongo \
        --tiller-namespace stage-system \
        --namespace stage \
        -f values.yaml \
        stable/mongodb
```

__Upgrading__:
- upgrading does not differ from installing: Helm passes chart alongside with params so it does not pass parameters
from previous installation. Thus to upgrade release, __you should pass same params that were used for installation__.

E.g. upgrading release from above with version (`mongodb-13.37` - only digits are used) of chart:
```bash
helm upgrade --name my-mogno \
        --tiller-namespace stage-system \
        --namespace stage \
        -f values.yaml \
        stable/mongodb \
        --version 13.37
```


__Rolling__:
- See history of releases for particular release "my-mongo"
```bash
helm history my-mongo --tiller-namespace stage-system
#REVISION  UPDATED                   STATUS      CHART             DESCRIPTION
#1         Fri Aug 31 15:17:57 2019  SUPERSEDED  mongodb-2.1.10  Install complete
#2         Fri Aug 31 15:21:08 2019  DEPLOYED    mongodb-2.1.10  Upgrade complete
#3         Fri Aug 31 16:05:01 2019  DEPLOYED    mongodb-13.37   Upgrade complete
```
- to rollback, upgrade to prev revision: `helm rollback my-mongo 2`

### Delete

Deleting with `helm delete my-mongo` only deletes k8s resources from cluster but not the release.
To remove both resources and release, use `helm delete --purge my-mongo` 

# Notes

### Troubleshooting
```bash
# in case of trouble do
minikube stop
minikube delete
minikube start

# in case of fire do
rm -rf ~/.minikube
rm -rf ~/.kube
```

- Pull images from local registry: exec `eval $(minikube docker-env)`. 
all images should be launched with flag `--image-pull-policy=Never` or with `spec.containers.imagePullPolicy: Never` in specification.
If it did not work, try rebuild image and u r OK
- Make sure linux version is downloaded with `curl -LO https://storage.googleapis.com... linux/amd64/kubectl`, not darwin
