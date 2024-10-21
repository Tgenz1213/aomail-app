<template>
    <div class="">
        <div
            class="sticky top-0 z-40 flex h-20 shrink-0 items-center gap-x-4 border-b border-black shadow-sm border-opacity-10 bg-white px-4 sm:gap-x-6 sm:px-6 lg:px-8"
        >
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
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { MagnifyingGlassIcon } from "@heroicons/vue/20/solid";

const searchQuery = ref("");

const clearSearch = () => {
    searchQuery.value = "";
};
</script>
