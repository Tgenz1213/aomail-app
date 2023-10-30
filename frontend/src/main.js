import { createApp } from 'vue'
import App from './App.vue'
import './assets/css/tailwind.css'
import router from './router';
//import GoogleLogin from 'vue3-google-login';
import axios from 'axios';
//import { createOAuthClient } from '@volverjs/auth-vue';

axios.defaults.headers.post['Cross-Origin-Opener-Policy'] = "same-origin-allow-popups";

const app = createApp(App);

app.use(router);

/*
app.use(GoogleLogin, {
    clientId: '900609376538-creikhrqkhuq82i7dh9lge3sg50526pi.apps.googleusercontent.com',
});*/

/*
const authClient = createOAuthClient({
    url: 'https://accounts.google.com',
    clientId: '900609376538-creikhrqkhuq82i7dh9lge3sg50526pi.apps.googleusercontent.com',
    scopes: 'https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/contacts.readonly https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email openid https://www.googleapis.com/auth/contacts.other.readonly',
  });

app.use(authClient, { global: true });*/

app.mount('#app');
