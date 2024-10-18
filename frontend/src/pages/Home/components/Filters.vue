<template>
  <div class="flex items-stretch border-l h-12 2xl:h-14 space-x-2 px-4">
    <div
      v-for="(filter, index) in visibleFilters"
      :key="index"
      class="relative group flex items-center"
    >
      <div
        class="flex items-center h-full relative group hover:bg-gray-100 transition-all duration-200"
      >
        <button
          @click="setActiveFilter(filter.name)"
          class="h-full px-3 focus:outline-none flex items-center justify-center relative"
        >
          <span
            class="relative z-10"
            :class="
              selectedFilter?.name === filter.name
                ? 'text-black font-medium'
                : 'text-black font-normal'
            "
          >
            {{ filter.name }}
          </span>
        </button>
        <div
          class="w-0 group-hover:w-6 overflow-hidden transition-all duration-200 flex items-center h-full"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-4 h-4 cursor-pointer flex-shrink-0 ml-1 mr-2"
            @click.stop="openUpdateFilterModal(filter)"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
            />
          </svg>
        </div>
        <div
          class="absolute bottom-0 left-0 w-full h-0.5 bg-black opacity-0 group-hover:opacity-100 transition-all duration-200"
          :class="{ 'opacity-100': selectedFilter?.name === filter.name }"
        ></div>
      </div>
    </div>
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
            <div
              v-for="filter in allFilters"
              :key="filter.name"
              class="flex items-center hover:bg-gray-100 rounded"
            >
              <button
                @click="setActiveFilter(filter.name)"
                class="flex-grow text-left px-2 py-1 text-sm focus:outline-none"
              >
                {{ filter.name }}
              </button>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-4 h-4 mr-2 cursor-pointer"
                @click.stop="openUpdateFilterModal(filter)"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
    <button
      @click="openNewFilterModal"
      class="px-2 py-1 text-gray-600 hover:bg-gray-100 focus:outline-none"
    >
      +
    </button>
  </div>
</template>
<script setup lang="ts">
import { Ref, computed, ref, inject, watch } from "vue";
import { Filter } from "../utils/types";

const openNewFilterModal = inject("openNewFilterModal") as () => void;
const scroll = inject('scroll', () => {}) as () => void;
const handleScroll = inject('handleScroll', () => {}) as () => void;
const openUpdateFilterModal = inject("openUpdateFilterModal") as (
  filter: Filter
) => void;
const fetchEmailsData = inject("fetchEmailsData") as (
  categoryName: string
) => Promise<void>;
const fetchFiltersData = inject("fetchFiltersData") as (
  categoryName: string
) => Promise<void>;
const filters = inject("filters") as Ref<{ [categoryName: string]: Filter[] }>;
const selectedCategory = inject("selectedCategory") as Ref<string>;
const selectedFilter = inject("selectedFilter") as Ref<Filter | undefined>;
const activeFilters = inject("activeFilters") as Ref<{
  [category: string]: Filter | undefined;
}>;
const showAllFiltersModal = ref(false);

const allFilters = computed((): Filter[] => {
  return filters.value[selectedCategory.value] || [];
});

const visibleFilters = computed((): Filter[] => {
  return allFilters.value.slice(0, 4);
});

const hiddenFiltersCount = computed((): number => {
  return Math.max(0, allFilters.value.length - visibleFilters.value.length);
});

const toggleMoreFilters = () => {
  showAllFiltersModal.value = !showAllFiltersModal.value;
};

const setActiveFilter = async (filterName: string) => {
  showAllFiltersModal.value = false;

  const filterArray = filters.value[selectedCategory.value];
  if (filterArray) {
    const filter = filterArray.find((f) => f.name === filterName);

    if (filter) {
      activeFilters.value[selectedCategory.value] = filter;
      await fetchEmailsData(selectedCategory.value);

      const container = document.querySelector(".custom-scrollbar");
      if (container) {
        container.scrollTop = 0;
      }

      scroll();
      handleScroll();

      localStorage.setItem(
        "activeFilters",
        JSON.stringify(activeFilters.value)
      );
    } else {
      console.error(
        `Filter with name "${filterName}" not found in category "${selectedCategory.value}".`
      );
      activeFilters.value[selectedCategory.value] = undefined;
    }
  } else {
    console.error(`No filters found for category "${selectedCategory.value}".`);
    activeFilters.value[selectedCategory.value] = undefined;
  }
};

watch(selectedCategory, async (newCategory) => {
  if (!activeFilters.value[newCategory]) {
    activeFilters.value[newCategory] = undefined;
  }

  await fetchEmailsData(newCategory);
  await fetchFiltersData(newCategory);

  showAllFiltersModal.value = false;
});
</script>
