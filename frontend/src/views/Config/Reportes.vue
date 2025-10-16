<template>
  <div class="form-wrapper">
    <h2 class="form-title">REPORTES DIARIOS DE PROGRAMACIÓN</h2>
    <InputText
      v-model="Idclientes"
      type="text"
      readonly
      v-show="mostrarInput"
      class="form-input "
    />
    <InputText
      v-model="Idseriales"
      type="text"
      readonly
      v-show="mostrarInput"
      class="form-input "
    />
    <InputText
      v-model="Idtrabajos"
      type="text"
      readonly
      v-show="mostrarInput"
      class="form-input "
    />
    <InputText
      v-model="Idempleados"
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
    <InputText
      v-model="Idestadocuenta"
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
            <label for="fecha" class="form-label">FECHA</label>
            <InputText
              v-model="fecha"
              id="fecha"
              type="date"
              placeholder="Fecha"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label class="form-label">CLIENTE</label>
            <AutoComplete
              v-model="selectedClientes"
              :suggestions="filteredClientes"
              field="clientes"
              dropdown
              optionValue="cliente_id"
              optionLabel="clientes"
              forceSelection
              placeholder="Escribe y selecciona un cliente"
              class="form-input"
              @complete="buscarClientes"
              @change="onClienteSeleccionado"

            />
          </div>
          <div class="form-field">
            <label class="form-label">SERIAL</label>
            <AutoComplete
              v-model="selectedSerial"
              :suggestions="filteredSerial"
              field="seriales"
              dropdown
              ref="serialref"
              optionValue="serial_id"
              optionLabel="seriales"
              placeholder="Escribe y selecciona un serial"
              class="form-input"
              :forceSelection="false"
              @complete="buscarSerial"
              @change="onSerialSeleccionado"

            />
          </div>
          <div class="form-field">
            <label for="vin" class="form-label">VIN</label>
            <InputText
              v-model="vin"
              id="vin"
              type="text"
              placeholder="Vin"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="motor" class="form-label">MOTOR</label>
            <InputText
              v-model="motor"
              id="motor"
              type="text"
              placeholder="Motor"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label class="form-label">TIPO DE TRABAJO</label>
            <AutoComplete
              v-model="selectedTrabajos"
              :suggestions="filteredTrabajos"
              field="trabajo"
              dropdown
              optionValue="trabajo_id"
              optionLabel="trabajo"
              forceSelection
              placeholder="Tipo de trabajo"
              class="form-input"
              @complete="buscarTrabajo"
              @change="onTrabajoSeleccionado"

            />
          </div>
          <div class="form-field">
            <label for="precio" class="form-label">PRECIO</label>
            <InputText
              v-model="precio"
              id="precio"
              type="number"
              placeholder="Precio"
              class="form-input"
            />
          </div>
          <!--          <div class="form-field">-->
          <!--            <label class="form-label">REALIZADO POR</label>-->
          <!--            <AutoComplete-->
          <!--              v-model="selectedEmpleados"-->
          <!--              :suggestions="filteredEmpleados"-->
          <!--              field="nombre"-->
          <!--              dropdown-->
          <!--              optionValue="empleado_id"-->
          <!--              optionLabel="nombre"-->
          <!--              forceSelection-->
          <!--              placeholder="Realizado por"-->
          <!--              class="form-input"-->
          <!--              @complete="buscarEmpleados"-->
          <!--              @change="onEmpleadoSeleccionado"-->

          <!--            />-->
          <!--          </div>-->
          <div class="form-field">
            <label class="form-label">ESTADO DE PAGO</label>
            <AutoComplete
              v-model="selectedEstadocuenta"
              :suggestions="filteredEstadocuenta"
              field="estado"
              dropdown
              optionValue="estado_id"
              optionLabel="estado"
              forceSelection
              placeholder="Estado de pago"
              class="form-input"
              @complete="buscarEstadocuenta"
              @change="onCuentaSeleccionada"
            />
          </div>
          <div class="form-field">
            <label class="form-label">OBSERVACIÓN</label>
            <InputText
              v-model="observacion"
              id="observ"
              type="text"
              placeholder="Observación"
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
      <h2 class="form-title">LISTADO REPORTES DIARIOS DE PROGRAMACIÓNRR</h2>
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
        :value="reportesTable"
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
        :sortField="'created_at'"
        :sortOrder="-1"
      >
