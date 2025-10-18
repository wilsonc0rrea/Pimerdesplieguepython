<template>
  <div class="form-wrapper">
    <h2 class="form-title">Perfil</h2>
    <InputText
      v-model="Idperfil"
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
            <label for="telefonos" class="form-label">TELÉFONOS</label>
            <InputText
              v-model="telefonos"
              id="telefonos"
              type="text"
              placeholder="Telefonos"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="email" class="form-label">EMAIL</label>
            <InputText
              v-model="email"
              id="email"
              type="text"
              readonly
              placeholder="Email"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="newpass" class="form-label">CONTRASEÑA NUEVA</label>
            <Password
              v-model="newpass"
              toggleMask
              id="newpass"
              type="password"
              placeholder="Contraseña nueva"
              class="form-input"
            />
          </div>
          <div class="form-field action-field">
            <label class="form-label invisible">ACCIONES</label> <!-- Label invisible para mantener alineación -->
            <Button
              type="button"
              label="Actualizar..."
              v-show="mostrarBtnUpdate"
              icon="pi pi-user-plus"
              :loading="loading"
              class="form-button hidden"
              @click="() => {
                editarPerfil()
              }"
            />
          </div>
        </div>
      </form>
    </section>
    <!-- DATATABLE -->
    <section class="form-section">
      <!--        <div class="datatable-card">-->
      <h2 class="form-title">LISTADO DE ROLES</h2>
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
        :value="perfiles"
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
        <Column field="usuario_nombre" header="Nombre" ></Column>
        <Column field="usuario_telefono" header="Teléfonos"></Column>
        <Column field="usuario_email" header="Email"></Column>
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
                  text: `Sr. usuario, está seguro que desea editar el perfil: ${slotProps.data.usuario_nombre}`,
                  icon: 'info',
                  showCancelButton: true,
                  confirmButtonColor: '#374151',
                  cancelButtonColor: '#ef4444',
                  confirmButtonText: 'Sí',
                  cancelButtonText: 'Cancelar'
                }).then(async (result) => {
                  if (result.isConfirmed) {
                    mostrarBtnUpdate = true
                    nombre = slotProps.data.usuario_nombre
                    telefonos = slotProps.data.usuario_telefono
                    email = slotProps.data.usuario_email
                    Idperfil = slotProps.data.usuario_id
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
import Swal from "sweetalert2";
const URI_ROOT = import.meta.env.VITE_API_URL;
const auth = useAuthStore()
const rol = ref('')
const Idperfil = ref('')
const nombre = ref('')
const telefonos = ref('')
const email = ref('')
const newpass = ref('')
const usuario_id = ref('')
const Idstate = ref('')
const fecha = ref('')
const loading = ref(false)
const mostrarInput = ref(false)
const mostrarBtnUpdate = ref(true)
const perfiles = ref([])

const filters = ref({
  global: {value: null, matchMode: FilterMatchMode.CONTAINS},
})
usuario_id.value = auth.user?.usuario_id


onMounted(async () => {
  await loadPerfil();
})

async function loadPerfil() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargartableperfil/' + usuario_id.value);
    if (!response.ok) throw new Error('Error')
    perfiles.value = await response.json()
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: 'No se pudieron cargar los perfiles. Intente más tarde.',
      icon: 'error'
    });
  }
}

function limpiarForm(){
  nombre.value = ""
  telefonos.value=""
  email.value=""
  newpass.value=""
  Idperfil.value=""
}
const validateEmailFormat = (email: string) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/ // patrón básico
  return emailRegex.test(email)
}
async function editarPerfil() {
  try {
    const userEmail = email.value.trim()

    if (!Idperfil.value || Idperfil.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor verifique los datos a editar',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }else if (!nombre.value || nombre.value.trim() === '') {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario por favor verifique el nombre',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    } else if (!validateEmailFormat(userEmail)) {
      return Swal.fire({
        title: 'Error',
        text: 'Sr. usuario. por favor verificar correo registrado',
        icon: 'error',
        confirmButtonText: 'Aceptar',
        confirmButtonColor: '#ef4444'
      })
    }
    const response = await fetch(`${URI_ROOT}/api/updateperfil`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        usuario_id: Idperfil.value,
        usuario_nombre: nombre.value,
        usuario_telefono: telefonos.value,
        usuario_email: email.value,
        usuario_password: newpass.value
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
      title: '¡Perfil actualizado!',
      text: `${data.user.usuario_nombre}`, // ✅ usamos lo que devuelve el backend
      icon: 'success',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#374151',

    })

    limpiarForm()
    // ✅ ¡Recarga la tabla!
    await loadPerfil();
    auth.logoutAndRedirect()

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
