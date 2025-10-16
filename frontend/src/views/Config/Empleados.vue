<template>
  <div class="form-wrapper">
    <h2 class="form-title">CREACIÓN DE EMPLEADOS</h2>
    <InputText
      v-model="Idempleados"
      type="text"
      readonly
      v-show="mostrarInput"
      class="form-input "
    />
    <InputText
      v-model="Idcargo"
      type="text"
      readonly
      v-show="mostrarInput"
      class="form-input "
    />
    <InputText
      v-model="Idrol"
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
            <label for="nombre" class="form-label">NOMBRE</label>
            <InputText
              v-model="nombre"
              id="nombre"
              type="text"
              placeholder="Nombre"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="dir" class="form-label">DIRECCIÓN</label>
            <InputText
              v-model="direccion"
              id="dir"
              type="text"
              placeholder="DIRECCION"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="tel" class="form-label">TELÉFONOS</label>
            <InputText
              v-model="telefonos"
              id="tel"
              type="text"
              placeholder="TELEFONOS"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="email" class="form-label">EMAIL</label>
            <InputText
              v-model="email"
              id="email"
              type="text"
              placeholder="EMAIL"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label class="form-label">CARGO</label>
            <AutoComplete
              v-model="selectedCargo"
              :suggestions="filteredCargos"
              field="cargo"
              optionValue="cargo_id"
              optionLabel="cargo"
              dropdown
              forceSelection
              placeholder="Escribe y selecciona un cargo"
              class="form-input"
              @complete="buscarCargo"
              @change="onCargoSeleccionado"
            />
          </div>
          <div class="form-field">
            <label class="form-label">ROL</label>
            <AutoComplete
              v-model="selectedRol"
              :suggestions="filteredRoles"
              field="rol"
              dropdown
              optionValue="rol_id"
              optionLabel="rol"
              forceSelection
              placeholder="Escribe y selecciona un rol"
              class="form-input"
              @complete="buscarRoles"
              @change="onRolSeleccionado"
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
                editarEmpleado()
              }"
            />
          </div>
        </div>
      </form>
    </section>
    <!-- DATATABLE -->
    <section class="form-section">
      <!--        <div class="datatable-card">-->
      <h2 class="form-title">LISTADO DE EMPLEADOS</h2>
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
        :value="empleadosTable"
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
        <Column field="empleado_id" header="#" style="width: 60px"></Column>
        <Column field="nombre" header="Nombre" sortable></Column>
        <Column field="direccion" header="Dirección"></Column>
        <Column field="telefonos" header="# Contacto"></Column>
        <Column field="email" header="Email"></Column>
        <Column field="rol.rol" header="Rol"></Column>
        <Column field="cargo.cargo" header="Cargo"></Column>
        <!--        <Column field="created_at" header="Fecha creado" sortable></Column>-->
        <!--        <Column field="updated_at" header="Fecha actualizado"></Column>-->
        <Column field="flag" header="Estado">
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
                  text: `Sr. usuario, está seguro que desea editar el empleado: ${slotProps.data.nombre}`,
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
                    nombre = slotProps.data.nombre
                    direccion = slotProps.data.direccion
                    telefonos = slotProps.data.telefonos
                    email = slotProps.data.email
                    Idempleados = slotProps.data.empleado_id
                    Idcargo = slotProps.data.cargo.cargo_id
                    Idrol = slotProps.data.rol.rol_id

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
                  text: `Sr. usuario, va desactivar el empleado: ${slotProps.data.nombre}`,
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
                    Idempleados = slotProps.data.empleado_id
                    editarEmpleadosTate()
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
                  text: `Sr. usuario, va activar el empleado: ${slotProps.data.nombre}`,
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
                    Idempleados = slotProps.data.empleado_id
                    editarEmpleadosTate()
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
                  text: `Sr. usuario, va eliminar el empleado: ${slotProps.data.nombre}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'

                }).then(async (result) => {
                  if (result.isConfirmed) {
                    Idempleados = slotProps.data.empleado_id
                    deleteEmpleados()
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
const nombre = ref('')
const email = ref('')
const telefonos = ref('')
const direccion = ref('')
const selectedCargo = ref(null)
const selectedRol = ref(null)
const Idempleados = ref('')
const Idcargo = ref('')
const Idrol = ref('')
const Idstate = ref('')
const loading = ref(false)
const mostrarInput = ref(false)
const mostrarBtnUpdate = ref(false)
const mostrarBtnCrear = ref(true)

const cargos = ref([])
const roles = ref([])
const filteredCargos = ref([])
const filteredRoles = ref([])
const empleadosTable = ref([])

const filters = ref({
  global: {value: null, matchMode: FilterMatchMode.CONTAINS},
})

function getFlagLabel(flag) {
  return flag === 1 || flag === true ? 'Activo' : 'Inactivo';
}

onMounted(async () => {
  try {
    await Promise.all([
      loadEmpleados(),
      loadRoles(),
      loadCargos()
    ])
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: {error},
      icon: 'error'
    });
  }
})

function onCargoSeleccionado() {
  if (selectedCargo.value) {
    const Wcd = selectedCargo.value.cargo_id
    Idcargo.value = Wcd
  } else {
    Idcargo.value = ''
  }
}

function onRolSeleccionado() {
  if (selectedRol.value) {
    const Wcd = selectedRol.value.rol_id
    Idrol.value = Wcd
  } else {
    Idrol.value = ''
  }
}

const buscarCargo = (event) => {
  loadCargos()
  let query = event.query?.toLowerCase() || ""
  if (!query.length) {
    // 👇 si no hay texto, muestra todos
    filteredCargos.value = cargos.value
  } else {
    filteredCargos.value = cargos.value.filter(c =>
      c.cargo.toLowerCase().includes(query)
    )
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

async function loadCargos() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargarcargos')
    if (!response.ok) throw new Error('Error')
    cargos.value = await response.json() // ✅ .value
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: {error},
      icon: 'error'
    });
  }
}

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

async function loadEmpleados() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargartableempleados');
    empleadosTable.value = await response.json()
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: 'No se pudieron cargar los empleados. Intente más tarde.',
      icon: 'error'
    });
  }
}
const validateEmailFormat = (email: string) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/ // patrón básico
  return emailRegex.test(email)
}

const handleSubmit = async () => {
  const userEmail = email.value.trim()
  if (!validateEmailFormat(userEmail)) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario. por favor verificar correo del empleado',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }else if (!nombre.value || nombre.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor ingrese el nombre del empleado',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (!direccion.value || direccion.value.length < 6) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor varificar dirección',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (Idcargo.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor cargo del empleado',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }else if (Idrol.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor rol del empleado',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }else if (Idrol.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor rol del empleado',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }

  loading.value = true
  try {
    const response = await fetch(`${URI_ROOT}/api/creaempleados`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        nombre: nombre.value,
        direccion: direccion.value,
        telefonos: telefonos.value,
        email: email.value,
        cargo_id: Idcargo.value,
        rol_id: Idrol.value,
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
      title: '¡Empleado creado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadEmpleados();


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
  nombre.value = ""
  direccion.value = ""
  telefonos.value = ""
  email.value = ""
  selectedCargo.value = ""
  selectedRol.value = ""
  Idcargo.value = ""
  Idrol.value = ""
  Idempleados.value = ""
}

async function editarEmpleado() {
  try {


    const userEmail = email.value.trim()
    if (!validateEmailFormat(userEmail)) {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario. por favor verificar correo del empleado',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }else if (!nombre.value || nombre.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor ingrese el nombre del empleado',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    } else if (!direccion.value || direccion.value.length < 6) {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor varificar dirección',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    } else if (Idcargo.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor cargo del empleado',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }else if (Idrol.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor rol del empleado',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }else if (Idrol.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor rol del empleado',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }


    const response = await fetch(`${URI_ROOT}/api/updateempleados`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        empleado_id: Idempleados.value,
        nombre: nombre.value,
        direccion: direccion.value,
        telefonos: telefonos.value,
        email: email.value,
        cargo_id: Idcargo.value,
        rol_id: Idrol.value,
      })
    })


    if (!response.ok) {
      const text = await response.text();
      let errorDetail = text;
      try {
        const errorData = JSON.parse(text);
        errorDetail = errorData.detail || JSON.stringify(errorData, null, 2);
      } catch (e) {
        // mantener text como fallback
      }
      throw new Error(errorDetail);
    }

    const data = await response.json()
    Swal.fire({
      title: '¡CLiente actualizado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })


    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadEmpleados();


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

async function editarEmpleadosTate() {
  try {
    if (Idempleados.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor item del empleado a editar el estado',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }
    const response = await fetch(`${URI_ROOT}/api/updateempleadostate`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        flag: Idstate.value,
        empleado_id: Idempleados.value
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
      title: '¡Estado de cliente creado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadEmpleados();


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

async function deleteEmpleados() {
  try {

    if (Idempleados.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor item del empleado a eliminar',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }
    const response = await fetch(`${URI_ROOT}/api/deleteempleados/` + Idempleados.value, {
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
      title: '¡Cliente eliminado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })
    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadEmpleados();


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
