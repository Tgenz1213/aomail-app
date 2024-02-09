<template>
  <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
    :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" />
  <div class="flex flex-col justify-center items-center h-screen" :class="bgColor">
    <div class="grid grid-cols-12 2xl:grid-cols-7 gap-8 2xl:gap-6">
      <div class="col-span-1 2xl:col-span-1">
        <div class="2xl:hidden h-full">
          <navbar></navbar>
        </div>
        <div class="hidden 2xl:block h-full">
          <navbar2></navbar2>
        </div>
      </div>
      <div class="col-span-11 2xl:col-span-6 xl:h-[93vh] xl:w-[86vw] 2xl:h-[825px] 2xl:w-[1450px]">
        <div class="flex gap-4 w-full h-full">
          <div id="firstMainColumn"
            class="flex-grow bg-gray-100 bg-opacity-75 rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg h-full xl:w-[43vw] 2xl:w-[700px]">
            <!--xl:h-[750px] xl:w-[625px] => 26/12/2023 DATA SAVE : xl:h-[95vh] xl:w-[43vw] 2xl:h-[825px] 2xl:w-[700px] -->
            <div
              class="flex items-center justify-center h-[65px] 2xl:h-[75px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-400 bg-opacity-10">
              <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
              <div class="flex gap-x-2 items-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                  stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
                </svg>
                <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">Assistant IA</h1>
              </div>
            </div>
            <div class="flex flex-col divide-y xl:h-[85vh] 2xl:h-[755px]">
              <div class="overflow-y-auto xl:h-[75vh] 2xl:h-[700px]" style="margin-right: 2px;" ref="scrollableDiv">
                <div class="px-10 py-6">
                  <div class="flex-grow">
                    <div id="AIContainer">
                    </div>
                  </div>
                </div>
              </div>
              <div class="flex-grow">
                <div class="flex px-6 2xl:py-8 pb-6 pt-4 relative w-full"><!-- Old value (26/12/2023) -->
                  <div class="flex flex-grow items-stretch">
                    <textarea id="dynamicTextarea" @keydown.enter="handleEnterKey" @input="adjustHeight"
                      v-model="textareaValue"
                      class="overflow-y-hidden left-0 pl-3 only:block w-full rounded-none rounded-l-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                      placeholder="Instruction"></textarea>
                  </div>
                  <button type="button" @click="handleAIClick"
                    class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-r-md px-3 py-2.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 bg-gray-50 hover:bg-gray-50 z-50">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="rgb(243 244 246)" class="w-6 h-6 text-gray-400">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div id="secondMainColumn"
            class="flex-grow bg-white rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg h-full xl:w-[43vw] 2xl:w-[700px]">
            <!--xl:h-[695px] xl:w-[560px]-->
            <div class="flex flex-col divide-y divide-gray-200 h-full w-full">
              <div
                class="flex items-center justify-center h-[65px] 2xl:h-[75px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-50">
                <div class="flex gap-x-2 items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                    stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672ZM12 2.25V4.5m5.834.166-1.591 1.591M20.25 10.5H18M7.757 14.743l-1.59 1.59M6 10.5H3.75m4.007-4.243-1.59-1.59" />
                  </svg>
                  <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">Saisie manuelle</h1>
                </div>
              </div>
              <form class="flex flex-grow w-full px-10">
                <div class="flex flex-col space-y-6 h-full w-full">
                  <div class="pt-8">
                    <div class="flex flex-wrap">
                      <!-- Main Recipients List -->
                      <div v-if="selectedPeople.length > 0" class="flex items-center mb-1">
                        <div v-for="person in selectedPeople" :key="person.email"
                          class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1">
                          {{ person.username }}
                          <button @click="removePersonFromMain(person)">×</button>
                        </div>
                      </div>
                      <!-- CC Recipients List -->
                      <div v-if="selectedCC.length > 0" class="flex items-center mb-1">
                        <div v-for="person in selectedCC" :key="person.email"
                          class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1">
                          <span class="font-semibold mr-1">CC:</span>
                          {{ person.username }}
                          <button @click="removePersonFromCC(person)">×</button>
                        </div>
                      </div>
                      <!-- CCI Recipients List -->
                      <div v-if="selectedCCI.length > 0" class="flex items-center mb-1">
                        <div v-for="person in selectedCCI" :key="person.email"
                          class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1">
                          <span class="font-semibold mr-1">CCI:</span>
                          {{ person.username }}
                          <button @click="removePersonFromCCI(person)">×</button>
                        </div>
                      </div>
                    </div>
                    <div class="flex items-stretch gap-1">
                      <div class="flex-grow">
                        <div class="relative items-stretch">
                          <div class="relative w-full">
                            <div v-if="!isFocused2 && !hasValueEverBeenEntered"
                              class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2">
                              <UserGroupIcon class="w-4 h-4 pointer-events-none" />
                              <label for="email"
                                class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none">Destinataire(s)</label>
                            </div>
                            <Combobox as="div" v-model="selectedPerson" @update:model-value="personSelected"
                              @blur="handleBlur2">
                              <ComboboxInput
                                class="w-full h-10 rounded-md border-0 bg-white py-2 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                                @change="query = $event.target.value" :display-value="(person) => person?.name"
                                @focus="handleFocusDestinary" @blur="handleBlur2($event)"
                                @keydown.enter="handleEnterKey" />

                              <ComboboxButton
                                class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
                                <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                              </ComboboxButton>

                              <!-- List possible email according to current input -->
                              <ComboboxOptions v-if="filteredPeople.length > 0 && filteredPeople.length <= 10"
                                class="absolute z-20 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                                <ComboboxOption v-for="person in filteredPeople.slice(0, 10)" :key="person.email"
                                  :value="person" as="template" v-slot="{ active, selected }">
                                  <li
                                    :class="['relative cursor-default select-none py-2 pl-3 pr-9', active ? 'bg-gray-500 text-white' : 'text-gray-900']">
                                    <div class="flex">
                                      <span :class="['truncate', selected && 'font-semibold']">{{ person.name }}</span>
                                      <span
                                        :class="['ml-2 truncate text-gray-500', active ? 'text-white' : 'text-gray-500']">{{
                                          person.email }}</span>
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
                        <!--<div class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 w-full max-w-2xl">
                                        <input type="text" name="username" id="userInput" autocomplete="username" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="janesmith">   
                                    </div>-->
                      </div>
                      <div class="flex gap-1">
                        <button type="button" @click="toggleCC"
                          :class="['inline-flex items-center gap-x-1.5 rounded-md px-2.5 py-1.5 text-sm font-semibold hover:bg-gray-600 hover:text-white', activeType === 'CC' ? 'bg-gray-500 text-white' : 'bg-gray-100 text-gray-400']"
                          class="ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">
                          CC
                        </button>

                        <!-- CCI Button -->
                        <button type="button" @click="toggleCCI"
                          :class="['inline-flex items-center gap-x-1.5 rounded-md px-2.5 py-1.5 text-sm font-semibold hover:bg-gray-600 hover:text-white', activeType === 'CCI' ? 'bg-gray-500 text-white' : 'bg-gray-100 text-gray-400']"
                          class="ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">
                          CCI
                        </button>
                      </div>
                    </div>
                  </div>
                  <div class="">
                    <div class="flex flex-wrap">
                      <div v-for="(file, index) in uploadedFiles" :key="index"
                        class="flex items-center mb-1 mr-1 bg-gray-200 rounded px-2 py-1">
                        {{ file.name }}
                        <button @click="removeFile(index)">×</button>
                      </div>
                    </div>
                    <div class="flex items-stretch gap-1">
                      <div class="flex-grow">
                        <div
                          class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 w-full">
                          <div class="relative w-full">
                            <div v-if="!isFocused && !inputValue"
                              class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 z-10">
                              <Bars2Icon class="w-4 h-4 pointer-events-none" />
                              <label for="username"
                                class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none">Objet</label>
                            </div>
                            <!--<input type="text" name="username" id="objectInput" autocomplete="username" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="janesmith">-->
                            <input id="objectInput" v-model="inputValue" type="text"
                              class="block h-10 flex-1 border-0 bg-transparent py-2 pl-3 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6 w-full z-20 relative"
                              @focus="handleFocusObject" @blur="handleBlur" @input="handleInputUpdateObject" />
                          </div>
                        </div>
                      </div>
                      <div class="flex">
                        <input type="file" ref="fileInput" @change="handleFileUpload" multiple hidden>
                        <button @click="triggerFileInput" type="button"
                          class="inline-flex items-center gap-x-1.5 rounded-md bg-gray-100 px-2.5 py-1.5 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-300 shadow-sm hover:ring-transparent hover:bg-gray-600 hover:text-white  focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                              d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                  <!--
                            <div class="col-span-full">
                            <label for="cover-photo" class="block text-sm font-medium leading-6 text-gray-900">Pièce jointes</label>
                                <div class="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-2">
                                <div class="text-center">
                                    <svg class="mx-auto h-8 w-12 text-gray-300" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                                    <path fill-rule="evenodd" d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z" clip-rule="evenodd" />
                                    </svg>
                                    <div class="mt-1 flex text-sm leading-6 text-gray-600">
                                    <label for="file-upload" class="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500">
                                        <span>Upload a file</span>
                                        <input id="file-upload" name="file-upload" type="file" class="sr-only">
                                    </label>
                                    <p class="pl-1">or drag and drop</p>
                                    </div>
                                </div>
                                </div>
                            </div>-->
                  <div class="flex flex-col flex-grow">
                    <!--<div class="flex space-x-1 items-center">
                                <Bars3BottomLeftIcon class="w-4 h-4" />
                                <label for="username" class="block text-sm font-medium leading-6 text-gray-900">Message</label>
                                </div>-->
                    <div class="flex-grow mb-20 h-[200px]">
                      <div id="editor" class="w-full"></div>
                      <!-- TO DEBUG : Overflow Error => 26/12/2023 => FIXED BUT TO CHECK IN DIFFERENT WINDOWS SIZE -->
                    </div>
                    <div class="flex mb-4">
                      <div class="inline-flex rounded-lg shadow-lg">
                        <button @click="sendEmail"
                          class="bg-gray-600 rounded-l-lg px-6 py-1 text-md font-semibold text-white hover:bg-gray-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600">Envoyer</button>
                        <Menu as="div" class="relative -ml-px block">
                          <MenuButton
                            class="relative inline-flex items-center rounded-r-lg  px-2 py-2 text-white border-l border-gray-300 bg-gray-600 hover:bg-gray-700 focus:z-10">
                            <!-- OLD : bg-gray-500 and hover:bg-gray-600 -->
                            <span class="sr-only">Open options</span>
                            <ChevronDownIcon class="h-8 w-5" aria-hidden="true" />
                          </MenuButton>
                          <transition enter-active-class="transition ease-out duration-100"
                            enter-from-class="transform opacity-0 scale-95"
                            enter-to-class="transform opacity-100 scale-100"
                            leave-active-class="transition ease-in duration-75"
                            leave-from-class="transform opacity-100 scale-100"
                            leave-to-class="transform opacity-0 scale-95">
                            <MenuItems
                              class="absolute right-0 z-10 -mr-1 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                              <div class="py-1">
                                <MenuItem v-for="item in items" :key="item.name" v-slot="{ active }">
                                <a :href="item.href"
                                  :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']">{{
                                    item.name }}</a>
                                </MenuItem>
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
    </div>
  </div>
  <!--
  <div class="pb-1 lg:pl-20 bg-gray-100">
      <div class="grid grid-cols-8 gap-6 h-72 items-center divide-x-8 divide-indigo-900 bg-blue-400">
          <div class="col-span-3 h-full bg-red-500">
                  
                  <div class="flex">
                      <div class="flex-shrink-0 self-center">
                          <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-indigo-800">
                              <span class="text-lg font-medium leading-none text-white">AO</span>
                          </span>
                      </div>
                      <div>
                          <p class="mt-1" id="animated-text" ref="animatedText"></p>
                      </div>
                  </div>
              </div>
          <div class="col-span-5 h-full bg-red-500">
              <p>Test</p>
          </div>
      </div>
  </div>-->
