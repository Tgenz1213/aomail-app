export BACKEND_PORT=8002
export FRONTEND_PORT=8082
export DB_PORT=5434
export ENV="augustin"
export TOPIC_NAME="sub_new_mail2"
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





# docker compose -p augustin_project up --build
# use this to force install reqs or delete backend instance
#docker compose -p augustin_project build --no-cache && docker compose -p augustin_project up

# Start the containers and build if necessary
docker compose -p augustin_project up --build -d


# Function to check if the container is healthy
check_container_health() {
  local container_name=$1
  local health=$(docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null)
  echo $health
}

# Wait for the backend container to be running
container_name="${ENV}_project-backend-1"

# Wait for the backend container to be healthy (if health check is configured)
if docker inspect --format='{{json .State.Health}}' "$container_name" 2>/dev/null | grep -q 'null'; then
  echo "$container_name does not have a health check configured."
else
  while [[ $(check_container_health "$container_name    ") != "healthy" ]]; do
    echo "Waiting for $container_name to be healthy..."
    sleep 5
  done
  echo "$container_name is healthy."
fi

# Extract the ID of the Google renew subscription
ID=$(docker exec -i $container_name crontab -l | grep 'crontab run' | awk -F 'run ' '{print $2}' | awk '{print $1}')
echo $ID



# documentation: https://crontab.guru/
CRON_JOB="* * * * * docker exec -i ${ENV}_project-backend-1 /usr/local/bin/python /app/manage.py crontab run $ID"
(crontab -l | grep -F "$CRON_JOB") && echo "Cron job already exists" || (crontab -l; echo "$CRON_JOB") | crontab -
