# Use the official Node.js image as the base image
FROM node:lts-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# Install the project dependencies
RUN npm install

# Copy the rest of your project's files into the working directory
#COPY . .

# Expose the port used by the Vue.js development server
# EXPOSE 8080

# Command to start the application in development mode
#CMD ["npm", "run", "serve"]
