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
  count = length(var.macs)

  name           = "${var.prefix}-${count.index}-root"
  pool           = libvirt_pool.pool.name
  base_volume_id = libvirt_volume.image.id
  size           = var.vm.disk
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


resource "libvirt_cloudinit_disk" "commoninit" {
  count = length(var.macs)

  name           = "commoninit_${count.index}.iso"
  pool           = libvirt_pool.pool.name
  user_data = templatefile("config-templates/cloud_init.tftpl", { })
  network_config = templatefile("config-templates/network_config.tftpl", { ip_address = var.vm.ip_base + count.index, mac_address = var.macs[count.index] })
}