<template>
  <div class="form-wrapper">
    <h2 class="form-title">REGISTRO DE MOTOR</h2>
    <form @submit.prevent="handleSubmit" class="form-grid">
      <div class="form-field half">
        <FloatLabel variant="in">
          <Dropdown id="clientes" v-model="form.rol" :options="pais"
                    option-value="value" placeholder="Seleccione el cliente" />
          <label for="clientes">CLIENTES</label>
        </FloatLabel>
      </div>
      <div class="form-field half">
        <FloatLabel variant="in">
          <InputText id="serial" type="text"/>
          <label for="serial">SERIAL</label>
        </FloatLabel>
      </div>
      <div class="form-field half">
        <FloatLabel variant="in">
          <InputText id="vin" type="text"/>
          <label for="vin">VIN</label>
        </FloatLabel>
      </div>
      <div class="form-field half">
        <FloatLabel variant="in">
          <InputText id="ncontacto" type="text"/>
          <label for="ncontacto">NÚMERO DE CONTACTO</label>
        </FloatLabel>
      </div>
      <div class="form-field small">
        <FloatLabel variant="in">
          <!--          <InputText id="ttrabajo"/>-->
          <Dropdown id="pais" v-model="form.rol" :options="pais"
                    option-value="value" placeholder="Seleccione el país" />
          <label for="pais">PAÍS</label>
        </FloatLabel>
      </div>
      <div class="form-field half">
        <FloatLabel variant="in">
          <!--          <InputText id="ttrabajo"/>-->
          <Dropdown id="ciudad" v-model="form.rol" :options="ciudad"
                    option-value="value" placeholder="Seleccione el ciudad" />
          <label for="ciudad">CIUDAD</label>
        </FloatLabel>
      </div>
      <div class="form-field half">
        <FloatLabel variant="in">
          <!--          <InputText id="ttrabajo"/>-->
          <Dropdown id="dpto" v-model="form.rol" :options="trabajo"
                    option-value="value" placeholder="Seleccione el departamento" />
          <label for="dpto">DEPARTAMENTO</label>
        </FloatLabel>
      </div>
    </form>
    <div>
      <!-- DATATABLE -->
      <div class="form-field full">
<!--        <div class="datatable-card">-->
          <div class="datatable-header">
            <h2 class="form-title">LISTADO DE CLIENTES</h2>
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
            <Column field="nombre" header="NOMBRE"></Column>
            <Column field="email" header="NIT-CÉDULA"></Column>
            <Column field="telefono" header="Teléfono"></Column>
            <Column field="telefono" header="PAÍS"></Column>
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
import Textarea from 'primevue/textarea'
import InputNumber from 'primevue/inputnumber'
import Checkbox from 'primevue/checkbox'
import Button from 'primevue/button'
import FloatLabel from 'primevue/floatlabel'
import { FilterMatchMode } from 'primevue/api'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';
import Swal from "sweetalert2";                   // optional

const form = ref({
  price: '',
  code: '',
  sku: '',
  description: '',
  quantity: 0,
  category: '',
  active: false
})


