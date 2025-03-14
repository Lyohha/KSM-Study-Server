from os import system, name
import os
import shutil
import json
import random
import shutil 


settings = {
    "count-cloud-vms": 5,
    "count-cloud-nonwg-vms": 5,
    "count-docker-vms": 5,
    "count-kubernetes-vms": 5,
    "count-gitlab-vms": 5,
}

vms = {
    1: 'cloud-vms',
    2: 'cloud-nonwg-vms',
    3: 'docker-vms',
    4: 'kubernetes-vms',
    5: 'gitlab-vms',
}

ip_start = {
    'cloud-vms': 100,
    'cloud-nonwg-vms': 120,
    'docker-vms': 140,
    'kubernetes-vms': 160,
    'gitlab-vms': 180,
}

ip_base = {
    'local': '192.168.1.',
    'wg': '10.0.1.',
}


def clrscr():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def read_vms_file(filename):
    path = 'config/server_controller/'
    try:
        with open(path + filename, "r") as file:
            config = json.load(file)
            file.close()
            return config
    except Exception as ex:
        print(ex)
        return {}
    

def save_vms_file(filename, config):
    path = 'config/server_controller/'
    try:
        with open(path + filename, "w") as file:
            json.dump(config, file)
            file.close()
            return config
    except Exception as ex:
        print(ex)
        return {}


def menu(items):
    index = 0

    while True:
        clrscr()
        i = 0
        while i < len(items):
            print(str(i + 1) + ".\t" + items[i])
            i += 1
        index = int(input())
        if index > 0 and index <= len(items):
            break

    return index


def vm_info(vm, id):
    while True:
        config = read_vms_file(vm + '.json')
        if not (str(id) in config):
            config[str(id)] = 'deleted'
        clrscr()
        print('VM Info')
        print('ID: ' + str(id))
        print('Virtaul Machines: ' + vm)
        print('Status: ' + config[str(id)])
        print('Local IP: ' + ip_base['local'] + str(ip_start[vm] + id))
        if vm != 'cloud-nonwg-vms':
            print('Wireguard IP: ' + ip_base['wg'] + str(ip_start[vm] + id))
        print()
        print('1. Deploy\t2. Start\t3. Stop\t\t4. Delete\t5. Back')
        # print('1.\tDeploy')
        # print('2.\tStart')
        # print('3.\tStop')
        # print('4.\tDelete')
        # print('5.\tBack')
        item = int(input())
        if item == 5:
            return
        if(item == 1):
            deploy_vm(vm, id)
        if(item == 2):
            start_vm(vm, id)
        if(item == 3):
            stop_vm(vm, id)
        if(item == 4):
            delete_vm(vm, id)


def update_vm_status(vm, id, status):
    config = read_vms_file(vm + '.json')
    print(config)
    config[str(id)] = status
    save_vms_file(vm + '.json', config)


