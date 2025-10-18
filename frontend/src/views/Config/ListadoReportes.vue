<template>
  <div class="form-wrapper ">
    <!-- Formulario de Creación -->
    <section class="form-section">
      <h2 class="form-title">LISTADO REPORTES DIARIOS</h2>
      <form @submit.prevent="handleSubmit" class="form-inline">
        <!-- Contenedor flex -->
        <div class="form-row">

          <div class="form-field">
            <label for="fechaini" class="form-label">FECHA INICIAL</label>
            <InputText
              v-model="fechainicial"
              id="fechaini"
              type="date"
              placeholder="Fecha"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label for="fechafin" class="form-label">FECHA FINAL</label>
            <InputText
              v-model="fechafinal"
              id="fechafin"
              type="date"
              placeholder="Fecha"
              class="form-input"
            />
          </div>
          <div class="form-field">
            <label class="form-label invisible">ACCIONES</label> <!-- Label invisible para mantener alineación -->
            <Button
              type="button"
              label="Buscar..."
              icon="pi pi-user-plus"
              :loading="loading"
              class="form-button hidden"
              @click="() => {
                buscarPorFechas()
              }"
            />
          </div>
        </div>
      </form>
    </section>
    <!-- DATATABLE -->
    <section class="form-section">
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
        :value="reportesTable"
        :filters="filters"
        :paginator="true"
        :rows="100"
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
          </template>
        </Column>
      </DataTable>
    </section>
  </div>
</template>

<script setup lang="ts">
// @ts-nocheck

import {onMounted, ref, watch} from 'vue'
import {FilterMatchMode} from 'primevue/api'
import {useAuthStore} from "@/stores/auth.js"
import Swal from "sweetalert2";
import jsPDF from "jspdf";
import logo from "@/assets/image/logo/mLogo.png"
import autoTable from "jspdf-autotable";

const auth = useAuthStore()
const URI_ROOT = import.meta.env.VITE_API_URL;

const fechainicial = ref('')
const fechafinal = ref('')
const reportesTable = ref([])
const loading = ref(false)
let dataSaldos

const filters = ref({
  global: {value: null, matchMode: FilterMatchMode.CONTAINS},
})

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

function AsignarFechas() {
  fechainicial.value = fechaFormateada.toString()
  fechafinal.value = fechaFormateada.toString()

}

// Validar fecha inicial cuando cambie
// watch(fechainicial, (newDate) => {
//   if (newDate && !isValidDate(newDate)) {
//     Swal.fire({
//       icon: 'error',
//       title: 'Fecha inválida',
//       text: 'La fecha inicial no es válida. Por favor seleccione una fecha correcta.',
//       confirmButtonColor: '#374151'
//     });
//     fechainicial.value = null; // limpiar si es inválida
//   }
// });
//
// // Validar fecha final
// watch(fechafinal, (newDate) => {
//   if (newDate && !isValidDate(newDate)) {
//     Swal.fire({
//       icon: 'error',
//       title: 'Fecha inválida',
//       text: 'La fecha final no es válida.',
//       confirmButtonColor: '#374151'
//     });
//     fechafinal.value = null;
//   }
// });
//
// function isValidDate(date) {
//   return date instanceof Date && !isNaN(date.getTime());
// }

function buscarPorFechas() {
  // if (!fechainicial.value || !fechafinal.value) {
  //   Swal.fire('Advertencia', 'Seleccione ambas fechas', 'warning');
  //   return;
  // }

  if (fechainicial.value > fechafinal.value) {
    Swal.fire('Advertencia', 'La fecha inicial no puede ser mayor que la final', 'warning');
    return;
  }

  // ✅ Aquí llamas a tu API
  loadTableReportesFechas();
};

async function loadTableReportes() {
  try {
    const response = await fetch(URI_ROOT + '/api/cargartablereportes/' + auth.user?.usuario_id);
    reportesTable.value = await response.json()
    dataSaldos = Array.isArray(reportesTable.value) ? reportesTable.value : [];

  } catch (error) {
    // Swal.fire({
    //   title: 'Error',
    //   text: 'No se pudieron cargar los clientes. Intente más tarde.',
    //   icon: 'error'
    // });
  }
}

