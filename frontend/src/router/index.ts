import { createRouter, createWebHistory } from 'vue-router'
// import { isLoggedIn, restoreSession } from '../stores/auth.js'
import { useAuthStore } from '../stores/auth.js'
// import LoginView from '../views/Auth/LoginView.vue'
// import RegisterView from '../views/Auth/RegisterView.vue'
const routes = [

  {
    path: '/logout',
    redirect: '/Auth/login'
  },
  // Ruta raíz: redirige a login
  {
    path: '/',
    redirect: '/Auth/login'
  },

  // Rutas de autenticación (públicas)
  {
    path: '/Auth/login',
    name: 'Login',
    component: () => import('../views/Auth/LoginView.vue'),
    meta: { public: true }  // ← ¡Pública!
  },
  {
    path: '/Auth/register',
    name: 'Register',
    component: () => import('../views/Auth/RegisterView.vue'),
    meta: { public: true }  // ← ¡Pública!
  },

  // Rutas protegidas (requieren login)
  {
    path: '/dashboard',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: { requiresAuth: true }  // ← ¡Protegida!
  },
  {
    path: '/usuarios/lista',
    component: () => import('../views/Usuarios/Lista.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/usuarios/crear',
    component: () => import('../views/Usuarios/Crear.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/usuarios/reportes/diarios',
    component: () => import('../views/Usuarios/ReportesDiarios.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/usuarios/reportes/mensuales',
    component: () => import('../views/Usuarios/ReportesMensuales.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/perfil',
    component: () => import('../views/Config/Perfil.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/sistema',
    component: () => import('../views/Config/Sistema.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/clientes',
    component: () => import('../views/Config/Clientes.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/motores',
    component: () => import('../views/Config/Motores.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/precios',
    component: () => import('../views/Config/Precios.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/reportes',
    component: () => import('../views/Config/Reportes.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/listadoreporte',
    component: () => import('../views/Config/ListadoReportes.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/cargos',
    component: () => import('../views/Config/Cargos.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/ttrabajos',
    component: () => import('../views/Config/Tipotrabajos.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/permisos',
    component: () => import('../views/Config/Permisos.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/roles',
    component: () => import('../views/Config/Roles.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/empleados',
    component: () => import('../views/Config/Empleados.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/finanzas/carteraxcobrar',
    component: () => import('../views/Finanzas/Carteraxcobrar.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/finanzas/saldos',
    component: () => import('../views/Finanzas/Saldos.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/finanzas/egresos',
    component: () => import('../views/Finanzas/Egresos.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/finanzas/ingresos',
    component: () => import('../views/Finanzas/Ingresos.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/estadisticaservicio',
    component: () => import('../views/Config/Estadisticaservicio.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/config/estadisticatrabajos',
    component: () => import('../views/Config/Estadisticatrabajos.vue'),
    meta: { requiresAuth: true }
  },
  // Redirección para rutas no encontradas
  {
    path: '/:pathMatch(.*)*',
    redirect: '/Auth/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 🔑 Guarda de navegación global con Pinia
// router.beforeEach((to, from, next) => {
//   const auth = useAuthStore()   // 👈 Obtén la instancia del store
//   if (to.meta.requiresAuth && !auth.isLoggedIn) {
//     next('/Auth/login')
//   } else if (auth.isLoggedIn && (to.path === '/Auth/login' || to.path === '/Auth/register')) {
//     next('/dashboard')
//   } else {
//     next()
//   }
// })
// 🔑 Guarda de navegación global con Pinia
router.beforeEach((to, from, next) => {
  // Solo redirige si intenta acceder a login/register estando logueado
  const auth = useAuthStore()

  if (to.meta.requiresAuth && auth.isLoggedIn && (to.path === '/Auth/login' || to.path === '/Auth/register')) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
