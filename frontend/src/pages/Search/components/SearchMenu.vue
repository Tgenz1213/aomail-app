<template>
    <div class="flex space-x-1 2xl:space-x-2 w-full px-6 pt-2">
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
                class="w-full h-full bg-gray-700 px-3 2xl:px-5 rounded-md text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center justify-between 2xl:text-lg"
            >
                {{ $t("searchPage.searchButton") }}
                <magnifying-glass-icon class="w-4 2xl:w-5" />
            </button>
        </div>
        <div>
            <Listbox v-model="selectedSearchMode">
                <div class="relative h-full">
                    <ListboxButton
                        class="relative w-full h-full cursor-default rounded-md bg-white px-2 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6 flex items-center"
                    >
                        <span class="block truncate flex-grow">{{ selectedSearchMode.value }}</span>
                        <span class="pl-1 pointer-events-none flex items-center">
                            <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                        </span>
                    </ListboxButton>
                    <transition
                        leave-active-class="transition ease-in duration-100"
                        leave-from-class="opacity-100"
                        leave-to-class="opacity-0"
                    >
                        <ListboxOptions
                            class="absolute z-10 mt-1 max-h-60 w-[120%] overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
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
                                        'relative cursor-default select-none py-2 pl-3',
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
    <AomailFilters :isOpen="isAomailFiltersOpen" />
    <ApiFilters :isOpen="isApiFiltersOpen" />
</template>

<script setup lang="ts">
import { postData } from "@/global/fetchData";
import { AomailSearchFilter, ApiSearchFilter, Email, EmailDetails, EmailProvider, KeyValuePair } from "@/global/types";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue";
import { MagnifyingGlassIcon, ChevronUpDownIcon } from "@heroicons/vue/24/outline";
import { inject, onMounted, onUnmounted, ref, Ref, watch } from "vue";
import AomailFilters from "./AomailFilters.vue";
import ApiFilters from "./ApiFilters.vue";
import { EmailApiIds, EmailApiListType } from "../utils/types";
import { i18n } from "@/global/preferences";
import { AOMAIL_SEARCH_KEY, API_SEARCH_KEY } from "@/global/const";

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const loading = inject<() => void>("loading");
const scrollToBottom = inject<() => void>("scrollToBottom");
const hideLoading = inject<() => void>("hideLoading");

const emailIds = inject<Ref<number[]>>("emailIds") || ref([]);
const emailApiIds = inject<Ref<EmailApiIds>>("emailApiIds") || ref<EmailApiIds>({});
const emailList = inject<Ref<Email[]>>("emailList") || ref([]);
const emailApiList = inject<Ref<EmailApiListType>>("emailApiList") || ref<EmailApiListType>({});
const selectedSearchMode =
    inject<Ref<KeyValuePair>>("selectedSearchMode") ||
    ref<KeyValuePair>({
        key: AOMAIL_SEARCH_KEY,
        value: i18n.global.t("searchPage.searchModes.aomail"),
    });
const searchModes =
    inject<Ref<KeyValuePair[]>>("searchModes") ||
    ref<KeyValuePair[]>([
        { key: AOMAIL_SEARCH_KEY, value: i18n.global.t("searchPage.searchModes.aomail") },
        { key: API_SEARCH_KEY, value: i18n.global.t("searchPage.searchModes.allEmails") },
    ]);

const inputValue = ref("");
const isFocused = ref(false);
const isAomailFiltersOpen = ref(false);
const isApiFiltersOpen = ref(false);
const aomailSearchFilters = ref<AomailSearchFilter>({});
const apiSearchFilters = ref<ApiSearchFilter>({});
const closeFilters = () => {
    isApiFiltersOpen.value = false;
    isAomailFiltersOpen.value = false;
};

function toggleFilters() {
    if (selectedSearchMode.value.key === AOMAIL_SEARCH_KEY) {
        isAomailFiltersOpen.value = !isAomailFiltersOpen.value;
    } else {
        isApiFiltersOpen.value = !isApiFiltersOpen.value;
    }
}

function handleFocusSearch() {
    isFocused.value = true;
}

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Enter" && isFocused.value) {
        event.preventDefault();
        searchEmails();
    }
};

watch(selectedSearchMode, () => {
    closeFilters();
});

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

onUnmounted(() => {
    document.removeEventListener("keydown", handleKeyDown);
});

function searchEmails() {
    if (selectedSearchMode.value.key === AOMAIL_SEARCH_KEY) {
        searchAomailEmails();
    } else {
        searchApiEmails();
    }
}

function mergeEmailData(
    target: Record<string, Record<string, Record<string, any>>>,
    source: Record<string, Record<string, Record<string, any>>>
) {
    for (const provider in source) {
        if (!target[provider]) {
            target[provider] = {}; // Create provider if missing
        }

        for (const email in source[provider]) {
            if (!target[provider][email]) {
                target[provider][email] = {}; // Create email entry if missing
            }

            for (const providerId in source[provider][email]) {
                if (!target[provider][email][providerId]) {
                    // Directly add if the providerId is new
                    target[provider][email][providerId] = source[provider][email][providerId];
                }
            }
        }
    }
}

