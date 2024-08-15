<template>
    <div class="flex space-x-2 hidden pr-2 w-full mb-4">
        <div class="flex flex-col gap-4">
            <div class="flex gap-4 gap-y-2 w-full flex-wrap">
                <div class="flex-1 min-w-[150px] mt-2 relative">
                    <Combobox as="div" v-model="selectedPerson">
                        <div class="relative flex items-center w-full">
                            <user-icon
                                class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400"
                            />
                            <ComboboxInput
                                class="w-full rounded-md border-0 bg-white py-3 pl-10 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 truncate"
                                @input="queryGetContacts = $event.target.value"
                                :display-value="(person) => person?.username"
                                :placeholder="$t('searchPage.toAddressesSelectedPlaceholder')"
                                style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden"
                            />
                            <ComboboxButton
                                class="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center focus:outline-none"
                            >
                                <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </ComboboxButton>
                        </div>
                        <ComboboxOptions
                            v-if="filteredPeople.length > 0"
                            class="absolute z-10 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm left-0 right-0"
                        >
                            <ComboboxOption
                                v-for="person in filteredPeople"
                                :value="person"
                                :key="person"
                                as="template"
                                v-slot="{ active, selected }"
                            >
                                <li
                                    @click="toggleSelection(person)"
                                    :class="[
                                        'relative cursor-default select-none py-2 pl-3 pr-9',
                                        active ? 'bg-gray-500 text-white' : 'text-gray-900',
                                    ]"
                                >
                                    <div class="flex">
                                        <span :class="['truncate', selected && 'font-semibold']">
                                            {{ person.username }}
                                        </span>
                                        <span
                                            :class="[
                                                'ml-2 truncate hidden text-gray-500',
                                                active ? 'text-indigo-200' : 'text-gray-500',
                                            ]"
                                        >
                                            &lt;{{ person.email }}&gt;
                                        </span>
                                    </div>
                                    <span
                                        v-if="selected"
                                        :class="[
                                            'absolute inset-y-0 right-0 flex items-center pr-4',
                                            active ? 'text-white' : 'text-gray-500',
                                        ]"
                                    >
                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                    </span>
                                </li>
                            </ComboboxOption>
                        </ComboboxOptions>
                    </Combobox>
                </div>
                <div class="flex-1 min-w-[150px] mt-2">
                    <div class="relative">
                        <div
                            class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-12 text-left flex items-center text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                            @click="toggleDropdown"
                            @click.self="toggleDropdown"
                        >
                            <adjustments-horizontal-icon class="w-5 h-5 mr-2 mt-2 mb-2 text-gray-400" />
                            <span class="block truncate text-gray-700">
                                {{
                                    attachmentsSelected.length > 0
                                        ? attachmentsSelected.map((item: any) => item.name).join(", ")
                                        : $t("searchPage.attachmentSelectedPlaceholder")
                                }}
                            </span>
                            <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                <ChevronUpDownIcon class="h-5 w-5 text-gray-400 mt-2 mb-2" aria-hidden="true" />
                            </span>
                        </div>
                        <transition
                            leave-active-class="transition ease-in duration-100"
                            leave-from-class="opacity-100"
                            leave-to-class="opacity-0"
                        >
                            <div
                                v-if="isAttachmentDropdownOpen"
                                class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                            >
                                <div
                                    v-for="type in attachmentTypes"
                                    :key="type.extension"
                                    class="relative cursor-default select-none py-2 pl-3 pr-9"
                                    :class="[isSelected(type) ? 'bg-gray-500 text-white' : 'text-gray-900']"
                                >
                                    <div class="flex items-center">
                                        <input
                                            type="checkbox"
                                            :id="type.extension"
                                            :value="type"
                                            v-model="attachmentsSelected"
                                            class="form-checkbox h-4 w-4 text-gray-600 transition duration-150 ease-in-out"
                                        />
                                        <label
                                            :for="type.extension"
                                            class="ml-2 block truncate"
                                            :class="[isSelected(type) ? 'font-semibold' : 'font-normal']"
                                        >
                                            {{ type.name }} {{ type.extension }}
                                        </label>
                                    </div>
                                    <span
                                        v-if="isSelected(type)"
                                        class="absolute inset-y-0 right-0 flex items-center pr-4"
                                        :class="[isSelected(type) ? 'text-white' : 'text-gray-500']"
                                    >
                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                    </span>
                                </div>
                            </div>
                        </transition>
                    </div>
                </div>
                <div class="flex-1 min-w-[150px] mt-2 relative">
                    <Combobox as="div" v-model="fromSelectedPerson">
                        <div class="relative flex items-center w-full">
                            <user-icon
                                class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400"
                            />
                            <ComboboxInput
                                class="w-full rounded-md border-0 bg-white py-3 pl-10 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 truncate"
                                @input="queryGetContacts = $event.target.value"
                                :display-value="(person) => person?.username"
                                :placeholder="$t('searchPage.fromAddressesSelectedPlaceholder')"
                                style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden"
                            />
                            <ComboboxButton
                                class="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center focus:outline-none"
                            >
                                <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </ComboboxButton>
                        </div>
                        <ComboboxOptions
                            v-if="filteredPeople.length > 0"
                            class="absolute z-10 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm left-0 right-0"
                        >
                            <ComboboxOption
                                v-for="person in filteredPeople"
                                :value="person"
                                :key="person"
                                as="template"
                                v-slot="{ active, selected }"
                            >
                                <li
                                    @click="toggleSelection(person)"
                                    :class="[
                                        'relative cursor-default select-none py-2 pl-3 pr-9',
                                        active ? 'bg-gray-500 text-white' : 'text-gray-900',
                                    ]"
                                >
                                    <div class="flex">
                                        <span :class="['truncate', selected && 'font-semibold']">
                                            {{ person.username }}
                                        </span>
                                        <span
                                            :class="[
                                                'ml-2 truncate hidden text-gray-500',
                                                active ? 'text-indigo-200' : 'text-gray-500',
                                            ]"
                                        >
                                            &lt;{{ person.email }}&gt;
                                        </span>
                                    </div>
                                    <span
                                        v-if="selected"
                                        :class="[
                                            'absolute inset-y-0 right-0 flex items-center pr-4',
                                            active ? 'text-white' : 'text-gray-500',
                                        ]"
                                    >
                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                    </span>
                                </li>
                            </ComboboxOption>
                        </ComboboxOptions>
                    </Combobox>
                </div>
                <div class="flex-1 min-w-[150px] mt-2 relative">
                    <div class="relative flex items-center w-full">
                        <EnvelopeIcon
                            class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400"
                        />
                        <input
                            type="text"
                            class="w-full rounded-md border-0 bg-white py-3 pl-10 pr-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                            :placeholder="$t('searchPage.subjectSelectedPlaceholder')"
                        />
                    </div>
                </div>
                <div class="flex-1 min-w-[150px] mt-2 relative">
                    <div class="relative flex items-center w-full">
                        <HashtagIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                        <input
                            type="text"
                            class="w-full rounded-md border-0 bg-white py-3 pl-10 pr-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                            :placeholder="$t('searchPage.keywordsPlaceholder')"
                        />
                    </div>
                </div>
                <div class="flex-1 min-w-[150px] mt-2 relative">
                    <div class="relative flex items-center w-full">
                        <CalendarIcon
                            class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
                        />
                        <input
                            type="date"
                            :value="startDate"
                            @input="updateDate"
                            class="w-full rounded-md border-0 bg-white py-3 pl-10 pr-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 appearance-none"
                            :placeholder="$t('searchPage.dateFromPlaceholder')"
                        />
                    </div>
                </div>
                <div class="flex-1 min-w-[150px] mt-2 relative">
                    <Listbox as="div" v-model="selectedSearchIn">
                        <div class="relative">
                            <ListboxButton
                                class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-12 text-left flex items-center text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                            >
                                <MagnifyingGlassIcon class="w-5 h-5 mr-2 mt-2 mb-2 text-gray-400" />
                                <span class="block truncate text-gray-700">
                                    {{
                                        selectedSearchIn
                                            ? $t(`searchPage.searchIn.${selectedSearchIn.key}`)
                                            : $t("searchPage.searchInSelectedPlaceholder")
                                    }}
                                </span>
                                <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400 mt-2 mb-2" aria-hidden="true" />
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
                                        v-for="option in searchIn"
                                        :key="option.key"
                                        :value="option"
                                        v-slot="{ active, selected }"
                                    >
                                        <li
                                            :class="[
                                                active ? 'bg-gray-500 text-white' : 'text-gray-900',
                                                'relative cursor-default select-none py-2 pl-3 pr-9',
                                            ]"
                                        >
                                            <span
                                                :class="[
                                                    selected ? 'font-semibold' : 'font-normal',
                                                    'block truncate ml-7 mr-2',
                                                ]"
                                            >
                                                {{ $t(`searchPage.searchIn.${option.key}`) }}
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
                <div class="flex-1 min-w-[150px] mt-2 relative">
                    <Listbox as="div" v-model="selectedInterval">
                        <div class="relative">
                            <ListboxButton
                                class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-12 text-left flex items-center text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                            >
                                <CalendarIcon class="w-5 h-5 mr-2 mt-2 mb-2 text-gray-400" />
                                <span class="block truncate text-gray-700">
                                    {{
                                        selectedInterval
                                            ? $t(`searchPage.dateIntervals.${selectedInterval}`)
                                            : $t("searchPage.dateRangePlaceholder")
                                    }}
                                </span>
                                <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400 mt-2 mb-2" aria-hidden="true" />
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
                                        v-for="interval in dateIntervals"
                                        :key="interval.key"
                                        :value="interval"
                                        v-slot="{ active, selected }"
                                    >
                                        <li
                                            :class="[
                                                active ? 'bg-gray-500 text-white' : 'text-gray-900',
                                                'relative cursor-default select-none py-2 pl-3 pr-9',
                                            ]"
                                        >
                                            <span
                                                :class="[
                                                    selected ? 'font-semibold' : 'font-normal',
                                                    'block truncate ml-7 mr-2',
                                                ]"
                                            >
                                                {{ $t(`searchPage.dateIntervals.${interval.key}`) }}
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
                <div class="flex-1 min-w-[150px] mt-2 relative">
                    <div class="relative flex items-center w-full">
                        <HandRaisedIcon
                            class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400"
                        />
                        <input
                            type="text"
                            class="w-full rounded-md border-0 bg-white py-3 pl-10 pr-4 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                            :placeholder="$t('searchPage.doesntContainPlaceholder')"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, inject, Ref } from "vue";
