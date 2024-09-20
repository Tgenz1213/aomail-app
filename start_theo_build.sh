export BACKEND_PORT=8001
export FRONTEND_PORT=8081
export SERVER_FRONTEND_PORT=8080
export DB_PORT=5433
export ENV="theo"
export NODE_ENV="development"
export TOPIC_NAME="sub_new_mail"
export POSTGRES_USER="django_admin"
export POSTGRES_PASSWORD="admin@2"
export POSTGRES_DB="mailassistantdb"

# Start the containers and build if necessary
docker compose -p ${ENV}_project up --build -d frontend_dev

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
