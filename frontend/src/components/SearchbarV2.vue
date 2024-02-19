<!--
  This example requires some changes to your config:
  
  ```
  // tailwind.config.js
  module.exports = {
    // ...
    plugins: [
      // ...
      require('@tailwindcss/forms'),
    ],
  }
  ```
-->
<template>
  <div class="">
    <div
      class="sticky top-0 z-40 flex h-20 shrink-0 items-center gap-x-4 shadow bg-white px-4 sm:gap-x-6 sm:px-6 lg:px-8">
      <div class="flex flex-1 gap-x-4 self-stretch lg:gap-x-6 pt-3.5">
        <form class="relative flex flex-1" action="#" method="GET">
          <label for="search-field" class="sr-only">Rechercher</label>
          <MagnifyingGlassIcon class="pointer-events-none absolute inset-y-0 left-0 h-full w-5 text-gray-400"
            aria-hidden="true" />
          <input v-model="searchQuery" id="search-field"
            class="h-full w-full border-0 py-0 pl-8 pr-0 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm"
            placeholder="Recherche..." type="search" name="search" />
        </form>
      </div>
    </div>
  </div>
</template>
  
<script setup>
/*import { ref } from 'vue'
import {
  CalendarIcon,
  ChartPieIcon,
  DocumentDuplicateIcon,
  FolderIcon,
  HomeIcon,
  UsersIcon,
} from '@heroicons/vue/24/outline'*/
import { MagnifyingGlassIcon } from '@heroicons/vue/20/solid';

/*
const navigation = [
  { name: 'Dashboard', href: '#', icon: HomeIcon, current: true },
  { name: 'Team', href: '#', icon: UsersIcon, current: false },
  { name: 'Projects', href: '#', icon: FolderIcon, current: false },
  { name: 'Calendar', href: '#', icon: CalendarIcon, current: false },
  { name: 'Documents', href: '#', icon: DocumentDuplicateIcon, current: false },
  { name: 'Reports', href: '#', icon: ChartPieIcon, current: false },
]
const teams = [
  { id: 1, name: 'Heroicons', href: '#', initial: 'H', current: false },
  { id: 2, name: 'Tailwind Labs', href: '#', initial: 'T', current: false },
  { id: 3, name: 'Workcation', href: '#', initial: 'W', current: false },
]
const userNavigation = [
  { name: 'Your profile', href: '#' },
  { name: 'Sign out', href: '#' },
]
 
const sidebarOpen = ref(false)*/
</script>