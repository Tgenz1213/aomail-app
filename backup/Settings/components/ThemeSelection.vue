<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />
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
import { ref, watch } from "vue"
import NotificationTimer from "@/components/NotificationTimer.vue"
import { fetchWithToken } from "@/global/security"
import { API_BASE_URL } from "@/global/const"
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue"
import ChevronUpDownIcon from "@heroicons/vue/24/outline/ChevronUpDownIcon"
import CheckIcon from "@heroicons/vue/24/outline/CheckIcon"
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp"
import { i18n } from "@/global/Settings/preferences"
import { KeyValuePair } from "@/global/types"

const themes = ref<KeyValuePair[]>([
    { key: "light", value: "constants.themeList.lightTheme" },
    { key: "dark", value: "constants.themeList.darkTheme" },
])

const storedThemeKey = localStorage.getItem("theme")
const themeIndex = themes.value.findIndex((theme) => theme.key === storedThemeKey)
const selectedTheme = ref<KeyValuePair>(themes.value[themeIndex] || themes.value[0])

const showNotification = ref(false)
const notificationTitle = ref("")
const notificationMessage = ref("")
const backgroundColor = ref("")
const timerId = ref<number | null>(null)

const updateThemeSelection = async (newTheme: KeyValuePair) => {
    selectedTheme.value = newTheme
    const newThemeKey = newTheme.key
    const currentTheme = localStorage.getItem("theme")

    if (newThemeKey === currentTheme) return

    localStorage.setItem("theme", newThemeKey)

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/preferences/set_theme/`, {
            headers: { "Content-Type": "application/json" },
            method: "POST",
            body: JSON.stringify({ theme: newThemeKey }),
        })

        if (response && response.ok) {
            const responseData = await response.json()
            if (responseData.message === "Theme updated successfully") {
                displayPopup(
                    "success",
                    i18n.global.t("constants.popUpConstants.successMessages.success"),
                    i18n.global.t(
                        "settingsPage.preferencesPage.popUpConstants.successMessages.themeUpdatedSuccessfully"
                    )
                )
            } else {
                displayPopup(
                    "error",
                    i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.errorUpdatingTheme"),
                    responseData.error
                )
            }
        } else {
            displayPopup(
                "error",
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.errorUpdatingTheme"),
                response?.statusText || "Unknown error"
            )
        }
    } catch (error) {
        if (error instanceof Error) {
            displayPopup(
                "error",
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.errorUpdatingTheme"),
                error.message
            )
        }
    }
}

const displayPopup = (type: "success" | "error", title: string, message: string) => {
    if (type === "error") {
        displayErrorPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message)
    } else {
        displaySuccessPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message)
    }
    timerId.value = window.setTimeout(dismissPopup, 4000)
}

const dismissPopup = () => {
    showNotification.value = false
    if (timerId.value !== null) {
        clearTimeout(timerId.value)
    }
}

watch(selectedTheme, updateThemeSelection)
</script>
