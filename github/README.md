# Quick start GitHub self-hosted Runner

For GitHub Runner needed create another user and set permissions. 

1. Create user for work GitHub Runner

:exclamation: Don`t change username for current work

```bash
sudo useradd -m ghuser
```

2. Create work folder

```bash
mkdir -p /home/ghuser/actions-runner/_work
```

3. Change permissions for new folder

```bash
sudo chown :docker -R /home/ghuser
sudo chmod 774 -R /home/ghuser
```

4. Add current user in docker group

```bash
sudo usermod -a -G docker <username>
```

5. Fill config env in docker-compose.yml file (lines 9-11)

:exclamation: Runner work only for one repository. For work in another repository need change config or start more runners.

6. Start GitHuv runner

:exclamation: Start command changed for add docker group in runner for start actions in docker containers

```bash
export GH_DOCKER_GROUP_ID=$(getent group docker | cut -d: -f3) && docker compose up -d
```