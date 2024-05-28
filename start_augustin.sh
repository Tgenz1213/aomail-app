export BACKEND_PORT=8002
export FRONTEND_PORT=8082
export DB_PORT=5434
export ENV="augustin"
export TOPIC_NAME="sub_new_mail2"
export POSTGRES_USER="django_admin"
export POSTGRES_PASSWORD="admin@2"
export POSTGRES_DB="mailassistantdb"

docker compose -p augustin_project up --build