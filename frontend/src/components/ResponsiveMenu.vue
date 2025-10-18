<template>
  <div class="layout-wrapper">
    <Menubar :model="processedMenu" class="custom-menubar" appendTo="body">
      <!-- Logo -->
      <template #start>
        <RouterLink to="/" class="logo-section">
          <!--          <img :src="logo" alt="Logo" class="logo-img" />-->
          <span class="app-name"></span>
        </RouterLink>
      </template>

      <!-- Usuario -->
      <template #end>
        <div class="user-profile">
          <img :src="user.avatar" alt="avatar" class="user-avatar"/>
          <div class="user-info">
            <span class="user-name">{{ user.name }}</span>
            <span class="user-role">{{ user.role }}</span>
          </div>
        </div>
      </template>
    </Menubar>
  </div>
</template>

<script setup lang="ts">
// @ts-nocheck

import {ref, onMounted, computed, watch, watchEffect} from "vue"
import {useMenu} from '@/composables/useMenu';
import {useRouter} from "vue-router"
import logo from "@/assets/image/logo/mLogo.png"
import Swal from "sweetalert2"
import {useAuthStore} from "../stores/auth.js"

const auth = useAuthStore()
const router = useRouter()
const menuItems = ref([])
const URI_ROOT = import.meta.env.VITE_API_URL
console.log("ProbandoURI " + URI_ROOT)
// const {filtrarMenu} = useMenu();
const menuLoaded = ref(false) // 👈 Bandera: ¿menú listo?
const processedMenu = ref([])
const user = computed(() => ({
  name: auth.user?.usuario_nombre || "Invitado",
  role: auth.user?.rol.rol || "Sin rol",
  avatar: auth.user?.avatar || logo
}))

onMounted(async () => {
  try {
    await Promise.all([
      loadDatamenu()
    ])
  } catch (error) {
    Swal.fire({
      title: 'Error',
      text: {error},
      icon: 'error'
    });
  }
})

async function loadDatamenu() {
  try {
    const res = await fetch(URI_ROOT + "/api/menu")
    if (!res.ok) throw new Error('Error')
    const data = await res.json()
    // console.log("Itemns",auth.permisos)
    // console.log("Permisos",auth.permisos)
    menuItems.value = data
  } catch (error) {
    // Swal.fire({
    //   title: 'Error',
    //   text: {error},
    //   icon: 'error'
    // });
  }
}

watch(
  [menuItems, () => auth.permisos],
  async ([menu, permisos]) => {
    if (menu.length && Object.keys(permisos || {}).length) {
      //await new Promise(resolve => setTimeout(resolve, 5000))

      const menuFiltrado = filtrarMenu(menu, auth.permisos)
      processedMenu.value = procesarComandos(menuFiltrado)
    } else {
      // processedMenu.value = []
    }
  },
  {deep: true, immediate: true}
)


function tienePermiso(modulo, permisos) {
  if (!modulo) return true // los ítems sin módulo (como Inicio o Salir) se muestran siempre

  // Normalizamos el nombre del módulo (sin tildes, espacios o mayúsculas)
  const normalizar = s =>
    s.toString()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-zA-Z0-9]/g, "")
      .toLowerCase()

  const moduloNorm = normalizar(modulo)
  for (const key in permisos) {
    if (normalizar(key) === moduloNorm) {
      return permisos[key].ver === true
    }
  }

  return true
}


function filtrarMenu(menu, permisos) {
  return menu
    .map(item => {
      const modulo = item.modulo
      // 🔒 Si el módulo principal tiene "ver: false", se oculta todo
      if (!tienePermiso(modulo, permisos)) {
        return null
      }
      // const puedeVer = tienePermiso(item.modulo, permisos)
      // // console.log(`🔑 ${item.modulo} → ${puedeVer}`)
      // return puedeVer ? item : null
      if (item.items && item.items.length > 0) {
        const subItems = filtrarMenu(item.items, permisos)
        return {...item, items: subItems}
      }
      return item
    })
    .filter(Boolean)
}


function procesarComandos(items) {
  return items.map(item => {
    // Si es un ítem de cierre de sesión
    if (item.command === 'logout') {
      return {...item, command: () => handleLogout()};
    }
    // Si tiene una ruta (`to`), conviértela en comando de navegación
    if (item.to) {
      return {
        ...item, command: () => router.push(item.to)
      };
    }
    // Si tiene submenú, procesarlo recursivamente
    if (item.items) {
      return {
        ...item, items: procesarComandos(item.items)
      };
    }
    // Si no tiene `to` ni `command`, devolver tal cual (puede ser un separador o título)
    return item;

  });
}


// const processedMenu = computed(() => {
//   return menuItems.value.map((item: any) => {
//
//     if (item.command === "logout") {
//       return { ...item, command: () => handleLogout() }
//     }
//
//     if (item.to) {
//       return { ...item, command: () => router.push(item.to) }
//     }
//     if (item.items) {
//       return { ...item, items: processSubMenu(item.items) }
//     }
//     return item
//   })
// })
//
// function processSubMenu(items: any[]) {
//   return items.map(item => {
//     if (item.command === "logout") {
//       return {...item, command: () => handleLogout()}
//     }
//     if (item.to) {
//       return {...item, command: () => router.push(item.to)}
//     }
//     if (item.items) {
//       return {...item, items: processSubMenu(item.items)}
//     }
//     return item
//   })
// }

async function handleLogout() {
  Swal.fire({
    title: "¿Cerrar sesión?",
    text: "Se cerrará tu sesión actual",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Sí, salir",
    confirmButtonColor: '#334155',
    cancelButtonText: "Cancelar",
    cancelButtonColor: '#ef4444',
  }).then(result => {
    if (result.isConfirmed) {
      auth.logoutAndRedirect()
    }
  })
}
</script>

<style scoped>
/* Estilo general del Menubar */
.custom-menubar {
  border: none;
  background: #fff;
  padding: 1rem 1rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
}

/* Logo */
.logo-section {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #334155;
}

.logo-img {
  width: 60px;
  height: 60px;
  border-radius: 6px;
  margin-right: 8px;
}

.app-name {
  font-weight: bold;
  font-size: 1.1rem;
}

/* Perfil de usuario */
.user-profile {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
  cursor: pointer;
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 2px solid #e2e8f0;
}

/*----- Perfil de Usuario ------*/
.user-info {
  display: flex;
  flex-direction: column;
  font-weight: bold;
  text-align: left;
}

.user-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.95rem;
  text-transform: uppercase;
}

.user-role {
  font-weight: bold;
  font-size: 0.8rem;
  color: #64748b;
}
</style>
