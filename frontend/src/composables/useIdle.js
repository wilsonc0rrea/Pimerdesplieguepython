// src/composables/useIdle.js
import {onMounted, onUnmounted} from 'vue'
import Swal from 'sweetalert2'
import {useAuthStore} from '@/stores/auth'

// tiempos (config)
const DEFAULT_IDLE_MS = 30 * 60 * 1000  // 15 minutos inactividad -> cerrar sesión
const WARNING_MS = 120 * 1000            // Mostrar advertencia 2 minuto antes

export function useIdle({
                          idleTime = DEFAULT_IDLE_MS,
                          warningTime = WARNING_MS,
                          onTimeout = null  // opcional callback
                        } = {}) {
  const auth = useAuthStore()
  let idleTimer = null
  let warningTimer = null

  const events = ['mousemove', 'mousedown', 'keypress', 'touchstart', 'wheel', 'scroll']

  function clearTimers() {
    if (idleTimer) {
      clearTimeout(idleTimer);
      idleTimer = null
    }
    if (warningTimer) {
      clearTimeout(warningTimer);
      warningTimer = null
    }
  }

  function startTimers() {
    clearTimers()
    // tiempo hasta mostrar warning
    const timeUntilWarning = Math.max(0, idleTime - warningTime)

    warningTimer = setTimeout(() => {
      showWarning()
    }, timeUntilWarning)

    // tiempo final (logout)
    idleTimer = setTimeout(() => {
      doLogout()
    }, idleTime)
  }

  function resetTimers() {
    startTimers()
  }

  function showWarning() {
    // muestra modal con SweetAlert2 y cuenta regresiva
    Swal.fire({
      title: 'Inactividad detectada',
      text: 'Serás desconectado por inactividad en 120 segundos. ¿Deseas permanecer conectado?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Permanecer conectado',
      cancelButtonText: 'Cerrar sesión',
      timer: warningTime,
      timerProgressBar: true,
      allowOutsideClick: false,
      allowEscapeKey: false
    }).then(result => {
      if (result.isConfirmed) {
        // usuario quiere seguir -> resetear timers
        resetTimers()
      } else {
        // usuario cancela -> logout
        doLogout()
      }
    })
  }

  async function doLogout() {
    clearTimers()
    // opcional: avisar backend para invalidar refresh token/session
    try {
      await fetch('/api/logout', {method: 'POST', credentials: 'include'})
    } catch (e) { /* ignora errores */
    }

    // limpiar store y redirigir
    if (onTimeout) onTimeout()
    else auth.logoutAndRedirect?.() // usa el método del store
  }

  function activityHandler() {
    resetTimers()
  }

  function visibilityHandler() {
    if (document.visibilityState === 'visible') {
      // reinicia cuando vuelva a la pestaña
      resetTimers()
    }
  }

  function start() {
    // attach listeners
    events.forEach(ev => window.addEventListener(ev, activityHandler))
    document.addEventListener('visibilitychange', visibilityHandler)
    startTimers()
  }

  function stop() {
    events.forEach(ev => window.removeEventListener(ev, activityHandler))
    document.removeEventListener('visibilitychange', visibilityHandler)
    clearTimers()
  }

  // hook lifecycle
  onMounted(() => {
    start()
  })
  onUnmounted(() => {
    stop()
  })

  return {start, stop, resetTimers, doLogout}
}
