<template>
  <div>
    <button @click="handleClick"
            :class="buttonClass">
      <div class="flex items-center">
        <i :class="item.icon" class="mr-2 text-blue-500"></i>
        <span>{{ item.label }}</span>
      </div>
      <i v-if="hasChildren" :class="isOpen ? 'pi pi-angle-down' : 'pi pi-angle-right'" class="text-gray-500"></i>
    </button>

    <Transition name="slide">
      <div v-if="isOpen && hasChildren" class="ml-4 mt-1 space-y-1">
        <MenuItemMobile v-for="(child, idx) in item.items" :key="idx" :item="child" />
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

const isOpen = ref(false)
const hasChildren = computed(() => props.item.items && props.item.items.length > 0)

const buttonClass = computed(() => {
  return `flex justify-between items-center w-full p-3 bg-white rounded shadow-sm hover:bg-gray-50 transition-colors ${hasChildren.value ? 'cursor-pointer' : ''}`
})

const handleClick = () => {
  if (hasChildren.value) {
    isOpen.value = !isOpen.value
  } else if (props.item.command) {
    props.item.command()
  }
}
</script>
