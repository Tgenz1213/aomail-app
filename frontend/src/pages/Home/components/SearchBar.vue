<template>
    <div class="sticky z-20 top-0 bg-white w-full flex relative border-b border-black shadow-sm border-opacity-10">
        <!-- Search bar -->
        <div class="z-40 flex flex-1 h-12 2xl:h-14 shrink-0 items-center gap-x-4 px-4 sm:gap-x-6 sm:px-6 lg:px-8">
            <div class="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
                <div class="relative flex flex-1">
                    <label for="search-field" class="sr-only">{{ $t("constants.userActions.searchbar_search") }}</label>
                    <MagnifyingGlassIcon
                        class="pointer-events-none absolute inset-y-0 left-0 h-full w-5 text-gray-400"
                        aria-hidden="true"
                    />
                    <input
                        v-model="searchQuery"
                        id="search-field"
                        class="h-full w-full border-0 py-0 pl-8 pr-8 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm"
                        :placeholder="$t('rulesPage.search')"
                        type="search"
                        name="search"
                    />
                    <button
                        v-if="searchQuery"
                        type="button"
                        @click="clearSearch"
                        class="absolute inset-y-0 right-0 flex items-center pr-2"
                    >
                        <svg
                            class="h-5 w-5 text-gray-400"
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 20 20"
                            fill="currentColor"
                            aria-hidden="true"
                        >
                            <path
                                fill-rule="evenodd"
                                d="M10 9.293l4.646-4.647a.5.5 0 01.708.708L10.707 10l4.647 4.646a.5.5 0 01-.708.708L10 10.707l-4.646 4.647a.5.5 0 01-.708-.708L9.293 10 4.646 5.354a.5.5 0 01.708-.708L10 9.293z"
                                clip-rule="evenodd"
                            />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <!-- Filter activation button (to the right of the search bar) -->
        <div class="flex h-12 2xl:h-14 mr-1">
            <button @click="toggleFilterSection" class="m-2 px-2 rounded-md hover:bg-gray-100 focus:outline-none">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-6 w-6 text-gray-500"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
                    />
                </svg>
            </button>
        </div>
        <div v-show="showFilters">
            <Filters />
        </div>
    </div>
</template>

<script setup lang="ts">
import { Ref, ref, inject, onMounted, watch } from "vue";
import Filters from "./Filters.vue";
import { MagnifyingGlassIcon } from "@heroicons/vue/20/solid";

const showFilters = ref(false);
const openFilters = ref<Record<string, boolean>>({});
const searchTimeout = ref<number | null>(null);

const selectedCategory = inject("selectedCategory") as Ref<string>;
const toSearch = inject("toSearch") as Ref<boolean>;
const searchQuery = inject("searchQuery") as Ref<string>;
const searchQueryLast = ref(searchQuery.value);
const fetchEmailsData = inject("fetchEmailsData") as (categoryName: string) => Promise<void>;

const toggleFilterSection = () => {
    showFilters.value = !showFilters.value;

    //openFilters.value[selectedCategory.value] = showFilters.value;

    localStorage.setItem("showFilters", JSON.stringify(openFilters.value));
    localStorage.setItem("showFiltersTab", JSON.stringify(showFilters.value));
};

const clearSearch = () => {
    searchQuery.value = "";
    if (searchTimeout.value) {
        clearTimeout(searchTimeout.value);
    }
};

function debounce(func: any, delay: number) {
    let timeoutId: ReturnType<typeof setTimeout>;
    return function (this: any, ...args: any[]) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

const performSearch = async () => {
    if (searchQuery.value.trim() !== "") {
        toSearch.value = true;
    } else {
        toSearch.value = false;
    }
    await fetchEmailsData(selectedCategory.value);
};

const debouncedSearch = debounce(performSearch, 500);

watch(searchQuery, () => {
    if (searchQuery.value.trim() !== "") {
        debouncedSearch();
    } else if (searchQueryLast.value !== searchQuery.value) {
        debouncedSearch();
    } else {
        if (searchTimeout.value) {
            clearTimeout(searchTimeout.value);
        }
    }
});

onMounted(() => {
    const storedFilters = localStorage.getItem("showFilters");
    if (storedFilters) {
        try {
            openFilters.value = JSON.parse(storedFilters) as Record<string, boolean>;
        } catch (e) {
            console.error("Error parsing stored filters:", e);
        }
    }

    const storedShowFilters = localStorage.getItem("showFiltersTab");
    if (storedShowFilters) {
        showFilters.value = true;
    }
});
</script>
