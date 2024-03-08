import { createRouter, createWebHistory } from 'vue-router'
import TitleMenu from '../views/TitleMenu.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: TitleMenu,
      children: [
        {
          path: '/',
          name: 'home',
          component: () => import('../views/HomeView.vue')
        },
        {
          path: '/user',
          name: 'user',
          component: () => import('../views/UserCenter.vue')
        },
        {
          path: '/help',
          name: 'help',
          component: () => import('../views/HelpView.vue')
        },
        {
          path: '/example',
          name: 'example',
          component: () => import('../views/ExampleView.vue')
        },
        {
          path: '/404',
          name: 'notFound',
          component: () => import('../views/NotFoundPageView.vue')
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/404'
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.path !== '/login' && !isAuthenticated()) {
    next('/login')
  } else {
    next()
  }
})

function isAuthenticated() {
  const token = localStorage.getItem('access_token')
  console.log('是否授权', token)
  if (token === null || token === undefined || token.length === 0) {
    return false
  } else {
    return true
  }
}

export default router
