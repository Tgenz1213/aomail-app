import { createApp } from 'vue'
import './styles.css';
/*
import Navbar from './components/Navbar.vue'

const app = createApp({});
app.component('Navbar', Navbar);
app.mount('#app');*/
import HomeV13 from './HomeV13.vue'
import New3 from './NewV3.vue'
import Search from './SearchV1.vue'
import Rules from './RulesV1.vue'
import Settings from './SettingsV1.vue'

const app = createApp({});
app.component('home13', HomeV13);
app.component('new3', New3);
app.component('search', Search);
app.component('rules', Rules);
app.component('settings', Settings);
app.mount('#app');
