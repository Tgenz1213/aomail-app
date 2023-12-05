<template>
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
            <div class="flex gap-4 w-full">
                <div id="firstMainColumn" class="flex-grow bg-gray-100 bg-opacity-75 rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg xl:h-[95vh] xl:w-[43vw] 2xl:h-[825px] 2xl:w-[700px]"> <!--xl:h-[750px] xl:w-[625px]-->
                    <div class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-400 bg-opacity-10"> <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
                    <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">Assistant IA</h1>
                    </div>
                    <div class="flex flex-col divide-y xl:h-[85vh] 2xl:h-[785px]">
                    <div class="overflow-y-auto xl:h-[75vh] 2xl:h-[700px]" style="margin-right: 2px;" ref="scrollableDiv">
                    <div class="px-10 py-4">
                        <div class="flex-grow">
                            <div id="DestinaryContainer">
                            </div>
                            <div id="UserDestinaryContainer">
                            </div>
                            <div id="UserObjectContainer">
                            </div>
                            <div id="UserAskContentContainer">
                            </div>
                            <div id="EmailContainer">
                            </div>
                        </div>
                    </div>
                    </div>
                    <div class="flex-grow">
                    <div class="flex px-6 2xl:py-10 py-6 relative w-full">
                        <div class="flex flex-grow items-stretch">
                            <textarea id="dynamicTextarea" @input="adjustHeight" v-model="textareaValue" class="overflow-y-hidden left-0 pl-3 only:block w-full rounded-none rounded-l-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" placeholder="Instruction"></textarea>
                        </div>
                        <button type="button" @click="handleAIClick" class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-r-md px-3 py-2.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 bg-gray-50 hover:bg-gray-50 z-50">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" stroke-width="1.5" stroke="rgb(243 244 246)" class="w-6 h-6 text-gray-400">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                            </svg>
                        </button>
                        </div>
                    </div>
                </div>
                </div>
                <div id="secondMainColumn" class="flex-grow bg-white rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg xl:h-[95vh] xl:w-[43vw] 2xl:h-[825px] 2xl:w-[700px]"> <!--xl:h-[695px] xl:w-[560px]-->
                    <div class="flex flex-col divide-y divide-gray-200 h-full w-full">
                        <div class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-50">
                        <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">Saisi manuel</h1>
                        </div>
                        <form class="flex flex-grow w-full px-10">
                            <div class="flex flex-col space-y-6 h-full w-full">
                                <div class="pt-8">
                                    <div class="flex flex-wrap">
                                        <!-- Main Recipients List -->
                                        <div v-if="selectedPeople.length > 0" class="flex items-center mb-1 mr-1 bg-gray-200 rounded px-2 py-1">
                                          <div v-for="person in selectedPeople" :key="person.username" class="flex items-center">
                                            {{ person.name }}
                                            <button @click="removePersonFromMain(person)">×</button>
                                          </div>
                                        </div>
                                        <!-- CC Recipients List -->
                                        <div v-if="selectedCC.length > 0" class="flex items-center mb-1 mr-1 bg-gray-200 rounded px-2 py-1">
                                            <div v-for="person in selectedCC" :key="person.username" class="flex items-center">
                                                <span class="font-semibold mr-1">CC:</span>
                                                {{ person.name }}
                                                <button @click="removePersonFromCC(person)">×</button>
                                            </div>
                                        </div>
                                        <!-- CCI Recipients List -->
                                        <div v-if="selectedCCI.length > 0" class="flex items-center mb-1 mr-1 bg-gray-200 rounded px-2 py-1">
                                            <div v-for="person in selectedCCI" :key="person.username" class="flex items-center">
                                                <span class="font-semibold mr-1">CCI:</span>
                                                {{ person.name }}
                                                <button @click="removePersonFromCCI(person)">×</button>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="flex items-stretch gap-1">
                                        <div class="flex-grow">
                                        <div class="relative items-stretch">
                                            <div class="relative w-full">
                                                <div 
                                                    v-if="!isFocused2 && !hasValueEverBeenEntered" 
                                                    class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2"
                                                >
                                                    <UserGroupIcon class="w-4 h-4 pointer-events-none" />
                                                    <label for="username" class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none">Destinaire(s)</label>
                                                </div>
                                                <Combobox as="div" v-model="selectedPerson" @update:model-value="personSelected" @blur="handleBlur2">
                                                    <ComboboxInput 
                                                        class="w-full h-10 rounded-md border-0 bg-white py-2 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" 
                                                        @change="query = $event.target.value" 
                                                        :display-value="(person) => person?.name"
                                                        @focus="handleFocus2"
                                                        @blur="handleBlur2"
                                                    />
                                                    <ComboboxButton class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
                                                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                                                    </ComboboxButton>

                                                    <ComboboxOptions v-if="filteredPeople.length > 0" class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                                                        <ComboboxOption v-for="person in filteredPeople" :key="person.username" :value="person" as="template" v-slot="{ active, selected }">
                                                            <li :class="['relative cursor-default select-none py-2 pl-3 pr-9', active ? 'bg-gray-500 text-white' : 'text-gray-900']">
                                                                <div class="flex">
                                                                    <span :class="['truncate', selected && 'font-semibold']">
                                                                        {{ person.name }}
                                                                    </span>
                                                                    <span :class="['ml-2 truncate text-gray-500', active ? 'text-indigo-200' : 'text-gray-500']">
                                                                        {{ person.username }}
                                                                    </span>
                                                                </div>

                                                                <span v-if="selected" :class="['absolute inset-y-0 right-0 flex items-center pr-4', active ? 'text-white' : 'text-gray-500']">
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
                                            <button 
                                            type="button" 
                                            @click="toggleCC"
                                            :class="['inline-flex items-center gap-x-1.5 rounded-md px-2.5 py-1.5 text-sm font-semibold hover:bg-gray-500 hover:text-white', activeType === 'CC' ? 'bg-gray-500 text-white' : 'bg-gray-100 text-gray-400']"
                                            class="ring-1 ring-inset ring-gray-300 shadow-sm hover:ring-gray-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                                            CC
                                            </button>

                                            <!-- CCI Button -->
                                            <button 
                                            type="button" 
                                            @click="toggleCCI"
                                            :class="['inline-flex items-center gap-x-1.5 rounded-md px-2.5 py-1.5 text-sm font-semibold hover:bg-gray-500 hover:text-white', activeType === 'CCI' ? 'bg-gray-500 text-white' : 'bg-gray-100 text-gray-400']"
                                            class="ring-1 ring-inset ring-gray-300 shadow-sm hover:ring-gray-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                                            CCI
                                            </button>
                                        </div>
                                    </div>
                                </div>
                                <div class="">
                                    <div class="flex flex-wrap">
                                        <div v-for="(file, index) in uploadedFiles" :key="index" class="flex items-center mb-1 mr-1 bg-gray-200 rounded px-2 py-1">
                                            {{ file.name }}
                                            <button @click="removeFile(index)">×</button>
                                        </div>
                                    </div>
                                    <div class="flex items-stretch gap-1">
                                    <div class="flex-grow">
                                        <div class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 w-full">
                                        <div class="relative w-full">
                                            <div 
                                            v-if="!isFocused && !inputValue" 
                                            class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 z-10"
                                            >
                                            <Bars2Icon class="w-4 h-4 pointer-events-none" />
                                            <label for="username" class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none">Objet</label>
                                            </div>
                                            <!--<input type="text" name="username" id="objectInput" autocomplete="username" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="janesmith">-->
                                            <input 
                                                id="objectInput" 
                                                v-model="inputValue"
                                                type="text" 
                                                class="block h-10 flex-1 border-0 bg-transparent py-2 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6 w-full z-20 relative" 
                                                @focus="handleFocus" 
                                                @blur="handleBlur"
                                            />
                                        </div>
                                        </div>
                                    </div>
                                    <div class="flex">
                                        <input type="file" ref="fileInput" @change="handleFileUpload" multiple hidden>
                                        <button @click="triggerFileInput" type="button" class="inline-flex items-center gap-x-1.5 rounded-md bg-gray-100 px-2.5 py-1.5 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-300 shadow-sm hover:ring-gray-800 hover:bg-gray-500 hover:text-white  focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13" />
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
                                    <div class="flex-grow mb-16"> <!-- TO DEBUG : Overflow Error -->
                                        <div id="editor" class="w-full"></div> 
                                    </div>
                                    <div class="flex mb-4">
                                    <div class="inline-flex rounded-lg shadow-lg">
                                        <button  class="bg-gray-500 rounded-l-lg px-8 py-2.5 text-md font-semibold text-white hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600">Envoyer</button>
                                        <Menu as="div" class="relative -ml-px block">
                                        <MenuButton class="relative inline-flex items-center rounded-r-lg  px-2 py-2 text-white border-l border-gray-300 bg-gray-500 hover:bg-gray-600 focus:z-10">
                                            <span class="sr-only">Open options</span>
                                            <ChevronDownIcon class="h-8 w-5" aria-hidden="true" />
                                        </MenuButton>
                                        <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                                            <MenuItems class="absolute right-0 z-10 -mr-1 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                                            <div class="py-1">
                                                <MenuItem v-for="item in items" :key="item.name" v-slot="{ active }">
                                                <a :href="item.href" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']">{{ item.name }}</a>
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
</template>

