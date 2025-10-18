<template>
  <div class="form-wrapper">
    <h2 class="form-title">CREACIÓN DE EGRESOS</h2>
    <InputText
      v-model="Idegreso"
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
      v-model="Idcuentadestino"
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
            <label for="concepto" class="form-label">CONCEPTO</label>
            <InputText
              v-model="concepto"
              id="concepto"
              type="text"
              placeholder="Concepto"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="valor" class="form-label">VALOR</label>
            <InputText
              v-model="valor"
              id="valor"
              type="text"
              placeholder="Valor"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label class="form-label">CUENTA PRINCIPAL</label>
            <AutoComplete
              v-model="selectedCuentadestino"
              :suggestions="filteredCuentadestino"
              field="cuenta_destino"
              dropdown
              optionValue="cuentadestino_id"
              optionLabel="cuenta_destino"
              forceSelection
              placeholder="Cuenta principal"
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
                editarEgresos()
              }"
            />
          </div>
        </div>
      </form>
    </section>
    <!-- DATATABLE -->
    <section class="form-section">
      <!--        <div class="datatable-card">-->
      <h2 class="form-title">LISTADO DE EGRESOS</h2>
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
        :value="egresos"
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
        <Column field="egreso_id" header="#" style="width: 60px"></Column>
        <Column field="concepto" header="Concepto" ></Column>
        <Column bodyClass="text-right" field="valor" header="Valor" ></Column>
        <Column field="usuario.usuario_nombre" header="Realizó" ></Column>
        <Column field="cuenta_destino.cuenta_destino" header="Cuenta" ></Column>
        <Column bodyClass="text-center" field="created_at" header="Fecha creado" sortable></Column>
        <Column bodyClass="text-center" field="updated_at" header="Fecha actualizado"></Column>
        <Column bodyClass="text-center" field="" header="Acciones" style="width: 150px">
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
                  text: `Sr. usuario, está seguro que desea editar el egreso: ${slotProps.data.concepto} con ID: ${slotProps.data.egreso_id}`,
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
                    concepto = slotProps.data.concepto
                    Idcuentadestino = slotProps.data.cuenta_destino.cuentadestino_id
                    selectedCuentadestino = slotProps.data.cuenta_destino.cuenta_destino
                    valor = slotProps.data.valor
                    Idegreso = slotProps.data.egreso_id

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
                  text: `Sr. usuario, va eliminar el egreso: ${slotProps.data.concepto} con el ID: ${slotProps.data.egreso_id}`,
                  icon: 'success',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'

                }).then(async (result) => {
                  if (result.isConfirmed) {
                    Idegreso = slotProps.data.egreso_id
                    deleteEgresos()
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
import {useAuthStore} from "@/stores/auth.js"
const auth = useAuthStore()
import Swal from "sweetalert2";                   // optional
const URI_ROOT = import.meta.env.VITE_API_URL;
const concepto = ref('')
const Idegreso = ref('')
const valor = ref('')
const loading = ref(false)
const mostrarInput = ref(false)
const mostrarBtnUpdate = ref(false)
const mostrarBtnCrear = ref(true)
const selectedCuentadestino = ref(null)
const filteredCuentadestino = ref([])
const cuentadestino = ref([])
const Idcuentadestino = ref('')

const egresos = ref([])

const filters = ref({
  global: {value: null, matchMode: FilterMatchMode.CONTAINS},
})

onMounted(async () => {
  await loadTableegresos();
  await loadCuentadestino()
})

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


async function loadTableegresos() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargartableegresos');
    egresos.value = await response.json()
  } catch (error) {
    // Swal.fire({
    //   title: 'Error',
    //   text: 'No se pudieron cargar los roles. Intente más tarde.',
    //   icon: 'error'
    // });
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

async function editarEgresos() {
  try {
    const valores = valor.value;
    const idcuenta = Idcuentadestino.value
    if (!concepto.value || concepto.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usaurio por favor ingrese el concepto',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }else if (!valores || isNaN(Number(valores)) || Number(valores) < 0) {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor verificar valor del egreso a realizar',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }else if (!idcuenta || isNaN(Number(idcuenta)) || Number(idcuenta) < 0) {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor verificar la cuenta para desembolso',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }

    const response = await fetch(`${URI_ROOT}/api/updateegresos`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        concepto: concepto.value,
        cuentadestino_id: Idcuentadestino.value,
        egreso_id: Idegreso.value,
        valor: valor.value,
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
      title: '¡Egreso actualizado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTableegresos();


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
  concepto.value = ""
  Idegreso.value=""
  Idcuentadestino.value=""
  valor.value=""
  selectedCuentadestino.value=""
}

async function deleteEgresos() {
  try {
    const response = await fetch(`${URI_ROOT}/api/deleteegresos/`+Idegreso.value, {
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
      title: '¡Egreso eliminado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTableegresos();


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
  const valores = valor.value;
  const idcuenta = Idcuentadestino.value
  if (!concepto.value || concepto.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usaurio por favor ingrese el concepto',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }else if (!valores || isNaN(Number(valores)) || Number(valores) < 0) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor verificar valor del egreso a realizar',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }else if (!idcuenta || isNaN(Number(idcuenta)) || Number(idcuenta) < 0) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor verificar la cuenta para desembolso',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }

  loading.value = true
  try {
    const response = await fetch(`${URI_ROOT}/api/creaegresos`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        concepto: concepto.value,
        valor: valor.value,
        cuentadestino_id: Idcuentadestino.value,
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
      title: '¡Egreso creado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTableegresos();


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
