<template>
  <div class="form-wrapper">
    <h2 class="form-title">GESTIÓN DE PERMISOS</h2>
    <InputText
      v-model="Idrol"
      type="text"
      readonly
      v-show="mostrarInput"
      class="form-input "
    />
    <InputText
      v-model="Idcontrolador"
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
            <label class="form-label">PERMISO POR ROLES</label>
            <AutoComplete
              v-model="selectedRoles"
              :suggestions="filteredRoles"
              field="rol"
              dropdown
              optionValue="rol_id"
              optionLabel="rol"
              forceSelection
              placeholder="Seleccione rol..."
              class="form-input"
              @complete="buscarRoles"
              @change="onRolSeleccionado"

            />
          </div>
        </div>
      </form>
    </section>
    <!-- DATATABLE -->
    <section class="form-section">
      <!--        <div class="datatable-card">-->
      <h2 class="form-title">LISTADO DE CONTROLADORES</h2>
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
        :value="filteredPermisos"
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
        paginator-template="RowsPerPageDropdown FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport"
        :sortField="'rol'"
        :sortOrder="1"
      >
<!--        <Column field="controladorID" header="#" style="width: 60px"></Column>-->
        <Column field="rol" header="Rol" sortable></Column>
        <Column field="controlador" header="Módulo" sortable></Column>
        <Column bodyClass="text-center" field="ver" header="Ver" sortable>
          <template #body="slotProps">
              <Button
                v-if="slotProps.data.ver === 1"
                icon="pi pi-minus-circle icon-xl"
                title="Desactivar"
                severity="danger"
                back
                text
                rounded
                @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de desactivar?',
                  text: `Sr. usuario, va desactivar el permiso de ver en : ${slotProps.data.controlador}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'
                }).then(async (result) => {
                  if (result.isConfirmed) {
                    if(slotProps.data.ver === 1){
                    Idver = 0
                    }
                    Idcontrolador = slotProps.data.controladorID
                    Idcrear = slotProps.data.crear
                    Ideditar = slotProps.data.editar
                    Ideliminar = slotProps.data.eliminar
                    editarVer()
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
                  text: `Sr. usuario, va activar el permiso de ver en: ${slotProps.data.controlador}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'

                }).then(async (result) => {
                  if (result.isConfirmed) {
                    if(slotProps.data.ver ===0){
                    Idver = 1
                    }
                    Idcontrolador = slotProps.data.controladorID
                    Idcrear = slotProps.data.crear
                    Ideditar = slotProps.data.editar
                    Ideliminar = slotProps.data.eliminar
                    editarVer()
                  }
                });
              }"
              />
          </template>
        </Column>
        <Column bodyClass="text-center" field="updated_at" header="Crear">
          <template #body="slotProps">
            <Button
              v-if="slotProps.data.crear === 1"
              icon="pi pi-minus-circle icon-xl"
              title="Desactivar"
              severity="danger"
              back
              text
              rounded
              @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de desactivar?',
                  text: `Sr. usuario, va desactivar el permiso de crear en: ${slotProps.data.controlador}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'
                }).then(async (result) => {
                  if (result.isConfirmed) {
                    if(slotProps.data.crear === 1){
                    Idcrear = 0
                    }
                    Idcontrolador = slotProps.data.controladorID
                    Ideditar = slotProps.data.editar
                    Idver = slotProps.data.ver
                    Ideliminar = slotProps.data.eliminar
                    editarCrear()
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
                  text: `Sr. usuario, va activar el permiso de crear en: ${slotProps.data.controlador}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'

                }).then(async (result) => {
                  if (result.isConfirmed) {
                    if(slotProps.data.crear === 0){
                    Idcrear = 1
                    }
                    Idcontrolador = slotProps.data.controladorID
                    Ideditar = slotProps.data.editar
                    Idver = slotProps.data.ver
                    Ideliminar = slotProps.data.eliminar
                    editarCrear()
                  }
                });
              }"
            />
          </template>
        </Column>
        <Column bodyClass="text-center" field="updated_at" header="Editar">
          <template #body="slotProps">
            <Button
              v-if="slotProps.data.editar === 1"
              icon="pi pi-minus-circle icon-xl"
              title="Desactivar"
              severity="danger"
              back
              text
              rounded
              @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de desactivar?',
                  text: `Sr. usuario, va desactivar el permiso de editar en : ${slotProps.data.controlador}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'
                }).then(async (result) => {
                  if (result.isConfirmed) {
                    if(slotProps.data.editar === 1){
                    Ideditar = 0
                    }
                    Idcontrolador = slotProps.data.controladorID
                    Idcrear = slotProps.data.crear
                    Idver = slotProps.data.ver
                    Ideliminar = slotProps.data.eliminar
                    editarEditar()
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
                  text: `Sr. usuario, va activar el permiso de editar en : ${slotProps.data.controlador}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'

                }).then(async (result) => {
                  if (result.isConfirmed) {
                    if(slotProps.data.editar === 0){
                    Ideditar = 1
                    }
                    Idcontrolador = slotProps.data.controladorID
                    Idcrear = slotProps.data.crear
                    Idver = slotProps.data.ver
                    Ideliminar = slotProps.data.eliminar
                    editarEditar()
                  }
                });
              }"
            />
          </template>
        </Column>
        <Column bodyClass="text-center" field="updated_at" header="Eliminar">
          <template #body="slotProps">
            <Button
              v-if="slotProps.data.eliminar === 1"
              icon="pi pi-minus-circle icon-xl"
              title="Desactivar"
              severity="danger"
              back
              text
              rounded
              @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de desactivar?',
                  text: `Sr. usuario, va desactivar el permiso de elimnar en : ${slotProps.data.controlador}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'
                }).then(async (result) => {
                  if (result.isConfirmed) {
                    if(slotProps.data.eliminar === 1){
                    Ideeliminar = 0
                    }
                    Idcontrolador = slotProps.data.controladorID
                    Idcrear = slotProps.data.crear
                    Idver = slotProps.data.ver
                    Ideeditar = slotProps.data.editar
                    editarEliminar()
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
                  text: `Sr. usuario, va activar el permiso de elimnar en : ${slotProps.data.controlador}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'

                }).then(async (result) => {
                  if (result.isConfirmed) {
                    if(slotProps.data.eliminar === 0){
                    Ideeliminar = 1
                    }
                    Idcontrolador = slotProps.data.controladorID
                    Idcrear = slotProps.data.crear
                    Idver = slotProps.data.ver
                    Ideeditar = slotProps.data.editar
                    editarEliminar()
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
import {onMounted, ref,computed} from 'vue'
import {FilterMatchMode} from 'primevue/api'
import {useAuthStore} from "@/stores/auth.js"
import Swal from "sweetalert2";

const URI_ROOT = import.meta.env.VITE_API_URL;
const cargo = ref('')
const Idpermiso = ref('')
const Idrol = ref('')
const Idcontrolador = ref('')
const Idver = ref('')
const Idcrear = ref('')
const Ideditar = ref('')
const Ideliminar = ref('')

const fecha = ref('')
const loading = ref(false)
const mostrarInput = ref(false)
const mostrarBtnUpdate = ref(false)
const mostrarBtnCrear = ref(true)

const permisos = ref([])
const roles = ref([])
const filteredRoles = ref([])
const selectedRoles = ref(null)
const tablePermisos = ref([])
const auth = useAuthStore()
const Puede = auth.permisos?.Permisos

const filters = ref({
  global: {value: null, matchMode: FilterMatchMode.CONTAINS},
})

onMounted(async () => {
  await loadPermisos();
  await loadRoles();
})

async function loadRoles() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargaroles')
    if (!response.ok) throw new Error('Error')
    roles.value = await response.json() // ✅ .value
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: {error},
      icon: 'error'
    });
  }
}
const buscarRoles = (event) => {
  loadRoles()
  let query = event.query?.toLowerCase() || ""
  if (!query.length) {
    // 👇 si no hay texto, muestra todos
    filteredRoles.value = roles.value
  } else {
    filteredRoles.value = roles.value.filter(c =>
      c.rol.toLowerCase().includes(query)
    )
  }
}

