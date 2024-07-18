<template>
  <div class="">
    <div
      class="sticky top-0 z-40 flex shrink-0 items-center gap-x-4 border-b border-black shadow-sm border-opacity-10 bg-white px-4 sm:gap-x-6 sm:px-6 lg:px-8"
      :style="{ height: height }"
    >
      <div class="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
        <form class="relative flex flex-1 items-center" action="#" method="GET">
          <label for="search-field" class="sr-only">{{ $t('constants.userActions.searchbar_search') }}</label>
          <MagnifyingGlassIcon class="pointer-events-none absolute left-0 h-5 w-5 text-gray-400"
            aria-hidden="true" />
          <input v-model="searchQuery" id="search-field"
            class="h-full w-full border-0 py-0 pl-8 pr-8 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm"
            :placeholder="$t('rulesPage.search')" type="search" name="search" />
          <button v-if="searchQuery" type="button" @click="clearSearch"
            class="absolute right-0 flex items-center pr-2">
            <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"
              fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd"
                d="M10 9.293l4.646-4.647a.5.5 0 01.708.708L10.707 10l4.647 4.646a.5.5 0 01-.708.708L10 10.707l-4.646 4.647a.5.5 0 01-.708-.708L9.293 10 4.646 5.354a.5.5 0 01.708-.708L10 9.293z"
                clip-rule="evenodd" />
            </svg>
          </button>
          <button v-if="showFilterButton" @click="toggleFilterPopup" type="button"
            class="absolute right-0 flex items-center pr-2 sm:pr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z" clip-rule="evenodd" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  </div>

  <!-- Filter Popup -->
  <div v-if="showFilterPopup" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen px-4 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="toggleFilterPopup"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium leading-6 text-gray-900" id="modal-title">Filtres</h3>
            <button @click="toggleFilterPopup" class="text-gray-400 hover:text-gray-500">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div v-for="(field, index) in filterFields" :key="index">
              <label :for="field.name" class="block text-sm font-medium text-gray-700">{{ field.label }}</label>
              <input v-if="field.type === 'text'" :type="field.type" :placeholder="field.placeholder" :id="field.name" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
              <input v-if="field.type === 'checkbox'" :type="field.type" :id="field.name" class="form-checkbox h-4 w-4 text-indigo-600">
              <select v-if="field.type === 'select'" :id="field.name" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                <option v-for="option in field.options" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button @click="applyFilters" type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-sm">
            Rechercher
          </button>
          <button @click="toggleFilterPopup" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
            Annuler
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { MagnifyingGlassIcon } from '@heroicons/vue/20/solid';

const props = defineProps({
  height: {
    type: String,
    default: '5rem' // équivalent à h-20 en Tailwind
  },
  showFilterButton: {
    type: Boolean,
    default: false
  },
  filterFields: {
    type: Array,
    default: () => []
  }
});

const searchQuery = ref('');
const showFilterPopup = ref(false);
const emits = defineEmits(['updateSearchQuery']);

const clearSearch = () => {
  searchQuery.value = '';
};

const toggleFilterPopup = () => {
  showFilterPopup.value = !showFilterPopup.value;
};

const applyFilters = () => {
  // Logique pour appliquer les filtres
  showFilterPopup.value = false;
};

// Émettre l'événement chaque fois que searchQuery change
watch(searchQuery, (newValue) => {
  emits('updateSearchQuery', newValue);
});
</script>