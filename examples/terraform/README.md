# Install Terraform on Ubuntu

```bash
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

# Fix errors with access to KVM virtual disks

```bash
sudo echo "security_driver = \"none\"" | sudo tee -a /etc/libvirt/qemu.conf > /dev/null
```

# Using local Cloud-init image

In file `terraform.tfvars` uncomment line 9 and comment line 7

# Run Terraform

```bash
sudo terraform apply
```

# Destroy Terraform infrastructure

```bash
sudo terraform destroy
```