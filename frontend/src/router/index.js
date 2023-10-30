import { createRouter, createWebHistory } from 'vue-router';
import { isUserAuthenticated } from '@/services/authService';
import Login from '@/views/Login.vue';
import SignUp from '@/views/SignUpV1.vue';
import SignUpPart2 from '@/views/SignUpV1_part2.vue';
import Home from '@/views/HomeV15.vue';
import New from '@/views/NewV4.vue';
import Rules from '@/views/RulesV2.vue';
import Settings from '@/views/SettingsV1.vue';

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
    path: '/signup_part2',
    name: 'signup_part2',
    component: SignUpPart2,
  },
  {
    path: '/home',
    name: 'home',
    meta: { requiresAuth: true },
    component: Home,
  },
  {
    path: '/new',
    name: 'new',
    meta: { requiresAuth: true },
    component: New,
  },
  {
    path: '/rules',
    name: 'rules',
    meta: { requiresAuth: true },
    component: Rules,
  },
  {
    path: '/settings',
    name: 'settings',
    meta: { requiresAuth: true },
    component: Settings,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = isUserAuthenticated();

  if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!isAuthenticated) {
          next({ name: 'login' });
      } else {
          next();
      }
  } else {
      next();
  }
});

export default router;
