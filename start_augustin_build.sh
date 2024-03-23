export BACKEND_PORT=8002
export FRONTEND_PORT=8082
export DB_PORT=5434
export ENV="augustin"
export TOPIC_NAME="sub_new_mail2"

docker compose -p augustin_project up --build