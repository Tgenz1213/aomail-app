# Use the official Python image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# COPY . .

# Copy the entrypoint script and set it as the entrypoint
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["entrypoint.sh"]

# TODO: remove
# Copy SSL certificates
COPY ./creds/keys/key.pem /etc/ssl/private/
COPY ./creds/keys/cert.pem /etc/ssl/certs/
