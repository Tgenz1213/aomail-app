export BACKEND_PORT=8001
export FRONTEND_PORT=8081
export DB_PORT=5433
export ENV="theo"
export TOPIC_NAME="sub_new_mail"
export POSTGRES_USER="django_admin"
export POSTGRES_PASSWORD="admin@2"
export POSTGRES_DB="mailassistantdb"

docker compose -p theo_project up