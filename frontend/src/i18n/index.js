import { createI18n } from 'vue-i18n';
import en from './en.json';
import fr from './fr.json';
/*import { fetchWithToken } from '../router/index.js';


/*
const messages = {
  en: en,
  fr: fr,
};

const fallbackLocale = 'en';

// Méthode pour récupérer le langage de l'utilisateur depuis le serveur
async function getUserLanguage() {
  try {
    const response = await fetchWithToken('http://localhost:9000/MailAssistant/user/preferences/get_language/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    return data.language || fallbackLocale;

  } catch (error) {
    console.error('Error fetching user language:', error);
    return fallbackLocale;
  }
}

const i18n = createI18n({
  // locale: browserLanguage,
  locale: await getUserLanguage(),
  fallbackLocale: fallbackLocale,
  messages,
});

export default i18n;*/

// Configuration des messages
const messages = {
  français: fr,
  english: en,
};

// Création de l'instance i18n avec la configuration
const i18n = createI18n({
  locale: 'english', // Langue par défaut
  fallbackLocale: 'français', // Langue de secours
  messages,
});

export default i18n;