function onRolSeleccionado() {
  if (selectedRoles.value) {
    const Wcd = selectedRoles.value.rol_id
    Idrol.value = Wcd
  } else {
    Idrol.value = ''
  }
}

const filteredPermisos = computed(() => {
  if (!selectedRoles.value) {
    return permisos.value; // o tablePermisos.value, según tu estructura
  }
  return tablePermisos.value.filter(item =>
    item.rol === selectedRoles.value.rol
  );
});
async function loadPermisos() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargartablepermisos');
    permisos.value = await response.json()
    tablePermisos.value = permisos.value
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: 'No se pudieron cargar los cargos. Intente más tarde.',
      icon: 'error'
    });
  }
}

async function editarVer() {
  try {
    const response = await fetch(`${URI_ROOT}/api/updatepermisos`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        ver: Idver.value,
        crear: Idcrear.value,
        editar: Ideditar.value,
        eliminar: Ideliminar.value,
        controladorpermiso_id: Idcontrolador.value
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

    // const data = await response.json()
    // Swal.fire({
    //   title: '¡Múdulo actualizado correctamente!',
    //   text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
    //   icon: 'success',
    //   confirmButtonText: 'Aceptar',
    //   confirmButtonColor: '#374151',
    //   timer: 2000,
    //   timerProgressBar: true
    // })
    // ✅ ¡Recarga la tabla!
    await loadPermisos();


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

async function editarCrear() {
  try {
    const response = await fetch(`${URI_ROOT}/api/updatepermisos`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        ver: Idver.value,
        crear: Idcrear.value,
        editar: Ideditar.value,
        eliminar: Ideliminar.value,
        controladorpermiso_id: Idcontrolador.value
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

    // const data = await response.json()
    // Swal.fire({
    //   title: '¡Múdulo actualizado correctamente!',
    //   text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
    //   icon: 'success',
    //   confirmButtonText: 'Aceptar',
    //   confirmButtonColor: '#374151',
    //   timer: 2000,
    //   timerProgressBar: true
    // })

    // ✅ ¡Recarga la tabla!
    await loadPermisos();


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

async function editarEditar() {
  try {
    const response = await fetch(`${URI_ROOT}/api/updatepermisos`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        ver: Idver.value,
        crear: Idcrear.value,
        editar: Ideditar.value,
        eliminar: Ideliminar.value,
        controladorpermiso_id: Idcontrolador.value
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

    // const data = await response.json()
    // Swal.fire({
    //   title: '¡Múdulo actualizado correctamente!',
    //   text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
    //   icon: 'success',
    //   confirmButtonText: 'Aceptar',
    //   confirmButtonColor: '#374151',
    //   timer: 2000,
    //   timerProgressBar: true
    // })

    // ✅ ¡Recarga la tabla!
    await loadPermisos();


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

async function editarEliminar() {
  try {
    const response = await fetch(`${URI_ROOT}/api/updatepermisos`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        ver: Idver.value,
        crear: Idcrear.value,
        editar: Ideditar.value,
        eliminar: Ideliminar.value,
        controladorpermiso_id: Idcontrolador.value
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

    // const data = await response.json()
    // Swal.fire({
    //   title: '¡Múdulo actualizado correctamente!',
    //   text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
    //   icon: 'success',
    //   confirmButtonText: 'Aceptar',
    //   confirmButtonColor: '#374151',
    //   timer: 2000,
    //   timerProgressBar: true
    // })

    // ✅ ¡Recarga la tabla!
    await loadPermisos();


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
