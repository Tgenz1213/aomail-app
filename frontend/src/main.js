import { createApp } from 'vue';
import App from './App.vue';
import './assets/css/tailwind.css';
import router from './router';
// import axios from 'axios';
import { createI18n } from 'vue-i18n';
import { ref } from 'vue';
import { fetchWithToken } from './router/index.js';
import messages from './i18n/index.js';


// API Base URLs
export const BASE_URL = `https://${process.env.VUE_APP_ENV}.aomail.ai/`;
export const API_BASE_URL = `https://${process.env.VUE_APP_ENV}.aomail.ai/MailAssistant/`;

// ================================================================
// Language Selection
// ================================================================
let languageSelected = ref('');

const fetchUserLanguage = async () => {
  const languages = ['french', 'american', 'german', 'russian', 'spanish', 'chinese', 'indian'];
  const storedLanguage = localStorage.getItem('language');

  if (storedLanguage && languages.includes(storedLanguage)) {
    languageSelected.value = storedLanguage;
    return;
  }

  const requestOptions = {
    headers: { 'Content-Type': 'application/json' },
    method: 'GET'
  };

  try {
    const url = `${API_BASE_URL}user/preferences/language/`;
    const response = await fetchWithToken(url, requestOptions);

    if (response.error) {
      console.log(response.error);
    } else if (response.language) {
      languageSelected.value = response.language;
      localStorage.setItem('language', languageSelected.value);
    }
  } catch (error) {
    console.log(error.message);
  }
};

await fetchUserLanguage();

// i18n Configuration
const i18n = createI18n({
  locale: languageSelected.value,
  fallbackLocale: 'english',
  messages,
});


// // Axios Configuration
// axios.defaults.headers.post['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups';

// ================================================================
// Create and Mount Vue App
// ================================================================
const app = createApp(App);

app.use(router);
app.use(i18n);
app.mount('#app');

export default i18n;
