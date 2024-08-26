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

if [ ! -d "backend/media/labels" ]; then
    mkdir -p backend/media/labels
fi

# docker compose -p augustin_project up --build
# use this to force install reqs or delete backend instance
#docker compose -p augustin_project build --no-cache && docker compose -p augustin_project up

# Start the containers and build if necessary
docker compose -p ${ENV}_project up --build -d

# Wait for the backend container to be running
container_name="${ENV}_project-backend-1"

# Extract the ID of the Google renew subscription
ID=""
while [ -z "$ID" ]; do
  ID=$(docker exec -i $container_name crontab -l | grep 'crontab run' | awk -F 'run ' '{print $2}' | awk '{print $1}')
  if [ -z "$ID" ]; then
    echo "No ID found. Retrying in 5 seconds..."
    sleep 5
  fi
done
echo "ID found: $ID"

# Define the cron job and add it if it doesn't exist
CRON_JOB="0 3 * * * docker exec -i ${ENV}_project-backend-1 /usr/local/bin/python /app/manage.py crontab run $ID"
(crontab -l | grep -F "$CRON_JOB") && echo "Cron job already exists" || (crontab -l; echo "$CRON_JOB") | crontab -


# Run migrations
docker exec -it "${container_name}" python manage.py makemigrations
docker exec -it "${container_name}" python manage.py migrate