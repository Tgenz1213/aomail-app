# Use the official Node.js image as the base image
FROM node:lts-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./
COPY .eslintrc.js ./

# Install the project dependencies
RUN npm install