const clientes = ref([
  { id: 1, nombre: 'Juan Pérez', email: 'juan@mail.com', telefono: '3001234567' },
  { id: 2, nombre: 'Ana Gómez', email: 'ana@mail.com', telefono: '3109876543' },
  { id: 3, nombre: 'Carlos Ruiz', email: 'carlos@mail.com', telefono: '3124567890' },
  { id: 1, nombre: 'Juan Pérez', email: 'juan@mail.com', telefono: '3001234567' },
  { id: 2, nombre: 'Ana Gómez', email: 'ana@mail.com', telefono: '3109876543' },
  { id: 3, nombre: 'Carlos Ruiz', email: 'carlos@mail.com', telefono: '3124567890' },
  { id: 1, nombre: 'Juan Pérez', email: 'juan@mail.com', telefono: '3001234567' },
  { id: 2, nombre: 'Ana Gómez', email: 'ana@mail.com', telefono: '3109876543' },
  { id: 3, nombre: 'Carlos Ruiz', email: 'carlos@mail.com', telefono: '3124567890' },
  { id: 1, nombre: 'Juan Pérez', email: 'juan@mail.com', telefono: '3001234567' },
  { id: 2, nombre: 'Ana Gómez', email: 'ana@mail.com', telefono: '3109876543' },
  { id: 3, nombre: 'Carlos Ruiz', email: 'carlos@mail.com', telefono: '3124567890' },
  { id: 1, nombre: 'Juan Pérez', email: 'juan@mail.com', telefono: '3001234567' },
  { id: 2, nombre: 'Ana Gómez', email: 'ana@mail.com', telefono: '3109876543' },
  { id: 3, nombre: 'Carlos Ruiz', email: 'carlos@mail.com', telefono: '3124567890' },
  { id: 1, nombre: 'Juan Pérez', email: 'juan@mail.com', telefono: '3001234567' },
  { id: 2, nombre: 'Ana Gómez', email: 'ana@mail.com', telefono: '3109876543' },
  { id: 3, nombre: 'Carlos Ruiz', email: 'carlos@mail.com', telefono: '3124567890' },
  { id: 1, nombre: 'Juan Pérez', email: 'juan@mail.com', telefono: '3001234567' },
  { id: 2, nombre: 'Ana Gómez', email: 'ana@mail.com', telefono: '3109876543' },
  { id: 3, nombre: 'Carlos Ruiz', email: 'carlos@mail.com', telefono: '3124567890' },
  { id: 1, nombre: 'Juan Pérez', email: 'juan@mail.com', telefono: '3001234567' },
  { id: 2, nombre: 'Ana Gómez', email: 'ana@mail.com', telefono: '3109876543' },
  { id: 3, nombre: 'Carlos Ruiz', email: 'carlos@mail.com', telefono: '3124567890' },
])

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
})

const agregarCliente = () => alert('Abrir modal para agregar cliente')
const editarCliente = (cliente) => {
  Swal.fire({
    title: 'Confirmación',
    text: `Sr. usuario, está seguro que desea edidtar a: ${cliente.nombre}`,
    icon: 'info',
    confirmButtonText: 'Aceptar',
    confirmButtonColor: '#ef4444'
  })
}
const eliminarCliente = (id) => alert(`Eliminar cliente con id ${id}`)

const skuOptions = ['SKU1', 'SKU2', 'SKU3']
const categories = ['Electrónica', 'Ropa', 'Hogar']
const selectedDate = ref(null)
const saveProduct = () => {
  console.log('Guardando...', form.value)
  alert('Producto guardado!')
}
</script>

<style scoped>
.datatable-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.datatable-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.datatable-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1f2937;
}

:deep(.p-datatable) {
  border-radius: 12px;
  overflow: hidden;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
  background-color: #f9fafb;
  font-weight: 600;
  color: #374151;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
  background-color: #f3f4f6;
  transition: 0.2s;
}
:deep(.p-datatable-scrollable-header) {
  position: sticky;
  top: 0;
  z-index: 2;
  background: #f3f4f6;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

:deep(.p-datatable-scrollable-body) {
  scrollbar-width: thin;
  scrollbar-color: #9ca3af #f3f4f6;
}

.form-wrapper {
  max-width: 1700px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.25);
}

.form-wrapper:hover {
  transform: translateY(-4px) !important;
  box-shadow: 0 12px 30px rgba(255, 255, 255, 0.25) !important;
}

.form-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #1f2937;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4 columnas iguales */
  gap: 1.5rem;
}

.form-field label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #374151;
}

.form-field.full {
  grid-column: span 2;
}

.form-field input {
  width: 100%;
}


.form-actions {
  grid-column: span 2;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

/* RESPONSIVE: en pantallas pequeñas cambia a 2x2 */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* RESPONSIVE: en móvil, 1 por fila */
@media (max-width: 480px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

</style>
