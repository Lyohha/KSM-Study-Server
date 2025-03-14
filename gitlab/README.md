# Starting sequence
1. Create folders config, data, logs
2. Start GitLab by command:

```bash
docker compose --profile gitlab up -d 
```

3. Create GitLab Runner in GitLab Settings, obtain token and insert token in docker-compose.yml file on line 66.

4. Start GitLab Runner Register by command:

```bash
docker compose --profile register up -d
```

5. Start GitLab Runner:

```bash
docker compose --profile main up -d 
```

6. Profit. You get worked GitLab with Runner.

# Add more runners
1. Create new volume for new GitLab Runner. 

2. Change volume in GitLab Runner register in line 63 in docker-compose.yml file.

3. Change runner name in line 73 in docker-compose.yml file.

4. Create GitLab Runner in GitLab Settings, obtain token and insert token in docker-compose.yml file on line 66.

5. Start GitLab Runner Register by command:

```bash
docker compose --profile register up -d
```

6. Create copy of block GitLab Runner in docker-compose.yml from lines 45 to 55 and insert copy in end of containers list.
7. Change container name. 
8. Change Runner volume in analog line 53.
9. Start GitLab Runner:

```bash
docker compose --profile main up -d 
```
10. Profit. You add additional Runner.