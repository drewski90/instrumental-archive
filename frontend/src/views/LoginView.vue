<template>
  <div class="login-root d-flex align-items-center justify-content-center">

    <div class="login-card p-4">

      <h3 class="mb-4 text-center">Sign in</h3>

      <form @submit.prevent="submit">

        <div class="mb-3">
          <label class="form-label text-light">Username</label>
          <input
            v-model="username"
            type="text"
            class="form-control glass-input"
            required
          />
        </div>

        <div class="mb-4">
          <label class="form-label text-light">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control glass-input"
            required
          />
        </div>

        <button class="btn btn-primary w-100 glass-btn" :disabled="auth.loading">
          {{ auth.loading ? "Signing in..." : "Login" }}
        </button>

        <div v-if="error" class="text-danger mt-3 text-center">
          {{ error }}
        </div>

      </form>

    </div>

  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const auth = useAuthStore()

const username = ref("")
const password = ref("")
const error = ref(null)

async function submit(){

  error.value = null

  try{
    await auth.login(username.value, password.value)
    router.push("/")   // redirect after login
  }
  catch(e){
    error.value = "Invalid credentials"
  }
}
</script>

<style scoped>
.login-root{
  min-height:100%;
}

/* glass card */
.login-card{
  width:360px;
  border-radius:20px;
  background:rgba(25,25,45,.55);
  backdrop-filter:blur(18px);
  border:1px solid rgba(255,255,255,.08);
  box-shadow:0 20px 60px rgba(0,0,0,.6);
}

/* inputs */
.glass-input{
  background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.08);
  color:white;
}

.glass-input:focus{
  background:rgba(255,255,255,.08);
  border-color:rgba(120,140,255,.6);
  box-shadow:0 0 0 0.2rem rgba(120,140,255,.2);
  color:white;
}

/* button */
.glass-btn{
  border-radius:12px;
  background:linear-gradient(90deg,#4f7cff,#8a4fff);
  border:none;
  font-weight:600;
}
</style>
