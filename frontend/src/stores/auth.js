import { defineStore } from 'pinia'
import api from '@/lib/api'

export const useAuthStore = defineStore('auth', {

  state: () => ({
    username: null,
    password: null,
    loading: false
  }),

  getters: {
    isAuthenticated: (s) => !!(s.username && s.password),
    authHeader: (s) => s.username? "Basic " + btoa(`${s.username}:${s.password}`): null
  },

  actions: {

    async login(username, password){

      this.loading = true

      try{
        const token = btoa(`${username}:${password}`)

        // verify credentials using auth header
        await api.post('/login', null, {
          headers: {
            Authorization: `Basic ${token}`
          }
        })

        // store credentials only after successful verification
        this.username = username
        this.password = password

      } finally {
        this.loading = false
      }
    },

    logout(){
      this.username = null
      this.password = null
    }
  }
})