<!--        <Column field="serial_id" header="#" style="width: 80px"></Column>-->
        <Column bodyClass="text-center" field="created_at" header="Fecha" sortable></Column>
        <Column bodyClass="text-center" field="updated_at" header="Cerró" sortable></Column>
        <Column field="clientes.clientes" header="Empresa"></Column>
        <Column bodyClass="text-right" field="seriales" header="# Serial"></Column>
        <Column bodyClass="text-right" field="vin" header="# Vin"></Column>
        <Column bodyClass="text-right" field="motor" header="# Motor"></Column>
        <Column field="trabajo.trabajo" header="Trabajo"></Column>
        <Column field="usuario.usuario_nombre" header="Realizó"></Column>
        <Column bodyClass="text-right" field="precio" header="Precio"></Column>
        <Column bodyClass="text-center" field="flag" header="Estado">
          <template #body="slotProps">
            {{ getFlagLabel(slotProps.data.flag) }}
          </template>
        </Column>
        <Column bodyClass="text-center" field="estado.estado" header="Cuenta"></Column>
        <Column field="observacion" header="Observación"></Column>
        <Column field="flag" header="Acciones" style="width: 150px">
          <template #body="slotProps">
            <div v-if="slotProps.data.flag === 1 || slotProps.data.flag === true">
              <Button
                icon="pi pi-pencil icon-xl"
                title="Editar"
                v-show="mostrarBtnEditar"
                severity="info"
                text
                rounded
                @click="() => {
                 Swal.fire({
                  title: 'Confirmación',
                  text: `Sr. usuario, está seguro que desea editar el cliente: ${slotProps.data.clientes.clientes}`,
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
                    const fechaConHora = slotProps.data.created_at
                    fecha = fechaConHora.split('T')[0]
                    selectedClientes = slotProps.data.clientes.clientes
                    Idclientes = slotProps.data.clientes.cliente_id
                    selectedSerial = slotProps.data.seriales
                    Idseriales = slotProps.data.serial_id
                    vin = slotProps.data.vin
                    motor = slotProps.data.motor
                    selectedTrabajos = slotProps.data.trabajo
                    Idtrabajos = slotProps.data.trabajo_id
                    precio = slotProps.data.precio
                    selectedEmpleados = slotProps.data.empleado.nombre
                    Idempleados = slotProps.data.usuario_id
                    Idestadocuenta = slotProps.data.estado.estado_id
                    selectedEstadocuenta = slotProps.data.estado.estado
                    observacion = slotProps.data.observacion
                  }
                });
              }"
              />
              <Button
                v-if="slotProps.data.flag === 1 || slotProps.data.flag === true"
                icon="pi pi-check-circle icon-xl"
                v-show="mostrarBtnCerrar"
                title="Cerrar"
                severity="danger"
                back
                text
                rounded
                @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de cerrar el servicio?',
                  text: `Sr. usuario, va cerrar el servicio: ${slotProps.data.clientes.clientes}`,
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
                    Idseriales = slotProps.data.serial_id
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
                v-show="mostrarBtnActivar"
                back
                text
                rounded
                @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de activar el servicio?',
                  text: `Sr. usuario, va activar el servicio: ${slotProps.data.clientes.clientes}`,
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
                    Idseriales = slotProps.data.serial_id
                    editarClientesTate()
                  }
                });
              }"
              />
              <Button
                icon="pi pi-trash icon-xl"
                title="Eliminar"
                severity="danger"
                v-show="mostrarBtnEliminar"
                back
                text
                rounded
                @click="() => {
                 Swal.fire({
                  title: '¿Estás seguro de eliminar?',
                  text: `Sr. usuario, va eliminar el cliente: ${slotProps.data.clientes.clientes} con serial: ${slotProps.data.seriales}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'

                }).then(async (result) => {
                  if (result.isConfirmed) {
                    Idseriales = slotProps.data.serial_id
                    deleteCliente()
                  }
                });
              }"
              />
            </div>
          </template>
        </Column>
      </DataTable>
      <!--        </div>-->
    </section>
  </div>
</template>

<script setup lang="ts">
import {onMounted, ref, computed} from 'vue'
import {FilterMatchMode} from 'primevue/api'
import {useAuthStore} from "@/stores/auth.js"
import Swal from "sweetalert2";

const auth = useAuthStore()
const URI_ROOT = import.meta.env.VITE_API_URL;
const vin = ref('')
const serial = ref('')
const motor = ref('')
const precio = ref('')
const serialref = ref(null);
const selectedClientes = ref(null)
const selectedSerial = ref(null)
const selectedTrabajos = ref(null)
const selectedEmpleados = ref(null)
const selectedEstadocuenta = ref(null)
const Idclientes = ref('')
const Idseriales = ref('')
const Idtrabajos = ref('')
const Idempleados = ref('')
const observacion = ref('')
const Idestadocuenta = ref('')
const Idstate = ref('')
const fecha = ref('')
const loading = ref(false)
const mostrarInput = ref(false)
const mostrarBtnUpdate = ref(false)
const mostrarBtnCrear = ref(true)
const mostrarBtnEditar = ref(true)
const mostrarBtnActivar = ref(true)
const mostrarBtnEliminar = ref(true)
const mostrarBtnCerrar = ref(true)
const mostrarColumnaAcciones = ref(false)
const reportesTable = ref([])
const seriales = ref([])
const clientes = ref([])
const trabajos = ref([])
const empleados = ref([])
const estadoCuenta = ref([])
const filteredClientes = ref([])
const filteredTrabajos = ref([])
const filteredSerial = ref([])
const filteredEmpleados = ref([])
const filteredEstadocuenta = ref([])
const nombrcliente = ref('')
const filters = ref({
  global: {value: null, matchMode: FilterMatchMode.CONTAINS},
})

const Puede = auth.permisos?.CReportes
if(Puede.crear == false){
  mostrarBtnCrear.value = false
  mostrarBtnCerrar.value = false
}
if(Puede.editar == false){
  mostrarBtnUpdate.value = false
  mostrarBtnEditar.value = false
  mostrarBtnActivar.value = false
}

if(Puede.eliminar == false){
  mostrarBtnEliminar.value = false
}

// Fecha actual como objeto Date
const fechaActual = new Date().toLocaleDateString('en-CA');
// Formateada como cadena legible (ej. "2025-10-08")
const fechaFormateada = fechaActual.split('T')[0];
AsignarFechas()

function getFlagLabel(flag) {
  return flag === 1 || flag === true ? 'En proceso' : 'Cerrado';
}

onMounted(async () => {
  try {
    await Promise.all([
      loadClientes(),
      loadTrabajos(),
      loadEmpleados(),
      loadEstadocuenta(),
      loadTableReportes()
    ])
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: {error},
      icon: 'error'
    });
  }
})

function AsignarFechas(){
  fecha.value = fechaFormateada.toString()

}
function obtenerValorEscrito() {
  const input = serialref.value?.$el?.querySelector('input');
  return input ? input.value : '';
}

function onClienteSeleccionado() {
  if (selectedClientes.value) {
    Idclientes.value = selectedClientes.value.cliente_id
    if (!Idclientes.value || Idclientes.value.trim() === '') {

    } else {
      filteredSerial.value = [];
      loadSerial()
    }
  } else {
    Idclientes.value = ''
  }
}

function onCuentaSeleccionada() {
  if (selectedEstadocuenta.value) {
    Idestadocuenta.value = selectedEstadocuenta.value.estado_id
    if (!Idestadocuenta.value || String(Idestadocuenta.value).trim() === '') {

    }
  } else {
    Idestadocuenta.value = ''
  }
}

function onTrabajoSeleccionado() {
  if (selectedTrabajos.value) {
    Idtrabajos.value = selectedTrabajos.value.trabajo_id
    if (!Idtrabajos.value || Idtrabajos.value.trim() === '') {

    }
  } else {
    Idtrabajos.value = ''
  }
}

function onSerialSeleccionado() {
  const serialEscrito = obtenerValorEscrito();
  if (selectedSerial.value.seriales) {
    Idseriales.value = selectedSerial.value.serial_id
    serial.value = selectedSerial.value.seriales
  } else {
    Idseriales.value = ''
    serial.value = serialEscrito
  }
}

function onEmpleadoSeleccionado() {
  if (selectedEmpleados.value) {
    Idempleados.value = selectedEmpleados.value.empleado_id
    if (!Idempleados.value || Idempleados.value.trim() === '') {

    }
  } else {
    Idempleados.value = ''
  }
}

// Filtra los cargos cuando el usuario escribe
const buscarClientes = (event) => {
  loadClientes()
  let query = event.query?.toLowerCase() || ""
  if (!query.length) {
    // 👇 si no hay texto, muestra todos los cargos
    filteredClientes.value = clientes.value
  } else {
    filteredClientes.value = clientes.value.filter(c =>
      c.clientes.toLowerCase().includes(query)
    )
  }
}

const buscarSerial = (event) => {
  loadSerial()
  let query = event.query?.toLowerCase() || ""
  if (!query.length) {
    // 👇 si no hay texto, muestra todos los cargos
    filteredSerial.value = seriales.value
  } else {
    filteredSerial.value = seriales.value.filter(c =>
      c.seriales.toLowerCase().includes(query)
    )
  }
}

const buscarEstadocuenta = (event) => {
  loadEstadocuenta()
  let query = event.query?.toLowerCase() || ""
  if (!query.length) {
    // 👇 si no hay texto, muestra todos los cargos
    filteredEstadocuenta.value = estadoCuenta.value
  } else {
    filteredEstadocuenta.value = estadoCuenta.value.filter(c =>
      c.estado.toLowerCase().includes(query)
    )
  }
}
const buscarEmpleados = (event) => {
  loadEmpleados()
  let query = event.query?.toLowerCase() || ""
  if (!query.length) {
    // 👇 si no hay texto, muestra todos los cargos
    filteredEmpleados.value = empleados.value
  } else {
    filteredEmpleados.value = empleados.value.filter(c =>
      c.nombre.toLowerCase().includes(query)
    )
  }
}
const buscarTrabajo = (event) => {
  loadTrabajos()
  let query = event.query?.toLowerCase() || ""
  if (!query.length) {
    // 👇 si no hay texto, muestra todos los cargos
    filteredTrabajos.value = trabajos.value
  } else {
    filteredTrabajos.value = trabajos.value.filter(c =>
      c.trabajo.toLowerCase().includes(query)
    )
  }
}

async function loadClientes() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargarclientes')
    if (!response.ok) throw new Error('Error')
    clientes.value = await response.json() // ✅ .value
  } catch (error) {
    // Swal.fire({
    //   title: 'Error',
    //   text: {error},
    //   icon: 'error'
    // });
  }
}

async function loadTrabajos() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargartrabajos')
    if (!response.ok) throw new Error('Error')
    trabajos.value = await response.json() // ✅ .value
  } catch (error) {
    // Swal.fire({
    //   title: 'Error',
    //   text: {error},
    //   icon: 'error'
    // });
  }

}

async function loadSerial() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargarserialcliente/' + Idclientes.value)
    if (!response.ok) throw new Error('Error')
    seriales.value = await response.json() // ✅ .value
  } catch (error) {
    // Swal.fire({
    //   title: 'Error',
    //   text: {error},
    //   icon: 'error'
    // });
  }

}

async function loadEmpleados() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargarempleados')

    if (!response.ok) throw new Error('Error')
    empleados.value = await response.json() // ✅ .value
  } catch (error) {
    // Swal.fire({
    //   title: 'Error',
    //   text: {error},
    //   icon: 'error'
    // });
  }

}

async function loadEstadocuenta() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargarestadocuenta')
    if (!response.ok) throw new Error('Error')
    estadoCuenta.value = await response.json() // ✅ .value
  } catch (error) {
    // Swal.fire({
    //   title: 'Error',
    //   text: {error},
    //   icon: 'error'
    // });
  }

}

async function loadTableReportes() {
  try {
    const UsuarioID = auth.user?.usuario_id
    const response = await fetch(URI_ROOT + '/api/cargartablereportes/'+ UsuarioID);
    reportesTable.value = await response.json()
  } catch (error) {
    // Swal.fire({
    //   title: 'Error',
    //   text: 'No se pudieron cargar los clientes. Intente más tarde.',
    //   icon: 'error'
    // });
  }


}


const handleSubmit = async () => {
  Idempleados.value = auth.user?.usuario_id
  if (Idclientes.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor ingrese el nombre del cliente',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (Idtrabajos.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor varificar tipo de trabajo no coincide',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (Idempleados.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor verificar el nombre del técnico',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (precio.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor verificar el valor del servicio',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (String(Idestadocuenta.value).trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor verificar el estado de pago',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }
  nombrcliente.value = selectedClientes.value.clientes
  loading.value = true
  try {
    const response = await fetch(`${URI_ROOT}/api/creareportes`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        fecha_servicio: fecha.value,
        cliente_id: Idclientes.value,
        seriales: serial.value,
        vin: vin.value,
        motor: motor.value,
        trabajo_id: Idtrabajos.value,
        precio: precio.value,
        // empleado_id: Idempleados.value,
        estado_id: Idestadocuenta.value,
        observacion: observacion.value,
        usuario_id: auth.user?.usuario_id
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
      title: '¡Cliente creado!',
      text: `"Reporte de ${nombrcliente.value} con serial ${serial.value} registrado correctamente"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151'
    })
    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTableReportes();


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

