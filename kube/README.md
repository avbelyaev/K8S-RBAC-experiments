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

### Secrets

data-field of secret contains base64ed string
```bash
echo -n 'victoria' | base64
# paste base64ed string into secret.yaml
```

### Port-forwarding

We can connect our machine directly to port of certain pod! Its very convenient for debugging 

Remember! Local->Remote

```bash
# connect localhost:8080 to remote pod's :5000
kubectl port-forward pod/flask 8080:5000

# we can also connect to deployment the same way
```

# TODO notes on HELM


# Helm

Download & unpack:
```bash
mkdir ~/helm
tar -zxvf helm-v2.0.0-linux-amd64.tgz -C helm 

# render templates
helm install --debug --dry-run ./mychart


Error: release failed: namespaces "default" is forbidden: User "system:serviceaccount:kube-system:default" cannot get namespaces in the namespace "default"

kubectl create sa --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy -n kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
```


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
