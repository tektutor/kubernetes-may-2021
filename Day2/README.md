# Kubernetes Commands 

### Make sure nginx image is loaded onto worker1 and worker2 in case of Multinode setup
```
docker load -i nginx.tar
```

### Verify if the nginx:1.18 docker image is loaded correctly
```
docker images
```

### To create NodePort service (External Service)
```
kubectl create deploy nginx --image=nginx:1.18
kubectl scale deploy/nginx --replicas=4
kubectl expose deploy nginx --type=NodePort --port=80
```

### Finding the nodeport service details
```
kubectl get svc/nginx
kubectl describe svc/nginx
```

### Accessing the NodePort Service from. 3-Node Setup
```
curl http://master:30218
curl http://worker1:30218
curl http://worker2:30218
```
You need to find the nodeport in your K8s cluster and replace 30218 with your nodeport.

### Accessing the NodePort Service from Minikube setup 
```
minikube ssh
minikube ip
curl http://localhost:30218
```
You need to find the nodeport in your K8s cluster and replace 30218 with your nodeport.


### To create Cluster service (Internal Service)
```
kubectl create deploy nginx --image=nginx:1.18
kubectl scale deploy/nginx --replicas=4
kubectl expose deploy nginx --type=ClusterIP --port=80
```
