export BACKEND_PORT=8004
export FRONTEND_PORT=8084
export SERVER_FRONTEND_PORT=8080
export DB_PORT=5434
export ENV="augustin"
export NODE_ENV="development"
export TOPIC_NAME="sub_new_mail2"
export POSTGRES_USER="django_admin"
export POSTGRES_PASSWORD="admin@2"
export POSTGRES_DB="mailassistantdb"

# Start the containers and build if necessary
docker compose -p ${ENV}_project up --build -d frontend_dev backend_dev

# Define the cron job and add it if it doesn't exist
CRON_JOB="0 3 * * * docker exec -i ${ENV}_project-backend-1 /usr/local/bin/python /app/manage.py crontab run $ID"
(crontab -l | grep -F "$CRON_JOB") && echo "Cron job already exists" || (crontab -l; echo "$CRON_JOB") | crontab -