<script setup>
import { defineProps, defineEmits, computed, ref, onMounted, nextTick } from 'vue';
import { watch } from 'vue';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue';
import { ChevronDownIcon } from '@heroicons/vue/20/solid';
import Quill from 'quill';

import {
    Combobox,
    ComboboxButton,
    ComboboxInput,
    //ComboboxLabel,
    ComboboxOption,
    ComboboxOptions,
  } from '@headlessui/vue'

const items = [
  { name: 'Envoyer à une heure', href: '#' },
]

const people = [
    { name: 'Leslie Alexander', username: '@lesliealexander' },
    { name: 'Theo', username: 'theohubert3@gmx.com'}
  ]
  
const selectedPeople = ref([]);
const selectedCC = ref([]);
const selectedCCI = ref([]);
const activeType = ref(null);  // null, 'CC', or 'CCI'

const query = ref('')
const filteredPeople = computed(() =>
query.value === ''
    ? people
    : people.filter((person) => {
        return person.name.toLowerCase().includes(query.value.toLowerCase())
    })
)

const props = defineProps(['modelValue']);
const emit = defineEmits(['update:selectedPerson']);
const selectedPerson = ref(props.modelValue);

watch(selectedPerson, (newValue) => {
    console.log(selectedPerson.value);
    hasValueEverBeenEntered.value = true; // to make the icon disappear
    if (selectedPerson.value && selectedPerson.value.username) {
        handleInputUpdate(selectedPerson.value.username);
    }  
    emit('update:selectedPerson', newValue);
});


