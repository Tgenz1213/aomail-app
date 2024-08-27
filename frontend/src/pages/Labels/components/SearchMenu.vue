<template>
    <div class="flex space-x-1 2xl:space-x-2 items-stretch w-full mb-4">
        <div class="relative w-full">
            <div class="flex w-full">
                <div class="relative flex-grow">
                    <div
                        v-if="!isFocus && !searchQuery"
                        class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 2xl:ml-3"
                    >
                        <magnifying-glass-icon class="w-4 h-4 pointer-events-none 2xl:w-5 2xl:h-5" />
                        <label
                            for="search"
                            class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none 2xl:text-base"
                        >
                            Labels search
                        </label>
                    </div>
                    <input
                        v-model="searchQuery"
                        type="text"
                        class="block rounded-l-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 h-10 2xl:h-11 flex-1 border-0 bg-transparent py-2 pl-3 text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 w-full z-20 relative 2xl:py-3 2xl:pl-4 2xl:text-base"
                        @focus="handleFocusSearch"
                        @blur="handleBlur"
                    />
                </div>
                <div class="relative">
                    <button
                        type="button"
                        class="group w-full h-full bg-gray-100 rounded-r-md p-2 text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 flex items-center justify-center 2xl:px-3 2xl:py-3 ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm"
                        @click="toggleFilters"
                    >
                        <svg
                            class="w-6 h-5 text-gray-400 group-hover:text-white"
                            aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="currentColor"
                            stroke="none"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M10.83 5a3.001 3.001 0 0 0-5.66 0H4a1 1 0 1 0 0 2h1.17a3.001 3.001 0 0 0 5.66 0H20a1 1 0 1 0 0-2h-9.17ZM4 11h9.17a3.001 3.001 0 0 1 5.66 0H20a1 1 0 1 1 0 2h-1.17a3.001 3.001 0 0 1-5.66 0H4a1 1 0 1 1 0-2Zm1.17 6H4 a1 1 0 1 0 0 2h1.17a3.001 3.001 0 0 0 5.66 0H20a1 1 0 1 0 0-2h-9.17a3.001 3.001 0 0 0-5.66 0Z"
                            />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <div>
            <button
                type="button"
                @click="searchLabels"
                class="w-full h-full bg-gray-700 rounded-md px-2 2xl:px-4 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center justify-between 2xl:px-7 2xl:text-lg"
            >
                {{ $t("constants.userActions.search") }}
                <magnifying-glass-icon class="w-4 2xl:w-5" />
            </button>
        </div>
        <select v-model="sort" class="ml-2 p-2 border border-gray-300 rounded-md">
            <option value="platform">Platform</option>
            <option value="itemName">Item Name</option>
            <option value="carrier">Carrier</option>
            <option value="postageDeadline">Postage Deadline</option>
        </select>

        <select v-model="order" class="ml-2 p-2 border border-gray-300 rounded-md">
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
        </select>
    </div>
    <Filters :isOpen="arefiltersOpen" />
</template>

<script setup lang="ts">
import { inject, Ref, ref } from "vue";
import { MagnifyingGlassIcon } from "@heroicons/vue/24/outline";
import Filters from "./Filters.vue";

const arefiltersOpen = ref(false);
const isFocus = ref(false);
const searchQuery = inject<Ref<string>>("searchQuery") || ref("");
const sort = inject<Ref<string>>("sort") || ref("sort");
const order = inject<Ref<number[]>>("order") || ref("order");

const searchLabels = inject<() => void>("searchLabels");

const handleFocusSearch = () => {
    isFocus.value = true;
};

const handleBlur = () => {
    isFocus.value = false;
};

const toggleFilters = () => {
    arefiltersOpen.value = !arefiltersOpen.value;
};
</script>
