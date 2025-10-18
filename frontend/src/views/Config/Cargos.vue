<template>
  <div class="form-wrapper">
    <h2 class="form-title">CREACIÓN DE CARGOS</h2>
    <InputText
      v-model="Idcargo"
      type="text"
      readonly
      v-show="mostrarInput"
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
            <label for="cargo" class="form-label">CARGO</label>
            <InputText
              v-model="cargo"
              id="cargo"
              type="text"
              placeholder="Cargo"
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
                editarCargos()
              }"
            />
          </div>
        </div>
      </form>
    </section>
    <!-- DATATABLE -->
    <section class="form-section">
      <!--        <div class="datatable-card">-->
      <h2 class="form-title">LISTADO DE CARGOS</h2>
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
        :value="cargos"
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
        <Column field="cargo_id" header="#" style="width: 60px"></Column>
        <Column field="cargo" header="Cargo" sortable></Column>
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
              icon="pi pi-pencil icon-xl"
              title="Editar"
              severity="info"
              text
              rounded
              @click="() => {
                 Swal.fire({
                  title: 'Confirmación',
                  text: `Sr. usuario, está seguro que desea editar el cargo: ${slotProps.data.cargo}`,
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
                    cargo = slotProps.data.cargo
                    Idcargo = slotProps.data.cargo_id
                  }
                });
              }"
            />
            <Button
              v-if="slotProps.data.flag === 1 || slotProps.data.flag === true"
              icon="pi pi-check-circle icon-xl"
              title="Desactivar"
              severity="danger"
              back
              text
              rounded
              @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de desactivar?',
                  text: `Sr. usuario, va desactivar el cargo: ${slotProps.data.cargo}`,
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
                    Idcargo = slotProps.data.cargo_id
                    editarCargosTate()
                  }
                });
              }"
            />
            <Button
              v-else
              icon="pi pi-check-circle icon-xl"
              title="Activar"
              severity="sucess"
              back
              text
              rounded
              @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de activar?',
                  text: `Sr. usuario, va activar el cargo: ${slotProps.data.cargo}`,
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
                    Idcargo = slotProps.data.cargo_id
                    editarCargosTate()
                  }
                });
              }"
            />
            <Button
              icon="pi pi-trash icon-xl"
              title="Eliminar"
              severity="danger"
              back
              text
              rounded
              @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de eliminar?',
                  text: `Sr. usuario, va eliminar el cargo: ${slotProps.data.cargo}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'

                }).then(async (result) => {
                  if (result.isConfirmed) {
                    Idcargo = slotProps.data.cargo_id
                    deleteCargos()
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
// @ts-nocheck
import {onMounted, ref} from 'vue'
import {FilterMatchMode} from 'primevue/api'
import Swal from "sweetalert2";
const URI_ROOT = import.meta.env.VITE_API_URL;
const cargo = ref('')
const Idcargo = ref('')
const Idstate = ref('')
const fecha = ref('')
const loading = ref(false)
const mostrarInput = ref(false)
const mostrarBtnUpdate = ref(false)
const mostrarBtnCrear = ref(true)

const cargos = ref([])

const filters = ref({
  global: {value: null, matchMode: FilterMatchMode.CONTAINS},
})

function getFlagLabel(flag) {
  return flag === 1 || flag === true ? 'Activo' : 'Inactivo';
}


onMounted(async () => {
  await loadCargos();
})

async function loadCargos() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargartablecargos');
    cargos.value = await response.json()
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: 'No se pudieron cargar los cargos. Intente más tarde.',
      icon: 'error'
    });
  }
}

async function editarCargos() {
  try {
    if (!cargo.value || cargo.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Por favor ingrese el nombre del cargo',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }

    const response = await fetch(`${URI_ROOT}/api/updatecargos`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        cargo: cargo.value,
        cargo_id: Idcargo.value
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
    await loadCargos();


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

async function editarCargosTate() {
  try {
    const response = await fetch(`${URI_ROOT}/api/updatecargostate`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        flag: Idstate.value,
        cargo_id: Idcargo.value
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
    await loadCargos();


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
  cargo.value = ""
  Idcargo.value=""
  Idstate.value=""
}

async function deleteCargos() {
  try {
    const response = await fetch(`${URI_ROOT}/api/deletecargos/`+Idcargo.value, {
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
    await loadCargos();


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




const handleSubmit = async () => {
  if (!cargo.value || cargo.value.trim() === '') {
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
    const response = await fetch(`${URI_ROOT}/api/creacargos`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({cargo: cargo.value})
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
    await loadCargos();


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
