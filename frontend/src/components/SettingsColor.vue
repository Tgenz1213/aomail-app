<!--<template>
  <RadioGroup v-model="selectedColor">
    <RadioGroupLabel class="block text-sm font-medium leading-6 text-gray-900">Couleur de fond</RadioGroupLabel>
    <div class="mt-4 flex items-center space-x-3"> 
    <div class="mt-2 flex items-center justify-center space-x-3">
      <RadioGroupOption as="template" v-for="color in colors" :key="color.name" :value="color" v-slot="{ active, checked }">
      <div :class="[color.selectedColor, active && checked ? 'ring ring-offset-1' : '', !active && checked ? 'ring-2' : '', 'relative -m-0.5 flex cursor-pointer items-center justify-center rounded-full p-0.5 focus:outline-none']">
        <RadioGroupLabel as="span" class="sr-only">{{ color.name }}</RadioGroupLabel>
        <div :class="['ring-container', color.ringColor]"></div>
        <span aria-hidden="true" :class="[color.bgColor, 'h-8 w-8 rounded-full border border-black border-opacity-10']" />
      </div>
    </RadioGroupOption>
    </div>
  </RadioGroup>
</template>-->

<template>
  <RadioGroup v-model="selectedColor">
    <div class="flex flex-wrap mt-1 justify-center">
      <RadioGroupOption as="template" v-for="color in colors" :key="color.name" :value="color"
        v-slot="{ active, checked }" @click="$emit('colorSelected', color.bgColor)">
        <div
          :class="[color.selectedColor, active && checked ? 'ring ring-offset-1' : '', !active && checked ? 'ring-2' : '', 'relative -m-0.5 mt-3 flex cursor-pointer items-center justify-center rounded-full p-0.5 focus:outline-none mx-1 mb-2']">
          <RadioGroupLabel as="span" class="sr-only">{{ color.name }}</RadioGroupLabel>
          <span aria-hidden="true"
            :class="[color.bgColor, 'h-8 w-8 rounded-full border border-black border-opacity-10']"></span>
        </div>
      </RadioGroupOption>
    </div>
  </RadioGroup>
</template>


<script setup>
import { ref, watch } from 'vue'
import { RadioGroup, RadioGroupLabel, RadioGroupOption } from '@headlessui/vue'

const props = defineProps({
  initialColor: String
})

const emits = defineEmits(['colorSelected']);

const colors = [
  { name: 'Gradient_Orange_Rose', bgColor: 'bg-gradient-to-r from-orange-200 to-rose-200', selectedColor: 'ring-orange-100' }, // TESTED
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-yellow-200 via-pink-200 to-pink-300', selectedColor: 'ring-pink-100' },
  { name: 'Gradient_Fuschia_Rose', bgColor: 'bg-gradient-to-r from-fuchsia-200 to-pink-200', selectedColor: 'ring-fuchsia-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-green-100 to-purple-200', selectedColor: 'ring-green-200' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-pink-200 via-purple-200 to-indigo-200', selectedColor: 'ring-purple-100' },
  { name: 'Gradient_Orange_Rose', bgColor: 'bg-gradient-to-r from-purple-200 via-violet-200 to-purple-200', selectedColor: 'ring-purple-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-purple-200 to-yellow-200', selectedColor: 'ring-yellow-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-yellow-100 via-yellow-200 to-yellow-300', selectedColor: 'ring-yellow-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-yellow-100 to-yellow-200', selectedColor: 'ring-yellow-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-purple-200 to-yellow-200', selectedColor: 'ring-yellow-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-rose-200 to-orange-100', selectedColor: 'ring-orange-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-b from-orange-200 to-yellow-100', selectedColor: 'ring-orange-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-orange-200 to-orange-100', selectedColor: 'ring-orange-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-yellow-200 to-red-200', selectedColor: 'ring-red-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-yellow-100 via-pink-100 to-pink-200', selectedColor: 'ring-pink-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-pink-100 to-pink-200', selectedColor: 'ring-pink-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-rose-300 to-pink200', selectedColor: 'ring-rose-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-rose-100 via-fuchsia-200 to-indigo-200', selectedColor: 'ring-rose-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-yellow-200 via-green-200 to-green-300', selectedColor: 'ring-green-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-green-200 via-green-200 to-blue-300', selectedColor: 'ring-green-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-green-100 to-green-200', selectedColor: 'ring-green-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-green-100 via-green-200 to-green-200', selectedColor: 'ring-green-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-yellow-100 via-green-100 to-green-200', selectedColor: 'ring-green-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-green-100 to-purple-200', selectedColor: 'ring-green-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-blue-200 to-blue-300', selectedColor: 'ring-blue-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-b from-sky-300 to-sky-200', selectedColor: 'ring-blue-100' }, // TESTED
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-sky-300 to-blue-300', selectedColor: 'ring-blue-100' }, // TESTED
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-cyan-100 to-cyan-200', selectedColor: 'ring-cyan-100' },
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-sky-300 to-cyan-200', selectedColor: 'ring-cyan-100' }, // TESTED
  { name: 'Gradient_', bgColor: 'bg-gradient-to-r from-blue-300 to-emerald-200', selectedColor: 'ring-blue-100' }, // TESTED
]

// Function to find the initial color
const findColor = (colorValue) => {
  return colors.find(color => color.bgColor === colorValue) || colors[0];
}

const selectedColor = ref(findColor(props.initialColor))

// Watch for changes in the initialColor prop
watch(() => props.initialColor, (newColor) => {
  selectedColor.value = findColor(newColor);
});

watch(selectedColor, (newValue) => {
  emits('colorSelected', newValue.bgColor);
});
</script>