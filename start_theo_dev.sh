export BACKEND_PORT=8001
export FRONTEND_PORT=8081
export SERVER_FRONTEND_PORT=8080
export DB_PORT=5433
export ENV="theo"
export NODE_ENV="development"
export TOPIC_NAME="sub_new_mail"
export POSTGRES_USER="django_admin"
export POSTGRES_PASSWORD="OOycmlVX8mDHiY6pGyAztF5Hg2ZxsYUIayBKkjdY18Axp05EvnT2UuKuNnV76b6BVXfo6NXOguCZ9BNrfdF5AjSbP09w9bqisMo"
export POSTGRES_DB="mailassistantdb"

# Start the containers and build if necessary
docker compose -p ${ENV}_project up --build -d frontend_dev backend_dev

# Wait for the backend container to be running
container_name="${ENV}_project-backend_dev-1"

# Extract the ID of the Google renew subscription
ID=""
while [ -z "$ID" ]; do
  ID=$(docker exec -i $container_name crontab -l 2>/dev/null | grep 'crontab run' | awk -F 'run ' '{print $2}' | awk '{print $1}' | head -n 1)
  if [ -z "$ID" ]; then
    echo "No ID found. Retrying in 5 seconds..."
    sleep 5
  fi
done
echo "ID found: $ID"

# Get the absolute path of the script's directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Define the cron job with the log file located in the same directory as the script
CRON_JOB="0 3 * * * docker exec -i ${container_name} /usr/local/bin/python /app/manage.py crontab run $ID >> $SCRIPT_DIR/aomail-cron.log 2>&1"

# Add cron job if it doesn’t already exist
(crontab -l | grep -F "$CRON_JOB") && echo "Cron job already exists" || (crontab -l; echo "$CRON_JOB") | crontab -
