# Repository for MailAssistant

## Quick Setup

```bash
# Install WSL (Debian distribution)
wsl --install -d Debian

# Update system and install necessary tools
sudo apt update
sudo apt install git
sudo apt install npm
sudo apt install postgresql

# replace prodvX by the current version
git clone -b prodvX https://your_pseudo:token@github.com/Teh45/MailAssistant.git

pip install -r requirements.txt
```

## Database Configuration
# Start PostgreSQL service and configure the database
```sql
sudo service postgresql start
sudo -u postgres psql
CREATE DATABASE mailassistantdb;
CREATE USER django_admin WITH PASSWORD 'admin@2';
GRANT ALL PRIVILEGES ON DATABASE mailassistantdb TO django_admin;
\c mailassistantdb
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO django_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO django_admin;
GRANT ALL ON SCHEMA public TO django_admin;
```

## Starting the Servers
# Grant execution permissions and start servers
```bash
chmod +x start_servers.sh
sudo ./start_servers.sh
```

## Testing Gmail API Authentication
To test the authentication for the Gmail API, you can use the following `curl` command by replacing `ACCESS_TOKEN` with your actual access token:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:9000/MailAssistant/api/authenticate-service
```