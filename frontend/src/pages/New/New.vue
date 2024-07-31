<template>
    <NotificationTimer :showNotification="showNotification" :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" @dismiss-popup="dismissPopup" />
    <div class="flex flex-col justify-center items-center h-screen" :class="bgColor">
        <div class="flex h-full w-full">
            <div class="w-[90px] bg-white ring-1 shadow-sm ring-black ring-opacity-5 2xl:w-[100px]">
                <navbar></navbar>
            </div>
            <div id="firstMainColumn"
                class="flex flex-col bg-gray-50 lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[700px]">
                <div class="flex items-center justify-center h-[65px] 2xl:h-[80px]">
                    <div class="flex gap-x-3 items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                            stroke="currentColor" class="w-6 h-6 2xl:w-7 2xl:h-7">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
                        </svg>
                        
                        <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ $t('constants.aiAssistant') }}
                        </h1>
                    </div>
                </div>
                <div class="flex flex-1 flex-col divide-y">
                    <div class="overflow-y-auto flex-1" style="margin-right: 2px;" ref="scrollableDiv">
                        <div class="px-10 py-4 2xl:px-13.5 2xl:py-6">
                            <div class="flex-grow">
                                <div id="AIContainer">
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="flex flex-col h-[22vh] 2xl:h-[23vh]">
                        <textarea id="dynamicTextarea" @keydown.enter="handleEnterKey" @input="adjustHeight"
                            v-model="textareaValue"
                            class="overflow-y-hidden pt-4 pl-6 flex-1 w-full border-transparent bg-transparent text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 focus:border-transparent focus:bg-transparent focus:ring-0 2xl:pt-5 2xl:pl-7 2xl:text-base"
                            :placeholder="$t('constants.instruction')">
                        </textarea>
                        <div v-if="stepcontainer == 1" class="flex justify-end m-3 2xl:m-5">
                            <div class="flex mt-4 space-x-4 items-center">
                                <div>
                                    <select id="lengthSelect"
                                        class="h-10 px-8 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white focus:bg-gray-900 focus:text-white border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                                        <option value="very short">{{ $t('newPage.veryBrief') }}</option>
                                        <option value="short" selected>{{ $t('newPage.brief') }}</option>
                                        <option value="long">{{ $t('newPage.long') }}</option>
                                    </select>
                                </div>
                                <div>
                                    <select id="formalitySelect"
                                        class="h-10 px-8 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white focus:bg-gray-900 focus:text-white border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                                        <option value="very informal">{{ $t('newPage.informal') }}</option>
                                        
                                        <option value="formal" selected>{{ $t('newPage.formal') }}</option>
                                        <option value="very formal">{{ $t('newPage.veryFormal') }}</option>
                                    </select>
                                </div>
                                <div class="flex items-center">
                                    <button @click="handleAIClick" type="button"
                                        class="2xl:w-[100px] w-[100px] rounded-md bg-gray-700 px-6 py-2.5 2xl:px-6 2xl:py-3 text-sm 2xl:text-base text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">
                                        {{ $t('constants.userActions.send') }}
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div v-else class="flex justify-end m-3 2xl:m-5">
                            <button @click="handleAIClick" type="button"
                                class="2xl:w-[100px] w-[80px] rounded-md bg-gray-700 px-5.5 py-2.5 2xl:px-6.5 2xl:py-3 2xl:text-base text-sm text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">{{
                                    $t('constants.userActions.send') }}</button>
                        </div>
                    </div>
                </div>
            </div>

            
            <div id="secondMainColumn"
                class="flex-grow bg-white lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[720px]">
                <div class="flex flex-col h-full w-full">
                    <!--Titre-->
                    <div class="flex items-center h-[65px] justify-center lg:py-5 2xl:h-[80px] min-h-8">
                        <div class="flex gap-x-3 items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                                stroke="currentColor" class="w-6 h-6 2xl:w-7 2xl:h-7">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672ZM12 2.25V4.5m5.834.166-1.591 1.591M20.25 10.5H18M7.757 14.743l-1.59 1.59M6 10.5H3.75m4.007-4.243-1.59-1.59" />
                            </svg>
                            <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{
                                $t('constants.userActions.enterManually')
                            }}</h1>
                        </div>
                    </div>

                    <form class="flex-1 flex flex-col w-full px-10 pt-4 2xl:px-14 2xl:pt-6 overflow-hidden">
                        <div class="flex flex-col space-y-5 h-full w-full">
                            <div class="">

                                <!--Recipie List and CC List-->
                                <div class="flex flex-wrap">
                                    <!-- Main Recipients List -->
                                    <div v-if="selectedPeople.length > 0" class="flex items-center mb-1">
                                        <div v-for="person in selectedPeople" :key="person.email"
                                            class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1 2xl:px-3 2xl:py-2 2xl:mr-2">
                                            {{ person.username || person.email }}
                                            <button @click="removePersonFromMain(person)">×</button>
                                        </div>
                                    </div>
                                    <!-- CC Recipients List -->
                                    <div v-if="selectedCC.length > 0" class="flex items-center mb-1">
                                        <div v-for="person in selectedCC" :key="person.email"
                                            class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1 2xl:px-3 2xl:py-2 2xl:mr-2">
                                            <span class="font-semibold mr-1 2xl:mr-2">{{
                                                $t('constants.sendEmailConstants.carbonCopyInitialsTwoDots') }}</span>
                                            {{ person.username || person.email }}
                                            <button @click="removePersonFromCC(person)">×</button>
                                        </div>
                                    </div>
                                    <!-- CCI Recipients List -->
                                    <div v-if="selectedCCI.length > 0" class="flex items-center mb-1">
                                        <div v-for="person in selectedCCI" :key="person.email"
                                            class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1 2xl:px-3 2xl:py-2 2xl:mr-2">
                                            <span class="font-semibold mr-1 2xl:mr-2">{{
                                                $t('constants.sendEmailConstants.blindCarbonCopyInitialsTwoDots')
                                            }}</span>
                                            {{ person.username || person.email }}
                                            <button @click="removePersonFromCCI(person)">×</button>
                                        </div>
                                    </div>
                                </div>
                                <!--Option de texte du mail-->
                                <div class="flex items-stretch gap-1 2xl:gap-2">
                                    <div class="flex-grow">
                                        <div class="relative items-stretch">

                                            <div class="relative w-full">
                                                <div v-if="!isFocused2"
                                                    class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 2xl:ml-3">
                                                    <UserGroupIcon
                                                        class="w-4 h-4 pointer-events-none 2xl:w-5 2xl:h-5" />
                                                    <label for="email"
                                                        class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none 2xl:text-base">{{
                                                            $t('constants.recipient') }}</label>
                                                </div>
                                                <Combobox as="div" v-model="selectedPerson"
                                                    @update:model-value="personSelected">
                                                    <ComboboxInput id="recipients"
                                                        class="w-full h-10 2xl:h-11 rounded-md border-0 bg-white py-2 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 2xl:py-3 2xl:pl-4 2xl:pr-14 2xl:text-base"
                                                        @change="query = $event.target.value"
                                                        :display-value="(person) => person?.name"
                                                        @focus="handleFocusDestinary" @blur="handleBlur2($event)"
                                                        @keydown.enter="handleEnterKey" />
                                                    <ComboboxButton
                                                        class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none 2xl:px-3">
                                                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400 2xl:h-6 2xl:w-6"
                                                            aria-hidden="true" />
                                                    </ComboboxButton>
                                                    <ComboboxOptions v-if="filteredPeople.length > 0"
                                                        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm 2xl:text-base"
                                                        style="z-index: 21">
                                                        <ComboboxOption v-for="person in filteredPeople"
                                                            :key="person.username" :value="person" as="template"
                                                            v-slot="{ active, selected }">
                                                            <li
                                                                :class="['relative cursor-default select-none py-2 pl-3 pr-9', active ? 'bg-gray-500 text-white' : 'text-gray-900']">
                                                                <div class="flex">
                                                                    <span
                                                                        :class="['truncate', selected && 'font-semibold']">
                                                                        {{ person.username }}
                                                                    </span>
                                                                    <span
                                                                        :class="['ml-2 truncate text-gray-800', active ? 'text-gray-200' : 'text-gray-800']">
                                                                        {{ person.email }}
                                                                    </span>
                                                                </div>
                                                                <span v-if="selected"
                                                                    :class="['absolute inset-y-0 right-0 flex items-center pr-4', active ? 'text-white' : 'text-gray-500']">
                                                                    <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                                                </span>
                                                            </li>
                                                        </ComboboxOption>
                                                    </ComboboxOptions>
                                                </Combobox>
                                            </div>


                                        </div>
                                    </div>

                                    <div class="flex gap-1 2xl:gap-2">
                                        <button type="button" @click="toggleCC"
                                            :class="['inline-flex items-center gap-x-1.5 rounded-md px-2.5 py-1.5 text-sm font-semibold hover:bg-gray-600 hover:text-white', activeType === 'CC' ? 'bg-gray-500 text-white' : 'bg-gray-100 text-gray-400']"
                                            class="ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 2xl:px-3 2xl:py-2 2xl:text-base">
                                            {{ $t('newPage.carbonCopyInitials') }}
                                        </button>
                                        <button type="button" @click="toggleCCI"
                                            :class="['inline-flex items-center gap-x-1.5 rounded-md px-2.5 py-1.5 text-sm font-semibold hover:bg-gray-600 hover:text-white', activeType === 'CCI' ? 'bg-gray-500 text-white' : 'bg-gray-100 text-gray-400']"
                                            class="ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 2xl:px-3 2xl:py-2 2xl:text-base">
                                            {{ $t('newPage.blindCarbonCopyInitials') }}
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div class="">
                                <div class="flex flex-wrap">
                                    <div v-for="(file, index) in uploadedFiles" :key="index"
                                        class="flex items-center mb-1 mr-1 bg-gray-200 rounded px-2 py-1 2xl:px-3 2xl:py-2 2xl:mr-2">
                                        {{ file.name }}
                                        <button @click="removeFile(index)">×</button>
                                    </div>
                                </div>
                                <div class="flex items-stretch gap-1 2xl:gap-2">
                                    <div class="flex-grow">
                                        <div
                                            class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 w-full">
                                            <div class="relative w-full">
                                                <div v-if="!isFocused && !inputValue"
                                                    class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 2xl:ml-3 z-10">
                                                    <Bars2Icon class="w-4 h-4 pointer-events-none 2xl:w-5 2xl:h-5" />
                                                    <label for="username"
                                                        class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none 2xl:text-base">{{
                                                            $t('constants.subject') }}</label>
                                                </div>
                                                <input id="objectInput" v-model="inputValue" type="text"
                                                    class="block h-10 2xl:h-11 flex-1 border-0 bg-transparent py-2 pl-3 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6 w-full z-20 relative 2xl:py-3 2xl:pl-4 2xl:text-base"
                                                    @focus="handleFocusObject" @blur="handleBlur"
                                                    @input="handleInputUpdateObject" />
                                            </div>
                                        </div>
                                    </div>
                                    <div class="flex">
                                        <input type="file" ref="fileInput" @change="handleFileUpload" multiple hidden>
                                        <button @click="triggerFileInput" type="button"
                                            class="inline-flex items-center gap-x-1.5 rounded-md bg-gray-100 px-2.5 py-1.5 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-300 shadow-sm hover:ring-transparent hover:bg-gray-600 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 2xl:px-3 2xl:py-2 2xl:text-base">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                                stroke-width="1.5" stroke="currentColor"
                                                class="w-6 h-6 2xl:w-7 2xl:h-7">
                                                <path stroke-linecap="round" stroke-linejoin="round"
                                                    d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13" />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div class="flex flex-col h-full space-y-5 pb-4 2xl:pb-6 overflow-hidden ">
                                <div class="flex-1 overflow-hidden h-screen border-b-2 rounded-lg">
                                    <div id="editor-container"
                                        class=" flex-1 h-full w-full flex flex-col border-solid ">
                                        <div id="editor" class="flex-1">
                                            <!-- Quill editor will be initialized here -->
                                        </div>
                                    </div>
                                </div>

                                <div class="flex gap-x-2 mb-5 2xl:gap-3 2xl:mb-6 items-stretch">
                                    <!-- EMAIL LIST -->
                                    <div class="relative flex-grow flex items-stretch">
                                        <Listbox as="div" v-model="emailSelected" class="w-full flex flex-col">
                                            <ListboxButton
                                                class="relative w-full h-full cursor-default rounded-md bg-white px-6 py-2 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6 2xl:px-7 2xl:py-3 2xl:text-base">
                                                <span class="block truncate">{{ emailSelected }}</span>
                                                <span
                                                    class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400"
                                                        aria-hidden="true" />
                                                </span>
                                            </ListboxButton>
                                            <transition leave-active-class="transition ease-in duration-100"
                                                leave-from-class="opacity-100" leave-to-class="opacity-0">
                                                <ListboxOptions
                                                    class="absolute z-10 mb-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm bottom-full">
                                                    <ListboxOption as="template" v-for="email in emailsLinked"
                                                        :key="email.email" :value="email.email"
                                                        v-slot="{ active, selected }">
                                                        <li
                                                            :class="[active ? 'bg-gray-800 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                                                            <span
                                                                :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{
                                                                    email.email }}</span>
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

                                    <div class="inline-flex rounded-lg shadow-lg items-stretch">
                                        <button @click="sendEmail"
                                            class="bg-gray-700 rounded-l-lg px-6 py-2 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center 2xl:px-7 2xl:py-3 2xl:text-lg">
                                            {{ $t('constants.userActions.send') }}
                                            <PaperAirplaneIcon class="w-4 2xl:w-5" aria-hidden="true" />
                                        </button>
                                        <Menu as="div" class="relative -ml-px block items-stretch">
                                            <MenuButton
                                                class="relative inline-flex items-center rounded-r-lg px-2 py-2 text-white border-l border-gray-300 bg-gray-700 hover:bg-gray-900 focus:z-10 2xl:px-3 2xl:py-3">
                                                <span class="sr-only">{{ $t('newPage.openOptions') }}</span>
                                                <ChevronDownIcon class="h-8 w-5 2xl:h-9 2xl:w-6" aria-hidden="true" />
                                            </MenuButton>
                                            <transition enter-active-class="transition ease-out duration-100"
                                                enter-from-class="transform opacity-0 -translate-y-2"
                                                enter-to-class="transform opacity-100 translate-y-0"
                                                leave-active-class="transition ease-in duration-75"
                                                leave-from-class="transform opacity-100 translate-y-0"
                                                leave-to-class="transform opacity-0 -translate-y-2">
                                                <MenuItems
                                                    class="absolute right-0 z-10 -mr-1 bottom-full mb-2 w-56 origin-bottom-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                                                        <div class="py-1">
                                                            <button
                                                                :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']"
                                                                @click="scheduleSend">
                                                                Schedule send
                                                            </button>
                                                        </div>
                                                </MenuItems>
                                            </transition>
                                        </Menu>
                                    </div>

                                </div>
                            </div>

                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
