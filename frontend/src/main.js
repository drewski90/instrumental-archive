import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAuthStore } from './stores/auth'
import router from './router'
import App from './App.vue'
import api from './lib/api'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap'

api.interceptors.request.use((config) => {
  const auth = useAuthStore()

  if (auth.authHeader) {
    config.headers = config.headers || {}
    config.headers.Authorization = auth.authHeader
  }

  return config
})

const app = createApp(App)

app.config.globalProperties.$api = api

app.use(createPinia())
app.use(router)

app.mount('#app')
