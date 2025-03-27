# Secrets needed for workflow 

`SSH_SERVER` - VPS server address

`SSH_USER` - VPS user

`SSH_PRIVATE_KEY` - private key for VPS user on VPS server

`WORK_DIR` - patch for deploy

# Base config for server

1. Create deploy folder:

```bash
sudo mkdir -p /var/www
```

2. Set permissions for folder:


```bash
sudo chown -R <username>:<usergroup> /var/www
```
