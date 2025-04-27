import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Login from '../views/Login.vue' // 你的登录页面

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    component: () => import('@/views/Dashboard.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/ads',
    redirect: '/ads/list',
    meta: { title: '广告管理' },
    children: [
      {
        path: 'list',
        component: () => import('@/views/ads/AdList.vue'),
        meta: { title: '我的广告' }
      },
      {
        path: 'api',
        component: () => import('@/views/ads/AdApi.vue'),
        meta: { title: '广告接口' }
      }
    ]
  },
  {
    path: '/account',
    component: () => import('@/views/Account/Account.vue'),
    meta: { title: '我的账户' ,
        requiresAuth: true
    }
  },
  {
    path: '/profile',
    component: () => import('@/views/Profile/Profile.vue'),
    meta: { title: '个人中心' ,
        requiresAuth: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const isAuthenticated = localStorage.getItem('currentUser')
    if (!isAuthenticated) {
      return next('/login')
    }
  }
  next()
})

export default router