</template>

<script setup>
import { computed, ref, onMounted, nextTick } from 'vue';
import { watch } from 'vue';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue';
import NotificationTimer from '@/components/NotificationTimer.vue';
import Quill from 'quill';
import { API_BASE_URL, MICROSOFT } from '@/global/const';

import {
    Combobox,
    ComboboxButton,
    ComboboxInput,
    ComboboxOption,
    Listbox,
    ListboxButton,
    ListboxOptions,
    ListboxOption,
    ChevronUpDownIcon,
    ComboboxOptions,
} from '@headlessui/vue'
import { useI18n } from 'vue-i18n';

// Use i18n
const { t } = useI18n();

// Variable to prevent the user from starting a prompt if AI is writing
let isAIWriting = ref(false);

// variables to display a notification
let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
let timerId = ref(null);

let history = ref({});





// lists of different types of recipients
const people = [];

const requestOptions = {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
};

// request to update the list of contacts (people array)
fetchWithToken(`${API_BASE_URL}user/contacts/`, requestOptions)
    .then(response => {
        people.push(...response);
    })
    .catch(error => {
        console.error("Error fetching contacts:", error);
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('constants.popUpConstants.errorMessages.contactFetchError');
        notificationMessage.value = error;
        displayPopup();
    });


const selectedPeople = ref([]);
const selectedCC = ref([]);
const selectedCCI = ref([]);
const activeType = ref(null);  // null, 'CC', or 'CCI'

