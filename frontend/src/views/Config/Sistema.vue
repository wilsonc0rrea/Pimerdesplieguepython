<template>
  <div class="form-wrapper">
    <h2 class="form-title">REPORTES DIARIOS DE PROGRAMACIÓN</h2>
    <form @submit.prevent="handleSubmit" class="form-grid">
      <div class="form-field half">
        <FloatLabel variant="in">
          <InputText id="fecha" type="date"/>
          <label for="fecha">FECHA</label>
        </FloatLabel>
      </div>
      <div class="form-field half">
        <FloatLabel variant="in">
          <InputText id="cliente"/>
          <label for="cliente">CLIENTE</label>
        </FloatLabel>
      </div>
      <div class="form-field small">
        <FloatLabel variant="in">
          <InputText id="serial"/>
          <label for="serial">SERIAL</label>
        </FloatLabel>
      </div>
      <div class="form-field half">
        <FloatLabel variant="in">
          <InputText id="vin"/>
          <label for="vin">VIN</label>
        </FloatLabel>
      </div>
      <div class="form-field half">
        <FloatLabel variant="in">
          <InputText id="motor"/>
          <label for="motor">MOTOR</label>
        </FloatLabel>
      </div>
      <div class="form-field half">
        <FloatLabel variant="in">
          <!--          <InputText id="ttrabajo"/>-->
          <Dropdown id="ttrabajo" v-model="form.rol" :options="trabajo"
                    option-value="value" placeholder="Seleccione el tipo de trabajo" />
          <label for="ttrabajo">TIPO DE TRABAJO</label>
        </FloatLabel>
      </div>
      <div class="form-field half">
        <FloatLabel variant="in">
          <InputText id="precio"/>
          <label for="precio">PRECIO</label>
        </FloatLabel>
      </div>
      <div class="form-field half">
        <FloatLabel variant="in">
          <Dropdown id="tecnico" placeholder="Seleccione el técnico" />
          <label for="tecnico">TÉCNICO</label>
        </FloatLabel>
      </div>
    </form>
  </div>

</template>

<script setup lang="ts">
// @ts-nocheck

import {ref} from 'vue'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Textarea from 'primevue/textarea'
import InputNumber from 'primevue/inputnumber'
import Checkbox from 'primevue/checkbox'
import Button from 'primevue/button'
import FloatLabel from 'primevue/floatlabel'

const form = ref({
  price: '',
  code: '',
  sku: '',
  description: '',
  quantity: 0,
  category: '',
  active: false
})

const skuOptions = ['SKU1', 'SKU2', 'SKU3']
const categories = ['Electrónica', 'Ropa', 'Hogar']
const selectedDate = ref(null)
const saveProduct = () => {
  console.log('Guardando...', form.value)
  alert('Producto guardado!')
}
</script>

<style scoped>

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
