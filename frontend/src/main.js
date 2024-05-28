import { createApp, ref } from 'vue';
import App from './App.vue';
import './assets/css/tailwind.css';
import router from './router';
import { createI18n } from 'vue-i18n';
import { fetchWithToken } from './router/index.js';
import messages from './i18n/index.js';

// =========================== API BASE URLS =========================== //
export const BASE_URL = `https://${process.env.VUE_APP_ENV}.aomail.ai/`;
export const API_BASE_URL = `https://${process.env.VUE_APP_ENV}.aomail.ai/MailAssistant/`;

// ==================== ALLOWED LANGUAGES AND THEMES =================== //
const languages = ['french', 'american', 'german', 'russian', 'spanish', 'chinese', 'indian'];
const themes = ['light', 'dark'];

// ========================== FETCH USER PREFERENCES ========================== //
const fetchUserPreference = async (endpoint, key, allowedValues) => {
  const storedValue = localStorage.getItem(key);

  if (storedValue && allowedValues.includes(storedValue)) {
    return storedValue;
  }

  const requestOptions = {
    headers: { 'Content-Type': 'application/json' },
    method: 'GET',
  };

  try {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetchWithToken(url, requestOptions);

    if (response.error) {
      console.log(response.error);
      return null;
    } else if (response[key]) {
      localStorage.setItem(key, response[key]);
      return response[key];
    }
  } catch (error) {
    console.log(error.message);
    return null;
  }
};

const initializePreferences = async () => {
  const currentUrl = window.location.href;

  if (
    currentUrl !== `${BASE_URL}` &&
    currentUrl !== `${BASE_URL}/signup` &&
    currentUrl !== `${BASE_URL}/signup_part2`
  ) {
    const language = await fetchUserPreference('user/preferences/language/', 'language', languages);
    languageSelected.value = language || 'english';
    await fetchUserPreference('user/preferences/theme/', 'theme', themes);
  }
};

// ======================== INITIALIZE PREFERENCES ======================== //
const languageSelected = ref('english');
const themeSelected = ref('light');
await initializePreferences();

// ============================ I18N CONFIGURATION ============================ //
const i18n = createI18n({
  locale: languageSelected.value,
  fallbackLocale: 'english',
  messages,
});

// ======================== CREATE AND MOUNT VUE APP ======================== //
const app = createApp(App);
app.use(router);
app.use(i18n);
app.mount('#app');

export default i18n;