const query = ref('');
const getFilteredPeople = (query, people) => {
    return computed(() => {
        if (query.value === '') {
            return people;
        } else {
            return people.filter((person) => {
                if (person.username === "") {
                    person.username = person.email
                        .split('@')[0]
                        .split(/\.|-/)
                        .map(p => p.charAt(0).toUpperCase() + p.slice(1))
                        .join(' ');
                }
                // VERY IMPORTANT: this line checks if the input matches either the username or the email
                return person.username.toLowerCase().includes(query.value.toLowerCase()) || person.email.toLowerCase().includes(query.value.toLowerCase());
            });
        }
    });
}

const filteredPeople = getFilteredPeople(query, people);
const emit = defineEmits(['update:selectedPerson']);
const selectedPerson = ref('');

watch(selectedPerson, (newValue) => {
    
    hasValueEverBeenEntered.value = true; 
    
    emit('update:selectedPerson', newValue);
});

const inputValue = ref('');
const isFirstTimeDestinary = ref(true); // to detect first letter object input
const isFirstTimeEmail = ref(true); // to detect first letter email content input
const isFocused = ref(false);
const isFocused2 = ref(false);
const hasValueEverBeenEntered = ref(false);

let emailsLinked = ref(null);
let emailSelected = ref('');
emailSelected.value = localStorage.getItem("email");

if (!emailSelected.value) {
    fetchWithToken(`${API_BASE_URL}user/get_first_email/`, requestOptions)
        .then(response => {
            emailSelected.value = response.email;
            localStorage.setItem("email", emailSelected.value);
        })
        .catch(error => {
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle.value = t('constants.popUpConstants.errorMessages.primaryEmailFetchError');
            notificationMessage.value = error;
            displayPopup();
        });
}

fetchWithToken(`${API_BASE_URL}user/emails_linked/`, requestOptions)
    .then(response => {
        emailsLinked.value = response;
    })
    .catch(error => {
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('constants.popUpConstants.errorMessages.emailFetchError');
        notificationMessage.value = error;
        displayPopup();
    });

function setEmailSelected() {
    localStorage.setItem("email", emailSelected.value);
}
function dismissPopup() {
    showNotification.value = false;
    // Cancel the timer
    clearTimeout(timerId.value);
}
function displayPopup() {
    showNotification.value = true;

    timerId.value = setTimeout(() => {
        dismissPopup();
    }, 4000);
}
// User pressed the object input
function handleFocusObject() {
    isFocused.value = true;
}
function handleBlur() {
    isFocused.value = false;
}
function handleFocusDestinary() {
    isFocused2.value = true;
}
function handleBlur2(event) {
    // Checks for a valid input email and adds it to the recipients list
    isFocused2.value = false;
    const inputValue = event.target.value.trim().toLowerCase();
    const emailFormat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (inputValue && emailFormat.test(inputValue)) {
        if (!people.find(person => person.email === inputValue)) {
            const newPerson = { username: '', email: inputValue };
            people.push(newPerson);
            selectedPeople.value.push(newPerson);
        }
    } else if (!filteredPeople.value.length && inputValue) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('constants.popUpConstants.errorMessages.invalidEmail');
        notificationMessage.value = t('constants.popUpConstants.errorMessages.emailFormatIncorrect');
        displayPopup();
    }
}

const AIContainer = ref(null);
let stepcontainer = 0;
const objectInput = ref(null);
const mailInput = ref(null);



let counter_display = 0; 

// Quill editor
const quill = ref(null);

// To keep the navbar always at the bottom when new content is added
const scrollableDiv = ref(null);
const scrollToBottom = async () => {
    await nextTick();
    const element = scrollableDiv.value;
    element.scrollTop = element.scrollHeight;
};

// AI instruction textarea input
const textareaValue = ref('');
const textareaValueSave = ref('');

// AI instruction button parameters
const lengthValue = ref('short');
const formalityValue = ref('formal');

// AI instruction to do revision on the mail
const subject = ref('');
const mail = ref('');
const MailCreatedByAI = ref(false); // to check if the AI create the Mail or not

// Loading animation
const isLoading = ref(false);


////////////////////////////////////////////////////// To Handle files upload ///////////////////////////////////////////////////////
const fileInput = ref(null);
let uploadedFiles = ref([]);
let fileObjects = ref([]);
const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25MB, Gmail's limit

const triggerFileInput = () => {
    fileInput.value.click();
};

const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    files.forEach(file => {
        if (file.size <= MAX_FILE_SIZE) {
            let localStorageuploadedFiles = localStorage.getItem("uploadedFiles");

            for (const currentFile of localStorageuploadedFiles) {
                if (currentFile.name == file) {
                    // Show the pop-up
                    backgroundColor = 'bg-red-200/[.89] border border-red-400';
                    notificationTitle = t('constants.popUpConstants.errorMessages.duplicateFile');
                    notificationMessage = t('constants.popUpConstants.errorMessages.fileAlreadyInserted');
                    displayPopup();
                    return;
                }
            }
            uploadedFiles.value.push({ name: file.name, size: file.size });
            fileObjects.value.push(file);
        } else {
            // Show the pop-up
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle = t('constants.popUpConstants.errorMessages.fileTooLarge');
            notificationMessage = t('constants.popUpConstants.errorMessages.fileSizeExceedsLimit');
            displayPopup();
            return;
        }
    });
    saveFileMetadataToLocalStorage();
};

const removeFile = (index) => {
    uploadedFiles.value.splice(index, 1);
    fileObjects.value.splice(index, 1);
    saveFileMetadataToLocalStorage();
};

const saveFileMetadataToLocalStorage = () => {
    localStorage.setItem('uploadedFiles', JSON.stringify(uploadedFiles.value));
};

