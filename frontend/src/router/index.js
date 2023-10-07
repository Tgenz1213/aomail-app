import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/views/Login.vue';
import SignUp from '@/views/SignUpV1.vue';
import Home from '@/views/HomeV15.vue';

const routes = [
  {
    path: '/',
    name: 'login',
    component: Login,
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUp,
  },
  {
    path: '/home',
    name: 'home',
    component: Home,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router;
