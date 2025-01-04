<template>
    <div class="flex">
        <div class="relative flex flex-1 space-x-4">
            <div class="flex w-full h-full space-x-4">
                <div class="flex w-full h-full">
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
                        class="block rounded-l-md shadow-sm ring-1 ring-gray-300 focus:ring-2 focus:ring-gray-500 h-full w-full border-0 py-0 pl-8 pr-8 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm"
                        @focus="handleFocusSearch"
                        @blur="handleBlur"
                    />
                    <div class="relative flex items-center">
                        <button
                            type="button"
                            class="group w-full h-full bg-gray-100 rounded-r-md p-2 text-gray-600 shadow-sm hover:bg-gray-600 focus:outline-none flex items-center justify-center ring-1 ring-gray-300"
                            @click="toggleFilters"
                        >
                            <svg
                                class="w-6 h-5 text-gray-400 group-hover:text-white"
                                aria-hidden="true"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    d="M10.83 5a3.001 3.001 0 0 0-5.66 0H4a1 1 0 1 0 0 2h1.17a3.001 3.001 0 0 0 5.66 0H20a1 1 0 1 0 0-2h-9.17ZM4 11h9.17a3.001 3.001 0 0 1 5.66 0H20a1 1 0 1 1 0 2h-1.17a3.001 3.001 0 0 1-5.66 0H4a1 1 0 1 1 0-2Zm1.17 6H4 a1 1 0 1 0 0 2h1.17a3.001 3.001 0 0 0 5.66 0H20a1 1 0 1 0 0-2h-9.17a3.001 3.001 0 0 0-5.66 0Z"
                                />
                            </svg>
                        </button>
                    </div>
                </div>
                <button
                    type="button"
                    @click="searchLabels"
                    class="p-4 bg-gray-700 rounded-md text-md font-semibold text-white hover:bg-gray-900 focus:outline-none flex gap-x-2 items-center justify-between 2xl:px-7 2xl:text-lg"
                >
                    {{ $t("constants.userActions.search") }}
                    <magnifying-glass-icon class="w-4 2xl:w-5" />
                </button>
            </div>
            <div class="w-full h-full flex space-x-4 items-center">
                <label class="font-medium text-gray-700">Sort by:</label>
                <select v-model="sort" class="border border-gray-300 rounded-md p-2 flex-grow">
                    <option value="platform">Platform</option>
                    <option value="itemName">Item Name</option>
                    <option value="carrier">Carrier</option>
                    <option value="postageDeadline">Postage Deadline</option>
                </select>

                <label class="font-medium text-gray-700">Order by:</label>
                <select v-model="order" class="border border-gray-300 rounded-md p-2 flex-grow">
                    <option value="asc">Ascending</option>
                    <option value="desc">Descending</option>
                </select>
            </div>
        </div>
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
