# Aomail Web Application

## Quick Setup

### Ask Théo HUBERT for your credentials
1) Setup the tunel with Wireguard by giving your public key
2) Setup VSC and wsl to connect to the server via ssh
3) Run your assigned script: ./start_{username}_dev.sh


# Debugging database migrations errors
```bash
sudo rm -fr backend/aomail/migrations
docker exec -it {username}_project-backend-1 python manage.py makemigrations --empty aomail
./start_{username}_dev.sh
```

# Adding a New Subdomain
1) Add the subdomain in the DNS server.
2) Add the subdomain in Nginx Proxy Manager.
3) Open the required port: `sudo ufw allow PORT_NUMBER` 
4) Update vue.config.js: Add the new domain to the list of allowedHosts.

## Tech Stack

- Frontend: Vue
- Backend: Django
- Containerization: Docker
- Web Server: Nginx

## Launch in Production

```bash
./build.sh
```

## Run in development

```bash
./start_{username}_dev.sh
```
