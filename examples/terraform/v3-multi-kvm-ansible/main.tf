resource "libvirt_pool" "pool" {
  name = "${var.prefix}_pool"
  type = "dir"
  target {
    path = "${var.pool_path}${var.prefix}_pool"
  }
}

resource "libvirt_volume" "image" {
  name   = var.image.name
  format = "qcow2"
  pool   = libvirt_pool.pool.name
  source = var.image.url
}

resource "libvirt_volume" "root" {
  count = length(var.macs)

  name           = "${var.prefix}_${count.index}_root"
  pool           = libvirt_pool.pool.name
  base_volume_id = libvirt_volume.image.id
  size           = var.vm.disk
}

resource "tls_private_key" "ssh_key" {
  count = length(var.macs)
  algorithm = "ED25519"
}

resource "libvirt_domain" "vm" {
  count = length(var.macs)

  name   = "${var.prefix}_master_${count.index}"
  memory = var.vm.ram
  vcpu   = var.vm.cpu

  network_interface {
    bridge         = var.vm.bridge
    wait_for_lease = true
    mac           = var.macs[count.index]
  }

  disk {
    volume_id = libvirt_volume.root[count.index].id
  }

  qemu_agent = true
  autostart  = true

  cloudinit = libvirt_cloudinit_disk.commoninit[count.index].id

  console {
    type        = "pty"
    target_port = "0"
    target_type = "serial"
  }
  console {
    type        = "pty"
    target_type = "virtio"
    target_port = "1"
  }
}

data "template_file" "user_data" {
  template = file("${path.module}/cloud_init.cfg")
}

data "template_file" "network_config" {
  template = file("${path.module}/network_config.cfg")
}

resource "libvirt_cloudinit_disk" "commoninit" {
  count = length(var.macs)

  name           = "commoninit_${count.index}.iso"
  pool           = libvirt_pool.pool.name
  user_data = templatefile("${path.module}/config-templates/cloud_init.tftpl", { 
    ssh_private_key = replace(tls_private_key.ssh_key[count.index].private_key_openssh, "\n", "\\n"),
    ssh_public_key = replace(tls_private_key.ssh_key[count.index].public_key_openssh, "\n", "\\n"),
    ssh_auth_key = replace(tls_private_key.ssh_key[count.index].public_key_openssh, "\n", "\\n")
  })
  network_config = templatefile("${path.module}/config-templates/network_config.tftpl", { ip_address = var.vm.ip_base + count.index, mac_address = var.macs[count.index] })
}

resource "local_file" "private_key" {
  count = length(var.macs)
  content  = tls_private_key.ssh_key[count.index].private_key_openssh
  filename = "${path.module}/ansible/.ssh/id_rsa_${count.index}"
  file_permission = "0400"
}

resource "local_file" "public_key" {
  count = length(var.macs)
  content  = tls_private_key.ssh_key[count.index].public_key_openssh
  filename = "${path.module}/ansible/.ssh/id_rsa_${count.index}.pub"
  file_permission = "0400"
}

resource "local_file" "cloud_init_test" {
  count = length(var.macs)
  content  = templatefile("${path.module}/config-templates/cloud_init.tftpl", { 
    ssh_private_key = replace(tls_private_key.ssh_key[count.index].private_key_openssh, "\n", "\\n"),
    ssh_public_key = replace(tls_private_key.ssh_key[count.index].public_key_openssh, "\n", "\\n"),
    ssh_auth_key = replace(tls_private_key.ssh_key[count.index].public_key_openssh, "\n", "\\n")
  })
  filename = "${path.module}/cloud_init_test_${count.index}"
}


resource "local_file" "hosts" {
  filename = "${path.module}/ansible/hosts.yml"
  content = templatefile("${path.module}/config-templates/hosts.tftpl", { vms = libvirt_domain.vm, path = path.module })

  provisioner "local-exec" {
    command = "ANSIBLE_CONFIG=${path.module}/ansible/ansible.cfg ansible-playbook ${path.module}/ansible/ansible_main.yml"
  }
}