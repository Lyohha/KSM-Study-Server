# Quick create virtual machine
## Download image
### Ubuntu 24.04
```bash
sudo wget -P ./ https://cloud-images.ubuntu.com/releases/24.04/release/ubuntu-24.04-server-cloudimg-amd64.img
```
## Quick start command

### Create disk with OS
```bash
sudo qemu-img create -F qcow2 -b ./ubuntu-24.04-server-cloudimg-amd64.img -f qcow2 ./base.qcow2 5G
```

### Generate MAC Addres
```bash
echo $(printf '52:54:00:%02x:%02x:%02x' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)))
```

### Create metadata file
```bash
sudo touch meta-data
```

### Create disk with configurations
:exclamation: Before use create metadata file and config files :arrow_down:
```bash
cloud-localds -v --network-config=network-config ./vm01-seed.qcow2 user-data meta-data
```

### Create Virtual Machine
```bash
sudo virt-install --connect qemu:///system --virt-type kvm --name vm01 --ram 2048 --vcpus=2 --os-variant ubuntu24.04 --disk path=./base.qcow2,device=disk --disk path=./vm01-seed.qcow2,device=disk --import --network network=default,model=virtio,mac=52:54:00:XX:XX:XX --noautoconsole
```

### Create Virtual Machine With Custom Network Bridge
:exclamation: Before using need create new brdige in KVM by xml file
```bash
sudo virt-install --connect qemu:///system --virt-type kvm --name vm01 --ram 2048 --vcpus=4 --os-variant ubuntu24.04 --disk path=./base.qcow2,device=disk --disk path=./vm01-seed.qcow2,device=disk --import --network bridge=nat1,model=virtio,mac=52:54:00:XX:XX:XX --noautoconsole
```

### List of virtual machines
```bash
virsh list
```

### Connect to virtual machine
```bash
virsh console vm01
```

### Remove Virtual Machine
```bash
virsh destroy vm01
virsh undefine vm01
```

### Fix Nameserver in virtual machine
```bash
sudo echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null
```

## Config for create virtual machine
### File: network-config 
#### Default
```
ethernets:
    eth001:
        addresses:
        - 192.168.122.21/24
        dhcp4: false
        gateway4: 192.168.122.1
        match:
            macaddress: 52:54:00:XX:XX:XX 
        nameservers:
            addresses:
            - 1.1.1.1
            - 8.8.8.8
        set-name: eth001
version: 2
```

#### For bridge:
```
ethernets:
    eth001:
        addresses:
        - 192.168.1.21/24
        dhcp4: false
        gateway4: 192.168.1.1
        match:
            macaddress: 52:54:00:XX:XX:XX 
        nameservers:
            addresses:
            - 1.1.1.1
            - 8.8.8.8
        set-name: eth001
version: 2
```

### File: user-data
```
#cloud-config
hostname: vm01
manage_etc_hosts: true
users:
  - name: student
    sudo: ALL=(ALL) NOPASSWD:ALL
    groups: users, admin, student
    home: /home/student
    shell: /bin/bash
    lock_passwd: false
ssh_pwauth: true
disable_root: false
chpasswd:
  list: |
    student:student
  expire: false
```

# Network configs for VM Utility

:exclamation: Before use VM Utility need fix IP addreses in configs.

## Technic
`Wireguard Server IP`: 10.0.1.1/24

`Wireguard IP for proxy in local nginx`: 10.0.1.2/24

## Students
`Wireguard IP's`: 192.168.1.2-100-100 /24 

## Cloud
`Local IP's`: 192.168.1.101-120 /24

`Wireguard IP's`: 10.0.1.101-120 /24

## Clound Not WG
`Local IP's`: 192.168.1.121-140 /24

## Docker
`Local IP's`: 192.168.1.141-160 /24

`Wireguard IP's`: 10.0.1.141-160 /24

## Kubernetes
`Local IP's`: 192.168.1.161-180 /24

`Wireguard IP's`: 10.0.1.161-180 /24

## GitLab
`Local IP's`: 192.168.1.181-200 /24

`Wireguard IP's`: 10.0.1.181-200 /24

