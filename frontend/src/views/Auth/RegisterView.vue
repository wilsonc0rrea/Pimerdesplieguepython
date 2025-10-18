<template>
  <div class="login-container">
    <div class="login-card">
      <img :src="logo"
           alt="Logo"
           class="w-20 h-20 mx-auto mb-4 rounded-full shadow-md"
      />
      <p>Accede a tu cuenta para continuar</p>

      <form @submit.prevent="handleSubmit">
        <div>
          <label class="form-label">Nombre completo</label>
          <InputText autocomplete="text" v-model="nombre" type="text" placeholder="Nombre completo"/>
        </div>

        <div>
          <label class="form-label">Correo Electrónico</label>
          <InputText v-model="email" type="email" placeholder="Correo Electrónico"/>
        </div>

        <div>
          <label class="form-label">Contraseña</label>
          <InputText v-model="password" :type="showPassword ? 'text' : 'password'" placeholder="Contraseña"/>
        </div>

        <!--          <div class="flex items-center">-->
        <!--            <Checkbox v-model="acceptTerms" inputId="terms" class="mr-2" />-->
        <!--            <label for="terms" class="text-sm text-gray-600 cursor-pointer">-->
        <!--              Acepto los <a href="#" class="text-green-600 hover:underline">Términos y Condiciones</a>-->
        <!--            </label>-->
        <!--          </div>-->
        <br>
        <Button
          type="submit"
          label="Crear Cuenta"
          icon="pi pi-user-plus"
          :loading="loading"
          class="w-full p-3 bg-gradient-to-r from-blue-600 to-blue-700
                           hover:from-blue-700 hover:to-blue-800 text-white font-semibold
                           rounded-xl shadow-md hover:shadow-lg transform hover:scale-[1.02]
                           transition-all duration-200"/>

        <div class="text-center mt-6">
          <p class="text-sm text-gray-600">
            ¿Ya tienes cuenta?
            <RouterLink to="/login" class="text-green-600 hover:text-green-800 font-medium ml-1">Inicia sesión
            </RouterLink>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-nocheck
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import logo from "@/assets/image/logo/mLogo.png"
import "@/assets/login.css"
import Swal from 'sweetalert2'
import {login} from '@/stores/auth.js' // 👈 ¡Importa la función login!
const URI_ROOT = import.meta.env.VITE_API_URL;


const router = useRouter()
const email = ref('')
const nombre = ref('')
const password = ref('')
const showPassword = ref(false)
const acceptTerms = ref(false)
const loading = ref(false)

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

    const response = await fetch(URI_ROOT + '/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        usuario_email: email.value,
        usuario_password: password.value,
        usuario_nombre: nombre.value
      })
    })

    if (!response.ok) {
      let errorDetail = 'Error desconocido'
      try {
        const errorData = await response.json()
        errorDetail = errorData.detail || JSON.stringify(errorData)
      } catch (e) {
        errorDetail = await response.text()
      }
      throw new Error(`Error ${response.status}: ${errorDetail}`)
    }
    const data = await response.json()
    // ✅ ¡Aquí actualizamos el estado global!
    //login(data.access_token || 'fake-token') // 👈 ¡Esto es clave!
    Swal.fire({
      title: '¡Bienvenido!',
      text: '¡Listo! Le hemos enviado un correo de verificación. Revíselo y confirme su cuenta para poder acceder.',
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#3b82f6'
    }).then(() => {
      // localStorage.setItem('isLoggedIn', 'true')
      // localStorage.setItem('token', data.access_token)
      // ✅ Redirige después de guardar el estado
      router.push('/login') // o '/home', según tu ruta
    })

  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: error.message || 'No se pudo conectar con el servidor',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } finally {
    loading.value = false
  }
}
</script>
