import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import HomeView from '../views/HomeView.vue'
import LibraryView from '../views/LibraryView.vue'
import UploadView from '../views/UploadView.vue'

const routes = [
  { path: '/', component: HomeView },

  { path: '/library', component: LibraryView },

  {
    path: '/upload',
    component: UploadView,
    meta: { requiresAuth: true }
  },

  {
    path: "/login",
    component: () => import("@/views/LoginView.vue")
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/* =======================================================
   Global auth guard
======================================================= */
router.beforeEach((to, from, next) => {

  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/login')
  } else {
    next()
  }

})

export default router
