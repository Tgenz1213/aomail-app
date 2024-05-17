import { createApp } from 'vue'
import App from './App.vue'
import './assets/css/tailwind.css'
import router from './router';
import axios from 'axios';
import i18n from './i18n'; 

// Define the API base URL globally
export const BASE_URL = `https://${process.env.VUE_APP_ENV}.aomail.ai/`;
export const API_BASE_URL = `https://${process.env.VUE_APP_ENV}.aomail.ai/MailAssistant/`;

axios.defaults.headers.post['Cross-Origin-Opener-Policy'] = "same-origin-allow-popups";

const app = createApp(App);

app.use(router);
app.use(i18n);

app.mount('#app');