const loadFileMetadataFromLocalStorage = () => {
    const files = JSON.parse(localStorage.getItem('uploadedFiles')) || [];
    uploadedFiles.value = files;
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// function linked to ENTER key listeners
function handleEnterKey(event) {
    // Allow pressing Enter with Shift to create a line break
    if (event.target.id === 'dynamicTextarea' && event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        handleAIClick();
    }
    else if (isFocused2.value) {
        event.preventDefault();
        handleBlur2(event);
        // the user is still on the input
        handleFocusDestinary();
    }
}

function displayMessage_old(message, ai_icon) {
    // Function to display a message from the AI Assistant

    const messageHTML = `
      <div class="flex pb-12">
        <div class="mr-4 flex">         
          <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              ${ai_icon}
            </svg>
          </span>   
        </div>
        <div>
          <p ref="animatedText${counter_display}"></p>
        </div>
      </div>
    `;
    AIContainer.value.innerHTML += messageHTML;
    const animatedParagraph = document.querySelector(`p[ref="animatedText${counter_display}"]`);
    counter_display += 1;
    animateText(message, animatedParagraph);
    scrollToBottom();
}

function displayMessage(message, ai_icon) {
    // Function to display a message from the AI Assistant

    const messageHTML = `
      <div class="flex pb-12">
        <div class="mr-4 flex">      
            <!--   
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full overflow-hidden">
              <img src="${ai_icon._value}" alt="ai_icon" class="max-w-full max-h-full rounded-full">
            </span>-->
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                ${ai_icon}
                </svg>
            </span> 
        </div>
        <div>
          <p ref="animatedText${counter_display}"></p>
        </div>
      </div>
    `;
    AIContainer.value.innerHTML += messageHTML;
    const animatedParagraph = document.querySelector(`p[ref="animatedText${counter_display}"]`);
    counter_display += 1;
    animateText(message, animatedParagraph);
    scrollToBottom();
}


async function handleAIClick() {

    if (isAIWriting.value) {
        return;
    }
    isAIWriting.value = true;

    // Declare variables outside the fetch scope
    let messageHTML = '';
    let userInput = textareaValue.value;
    let imageURL = require('@/assets/user.png');

    // Fetches the profile image URL from the server
    const requestOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'email': emailSelected.value
        },
    };

    const data = await fetchWithToken(`${API_BASE_URL}user/social_api/get_profile_image/`, requestOptions);

    if (data.profile_image_url) {
        imageURL = data.profile_image_url;
    }

    const profileImageHTML = `
      <img src="${imageURL}" alt="Profile Image" class="h-14 w-14 rounded-full">
    `;

    // Create the complete message HTML with the profile image and text
    messageHTML = `
      <div class="flex pb-12">
        <div class="mr-4 flex">
          <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
            ${profileImageHTML}
          </span>
        </div>
        <div>
          <p class="font-serif">${userInput}</p>
        </div>
      </div>
    `;

    AIContainer.value.innerHTML += messageHTML;
    textareaValueSave.value = textareaValue.value;
    textareaValue.value = '';
    scrollToBottom();

    setTimeout(async () => {
        if (stepcontainer == 0) {
            if (textareaValueSave.value == '') {
                const message = t('constants.sendEmailConstants.noRecipientsEntered');
                const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`
                displayMessage(message, ai_icon);
            } else {
                try {
                    isLoading.value = true;
                    loading();
                    scrollToBottom();
                    const result = await findUser(textareaValueSave.value);

                    hideLoading();
                    
                    let noUsersAdded = true;
                    let WaitforUserChoice = false;
                    if (result.error != "Invalid input or query not about email recipients") { 
                        
                        const main_recipients = userSearchResult.value.main_recipients;
                        const cc_recipients = userSearchResult.value.cc_recipients;
                        const bcc_recipients = userSearchResult.value.bcc_recipients;
                        

                        for (let i = 0; i < main_recipients.length; i++) {
                            const user = main_recipients[i];
                            const emails = user.email;

                            if (emails.length == 1) {
                                const person = { username: user.username, email: emails[0] };
                                selectedPeople.value.push(person);
                                main_recipients.splice(i, 1);
                                noUsersAdded = false;
                                i--;
                            }
                        }

                        for (let i = 0; i < cc_recipients.length; i++) {
                            const user = cc_recipients[i];
                            const emails = user.email;

                            if (emails.length == 1) {
                                const person = { username: user.username, email: emails[0] };
                                selectedCC.value.push(person);
                                delete cc_recipients[i];
                                cc_recipients.splice(i, 1);
                                noUsersAdded = false;
                                i--;
                            }
                        }

                        for (let i = 0; i < bcc_recipients.length; i++) {
                            const user = bcc_recipients[i];
                            const emails = user.email;

                            if (emails.length == 1) {
                                const person = { username: user.username, email: emails[0] };
                                selectedCCI.value.push(person);
                                bcc_recipients.splice(i, 1);
                                noUsersAdded = false;
                                i--;
                            }
                        }

                        // This condition is used to display the diffrent mail possibilities
                        if (main_recipients.length > 0 || cc_recipients.length > 0 || bcc_recipients.length > 0) {

                            


                            const messageHTML = `
                                <div class="flex pb-2">
                                    <div class="mr-4 flex">
                                        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
                                            </svg>
                                        </span>   
                                    </div>
                                    <div>                                        
                                        <p>${t('constants.sendEmailConstants.multipleEmailsFoundForSomeRecipients')}</p>
                                    </div>
                                </div>
                            `;
                            
                            AIContainer.value.innerHTML += messageHTML;

                            if (main_recipients.length > 0) {
                                WaitforUserChoice = true;
                                const emailList = [];

                                for (const user of main_recipients) {
                                    for (const email of user.email) {
                                        if (user.email !== '') {
                                            // Creating an object for each email and pushing it to the emailList array
                                            const emailMapping = {};
                                            emailMapping[user.username] = email;
                                            emailList.push(emailMapping);
                                            noUsersAdded = false;
                                        }
                                    }
                                }
                                console.log("emailList", emailList);
                                askChoiceRecipier(emailList, "main");
                            }
                            if (cc_recipients.length > 0) {
                                WaitforUserChoice = true;
                                const emailList = [];

                                for (const user of cc_recipients) {
                                    for (const email of user.email) {
                                        if (user.email !== '') {
                                            // Creating an object for each email and pushing it to the emailList array
                                            const emailMapping = {};
                                            emailMapping[user.username] = email;
                                            emailList.push(emailMapping);
                                            noUsersAdded = false;
                                        }
                                    }
                                }
                                askChoiceRecipier(emailList, "cc");
                            }
                            if (bcc_recipients.length > 0) {
                                WaitforUserChoice = true;
                                const emailList = [];

                                for (const user of bcc_recipients) {
                                    for (const email of user.email) {
                                        if (user.email !== '') {
                                            // Creating an object for each email and pushing it to the emailList array
                                            const emailMapping = {};
                                            emailMapping[user.username] = email;
                                            emailList.push(emailMapping);
                                            noUsersAdded = false;
                                        }
                                    }
                                }
                                askChoiceRecipier(emailList, "bcc");
                            }
                            // To display the button to go to the next step 
                            NextStepRecipier();
                            scrollToBottom();
                        }

                        if (noUsersAdded) {
                            console.log("DEBUG");
                            const message = t('constants.sendEmailConstants.noRecipientsFoundPleaseTryAgainOrEnterManually');
                            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
                    
                            
                            displayMessage(message, ai_icon);
                        } else if (!WaitforUserChoice) {
                            stepcontainer = 1;
                            askContent();
                        }
                    } else {
                        const message = t('constants.sendEmailConstants.noRecipientsFoundPleaseTryAgainOrEnterManually');
                        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
                 
                        
                        displayMessage(message, ai_icon);
                    }
                } catch (error) {
                    const message = t('constants.sendEmailConstants.processingErrorTryAgain')
                    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
              
                    
                    displayMessage(message, ai_icon);
                    
                }
            }
        } else if (stepcontainer == 1) {
            // if the user enter an empty value
            if (textareaValueSave.value == '') {
                const message = t('constants.sendEmailConstants.noDraftsEnteredPleaseTryAgain');
                const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`
            
                
                displayMessage(message, ai_icon);
            } else {

                console.log('Length:', lengthValue.value, 'Formality:', formalityValue.value);

                try {
                    loading();
                    scrollToBottom();
                    const requestOptions = {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            input_data: textareaValueSave.value,
                            length: lengthValue.value,
                            formality: formalityValue.value,
                        })
                    };

                    const result = await fetchWithToken(`${API_BASE_URL}api/new_email_ai/`, requestOptions);
                    hideLoading();
                    subject.value = result.subject;
                    mail.value = result.mail;
                    console.log(result);
                    if (result.subject && result.mail) {
                        stepcontainer = 2;
                        
                        const formattedMail = result.mail.replace(/\n/g, '<br>');
                        const messageHTML = `
                      <div class="flex pb-12">
                          <div class="mr-4 flex">
                              <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                                </svg>
                              </span>   
                          </div>
                          <div>
                              <p><strong>${t('newPage.subject')}</strong> ${result.subject}</p>
                              <p><strong>${t('newPage.emailContent')}</strong> ${formattedMail}</p>
                          </div>
                      </div>
                  `;
                        AIContainer.value.innerHTML += messageHTML;
                        inputValue.value = result.subject;
                        MailCreatedByAI.value = true;
                        
                        const quillEditorContainer = quill.value.root;
                        let modified_email_body = result.mail.replace(/<\/p>/g, "</p><p></p>");
                        quillEditorContainer.innerHTML = modified_email_body;
                        const message = t('constants.sendEmailConstants.emailFeedbackRequest');
                        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
                        
                        
                        displayMessage_old(message, ai_icon);
                    } else {
                        hideLoading();
                        const message = t('constants.sendEmailConstants.processingErrorTryAgain')
                        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
                       
                        
                        displayMessage(message, ai_icon);
                        console.log('Subject or Email is missing in the response');
                    }
                } catch (error) {
                    hideLoading();
                    const message = t('constants.sendEmailConstants.processingErrorTryAgain')
                    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
                    
                    
                    displayMessage(message, ai_icon);
                    console.error('There was a problem with the fetch operation: ', error);
                }
            }
        } else if (stepcontainer == 2) {
            // if the user enter an empty value
            if (textareaValueSave.value == '') {
                const message = t('constants.sendEmailConstants.noSuggestionsEnteredPleaseTryAgain');
                const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`
               
                
                displayMessage(message, ai_icon);
            } else {
                try {
                    loading();
                    scrollToBottom();

                    const requestOptions = {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            userInput: textareaValueSave.value,
                            length: lengthValue.value,
                            formality: formalityValue.value,
                            subject: inputValue.value,
                            body: mail.value,
                            history: history.value
                        }),
                    };

                    const result = await fetchWithToken(`${API_BASE_URL}api/improve_draft/`, requestOptions);
                    console.log(result);

                    hideLoading();
                    subject.value = result.subject;
                    mail.value = result.email_body;
                    history.value = result.history;
                    console.log(result);
                    if (result.subject && result.email_body) {
                        
                        hideLoading();
                        const formattedMail = result.email_body.replace(/\n/g, '<br>');
                        const messageHTML = `
                      <div class="flex pb-12">
                          <div class="mr-4 flex">
                              <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                                </svg>
                              </span>   
                          </div>
                          <div>
                              <p><strong>${t('newPage.subject')}</strong> ${result.subject}</p>
                              <p><strong>${t('newPage.emailContent')}</strong> ${formattedMail}</p>
                          </div>
                      </div>
                  `;
                        AIContainer.value.innerHTML += messageHTML;
                        inputValue.value = result.subject;
                        const quillEditorContainer = quill.value.root;
                        quillEditorContainer.innerHTML = result.email_body;
                        quillEditorContainer.style.cssText = 'p { margin-bottom: 20px; }';


                        const message = t('constants.sendEmailConstants.betterEmailFeedbackRequest');
                        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
                        
                        
                        displayMessage_old(message, ai_icon);
                    } else {
                        hideLoading();
                        const message = t('constants.sendEmailConstants.processingErrorTryAgain')
                        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
                       
                        
                        displayMessage(message, ai_icon);
                        console.log('Subject or Email is missing in the response');
                    }
                } catch (error) {
                    
                    hideLoading();
                    const message = t('constants.sendEmailConstants.processingErrorTryAgain')
                    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
                    
                    
                    displayMessage(message, ai_icon);
                    
                }
            }
        }
    }, 0);
}
const bgColor = ref(''); 

const userSearchResult = ref(null);

async function findUser(searchQuery) {

    const requestOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    };

    try {
        const data = await fetchWithToken(`${API_BASE_URL}api/find_user_ai/?query=` + encodeURIComponent(searchQuery), requestOptions);
        console.log(data);
        userSearchResult.value = data; // Update the reactive variable
        return data
    } catch (error) {
        console.error("Error fetching user information:", error.message);
    }
}



onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
    localStorage.removeItem("uploadedFiles");

    
    bgColor.value = localStorage.getItem('bgColor');
    
    loadFileMetadataFromLocalStorage(); 
    window.addEventListener('resize', scrollToBottom); // To keep the scroll in the scrollbar at the bottom even when viewport change

    var toolbarOptions = [
        [{ 'font': [] }],
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
        ['bold', 'italic', 'underline'],
        [{ 'color': [] }, { 'background': [] }],
        [{ 'list': 'ordered' }, { 'list': 'bullet' }],
        [{ 'align': [] }],
        ['blockquote', 'code-block']
    ];

    // Initialize Quill editor
    quill.value = new Quill('#editor', {
        theme: 'snow',
        modules: {
            toolbar: toolbarOptions
        }
    });

    

    // DOM-related code
    AIContainer.value = document.getElementById('AIContainer');

    const message = t('constants.sendEmailConstants.emailRecipientRequest');
    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
  
    
    displayMessage(message, ai_icon);
    objectInput.value = document.getElementById('objectInput');

    quill.value.on('text-change', function () {
        mailInput.value = quill.value.root.innerHTML;
        
        
        if (isFirstTimeEmail.value && !MailCreatedByAI.value) {
            const quillContent = quill.value.root.innerHTML;
            if (quillContent.trim() !== '<p><br></p>') {
                mail.value = quillContent;
                handleInputUpdateMailContent(quillContent);
                isFirstTimeEmail.value = false;
            }
        }
        MailCreatedByAI.value = false;
    });

    

    const form = objectInput.value.closest('form');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
        });
    }
});

watch(uploadedFiles, () => {
    saveFileMetadataToLocalStorage();
}, { deep: true });

function animateText(text, target) {
    let characters = text.split("");
    let currentIndex = 0;
    const interval = setInterval(() => {
        if (currentIndex < characters.length) {
            target.textContent += characters[currentIndex];
            currentIndex++;
        } else {
            // AI has finished to write its message
            clearInterval(interval);
            // reset the status
            isAIWriting.value = false;
        }
    }, 30);
}

function personSelected(person) {
    if (!person) return;

    switch (activeType.value) {
        case 'CC':
            if (!selectedCC.value.includes(person)) {
                selectedCC.value.push(person);
            }
            break;
        case 'CCI':
            if (!selectedCCI.value.includes(person)) {
                selectedCCI.value.push(person);
            }
            break;
        default:
            if (!selectedPeople.value.includes(person)) {
                selectedPeople.value.push(person);
                
            }
    }

    if (isFirstTimeDestinary.value) {
        
        stepcontainer = 1;
        askContent(); 
        
        isFirstTimeDestinary.value = false;
    }

    selectedPerson.value = null;
    
}

function toggleCC() {
    activeType.value = activeType.value === 'CC' ? null : 'CC';
}

function toggleCCI() {
    activeType.value = activeType.value === 'CCI' ? null : 'CCI';
}

function removePersonFromMain(personToRemove) {
    selectedPeople.value = selectedPeople.value.filter(person => person !== personToRemove);
}

function removePersonFromCC(personToRemove) {
    selectedCC.value = selectedCC.value.filter(person => person !== personToRemove);
}

function removePersonFromCCI(personToRemove) {
    selectedCCI.value = selectedCCI.value.filter(person => person !== personToRemove);
}





function handleInputUpdateMailContent(newMessage) {

    if (newMessage !== '') {
        if ((selectedPeople.value.length > 0 || selectedCC.value.length > 0 || selectedCCI.value.length > 0)) {

            askContentAdvice();
            stepcontainer = 2;
            

            scrollToBottom(); 
            
        }
    }
}


const happy_icon = ref(require('@/assets/ao-happy.png'));

function askContent() {
    
    const message = t('constants.sendEmailConstants.draftEmailRequest'); 
    
    const ai_icon = happy_icon;
    
    const messageHTML = `
      <div class="pb-12">
        <div class="flex">
            <div class="mr-4">
                <!--
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full overflow-hidden">
                    <img src="${ai_icon._value}" alt="ai_icon" class="max-w-full max-h-full rounded-full">
                </span>-->
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                  </svg>
                </span>
            </div>
            <div>
                <div class="flex flex-col">
                  <p ref="animatedText${counter_display}"></p>
                  </div>
                </div>
            </div>
        </div>
      </div>
    `;


    AIContainer.value.innerHTML += messageHTML;
    const animatedParagraph = document.querySelector(`p[ref="animatedText${counter_display}"]`);
    counter_display += 1;
    animateText(message, animatedParagraph);

    scrollToBottom();
    
}

function askContentAdvice() {
     const message = t('constants.sendEmailConstants.emailCompositionAssistance'); // Older : const message = "Pouvez-vous fournir un brouillon de l'email que vous souhaitez rédiger ?";

     
    const ai_icon = happy_icon;
    const messageHTML = `
      <div class="pb-12">
        <div class="flex">
            <div class="mr-4">
                <!--
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full overflow-hidden">
                    <img src="${ai_icon._value}" alt="ai_icon" class="max-w-full max-h-full rounded-full">
                </span>-->
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
                  </svg>
                </span>
            </div>
            <div>
                <div class="flex flex-col">
                  <p ref="animatedText${counter_display}"></p>
                  <div class="flex mt-4">
                    <div class="mr-4">
                      <button type="button" id="spellCheckButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                        ${t('newPage.correctSpelling')}
                      </button>
                    </div>
                    <div>
                      <button type="button" id="CopyWritingCheckButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                        ${t('newPage.checkCopywriting')}
                      </button>
                    </div>
                  </div>
                  <div class="flex mt-4">
                    <div class="mr-4">
                      <button type="button" id="WriteBetterButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                        ${t('newPage.improveWriting')}
                      </button>
                    </div>
                  </div>
                </div>
            </div>
        </div>
      </div>
    `;
    AIContainer.value.innerHTML += messageHTML;

    // To check the ortgraph of the subject and the mail
    setTimeout(() => {
        const spellCheckButton = document.getElementById('spellCheckButton');
        if (spellCheckButton) {
            spellCheckButton.addEventListener('click', checkSpelling);
        }
    }, 0);

    setTimeout(() => {
        const CopyWritingCheckButton = document.getElementById('CopyWritingCheckButton');
        if (CopyWritingCheckButton) {
            CopyWritingCheckButton.addEventListener('click', checkCopyWriting);
        }
    }, 0);

    setTimeout(() => {
        const WriteBetterButton = document.getElementById('WriteBetterButton');
        if (WriteBetterButton) {
            WriteBetterButton.addEventListener('click', WriteBetter);
        }
    }, 0);

    const animatedParagraph = document.querySelector(`p[ref="animatedText${counter_display}"]`);
    counter_display += 1;
    animateText(message, animatedParagraph);
}

// To display the button for one choice of the recipier for the user
function askChoiceRecipier(list, type) {
    let buttonsHTML = '';

    const firstUsername = Object.keys(list[0])[0];
    // Display the type of recipient
    const userLabel = (type === 'main') ? t('newPage.mainRecipient') : (type === 'cc') ? t('newPage.ccRecipient') : t('newPage.bccRecipient');
    // Display the username before the list of emails
    const usernameHTML = `<div>${t('newPage.forUser')}<strong>${firstUsername}</strong> [${userLabel}]</div>`;

    list.forEach((item, index) => {
        // Extract the first (and presumably only) key in the dictionary, which is the username
        const username = Object.keys(item)[0];
        // Accessing the email using the username key
        const email = item[username];
        // Generating a unique ID for each button based on the index to ensure it's unique
        const buttonLabel = (type === 'main') ? 'main' : (type === 'cc') ? 'cc' : 'bcc';
        const buttonId = `button-${buttonLabel}-${index}`;

        // if index is a even number 
        if (index % 2 === 0) {
            // open the div
            buttonsHTML += '<div class="mr-4">';
        }

        buttonsHTML += `
            <div class="mr-4">
                <button type="button" id="${buttonId}" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                    ${email}
                </button>
            </div>
        `;

        // if index is an odd number or its the last element
        if (index % 2 == 1 || index === list.length - 1) {
            // close the div
            buttonsHTML += '</div>';
        }
    });

    const messageHTML = `
        <div class="flex pb-1 pl-[72px]">
            <div class="flex flex-col">
                ${usernameHTML}
                <br>
                ${buttonsHTML}
            </div>
        </div>
        <br>
    `;

    AIContainer.value.innerHTML += messageHTML;

    list.forEach((item, index) => {
        const buttonLabel = (type === 'main') ? 'main' : (type === 'cc') ? 'cc' : 'bcc';
        const buttonId = `button-${buttonLabel}-${index}`;

        setTimeout(() => {
            const button = document.getElementById(buttonId);

            button.addEventListener('click', () => {
                const username = Object.keys(item)[0];
                const email = item[username];

                if (type === 'main') {
                    const person = { username: username, email: email };
                    const isPersonAlreadySelected = selectedPeople.value.some(p => p.email === person.email);
                    if (!isPersonAlreadySelected) {
                        selectedPeople.value.push(person);
                    }
                } else if (type === 'cc') {
                    const person = { username: username, email: email };
                    const isPersonAlreadySelected = selectedCC.value.some(p => p.email === person.email);
                    if (!isPersonAlreadySelected) {
                        selectedCC.value.push(person);
                    }
                } else {
                    const person = { username: username, email: email };
                    const isPersonAlreadySelected = selectedCCI.value.some(p => p.email === person.email);
                    if (!isPersonAlreadySelected) {
                        selectedCCI.value.push(person);
                    }
                }
            });
        }, 0);
    });
}

function NextStepRecipier() {

    const messageHTML = `
      <div class="flex pb-12 pl-[72px]">
        <div class="flex flex-col">
          <div class="flex mt-4">
            <div class="mr-4">
              <button type="button" id="nextButton" class="flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-gray-900 text-white hover:bg-black border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
                ${t('newPage.moveToNextStep')}
              </button>
          </div>
        </div>
      </div>
    `;

    AIContainer.value.innerHTML += messageHTML;

    setTimeout(() => {
        const nextButton = document.getElementById('nextButton');
        if (nextButton) {
            nextButton.addEventListener('click', () => {
                console.log("DEBUG B4", stepcontainer)
                stepcontainer = 1;
                console.log("DEBUG AFTER click ( Passez à la suite)", stepcontainer)
                askContent();
                console.log("DEBUG AFTER askContent ( Passez à la suite)", stepcontainer)
            });
        }
    }, 0);
}

async function checkSpelling() {
    try {
        loading();
        scrollToBottom();

        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email_subject: inputValue.value,
                email_body: mailInput.value,
            }),
        };

        const result = await fetchWithToken(`${API_BASE_URL}api/correct_email_language/`, requestOptions);

        hideLoading();
        
        // retrieve num of corrections
        console.log(result);
        if (result.corrected_subject && result.corrected_body) {
            
            const formattedMail = result.corrected_body.replace(/\n/g, '<br>');
            const messageHTML = `
              <div class="flex pb-12">
                  <div class="mr-4 flex">
                      <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                        </svg>
                      </span>   
                  </div>
                  <div>
                      <p><strong>${t('newPage.subject')}</strong> ${result.corrected_subject}</p>
                      <p><strong>${t('newPage.emailContent')}</strong> ${formattedMail}</p>
                  </div>
              </div>
          `;
            AIContainer.value.innerHTML += messageHTML;
            inputValue.value = result.corrected_subject;
            const quillEditorContainer = quill.value.root;
            quillEditorContainer.innerHTML = result.corrected_body;

            const message = t('constants.sendEmailConstants.spellingCorrectionRequest');
            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
           
            
            displayMessage(message, ai_icon);
        } else {
            hideLoading();
            const message = t('constants.sendEmailConstants.processingErrorApology')
            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
       
            
            displayMessage(message, ai_icon);
            console.log('Subject or Email is missing in the response');
        }

    } catch (error) {
        
        hideLoading();
        const message = t('constants.sendEmailConstants.processingErrorApology')
        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
      
        
        displayMessage(message, ai_icon);
    }
}

async function checkCopyWriting() {
    try {
        loading();
        scrollToBottom();

        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email_subject: inputValue.value,
                email_body: mailInput.value,
            }),
        };

        const result = await fetchWithToken(`${API_BASE_URL}api/check_email_copywriting/`, requestOptions);

        hideLoading();
        
        // retrieve num of corrections
        console.log(result);
        if (result.feedback_copywriting) {
            
            const formattedCopWritingOutput = result.feedback_copywriting.replace(/\n/g, '<br>');

            const messageHTML = `
              <div class="flex pb-12">
                  <div class="mr-4 flex">
                      <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                        </svg>
                      </span>   
                  </div>
                  <div>
                      <p>${formattedCopWritingOutput}</p>
                  </div>
              </div>
          `;
            AIContainer.value.innerHTML += messageHTML;

            const message = t('constants.sendEmailConstants.copywritingCheckRequest');
            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
          
            
            displayMessage(message, ai_icon);
        } else {
            hideLoading();
            const message = t('constants.sendEmailConstants.processingErrorApology')
            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
        
            
            displayMessage(message, ai_icon);
            console.log('Subject or Email is missing in the response');
        }

    } catch (error) {
        
        hideLoading();
        const message = t('constants.sendEmailConstants.processingErrorApology')
        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
     
        
        displayMessage(message, ai_icon);
    }
}

async function WriteBetter() {
    try {
        loading();
        scrollToBottom();
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                userInput: textareaValueSave.value,
                length: lengthValue.value,
                formality: formalityValue.value,
                subject: inputValue.value,
                body: mail.value,
                history: history.value
            }),
        };

        const result = await fetchWithToken(`${API_BASE_URL}api/improve_draft/`, requestOptions);

        hideLoading();
        console.log(result);
        subject.value = result.subject;
        mail.value = result.email_body;
        history.value = result.history;
        if (result.subject && result.email_body) {
            
            const messageHTML = `
            <div class="flex pb-12">
                <div class="mr-4 flex">
                    <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                      </svg>
                    </span>   
                </div>
                <div>
                    <p><strong>${t('newPage.subject')}</strong> ${result.subject}</p>
                    <p><strong>${t('newPage.emailContent')}</strong> ${result.email_body}</p>
                </div>
            </div>
        `;
            AIContainer.value.innerHTML += messageHTML;
            inputValue.value = result.subject;
            const quillEditorContainer = quill.value.root;
            quillEditorContainer.innerHTML = result.email_body;

            const message = t('constants.sendEmailConstants.betterEmailFeedbackRequest');
            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
           
            
            displayMessage(message, ai_icon);
        } else {
            hideLoading();
            const message = t('constants.sendEmailConstants.processingErrorTryAgain')
            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`

            
            displayMessage(message, ai_icon);
            console.log('Subject or Email is missing in the response');
        }
    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        
        const message = t('constants.sendEmailConstants.processingErrorTryAgain')
        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
       
        
        displayMessage(message, ai_icon);
        console.error('There was a problem with the fetch operation: ', error);
    }
}

