<template>
    <div
        class="sticky top-0 z-40 flex h-20 shrink-0 items-center gap-x-4 border-b border-black shadow-sm border-opacity-10 bg-white sm:pl-6 lg:pl-8"
    >
        <div class="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
            <div class="relative flex flex-1">
                <label for="search-field" class="sr-only">
                    {{ $t("constants.userActions.searchbar_search") }}
                </label>
                <MagnifyingGlassIcon
                    class="pointer-events-none absolute inset-y-0 left-0 h-full w-5 text-gray-400"
                    aria-hidden="true"
                />
                <input
                    v-model="searchInput"
                    id="search-field"
                    class="h-full w-full border-0 py-0 pl-8 pr-8 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm"
                    :placeholder="$t('rulesPage.search')"
                    type="search"
                    name="search"
                />
                <div class="relative flex items-center">
                    <!-- Toggle Filters Button -->
                    <button
                        type="button"
                        class="group w-full h-full bg-gray-100 text-white hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 flex items-center justify-center px-4 2xl:px-5 2xl:py-3 border-l border-gray-200"
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
                    <!-- Search Button -->
                    <button
                        type="button"
                        @click="fetchRules"
                        class="w-full h-full bg-gray-700 px-8 2xl:px-10 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center justify-between 2xl:text-lg"
                    >
                        {{ $t("constants.userActions.search") }}
                        <magnifying-glass-icon class="w-4 2xl:w-5" />
                    </button>
                </div>
            </div>
        </div>
    </div>
    <Filters :isOpen="arefiltersOpen" @update:filters="updateFilters" @fetchRules="fetchRules" />
</template>

<script setup lang="ts">
import { inject, Ref, ref } from "vue";
import { MagnifyingGlassIcon } from "@heroicons/vue/20/solid";
import Filters from "./Filters.vue";

const arefiltersOpen = ref(false);
const searchInput = inject<Ref<string>>("searchInput") || ref("");
const advancedFilters = ref<Record<string, any>>({});

const emit = defineEmits<{
    (
        e: "fetchRules",
        params: {
            search: string;
            advanced: boolean;
            logicalOperator?: string;
            domains?: string[];
            senderEmails?: string[];
            hasAttachments?: boolean;
            categories?: string[];
            priorities?: string[];
            answers?: string[];
            relevance?: string[];
            flags?: string[];
            emailDealWith?: string;
        }
    ): void;
}>();

const fetchRules = () => {
    hideFilters();
    if (Object.keys(advancedFilters.value).length > 0) {
        // Send advanced search
        emit("fetchRules", {
            search: searchInput.value,
            advanced: true,
            ...advancedFilters.value,
        });
    } else {
        // Send basic search
        emit("fetchRules", {
            search: searchInput.value,
            advanced: false,
        });
    }
};

function updateFilters(filters: Record<string, any>) {
    advancedFilters.value = filters;
}

function toggleFilters() {
    arefiltersOpen.value = !arefiltersOpen.value;
}

function hideFilters() {
    arefiltersOpen.value = false;
}
</script>
