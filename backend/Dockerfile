# Base stage for building the application
FROM python:3.11 AS base
WORKDIR /app
RUN apt-get update && apt-get install -y cron
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY . .

# Development mode
FROM base AS development
ENTRYPOINT ["entrypoint.sh"]
EXPOSE 8000

# Production mode
FROM base AS production
ENTRYPOINT ["entrypoint.sh"]
EXPOSE 8000
