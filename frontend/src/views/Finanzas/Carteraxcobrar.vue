<template>
  <div class="form-wrapper">
    <h2 class="form-title">CARTERA POR COBRAR</h2>
    <InputText
      v-model="Idcuentabancaria"
      type="text"
      readonly
      v-show="mostrarInput"
      class="form-input "
    />
    <InputText
      v-model="Idcuentadestino"
      type="text"
      readonly
      v-show="mostrarInput"
      class="form-input "
    />
    <InputText
      v-model="Idclientes"
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
            <label for="cliente" class="form-label">CLIENTE</label>
            <InputText
              v-model="clientes"
              id="cliente"
              type="text"
              readonly="true"
              placeholder="Costo servicio"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="costo" class="form-label">COSTO SERVICIO</label>
            <InputText
              v-model="costo"
              id="costo"
              type="text"
              readonly="true"
              placeholder="Costo servicio"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="abonado" class="form-label">COSTO ABONADO</label>
            <InputText
              v-model="abonado"
              id="abonado"
              type="number"
              min="0"
              step="0.01"
              autofocus fluid
              @input="actualizarPrecio"
              placeholder="Costo abonado"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="total" class="form-label">SALDO TOTAL</label>
            <InputText
              v-model="total"
              id="total"
              type="text"
              readonly="true"
              placeholder="Saldo total"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label class="form-label">MEDIO DE PAGO</label>
            <AutoComplete
              v-model="selectedCuentabancaria"
              :suggestions="filteredCuentabancaria"
              field="cuenta"
              dropdown
              optionValue="cuenta_id"
              optionLabel="cuenta"
              forceSelection
              placeholder="Cuenta bancaria"
              class="form-input"
              @complete="buscarCuentabancaria"
              @change="onCuentabancariaSeleccionado"

            />
          </div>
          <div class="form-field">
            <label class="form-label">CUENTA DE DESTINO</label>
            <AutoComplete
              v-model="selectedCuentadestino"
              :suggestions="filteredCuentadestino"
              field="cuenta_destino"
              dropdown
              optionValue="cuentadestino_id"
              optionLabel="cuenta_destino"
              forceSelection
              placeholder="Cuenta destino"
              class="form-input"
              @complete="buscarCuentadestino"
              @change="onCuentadestinoSeleccionado"

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
      <h2 class="form-title">LISTADO DE CARTERA POR COBRAR</h2>
      <div class="datatable-header">
        <div>
           <span class="p-input-icon-left">
              <InputText
                v-model="filters.global.value"
                placeholder="Buscar..."
                class="p-inputtext-sm"
              />
            </span>
        </div>
        <div>
          <Button
            label="Exportar a PDF"
            icon="pi pi-file-pdf"
            class="form-button"
            @click="exportToPDF"
          />
        </div>

      </div>

      <DataTable
        :value="tableCuentaxcobrar"
        :filters="filters"
        :total-records="totalRecords"
        :paginator="true"
        :rows="60"
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
        <Column field="cliente_id" header="#" style="width: 60px; alin"></Column>
        <Column field="clientes" header="Cliente" sortable></Column>
        <Column bodyClass="text-right" field="debe" header="Debe" sortable></Column>
        <Column bodyClass="text-right" field="haber" header="Haber" sortable></Column>
        <Column bodyClass="text-right" field="saldo" header="Saldo"></Column>
        <Column field="flag" header="Estado" sortable>
          <template #body="slotProps">
            {{ getFlagLabel(slotProps.data.saldo) }}
          </template>
        </Column>
        <Column class="text-center" field="flag" header="Acciones" style="width: 150px">
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
                    limpiarForm()
                    Idclientes = slotProps.data.cliente_id
                    clientes = slotProps.data.clientes
                    let ValidaHaber = slotProps.data.haber
                    total= slotProps.data.saldo

                    if(ValidaHaber >0){
                      costo= slotProps.data.saldo
                    }else{
                      costo= slotProps.data.debe
                    }
                  }
                });
              }"
            />
            <Button
              icon="pi pi-eye icon-xl"
              title="Detalle"
              severity="info"
              text
              rounded
              @click="() => {
                modalVisible = true
                Idclientes = slotProps.data.cliente_id
                clientes = slotProps.data.clientes
                loadTableservicios()
              }"
            />

          </template>
        </Column>
      </DataTable>
      <!--        </div>-->
    </section>
  </div>
  <template>
    <!-- Modal principal -->
    <Dialog
      v-model:visible="modalVisible"
      modal
      :style="{ width: '95vw', maxWidth: '1200px' }"
      :breakpoints="{ '768px': '95vw' }"
      :draggable="false"
      :closable="true"
      :close-on-escape="true"
      @update:visible="onModalClose"
      class="p-dialog-custom"
    >
      <template #header>
        <div class="flex items-center gap-3">
          <h2 class="text-xl font-bold text-gray-800">SERVICIOS PRESTADOS</h2>
        </div>
      </template>

      <!-- ✅ TU CONTENIDO EXISTENTE AQUÍ (sin el h2 principal) -->
      <div class="form-wrapper max-h-[70vh] overflow-y-auto px-2">
        <!-- Inputs ocultos -->
        <InputText v-model="Idseriales" type="text" readonly v-show="mostrarInput" class="hidden"/>
        <InputText v-model="Idservicio" type="text" readonly v-show="mostrarInput" class="hidden"/>

        <!-- Formulario -->
        <section class="form-section mb-6">
          <form @submit.prevent="handleSubmit" class="form-inline">
            <div class="form-row">
              <!-- Tus campos existentes -->
              <div class="form-field">
                <label for="clienteserv" class="form-label">CLIENTE</label>
                <InputText
                  v-model="clienteservicio"
                  id="clienteserv"
                  type="text"
                  readonly
                  placeholder="Cliente"
                  class="form-input"
                />
              </div>
              <div class="form-field">
                <label for="costoservicio" class="form-label">COSTO SERVICIO</label>
                <InputText
                  v-model="costoservicio"
                  id="costoservicio"
                  type="number"
                  min="0"
                  step="0.01"
                  autofocus
                  placeholder="Costo servicio"
                  class="form-input"
                />
              </div>
              <div class="form-field">
                <label for="serial" class="form-label">SERIAL</label>
                <InputText
                  v-model="serialservicio"
                  id="serial"
                  readonly
                  placeholder="Serial"
                  class="form-input"
                />
              </div>
              <div class="form-field">
                <label for="servicio" class="form-label">SERVICIO</label>
                <InputText
                  v-model="servicioxcobrar"
                  id="servicio"
                  readonly
                  placeholder="Servicio"
                  class="form-input"
                />
              </div>
              <div class="text-center form-field action-field">
                <label class="form-label invisible">ACCIONES</label>
                <Button
                  type="button"
                  label="Actualizar..."
                  v-show="mostrarBtnUpdateServicio"
                  icon="pi pi-user-plus"
                  :loading="loading"
                  class="form-button"
                  @click="() => {
                    editarServicios()
                  }"
                />
              </div>
            </div>
          </form>
        </section>

        <!-- DataTable -->
        <section class="form-section">

          <h3 class="form-title text-lg font-semibold mb-3">LISTADO DE CARTERA POR COBRAR</h3>
          <div class="datatable-header mb-3">
          <span class="p-input-icon-left">
            <InputText
              v-model="filters.global.value"
              placeholder="Buscar..."
              class="p-inputtext-sm w-full md:w-64"
            />
          </span>
          </div>

          <DataTable
            :value="tableServiciosxcobrar"
            :filters="filters"
            :paginator="true"
            :rows="60"
            paginator
            responsive-layout="scroll"
            filterDisplay="menu"
            striped-rows
            currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords}"
            paginator-template="RowsPerPageDropdown FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport"
            :sortField="'created_at'"
            :sortOrder="-1"
            style="font-size: 0.875rem"
          >
            <Column field="clientes.clientes" header="Cliente" sortable></Column>
            <Column bodyClass="text-right" field="seriales" header="# Serial"></Column>
            <!--            <Column bodyClass="text-right" field="vin" header="# Vin"></Column>-->
            <!--            <Column bodyClass="text-right" field="motor" header="# Motor"></Column>-->
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
                <Button
                  icon="pi pi-pencil icon-xl"
                  title="Editar"
                  severity="info"
                  text
                  rounded
                  @click="() => {
                 Swal.fire({
                  title: 'Confirmación',
                  text: `Sr. usuario, está seguro que desea editar el cliente: ${slotProps.data.clientes.clientes} con el servicio ${slotProps.data.trabajo.trabajo}`,
                  icon: 'info',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar',
                  customClass: {
                    container: 'swal-overlay-high'
                  }
                }).then(async (result) => {
                  if (result.isConfirmed) {
                    limpiarFormServicio()
                    mostrarBtnUpdateServicio = true
                    Idseriales = slotProps.data.serial_id
                    clienteservicio = slotProps.data.clientes.clientes
                    costoservicio= slotProps.data.precio
                    serialservicio =slotProps.data.seriales
                    Idservicio =slotProps.data.trabajo.trabajo_id
                    servicioxcobrar =slotProps.data.trabajo.trabajo

                  }
                });
              }"
                />

              </template>
            </Column>
          </DataTable>
        </section>
      </div>

      <template #footer>
        <div class="flex justify-end">
          <Button
            label="Cerrar"
            severity="secondary"
            @click="closeModal"
            class="px-4 py-2"
          />
        </div>
      </template>
    </Dialog>
  </template>


