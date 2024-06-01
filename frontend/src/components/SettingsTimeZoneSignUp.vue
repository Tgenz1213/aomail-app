<template>
    <Listbox v-model="selectedTimeZone">
        <ListboxButton
            class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6">
            <span class="block truncate">{{ selectedTimeZone.value }}</span>
            <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
            </span>
        </ListboxButton>
        <ListboxOptions
            class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
            as="ul">
            <ListboxOption v-for="timezone in timezones" :key="timezone" :value="{ value: timezone }"
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
    </Listbox>
</template>

<script setup>
import { ref, watch } from 'vue';
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, ChevronUpDownIcon, CheckIcon } from '@headlessui/vue';
// TODO (good luck) fix packages conflicts
import moment from 'moment-timezone';

// Get the list of all time zones
const timezones = ref(moment.tz.names());

if (!localStorage.getItem("timezone")) {
    localStorage.setItem("timezone", "UTC");
}
const storedTimeZone = localStorage.getItem("timezone");
const selectedTimeZone = ref({ value: storedTimeZone });

const updateTimeZoneSelection = (newTimeZone) => {
    localStorage.setItem('timezone', newTimeZone.value);
};

watch(selectedTimeZone, updateTimeZoneSelection);
</script>