<template>
    <div>
        <Listbox v-model="selectedTimeZone">
            <ListboxButton
                class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6">
                <span class="block truncate">{{ selectedTimeZone }}</span>
                <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                </span>
            </ListboxButton>
            <ListboxOptions
                class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                as="ul" @scroll="handleScroll">
                <ListboxOption v-for="timezone in visibleTimezones" :key="timezone" :value="timezone"
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
    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, ChevronUpDownIcon, CheckIcon } from '@headlessui/vue';
import moment from 'moment-timezone';

const timezones = ref(moment.tz.names());
// Load the first 25% of the list to avoid UX freeze
const initialLoadCount = Math.ceil(timezones.value.length * 0.25);
const visibleTimezones = ref(timezones.value.slice(0, initialLoadCount));

const selectedTimeZone = ref(localStorage.getItem('timezone') || 'UTC');

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

const updateTimeZoneSelection = (newTimeZone) => {
    localStorage.setItem('timezone', newTimeZone);
    selectedTimeZone.value = newTimeZone;
};

watch(selectedTimeZone, (newTimeZone) => {
    updateTimeZoneSelection(newTimeZone);
});
</script>