</template>

<script setup lang="ts">
// @ts-nocheck
import {onMounted, ref, computed} from 'vue'
import {FilterMatchMode} from 'primevue/api'
import FocusTrap from 'primevue/focustrap';
import {useAuthStore} from "@/stores/auth.js"
import jsPDF from 'jspdf';
import autoTable from "jspdf-autotable";
import Swal from "sweetalert2";
import logo from "@/assets/image/logo/mLogo.png"
import Image from "primevue/image";

const auth = useAuthStore()
const URI_ROOT = import.meta.env.VITE_API_URL;
const costo = ref(0)
const costoservicio = ref(0)
const abonado = ref('')
const total = ref(0)
const clientes = ref('')
const clienteservicio = ref('')
const modalVisible = ref(false);
const serialservicio = ref('')
const servicioxcobrar = ref('')
const Idservicio = ref('')
const Idcuentabancaria = ref('')
const Idcuentadestino = ref('')
const Idclientes = ref('')
const Idseriales = ref('')
const loading = ref(false)
const mostrarInput = ref(false)
const mostrarBtnUpdate = ref(false)
const mostrarBtnCrear = ref(true)
const mostrarBtnUpdateServicio = ref(true)

const selectedCuentabancaria = ref(null)
const selectedCuentadestino = ref(null)
const filteredCuentabancaria = ref([])
const filteredCuentadestino = ref([])

