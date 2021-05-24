# Kubernetes - Day 1

## Installing minikube
Minikube setup let's you create a light-weight Kubernetes cluster in your laptop/desktop.  Minikube doesn't require high-end machines and it works in Windows, Mac OS and Linux.

### Minikube requires Docker, hence let's install Docker Community Edition
```
sudo yum install -y yum-utils
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce

sudo systemctl enable docker && sudo systemctl start docker
```

Regular user(non-admin) user's will not have permission to issue docker commands by default, the below
steps will added the 'user' into docker group.   Any user who is part of docker group will gain minimal root permissions to play with docker commands.
```
sudo usermod -aG docker user
sudo su user
```

### Let's download and install minikube as shown below
```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

For detailed instruction, refer the below official page
```
https://minikube.sigs.k8s.io/docs/start/
```

### Make sure minikube is in path. As regular user, type the below command
```
which minikube
```

In case, minikube is already in path, you will get the below out
```
/usr/local/bin/minikube
```

In case, you are not getting the above output then make sure you type the below as a regular user(non-root)
Edit the /home/user/.bashrc and append the below line at the end of the file
```
export PATH=/usr/local/bin:$PATH
```

In order to apply the recently added path settings, you need to run
```
source /home/user/.bashrc
```

### Starting minkube as regular user (non-root)
```
minikube start --driver=docker
```

### Install kubectl to work with the K8s cluster
```
curl -LO https://dl.k8s.io/release/v1.21.0/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin
```

### Test if kubectl is able to communicate with Minikube cluster as regular user
```
kubectl get nodes
kubectl get pods -n kube-system
```

### How Kubernetes assigns same IP to all containers in a Pod
```
docker run -d --name pause --hostname pause k8s.gc.io/pause:3.2
docker run -d --name nginx --network=container:pause nginx:1.18
```

### Creating your first deployment
```
kubectl create deployment nginx --image=nginx:1.18
kubectl get deploy
```

### Scaling up the nginx deployment
```
kubectl scale deploy/nginx --replicas=4
kubectl scale deploy/nginx --replicas=6
```

### Scaling down the nginx deployment
```
kubectl scale deploy/nginx --replicas=2
kubectl scale deploy/nginx --replicas=0
```

### Listing all the user-plane pods
```
kubectl get pods
kubectl get pod
kubectl get po
```

### Listing pods in wide output format
```
kubectl get po -o wide
```

### Listing pods in watch mode
```
kubectl get po -o wide -w
```

### Getting inside a pod
```
kubectl exec -it mypod bash
```

### Listing all the deployments in default namespace
```
kubectl get deployments
kubectl get deployment
kubectl get deploy
```

### Listing all the replicasets in default namespace
```
kubectl get replicasets
kubectl get replicaset
kubectl get rs
```

### Listing all the pods in all namespaces
```
kubectl get po --all-namespaces
```

### Listing all resources in all namespaces
```
kubectl get all --all-namespaces
```

### Finding more details about deploy,rs,po
```
kubectl describe deploy/nginx
kubectl describe rs/nginx-replicaset-name 
kubectl describe pod/pod-name
```