</template>

<script setup>
import { defineProps, defineEmits, computed, ref, onMounted, nextTick } from 'vue';
import { watch } from 'vue';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue';
import ShowNotification from '../components/ShowNotification.vue';
//import { ChevronDownIcon, XMarkIcon } from '@heroicons/vue/20/solid';
import { fetchWithToken } from '../router/index.js';
import Quill from 'quill';
import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
} from '@headlessui/vue'


// variables to display a notification
let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');

const items = [
  { name: 'Envoyer à une heure', href: '#' },
]

// lists of different types of recipients
const people = [];

const requestOptions = {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
  },
};

// request to update the list of contacts (people array)
fetchWithToken('http://localhost:9000/MailAssistant/user/contacts/', requestOptions)
  .then(response => people.push(...response))
  .catch(error => console.error("Error fetching contacts:", error));

const selectedPeople = ref([]);
const selectedCC = ref([]);
const selectedCCI = ref([]);
const activeType = ref(null);  // null, 'CC', or 'CCI'

const query = ref('')
const getFilteredPeople = (query, people) => {
  return computed(() =>
    query.value === ''
      ? people
      : people.filter((person) => {
        // Check if either the username or the email includes the query
        return person.username.toLowerCase().includes(query.value.toLowerCase()) ||
          person.email.toLowerCase().includes(query.value.toLowerCase());
      })
  );
};

