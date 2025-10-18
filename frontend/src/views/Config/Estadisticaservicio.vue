<template>
  <div class="form-wrapper">
    <section class="form-section">
      <div>
        <h2 class="text-2xl font-bold text-primary">Estadísticas de Servicios</h2>
      </div>

      <div class="form-field">
        <label for="fecha" class="form-label">Mes:</label>
        <InputText
          v-model="fecha"
          id="fecha"
          dateFormat="MM yy"
          type="month"
          placeholder="Fecha"
          class="form-input"
        />
      </div>

      <Chart
        type="bar"
        :data="chartData"
        :options="chartOptions"
        style="height: 300px"
      />

      <Dialog
        v-model:visible="mostrarDetalle"
        modal
        header="Detalle de Servicios"
        :style="{ width: '60vw' }"
      >
        <div v-if="personaSeleccionada">
          <h3 class="text-xl font-semibold mb-3">
            {{ personaSeleccionada.nombre }}
          </h3>
          <p class="text-sm text-600 mb-4">
            Servicios atendidos en fecha {{ fecha }}: con un total de {{ personaSeleccionada.servicios.length }}
          </p>

          <DataTable
            :value="personaSeleccionada.servicios"
            paginator
            :rows="30"
            responsiveLayout="scroll"
            class="p-datatable-sm"
          >
            <Column field="fecha" header="Fecha" sortable/>
            <Column field="servicio" header="Servicio" sortable/>
            <Column field="cliente" header="Cliente" sortable/>
          </DataTable>
        </div>
      </Dialog>
    </section>
  </div>
</template>

<script setup lang="ts">
// @ts-nocheck
import {ref, computed, watch, onMounted} from "vue";
import Swal from "sweetalert2";

const dataservicios = ref([])
const datatableservicios = ref([])
const fecha = ref('')
const fechaSeleccionada = ref('')
const URI_ROOT = import.meta.env.VITE_API_URL;
const mostrarDetalle = ref(false);
const personaSeleccionada = ref(null);
// const fechaActual = new Date().toLocaleDateString('en-CA');
// const fechaFormateada = fechaActual.split('T')[0];
// fecha.value = fechaFormateada.toString()

const fechaActual = new Date().toLocaleDateString('en-CA') // "2025-10-15"
const [anio, mes] = fechaActual.split('-') // divide por guion
const fechaFormateada = `${anio}-${mes}`   // une solo año y mes
fecha.value = fechaFormateada

onMounted(async () => {
  try {
    await Promise.all([
      loadDataservicios()
    ])
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: {error},
      icon: 'error'
    });
  }
})

async function loadDataservicios() {
  try {
    const response = await fetch(URI_ROOT + `/api/cargarestadisticaservicios/?mes=${fecha.value}`)
    if (!response.ok) throw new Error('Error')
    dataservicios.value = await response.json()
  } catch (error) {
    // Swal.fire({
    //   title: 'Error',
    //   text: {error},
    //   icon: 'error'
    // });
  }
}


const filtrados = computed(() => {
  return dataservicios.value.map((persona) => {
    const serviciosMes = persona.servicios.filter((s) =>
      s.fecha.startsWith(fecha.value)
    );
    return {...persona, servicios: serviciosMes, total: serviciosMes.length};
  });
});

const chartData = computed(() => ({
  labels: filtrados.value.map((p) => p.nombre),
  datasets: [
    {
      label: "Servicios atendidos",
      backgroundColor: "#1f2937",
      data: filtrados.value.map((p) => p.total),
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false, // 👈 Permite que el height CSS se aplique
  plugins: {
    legend: {display: false},
    tooltip: {
      callbacks: {
        label: (context) => `Servicios: ${context.raw}`,
      },
    },
  },
  onClick: (e, elements, chart) => {
    if (elements.length > 0) {
      const index = elements[0].index;
      personaSeleccionada.value = filtrados.value[index];
      mostrarDetalle.value = true;
    }
  },
  scales: {
    x: {ticks: {color: "#6b7280"}},
    y: {
      beginAtZero: true,
      ticks: {stepSize: 1, color: "#6b7280"},
      grid: {color: "#e5e7eb"},
    },
  },
};
</script>
