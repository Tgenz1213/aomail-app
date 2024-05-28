export BACKEND_PORT=8001
export FRONTEND_PORT=8081
export DB_PORT=5433
export ENV="theo"
export TOPIC_NAME="sub_new_mail"
export POSTGRES_USER="django_admin"
export POSTGRES_PASSWORD="admin@2"
export POSTGRES_DB="mailassistantdb"


# Create the folder backend/media/pictures if it doesn't exist
if [ ! -d "backend/media" ]; then
    mkdir -p backend/media/pictures
fi

# Create the folder backend/MailAssistant/controllers/trees if it doesn't exist
if [ ! -d "backend/MailAssistant/controllers/trees" ]; then
    mkdir -p backend/MailAssistant/controllers/trees
fi

docker compose -p theo_project up --build
# use this to force install reqs or delete backend instance
#docker compose -p theo_project build --no-cache && docker compose -p theo_project up