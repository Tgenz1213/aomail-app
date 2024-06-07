<template>
    <ShowNotification :showNotification="showTimezoneNotification" :notificationTitle="timezoneNotificationTitle"
        :notificationMessage="timezoneNotificationMessage" :backgroundColor="timezoneBackgroundColor"
        @dismiss-popup="dismissTimezonePopup" />

    <div class="relative">
        <Listbox as="div" v-model="selectedTimeZone">
            <ListboxButton
                class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6">
                <span class="block truncate">{{ selectedTimeZone }}</span>
                <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                </span>
            </ListboxButton>
            <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
                leave-to-class="opacity-0">
                <ListboxOptions @scroll="handleScroll"
                    class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption as="template" v-for="timezone in visibleTimezones" :key="timezone" :value="timezone"
                        v-slot="{ active, selected }">
                        <li
                            :class="[active ? 'bg-gray-800 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                            <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{ timezone
                                }}</span>
                            <span v-if="selected"
                                :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                            </span>
                        </li>
                    </ListboxOption>
                </ListboxOptions>
            </transition>
        </Listbox>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import ShowNotification from '../components/ShowNotification.vue';
import { fetchWithToken } from '../router/index.js';
import { API_BASE_URL } from '@/main';
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, ChevronUpDownIcon, CheckIcon } from '@headlessui/vue';
import moment from 'moment-timezone';

// Timezone options
const timezones = ref(moment.tz.names());
const initialLoadCount = Math.ceil(timezones.value.length * 0.25);
const visibleTimezones = ref(timezones.value.slice(0, initialLoadCount));

// Selected timezone
const storedTimeZone = localStorage.getItem("timezone");
const selectedTimeZone = ref(storedTimeZone);

// Notification state
const showTimezoneNotification = ref(false);
const timezoneNotificationTitle = ref('');
const timezoneNotificationMessage = ref('');
const timezoneBackgroundColor = ref('');
let timezoneTimerId = null;

// Functions
const dismissTimezonePopup = () => {
    showTimezoneNotification.value = false;
    clearTimeout(timezoneTimerId);
};

const displayTimezonePopup = () => {
    showTimezoneNotification.value = true;
    timezoneTimerId = setTimeout(dismissTimezonePopup, 4000);
};

const updateTimezoneSelection = async (newTimeZone) => {
    selectedTimeZone.value = newTimeZone;
    const currentZone = localStorage.getItem('timezone');

    if (newTimeZone === currentZone) return;

    localStorage.setItem('timezone', newTimeZone);

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/preferences/set_timezone/`, {
            headers: { 'Content-Type': 'application/json' },
            method: "POST",
            body: JSON.stringify({ timezone: newTimeZone }),
        });

        if (response.error) {
            setTimezoneNotification('bg-red-300', 'Error updating timezone', response.error);
        } else if (response.message === "Timezone updated successfully") {
            setTimezoneNotification('bg-green-300', 'Success!', 'Timezone updated successfully');
        }
    } catch (error) {
        setTimezoneNotification('bg-red-300', 'Error updating timezone', error.message);
    }
};

const setTimezoneNotification = (color, title, message) => {
    timezoneBackgroundColor.value = color;
    timezoneNotificationTitle.value = title;
    timezoneNotificationMessage.value = message;
    displayTimezonePopup();
};

// Lazy load more timezones
const loadMoreTimezones = () => {
    const currentCount = visibleTimezones.value.length;
    const newCount = currentCount + initialLoadCount;
    visibleTimezones.value = timezones.value.slice(0, newCount);
};

const handleScroll = (event) => {
    const listbox = event.target;
    if (listbox.scrollTop + listbox.clientHeight >= listbox.scrollHeight - 50) {
        loadMoreTimezones();
    }
};

watch(selectedTimeZone, updateTimezoneSelection);
</script>