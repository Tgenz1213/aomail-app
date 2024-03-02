# Utilisez l'image officielle Python comme image parente
FROM python:3.11

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier des dépendances dans le répertoire de travail
COPY ./requirements.txt .

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste du code source de votre application dans le répertoire de travail
COPY . .

# Copy the entrypoint script and set it as the entrypoint
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["entrypoint.sh"]

# Commande pour démarrer votre application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