async function searchApiEmails() {
    loading?.();
    scrollToBottom?.();
    closeFilters?.();
    emailList.value = [];
    emailApiList.value = {};

    let result;
    if (
        apiSearchFilters.value.emailProvider ||
        apiSearchFilters.value.subject ||
        apiSearchFilters.value.body ||
        apiSearchFilters.value.dateFrom ||
        apiSearchFilters.value.fileExtensions ||
        apiSearchFilters.value.filenames ||
        apiSearchFilters.value.fromAddresses ||
        apiSearchFilters.value.fromAddresses ||
        apiSearchFilters.value.searchIn ||
        apiSearchFilters.value.toAddresses
    ) {
        apiSearchFilters.value.advanced = true;
        result = await postData(`user/get_api_emails_ids/`, apiSearchFilters.value);
    } else {
        result = await postData(`user/get_api_emails_ids/`, inputValue.value ? { query: inputValue.value } : {});
    }

    if (!result.success) {
        displayPopup?.("error", i18n.global.t("searchPage.errors.failedToFetchEmails"), result.error as string);
        hideLoading?.();
        return;
    }

    emailApiIds.value = result.data;
    let nbLimitedApiIds = 0;
    let limitedApiIds: EmailApiIds = {};

    Object.entries(emailApiIds.value).forEach(([provider, dictEmails]) => {
        const typedProvider = provider as EmailProvider;
        Object.entries(dictEmails).forEach(([email, listIds]) => {
            if (nbLimitedApiIds < 50) {
                if (!limitedApiIds[typedProvider]) {
                    limitedApiIds[typedProvider] = {};
                }
                limitedApiIds[typedProvider][email] = listIds.slice(0, 50 - nbLimitedApiIds);
                nbLimitedApiIds += limitedApiIds[typedProvider][email].length;
            }
        });
    });

    const getIdsSlice = (start: number, count: number): EmailApiIds | null => {
        const slice: EmailApiIds = {};
        let found = 0;

        for (const [provider, emails] of Object.entries(limitedApiIds)) {
            slice[provider as EmailProvider] = {};

            for (const [email, ids] of Object.entries(emails)) {
                const currentSlice = ids.slice(start, start + count);
                if (currentSlice.length > 0) {
                    slice[provider as EmailProvider]![email] = currentSlice;
                    found += currentSlice.length;
                }
            }

            if (Object.keys(slice[provider as EmailProvider]!).length === 0) {
                delete slice[provider as EmailProvider];
            }
        }

        return found > 0 ? slice : null;
    };

    const firstSlice = getIdsSlice(0, 2);
    if (firstSlice) {
        const firstBatchResult = await postData(`user/get_api_emails_data/`, {
            limitedApiIds: firstSlice,
        });

        if (firstBatchResult.success) {
            emailApiList.value = firstBatchResult.data.data;
        }
    }
    hideLoading?.();

    let currentIndex = 2;
    let keepFetching = true;
    while (keepFetching) {
        const nextSlice = getIdsSlice(currentIndex, 2);
        if (!nextSlice) {
            keepFetching = false;
            break;
        }

        const batchResult = await postData(`user/get_api_emails_data/`, {
            limitedApiIds: nextSlice,
        });

        if (batchResult.success) {
            mergeEmailData(emailApiList.value, batchResult.data.data);
            console.log(emailApiList.value);
        }

        currentIndex += 2;
        await new Promise((resolve) => setTimeout(resolve, 100));
    }
}

async function searchAomailEmails() {
    loading?.();
    scrollToBottom?.();
    closeFilters?.();

    let result;
    if (
        aomailSearchFilters.value.emailProvider ||
        aomailSearchFilters.value.subject ||
        aomailSearchFilters.value.senderEmail ||
        aomailSearchFilters.value.senderName ||
        aomailSearchFilters.value.CCEmails ||
        aomailSearchFilters.value.CCNames ||
        aomailSearchFilters.value.category ||
        aomailSearchFilters.value.emailAddresses ||
        aomailSearchFilters.value.archive ||
        aomailSearchFilters.value.replyLater ||
        aomailSearchFilters.value.read ||
        aomailSearchFilters.value.sentDate ||
        aomailSearchFilters.value.readDate ||
        aomailSearchFilters.value.answer ||
        aomailSearchFilters.value.relevance ||
        aomailSearchFilters.value.priority ||
        aomailSearchFilters.value.hasAttachments ||
        aomailSearchFilters.value.spam ||
        aomailSearchFilters.value.scam ||
        aomailSearchFilters.value.newsletter ||
        aomailSearchFilters.value.notification ||
        aomailSearchFilters.value.meeting
    ) {
        aomailSearchFilters.value.advanced = true;
        result = await postData(`user/emails_ids/`, aomailSearchFilters.value);
    } else {
        result = await postData(`user/emails_ids/`, inputValue.value ? { search: inputValue.value } : {});
    }

    if (!result.success) {
        displayPopup?.("error", i18n.global.t("searchPage.errors.failedToFetchEmails"), result.error as string);
        hideLoading?.();
        return;
    }

    emailIds.value = result.data.ids;
    const limitedEmails: number[] = result.data.ids.slice(0, 25);
    const resultEmailsData = await postData(`user/get_emails_data/`, {
        ids: limitedEmails,
    });

    hideLoading?.();
    if (!resultEmailsData.success) {
        displayPopup?.(
            "error",
            i18n.global.t("searchPage.errors.failedToFetchEmailDetails"),
            resultEmailsData.error as string
        );
        return;
    }

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
