path = 'config/wireguard/clients/'

path_t = path + 'cloud-vms/'

real_server = '<server_domain>'

j = 1
while j <= 20:
    file_content = False
    with open(path_t + str(j) + '/wg0.conf', "r") as file:
        file_content = file.read()
    
    file_content = file_content.replace('192.168.1.20', real_server)

    with open(path_t + str(j) + '/wg0.conf', "w") as file:
        file.write(file_content)
    j += 1


path_t = path + 'kubernetes-vms/'

j = 1
while j <= 20:
    file_content = False
    with open(path_t + str(j) + '/wg0.conf', "r") as file:
        file_content = file.read()
    
    file_content = file_content.replace('192.168.1.20', real_server)

    with open(path_t + str(j) + '/wg0.conf', "w") as file:
        file.write(file_content)
    j += 1


path_t = path + 'cloud-nonwg-vms/'

j = 1
while j <= 20:
    file_content = False
    with open(path_t + str(j) + '/wg0.conf', "r") as file:
        file_content = file.read()
    
    file_content = file_content.replace('192.168.1.20', real_server)

    with open(path_t + str(j) + '/wg0.conf', "w") as file:
        file.write(file_content)
    j += 1


path_t = path + 'docker-vms/'

j = 1
while j <= 20:
    file_content = False
    with open(path_t + str(j) + '/wg0.conf', "r") as file:
        file_content = file.read()
    
    file_content = file_content.replace('192.168.1.20', real_server)

    with open(path_t + str(j) + '/wg0.conf', "w") as file:
        file.write(file_content)
    j += 1


path_t = path + 'gitlab-vms/'

j = 1
while j <= 20:
    file_content = False
    with open(path_t + str(j) + '/wg0.conf', "r") as file:
        file_content = file.read()
    
    file_content = file_content.replace('192.168.1.20', real_server)

    with open(path_t + str(j) + '/wg0.conf', "w") as file:
        file.write(file_content)
    j += 1
    