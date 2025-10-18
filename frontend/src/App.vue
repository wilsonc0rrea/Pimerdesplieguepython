<template>
  <div class="app-container">
    <!-- 🔑 Si NO está logueado → login centrado -->
    <div v-if="!auth.isLoggedIn" class="min-h-screen flex items-center justify-center">
      <RouterView />
    </div>

    <!-- 🔑 Si está logueado → layout con menú y contenido -->
    <div v-else class="min-h-screen bg-gray-50 flex flex-col">
      <ResponsiveMenu :user="auth.user"/>
      <div class="dashboard-content flex-1">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-nocheck

import ResponsiveMenu from './components/ResponsiveMenu.vue'
import { ref, onMounted,onBeforeMount } from 'vue'
import { useAuthStore } from './stores/auth.js'
const initializing = ref(true) // ✅ Nuevo: estado de carga
const auth = useAuthStore()

onMounted(async () => {
  // await auth.restoreSession()
  // initializing.value = false
  try {
    await auth.restoreSession()
  } catch (error) {
    // Puedes manejar el error, por ejemplo:
    // - redirigir al login
    // - mostrar una notificación
    // - limpiar el estado
    //router.push("/login")
  } finally {
    initializing.value = false
  }
})

</script>

<style scoped>
.app-container {
  height: 100vh;
}

</style>
