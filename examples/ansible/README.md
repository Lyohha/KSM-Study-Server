# Install Ansible

```bash
sudo apt-get install ansible
```

# Check connect to hosts from file

```bash
sudo ansible all -i hosts.yml -m ping
```

# Execute playbook

```bash
sudo ansible-playbook -i hosts.yml ansible_main.yml
```