def deploy_vm(vm, id):
    config_mac = read_vms_file('mac-' + vm + '.json')
    mac_address = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    config_mac[str(id)] = mac_address
    save_vms_file('mac-' + vm + '.json', config_mac)

    path = 'vms/' + vm + '-' + str(id)
    try:
        os.mkdir(path)
    except Exception as ex:
        None

    # Ubuntu 18.04 depricated version
    # os.system('qemu-img create -F qcow2 -b ./../../images/ubuntu-18.04-server-cloudimg-amd64.img -f qcow2 ./' + path + '/vm-disk.qcow2 5G')
    os.system('qemu-img create -F qcow2 -b ./../../images/ubuntu-24.04-server-cloudimg-amd64.img -f qcow2 ./' + path + '/vm-disk.qcow2 5G')

    with open(path + "/network-config", "w") as file:
        file.write("ethernets:\n")
        file.write("  eth001:\n")
        # file.write("    addresses: [192.168.1." + str(ip_start[vm] + id) + "]\n")
        file.write("    addresses:\n")
        file.write("    - 192.168.1." + str(ip_start[vm] + id) + "/24\n")
        file.write("    dhcp4: false\n")
        file.write("    gateway4: 192.168.1.100\n")
        file.write("    match:\n")
        file.write("      macaddress: " + mac_address + "\n")
        file.write("    nameservers:\n")
        file.write("      addresses: [192.168.1.100, 8.8.8.8, 1.1.1.1]\n")
        file.write("    set-name: eth001\n")
        file.write("version: 2\n")

    with open(path + "/user-data", "w") as file:
        file.write("#cloud-config\n")
        file.write("hostname: " + vm + "-" + str(id) + "\n")
        file.write("manage_etc_hosts: true\n")
        file.write("users:\n")
        file.write("  - name: student\n")
        file.write("    sudo: ALL=(ALL) NOPASSWD:ALL\n")
        file.write("    groups: users, admin\n")
        file.write("    home: /home/student\n")
        file.write("    shell: /bin/bash\n")
        file.write("    lock_passwd: false\n")
        file.write("ssh_pwauth: true\n")
        file.write("disable_root: false\n")
        file.write("chpasswd:\n")
        file.write("  list: |\n")
        file.write("    student:student\n")
        file.write("  expire: false\n")

        # file.write("\n")
        file.write("wireguard:\n")
        file.write("  interfaces:\n")
        file.write("    - name: wg0\n")
        file.write("      config_path: /etc/wireguard/wg0.conf\n")
        file.write("      content: |\n")
        with open('./config/wireguard/clients/' + vm + '/' + str(id) + '/wg0.conf', "r") as file_config:
            for line in file_config:
                file.write("        " + line)

    if os.path.exists(path + "/meta-data"):
        os.remove(path + "/meta-data")
    
    with open(path + "/meta-data", 'w') as file:
        pass

    os.system('cloud-localds -v --network-config=./vms/' + vm + "-" + str(id) + '/network-config ./vms/' + vm + "-" + str(id) + '/vm-config.qcow2 ./vms/' + vm + "-" + str(id) + '/user-data ./vms/' + vm + "-" + str(id) + '/meta-data')
    # os.system('cloud-localds -v --network-config=./vms/' + vm + "-" + str(id) + '/network-config ./vms/' + vm + "-" + str(id) + '/vm-config.qcow2 ./vms/' + vm + "-" + str(id) + '/user-data ./vms/' + vm + "-" + str(id) + '/meta-data ./vms/' + vm + "-" + str(id) + '/wireguard-config-data')

    # Dissabled by error of nameserver
    # if not (vm == 'cloud-nonwg-vms'):
        # os.system('virt-customize -a ' + path + '/vm-disk.qcow2 --network --update')
        # os.system('virt-customize -a ' + path + '/vm-disk.qcow2 --network --install wireguard')
        # os.system('virt-customize -a ' + path + '/vm-disk.qcow2 --network --install openresolv')
        # os.system('virt-customize -a ' + path + '/vm-disk.qcow2 --copy-in ' + './config/wireguard/clients/' + vm + '/' + str(id) + '/wg0.conf:/etc/wireguard/')

    update_vm_status(vm, id, 'deployed')
    input('Confirm')
    return


def start_vm(vm, id):
    config_mac = read_vms_file('mac-' + vm + '.json')
    if not (str(id) in config_mac):
        mac_address = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        config_mac[str(id)] = mac_address
        save_vms_file('mac-' + vm + '.json', config_mac)
    
    mac_address = config_mac[str(id)] 
    command = 'virt-install --connect qemu:///system --virt-type kvm --name ' + vm + '-' + str(id) + ' --ram 2048 --vcpus=2 --os-variant ubuntu24.04 --disk path=./vms/' + vm + "-" + str(id) + '/vm-disk.qcow2,device=disk --disk path=./vms/' + vm + "-" + str(id) + '/vm-config.qcow2,device=disk --import --network bridge=nat1,model=virtio,mac=' + mac_address + ' --noautoconsole'
    print(command)
    os.system(command)

    update_vm_status(vm, id, 'work')
    
    input('Confirm')
    return


def stop_vm(vm, id):

    os.system('virsh destroy ' + vm + '-' + str(id))
    os.system('virsh undefine ' + vm + '-' + str(id))

    update_vm_status(vm, id, 'stoped')
    return


def delete_vm(vm, id):
    path = 'vms/' + vm + '-' + str(id)
    shutil.rmtree(path)
    update_vm_status(vm, id, 'deleted')
    return


def vms_list(item):
    vm = vms[item + 1]
    count = settings['count-' + vm]

    while True:
        config = read_vms_file(vm + '.json')
        clrscr()
        print('Cloud VM`s')
        i = 0
        while i < count:
            if not (str(i + 1) in config):
                config[str(i + 1)] = 'deleted'
            info = str(i + 1) + ".\t" + config[str(i + 1)] + '\t\t'
            
            info = info + ip_base['local'] + str(ip_start[vm] + i) + '\t'
            if vm != 'cloud-nonwg-vms':
                info = info + ip_base['wg'] + str(ip_start[vm] + i) + '\t'
            print(info)
            i += 1

        print("0.\tBack")

        index = int(input())
        if index == 0:
            return
        if index > 0 and index <= count:
            vm_info(vm, index)


def main():
    while(True):
        clrscr()
        print('VM Controller')
        item = menu(['Cloud VM`s', 'Cloud non WG VM`s', 'Docker VM`s' 'Kubernetes VM`s', 'GitLab VM`s', 'Exit'])
        if item == 5:
            return
        vms_list(item)
        




main()