async function loadTableReportesFechas() {
  try {
    // const response = await fetch(URI_ROOT + '/api/cargartablereportesfechas');
    // reportesTable.value = await response.json()
    const response = await fetch(`${URI_ROOT}/api/cargartablereportesfechas/` + fechainicial.value + "/" + fechafinal.value)
    if (!response.ok) throw new Error('Error en la petición');

    //reportesTable.value = await response.json();
    const data = await response.json();
    reportesTable.value = Array.isArray(data) && data.length > 0 ? data : [];
    // ✅ Si hay datos, los asignas. Si no, asignas array vacío.
    dataSaldos = Array.isArray(reportesTable.value) ? reportesTable.value : [];

  } catch (error) {
    // ✅ En caso de error, también limpia la tabla
    reportesTable.value = [];
    Swal.fire({
      title: 'Error',
      text: 'No se pudieron cargar los datos. Intente más tarde.',
      icon: 'error'
    });
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
    orientation: 'landscape',
    unit: 'mm',
    //format: 'a4' // ✅ Tamaño carta
    format: [216, 330] // ✅ Tamaño oficio
  });
  // 1. Logo y título
  doc.setFont('helvetica'); // ← Cambia la fuente global
  doc.setFontSize(18);
  doc.setTextColor(40, 40, 40);
  doc.text('LISTADO REPORTES DIARIOS', 14, 20);

  try {
    // ✅ Espera a que la imagen cargue
    const img = await loadImagePDF(logo);
    doc.addImage(img, 'PNG', 280, 12, 30, 10);
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
    {header: 'Fecha', dataKey: 'created_at'},
    {header: 'F. Final', dataKey: 'updated_at'},
    {header: 'Empresa', dataKey: 'clientes'},
    {header: 'Serial', dataKey: 'seriales'},
    {header: 'Vin', dataKey: 'vin'},
    {header: 'Motor', dataKey: 'motor'},
    {header: 'Trabajo', dataKey: 'trabajo'},
    {header: 'Realizó', dataKey: 'usuario_nombre'},
    {header: 'Precio', dataKey: 'precio'},
    {header: 'Estado', dataKey: ''},
    {header: 'Cuenta', dataKey: 'estado'}

  ];

  const formatCurrency = (value) => {
    const num = parseFloat(value);
    if (isNaN(num)) return '---';
    return `${num.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')}`;
  };

  const rows = dataSaldos.map(row => [
    row.created_at || '—',
    row.updated_at || '—',
    row.clientes.clientes || '—',
    row.seriales || '—',
    row.vin || '—',
    row.motor || '—',
    row.trabajo.trabajo || '—',
    row.usuario.usuario_nombre || '—',
    formatCurrency(row.precio),
    row.usuario_nombre || '—',
    row.estado.estado || '—',
  ]);
  const totalSaldo = dataSaldos.reduce((sum, row) => sum + parseFloat(row.precio || 0), 0);

  rows.push([
    {content: 'TOTAL', styles: {fontStyle: 'bold'}},
    '---',
    '---',
    '---',
    '---',
    '---',
    '---',
    '---',
    '---',
    {content: formatCurrency(totalSaldo), styles: {fontStyle: 'bold'}},
    '---',
  ]);
  // 4. Generar tabla con estilo
  autoTable(doc, {
    startY: 25,
    head: [columns.map(col => col.header)],
    body: rows,

    columnStyles: {
      0: {halign: 'center', cellWidth: 30},
      1: {halign: 'center', cellWidth: 30},
      2: {halign: 'left', cellWidth: 30},
      3: {halign: 'right', cellWidth: 30},
      4: {halign: 'right', cellWidth: 30},
      5: {halign: 'right', cellWidth: 30},
      6: {halign: 'left', cellWidth: 30},
      7: {halign: 'left', cellWidth: 30},
      8: {halign: 'right', cellWidth: 30}
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
    doc.text(`Listado de reportes diarios - elabarado por ${auth.user?.usuario_nombre} - día ${reporteFecha}`, 14, doc.internal.pageSize.height - 10);
    doc.text(
      `Página ${i} de ${pageCount}`,
      doc.internal.pageSize.width - 15,           // centro horizontal
      doc.internal.pageSize.height - 10,         // 10mm desde abajo
      {align: 'right'}
    );
  }

  // 6. Descargar
  doc.save(`cartera_cobrar_${reporteFecha.replace(/\//g, '-')}.pdf`);

};

</script>
