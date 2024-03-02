import { createRouter, createWebHistory } from 'vue-router';
import { isUserAuthenticated } from '@/services/authService';
import Login from '@/views/UserLogin.vue';
import SignUp from '@/views/SignUpV1.vue';
import SignUpPart2 from '@/views/SignUpV1_part2.vue';
import Home from '@/views/HomeV15.vue';
import New from '@/views/NewV4.vue';
import Answer from '@/views/AnswerV1.vue';
import Rules from '@/views/RulesV2.vue';
import Settings from '@/views/SettingsV1.vue';
import Search from '@/views/SearchV2.vue';
import ReplyLater from '@/views/ReplyLaterV1.vue';
import NotFound from '@/views/NotFound.vue';
import { API_BASE_URL } from '@/main';


async function fetchWithToken(url, options = {}) {
  const accessToken = localStorage.getItem('access_token');
  if (!options.headers) {
    options.headers = {};
  }
  if (accessToken) {
    options.headers['Authorization'] = `Bearer ${accessToken}`;
  }

  try {
    let response = await fetch(url, options);

    console.log("------------> DEBUG RESPONSE", response); // To delete after test (only Theo can delete)

    if (response.status == 401) {
      const refreshResponse = await fetch(`${API_BASE_URL}api/token/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ access_token: accessToken })
      });

      console.log("----------------> DEBUG", refreshResponse); // To delete after test (only Theo can delete)

      if (refreshResponse.ok) {
        const refreshData = await refreshResponse.json();
        const newAccessToken = refreshData.access_token;
        localStorage.setItem('access_token', newAccessToken);
        options.headers['Authorization'] = `Bearer ${newAccessToken}`;
        response = await fetch(url, options);
      } else {
        throw new Error('Unauthorized: Please log in again');
      }
    }
    // Access token is still valid
    // Handles other errors
    else {
      console.log("DEBUG 2", response); // To delete after test (only Theo can delete)
      return response.json();
    }

    // Failed to refresh the token
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    console.error('Error in fetchWithToken:', error.message);
    throw error;
  }
}

async function getBackgroundColor() {
  const response = await fetchWithToken(`${API_BASE_URL}user/preferences/bg_color/`);
  const bgColor = response.bg_color;
  localStorage.setItem('bgColor', bgColor);
}

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
    path: '/answer',
    name: 'answer',
    meta: { requiresAuth: true },
    component: Answer,
  },
  {
    path: '/search',
    name: 'search',
    meta: { requiresAuth: true },
    component: Search,
  },
  {
    path: '/reply_later',
    name: 'reply_later',
    meta: { requiresAuth: true },
    component: ReplyLater,
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
  },
  {
    path: '/:catchAll(.*)',
    name: 'not-found',
    component: NotFound,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  // true if authenticated else false
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
export { fetchWithToken, getBackgroundColor };