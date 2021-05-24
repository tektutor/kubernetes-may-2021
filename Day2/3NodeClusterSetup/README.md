### Common Installation Procedure for Master and Worker Nodes

### Kubernetes Pre-requisites
Disable Virtual Memory (swap parition)
```
swapoff -a
```
To permanently disable swap partition,  edit  the /etc/fstab file root user and comment the swap partition.
vim /etc/fstab
```
Comment out the entire line with the swap partition before saving the /etc/fstab file.

Disable SELINUX
```
setenforce 0
```
To permanently disable  SELINUX, you need to edit /etc/selinux/config file and change enforcing to disabled.

Configure the hostnames of master and all worker nodes
In Master Node
```
hostnamectl set-hostname master
```

In worker1 Node
```
hostnamectl  set-hostname worker1
```

In worker2 Node
```
hostnamectl set-hostnamme worker2
```

Append the IPAddresses of master, worker1 and worker2 as shown below in /etc/hosts files
```
192.168.254.129 master 
192.168.254.130 worker1
192.168.254.131 worker2
```

### Firewall configurations

#### Open Master Node Ports in firewall
```
firewall-cmd --permanent --add-port=6443/tcp
firewall-cmd --permanent --add-port=2379-2380/tcp
firewall-cmd --permanent --add-port=10250-10252/tcp
firewall-cmd --permanent --add-port=10255/tcp
firewall-cmd --permanent --add-masquerade
firewall-cmd --permanent --zone=trusted  --add-source=192.168.0.0/16 
modprobe br_netfilter
systemctl daemon-reload
systemctl restart firewalld
systemctl status firewalld
firewall-cmd --list-all
```


### Open Worker Node Ports in firewall
```
firewall-cmd --permanent --add-port=10250/tcp
firewall-cmd --permanent --add-port=30000-32767/tcp
firewall-cmd --permanent --add-masquerade
firewall-cmd --permanent --zone=trusted  --add-source=192.168.0.0/16 
modprobe br_netfilter
systemctl daemon-reload
systemctl restart firewalld
systemctl status firewalld
firewall-cmd --list-all
```

#### Install Docker CE
```
sudo yum install -y yum-utils
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-e
sudo usermod -aG docker user
```

### Configure Docker Engine to use systemd driver
vim /etc/docker/daemon.json

```
{
  "exec-opts": ["native-cgroupdriver=systemd"],
  "log-driver": "json-file",
  "logs-opts": {
     "max-size": "100m"
  },
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ]
}

mkdir -p /etc/systemd/system/docker.service.d
systemctl daemon-reload
sudo systemctl enable docker && sudo systemctl start docker
```


Configure IPTables to see bridge traffic
```
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system
```

### Install kubectl kubeadm and kubelet on Master & all worker nodes
```
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF

sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
```

### Configure kubelet
```
sudo vim /etc/sysconfig/kubelet
KUBELET_EXTRA_ARGS= --runtime-cgroups=/system//system.slice --kubelet-cgroups=/systemd/system.slice

sudo systemctl enable --now kubelet
```

### Bootstrapping Master Node
```
kubeadm init --pod-network-cidr=192.168.0.0/16


