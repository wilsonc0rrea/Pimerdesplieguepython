// // composables/useMenu.js
// import { useAuthStore } from '@/stores/auth';
//
// export function useMenu() {
//   const auth = useAuthStore();
//
//   const filtrarMenu = (items,permisos) => {
//     // // Si permisos está vacío, devuelve [] (no filtra)
//     // if (!permisos || Object.keys(permisos).length === 0) {
//     //   return []; // o items si quieres mostrar todo sin permisos
//     // }
//     return items
//       .map(item => {
//         // Si el ítem tiene submenú (item.items), filtrarlo recursivamente
//         if (item.items) {
//           const subItemsFiltrados = filtrarMenu(item.items, permisos);
//           // Solo mantener el ítem padre si tiene subítems visibles
//           return subItemsFiltrados.length > 0
//             ? { ...item, items: subItemsFiltrados }
//             : null;
//         }
//         // Si es un ítem hoja, verificar permiso de "ver"
//         const modulo = item.modulo || item.label;
//         if (permisos[modulo]?.ver) {
//           return item;
//         }
//         // Si no tiene permiso de "ver", ocultarlo
//         return null;
//       })
//       .filter(Boolean); // eliminar nulls
//   };
//
//   return { filtrarMenu };
// }
// composables/useMenu.js
import { useAuthStore } from '@/stores/auth'

export function useMenu() {
  const auth = useAuthStore()

  const filtrarMenu = (items = [], permisos = {}) => {
    try {
      if (!Array.isArray(items)) {
        console.warn("⚠️ filtrarMenu: 'items' no es un array:", items)
        return []
      }

      if (!permisos || typeof permisos !== "object") {
        console.warn("⚠️ filtrarMenu: 'permisos' inválido:", permisos)
        return items // Si no hay permisos, mostrar todo para depurar
      }

      const resultado = items
        .map(item => {
          // 🧩 Si tiene submenú, filtrarlo recursivamente
          if (item.items && Array.isArray(item.items)) {
            const subItemsFiltrados = filtrarMenu(item.items, permisos)
            return subItemsFiltrados.length > 0
              ? { ...item, items: subItemsFiltrados }
              : null
          }

          // 🧠 Determinar el nombre del módulo
          const modulo = item.modulo || item.label
          if (!modulo) {
            console.warn("⚠️ Item sin módulo o label:", item)
            return null
          }

          // ✅ Permiso 'ver'
          if (permisos[modulo]?.ver) {
            return item
          }

          return null
        })
        .filter(Boolean)

      // 🔍 Logging opcional para depurar
      return resultado
    } catch (error) {
      return []
    }
  }

  return { filtrarMenu }
}