import { Combobox, ComboboxButton, ComboboxInput, ComboboxOption, ComboboxOptions } from "@headlessui/vue";
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from "@headlessui/vue";
import {
    CheckIcon,
    ChevronUpDownIcon,
    MagnifyingGlassIcon,
    UserIcon,
    AdjustmentsHorizontalIcon,
    EnvelopeIcon,
    HashtagIcon,
    CalendarIcon,
    HandRaisedIcon,
} from "@heroicons/vue/24/outline";
import { AttachmentType, KeyValuePair, Recipient } from "@/global/types";

const attachmentsSelected = inject<Ref<AttachmentType[]>>("attachmentsSelected") || ref([]);
const startDate = inject<Ref<string>>("startDate") || ref("");
const selectedInterval = inject<Ref<string>>("selectedInterval") || ref("");
const selectedRecipients = inject<Ref<Recipient[]>>("selectedRecipients") || ref([]);
const fromSelectedPerson = inject<Ref<Recipient[]>>("fromSelectedPerson") || ref([]);
const selectedPerson = inject<Ref<Recipient[]>>("selectedPerson") || ref([]);
const selectedSearchIn = inject<Ref<KeyValuePair>>("selectedSearchIn") || ref({});
const isAttachmentDropdownOpen = ref(false);

