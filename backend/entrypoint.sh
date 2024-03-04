#!/bin/sh

# Wait for the database to be ready
echo "Waiting for database to be ready..."
# Add a loop here to check for DB readiness if necessary

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Start the Django application
echo "Starting Django application..."
exec "$@"