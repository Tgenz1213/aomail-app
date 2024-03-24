<template>
  <RadioGroup v-model="selectedColor">
    <!-- Split colors into three rows -->
    <div class="flex flex-wrap justify-center">
      <!-- Iterate over each row -->
      <template v-for="rowIndex in 3" :key="rowIndex">
        <!-- Start a new row -->
        <div class="flex items-center mb-1">
          <!-- Iterate over ten colors in each row -->
          <template v-for="colIndex in 10" :key="(rowIndex - 1) * 10 + colIndex">
            <!-- Calculate the index of the color -->
            <template v-if="(rowIndex - 1) * 10 + colIndex <= colors.length">
              <!-- Render the color -->
              <RadioGroupOption :value="colors[(rowIndex - 1) * 10 + colIndex - 1]" v-slot="{ active, checked }"
                @click="$emit('colorSelected', colors[(rowIndex - 1) * 10 + colIndex - 1].bgColor)">
                <div :class="[
    colors[(rowIndex - 1) * 10 + colIndex - 1].selectedColor,
    active && checked ? 'ring ring-offset-1' : '',
    !active && checked ? 'ring-2' : '',
    'relative -m-0.5 mt-3 flex cursor-pointer items-center justify-center rounded-full p-0.5 focus:outline-none mx-1 mb-2'
  ]">
                  <span aria-hidden="true" :class="[
    colors[(rowIndex - 1) * 10 + colIndex - 1].bgColor,
    'h-8 w-8 rounded-full border border-black border-opacity-10'
  ]"></span>
                </div>
              </RadioGroupOption>
            </template>
          </template>
        </div>
      </template>
    </div>
  </RadioGroup>
</template>


<script setup>
import { ref } from 'vue'
import { RadioGroup, RadioGroupOption } from '@headlessui/vue'


const props = defineProps({
  initialColor: String
})

const colors = [
  { bgColor: 'bg-gradient-to-r from-orange-200 to-rose-200', selectedColor: 'ring-orange-100' },
  { bgColor: 'bg-gradient-to-r from-yellow-200 via-pink-200 to-pink-300', selectedColor: 'ring-pink-100' },
  { bgColor: 'bg-gradient-to-r from-fuchsia-200 to-pink-200', selectedColor: 'ring-fuchsia-100' },
  { bgColor: 'bg-gradient-to-r from-green-100 to-purple-200', selectedColor: 'ring-green-200' },
  { bgColor: 'bg-gradient-to-r from-pink-200 via-purple-200 to-indigo-200', selectedColor: 'ring-purple-100' },
  { bgColor: 'bg-gradient-to-r from-purple-200 via-violet-200 to-purple-200', selectedColor: 'ring-purple-100' },
  { bgColor: 'bg-gradient-to-r from-purple-200 to-yellow-200', selectedColor: 'ring-yellow-100' },
  { bgColor: 'bg-gradient-to-r from-yellow-100 via-yellow-200 to-yellow-300', selectedColor: 'ring-yellow-100' },
  { bgColor: 'bg-gradient-to-r from-yellow-100 to-yellow-200', selectedColor: 'ring-yellow-100' },
  { bgColor: 'bg-gradient-to-r from-purple-200 to-yellow-200', selectedColor: 'ring-yellow-100' },
  { bgColor: 'bg-gradient-to-r from-rose-200 to-orange-100', selectedColor: 'ring-orange-100' },
  { bgColor: 'bg-gradient-to-b from-orange-200 to-yellow-100', selectedColor: 'ring-orange-100' },
  { bgColor: 'bg-gradient-to-r from-orange-200 to-orange-100', selectedColor: 'ring-orange-100' },
  { bgColor: 'bg-gradient-to-r from-yellow-200 to-red-200', selectedColor: 'ring-red-100' },
  { bgColor: 'bg-gradient-to-r from-yellow-100 via-pink-100 to-pink-200', selectedColor: 'ring-pink-100' },
  { bgColor: 'bg-gradient-to-r from-pink-100 to-pink-200', selectedColor: 'ring-pink-100' },
  { bgColor: 'bg-gradient-to-r from-rose-300 to-pink200', selectedColor: 'ring-rose-100' },
  { bgColor: 'bg-gradient-to-r from-rose-100 via-fuchsia-200 to-indigo-200', selectedColor: 'ring-rose-100' },
  { bgColor: 'bg-gradient-to-r from-yellow-200 via-green-200 to-green-300', selectedColor: 'ring-green-100' },
  { bgColor: 'bg-gradient-to-r from-green-200 via-green-200 to-blue-300', selectedColor: 'ring-green-100' },
  { bgColor: 'bg-gradient-to-r from-green-100 to-green-200', selectedColor: 'ring-green-100' },
  { bgColor: 'bg-gradient-to-r from-green-100 via-green-200 to-green-200', selectedColor: 'ring-green-100' },
  { bgColor: 'bg-gradient-to-r from-yellow-100 via-green-100 to-green-200', selectedColor: 'ring-green-100' },
  { bgColor: 'bg-gradient-to-r from-green-100 to-purple-200', selectedColor: 'ring-green-100' },
  { bgColor: 'bg-gradient-to-r from-blue-200 to-blue-300', selectedColor: 'ring-blue-100' },
  { bgColor: 'bg-gradient-to-b from-sky-300 to-sky-200', selectedColor: 'ring-blue-100' },
  { bgColor: 'bg-gradient-to-r from-sky-300 to-blue-300', selectedColor: 'ring-blue-100' },
  { bgColor: 'bg-gradient-to-r from-cyan-100 to-cyan-200', selectedColor: 'ring-cyan-100' },
  { bgColor: 'bg-gradient-to-r from-sky-300 to-cyan-200', selectedColor: 'ring-cyan-100' },
  { bgColor: 'bg-gradient-to-r from-blue-300 to-emerald-200', selectedColor: 'ring-blue-100' },
]

const findColor = (colorValue) => {
  return colors.find(color => color.bgColor === colorValue) || colors[0];
}
const selectedColor = ref(findColor(props.initialColor));
</script>