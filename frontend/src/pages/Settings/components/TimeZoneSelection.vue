<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />

    <div class="relative">
        <Listbox as="div" v-model="selectedTimeZone">
            <ListboxButton
                class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6"
            >
                <span class="block truncate">{{ selectedTimeZone }}</span>
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
                    @scroll="handleScroll"
                    class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                >
                    <ListboxOption
                        as="template"
                        v-for="timezone in visibleTimezones"
                        :key="timezone"
                        :value="timezone"
                        v-slot="{ active, selected }"
                    >
                        <li
                            :class="[
                                active ? 'bg-gray-800 text-white' : 'text-gray-900',
                                'relative cursor-default select-none py-2 pl-3 pr-9',
                            ]"
                        >
                            <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                                {{ timezone }}
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

// todo: replace all "GET" and "POST" backend call with getData & postData from @/global/fetchData file


import { ref, watch } from "vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue";
import ChevronUpDownIcon from "@heroicons/vue/24/outline/ChevronUpDownIcon";
import CheckIcon from "@heroicons/vue/24/outline/CheckIcon";
import moment from "moment-timezone";
import { fetchWithToken } from "@/global/security";
import { API_BASE_URL } from "@/global/const";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { i18n } from "@/pages/Settings/utils/preferences";

const timezones = ref(moment.tz.names());
const initialLoadCount = Math.ceil(timezones.value.length * 0.25);
const visibleTimezones = ref(timezones.value.slice(0, initialLoadCount));

const storedTimeZone = localStorage.getItem("timezone");
const selectedTimeZone = ref(storedTimeZone || "");

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

const updateTimezoneSelection = async (newTimeZone: string) => {
    selectedTimeZone.value = newTimeZone;
    const currentZone = localStorage.getItem("timezone");

    if (newTimeZone === currentZone) return;

    localStorage.setItem("timezone", newTimeZone);

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/preferences/set_timezone/`, {
            headers: { "Content-Type": "application/json" },
            method: "POST",
            body: JSON.stringify({ timezone: newTimeZone }),
        });
        if (response instanceof Response) {
            const data = await response.json();

            if (data.error) {
                displayPopup(
                    "error",
                    i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.errorUpdatingTimezone"),
                    data.error
                );
            } else if (data.message === "Timezone updated successfully") {
                displayPopup(
                    "success",
                    i18n.global.t("constants.popUpConstants.successMessages.success"),
                    i18n.global.t(
                        "settingsPage.preferencesPage.popUpConstants.successMessages.timezoneUpdatedSuccessfully"
                    )
                );
            }
        }
    } catch (error) {
        if (error instanceof Error) {
            displayPopup(
                "error",
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.errorUpdatingTimezone"),
                error.message
            );
        }
    }
};

const loadMoreTimezones = () => {
    const currentCount = visibleTimezones.value.length;
    const newCount = currentCount + initialLoadCount;
    visibleTimezones.value = timezones.value.slice(0, newCount);
};

const handleScroll = (event: Event) => {
    const listbox = event.target as HTMLElement;
    if (listbox.scrollTop + listbox.clientHeight >= listbox.scrollHeight - 50) {
        loadMoreTimezones();
    }
};

watch(selectedTimeZone, updateTimezoneSelection);
</script>
