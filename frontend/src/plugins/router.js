import { createRouter, createWebHistory } from "vue-router";
import store from '@/store';

const routes = [
  {
    path: '',
    name: 'home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/admin-dashboard',
    name: 'admin-dashboard',
    component: () => import('@/views/dashboard.vue'),
    meta: { 
      requiresAuth: true,
      role: 'admin'
    }
  },
  {
    path: '/professional-dashboard',
    name: 'professional-dashboard',
    component: () => import('@/views/ProfessionalDashboard.vue'),
    meta: { 
      requiresAuth: true,
      role: 'professional'
    }
  },
    {
      path: '/:pathMatch(.*)*',
      beforeEnter: (to, from, next) => {
        // Handle both login and signup query parameters
        if (to.query.login === 'true' || to.query.signup === 'true') {
          next();
        } else {
          next();
        }
      }
    }
  ]


const router = createRouter({
    routes,
    history: createWebHistory(),
})

router.beforeEach(async (to, from, next) => {

  const accessToken = localStorage.getItem('access_token');
  const user = JSON.parse(localStorage.getItem('user'));
  
  if (accessToken && !store.getters['module1/isAuthenticated']) {
    try {
      store.commit('module1/SET_TOKENS', {
        accessToken,
        refreshToken: localStorage.getItem('refresh_token')
      });
      store.commit('module1/SET_USER', user);

      await store.dispatch('module1/fetchUserProfile');
    } catch (error) {
      console.error('Failed to restore auth state:', error);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      return next({ path: '/', query: { login: 'true' }});
    }
  }

  const isAuthenticated = store.getters['module1/isAuthenticated'];
  const userRole = store.getters['module1/userRole'];

  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      return next({ path: '/', query: { login: 'true' }});
    }

    if (to.meta.role && to.meta.role !== userRole) {
      if (userRole === 'admin') {
        return next({ name: 'admin-dashboard' });
      } else if (userRole === 'professional') {
        return next({ name: 'professional-dashboard' });
      } else {
        return next({ path: '/' });
      }
    }
  }

  // Handle automatic redirects for authenticated users
  if (isAuthenticated && to.path === '/') {
    if (userRole === 'admin') {
      return next({ name: 'admin-dashboard' });
    } else if (userRole === 'professional') {
      return next({ name: 'professional-dashboard' });
    }
  }

  next();
});


export default router;