const inputValue = ref('');
const isFocused = ref(false);
const isFocused2 = ref(false);
const hasValueEverBeenEntered = ref(false);

function handleFocus() {
  isFocused.value = true;
}

function handleBlur() {
  isFocused.value = false;
}

function handleFocus2() {
  isFocused2.value = true;
}

function handleBlur2() {
  isFocused2.value = false;
}

const DestinaryContainer = ref(null);
const messagesContainer = ref(null);
const objectInput = ref(null);
const objectContainer = ref(null);
const askContentContainer = ref(null);
const EmailContainer = ref(null);

// To keep the navbar always at the bottom when new content is added
const scrollableDiv = ref(null);
const scrollToBottom = async () => {
    await nextTick();
    const element = scrollableDiv.value;
    element.scrollTop = element.scrollHeight;
};

// AI instruction textarea input
const textareaValue = ref('');

/*
const adjustHeight = (event) => {
    // Votre logique pour ajuster la hauteur
};*/

////////////////////////////////////////////////////// To Handle files upload ///////////////////////////////////////////////////////
const fileInput = ref(null);
const uploadedFiles = ref([]);
const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25MB, Gmail's limit

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileUpload = (event) => {
  const files = Array.from(event.target.files);
  files.forEach(file => {
    if (file.size <= MAX_FILE_SIZE) {
      uploadedFiles.value.push({ name: file.name, size: file.size });
    } else {
      alert("File size exceeds Gmail's limit");
    }
  });
  saveFileMetadataToLocalStorage();
};

