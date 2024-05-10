export BACKEND_PORT=8001
export FRONTEND_PORT=8081
export DB_PORT=5433
export ENV="theo"
export TOPIC_NAME="sub_new_mail"


# Create the folder backend/media/pictures if it doesn't exist
if [ ! -d "backend/media" ]; then
    mkdir -p backend/media/pictures
fi

docker compose -p theo_project up --build
#docker compose -p theo_project build --no-cache && docker compose -p theo_project up