const cuentas = ref([])
const cuentadestino = ref([])
const tableCuentaxcobrar = ref([])
const tableServiciosxcobrar = ref([])
let totalRecords = ref(0);
let valor = 0
let Costo = 0
let Saldo = 0
let dataSaldos

const closeModal = () => {
  modalVisible.value = false;
};

const onModalClose = (visible: boolean) => {
  if (!visible) {
    limpiarForm();
    loadTableCuentasxcobrar()
  }
};

const filters = ref({
  global: {value: null, matchMode: FilterMatchMode.CONTAINS},
})

function getFlagLabel(saldo) {
  return saldo > 0 ? 'En proceso' : 'Cancelado';
}


onMounted(async () => {
  await loadCuentabancaria();
  await loadCuentadestino();
  await loadTableCuentasxcobrar();
})
totalRecords = computed(() => tableCuentaxcobrar.value.length);

function onCuentabancariaSeleccionado() {
  if (selectedCuentabancaria.value) {
    Idcuentabancaria.value = selectedCuentabancaria.value.cuenta_id
    if (!Idcuentabancaria.value) {
      // return Swal.fire({
      //   title: 'Error',
      //   text: 'Sr. usuario por favor varificar datos del cliente',
      //   icon: 'error',
      //   confirmButtonText: 'Aceptar',
      //   confirmButtonColor: '#ef4444'
      // })
    }
  } else {
    Idcuentabancaria.value = ''
  }
}

