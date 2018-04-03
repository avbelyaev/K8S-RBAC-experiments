# start up
```bash
minikube --vm-driver=virtualbox start
```


# append local docker
```bash
eval $(minikube docker-env)
```


# cluster info
```bash
kubectl cluster-info === minikube ip
```


# run
```bash
kubectl run hello-minikube --image=k8s.gcr.io/echoserver:1.4 --port=8080

#image from local
docker build -t flask:1 .
kubectl run hello-flask --image=flask:1 --port=5000 --image-pull-policy=Never

#expose deployment as service
kubectl expose deployment hello-flask --type=NodePort

#get service ip:port and check it
curl $(minikube service hello-flask --url)/hello
```


# run from file
```bash
kubectl create -f file.yaml

#update changes in file
kubectl apply -f file.yml
```


# run info
```bash
kubectl get {pod/service/deployment}
kubectl get pods -l app=flask
kubectl describe pods hello-minikube-6bd65c5cb7-676hf
kubectl describe {deployment/service} hello-world
```


# stop/remove resource
```bash
kubectl delete pod hello-minikube-6bd65c5cb7-676hf
kubectl delete service,pod,deployment hello-minikube
```

# Notes
- to pull images from local docker registry, after minikube start, run `eval $(minikube docker-env)` 
and all images should be launched with flag `--image-pull-policy=Never`
