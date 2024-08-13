<template>
    <div class="relative">
        <Listbox as="div" v-model="selectedTheme">
            <ListboxButton
                class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6"
            >
                <span class="block truncate">{{ $t(selectedTheme.value) }}</span>
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
                        v-for="theme in themes"
                        :key="theme.key"
                        :value="theme"
                        v-slot="{ active, selected }"
                    >
                        <li
                            :class="[
                                active ? 'bg-gray-800 text-white' : 'text-gray-900',
                                'relative cursor-default select-none py-2 pl-3 pr-9',
                            ]"
                        >
                            <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                                {{ $t(theme.value) }}
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

<script setup lang="ts">
import { inject, ref, watch } from "vue";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue";
import ChevronUpDownIcon from "@heroicons/vue/24/outline/ChevronUpDownIcon";
import CheckIcon from "@heroicons/vue/24/outline/CheckIcon";
import { i18n } from "@/global/preferences";
import { KeyValuePair } from "@/global/types";
import { postData } from "@/global/fetchData";

const themes = ref<KeyValuePair[]>([
    { key: "light", value: "constants.themeList.lightTheme" },
    { key: "dark", value: "constants.themeList.darkTheme" },
]);
const storedThemeKey = localStorage.getItem("theme");
const themeIndex = themes.value.findIndex((theme) => theme.key === storedThemeKey);
const selectedTheme = ref<KeyValuePair>(themes.value[themeIndex] || themes.value[0]);

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const updateThemeSelection = async (newTheme: KeyValuePair) => {
    selectedTheme.value = newTheme;
    const newThemeKey = newTheme.key;
    const currentTheme = localStorage.getItem("theme");

    if (newThemeKey === currentTheme) return;

    localStorage.setItem("theme", newThemeKey);

    const result = await postData(`user/preferences/set_theme/`, { theme: newThemeKey });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.errorUpdatingTheme"),
            result.error as string
        );
        return;
    }

    displayPopup?.(
        "success",
        i18n.global.t("constants.popUpConstants.successMessages.success"),
        i18n.global.t("settingsPage.preferencesPage.popUpConstants.successMessages.themeUpdatedSuccessfully")
    );
};

watch(selectedTheme, updateThemeSelection);
</script>