const filteredPeople = getFilteredPeople(query, people);
const props = defineProps(['modelValue']);
const emit = defineEmits(['update:selectedPerson']);
const selectedPerson = ref(props.modelValue);

watch(selectedPerson, (newValue) => {
  // console.log(selectedPerson.value);
  hasValueEverBeenEntered.value = true; // to make the icon disappear
  /*if (selectedPerson.value && selectedPerson.value.username) {
      //handleInputUpdate(selectedPerson.value.username);
  }  */
  emit('update:selectedPerson', newValue);
});

const inputValue = ref('');
const isFirstTimeDestinary = ref(true); // to detect first letter object input
const isFirstTimeEmail = ref(true); // to detect first letter email content input
const isFocused = ref(false);
const isFocused2 = ref(false);
const hasValueEverBeenEntered = ref(false);


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
  const inputValue = event.target.value.trim();
  const emailFormat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (inputValue && emailFormat.test(inputValue)) {
    console.log("test debug ==>");
    // Add the input email to the list of recipients
    // TODO: ask if we save it in DB or if we wait till the email is sent
    if (!people.find(person => person.email === inputValue)) {
      const newPerson = { name: inputValue, email: inputValue };
      people.push(newPerson);
      selectedPeople.value.push(newPerson);
      // remove the pop up
      showNotification = false;
    }
  } else if (filteredPeople._value.length == 0) {
    // Show the pop-up
    showNotification = true;
    backgroundColor = 'bg-red-300';
    notificationTitle.value = 'Email invalide';
    notificationMessage.value = 'Le format de l\'email est incorrect'
  }
}

const AIContainer = ref(null);
let stepcontainer = 0;
const objectInput = ref(null);
const mailInput = ref(null);

