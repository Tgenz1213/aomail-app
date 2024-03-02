# Utilisez l'image officielle Node.js comme image parente
FROM node:lts-alpine

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier 'package.json' et 'package-lock.json' (si disponible)
COPY package*.json ./

# Installez les dépendances du projet
RUN npm install

# Copiez le reste des fichiers de votre projet dans le répertoire de travail
COPY . .

# Exposez le port utilisé par le serveur de développement Vue.js
EXPOSE 8080

# Commande pour démarrer l'application en mode développement
CMD ["npm", "run", "serve"]