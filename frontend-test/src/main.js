import { createApp } from 'vue'
import './styles.css';
/*
import Navbar from './components/Navbar.vue'

const app = createApp({});
app.component('Navbar', Navbar);
app.mount('#app');*/

import Home from './Home.vue'
import HomeV2 from './HomeV2.vue'
import HomeV3 from './HomeV3.vue'
import HomeV4 from './HomeV4.vue'
import HomeV5 from './HomeV5.vue'
import HomeV6 from './HomeV6.vue'
import HomeV7 from './HomeV7.vue'
import HomeV8 from './HomeV8.vue'
import HomeV9 from './HomeV9.vue'
import HomeV10 from './HomeV10.vue'
import HomeV11 from './HomeV11.vue'
import HomeV12 from './HomeV12.vue'
import HomeV13 from './HomeV13.vue'
import New from './New.vue'
import New1 from './NewV1.vue'
import New2 from './NewV2.vue'
import New3 from './NewV3.vue'
import Search from './SearchV1.vue'
import Rules from './RulesV1.vue'
import Settings from './SettingsV1.vue'
import Contact from './Contact.vue'

const app = createApp({});
app.component('home', Home);
app.component('home2', HomeV2);
app.component('home3', HomeV3);
app.component('home4', HomeV4);
app.component('home5', HomeV5);
app.component('home6', HomeV6);
app.component('home7', HomeV7);
app.component('home8', HomeV8);
app.component('home9', HomeV9);
app.component('home10', HomeV10);
app.component('home11', HomeV11);
app.component('home12', HomeV12);
app.component('home13', HomeV13);
app.component('new', New);
app.component('new1', New1);
app.component('new2', New2);
app.component('new3', New3);
app.component('search', Search);
app.component('contact', Contact);
app.component('rules', Rules);
app.component('settings', Settings);
app.mount('#app');
