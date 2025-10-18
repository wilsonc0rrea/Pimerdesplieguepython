<template>
  <div class="login-container">
    <div class="login-card">
      <img
        :src="logo"
        alt="Logo"
        class="w-20 h-20 mx-auto mb-4 rounded-full shadow-md"
      />
      <h2 class="text-xl font-semibold mb-2">Bienvenido</h2>
      <p class="text-gray-600 mb-6">Accede a tu cuenta para continuar</p>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Campo de correo -->
        <div class="text-left">
          <label class="block text-sm font-medium text-gray-700 mb-1">Correo electrónico</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="ejemplo@correo.com"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          />
        </div>

        <!-- Campo de contraseña -->
        <div class="text-left">
          <label class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
          <input
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="••••••••"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          />
        </div>

        <!-- Botón de login -->
        <Button
          type="submit"
          label="Iniciar Sesión"
          icon="pi pi-sign-in"
          :loading="loading"
          class="w-full bg-blue-700 hover:bg-blue-800 text-white font-semibold rounded-lg py-2 mt-2 transition-all"
        />

        <!-- Links inferiores -->
        <div class="text-center text-sm mt-4 space-y-2">
          <RouterLink
            to="/Auth/register"
            class="text-blue-600 hover:text-blue-800 font-medium block"
          >
            ¿No tienes cuenta? Regístrate
          </RouterLink>
          <RouterLink
            to="/Auth/forgot"
            class="text-blue-600 hover:text-blue-800 block"
          >
            ¿Olvidaste tu contraseña?
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>


<script setup lang="ts">
// @ts-nocheck
import {ref, reactive} from 'vue'
import {useRouter} from 'vue-router'
import logo from "@/assets/image/logo/mlogo.png"
import "@/assets/login.css"
import Swal from 'sweetalert2'
import {login} from '@/stores/auth.js' // 👈 ¡Importa la función login!

//------  Probando ---------
import { useAuthStore } from '@/stores/auth'
import { useIdle } from '@/composables/useIdle'
const auth = useAuthStore()
const { start } = useIdle({
  idleTime: 15*60*1000, // 15 min
  warningTime: 60*1000, // aviso 1 min antes
  onTimeout: () => {
    auth.clearSession()
    router.push('/login')
  }
})
//------ Fin probando ------

const URI_ROOT = import.meta.env.VITE_API_URL;

const router = useRouter()
const formData = reactive({
  email: '',
  password: ''
})
const errors = ref({
  email: '',
  password: ''
})
const email = ref('')
const password = ref('')
const showPassword = ref(false)
// ✅ Declara "loading" como un ref
const loading = ref(false);

const validateForm = () => {
  let isValid = true
  // const RespEmail = validateEmail(email.value)
  // ✅ Validación de formato de email
  const Email = email.value
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!Email || Email == ' ' || Email.startsWith('.') || Email.endsWith('.') || Email == '.' || !emailRegex.test(Email) || Email.includes('..')) {
    Swal.fire({
      title: 'Error',
      text: 'Por favor, verificar el correo al parecer está mal diligenciado',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
    // isValid = false
  } else if (!password.value) {
    Swal.fire({
      title: 'Error',
      text: 'La contraseña es requerida',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
    isValid = false
  } else if (password.value.length < 6) {
    Swal.fire({
      title: 'Error',
      text: 'Por favor, La contraseña debe tener al menos 6 caracteres',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
    isValid = false
  }

  return isValid
}

const validateEmailFormat = (email: string) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/ // patrón básico
  return emailRegex.test(email)
}
const handleSubmit = async () => {
  const userEmail = email.value.trim()

  if (!validateEmailFormat(userEmail)) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario. por favor verificar correo registrado',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }
  if (!password.value || password.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Por favor verifique su contraseña',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }
  loading.value = true
  try {
    const response = await fetch(URI_ROOT + '/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // 🔑 manda cookies al backend
      body: JSON.stringify({
        usuario_email: email.value,
        usuario_password: password.value
      }),
    })
    const contentType = response.headers.get("content-type")
    let data = null
    if (contentType && contentType.includes("application/json")) {
      data = await response.json()
    } else {
      data = await response.text()
    }
    stop()

    if (!response.ok) {
      let errorDetail = 'Error desconocido'
      try {
        const errorData = await response.json()
        data = errorData.detail || JSON.stringify(errorData)
      } catch (e) {
        data = await response.text()
      }
      throw new Error(`Error ${response.status}: ${errorDetail}`)
    }
    Swal.fire({
      title: '¡Bienvenido!',
      text: `Has iniciado sesión: ${data.usuario_nombre}, correctamente`,
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#334155'
    }).then(() => {

      // ✅ Guarda la sesión en el store global
      auth.setSession(data,data.controlador)
      // ✅ Activa el control de inactividad
      start()
      // ✅ Redirige
      router.push('/dashboard')
    })

  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: error.detail || 'Credenciales incorrectas',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } finally {
    loading.value = false
  }

}

</script>
