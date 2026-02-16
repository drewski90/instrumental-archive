import { defineStore } from 'pinia'
import api from '@/lib/api'

export const useAuthStore = defineStore('auth', {

  state: () => ({
    username: sessionStorage.getItem('username'),
    password: sessionStorage.getItem('password'),
    loading: false
  }),

  getters: {
    isAuthenticated: (s) => !!(s.username && s.password),
    authHeader: (s) =>
      s.username ? "Basic " + btoa(`${s.username}:${s.password}`) : null
  },

  actions: {

    async login(username, password) {
      this.loading = true
      try {
        const token = btoa(`${username}:${password}`)

        await api.post('/login', null, {
          headers: { Authorization: `Basic ${token}` }
        })

        this.username = username
        this.password = password

        sessionStorage.setItem('username', username)
        sessionStorage.setItem('password', password)

      } finally {
        this.loading = false
      }
    },

    logout() {
      this.username = null
      this.password = null
      sessionStorage.removeItem('username')
      sessionStorage.removeItem('password')
    }
  }
})
