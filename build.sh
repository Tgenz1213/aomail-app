export BACKEND_PORT=8002
export FRONTEND_PORT=8082
export SERVER_FRONTEND_PORT=80
export DB_PORT=5435
export ENV="app"
export NODE_ENV="production"
export TOPIC_NAME="app_prod_sub_new_mail"
export POSTGRES_USER="django_admin"
export POSTGRES_PASSWORD="admin@2"
export POSTGRES_DB="mailassistantdb"

# Start the containers and build if necessary
docker compose -p ${ENV}_prod up --build -d frontend_prod backend_prod

# Define the cron job and add it if it doesn't exist
CRON_JOB="0 3 * * * docker exec -i ${ENV}_prod-backend /usr/local/bin/python /app/manage.py crontab run $ID"
(crontab -l | grep -F "$CRON_JOB") && echo "Cron job already exists" || (crontab -l; echo "$CRON_JOB") | crontab -
