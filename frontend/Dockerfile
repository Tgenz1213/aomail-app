FROM node:lts-alpine AS build

WORKDIR /app

COPY package*.json ./
COPY .eslintrc.js ./

RUN npm install
RUN npm run build