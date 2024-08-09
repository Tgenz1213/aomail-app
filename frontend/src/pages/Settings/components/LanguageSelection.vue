<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />
    <div class="relative">
        <Listbox v-model="selectedLanguage">
            <ListboxButton
                class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6"
            >
                <span class="block truncate">{{ $t(selectedLanguage.value) }}</span>
                <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
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
                        as="template"
                        v-for="language in languages"
                        :key="language.key"
                        :value="language"
                        v-slot="{ active, selected }"
                    >
                        <li
                            :class="[
                                active ? 'bg-gray-800 text-white' : 'text-gray-900',
                                'relative cursor-default select-none py-2 pl-3 pr-9',
                            ]"
                        >
                            <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                                {{ $t(language.value) }}
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
        </Listbox>
    </div>
</template>

<script lang="ts" setup>
import { ref, watch } from "vue";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue";
import NotificationTimer from "@/components/NotificationTimer.vue";
import { fetchWithToken } from "@/global/security";
import { API_BASE_URL } from "@/global/const";
import ChevronUpDownIcon from "@heroicons/vue/24/outline/ChevronUpDownIcon";
import CheckIcon from "@heroicons/vue/24/outline/CheckIcon";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { KeyValuePair } from "@/global/types";
import { i18n } from "@/global/Settings/preferences";

const languages: KeyValuePair[] = [
    { key: "french", value: i18n.global.t("constants.languagesList.french") },
    { key: "american", value: i18n.global.t("constants.languagesList.american") },
    { key: "german", value: i18n.global.t("constants.languagesList.german") },
    { key: "russian", value: i18n.global.t("constants.languagesList.russian") },
    { key: "spanish", value: i18n.global.t("constants.languagesList.spanish") },
    { key: "chinese", value: i18n.global.t("constants.languagesList.chinese") },
    { key: "indian", value: i18n.global.t("constants.languagesList.indian") },
];

const storedLanguageKey = localStorage.getItem("language");
const initialLanguage = languages.find((lang) => lang.key === storedLanguageKey) || languages[1];
const selectedLanguage = ref<KeyValuePair>(initialLanguage);

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

const dismissPopup = () => {
    showNotification.value = false;
    if (timerId.value !== null) {
        clearTimeout(timerId.value);
    }
};

const displayPopup = (type: "success" | "error", title: string, message: string) => {
    if (type === "error") {
        displayErrorPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    } else {
        displaySuccessPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    }
    timerId.value = window.setTimeout(dismissPopup, 4000);
};

const updateLanguageSelection = async (newLanguage: KeyValuePair) => {
    selectedLanguage.value = newLanguage;
    const newLanguageKey = newLanguage.key;
    const currentLanguage = localStorage.getItem("language");

    if (newLanguageKey === currentLanguage) return;

    localStorage.setItem("language", newLanguageKey);

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/preferences/set_language/`, {
            headers: { "Content-Type": "application/json" },
            method: "POST",
            body: JSON.stringify({ language: newLanguageKey }),
        });

        if (response && response instanceof Response) {
            const data = await response.json();
            if (data.error) {
                displayPopup(
                    "error",
                    i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.errorGettingLanguage"),
                    data.error
                );
            } else if (data.message === "Language updated successfully") {
                (i18n.global.locale as string) = newLanguageKey;

                displayPopup(
                    "success",
                    i18n.global.t("constants.popUpConstants.successMessages.success"),
                    i18n.global.t(
                        "settingsPage.preferencesPage.popUpConstants.successMessages.languageUpdatedSuccessfully"
                    )
                );
            }
        }
    } catch (error) {
        if (error instanceof Error) {
            displayPopup(
                "error",
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.errorGettingLanguage"),
                error.message
            );
        }
    }
};

watch(selectedLanguage, updateLanguageSelection);
</script>


<!-- // todo: replace all "GET" and "POST" backend call with getData & postData from @/global/fetchData file -->