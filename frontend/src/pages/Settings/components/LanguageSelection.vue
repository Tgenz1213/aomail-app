<template>
    <div class="relative">
        <Listbox v-model="selectedLanguage">
            <ListboxButton
                class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6"
            >
                <span class="block truncate">
                    <flag :iso="selectedLanguage.iso" />
                    {{ $t(selectedLanguage.value) }}
                </span>
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
                                <flag :iso="language.iso" />
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
import { inject, ref, watch } from "vue";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue";
import ChevronUpDownIcon from "@heroicons/vue/24/outline/ChevronUpDownIcon";
import CheckIcon from "@heroicons/vue/24/outline/CheckIcon";
import { KeyValuePair } from "@/global/types";
import { i18n } from "@/global/preferences";
import { postData } from "@/global/fetchData";
import { AllowedLanguageType } from "@/global/const";

interface Language extends KeyValuePair {
    iso: string;
}

const languages: Language[] = [
    { key: "french", value: i18n.global.t("constants.languagesList.french"), iso: "fr" },
    { key: "american", value: i18n.global.t("constants.languagesList.american"), iso: "us" },
    { key: "german", value: i18n.global.t("constants.languagesList.german"), iso: "de" },
    { key: "russian", value: i18n.global.t("constants.languagesList.russian"), iso: "ru" },
    { key: "spanish", value: i18n.global.t("constants.languagesList.spanish"), iso: "es" },
    { key: "chinese", value: i18n.global.t("constants.languagesList.chinese"), iso: "cn" },
    { key: "indian", value: i18n.global.t("constants.languagesList.indian"), iso: "in" },
];
const storedLanguageKey = localStorage.getItem("language");
const initialLanguage = languages.find((lang) => lang.key === storedLanguageKey) || languages[1];
const selectedLanguage = ref<Language>(initialLanguage);

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const updateLanguageSelection = async (newLanguage: Language) => {
    selectedLanguage.value = newLanguage;
    const newLanguageKey = newLanguage.key as AllowedLanguageType;
    const currentLanguage = localStorage.getItem("language");

    if (newLanguageKey === currentLanguage) return;

    localStorage.setItem("language", newLanguageKey);
    i18n.global.locale = newLanguageKey;

    const result = await postData(`user/preferences/set_language/`, { language: newLanguageKey });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.errorGettingLanguage"),
            result.error as string
        );
    }

    displayPopup?.(
        "success",
        i18n.global.t("constants.popUpConstants.successMessages.success"),
        i18n.global.t("settingsPage.preferencesPage.popUpConstants.successMessages.languageUpdatedSuccessfully")
    );
};

watch(selectedLanguage, updateLanguageSelection);
</script>