const updateDate = (event: { target: { value: string } }) => {
    startDate.value = event.target.value;
};

const dateIntervals = [
    { key: "oneDay" },
    { key: "threeDays" },
    { key: "oneWeek" },
    { key: "twoWeeks" },
    { key: "oneMonth" },
    { key: "twoMonths" },
    { key: "sixMonths" },
    { key: "oneYear" },
];

const searchIn: KeyValuePair[] = [
    { key: "all", value: "All" },
    { key: "read", value: "Read" },
    { key: "notRead", value: "Not read" },
];

const attachmentTypes: AttachmentType[] = [
    { extension: ".docx", name: "Word Document" },
    { extension: ".xlsx", name: "Excel Spreadsheet" },
    { extension: ".pptx", name: "PowerPoint Presentation" },
    { extension: ".pdf", name: "PDF Document" },
    { extension: ".jpg", name: "JPEG Image" },
    { extension: ".png", name: "PNG Image" },
    { extension: ".gif", name: "GIF Image" },
    { extension: ".txt", name: "Text Document" },
    { extension: ".zip", name: "ZIP Archive" },
    { extension: ".mp3", name: "MP3 Audio" },
    { extension: ".mp4", name: "MP4 Video" },
    { extension: ".html", name: "HTML Document" },
];

const toggleDropdown = () => {
    isAttachmentDropdownOpen.value = !isAttachmentDropdownOpen.value;
};

const isSelected = (type: AttachmentType): boolean => {
    console.log("attachmentsSelected", attachmentsSelected.value);
    return attachmentsSelected.value.some((item: AttachmentType) => item.extension === type.extension);
};

const toggleSelection = (person: Recipient) => {
    const index = selectedRecipients.value.findIndex((recipient) => recipient.email === person.email);
    if (index === -1) {
        selectedRecipients.value.push(person);
    } else {
        selectedRecipients.value.splice(index, 1);
    }
};
</script>

<style scoped>
input[type="date"]::-webkit-calendar-picker-indicator {
    opacity: 0;
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
}
</style>
