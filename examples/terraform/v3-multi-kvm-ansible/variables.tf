# Prefixes for virtual machines
variable "prefix" {
  type    = string
  default = "tf-v2-"
}

# Path for save virtual machines
variable "pool_path" {
  type    = string
  default = "/var/lib/libvirt/"
}

# Cloud-init image config
variable "image" {
  type = object({
    name = string
    url  = string
  })
}

# Virtual machine config
variable "vm" {
  type = object({
    cpu     = number
    ram     = number
    disk    = number
    bridge  = string
    ip_base = number
  })
}

# mac addresses
variable "macs" {
  type = list(string)
}