let counter_display = 0; // to create the animation of the text displayed

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
const uploadedFiles = ref([]);
const fileObjects = ref([]);
const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25MB, Gmail's limit

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileUpload = (event) => {
  const files = Array.from(event.target.files);
  files.forEach(file => {
    if (file.size <= MAX_FILE_SIZE) {
      uploadedFiles.value.push({ name: file.name, size: file.size });
      fileObjects.value.push(file);
    } else {
      alert("File size exceeds Gmail's limit");
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
  // works but if ENTER is pressed again it removes a user from the destinary list
  /*else if (isFocused2.value) {
    console.log("aie");
    handleBlur2(event);
  }
  */
}

function displayMessage(message, ai_icon) {
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

const handleAIClick = async () => {

  // Declare variables outside the fetch scope
  let messageHTML = '';
  let userInput = textareaValue.value;

  // Fetches the profile image URL from the server
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'email': localStorage.getItem('email')
    },
  };

  const data = await fetchWithToken('http://localhost:9000/MailAssistant/api/get_profile_image/', requestOptions);
  let imageURL = data.profile_image_url || require('@/assets/user.png');
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
        <p class="font-serif" >${userInput}</p>
      </div>
    </div>
  `;
  AIContainer.value.innerHTML += messageHTML;
  textareaValueSave.value = textareaValue.value;
  textareaValue.value = '';

  setTimeout(async () => {
    if (stepcontainer == 0) {
      if (textareaValueSave.value == '') {
        const message = "Vous n'avez saisi aucun destinataire(s), veuillez réessayer"
        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`
        displayMessage(message, ai_icon);
      } else {
        try {
          isLoading.value = true;
          loading();
          const result = await findUser(textareaValueSave.value);
          hideLoading();
          //textareaValue.value = ''; // TO REINIT => CREATE A WASTE OF TIME => DO NOT USE BUT KEEP IF NEEDED
          let noUsersAdded = true;
          let WaitforUserChoice = false;
          if (result !== "Invalid input or query not about email recipients") { // To update to handle the main error

            const main_recipients = userSearchResult.value.main_recipients;
            const cc_recipients = userSearchResult.value.cc_recipients;
            const bcc_recipients = userSearchResult.value.bcc_recipients;
            console.log("debug", main_recipients, cc_recipients, bcc_recipients);

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

              /* The animation does not work => TO FIX
              const message = "J'ai trouvé plusieurs mails pour certains destinataires, sélectionez les mails qui correspondent";
              const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />`
              await displayMessage(message, ai_icon);*/

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
                            <p>J'ai trouvé plusieurs mails pour certains destinataires, sélectionez les mails qui correspondent</p>
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

            }

            if (noUsersAdded) {
              console.log("DEBUG");
              const message = "Je n'ai pas trouvé de destinataires, veuillez réessayer ou saisir manuellement";
              const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
              displayMessage(message, ai_icon);
            } else if (!WaitforUserChoice) {
              stepcontainer = 1;
              askContent();
            }
          } else {
            console.log("No matching emails found.");
          }
        } catch (error) {
          console.error("Error finding user:", error.message);
        }
      }
    } else if (stepcontainer == 1) {
      // if the user enter an empty value
      if (textareaValueSave.value == '') {
        const message = "Vous n'avez saisi aucun brouillon, veuillez réessayer";
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
              'Content-Type': 'application/json',
              'email': localStorage.getItem('email')
            },
            body: JSON.stringify({
              input_data: textareaValueSave.value,
              length: lengthValue.value,
              formality: formalityValue.value,
            })
          };

          const result = await fetchWithToken('http://localhost:9000/MailAssistant/api/new_email_ai/', requestOptions);
          hideLoading();
          subject.value = result.subject;
          mail.value = result.mail;
          console.log(result);
          if (result.subject && result.mail) {
            stepcontainer = 2;
            // TO FINISH => animation
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
                            <p><strong>Objet:</strong> ${result.subject}</p>
                            <p><strong>Email:</strong> ${formattedMail}</p>
                        </div>
                    </div>
                `;
            AIContainer.value.innerHTML += messageHTML;
            inputValue.value = result.subject;
            MailCreatedByAI.value = true;
            //quill.value.clipboard.dangerouslyPasteHTML(formattedMail); OLD WAY : works but impossible to manuallty delete on quill
            //const delta = quill.value.clipboard.convert(formattedMail); OLD 2
            //console.log(delta); // Check the structure of the delta OLD 2
            const quillEditorContainer = quill.value.root;
            let modified_email_body = result.mail.replace(/<\/p>/g, "</p><p></p>");
            quillEditorContainer.innerHTML = modified_email_body;
            //quill.value.update();

            // TO FINISH => create button with new options to reformat quickly the email written (more short, more formal, more strict)
            const message = "Est-ce que ce mail vous convient ? Vous pouvez me fournir des indications pour que je l'adapte à vos besoins";
            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
            displayMessage(message, ai_icon);
          } else {
            hideLoading();
            const message = "Je m'excuse, j'ai fait une erreur de traitement. Est-ce que vous pouvez réessayer ?"
            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
            displayMessage(message, ai_icon);
            console.log('Subject or Email is missing in the response');
          }
        } catch (error) {
          hideLoading();
          const message = "Je m'excuse, j'ai fait une erreur de traitement. Est-ce que vous pouvez réessayer ?"
          const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
          displayMessage(message, ai_icon);
          console.error('There was a problem with the fetch operation: ', error);
        }
      }
    } else if (stepcontainer == 2) {
      // if the user enter an empty value
      if (textareaValueSave.value == '') {
        const message = "Vous n'avez saisi aucune suggestion, veuillez réessayer.";
        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`
        displayMessage(message, ai_icon);
      } else {
        try {
          loading();
          scrollToBottom();

          const requestOptions = {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'email': localStorage.getItem('email')
            },
            body: JSON.stringify({
              mail_content: mail.value,
              user_recommendation: textareaValueSave.value,
              email_subject: inputValue.value,
            }),
          };

          const result = await fetchWithToken('http://localhost:9000/MailAssistant/api/new_email_recommendations/', requestOptions);

          hideLoading();
          subject.value = result.subject;
          mail.value = result.email_body;
          console.log(result);
          if (result.subject && result.email_body) {
            // TO FINISH => animation
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
                            <p><strong>Objet:</strong> ${result.subject}</p>
                            <p><strong>Email:</strong> ${formattedMail}</p>
                        </div>
                    </div>
                `;
            AIContainer.value.innerHTML += messageHTML;
            inputValue.value = result.subject;
            const quillEditorContainer = quill.value.root;
            quillEditorContainer.innerHTML = result.email_body;
            quillEditorContainer.style.cssText = 'p { margin-bottom: 20px; }';


            // TO FINISH => create button with new options to reformat quickly the email written (more short, more formal, more strict)
            const message = "Est-ce que ce mail vous convient mieux ?";
            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
            displayMessage(message, ai_icon);
          } else {
            hideLoading();
            const message = "Je m'excuse, j'ai fait une erreur de traitement. Est-ce que vous pouvez réessayer ?"
            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
            displayMessage(message, ai_icon);
            console.log('Subject or Email is missing in the response');
          }
        } catch (error) {
          console.error('Error:', error);
          hideLoading();
          const message = "Je m'excuse, j'ai fait une erreur de traitement. Est-ce que vous pouvez réessayer ?"
          const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
          displayMessage(message, ai_icon);
          console.error('There was a problem with the fetch operation: ', error);
        }
      }
    }
  }, 400);
};
const bgColor = ref(''); // Initialize a reactive variable

/* DOES NOT WORK => TO CHECK */
const userSearchResult = ref(null);

async function findUser(searchQuery) {

  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'email': localStorage.getItem('email')
    },
  };

  try {
    const data = await fetchWithToken('http://localhost:9000/MailAssistant/api/find-user-ai/?query=' + encodeURIComponent(searchQuery), requestOptions);
    console.log(data);
    userSearchResult.value = data; // Update the reactive variable
  } catch (error) {
    console.error("Error fetching user information:", error.message);
  }
}

/*
function levenshteinDistance(a, b) {
const matrix = [];

for (let i = 0; i <= b.length; i++) {
  matrix[i] = [i];
}

for (let j = 0; j <= a.length; j++) {
  matrix[0][j] = j;
}

for (let i = 1; i <= b.length; i++) {
  for (let j = 1; j <= a.length; j++) {
    if (b.charAt(i - 1) === a.charAt(j - 1)) {
      matrix[i][j] = matrix[i - 1][j - 1];
    } else {
      matrix[i][j] = Math.min(matrix[i - 1][j - 1] + 1, Math.min(matrix[i][j - 1] + 1, matrix[i - 1][j] + 1));
    }
  }
}

return matrix[b.length][a.length];
}

function transformUsersDict(usersDict) {
return Object.entries(usersDict).map(([email, username]) => ({
  email: email,
  username: username || email 
}));
}

function findUser(userInput, usersDict) {
const usersList = transformUsersDict(usersDict);
console.log("userInput", userInput);
console.log("usersList", usersList);
let bestMatch = null;
let lowestDistance = Infinity;

for (const user of usersList) {
  let emailDistance = levenshteinDistance(userInput.toLowerCase(), user.email.toLowerCase());
  let usernameDistance = levenshteinDistance(userInput.toLowerCase(), user.username.toLowerCase());

  if (emailDistance < lowestDistance) {
    lowestDistance = emailDistance;
    bestMatch = user;
  }

  if (usernameDistance < lowestDistance) {
    lowestDistance = usernameDistance;
    bestMatch = user;
  }
}

return bestMatch ? { email: bestMatch.email, username: bestMatch.username } : "No matching user found";
}

const emailSenders = ref(null);

function fetchEmailSenders() {
fetch('http://localhost:9000/MailAssistant/api/get_unique_email_senders', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
    'Content-Type': 'application/json'
  }
})
.then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
})
.then(data => {
  console.log("email senders", data);
  emailSenders.value = data;
})
.catch(error => {
  console.error('Error fetching email senders:', error);
});
} */

onMounted(() => {

  // Run the function every second
  setInterval(() => {
    showNotification = false;
  }, 1000);

  bgColor.value = localStorage.getItem('bgColor');
  //fetchEmailSenders();
  loadFileMetadataFromLocalStorage(); // For uploaded file

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

  /*
  quill.on('selection-change', function(range, oldRange, source) {
  if (range === null && oldRange !== null) {
      console.log('Selection changed');
      var quillContent = quill.root.innerHTML;
      handleInputUpdate3(quillContent);
  }
  });*/

  // DOM-related code
  AIContainer.value = document.getElementById('AIContainer');

  const message = "Bonjour, à quelle destinaire(s) souhaitez vous envoyer cet email ?";
  const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
  displayMessage(message, ai_icon);
  objectInput.value = document.getElementById('objectInput');

  quill.value.on('text-change', function () {
    mailInput.value = quill.value.root.innerHTML;
    // console.log("MAIL", MailCreatedByAI.value);
    // console.log("First", isFirstTimeEmail.value);
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

  /* OLD TO DELETE
  let quillContainer = document.querySelector('#editor');

  quillContainer.addEventListener('mouseleave', function() {
      console.log('Mouse has left the Quill editor area');

      // Call the function to handle the input on mouseleave
      console.log(quill.value.root.innerHTML)
      const quillContent = quill.value.root.innerHTML;

      if (quillContent.trim() !== '<p><br></p>') {
        handleInputUpdateMailContent(quill.value.root.innerHTML);
      }
  });*/

  // Event Listeners
  /*
  objectInput.value.addEventListener('blur', handleInputUpdateObject);
  objectInput.value.addEventListener('keyup', function(e) {
      if (e.keyCode === 13) {
          handleInputUpdateObject();
      }
  });*/

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
      clearInterval(interval);
    }
  }, 30);
}


/*function personSelected() { OLD TO DELETE
console.log(selectedPerson.value);
if (selectedPerson.value && !selectedPeople.value.includes(selectedPerson.value)) {
  selectedPeople.value.push(selectedPerson.value); // Add the selected person to the array
  selectedPerson.value = null; // Clear the current selection
  //handleInputUpdate(selectedPerson.value.username);
}
}*/

function personSelected(person) {
  if (!person) return;

  // To display AI
  let displayText = '';

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
        // console.log("DEBUG People -->", selectedPeople.value);
      }
  }

  if (isFirstTimeDestinary.value) {
    askContent();
    stepcontainer = 1;
    isFirstTimeDestinary.value = false;
  }

  selectedPerson.value = null;

  // To display AI (value entered by the user)
  // OPTIONAL : DEACTIVATED BY DEFAULT => UX DESIGN => TO VALIDATE
  /*
  if (selectedPeople.value.length > 0) {
    const peopleNames = selectedPeople.value.map(person => person.name);
    displayText += peopleNames.join(', ');
  }
  
  if (selectedCC.value.length > 0) {
      if (displayText.length > 0) displayText += ', ';
      const ccNames = selectedCC.value.map(person => person.name);
      displayText += 'CC : '
      displayText += ccNames.join(', ');
  }
  
  if (selectedCCI.value.length > 0) {
      if (displayText.length > 0) displayText += ', ';
      const cciNames = selectedCCI.value.map(person => person.name);
      displayText += 'CCI : '
      displayText += cciNames.join(', ');
  }
  
  
  let messageContainer = document.getElementById('object_input_user');
  
  const messageHTML = `
      <div id='object_input_user' class="flex pb-12">
          <div class="mr-4 flex">
              <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-slate-500">
                <span class="text-lg font-medium leading-none text-white">TH</span>
              </span>   
          </div>
          <div>
              <p class="font-serif">${displayText}</p>
          </div>
      </div>
    `;
  
  if (messageContainer) {
      messageContainer.outerHTML = messageHTML;
  } else {
      AIContainer.value.innerHTML += messageHTML;
      display("N'hésitez pas à m'indiquer un autre destinataire", counter_display); // MAYBE TO DELETE
      counter_display += 1; // MAYBE TO DELETE
  }*/

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


/* INPUT to handle SELECT => NOT USED
function handleInputUpdate(selectedUsername) {
const newMessage = selectedUsername.trim();

if (newMessage !== '') {
    // Ask the user to enter a content
    console.log(askContentContainer.value.innerHTML);
    setTimeout(() => {
      if (askContentContainer.value.innerHTML == ''){
        askContent();
      }
    }, 400);
    // Ask the user to enter a content
    //askContent(); 
    // Clear the container
    messagesContainer.value.innerHTML = '';

    // Insert the full structure
    const messageHTML = `
        <div class="flex pb-12">
            <div class="mr-4 flex">
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-slate-500">
                    <span class="text-lg font-medium leading-none text-white">TH</span>
                </span>   
            </div>
            <div>
                <p class="font-serif" ref="">${newMessage}</p>
            </div>
        </div>
    `;

    messagesContainer.value.innerHTML = messageHTML;

    //const targetParagraph = messagesContainer.value.querySelector('p[ref="animatedText2"]');
    //animateText(newMessage, targetParagraph);
}
}*/

function handleInputUpdateObject() {

  /* OLD OPTIONAL => 
  if ((selectedPeople.value.length > 0 || selectedCC.value.length > 0 || selectedCCI.value.length > 0)) {
    if (isFirstTimeObject.value && stepcontainer == 0) {
      askContent();
      stepcontainer = 1;
      isFirstTimeObject.value = false;
    }
  } */
  console.log("Input entered object")
}

function handleInputUpdateMailContent(newMessage) {

  if (newMessage !== '') {
    if ((selectedPeople.value.length > 0 || selectedCC.value.length > 0 || selectedCCI.value.length > 0)) {

      askContentAdvice();
      stepcontainer = 2;

      // console.log("TEST STEP", stepcontainer);

      // Insert the full structure
      // OPTION : Check UX Before activate (desactivated for UX reasons)
      /*
      const messageHTML = `
          <div class="flex pb-12">
              <div class="mr-4 flex">
                  <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-slate-500">
                      <span class="text-lg font-medium leading-none text-white">TH</span>
                  </span>   
              </div>
              <div class="font-serif">
                  ${newMessage}
              </div>
          </div>
      `;
      AIContainer.value.innerHTML += messageHTML;*/

      scrollToBottom(); // To scroll to the bottom
    }
  }
}

/*
onBeforeUnmount(() => {
  window.removeEventListener('resize', scrollToBottom);
});*/


function askContent() {
  // Your previous code to display the message when the component is mounted
  const message = "N'hésitez pas à fournir un brouillon de l'email que vous souhaitez rédiger"; // Older : const message = "Pouvez-vous fournir un brouillon de l'email que vous souhaitez rédiger ?
  const messageHTML = `
    <div class="pb-12">
      <div class="flex">
          <div class="mr-4">
              <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                </svg>
              </span>
          </div>
          <div>
              <div class="flex flex-col">
                <p ref="animatedText${counter_display}"></p>
                <div class="flex mt-4">
                  <div class="mr-4">
                      <select id="lengthSelect" class="h-10 px-8 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white focus:bg-gray-900 focus:text-white border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900"> <!-- OLD : focus:ring-2 focus:ring-gray-600 focus:ring-inset focus:border-gray-600 -->
                          <option value="very short">Très bref</option>
                          <option value="short" selected>Bref</option>
                          <option value="long">Long</option>
                      </select>
                  </div>
                  <div>
                      <select id="formalitySelect" class="h-10 px-8 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white focus:bg-gray-900 focus:text-white border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900"> <!-- OLD : focus:ring-2 focus:ring-gray-600 focus:ring-inset focus:border-gray-600 -->
                          <option value="very informal">Non formel</option>
                          <option value="informal">Peu formel</option>
                          <option value="formal" selected>Formel</option>
                          <option value="very formal">Très formel</option>
                      </select>
                  </div>
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

  const lengthSelect = document.getElementById('lengthSelect');
  const formalitySelect = document.getElementById('formalitySelect');

  lengthSelect.addEventListener('change', () => {
    lengthValue.value = lengthSelect.value;
    console.log('Length:', lengthValue);
  });

  formalitySelect.addEventListener('change', () => {
    formalityValue.value = formalitySelect.value;
    console.log('Formality:', formalityValue);
  });
}

function askContentAdvice() {
  // Your previous code to display the message when the component is mounted
  const message = "Comment puis-je vous aider à rédiger votre mail ?"; // Older : const message = "Pouvez-vous fournir un brouillon de l'email que vous souhaitez rédiger ?";

  const messageHTML = `
    <div class="pb-12">
      <div class="flex">
          <div class="mr-4">
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
                      Corrige l'orthographe
                    </button>
                  </div>
                  <div>
                    <button type="button" id="CopyWritingCheckButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                      Vérifie le copywriting
                    </button>
                  </div>
                </div>
                <div class="flex mt-4">
                  <div class="mr-4">
                    <button type="button" id="WriteBetterButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                      Améliore l'écriture
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

  // Display the username before the list of emails
  const usernameHTML = `<div>Pour l'utilisateur : <strong>${firstUsername}</strong></div>`;

  list.forEach((item, index) => {
    // Extract the first (and presumably only) key in the dictionary, which is the username
    const username = Object.keys(item)[0];
    const email = item[username]; // Accessing the email using the username key

    // Generating a unique ID for each button based on the index to ensure it's unique
    const buttonId = `button-${index}`;

    buttonsHTML += `
      <div class="mr-4">
        <button type="button" id="${buttonId}" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
          ${email} <!-- Displaying the email on the button -->
        </button>
      </div>
    `;
  });

  const messageHTML = `
    <div class="flex pb-1 pl-[72px]">
      <div class="flex flex-col">
        ${usernameHTML}
        <div class="flex mt-4">
          ${buttonsHTML}
        </div>
      </div>
    </div>
  `;

  AIContainer.value.innerHTML += messageHTML;

  // Add event listeners to the buttons
  list.forEach((item, index) => {
    const buttonId = `button-${index}`;
    setTimeout(() => {
      const button = document.getElementById(buttonId);
      if (button) {
        button.addEventListener('click', () => {
          const username = Object.keys(item)[0]; // Re-extracting the username for the click event
          const email = item[username]; // Accessing the email using the username key
          console.log(`Username: ${username}, Email: ${email}`);
          if (type === 'main') {
            const person = { username: username, email: email };
            selectedPeople.value.push(person);
          } else if (type === 'cc') {
            const person = { username: username, email: email };
            selectedCC.value.push(person);
          } else {
            const person = { username: username, email: email };
            selectedCCI.value.push(person);
          }
        });
      }
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
              Passez à la suite
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
        stepcontainer = 1;
        askContent();
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
        'Content-Type': 'application/json',
        'email': localStorage.getItem('email')
      },
      body: JSON.stringify({
        email_subject: inputValue.value,
        email_body: mailInput.value,
      }),
    };

    const result = await fetchWithToken('http://localhost:9000/MailAssistant/api/correct_email_language/', requestOptions);

    hideLoading();
    //subject.value = result.corrected_subject; TO DELETE ?
    //mail.value = result.corrected_body; TO DELETE ?
    // retrieve num of corrections
    console.log(result);
    if (result.corrected_subject && result.corrected_body) {
      // TO FINISH => animation
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
                    <p><strong>Objet:</strong> ${result.corrected_subject}</p>
                    <p><strong>Email:</strong> ${formattedMail}</p>
                </div>
            </div>
        `;
      AIContainer.value.innerHTML += messageHTML;
      inputValue.value = result.corrected_subject;
      const quillEditorContainer = quill.value.root;
      quillEditorContainer.innerHTML = result.corrected_body;

      // TO FINISH => create button with new options to reformat quickly the email written (more short, more formal, more strict)
      const message = "J'ai corrigé l'orthographe, est-ce que souhaitez autre chose ?";
      const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
      displayMessage(message, ai_icon);
    } else {
      hideLoading();
      const message = "Je m'excuse, j'ai fait une erreur de traitement."
      const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
      displayMessage(message, ai_icon);
      console.log('Subject or Email is missing in the response');
    }

  } catch (error) {
    console.error('Error:', error);
    hideLoading();
    const message = "Je m'excuse, j'ai fait une erreur de traitement."
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
        'Content-Type': 'application/json',
        'email': localStorage.getItem('email')
      },
      body: JSON.stringify({
        email_subject: inputValue.value,
        email_body: mailInput.value,
      }),
    };

    const result = await fetchWithToken('http://localhost:9000/MailAssistant/api/check_email_copywriting/', requestOptions);

    hideLoading();
    //subject.value = result.corrected_subject; TO DELETE ?
    //mail.value = result.corrected_body; TO DELETE ?
    // retrieve num of corrections
    console.log(result);
    if (result.feedback_copywriting) {
      // TO FINISH => animation
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

      // TO FINISH => create button with new options to reformat quickly the email written (more short, more formal, more strict)
      const message = "J'ai vérifié le copywriting, est-ce que souhaitez autre chose ?";
      const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
      displayMessage(message, ai_icon);
    } else {
      hideLoading();
      const message = "Je m'excuse, j'ai fait une erreur de traitement."
      const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
      displayMessage(message, ai_icon);
      console.log('Subject or Email is missing in the response');
    }

  } catch (error) {
    console.error('Error:', error);
    hideLoading();
    const message = "Je m'excuse, j'ai fait une erreur de traitement."
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
        'email': localStorage.getItem('email')
      },
      body: JSON.stringify({
        email_body: mailInput.value,
        email_subject: inputValue.value,
      }),
    };

    const result = await fetchWithToken('http://localhost:9000/MailAssistant/api/gpt_improve_email_writing/', requestOptions);

    hideLoading();
    console.log(result);
    subject.value = result.subject;
    mail.value = result.body;
    if (result.subject && result.email_body) {
      // TO FINISH => animation
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
                  <p><strong>Objet:</strong> ${result.subject}</p>
                  <p><strong>Email:</strong> ${result.email_body}</p>
              </div>
          </div>
      `;
      AIContainer.value.innerHTML += messageHTML;
      inputValue.value = result.subject;
      const quillEditorContainer = quill.value.root;
      quillEditorContainer.innerHTML = result.email_body;

      // TO FINISH => create button with new options to reformat quickly the email written (more short, more formal, more strict)
      const message = "Est-ce que ce mail vous convient mieux ?";
      const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
      displayMessage(message, ai_icon);
    } else {
      hideLoading();
      const message = "Je m'excuse, j'ai fait une erreur de traitement. Est-ce que vous pouvez réessayer ?"
      const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
      displayMessage(message, ai_icon);
      console.log('Subject or Email is missing in the response');
    }
  } catch (error) {
    console.error('Error:', error);
    hideLoading();
    // Handling error => TO PUT IN A FUNCTION
    const message = "Je m'excuse, j'ai fait une erreur de traitement. Est-ce que vous pouvez réessayer ?"
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

async function sendEmail() {
  // Send an email with input parameters

  const emailSubject = inputValue.value;
  const emailBody = quill.value.root.innerHTML; // or use quillEditor.value.getText() for plain text
  const recipients = selectedPeople.value.map(person => person.email); // Adjust according to your data structure
  const ccRecipients = selectedCC.value.map(person => person.email);
  const bccRecipients = selectedCCI.value.map(person => person.email);

  const formData = new FormData();
  formData.append('subject', emailSubject);
  formData.append('message', emailBody);
  fileObjects.value.forEach(file => formData.append('attachments', file));

  // Add recipients, CC, and BCC to formData if needed
  // Adjust the field names according to your API's expected format
  formData.append('to', recipients.join(','));
  formData.append('cc', ccRecipients.join(','));
  formData.append('cci', bccRecipients.join(','));

  try {
    const response = await fetchWithToken('http://localhost:9000/MailAssistant/api/send_mail/', {
      method: 'POST',
      headers: {
        email: localStorage.getItem('email')
      },
      body: formData
    });

    if (response.message === 'Email sent successfully!') {
      // Show the pop-up
      showNotification = true;
      backgroundColor = 'bg-green-300';
      notificationTitle = 'Succès !';
      notificationMessage = 'Votre email a été envoyé avec succès.';

      // Other logic
      inputValue.value = '';
      quill.value.root.innerHTML = '';
      selectedPeople.value = [];
      selectedCC.value = [];
      selectedCCI.value = [];
      stepcontainer = 0;
      AIContainer.value.innerHTML = '';
      AIContainer.value = document.getElementById('AIContainer');

      const message = "Bonjour, à quelle destinaire(s) souhaitez vous envoyer cet email ?";
      const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
      displayMessage(message, ai_icon);
    } else {
      // Show the pop-up
      showNotification = true;
      backgroundColor = 'bg-red-300';
      notificationTitle.value = 'Erreur d\'envoi d\'email';
      notificationMessage.value = response.message;
    }
  } catch (error) {
    // Show the pop-up
    showNotification = true;
    backgroundColor = 'bg-red-300';
    notificationTitle.value = 'Erreur d\'envoi d\'email';
    notificationMessage.value = error;
  }
}
</script>

<script>
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';
import {
  UserGroupIcon,
  Bars2Icon,
  //Bars3BottomLeftIcon,
  //ChatBubbleOvalLeftEllipsisIcon,
  ChevronDownIcon
} from '@heroicons/vue/24/outline'


export default {
  components: {
    Navbar,
    Navbar2,
    UserGroupIcon,
    Bars2Icon,
    ChevronDownIcon
    // ChatBubbleOvalLeftEllipsisIcon,
    // Bars3BottomLeftIcon
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