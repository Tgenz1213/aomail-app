export BACKEND_PORT=8003
export FRONTEND_PORT=8083
export DB_PORT=5435
export ENV="jean"
# TODO: add TOPIC_NAME="sub_new_mail_jean" in google project

# Create the folder backend/media/pictures if it doesn't exist
if [ ! -d "backend/media" ]; then
    mkdir -p backend/media/pictures
fi
# Create the folder backend/MailAssistant/controllers/trees if it doesn't exist
if [ ! -d "backend/MailAssistant/controllers/trees" ]; then
    mkdir -p backend/MailAssistant/controllers/trees
fi

docker compose -p jean_project up --build
# use this to force install reqs or delete backend instance
#docker compose -p jean_project build --no-cache && docker compose -p jean_project up