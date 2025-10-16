<template>
  <div class="min-h-screen bg-gray-50">
    <!-- ✅ Solo muestra el menú si el usuario está logueado -->
    <ResponsiveMenu v-if="isLoggedIn" />
    <main class="container mx-auto px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeMount } from 'vue'
import { isLoggedIn } from './stores/auth.js'
import ResponsiveMenu from './components/ResponsiveMenu.vue'
import {useAuthStore} from "../stores/auth";

const stored = localStorage.getItem('isLoggedIn') === 'true'
isLoggedIn.value = stored
const auth = useAuthStore()
const initializing = ref(true)
onBeforeMount(async () => {
  await auth.restoreSession() // ✅ Espera a que todo esté listo
  initializing.value = false
})
</script>