function onCuentadestinoSeleccionado() {
  if (selectedCuentadestino.value) {
    Idcuentadestino.value = selectedCuentadestino.value.cuentadestino_id
    if (!Idcuentadestino.value) {
      // return Swal.fire({
      //   title: 'Error',
      //   text: 'Sr. usuario por favor varificar datos del cliente',
      //   icon: 'error',
      //   confirmButtonText: 'Aceptar',
      //   confirmButtonColor: '#ef4444'
      // })
    }
  } else {
    Idcuentadestino.value = ''
  }
}

const buscarCuentabancaria = (event) => {
  loadCuentabancaria()
  let query = event.query?.toLowerCase() || ""
  if (!query.length) {
    // 👇 si no hay texto, muestra todos los cargos
    filteredCuentabancaria.value = cuentas.value
  } else {
    filteredCuentabancaria.value = cuentas.value.filter(c =>
      c.cuenta.toLowerCase().includes(query)
    )
  }
}

const buscarCuentadestino = (event) => {
  loadCuentadestino()
  let query = event.query?.toLowerCase() || ""
  if (!query.length) {
    // 👇 si no hay texto, muestra todos los cargos
    filteredCuentadestino.value = cuentadestino.value
  } else {
    filteredCuentadestino.value = cuentadestino.value.filter(c =>
      c.cuenta_destino.toLowerCase().includes(query)
    )
  }
}

// Procesa el input del precio
function actualizarPrecio(event) {
  valor = event.target.value;
  Costo = costo.value
  Saldo = costo.value
  valor = parseFloat(valor)
  let Total = 0
  // Validar que sea un número válido
  if (isNaN(valor) || valor <= 0) {
    Swal.fire({
      title: 'Error',
      text: 'Por favor, ingresa un monto válido mayor a 0.',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      icon: 'error'
    }).then(() => {
      console.log("Costo" + Costo)
      total.value = Costo
    });
  }
  // Validar que no supere el saldo
  if (valor > Costo) {
    Swal.fire({
      title: 'Error',
      text: `El monto ${valor} excede el saldo ${Costo} disponible.`,
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      icon: 'error'
    }).then(() => {
      total.value = Costo
    });
  }
  // Si todo está bien, descontar
  Saldo -= valor;
  total.value = Saldo

}

async function loadCuentabancaria() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargarmediopago');
    cuentas.value = await response.json()
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: 'No se pudieron cargar los cargos. Intente más tarde.',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      icon: 'error'
    });
  }
}

async function loadCuentadestino() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargarcuentadestino');
    cuentadestino.value = await response.json()
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: 'No se pudieron cargar los cargos. Intente más tarde.',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      icon: 'error'
    });
  }
}

async function loadTableCuentasxcobrar() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargartablecarteraxcobrar');
    tableCuentaxcobrar.value = await response.json()
    dataSaldos = Array.isArray(tableCuentaxcobrar.value)
      ? tableCuentaxcobrar.value
      : [];


  } catch (error) {

  }
}

