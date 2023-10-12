import { createApp } from 'vue'
import App from './App.vue'
import './assets/css/tailwind.css'
import router from './router';
import GoogleLogin from 'vue3-google-login';
import axios from 'axios';

axios.defaults.headers.post['Cross-Origin-Opener-Policy'] = "same-origin-allow-popups";

const app = createApp(App);

app.use(router);

app.use(GoogleLogin, {
    clientId: '900609376538-creikhrqkhuq82i7dh9lge3sg50526pi.apps.googleusercontent.com',
});

app.mount('#app');
