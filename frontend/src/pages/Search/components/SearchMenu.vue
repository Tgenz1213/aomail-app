<template>
    <div class="flex space-x-1 2xl:space-x-2 items-stretch w-full mb-4">
        <div class="relative w-full">
            <div class="flex w-full">
                <div class="relative flex-grow">
                    <div
                        v-if="!isFocused && !inputValue"
                        class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 2xl:ml-3"
                    >
                        <magnifying-glass-icon class="w-4 h-4 pointer-events-none 2xl:w-5 2xl:h-5" />
                        <label
                            for="search"
                            class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none 2xl:text-base"
                        >
                            {{ $t("searchPage.searchPlaceholder") }}
                        </label>
                    </div>
                    <input
                        v-model="inputValue"
                        type="text"
                        class="block rounded-l-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 h-10 2xl:h-11 flex-1 border-0 bg-transparent py-2 pl-3 text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 w-full z-20 relative 2xl:py-3 2xl:pl-4 2xl:text-base"
                        @focus="handleFocusSearch"
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
                @click="searchEmails"
                class="w-full h-full bg-gray-700 rounded-md px-2 2xl:px-4 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center justify-between 2xl:px-7 2xl:text-lg"
            >
                {{ $t("searchPage.searchButton") }}
                <magnifying-glass-icon class="w-4 2xl:w-5" />
            </button>
        </div>
        <div class="flex-grow h-full">
            <Listbox v-model="selectedSearchMode">
                <div class="relative h-full">
                    <ListboxButton
                        class="relative w-full h-full cursor-default rounded-md bg-white px-3 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6 flex items-center"
                    >
                        <span class="block truncate flex-grow">{{ selectedSearchMode.value }}</span>
                        <span class="pointer-events-none flex items-center">
                            <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                        </span>
                    </ListboxButton>
                    <transition
                        leave-active-class="transition ease-in duration-100"
                        leave-from-class="opacity-100"
                        leave-to-class="opacity-0"
                    >
                        <ListboxOptions
                            class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                        >
                            <ListboxOption
                                v-for="searchMode in searchModes"
                                :key="searchMode.key"
                                :value="searchMode"
                                v-slot="{ active, selected }"
                            >
                                <li
                                    :class="[
                                        active ? 'bg-gray-800 text-white' : 'text-gray-900',
                                        'relative cursor-default select-none py-2 pl-3 pr-9',
                                    ]"
                                >
                                    <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                                        {{ searchMode.value }}
                                    </span>
                                    <span
                                        v-if="selected"
                                        :class="[
                                            active ? 'text-white' : 'text-gray-500',
                                            'absolute inset-y-0 right-0 flex items-center pr-4',
                                        ]"
                                    >
                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                    </span>
                                </li>
                            </ListboxOption>
                        </ListboxOptions>
                    </transition>
                </div>
            </Listbox>
        </div>
    </div>
</template>

<script setup lang="ts">
import { postData } from "@/global/fetchData";
import { Email, EmailDetails, KeyValuePair } from "@/global/types";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue";
import { MagnifyingGlassIcon } from "@heroicons/vue/24/outline";
import { inject, ref, Ref } from "vue";

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const loading = inject<() => void>("loading");
const scrollToBottom = inject<() => void>("scrollToBottom");
const hideLoading = inject<() => void>("hideLoading");

const emailIds = inject<Ref<number[]>>("emailIds") || ref([]);
const emailList = inject<Ref<Email[]>>("emailList") || ref([]);
const inputValue = ref("");
const isFocused = ref(false);

const searchModes: KeyValuePair[] = [
    { key: "aomail", value: "Aomail" },
    { key: "api", value: "API" },
];
const selectedSearchMode = ref<KeyValuePair>(searchModes[0]);

async function toggleFilters() {
    if (selectedSearchMode.value.key === "aomail") {
        // todo: show aomail filters
    } else {
        // todo: show api filters
    }
}

function handleFocusSearch() {
    isFocused.value = true;
}

async function searchEmails() {
    loading?.();
    scrollToBottom?.();

    const result = await postData(`user/emails_ids/`, {
        subject: inputValue.value,
    });

    if (!result.success) {
        displayPopup?.("error", "Failed to fetch emails", result.error as string);
        hideLoading?.();
        return;
    }

    emailIds.value = result.data.ids;
    const limitedEmails: number[] = result.data.ids.slice(0, 25);
    const resultEmailsData = await postData(`user/get_emails_data/`, {
        ids: limitedEmails,
    });

    if (!resultEmailsData.success) {
        displayPopup?.("error", "Failed to fetch email details", resultEmailsData.error as string);
        hideLoading?.();
        return;
    }
    hideLoading?.();

    const emailDetails: EmailDetails = resultEmailsData.data;

    emailList.value = [];
    for (const [category, priorities] of Object.entries(emailDetails.data)) {
        for (const [priority, emails] of Object.entries(priorities)) {
            if (Array.isArray(emails)) {
                for (const email of emails) {
                    emailList.value.push({
                        ...email,
                        category,
                        priority,
                    });
                }
            }
        }
    }
}
</script>
