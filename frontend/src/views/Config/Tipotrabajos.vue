<template>
  <div class="form-wrapper">
    <h2 class="form-title">CREACIÓN TIPOS DE TRABAJO</h2>
    <InputText
      v-model="Idtrabajo"
      type="text"
      readonly
      v-show="true"
      class="form-input "
    />
    <InputText
      v-model="Idstate"
      type="text"
      readonly
      v-show="mostrarInput"
      class="form-input "
    />
    <!-- Formulario de Creación -->
    <section class="form-section">
      <form @submit.prevent="handleSubmit" class="form-inline">
        <!-- Contenedor flex -->
        <div class="form-row">

          <div class="form-field">
            <label for="traba" class="form-label">TIPO DE TRABAJO</label>
            <InputText
              v-model="tipotrabajo"
              id="traba"
              type="text"
              placeholder="Tipo de trabajo"
              class="form-input"
            />
          </div>
          <div class="form-field action-field">
            <label class="form-label invisible">ACCIONES</label> <!-- Label invisible para mantener alineación -->
            <Button
              type="submit"
              label="Crear..."
              v-show="mostrarBtnCrear"
              icon="pi pi-user-plus"
              :loading="loading"
              class="form-button"
            />
            <Button
              type="button"
              label="Actualizar..."
              v-show="mostrarBtnUpdate"
              icon="pi pi-user-plus"
              :loading="loading"
              class="form-button hidden"
              @click="() => {
                editarTipos()
              }"
            />
          </div>
        </div>
      </form>
    </section>
    <!-- DATATABLE -->
    <section class="form-section">
      <!--        <div class="datatable-card">-->
      <h2 class="form-title">LISTADO TIPOS DE TRABAJO</h2>
      <div class="datatable-header">
            <span class="p-input-icon-left">
              <InputText
                v-model="filters.global.value"
                placeholder="Buscar..."
                class="p-inputtext-sm"
              />
            </span>
      </div>

      <DataTable
        :value="trabajos"
        :filters="filters"
        :paginator="true"
        :rows="60"
        paginator
        scrollable
        scrollHeight="800px"
        responsive-layout="scroll"
        filterDisplay="menu"
        striped-rows
        currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} registros"
        :sortField="'created_at'"
        :sortOrder="-1"
      >
        <Column field="ttrabajo_id" header="#" style="width: 60px"></Column>
        <Column field="trabajo" header="Cargo" sortable></Column>
        <Column field="created_at" header="Fecha creado" sortable></Column>
        <Column field="updated_at" header="Fecha actualizado"></Column>
        <Column field="flag" header="Estado" sortable>
          <template #body="slotProps">
            {{ getFlagLabel(slotProps.data.flag) }}
          </template>
        </Column>
        <Column field="flag" header="Acciones" style="width: 150px">
          <template #body="slotProps">
            <Button
              icon="pi pi-pencil"
              title="Editar"
              severity="info"
              text
              rounded
              @click="() => {
                 Swal.fire({
                  title: 'Confirmación',
                  text: `Sr. usuario, está seguro que desea editar el tipo de trabajo: ${slotProps.data.trabajo}`,
                  icon: 'info',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'
                }).then(async (result) => {
                  if (result.isConfirmed) {
                    mostrarBtnUpdate = true
                    mostrarBtnCrear = false
                    tipotrabajo = slotProps.data.trabajo
                    Idtrabajo = slotProps.data.trabajo_id
                  }
                });
              }"
            />
            <Button
              v-if="slotProps.data.flag === 1 || slotProps.data.flag === true"
              icon="pi pi-check-circle"
              title="Desactivar"
              severity="danger"
              back
              text
              rounded
              @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de desactivar?',
                  text: `Sr. usuario, va desactivar el tipo de trabajo: ${slotProps.data.trabajo}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'
                }).then(async (result) => {
                  if (result.isConfirmed) {
                    if(slotProps.data.flag === true || slotProps.data.flag === 1){
                    Idstate = 0
                    }
                    Idtrabajo = slotProps.data.trabajo_id
                    editarTiposTate()
                  }
                });
              }"
            />
            <Button
              v-else
              icon="pi pi-check-circle"
              title="Activar"
              severity="sucess"
              back
              text
              rounded
              @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de activar?',
                  text: `Sr. usuario, va activar el tipo de trabajo: ${slotProps.data.trabajo}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'

                }).then(async (result) => {
                  if (result.isConfirmed) {
                    if(slotProps.data.flag === false || slotProps.data.flag === 0){
                    Idstate = 1
                    }
                    Idtrabajo = slotProps.data.trabajo_id
                    editarTiposTate()
                  }
                });
              }"
            />
            <Button
              icon="pi pi-trash"
              title="Eliminar"
              severity="danger"
              back
              text
              rounded
              @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de eliminar?',
                  text: `Sr. usuario, va eliminar el cargo: ${slotProps.data.trabajo}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'

                }).then(async (result) => {
                  if (result.isConfirmed) {
                    Idcargo = slotProps.data.trabajo_id
                    deleteTipos()
                  }
                });
              }"
            />
          </template>
        </Column>
      </DataTable>
      <!--        </div>-->
    </section>
  </div>
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue'
import {FilterMatchMode} from 'primevue/api'
import Swal from "sweetalert2";
const URI_ROOT = import.meta.env.VITE_API_URL;
const tipotrabajo = ref('')
const Idtrabajo = ref('')
const Idstate = ref('')
const fecha = ref('')
const loading = ref(false)
const mostrarInput = ref(false)
const mostrarBtnUpdate = ref(false)
const mostrarBtnCrear = ref(true)

const trabajos = ref([])

const filters = ref({
  global: {value: null, matchMode: FilterMatchMode.CONTAINS},
})

function getFlagLabel(flag) {
  return flag === 1 || flag === true ? 'Activo' : 'Inactivo';
}


onMounted(async () => {
  await loadTrabajos();
})

async function loadTrabajos() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargartabletrabajos');
    trabajos.value = await response.json()
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: 'No se pudieron cargar los cargos. Intente más tarde.',
      icon: 'error'
    });
  }
}


const handleSubmit = async () => {
  if (!tipotrabajo.value || tipotrabajo.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Por favor ingrese el nombre del cargo',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }

  loading.value = true
  try {
    const response = await fetch(`${URI_ROOT}/api/creatipotrabajos`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({trabajo: tipotrabajo.value})
    })

    if (!response.ok) {
      const text = await response.text()
      let errorDetail = text
      try {
        const errorData = JSON.parse(text)
        errorDetail = errorData.detail || JSON.stringify(errorData)
      } catch (e) {
      }
      throw new Error(errorDetail)
    }

    const data = await response.json()
    Swal.fire({
      title: '¡Cargo creado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })


    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTrabajos();


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

function limpiarForm(){
  tipotrabajo.value = ""
  Idstate.value = ""
  Idtrabajo.value = ""
}

async function editarTipos() {
  try {
    if (!tipotrabajo.value || tipotrabajo.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Por favor ingrese el nombre del cargo',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }

    const response = await fetch(`${URI_ROOT}/api/updatetipotrabajo`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        trabajo: tipotrabajo.value,
        trabajo_id: Idtrabajo.value
      })
    })

    if (!response.ok) {
      const text = await response.text()
      let errorDetail = text
      try {
        const errorData = JSON.parse(text)
        errorDetail = errorData.detail || JSON.stringify(errorData)
      } catch (e) {
      }
      throw new Error(errorDetail)
    }

    const data = await response.json()
    Swal.fire({
      title: '¡Cargo creado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTrabajos();


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

async function editarTiposTate() {
  try {
    const response = await fetch(`${URI_ROOT}/api/updatetrabajostate`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        flag: Idstate.value,
        trabajo_id: Idtrabajo.value
      })
    })

    if (!response.ok) {
      const text = await response.text()
      let errorDetail = text
      try {
        const errorData = JSON.parse(text)
        errorDetail = errorData.detail || JSON.stringify(errorData)
      } catch (e) {
      }
      throw new Error(errorDetail)
    }

    const data = await response.json()
    Swal.fire({
      title: '¡Tipo de trabajo creado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTrabajos();


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

async function deleteTipos() {
  try {
    const response = await fetch(`${URI_ROOT}/api/deletetrabajos/`+Idtrabajo.value, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
    })

    if (!response.ok) {
      const text = await response.text()
      let errorDetail = text
      try {
        const errorData = JSON.parse(text)
        errorDetail = errorData.detail || JSON.stringify(errorData)
      } catch (e) {
      }
      throw new Error(errorDetail)
    }

    const data = await response.json()
    Swal.fire({
      title: '¡Cargo eliminado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTrabajos();


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
