resource "libvirt_pool" "pool" {
  name = "${var.prefix}pool"
  type = "dir"
  target {
    path = "${var.pool_path}${var.prefix}pool"
  }
}

resource "libvirt_volume" "image" {
  name   = var.image.name
  format = "qcow2"
  pool   = libvirt_pool.pool.name
  source = var.image.url
}

resource "libvirt_volume" "root" {
  name           = "${var.prefix}root"
  pool           = libvirt_pool.pool.name
  base_volume_id = libvirt_volume.image.id
  size           = var.vm.disk
}

resource "libvirt_domain" "vm" {
  name   = "${var.prefix}master_2"
  memory = var.vm.ram
  vcpu   = var.vm.cpu

  network_interface {
    bridge         = var.vm.bridge
    wait_for_lease = true
    mac           = "52:54:00:4d:d9:6f"
  }

  disk {
    volume_id = libvirt_volume.root.id
  }

  qemu_agent = true
  autostart  = true

  cloudinit = libvirt_cloudinit_disk.commoninit.id

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
  name           = "commoninit.iso"
  pool           = libvirt_pool.pool.name
  user_data      = data.template_file.user_data.rendered
  network_config = data.template_file.network_config.rendered
}