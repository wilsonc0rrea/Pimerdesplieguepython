<template #content>
  <section class="form-section">
    <div class="p-6">
      <div class="dashboard-grid mb-8 text-center">
        <Card class="text-ultra-large shadow-md hover:shadow-xl transition-shadow duration-300"
              @click="router.push('/config/clientes')">
          <template #title>
            <div class="font-bold text-lg">Clientes activos</div>
          </template>
          <template #content>
            <CountTo :start-val="0" :end-val="clienteactivo" :duration="3000" class="text-4xl font-bold text-primary"
            />
          </template>
          <template #footer>
            <div class="flex gap-4 mt-4 justify-center">
              <img :src="logouser" alt="logousers">
            </div>
          </template>
        </Card>
        <Card class="text-ultra-large shadow-md hover:shadow-xl transition-shadow duration-300">
          <template #title>
            <div class="flex items-center gap-3">
              <span class="font-medium text-gray-600">Usuarios Activos</span>
            </div>
          </template>
          <template #content>
            <count-to :start-val="0" :end-val="usauriosactivos" :duration="3000"
                      class="text-4xl font-bold text-green-600"/>
          </template>
          <template #footer>
            <div class="flex gap-4 mt-4 justify-center">
              <img :src="logolocation" alt="logolocation">
            </div>
          </template>
        </Card>
        <Card class="text-ultra-large shadow-md hover:shadow-xl transition-shadow duration-300"
              @click="router.push('/config/reportes')">
          <template #title>
            <div class="flex items-center gap-3">
              <span class="font-medium text-gray-600">Servicios Activos</span>
            </div>
          </template>
          <template #content>
            <count-to :start-val="0" :end-val="serviciosactivos" :duration="3000"
                      class="text-4xl font-bold text-green-600"/>
          </template>
          <template #footer>
            <div class="flex gap-4 mt-4 justify-center">
              <img :src="logouser" alt="logousers">
            </div>
          </template>
        </Card>
        <Card class="text-ultra-large shadow-md hover:shadow-xl transition-shadow duration-300"
              @click="router.push('/config/reportes')">
          <template #title>
            <div class="flex items-center gap-3">
              <span class="font-medium text-gray-600">Servicios realizados</span>
            </div>
          </template>
          <template #content>
            <count-to :start-val="0" :end-val="serviciosinactivos" :duration="3000"
                      class="text-4xl font-bold text-green-600"/>
          </template>
          <template #footer>
            <div class="flex gap-4 mt-4 justify-center">
              <img :src="logolocation" alt="logolocation">
            </div>
          </template>
        </Card>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue'

const remember = ref(false)
import router from '@/router' // ajusta a tu router
import logouser from "@/assets/image/users.svg"
import logolocation from "@/assets/image/locations.svg"
import Swal from "sweetalert2";
import {CountTo} from "vue3-count-to"

const Data = ref([])
const clienteactivo = ref(0)
const serviciosactivos = ref(0)
const serviciosinactivos = ref(0)
const usauriosactivos = ref(0)
const URI_ROOT = import.meta.env.VITE_API_URL;

onMounted(async () => {
  try {
    await Promise.all([
      loadData()
    ])
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: {error},
      icon: 'error'
    });
  }
})


async function loadData() {
  try {
    const response = await fetch(URI_ROOT + '/api/estadisticas-generales')
    if (!response.ok) throw new Error('Error')
    const data = await response.json()
    clienteactivo.value = data.clientes
    usauriosactivos.value = data.usuarios
    serviciosactivos.value = data.serviciosActivos
    serviciosinactivos.value = data.serviciosInactivos
  } catch (error) {
    // Swal.fire({
    //   title: 'Error',
    //   text: {error},
    //   icon: 'error'
    // });
  }

}

</script>

<style scoped>

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 640px) {
  .dashboard-grid {
    grid-template-columns: repeat(1, 1fr);
  }
}

@media (min-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1280px) {
  .dashboard-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Transiciones suaves */
.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
}

/* Efecto sutil al pasar el mouse */
.p-card {
  /*background-color: rgba(255, 255, 255, 0.95) !important;*/
  backdrop-filter: blur(10px) !important;
  border-radius: 8px !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  transition: all 0.3s ease !important;
}

.p-card:hover {
  transform: translateY(-4px) !important;
  box-shadow: 0 12px 30px rgba(255, 255, 255, 0.25) !important;
}

/* Títulos dentro de las cards */
.p-card .p-card-title {
  font-weight: 600 !important;
}


</style>
