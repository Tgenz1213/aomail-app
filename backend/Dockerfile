# ChatGPT: add a clean documentation as a senior Python developer with 20 years of experience with Docker

# Utilisez l'image officielle Python comme image parente
FROM python:3.11

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier des dépendances dans le répertoire de travail
COPY ./requirements.txt .

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste du code source de votre application dans le répertoire de travail
#COPY . .

# Copy the entrypoint script and set it as the entrypoint
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["entrypoint.sh"]

COPY ./creds/keys/key.pem /etc/ssl/private/
COPY ./creds/keys/cert.pem /etc/ssl/certs/

# I think none of these have ever been ran
#CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:8000", "--cert-file", "/etc/ssl/certs/cert.pem", "--key-file", "/etc/ssl/private/key.pem"]

#EXPOSE 8000
#CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "MailAssistant_project.asgi:application"]

# Ajouter les taches planifiées
#CMD ["python", "manage.py", "crontab", "add"]

# Commande pour démarrer votre application
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
