<template>
  <div class="form-wrapper">
    <h2 class="form-title">CREACIÓN DE SALDOS</h2>
    <InputText
      v-model="Idcuentadestino"
      type="number"
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
      v-model="Idsaldo"
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
            <label for="observacion" class="form-label">Observación</label>
            <InputText
              v-model="observacion"
              id="observacion"
              type="text"
              placeholder="observacion"
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
                editarSaldosiniciales()
              }"
            />
          </div>
        </div>
      </form>
    </section>
    <!-- DATATABLE -->
    <section class="form-section">
      <!--        <div class="datatable-card">-->
      <h2 class="form-title">LISTADO DE SALDOS</h2>
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
        :value="tableSaldos"
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
<!--        <Column field="saldo_id" header="#" style="width: 60px"></Column>-->
        <Column field="cuenta_destino.cuenta_destino" header="Cta. principal"></Column>
        <Column bodyClass="text-right" field="saldo" header="Saldo"></Column>
        <Column bodyClass="text-right" field="debe" header="Debe"></Column>
        <Column bodyClass="text-right" field="haber" header="Haber"></Column>
        <Column field="observacion" header="Observacion"></Column>
        <Column bodyClass="text-center" field="created_at" header="Fecha creado" sortable></Column>
        <Column bodyClass="text-center" field="usuario.usuario_nombre" header="Realizó" sortable></Column>
        <Column bodyClass="text-center" field="" header="Movimiento">
          <template #body="slotProps">
            <div>
              <span v-if="slotProps.data.debe > 0" class="badge bg-danger">
                Salida
              </span>
              <span v-else-if="slotProps.data.haber > 0" class="badge bg-success">
              Entrada
              </span>
              <span v-else class="badge bg-success">
              Entrada
              </span>
            </div>
          </template>
        </Column>
        <Column bodyClass="text-center" field="flag" header="Acciones" style="width: 150px">
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
                  text: `Sr. usuario, está seguro que desea editar saldo inicial de: ${slotProps.data.cuenta_destino.cuenta_destino}, con siguiente ID: ${slotProps.data.saldo_id}`,
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
                    let SaldoInicial= slotProps.data.saldo
                    if(SaldoInicial > 0){
                      Idcuentadestino = slotProps.data.cuenta_destino.cuentadestino_id
                      selectedCuentadestino = slotProps.data.cuenta_destino.cuenta_destino
                      Idsaldo= slotProps.data.saldo_id
                      valor=slotProps.data.saldo
                      observacion=slotProps.data.observacion
                    }else{
                       Swal.fire({
                          title: 'Error',
                          text: `No se puede editar el siguiente movimiento ${slotProps.data.cuenta_destino.cuenta_destino}, no es un saldo inicial.`,
                          confirmButtonText: 'Aceptar',
                          confirmButtonColor: '#374151',
                          icon: 'error'
                       });
                    }

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
import {useAuthStore} from "@/stores/auth.js"

const auth = useAuthStore()

import Swal from "sweetalert2";                   // optional
const URI_ROOT = import.meta.env.VITE_API_URL;

const valor = ref('')
const Idstate = ref('')
const Idsaldo = ref('')
const observacion = ref('')

const loading = ref(false)
const mostrarInput = ref(false)
const mostrarBtnUpdate = ref(false)
const mostrarBtnCrear = ref(true)
const selectedCuentadestino = ref(null)
const filteredCuentadestino = ref([])
const cuentadestino = ref([])
const tableSaldos = ref([])
const Idcuentadestino = ref('')


const filters = ref({
  global: {value: null, matchMode: FilterMatchMode.CONTAINS},
})

function getFlagLabel(flag) {
  return flag === 1 || flag === true ? 'Activo' : 'Inactivo';
}


onMounted(async () => {
  await loadCuentadestino();
  await loadTableSaldos();
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

async function editarSaldosiniciales() {
  const valores = valor.value;
  const idcuenta = Idcuentadestino.value
  try {
    if (!idcuenta || Number(idcuenta) < 0) {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor verificar cuenta principal',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    } else if (!valores || isNaN(Number(valores)) || Number(valores) < 0) {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor verificar valor del movimiento a realizar',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    } else if (!observacion.value || observacion.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor debe realizar una observación del movimiento',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }

    const response = await fetch(`${URI_ROOT}/api/updatesaldoinicial`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        saldo_id: Idsaldo.value,
        saldo: valor.value,
        observacion: observacion.value,
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
      title: '¡Saldo actualizado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTableSaldos();


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

async function loadTableSaldos() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargartablesaldos');
    tableSaldos.value = await response.json()
  } catch (error) {
    // Swal.fire({
    //   title: 'Error',
    //   text: 'No se pudieron cargar los clientes. Intente más tarde.',
    //   icon: 'error'
    // });
  }


}

function limpiarForm() {
  Idcuentadestino.value = ""
  observacion.value = ""
  Idstate.value = ""
  observacion.value = ""
  Idsaldo.value = ""
  valor.value = ""
  selectedCuentadestino.value = ""
  valor.value = ""

}

const handleSubmit = async () => {
  const valores = valor.value;
  const idcuenta = Idcuentadestino.value
  if (!idcuenta || Number(idcuenta) < 0) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor verificar cuenta principal',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (!valores || isNaN(Number(valores)) || Number(valores) < 0) {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor verificar valor del movimiento a realizar',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  } else if (!observacion.value || observacion.value.trim() === '') {
    return Swal.fire({
      title: 'Error',
      text: 'Sr. usuario por favor debe realizar una observación del movimiento',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ef4444'
    })
  }

  loading.value = true
  try {
    console.log(valor.value, Idcuentadestino.value, observacion.value, auth.user?.usuario_id)
    const response = await fetch(`${URI_ROOT}/api/crearsaldos`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        saldo: valores,
        cuentadestino_id: Idcuentadestino.value,
        observacion: observacion.value,
        usuario_id: auth.user?.usuario_id
      }),

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
      title: '¡Saldo creado!',
      text: `"${data.message}"`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',
      timer: 2000,
      timerProgressBar: true
    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadTableSaldos();


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