function loading() {
    // Use `nbr` in the template literal to set the reference dynamically
    const messageHTML = `
      <div id="dynamicLoadingIndicator" class="pb-12">
        <div class="flex">
            <div class="mr-4">
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900">
                    <span class="text-lg font-medium leading-none text-white">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15a4.5 4.5 0 0 0 4.5 4.5H18a3.75 3.75 0 0 0 1.332-7.257 3 3 0 0 0-3.758-3.848 5.25 5.25 0 0 0-10.233 2.33A4.502 4.502 0 0 0 2.25 15Z" />
                      </svg>
                    </span>
                </span>
            </div>
            <div>
              <div class="loading-spinner"></div>
            </div>
        </div>
      </div>
    `;

    AIContainer.value.innerHTML += messageHTML;
}

function hideLoading() {
    const loadingElement = document.getElementById('dynamicLoadingIndicator');
    if (loadingElement) {
        loadingElement.remove();
    }
}


async function scheduleSend() {
    const emailSubject = inputValue.value;
    const emailBody = quill.value.root.innerHTML;

    for (const tupleEmail of emailsLinked.value) {
        if (emailSelected.value === tupleEmail.email && tupleEmail.type_api !== MICROSOFT) {
            // Show the pop-up
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle.value = 'Email service provider not supported';
            notificationMessage.value = 'Scheduled send is only available for Outlook accounts';
            displayPopup();
            return;
        }
    }

    if (!emailSubject.trim()) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('constants.popUpConstants.errorMessages.emailSendError');
        notificationMessage.value = t('constants.popUpConstants.errorMessages.emailSendErrorNoSubject');
        displayPopup();
        return;
    } else if (emailBody == "<p><br></p>") {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('constants.popUpConstants.errorMessages.emailSendError');
        notificationMessage.value = t('constants.popUpConstants.errorMessages.emailSendErrorNoObject');
        displayPopup();
        return;
    } else if (selectedPeople.value.length == 0) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('constants.popUpConstants.errorMessages.emailSendError');
        notificationMessage.value = t('constants.popUpConstants.errorMessages.emailSendErrorNoRecipient');
        displayPopup();
        return;
    }

    const formData = new FormData();

    formData.append('subject', emailSubject);
    formData.append('message', emailBody);
    fileObjects.value.forEach(file => formData.append('attachments', file));

    // Add recipients to formData
    selectedPeople.value.forEach(person => formData.append('to', person.email));

    // Add CC recipients to formData
    if (selectedCC.value.length > 0) {
        selectedCC.value.forEach(person => formData.append('cc', person.email));
    }
    // Add BCC recipients to formData
    if (selectedCCI.value.length > 0) {
        selectedCCI.value.forEach(person => formData.append('cci', person.email));
    }
    formData.append('email', emailSelected.value);
    // update here with the date and time provided by the user
    formData.append('datetime', "2024-07-02T10:00:00Z");

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/social_api/send_schedule_email/`, {
            method: 'POST',
            body: formData
        });

        if (response.message === 'Email scheduled successfully!') {
            // Show the pop-up
            backgroundColor = 'bg-green-200/[.89] border border-green-400';
            notificationTitle = 'Email scheduled successfully!';
            notificationMessage = 'Your email will be send on time';
            displayPopup();

            // Other logic
            inputValue.value = '';
            quill.value.root.innerHTML = '';
            selectedPeople.value = [];
            selectedCC.value = [];
            selectedCCI.value = [];
            stepcontainer = 0;
            AIContainer.value.innerHTML = '';
            AIContainer.value = document.getElementById('AIContainer');

            localStorage.removeItem("uploadedFiles");
            uploadedFiles.value = [];
            fileObjects.value = [];

            const message = t('constants.sendEmailConstants.emailRecipientRequest');
            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
           
            
            displayMessage(message, ai_icon);
        } else {
            // Show the pop-up
            notificationMessage.value = response.error;
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle.value = t('constants.popUpConstants.errorMessages.emailSendError');
            displayPopup();
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('constants.popUpConstants.errorMessages.emailSendError');
        notificationMessage.value = error.message;
        displayPopup();
    }
}


async function sendEmail() {
    const emailSubject = inputValue.value;
    const emailBody = quill.value.root.innerHTML;

    if (!emailSubject.trim()) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('constants.popUpConstants.errorMessages.emailSendError');
        notificationMessage.value = t('constants.popUpConstants.errorMessages.emailSendErrorNoSubject');
        displayPopup();
        return;
    } else if (emailBody == "<p><br></p>") {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('constants.popUpConstants.errorMessages.emailSendError');
        notificationMessage.value = t('constants.popUpConstants.errorMessages.emailSendErrorNoObject');
        displayPopup();
        return;
    } else if (selectedPeople.value.length == 0) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('constants.popUpConstants.errorMessages.emailSendError');
        notificationMessage.value = t('constants.popUpConstants.errorMessages.emailSendErrorNoRecipient');
        displayPopup();
        return;
    }

    const formData = new FormData();

    formData.append('subject', emailSubject);
    formData.append('message', emailBody);
    fileObjects.value.forEach(file => formData.append('attachments', file));

    // Add recipients to formData
    selectedPeople.value.forEach(person => formData.append('to', person.email));

    // Add CC recipients to formData
    if (selectedCC.value.length > 0) {
        selectedCC.value.forEach(person => formData.append('cc', person.email));
    }
    // Add BCC recipients to formData
    if (selectedCCI.value.length > 0) {
        selectedCCI.value.forEach(person => formData.append('cci', person.email));
    }
    formData.append('email', emailSelected.value);

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/social_api/send_email/`, {
            method: 'POST',
            body: formData
        });

        if (response.message === 'Email sent successfully!') {
            // Show the pop-up
            backgroundColor = 'bg-green-200/[.89] border border-green-400';
            notificationTitle = t('constants.popUpConstants.successMessages.success');
            notificationMessage = t('constants.popUpConstants.successMessages.emailSuccessfullySent');
            displayPopup();

            // Other logic
            inputValue.value = '';
            quill.value.root.innerHTML = '';
            selectedPeople.value = [];
            selectedCC.value = [];
            selectedCCI.value = [];
            stepcontainer = 0;
            AIContainer.value.innerHTML = '';
            AIContainer.value = document.getElementById('AIContainer');

            localStorage.removeItem("uploadedFiles");
            uploadedFiles.value = [];
            fileObjects.value = [];

            const message = t('constants.sendEmailConstants.emailRecipientRequest');
            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
          
            
            displayMessage(message, ai_icon);
        } else {
            // Show the pop-up
            notificationMessage.value = response.error;
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle.value = t('constants.popUpConstants.errorMessages.emailSendError');
            displayPopup();
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('constants.popUpConstants.errorMessages.emailSendError');
        notificationMessage.value = error.message;
        displayPopup();
    }
}

