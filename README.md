<pre>
 ______   ______   __    __   ______   __   __        
/\  __ \ /\  __ \ /\ "-./  \ /\  __ \ /\ \ /\ \       
\ \  __ \\ \ \/\ \\ \ \-./\ \\ \  __ \\ \ \\ \ \____  
 \ \_\ \_\\ \_____\\ \_\ \ \_\\ \_\ \_\\ \_\\ \_____\ 
  \/_/\/_/ \/_____/ \/_/  \/_/ \/_/\/_/ \/_/ \/_____/                                                 
</pre>

# Aomail: 🤖 Ao helps users to classify their emails

**Working**
- ⌚ Email and response generation
- 📑 Auto classification & summary
- 🔗 Multi accounts in 1 app

**Development**
- 🔍 Search response among emails

## Quick Setup

### Ask Théo HUBERT for your credentials
1) Setup the tunel with Wireguard by giving your public key
2) Setup VSC and wsl to connect to the server via ssh
3) Run your assigned script: start_username_build.sh


# DEBUGGING DATABASE MIGRATIONS ERROR
```bash
sudo rm -fr backend/aomail/migrations
docker exec -it augustin_project-backend-1 python manage.py makemigrations --empty aomail
./start_{theo}_build.sh
./start_{theo}_build.sh
```