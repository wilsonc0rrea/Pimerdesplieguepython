// 1️⃣ Importa la función para crear una instancia de Vue
import { createApp } from 'vue'
import { createPinia } from 'pinia'
// 2️⃣ Importa el componente raíz de tu app (App.vue)
import App from './App.vue'
// 3️⃣ Importa el router (Vue Router) para navegación entre vistas
import router from './router'

// 4️⃣ Importa el componente Menubar de PrimeVue (barra de menú horizontal)
import Menubar from 'primevue/menubar'
// 5️⃣ Importa el tema visual de PrimeVue (Lara Light Blue) → Define colores, bordes, sombras, tipografía
import 'primevue/resources/themes/lara-light-blue/theme.css'
// 6️⃣ Importa los iconos de PrimeIcons (usados en botones, menús, etc.)
import 'primeicons/primeicons.css'
// 7️⃣ Importa el plugin principal de PrimeVue (configuración global)
import PrimeVue from 'primevue/config'
// 8️⃣ Importa los estilos base de PrimeVue (estructura de componentes, sin tema)
import 'primevue/resources/primevue.min.css'
// 9️⃣ Importa otros componentes que usarás
import TieredMenu from 'primevue/tieredmenu'  // Menú desplegable multinivel
import Checkbox from 'primevue/checkbox'      // Checkbox con estilo PrimeVue
import InputNumber from 'primevue/inputnumber';

import Password from 'primevue/password'

import Card from 'primevue/card'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import AutoComplete from 'primevue/autocomplete'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';
import Dialog from 'primevue/dialog';
import Chart from "primevue/chart";
import Calendar from "primevue/calendar";
// 🔟 Crea la instancia de la app Vue
const app = createApp(App)
const pinia = createPinia()
// 11️⃣ Instala PrimeVue como plugin global (con efecto "ripple" al hacer click)
app.use(PrimeVue, { ripple: true })
// 12️⃣ Instala Vue Router para manejar navegación
app.use(pinia)
app.use(router)
// 13️⃣ Registra componentes de PrimeVue globalmente (para usarlos sin importarlos en cada componente)
app.component('InputText', InputText)
app.component('Checkbox', Checkbox)
app.component('Menubar', Menubar)
app.component('TieredMenu', TieredMenu)
app.component('Button', Button)
app.component('Password', Password)
app.component('Card', Card)
app.component('Row', Row)
app.component('ColumnGroup', ColumnGroup)
app.component('Column', Column)
app.component('DataTable', DataTable)
app.component('AutoComplete', AutoComplete)
app.component('Dropdown', Dropdown)
app.component('InputNumber', InputNumber)
app.component('Dialog', Dialog);
app.component('Chart', Chart);
app.component('Calendar', Calendar);
// 14️⃣ Monta la app en el elemento con id="app" del index.html
app.mount('#app')

// ✅ Añadir clase cuando la app se monte → activa el fade-in
document.getElementById('app')?.classList.add('mounted')