const removeFile = (index) => {
  uploadedFiles.value.splice(index, 1);
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

const handleAIClick = () => {
  const elements = [
    document.getElementById("UserDestinaryContainer"),
    document.getElementById("UserObjectContainer"),
    document.getElementById("EmailContainer"),
  ];
  console.log(textareaValue.value); // Cela imprimera la valeur de la textarea

  // Vous pouvez maintenant vérifier la valeur et exécuter votre logique désirée
  if (!elements[0].innerHTML.trim() && !elements[1].innerHTML.trim() && !elements[2].innerHTML.trim() && textareaValue.value != '') {
    const messageHTML = `
    <div class="flex pb-12">
        <div class="mr-4 flex">
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-slate-500">
              <span class="text-lg font-medium leading-none text-white">TH</span>
            </span>   
        </div>
        <div>
            <p class="font-serif" >"${textareaValue.value}"</p>
        </div>
    </div>
  `;
    elements[0].innerHTML += messageHTML;

    setTimeout(async () => {
      if (askContentContainer.value.innerHTML == '') {
        try {
          const result = await findUser(textareaValue.value);
          textareaValue.value = '';
          console.log(userSearchResult.value);
          let noUsersAdded = true;
          if (userSearchResult.value !== "Invalid input or query not about email recipients") { // To update to handle the main error
            for (const [category, recipients] of Object.entries(userSearchResult.value)) {
              for (const [key, value] of Object.entries(recipients)) {
                if (key !== "" && value !== "No matching emails found.") {
                  for (const [email, name] of Object.entries(value)) {
                    const person = { name: name, email: email };
                    if (category === "main_recipients") {
                      selectedPeople.value.push(person);
                    } else if (category === "cc_recipients") {
                      selectedCC.value.push(person);
                    } else if (category === "bcc_recipients") {
                      selectedCCI.value.push(person);
                    }
                    noUsersAdded = false;
                  }
                }
              }
            }
            if (noUsersAdded) {
              console.log("No user added");
              const UserDestinaryContainer = document.getElementById('UserDestinaryContainer');
              const message = "Je n'ai pas trouvé de destinataires, veuillez ressayer ou saisir manuellement";
              const messageHTML = `
              <div class="flex pb-12">
                  <div class="mr-4 flex">
                      <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-500">
                          <span class="text-lg font-medium leading-none text-white">AO</span>
                      </span>   
                  </div>
                  <div>
                      <p>Je n'ai pas trouvé de destinataires, veuillez ressayer ou saisir manuellement</p>
                  </div>
              </div>
              `;
              UserDestinaryContainer.innerHTML += messageHTML;
              //const animatedParagraph = document.querySelector('p[ref="animatedText1"]');
              //animateText(message, animatedParagraph);
            } else {
              askContent();
            }
          } else {
            console.log("No matching emails found.");
          }
        } catch (error) {
          console.error("Error finding user:", error.message);
        }
      }
    }, 400);
  } else if (elements[0].innerHTML.trim() && !elements[2].innerHTML.trim() && textareaValue.value != '') {
      // Faites autre chose
      const messageHTML = `
      <div class="flex pb-12">
          <div class="mr-4 flex">
              <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-slate-500">
                <span class="text-lg font-medium leading-none text-white">TH</span>
              </span>   
          </div>
          <div>
              <p class="font-serif" >${textareaValue.value}</p>
          </div>
      </div>
      `;
      elements[2].innerHTML += messageHTML;
      textareaValue.value = '';
  }
};

async function refreshToken() {
    // Get the refresh token from local storage
    const refresh_token = localStorage.getItem('refreshToken');

    if (!refresh_token) {
        throw new Error('No refresh token found');
    }

    // Set up the request options for the fetch call
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refresh_token }),
    };

    try {
        // Make the POST request to the refresh token endpoint
        const response = await fetch('http://localhost:9000/MailAssistant/api/token/refresh/', requestOptions);

        // Check if the response status is OK (200)
        if (!response.ok) {
            throw new Error(`Failed to refresh token: ${response.statusText}`);
        }

        // Parse the JSON response to get the new access token
        const data = await response.json();
        const new_access_token = data.access;

        // Save the new access token to local storage
        localStorage.setItem('userToken', new_access_token);

        return new_access_token;
    } catch (error) {
        console.error('Error refreshing token: ', error.message);
        // Handle the error (e.g., by redirecting the user to a login page)
        throw error;
    }
}

const bgColor = ref(''); // Initialize a reactive variable

