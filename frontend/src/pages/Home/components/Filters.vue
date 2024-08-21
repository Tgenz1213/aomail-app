<template>
  <div class="flex items-stretch border-l h-12 2xl:h-14 space-x-2 px-4">
    <button 
    v-for="(filter, index) in visibleFilters" 
    :key="index"
    @click="setActiveFilter(filter.name)"
    :class="[
        'px-3 py-1 focus:outline-none flex items-center relative',
        activeFilter === filter.name ? 'text-black' : 'text-gray-600 hover:bg-gray-100'
    ]"
    >
    {{ filter.name }}
    <div v-if="activeFilter === filter.name" class="absolute bottom-0 left-0 w-full h-0.5 bg-black"></div>
    </button>
    <div class="relative flex items-center">
      <button 
          v-if="hiddenFiltersCount > 0"
          @click="toggleMoreFilters" 
          class="px-2 py-1 text-gray-600 rounded hover:bg-gray-100 focus:outline-none"
          data-more-filters
      >
          {{ hiddenFiltersCount }} more...
      </button>
      <!-- Modal to display all filters -->
      <div 
          v-if="showAllFiltersModal && filters" 
          ref="moreFiltersModal"
          class="absolute top-full right-0 mt-1 z-50 w-64 rounded bg-white shadow-sm ring-1 ring-black ring-opacity-10"
      >
          <div class="p-2">
          <h2 class="text-sm font-bold mb-2">All filters</h2>
          <div class="space-y-1 h-full overflow-y-auto">
              <button 
              v-for="filter in filters" 
              :key="filter.name"
              @click="setActiveFilter(filter.name)"
              class="w-full text-left px-2 py-1 text-sm hover:bg-gray-100 focus:outline-none rounded"
              >
              {{ filter.name }}
              </button>
          </div>
          </div>
      </div>
    </div>
    <button @click="openNewFilterModal" class="px-2 py-1 text-gray-600 hover:bg-gray-100 focus:outline-none">+</button>
  </div>
</template>
<script setup lang="ts">
import { Ref, computed, ref, inject, watch } from 'vue';
import { Filter } from "../utils/types";

const openNewFilterModal = inject('openNewFilterModal') as () => void;
const filters = inject('filters') as Ref<Filter[]>;

const activeFilter = ref('');
const showAllFiltersModal = ref(false);

const hiddenFiltersCount = computed(() => {
  return Math.max(0, filters.value.length - visibleFilters.value.length);
});

const visibleFilters = computed(() => {
  return filters.value.slice(0, 4);
});

const toggleMoreFilters = () => {
  showAllFiltersModal.value = !showAllFiltersModal.value;
};

const setActiveFilter = (filterName: string) => {
  activeFilter.value = filterName;
  showAllFiltersModal.value = false;
};

</script>