function handleKeyDown(event) {

    if (event.key == 'Tab') {
        event.preventDefault();

        if (document.getElementById('editor').contains(document.activeElement)) {
            return;
        } else if (selectedCCI.value.length == 0 && selectedCC.value.length == 0 && selectedPeople.value.length == 0 && document.activeElement.id != 'recipients') {
            activeType.value = null;
            document.getElementById('recipients').focus();
        } else if (inputValue.value == '' && isFocused.value == false) {
            document.getElementById('objectInput').focus();
        } else if (quill.value.root.innerHTML == '<p><br></p>') {
            quill.value.focus();
        } else {
            // Logic to rotate
            if (document.activeElement.id === 'recipients') {
                document.getElementById('objectInput').focus();
            } else if (document.activeElement.id === 'dynamicTextarea') {
                document.getElementById('recipients').focus();
            } else {
                document.getElementById('dynamicTextarea').focus();
            }
        }
    } else if (event.ctrlKey) {
        switch (event.key) {
            case 'b':
                quill.value.focus();
                event.preventDefault();
                break;
            case 'd':
                document.getElementById('recipients').focus();
                event.preventDefault();
                break;
            case 'k':
                document.getElementById('dynamicTextarea').focus();
                event.preventDefault();
                break;
            case 'o':
                document.getElementById('objectInput').focus();
                event.preventDefault();
                break;
            case 'Enter':
                sendEmail();
                break;
        }
    }
}
</script>

