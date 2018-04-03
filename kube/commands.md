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
kubectl run hello-flask --image=flask:1 --image-pull-policy=Never

#expose deployment as service
kubectl expose deployment hello-minikube --type=NodePort
```


# run info
```bash
kubectl get pod
kubectl describe pods hello-minikube-6bd65c5cb7-676hf
kubectl describe {deployment/service} hello-world
```


# stop/remove resource
```bash
kubectl delete pod hello-minikube-6bd65c5cb7-676hf
kubectl delete service,pod,deployment hello-minikube
```