async function getUserBgColor() {
  try {
    const response = await fetch('http://localhost:9000/MailAssistant/user/preferences/bg_color/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('userToken')}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log(data);
    bgColor.value = data.bg_color; // Update the reactive variable
  } catch (error) {
    console.error("Error fetching user background color:", error.message);
  }
}

/* DOES NOT WORK => TO CHECK */
const userSearchResult = ref(null);

async function findUser(searchQuery) {
  try {
    const response = await fetch('http://localhost:9000/MailAssistant/api/find-user-ai/?query=' + encodeURIComponent(searchQuery), {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('userToken')}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
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
      'Authorization': `Bearer ${localStorage.getItem('userToken')}`,
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

    refreshToken();
    getUserBgColor();
    //fetchEmailSenders();
    loadFileMetadataFromLocalStorage(); // For uploaded file

    window.addEventListener('resize', scrollToBottom); // To keep the scroll in the scrollbar at the bottom even when viewport change

    var toolbarOptions = [
    [{ 'font': [] }],
    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
    ['bold', 'italic', 'underline'],
    [{ 'color': [] }, { 'background': [] }],
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    [{ 'align': [] }],
    ['blockquote', 'code-block']                                      
    ];

    // Initialize Quill editor
    var quill = new Quill('#editor', {
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
    DestinaryContainer.value = document.getElementById('DestinaryContainer');

    const message = "Bonjour, à quelle destinaire(s) souhaitez vous envoyer cet email ?";

    const messageHTML = `
    <div class="flex pb-12">
        <div class="mr-4 flex">
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-500">
                <span class="text-lg font-medium leading-none text-white">AO</span>
            </span>   
        </div>
        <div>
            <p ref="animatedText1"></p>
        </div>
    </div>
    `;

    DestinaryContainer.value.innerHTML += messageHTML;

    const animatedParagraph = document.querySelector('p[ref="animatedText1"]');
    animateText(message, animatedParagraph);

    messagesContainer.value = document.getElementById('UserDestinaryContainer');
    objectInput.value = document.getElementById('objectInput');
    objectContainer.value = document.getElementById('UserObjectContainer');
    askContentContainer.value = document.getElementById('UserAskContentContainer')
    EmailContainer.value = document.getElementById('EmailContainer');

    let quillContainer = document.querySelector('#editor');

    quillContainer.addEventListener('mouseleave', function() {
        console.log('Mouse has left the Quill editor area');

        // Call the function to handle the input on mouseleave
        console.log(quill.root.innerHTML)
        const quillContent = quill.root.innerHTML;

        if (quillContent.trim() !== '<p><br></p>') {
          handleInputUpdate3(quill.root.innerHTML);
        }
    });

    // Event Listeners
    objectInput.value.addEventListener('blur', handleInputUpdate2);
    objectInput.value.addEventListener('keyup', function(e) {
        if (e.keyCode === 13) {
            handleInputUpdate2();
        }
    });

    const form = objectInput.value.closest('form');
    if (form) {
        form.addEventListener('submit', function(e) {
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

  selectedPerson.value = null;  // Clear the current selection
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
}

function handleInputUpdate2() {

  if ((selectedPeople.value.length > 0 || selectedCC.value.length > 0 || selectedCCI.value.length > 0) && (EmailContainer.value.innerHTML.trim() == '')) {
    askContent();
  }
}

function handleInputUpdate3(newMessage) {

  if (newMessage !== '') {
      // Clear the container
      EmailContainer.value.innerHTML = '';

      // Insert the full structure
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
      EmailContainer.value.innerHTML = messageHTML;

      scrollToBottom(); // To scroll to the bottom

      //const targetParagraph = EmailContainer.value.querySelector('p[ref="animatedText4"]');
      //animateText(newMessage, targetParagraph);
  }
}

/*
onBeforeUnmount(() => {
    window.removeEventListener('resize', scrollToBottom);
});*/

function askContent() {
    // Your previous code to display the message when the component is mounted
    const message = "Pouvez-vous fournir un brouillon de l'email que vous souhaitez rédiger ou bien choisir l'une des réponses suivantes ?";

    const messageHTML = `
        <div class="flex pb-12">
            <div class="mr-4 flex">
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-500">
                    <span class="text-lg font-medium leading-none text-white">AO</span>
                </span>   
            </div>
            <div>
                <p ref="animatedText5"></p>
            </div>
        </div>
    `;

    askContentContainer.value.innerHTML += messageHTML;
    const animatedParagraph = document.querySelector('p[ref="animatedText5"]');
    animateText(message, animatedParagraph);
}

</script>

<script>
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';

import {
  //ChatBubbleOvalLeftEllipsisIcon,
  UserGroupIcon,
  Bars2Icon,
  //Bars3BottomLeftIcon,
} from '@heroicons/vue/24/outline'

  /*
  const userDestinaryContainer = document.getElementById('UserDestinaryContainer');
  const emailContainer = document.getElementById('EmailContainer');
    
  // Check if UserDestinaryContainer has content (not just whitespace)
  if (userDestinaryContainer.textContent.trim() !== '') {
     emailContainer.innerHTML = `
        <div class="flex pb-12">
          <div class="mr-4 flex">
              <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-500">
                  <span class="text-lg font-medium leading-none text-white">AO</span>
              </span>   
          </div>
          <div>
              <p ref="animatedText3">Veuillez choisir l'une des options ci-dessous ou saisissez un brouillon portant sur le sujet de votre mail</p>
          </div>
        </div>';`
  } else {
    emailContainer.innerHTML = ''; // Clear the EmailContainer if desired
  }

  const animatedParagraph2 = document.querySelector('p[ref="animatedText3"]');
  animateText(message, animatedParagraph2);*/

export default {
  components: {
    Navbar,
    Navbar2,
    //ChatBubbleOvalLeftEllipsisIcon,
    UserGroupIcon,
    Bars2Icon,
    //Bars3BottomLeftIcon
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
  },
  mounted() {
  }
}
</script>
