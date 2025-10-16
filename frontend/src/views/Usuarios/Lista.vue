<template>
  <div class="bg-white rounded-lg shadow p-8">
    <h2 class="text-2xl font-bold text-gray-800 mb-4">Lista de Usuarios</h2>
    <p>Contenido de la lista de usuarios...</p>
    <div class="mt-4 space-y-2">
      <div v-for="n in 5" :key="n" class="p-3 border rounded hover:bg-gray-50">
        Usuario {{ n }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const users = [
  { id: 1, name: 'Ana García', email: 'ana@example.com' },
  { id: 2, name: 'Luis Martínez', email: 'luis@example.com' },
  { id: 3, name: 'Carla Sánchez', email: 'carla@example.com' }
]
</script>