function limpiarForm() {
  fecha.value = ""
  vin.value = ""
  motor.value = ""
  motor.value = ""
  selectedClientes.value = ""
  selectedSerial.value = ""
  selectedTrabajos.value = ""
  selectedEmpleados.value = ""
  selectedEstadocuenta.value = ""
  Idstate.value = ""
  Idtrabajos.value = ""
  Idclientes.value = ""
  Idseriales.value = ""
  Idempleados.value = ""
  observacion.value = ""
  Idestadocuenta.value = ""
  precio.value = ""
  seriales.value = []
  AsignarFechas()

}

async function editarClientes() {
  try {
    if (!fecha.value || fecha.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor ingrese la fecha',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    } else if (!Idclientes.value) {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor varificar nombre de cliente',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    } else if (Idtrabajos.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor verifique el tipo de trabajo',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    } else if (precio.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor verifique valor del servicio',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    } else if (Idempleados.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor verifique nombre del técnico',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }
    console.log(auth.user?.usuario_id)
    const response = await fetch(`${URI_ROOT}/api/updatereportes`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        serial_id: Idseriales.value,
        fecha_servicio: fecha.value,
        cliente_id: Idclientes.value,
        seriales: selectedSerial.value,
        vin: vin.value,
        motor: motor.value,
        trabajo_id: Idtrabajos.value,
        precio: precio.value,
        empleado_id: Idempleados.value,
        estado_id: Idestadocuenta.value,
        observacion: observacion.value,
        updated_usuario_id: auth.user?.usuario_id

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
      title: '¡Reporte actualizado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTableReportes();


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
    const response = await fetch(`${URI_ROOT}/api/updatereportestate`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        flag: Idstate.value,
        serial_id: Idseriales.value
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
    await loadTableReportes();


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
    const response = await fetch(`${URI_ROOT}/api/deletereportes/` + Idseriales.value, {
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
      title: '¡Reporte eliminado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151'

    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTableReportes();


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
