# Use the official Node.js image as the base image
FROM node:lts-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# Install the project dependencies and TypeScript
RUN npm install && \
    npm install -g typescript