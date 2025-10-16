// src/stores/auth.js
import {defineStore} from 'pinia'
import {ref} from 'vue'
import router from '@/router' // ajusta a tu router
const URI_ROOT = import.meta.env.VITE_API_URL;

export const useAuthStore = defineStore('auth', () => {
  const token = ref(null)       // opcional: si usas cookie HttpOnly, token puede quedar null
  const user = ref(null)
  const permisos = ref({})
  const isLoggedIn = ref(false)

  // ✅ Solo en memoria: nada en localStorage
  const setSession = (userData, userPermisos) => {
    isLoggedIn.value = true
    user.value = userData
    permisos.value = userPermisos

  }

  const clearSession = () => {
    isLoggedIn.value = false
    user.value = null
    permisos.value = {}
    if (router.currentRoute.value.path !== '/Auth/login') {
      router.push('/Auth/login');
    }
  }

  // ✅ Restaurar sesión usando la cookie
  const restoreSession = async () => {
    try {
      const res = await fetch(`${URI_ROOT}/api/me`, {
        credentials: 'include' // ✅ Incluye la cookie HttpOnly
      })
      if (res.ok) {
        const data = await res.json()
        // Convertir array de permisos a objeto { modulo: { ... } }
        const permisosObj = {}
        data.controlador.forEach(p => {
          permisosObj[p.modulo] = {
            ver: p.ver === 1,
            crear: p.crear === 1,
            editar: p.editar === 1,
            eliminar: p.eliminar === 1
          }
        })
        user.value = data
        permisos.value = permisosObj
        isLoggedIn.value = true // ✅ Último paso

      } else {
        clearSession()
      }
    } catch (error) {
      clearSession()
    }
  }

  const logoutAndRedirect = async () => {
    try {
      // 1. Llamar al backend para eliminar la cookie
      const res = await fetch(`${URI_ROOT}/api/salir`, {
        method: 'POST',
        credentials: 'include' // ✅ Incluye la cookie HttpOnly
      })
      if (res.ok) {
        // 2. Limpiar el estado en memoria
        clearSession(); // → isLoggedIn = false, user = null, permisos = {}
        // 3. Redirigir al login
        router.push('/login');
      }
    } catch (error) {
      console.warn("Error al cerrar sesión en backend:", error);
      // Aun así, limpia el frontend
    }
  }
  return {
    user,
    permisos,
    setSession,
    restoreSession,
    clearSession,
    logoutAndRedirect,
    isLoggedIn
  }
})
