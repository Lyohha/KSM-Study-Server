prefix = "tf-test-2-"

pool_path = "/var/terraform/"

image = {
  name = "ubuntu-focal"
  url  = "https://cloud-images.ubuntu.com/releases/24.04/release/ubuntu-24.04-server-cloudimg-amd64.img"
  # Change link to local image file
  # url  = "images/ubuntu-24.04-server-cloudimg-amd64.img"
}

vm = {
  bridge  = "virbr0"
  cpu     = 1
  disk    = 10 * 1024 * 1024 * 1024
  ram     = 3072
  ip_base = 210
}

macs = [
  "52:54:00:4d:d9:60",
  "52:54:00:4d:d9:61",
  "52:54:00:4d:d9:62",
]