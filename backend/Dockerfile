# Use the official Python image as the base image
FROM python:3.11

# Install cron
RUN apt-get update && apt-get install -y cron

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create the folders backend/media/pictures and backend/media/labels if they don't exist
RUN mkdir -p backend/media/pictures backend/media/labels

# Copy the entrypoint script and set it as the entrypoint
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copy the application code into the container
COPY . .

# Set the entrypoint script
ENTRYPOINT ["entrypoint.sh"]

# Expose the port the app runs on
EXPOSE 8000