<script>
import NavBarLarge from '@/components/NavBarLarge.vue';
import NavBarSmall from '@/components/NavBarSmall.vue';
import {
    UserGroupIcon,
    Bars2Icon,
    
    ChevronDownIcon
} from '@heroicons/vue/24/outline'

import {
    PaperAirplaneIcon
} from '@heroicons/vue/24/solid'
import { fetchWithToken } from '@/global/security';


export default {
    components: {
        Navbar,
        Navbar2,
        UserGroupIcon,
        Bars2Icon,
        ChevronDownIcon,
        PaperAirplaneIcon
        
    },
    methods: {
        adjustHeight(event) {
            const textarea = event.target;
            const maxHeight = 250; // Set your desired max height in pixels. TO SET DEPENDING OF THE SIZE OF THE VIEWPORT

            // Reset height to auto to correctly calculate the new scrollHeight
            textarea.style.height = 'auto';

            if (textarea.scrollHeight > maxHeight) {
                textarea.style.height = maxHeight + 'px';
                textarea.style.overflowY = 'auto'; // Enable scrolling when content exceeds maxHeight.
            } else {
                textarea.style.height = textarea.scrollHeight + 'px';
                textarea.style.overflowY = 'hidden'; // Hide the scrollbar when content is below maxHeight.
            }
        },
    }
}
</script>


<!-- TODO: FOLLOW these guidelines anyway
the import of constants and function are correct. You must do the following operations:

create functions: displaySuccessPopUp & displayErrorPpUp instead of hardcodin everywhere
if possible put everything under script setup if its more optimal and easier to manage
remove all comments (unless those who mentionned Théo & Jean) you DELETE the rest no execption
optimize the code
use strictly camelCase
we are using TypeScript so migrate everything where its needed using interfaces or types -->