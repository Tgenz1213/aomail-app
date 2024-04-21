<template>
  <Listbox as="div" v-model="selected">
    <ListboxButton
      class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 sm:text-sm sm:leading-6"
    >
      <span class="block truncate">{{ selected ? selected.name : 'Aucune' }}</span>
      <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
      </span>
    </ListboxButton>
    <transition
      leave-active-class="transition ease-in duration-100"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <ListboxOptions
        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
      >
        <ListboxOption
          as="template"
          v-for="type in attachmentTypes"
          :key="type.extension"
          :value="type"
          v-slot="{ active, selected }"
        >
          <li
            :class="[active ? 'bg-gray-500 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']"
          >
            <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
              {{ type.name }} {{ type.extension }}
            </span>
            <span
              v-if="selected"
              :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']"
            >
              <CheckIcon class="h-5 w-5" aria-hidden="true" />
            </span>
          </li>
        </ListboxOption>
      </ListboxOptions>
    </transition>
  </Listbox>
</template>

<script setup>
import { ref } from 'vue'
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/vue'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'

const attachmentTypes = [
  { extension: ".docx", name: "Word Document" },
  { extension: ".xlsx", name: "Excel Spreadsheet" },
  { extension: ".pptx", name: "PowerPoint Presentation" },
  { extension: ".pdf", name: "PDF Document" },
  { extension: ".jpg", name: "JPEG Image" },
  { extension: ".png", name: "PNG Image" },
  { extension: ".gif", name: "GIF Image" },
  { extension: ".txt", name: "Text Document" },
  { extension: ".zip", name: "ZIP Archive" },
  { extension: ".mp3", name: "MP3 Audio" },
  { extension: ".mp4", name: "MP4 Video" },
  { extension: ".html", name: "HTML Document" },
  { extension: null, name: "Aucune" },
]

const selected = ref(null)
</script>
