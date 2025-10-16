<template>
  <div class="form-wrapper">
    <h2 class="form-title">CREACIÓN DE CLIENTES</h2>
    <InputText
      v-model="Idclientes"
      type="text"
      readonly
      v-show="mostrarInput"
      class="form-input "
    />
    <InputText
      v-model="Idpais"
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
            <label for="nombre" class="form-label">NOMBRE - EMPRESA</label>
            <InputText
              v-model="nombre"
              id="nombre"
              type="text"
              placeholder="Nombre - Empresa"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="nit" class="form-label">NIT - CÉDULA</label>
            <InputText
              v-model="identificacion"
              id="nit"
              type="text"
              placeholder="NIT - CÉDULA"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="contacto" class="form-label">NÚMERO DE CONTACTOS</label>
            <InputText
              v-model="telefonos"
              id="contacto"
              type="text"
              placeholder="NÚMERO DE CONTACTOS"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label class="form-label">PAÍS</label>

            <AutoComplete
              v-model="selectedPais"
              :suggestions="filteredPaises"
              field="paises"
              dropdown
              optionValue="pais_id"
              optionLabel="paises"
              forceSelection
              placeholder="Escribe y selecciona un país"
              class="form-input"
              @complete="buscarPais"
              @change="onPaisSeleccionado"

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
                editarClientes()
              }"
            />
          </div>
        </div>
      </form>
    </section>
    <!-- DATATABLE -->
    <section class="form-section">
      <!--        <div class="datatable-card">-->
      <h2 class="form-title">LISTADO DE CLIENTES</h2>
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
        :value="clientesTable"
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
        <Column field="cliente_id" header="#" style="width: 60px"></Column>
        <Column field="clientes" header="Nombre" sortable></Column>
        <Column field="identificacion" header="Identificación"></Column>
        <Column field="numero_contacto" header="# Contacto"></Column>
        <Column field="pais.paises" header="País"></Column>
        <Column field="created_at" header="Fecha creado" sortable></Column>
        <Column field="updated_at" header="Fecha actualizado"></Column>
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
                  text: `Sr. usuario, está seguro que desea editar el cliente: ${slotProps.data.clientes}`,
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
                    nombre = slotProps.data.clientes
                    identificacion = slotProps.data.identificacion
                    telefonos = slotProps.data.numero_contacto
                    Idpais = slotProps.data.pais.pais_id
                    Idclientes = slotProps.data.cliente_id
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
                  text: `Sr. usuario, va desactivar el cliente: ${slotProps.data.clientes}`,
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
                    Idclientes = slotProps.data.cliente_id
                    editarClientesTate()
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
                  text: `Sr. usuario, va activar el cliente: ${slotProps.data.clientes}`,
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
                    Idclientes = slotProps.data.cliente_id
                    editarClientesTate()
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
                  text: `Sr. usuario, va eliminar el cliente: ${slotProps.data.clientes}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'

                }).then(async (result) => {
                  if (result.isConfirmed) {
                    Idclientes = slotProps.data.cliente_id
                    deleteCliente()
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
import Swal from "sweetalert2";                   // optional
const URI_ROOT = import.meta.env.VITE_API_URL;
const nombre = ref('')
const identificacion = ref('')
const telefonos = ref('')
const pais = ref('')
const selectedPais = ref(null)
const Idclientes = ref('')
const Idpais = ref('')
const Idstate = ref('')
const fecha = ref('')
const loading = ref(false)
const mostrarInput = ref(false)
const mostrarBtnUpdate = ref(false)
const mostrarBtnCrear = ref(true)
const clientesTable = ref([])
const paises = ref([])
const filteredPaises = ref([])

const filters = ref({
  global: {value: null, matchMode: FilterMatchMode.CONTAINS},
})

function getFlagLabel(flag) {
  return flag === 1 || flag === true ? 'Activo' : 'Inactivo';
}

onMounted(async () => {
  try {
    await Promise.all([
      loadCLientes(),
      loadPaises()
    ])
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: {error},
      icon: 'error'
    });
  }
})

// Filtra los cargos cuando el usuario escribe
const buscarPais = (event) => {
  loadPaises()
  let query = event.query?.toLowerCase() || ""
  if (!query.length) {
    // 👇 si no hay texto, muestra todos los cargos
    filteredPaises.value = paises.value
  } else {
    filteredPaises.value = paises.value.filter(c =>
      c.paises.toLowerCase().includes(query)
    )
  }
}

function onPaisSeleccionado() {
  if (selectedPais.value) {
    const Wcd = selectedPais.value.pais_id
    Idpais.value = Wcd
  } else {
    Idpais.value = ''
  }
}

async function loadPaises() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargarpaises')
    if (!response.ok) throw new Error('Error')
    paises.value = await response.json() // ✅ .value
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: {error},
      icon: 'error'
    });
  }

}

async function loadCLientes() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargartableclientes');
    clientesTable.value = await response.json()
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: 'No se pudieron cargar los clientes. Intente más tarde.',
      icon: 'error'
    });
  }


}


const handleSubmit = async () => {
  if (!nombre.value || nombre.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor ingrese el nombre del cliente',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (!identificacion.value || identificacion.value.length < 6) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favorvarificar número de identificación debe ser mínimo de 6 digitos',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }

  loading.value = true
  try {
    const response = await fetch(`${URI_ROOT}/api/creaclientes`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        clientes: nombre.value,
        identificacion: identificacion.value,
        numero_contacto: telefonos.value,
        pais_id: Idpais.value,
      })
    })
    console.log(response)

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
      title: '¡Cliente creado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })
    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadCLientes();


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
  identificacion.value = ""
  telefonos.value = ""
  pais.value = ""
  Idpais.value = ""
  Idstate.value = ""
  Idclientes.value = ""
}
async function editarClientes() {
  try {
    if (!nombre.value || nombre.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor ingrese el nombre del cliente',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    } else if (!identificacion.value || identificacion.value.length < 6) {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favorvarificar número de identificación debe ser mínimo de 6 digitos',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    } else if (Idpais.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor ingrese el país del cliente',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }

    const response = await fetch(`${URI_ROOT}/api/updateclientes`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        cliente_id: Idclientes.value,
        clientes: nombre.value,
        identificacion: identificacion.value,
        numero_contacto: telefonos.value,
        pais_id: Idpais.value
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
    await loadCLientes();


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

async function editarClientesTate() {
  try {
    const response = await fetch(`${URI_ROOT}/api/updateclientestate`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        flag: Idstate.value,
        cliente_id: Idclientes.value
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
    await loadCLientes();


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

async function deleteCliente() {
  try {
    const response = await fetch(`${URI_ROOT}/api/deleteclientes/` + Idclientes.value, {
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
    await loadCLientes();


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
