<template>
    <div class="relative">
        <Listbox as="div" v-model="selectedTimeZone">
            <div class="mb-2">
                <input
                    type="text"
                    v-model="searchQuery"
                    placeholder="Search time zones..."
                    class="w-full p-2 border rounded-md"
                />
            </div>
            <ListboxButton
                class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6"
            >
                <span class="block truncate">{{ selectedTimeZone || "Select a timezone" }}</span>
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
                    <li
                        v-if="filteredTimezones.length === 0"
                        class="relative cursor-default select-none py-2 pl-3 pr-9 text-gray-500"
                    >
                        No results found
                    </li>
                    <ListboxOption
                        v-else
                        as="template"
                        v-for="timezone in filteredTimezones"
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
import { ref, computed, watch, inject } from "vue";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue";
import ChevronUpDownIcon from "@heroicons/vue/24/outline/ChevronUpDownIcon";
import CheckIcon from "@heroicons/vue/24/outline/CheckIcon";
import moment from "moment-timezone";
import { i18n } from "@/global/preferences";
import { postData } from "@/global/fetchData";

const timezones = ref(moment.tz.names());
const searchQuery = ref("");
const initialLoadCount = Math.ceil(timezones.value.length * 0.25);
const visibleTimezones = ref(timezones.value.slice(0, initialLoadCount));
const storedTimeZone = localStorage.getItem("timezone");
const selectedTimeZone = ref(storedTimeZone || "");

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const updateTimezoneSelection = async (newTimeZone: string) => {
    selectedTimeZone.value = newTimeZone;
    const currentZone = localStorage.getItem("timezone");

    if (newTimeZone === currentZone) return;

    localStorage.setItem("timezone", newTimeZone);

    const result = await postData(`user/preferences/set_timezone/`, { timezone: newTimeZone });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.errorUpdatingTimezone"),
            result.error as string
        );
        return;
    }

    displayPopup?.(
        "success",
        i18n.global.t("constants.popUpConstants.successMessages.success"),
        i18n.global.t("settingsPage.preferencesPage.popUpConstants.successMessages.timezoneUpdatedSuccessfully")
    );
};

const filteredTimezones = computed(() => {
    const filtered = timezones.value.filter((timezone) =>
        timezone.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
    return filtered.slice(0, visibleTimezones.value.length);
});

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
