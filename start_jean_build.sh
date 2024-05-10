export BACKEND_PORT=8003
export FRONTEND_PORT=8083
export DB_PORT=5435
export ENV="jean"

# Create the folder backend/media/pictures if it doesn't exist
if [ ! -d "backend/media" ]; then
    mkdir -p backend/media/pictures
fi

docker compose -p jean_project up --build