async function loadTableservicios() {
  try {

    const response = await fetch(`${URI_ROOT}/api/cargartableservicioxcobrar/` + Idclientes.value)

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
    tableServiciosxcobrar.value = await response.json()
    limpiarFormServicio()


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
  costo.value = ""
  clientes.value = ""
  abonado.value = ""
  total.value = ""
  selectedCuentabancaria.value = ""
  selectedCuentadestino.value = ""
  Idcuentadestino.value = ""
  Idcuentabancaria.value = ""
  Idclientes.value = ""
}

function limpiarFormServicio() {
  costoservicio.value = ""
  clienteservicio.value = ""
  serialservicio.value = ""
  Idseriales.value = ""
  servicioxcobrar.value = ""
  Idservicio.value = ""
}

async function editarServicios() {
  const costo = costoservicio.value;
  try {
    if (!Idseriales.value || Idseriales.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor el movimiento',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444',
        customClass: {
          container: 'swal-overlay-high'
        }
      })
    } else if (!clienteservicio.value || clienteservicio.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor varificar nombre de cliente',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444',
        customClass: {
          container: 'swal-overlay-high'
        }
      })
    } else if (!costo || isNaN(Number(costo)) || Number(costo) < 0) {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor verifique el nuevo valor',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444',
        customClass: {
          container: 'swal-overlay-high'
        }
      })
    }

    const response = await fetch(`${URI_ROOT}/api/updatereporteserviciosxcobrar`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        serial_id: Idseriales.value,
        precio: costoservicio.value,
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
      title: '¡Servicio actualizado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true,
      customClass: {
        container: 'swal-overlay-high'
      }

    })

    limpiarFormServicio()
    // ✅ ¡Recarga la tabla!
    await loadTableservicios();
    await loadTableCuentasxcobrar();


  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: error.message || 'No se pudo conectar con el servidor',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444',
      customClass: {
        container: 'swal-overlay-high'
      }
    })
  } finally {
    loading.value = false
  }
}


