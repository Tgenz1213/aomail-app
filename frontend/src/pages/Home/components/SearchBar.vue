<template>
    <div class="relative" height="3rem">
        <div
            class="sticky top-0 z-40 flex shrink-0 items-center gap-x-4 border-b border-black shadow-sm border-opacity-10 bg-white px-4 sm:gap-x-6 sm:px-6 lg:px-8"
            :style="{ height: height }"
        >
            <div class="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
                <form class="relative flex flex-1 items-center" action="#" method="GET">
                    <label for="search-field" class="sr-only">{{ $t("constants.userActions.searchbar_search") }}</label>
                    <MagnifyingGlassIcon
                        class="pointer-events-none absolute left-0 h-5 w-5 text-gray-400"
                        aria-hidden="true"
                    />
                    <input
                        v-model="searchQuery"
                        id="search-field"
                        class="h-full w-full border-0 py-0 pl-8 pr-20 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm"
                        :placeholder="$t('rulesPage.search')"
                        name="search"
                    />
                    <div class="absolute right-0 flex items-center">
                        <button
                            v-if="showFilterButton"
                            @click="toggleFilterPopup"
                            type="button"
                            class="flex items-center pr-2 sm:pr-4"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                class="h-5 w-5 text-gray-400"
                                viewBox="0 0 20 20"
                                fill="currentColor"
                            >
                                <path
                                    fill-rule="evenodd"
                                    d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z"
                                    clip-rule="evenodd"
                                />
                            </svg>
                        </button>
                        <button
                            v-if="searchQuery"
                            type="button"
                            @click="clearSearch"
                            class="flex items-center pr-2 sm:pr-4"
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
                </form>
            </div>
        </div>
        <div
            v-if="showFilterPopup"
            class="absolute left-0 right-0 mt-1 bg-white border border-gray-300 shadow-lg rounded-md z-50"
            style="width: 90%"
        >
            <div class="p-4">
                <div class="grid grid-cols-3 gap-4 text-sm">
                    <div v-for="(field, index) in filters" :key="index" class="flex flex-col">
                        <label :for="field.name" class="mb-1 text-sm font-medium text-gray-700">
                            {{ field.label }}
                        </label>
                        <input
                            v-if="field.type === 'text'"
                            :type="field.type"
                            :placeholder="field.placeholder"
                            :id="field.name"
                            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                        />
                        <div v-if="field.type === 'checkbox'" class="flex items-center">
                            <input
                                :type="field.type"
                                :id="field.name"
                                class="form-checkbox h-4 w-4 text-indigo-600 mr-2"
                            />
                            <span class="text-sm text-gray-700">{{ field.label }}</span>
                        </div>
                        <select
                            v-if="field.type === 'select'"
                            :id="field.name"
                            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                        >
                            <option v-for="option in field.options" :key="option.value" :value="option.value">
                                {{ option.label }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="mt-4 flex justify-end space-x-3 text-sm">
                    <button
                        @click="toggleFilterPopup"
                        class="px-3 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                    >
                        Annuler
                    </button>
                    <button
                        @click="applyFilters"
                        class="px-3 py-2 bg-gray-800 text-white rounded-md hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                        Rechercher
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
// todo: instead of a form use strictly v-model and use a function to make the API call with postData

import { ref, watch } from "vue";
import { MagnifyingGlassIcon } from "@heroicons/vue/20/solid";

const props = defineProps({
    height: {
        type: String,
        default: "5rem",
    },
    showFilterButton: {
        type: Boolean,
        default: false,
    },
});

const filters = [
    { key: "from", label: "De", type: "text", placeholder: "De" },
    { key: "to", label: "À", type: "text", placeholder: "À" },
    { key: "subject", label: "Objet", type: "text", placeholder: "Objet" },
    {
        key: "contains",
        label: "Contient les mots",
        type: "text",
        placeholder: "Contient les mots",
    },
    {
        key: "doesNotContain",
        label: "Ne contient pas",
        type: "text",
        placeholder: "Ne contient pas",
    },
    {
        key: "size",
        label: "Taille",
        type: "select",
        options: [
            { value: "greater", label: "supérieure à" },
            { value: "less", label: "inférieure à" },
        ],
    },
    {
        key: "dateRange",
        label: "Plage de dates",
        type: "select",
        options: [
            { value: "1day", label: "1 jour" },
            { value: "1week", label: "1 semaine" },
            { value: "1month", label: "1 mois" },
            { value: "1year", label: "1 an" },
        ],
    },
    {
        key: "searchIn",
        label: "Rechercher",
        type: "select",
        options: [
            { value: "all", label: "Tous les messages" },
            { value: "read", label: "Messages lus" },
            { value: "unread", label: "Messages non lus" },
        ],
    },
    { key: "hasAttachment", label: "Contenant une pièce jointe", type: "checkbox" },
    { key: "excludeChats", label: "Ne pas inclure les chats", type: "checkbox" },
];
const searchQuery = ref("");
const showFilterPopup = ref(false);
const emits = defineEmits(["updateSearchQuery"]);

const clearSearch = () => {
    searchQuery.value = "";
};

const toggleFilterPopup = () => {
    showFilterPopup.value = !showFilterPopup.value;
};

const applyFilters = () => {
    showFilterPopup.value = false;
};

watch(searchQuery, (newValue) => {
    emits("updateSearchQuery", newValue);
});
</script>
