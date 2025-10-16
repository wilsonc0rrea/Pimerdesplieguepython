<template>
  <div class="form-wrapper">
    <h2 class="form-title">CREAR REPORTES DIARIOS DE PROGRAMACIÓN</h2>
    <form @submit.prevent="handleSubmit" class="form-grid">
      <div class="form-field half">
        <label for="fecha">FECHA</label>
        <InputText v-model="fecha" id="fecha" autocomplete="off" type="date"/>
      </div>
      <div class="form-field half">
        <label for="cliente">CLIENTE</label>
        <InputText v-model="cliente" id="cliente" name="cliente"/>
      </div>
      <div class="form-field small">
        <label for="serial">SERIAL</label>
        <InputText v-model="serial" id="serial"/>
      </div>
      <div class="form-field half">
        <label for="vin">VIN</label>
        <InputText v-model="vin" id="vin"/>
      </div>
      <div class="form-field half">
        <label for="motor">MOTOR</label>
        <InputText v-model="motor" id="motor"/>
      </div>
      <div class="form-field half">
        <label for="ttrabajo">TIPO DE TRABAJO</label>
        <Dropdown v-model="ttrabajo" id="ttrabajo"
                  option-value="value" placeholder="Seleccione el tipo de trabajo"/>
      </div>
      <div class="form-field half">
        <label for="precio">PRECIO</label>
        <InputText v-model="precio" id="precio"/>
      </div>
      <div class="form-field half">
        <label for="tecnico">TÉCNICO</label>
        <Dropdown v-model="tecnico" id="tecnico"
                  option-value="value" placeholder="Seleccione el técnico"/>
      </div>
      <div class="form-field half">
        <Button
          type="submit"
          label="Crear..."
          icon="pi pi-user-plus"
          :loading="loading"
        />
      </div>
    </form>
    <div>
      <!-- DATATABLE -->
      <div class="form-field full">
        <!--        <div class="datatable-card">-->
        <h2 class="form-title">LISTADO REPORTES DIARIOS DE PROGRAMACIÓN</h2>
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
          :value="clientes"
          :filters="filters"
          :paginator="true"
          :rows="60"
          paginator
          scrollable
          scrollHeight="400px"
          responsive-layout="scroll"
          filterDisplay="menu"
          striped-rows
          currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords} registros"
          paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
          class="custom-datatable"
        >
          <Column field="id" header="#" style="width: 60px"></Column>
          <Column field="nombre" header="Nombre"></Column>
          <Column field="email" header="Correo"></Column>
          <Column field="telefono" header="Teléfono"></Column>
          <Column header="Acciones" style="width: 150px">
            <template #body="slotProps">
              <Button
                icon="pi pi-pencil"
                severity="info"
                text
                rounded
                @click="editarCliente(slotProps.data)"
              />
              <Button
                icon="pi pi-trash"
                severity="danger"
                text
                rounded
                @click="eliminarCliente(slotProps.data.id)"
              />
            </template>
          </Column>
        </DataTable>
        <!--        </div>-->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Button from 'primevue/button'
import {FilterMatchMode} from 'primevue/api'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';
import Swal from "sweetalert2";
import {useRouter} from "vue-router";                   // optional
const loading = ref(false)
const router = useRouter()

const clientes = ref([
  {id: 1, nombre: 'Juan Pérez', email: 'juan@mail.com', telefono: '3001234567'},
  {id: 2, nombre: 'Ana Gómez', email: 'ana@mail.com', telefono: '3109876543'},
])

const filters = ref({
  global: {value: null, matchMode: FilterMatchMode.CONTAINS},
})

const agregarCliente = () => alert('Abrir modal para agregar cliente')
const editarCliente = (cliente) => {
  Swal.fire({
    title: 'Confirmación',
    text: `Sr. usuario, está seguro que desea editar a: ${cliente.nombre}`,
    icon: 'info',
    confirmButtonText: 'Aceptar',
    confirmButtonColor: '#ef4444'
  })
}
const eliminarCliente = (id) => alert(`Eliminar cliente con id ${id}`)

const selectedDate = ref(null)
const fecha = ref('')
const cliente = ref('')
const serial = ref('')
const precio = ref('')
const tecnico = ref('')
const vin = ref('')
const motor = ref('')
const ttrabajo = ref('')
const fechaInvalida = ref(false)

const handleSubmit = async () => {
  if (!fecha.value) {
    Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor verificar fecha en blanco',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }else if(!cliente.value || cliente.value.length < 6){
    Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor verificar nombre de cliente',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }else if(!ttrabajo.value){
    Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor verificar tipo de trabajo en blanco',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }else{

    loading.value = true
    try {

      const response = await fetch('http://localhost:8000/api/crearusuario', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fecha: fecha.value,
          cliente: cliente.value,
          serial: serial.value,
          precio: precio.value,
          tecnico: tecnico.value,
          vin: vin.value,
          motor: motor.value,
          ttrabajo: ttrabajo.value,
        })
      })

      if (!response.ok) {
        let errorDetail = 'Error desconocido'
        try {
          const errorData = await response.json()
          errorDetail = errorData.detail || JSON.stringify(errorData)
        } catch (e) {
          errorDetail = await response.text()
        }
        throw new Error(`Error ${response.status}: ${errorDetail}`)
      }
      const data = await response.json()
      // ✅ ¡Aquí actualizamos el estado global!
      login(data.access_token || 'fake-token') // 👈 ¡Esto es clave!
      Swal.fire({
        title: '¡Bienvenido!',
        text: 'Has iniciado sesión correctamente',
        icon: 'success',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#3b82f6',
        timer: 2000,
        timerProgressBar: true
      }).then(() => {

      })

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
}

</script>
