# Base stage for building the application
FROM node:lts-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Development mode
FROM base AS development
EXPOSE 8080
CMD ["npm", "run", "serve"]

# Production mode
FROM base AS build
ARG VUE_APP_ENV
ARG VUE_APP_BASE_URL
ARG VUE_APP_API_BASE_URL
RUN npm run build

FROM nginx:alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
