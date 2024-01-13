import { createApp } from 'vue'
import App from './App.vue'
import './assets/css/tailwind.css'
import router from './router';  // Change this line
import axios from 'axios';
//import GoogleLogin from 'vue3-google-login';
//import { createOAuthClient } from '@volverjs/auth-vue';

axios.defaults.headers.post['Cross-Origin-Opener-Policy'] = "same-origin-allow-popups";

const app = createApp(App);

app.use(router);

app.mount('#app');