const handleSubmit = async () => {
  const servicio = costo.value;
  const abonos = abonado.value;
  const saldos = total.value;
  const mediopago = Idcuentabancaria.value;
  const cuentadestino = Idcuentadestino.value;
  if (!servicio || isNaN(Number(servicio)) || Number(servicio) < 0) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor ingrese el costo del servicio',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (!abonos || isNaN(Number(abonos)) || Number(abonos) < 0) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor ingrese el valor de lo abonado',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (!saldos || isNaN(Number(saldos)) || Number(saldos) < 0) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor verificar el saldo final',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (!Idclientes.value || Idclientes.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor ingrese el nombre del cliente',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (!mediopago || isNaN(Number(mediopago)) || Number(mediopago) < 0) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor ingrese medio de pago',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (!cuentadestino || isNaN(Number(cuentadestino)) || Number(cuentadestino) < 0) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor ingrese la cuenta de destino',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }

  loading.value = true
  try {
    const response = await fetch(`${URI_ROOT}/api/creacarteraxcobrar`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        cliente_id: Idclientes.value,
        debe: costo.value,
        haber: abonado.value,
        usuario_id: auth.user?.usuario_id,
        clientes: clientes.value,
        cuenta_id: Idcuentabancaria.value,
        cuentadestino_id: Idcuentadestino.value
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
      title: '¡Cartera x cobrar creada!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTableCuentasxcobrar();


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

function loadImagePDF(src) {
  return new Promise((resolve, reject) => {
    const img = new window.Image();
    img.crossOrigin = 'Anonymous'; // evita errores CORS
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });
}


const exportToPDF = async () => {
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  });
  // 1. Logo y título
  doc.setFont('helvetica'); // ← Cambia la fuente global
  doc.setFontSize(18);
  doc.setTextColor(40, 40, 40);
  doc.text('CARTERA POR COBRAR', 14, 20);

  try {
    // ✅ Espera a que la imagen cargue
    const img = await loadImagePDF(logo);
    doc.addImage(img, 'PNG', 165, 12, 30, 10);
  } catch (error) {
    console.warn('No se pudo cargar el logo:', error);
    // Continúa sin logo
  }

  // 2. Fecha
  function formatearFechaHora(fecha = new Date()) {
    const opciones = {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return fecha.toLocaleDateString('es-ES', opciones);
  }

// Uso
  const reporteFecha = formatearFechaHora();
  doc.setFontSize(10);
  doc.setTextColor(100, 100, 100);
  // doc.text(`Generado el: ${fecha}`, 14, 26);

  // 3. Preparar datos de la tabla
  const columns = [
    {header: 'Cliente', dataKey: 'clientes'},
    {header: 'Debe', dataKey: 'debe'},
    {header: 'Haber', dataKey: 'haber'},
    {header: 'Saldo', dataKey: 'saldo'}

  ];

  const formatCurrency = (value) => {
    const num = parseFloat(value);
    if (isNaN(num)) return '---';
    return `${num.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')}`;
  };

  // const rows = tableCuentaxcobrar.value.map(item => ({
  //   clientes: item.clientes,
  //   debe: parseFloat(item.debe).toFixed(2),
  //   haber: parseFloat(item.haber).toFixed(2),
  //   saldo: parseFloat(item.saldo).toFixed(2)
  // }));
  const rows = dataSaldos.map(row => [
    row.clientes || '—',
    formatCurrency(row.debe),
    formatCurrency(row.haber),
    formatCurrency(row.saldo)
  ]);
  const totalSaldo = dataSaldos.reduce((sum, row) => sum + parseFloat(row.saldo || 0), 0);

  rows.push([
    {content: 'TOTAL', styles: {fontStyle: 'bold'}},
    '---',
    '---',
    {content: formatCurrency(totalSaldo), styles: {fontStyle: 'bold'}}
  ]);
  // 4. Generar tabla con estilo
  autoTable(doc, {
    startY: 25,
    head: [columns.map(col => col.header)],
    body: rows,

    columnStyles: {
      0: {halign: 'left'},                  // Cliente a la izquierda
      1: {halign: 'right', cellWidth: 30},                 // Debe a la derecha
      2: {halign: 'right', cellWidth: 30},                 // Haber a la derecha
      3: {halign: 'right', cellWidth: 30}                  // Saldo a la derecha
    },

    theme: 'grid',
    styles: {
      fontSize: 9,
      cellPadding: 3,
      halign: 'center',
      valign: 'middle'
    },
    headStyles: {
      fillColor: [15, 59, 89], // Azul profesional
      textColor: 255,
      fontSize: 10,
      fontStyle: 'bold',
      halign: 'center' // Centra las cabeceras
    },
    alternateRowStyles: {
      fillColor: [245, 245, 245] // Gris suave
    },
    // didParseCell: function (data) {
    //   // Aplicar color según estado (saldo)
    //   if (data.section === 'body' && data.column.index === 3) { // columna "Saldo"
    //     const saldo = parseFloat(data.cell.raw.replace('$', ''));
    //     // if (saldo <= 0) {
    //     //   data.cell.styles.textColor = [40, 167, 69]; // Verde
    //     // } else {
    //     //   data.cell.styles.textColor = [220, 53, 69]; // Rojo
    //     // }
    //   }
    // }
  });

  // 5. Añadir pie de página
  const pageCount = doc.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFontSize(8);
    doc.setTextColor(150, 150, 150);
    doc.text(`Sistema de Gestión Financiera - elabarado por ${auth.user?.usuario_nombre} - día ${reporteFecha}`, 14, doc.internal.pageSize.height - 10);
    doc.text(
      `Página ${i} de ${pageCount}`,
      doc.internal.pageSize.width - 15,           // derecha horizontal
      doc.internal.pageSize.height - 10,         // 10mm desde abajo
      {align: 'right'}
    );
  }

  // 6. Descargar
  doc.save(`cartera_cobrar_${reporteFecha.replace(/\//g, '-')}.pdf`);

};


</script>

