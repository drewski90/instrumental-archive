<template>
  <nav class="app-nav d-flex align-items-center px-4">

    <div class="nav-brand me-4">
      Andrew Martinez
    </div>

    <div class="d-flex gap-3">

      <RouterLink class="nav-link" to="/">
        Browse
      </RouterLink>

      <!-- Only visible when logged in -->
      <RouterLink
        v-if="auth.isAuthenticated"
        class="nav-link"
        to="/upload"
      >
        Upload
      </RouterLink>

      <!-- Only visible when logged OUT -->
      <RouterLink
        v-if="!auth.isAuthenticated"
        class="nav-link"
        to="/login"
      >
        Login
      </RouterLink>

    </div>

    <div class="ms-auto d-flex gap-2">

      <button
        v-if="auth.isAuthenticated"
        class="btn btn-sm btn-outline-light"
        @click="logout"
      >
        Logout
      </button>

    </div>

  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

function logout(){
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
.app-nav{
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;

  display:flex;
  align-items:center;

  backdrop-filter: blur(14px);
  background: rgba(15,15,35,0.35);
  border-bottom: 1px solid rgba(255,255,255,.06);

  z-index:1000;
}

.nav-brand{
  font-weight:600;
  letter-spacing:2px;
  color:white;
}

.nav-link{
  color: rgba(255,255,255,.7);
  text-decoration:none;
  font-weight:500;
  transition: all .2s ease;
}

.nav-link:hover{
  color:white;
  text-shadow:0 0 10px rgba(120,140,255,.6);
}
</style>
