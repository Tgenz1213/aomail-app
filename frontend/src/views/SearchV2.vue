<template>
  <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
    :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" />
  <div class="flex flex-col justify-center items-center h-screen" :class="bgColor">
    <div class="flex h-full w-full">
      <div class="w-[90px] bg-white ring-1 shadow-sm ring-black ring-opacity-5 2xl:w-[100px]">
        <navbar></navbar>
      </div>
      <div id="firstMainColumn"
        class="flex flex-col bg-gray-50 lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[700px]">
        <!--xl:h-[750px] xl:w-[625px] => 26/12/2023 DATA SAVE : xl:h-[95vh] xl:w-[43vw] 2xl:h-[825px] 2xl:w-[700px] -->
        <div
          class="flex items-center justify-center h-[65px] 2xl:h-[80px]">
          <div class="flex gap-x-3 items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                stroke="currentColor" class="w-6 h-6 2xl:w-7 2xl:h-7">
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
            </svg>
            <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ $t('Search_vue.titre') }}</h1>
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
            <textarea id="dynamicTextarea"
                @input="adjustHeight" v-model="textareaValue"
                class="overflow-y-hidden pt-4 pl-6 flex-1 w-full border-transparent bg-transparent text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 focus:border-transparent focus:bg-transparent focus:ring-0 2xl:pt-5 2xl:pl-7 2xl:text-base"
                placeholder="Instruction">
            </textarea>
            <div class="flex justify-end m-3 2xl:m-5">
              <button type="button" @click="handleAIClick" class="2xl:w-[100px] w-[80px] rounded-md bg-gray-700 px-5.5 py-2.5 2xl:px-6.5 2xl:py-3 2xl:text-base text-sm text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">Envoyer</button> 
            </div>
          </div>
        </div>
      </div>
      <div id="secondMainColumn"
        class="flex-grow bg-white lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[720px]">
        <!--xl:h-[695px] xl:w-[560px]-->
        <div
          class="flex items-center justify-center h-[65px] 2xl:h-[80px]">
          <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
          <div class="flex gap-x-3 items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                stroke-width="1" stroke="currentColor" class="w-6 h-6 2xl:w-7 2xl:h-7">
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672ZM12 2.25V4.5m5.834.166-1.591 1.591M20.25 10.5H18M7.757 14.743l-1.59 1.59M6 10.5H3.75m4.007-4.243-1.59-1.59" />
            </svg>
            <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ $t('Search_vue.titre2') }}</h1>
          </div>
        </div>
        <div class="flex flex-col h-full w-full">
          <div class="flex flex-col w-full px-6 pt-2">
            <div class="flex space-x-1 items-center">
              <magnifying-glass-icon class="w-4 h-4" />
              <label for="email" class="block text-sm font-medium leading-6 text-gray-900">{{
                $t('Search_vue.Recherche') }}</label>
            </div>
            <div class="flex space-x-2 items-center">
              <div class="flex-grow w-full">
                <div class="relative flex flex-grow items-stretch mt-2">
                  <input v-model="query" type="text" placeholder="Rechercher" autocomplete="given-name"
                    class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6">
                </div>
              </div>
              <div class="flex-1 mt-2">
                <button type="button" @click="searchEmails"
                  class="w-28 rounded-md bg-gray-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">{{
                    $t('Search_vue.bouton_recherche') }}</button>
              </div>
            </div>
          </div>
          <div class="flex flex-col w-full px-6 pt-4">
            <div class="grid grid-cols-2 gap-4">
              <div class="col-span-1 shadow-sm">
                <div class="flex space-x-1 items-center">
                  <user-icon class="w-4 h-4" />
                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">toAddressesSelected
                    (optionnel)</label>
                </div>
                <div class="relative items-stretch mt-2">
                  <Combobox as="div" v-model="selectedPerson">
                    <ComboboxInput
                      class="w-full rounded-md border-0 bg-white py-1.5 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                      @input="query = $event.target.value" :display-value="(person) => person?.username" />
                    <ComboboxButton
                      class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
                      <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                    </ComboboxButton>
                    <ComboboxOptions v-if="filteredPeople.length > 0"
                      class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                      <ComboboxOption v-for="person in filteredPeople" :value="person" :key="person" as="template"
                        v-slot="{ active, selected }">
                        <li @click="toggleSelection(person)"
                          :class="['relative cursor-default select-none py-2 pl-3 pr-9', active ? 'bg-gray-500 text-white' : 'text-gray-900']">
                          <div class="flex">
                            <span :class="['truncate', selected && 'font-semibold']">
                              {{ person.username }}
                            </span>
                            <span
                              :class="['ml-2 truncate text-gray-500', active ? 'text-indigo-200' : 'text-gray-500']">
                              &lt;{{ person.email }}&gt;
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
                  <div v-if="selectedRecipients.length > 0" class="mt-2 flex flex-wrap">
                    <span v-for="recipient in selectedRecipients" :key="recipient.email"
                      class="bg-gray-200 px-2 py-1.5 rounded-full text-sm font-semibold mr-2 mb-2">
                      {{ recipient.username }}
                      <button @click="removeRecipient(recipient)"
                        class="ml-1 text-red-600 focus:outline-none hover:text-red-800">&times;</button>
                    </span>
                  </div>
                </div>
              </div>
              <div class="col-span-1 shadow-sm">
                <div class="flex space-x-1 items-center">
                  <adjustments-horizontal-icon class="w-4 h-4" />
                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">TODO: list of
                    selected: Type de pièce jointe
                  </label>
                </div>
                <div class="relative items-stretch mt-2">
                  <!-- TODO: a LIST of attachments choices -->
                  <Listbox as="div" v-model="attachmentSelected">
                    <ListboxButton
                      class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 sm:text-sm sm:leading-6">
                      <span class="block truncate">{{ attachmentSelected ? attachmentSelected.name : 'Aucune'
                        }}</span>
                      <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                      </span>
                    </ListboxButton>
                    <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
                      leave-to-class="opacity-0">
                      <ListboxOptions
                        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                        <ListboxOption as="template" v-for="type in attachmentTypes" :key="type.extension"
                          :value="type" v-slot="{ active, attachmentSelected }">
                          <li
                            :class="[active ? 'bg-gray-500 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                            <span :class="[attachmentSelected ? 'font-semibold' : 'font-normal', 'block truncate']">
                              {{ type.name }} {{ type.extension }}
                            </span>
                            <span v-if="attachmentSelected"
                              :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                              <CheckIcon class="h-5 w-5" aria-hidden="true" />
                            </span>
                          </li>
                        </ListboxOption>
                      </ListboxOptions>
                    </transition>
                  </Listbox>



                </div>
              </div>
              <!-- SECOND ROW OF INPUTS -->



              <div class="col-span-1 shadow-sm">
                <div class="flex space-x-1 items-center">
                  <user-icon class="w-4 h-4" />
                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">fromAddressesSelected
                    (optionnel)</label>
                </div>
                <div class="relative items-stretch mt-2">


                  <Combobox as="div" v-model="selectedFromPerson">
                    <ComboboxInput
                      class="w-full rounded-md border-0 bg-white py-1.5 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                      @input="query = $event.target.value" :display-value="(person) => person?.username" />
                    <ComboboxButton
                      class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
                      <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                    </ComboboxButton>

                    <ComboboxOptions v-if="filteredFromPeople.length > 0"
                      class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                      <ComboboxOption v-for="person in filteredFromPeople" :value="person" :key="person"
                        as="template" v-slot="{ active, selected }">
                        <li @click="toggleSelectionFromAddress(person)"
                          :class="['relative cursor-default select-none py-2 pl-3 pr-9', active ? 'bg-gray-500 text-white' : 'text-gray-900']">
                          <div class="flex">
                            <span :class="['truncate', selected && 'font-semibold']">
                              {{ person.username }}
                            </span>
                            <span
                              :class="['ml-2 truncate text-gray-500', active ? 'text-indigo-200' : 'text-gray-500']">
                              &lt;{{ person.email }}&gt;
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

                  <div v-if="selectedFromAddresses.length > 0" class="mt-2 flex flex-wrap">
                    <span v-for="recipient in selectedFromAddresses" :key="recipient.email"
                      class="bg-gray-200 px-2 py-1.5 rounded-full text-sm font-semibold mr-2 mb-2">
                      {{ recipient.username }}
                      <button @click="removeRecipientFromAddress(recipient)"
                        class="ml-1 text-red-600 focus:outline-none hover:text-red-800">&times;</button>
                    </span>
                  </div>





                </div>
              </div>
              <div class="col-span-1 shadow-sm">
                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Tout les fields doivent
                  être ds advanced à part recherche</label>

                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">INT FIELD:
                  max_results</label>

                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">BOOL FIELD:
                  advanced</label>
                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">LIST FIELD: emails
                  Linked for search</label>
                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">INPUT FIELD:
                  subject</label>
                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">INPUT FIELD:
                  body</label>
                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">INPUT FIELD:
                  date_from</label>
                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">INPUT FIELD:
                  search_in</label>
              </div>










            </div>
          </div>
          <!-- h-[600px] 2xl:h-[700px] -->
          <div class="flex-grow p-6 mr-2">
            <div class="h-96 flex flex-col">
              <div class="flex-1 overflow-y-auto">
                <div
                  class="flex h-full items-center justify-center rounded-lg border-2 border-dashed border-gray-300 text-center">
                  <div
                    class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm ring-black ring-opacity-5 overflow-y-auto custom-scrollbar max-h-full">
                    <ul v-if="searchResult && Object.keys(searchResult).length > 0" role="list"
                      class="flex flex-col w-full">
                      <li v-for="(listIds, email) in searchResult.Gmail" :key="email" class="mb-4">
                        <svg class="-ml-0.5 h-5 w-5" aria-hidden="true" viewBox="0 0 24 24"
                          xmlns="http://www.w3.org/2000/svg" fill="currentColor">
                          <path
                            d="M23.4392061,12.2245191 C23.4392061,11.2412519 23.3594198,10.5237252 23.1867481,9.77963359 L11.9587786,9.77963359 L11.9587786,14.2176183 L18.5493435,14.2176183 C18.4165191,15.3205191 17.6989924,16.9814656 16.104458,18.0975573 L16.0821069,18.2461374 L19.6321832,20.9963359 L19.8781374,21.0208855 C22.1369771,18.9347176 23.4392061,15.8652824 23.4392061,12.2245191"
                            id="Shape" fill="#4285F4"></path>
                          <path
                            d="M11.9587786,23.9175573 C15.1876031,23.9175573 17.898229,22.8545038 19.8781374,21.0208855 L16.104458,18.0975573 C15.094626,18.8018015 13.7392672,19.2934351 11.9587786,19.2934351 C8.79636641,19.2934351 6.11230534,17.2073588 5.15551145,14.3239695 L5.01526718,14.3358779 L1.32384733,17.1927023 L1.27557252,17.3269008 C3.24210687,21.2334046 7.28152672,23.9175573 11.9587786,23.9175573"
                            id="Shape" fill="#34A853"></path>
                          <path
                            d="M5.15551145,14.3239695 C4.90305344,13.5798779 4.75694656,12.7825649 4.75694656,11.9587786 C4.75694656,11.1349008 4.90305344,10.3376794 5.14222901,9.59358779 L5.13554198,9.4351145 L1.3978626,6.53239695 L1.27557252,6.59056489 C0.465068702,8.21166412 0,10.0320916 0,11.9587786 C0,13.8854656 0.465068702,15.7058015 1.27557252,17.3269008 L5.15551145,14.3239695"
                            id="Shape" fill="#FBBC05"></path>
                          <path
                            d="M11.9587786,4.62403053 C14.2043359,4.62403053 15.719084,5.59401527 16.5828092,6.40461069 L19.9578321,3.10928244 C17.8850382,1.18259542 15.1876031,0 11.9587786,0 C7.28152672,0 3.24210687,2.68406107 1.27557252,6.59056489 L5.14222901,9.59358779 C6.11230534,6.71019847 8.79636641,4.62403053 11.9587786,4.62403053"
                            id="Shape" fill="#EB4335"></path>
                        </svg>
                        <p>Email found for: {{ email }}</p>
                        <ul>
                          <li v-for="id in listIds" :key="id"
                            class="px-6 md:py-6 2xl:py-6 hover:bg-opacity-70 dark:hover:bg-red-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center">
                            <p class="text-sm font-semibold leading-6 text-red-700 dark:text-white">{{ id }}</p>
                          </li>
                        </ul>
                      </li>
                      <li v-for="(listIds, email) in searchResult.Outlook" :key="email" class="mb-4">
                        <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21">
                          <rect x="1" y="1" width="9" height="9" fill="#f25022" />
                          <rect x="1" y="11" width="9" height="9" fill="#00a4ef" />
                          <rect x="11" y="1" width="9" height="9" fill="#7fba00" />
                          <rect x="11" y="11" width="9" height="9" fill="#ffb900" />
                        </svg>
                        <p>Email found for: {{ email }}</p>
                        <ul>
                          <li v-for="id in listIds" :key="id"
                            class="px-6 md:py-6 2xl:py-6 hover:bg-opacity-70 dark:hover:bg-red-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center">
                            <p class="text-sm font-semibold leading-6 text-red-700 dark:text-white">{{ id }}</p>
                          </li>
                        </ul>
                      </li>
                    </ul>
                    <div v-else>
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                        stroke="currentColor" class="w-12 h-12 mx-auto text-gray-400">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="M15.182 16.318A4.486 4.486 0 0012.016 15a4.486 4.486 0 00-3.198 1.318M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
                      </svg>
                      <span class="mt-2 block text-sm font-semibold text-gray-900">{{
                        $t('Search_vue.Resultats_négatif') }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, nextTick, onMounted } from 'vue';
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';
import { fetchWithToken, getBackgroundColor } from '../router/index.js';
import { API_BASE_URL } from '@/main';
import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
} from '@headlessui/vue';
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/vue';
import { CheckIcon, ChevronUpDownIcon, MagnifyingGlassIcon, UserIcon, AdjustmentsHorizontalIcon } from '@heroicons/vue/24/outline';


let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
let timerId = ref(null);


// Main variables
const AIContainer = ref(null);
const bgColor = ref('');
let counter_display = 0;
let query = ref('');
const scrollableDiv = ref(null);
const scrollToBottom = async () => {
  await nextTick();
  const element = scrollableDiv.value;
  element.scrollTop = element.scrollHeight;
};
let isAIWriting = ref(false);
let searchResult = ref({});
const textareaValue = ref('');


const attachmentTypes = [
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
  { extension: null, name: "Aucune" },
]

const attachmentSelected = ref(null)

let emailsLinked = ref('');

const contacts = [];
const queryGetContacts = ref('')
const selectedPerson = ref(null)
const selectedRecipients = ref([])

const selectedFromPerson = ref(null)
const selectedFromAddresses = ref([])


const filteredFromPeople = computed(() =>
  queryGetContacts.value === ''
    ? contacts
    : contacts.filter((person) => {
      return person.username.toLowerCase().includes(queryGetContacts.value.toLowerCase())
    })
)

const filteredPeople = computed(() =>
  queryGetContacts.value === ''
    ? contacts
    : contacts.filter((person) => {
      return person.username.toLowerCase().includes(queryGetContacts.value.toLowerCase())
    })
)

const toggleSelection = (person) => {
  const index = selectedRecipients.value.findIndex((recipient) => recipient.email === person.email)
  if (index === -1) {
    selectedRecipients.value.push(person)
  } else {
    selectedRecipients.value.splice(index, 1)
  }
}

const removeRecipient = (recipient) => {
  const index = selectedRecipients.value.findIndex((r) => r.email === recipient.email)
  if (index !== -1) {
    selectedRecipients.value.splice(index, 1)
  }
}


const toggleSelectionFromAddress = (person) => {
  const index = selectedFromAddresses.value.findIndex((recipient) => recipient.email === person.email)
  if (index === -1) {
    selectedFromAddresses.value.push(person)
  } else {
    selectedFromAddresses.value.splice(index, 1)
  }
}

const removeRecipientFromAddress = (recipient) => {
  const index = selectedFromAddresses.value.findIndex((r) => r.email === recipient.email)
  if (index !== -1) {
    selectedFromAddresses.value.splice(index, 1)
  }
}

const requestOptions = {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
  },
}
fetchWithToken(`${API_BASE_URL}user/contacts/`, requestOptions)
  .then(response => {
    contacts.push(...response);
  })
  .catch(error => {
    backgroundColor = 'bg-red-300';
    notificationTitle.value = 'Erreur récupération des contacts';
    notificationMessage.value = error;
    displayPopup();
  });





// Mounted lifecycle hook
onMounted(async () => {
  getBackgroundColor();
  fetchEmailLinked();
  bgColor.value = localStorage.getItem('bgColor');

  AIContainer.value = document.getElementById('AIContainer');

  await askQueryUser();
});


async function fetchEmailLinked() {
  const requestOptions = {
    headers: {
      'Content-Type': 'application/json'
    }
  };

  try {
    const response = await fetchWithToken(`${API_BASE_URL}user/emails_linked/`, requestOptions);

    if ("error" in response) {
      // Show the pop-up
      backgroundColor = 'bg-red-300';
      notificationTitle = 'Erreur récupération des emails liés';
      notificationMessage = response.error;
      displayPopup();
    } else {
      emailsLinked.value = response;
    }
  } catch (error) {
    // Show the pop-up
    backgroundColor = 'bg-red-300';
    notificationTitle = 'Erreur récupération des emails liés';
    notificationMessage = error.message;
    displayPopup();
  }
}

// ULTRA IMPORTANT: THIS FUNCTION IS LIKE SEARCH MANUALLY BUT WITH USER STRING INPUT
// async function handleAIClick() {

//   if (isAIWriting.value) {
//     return;
//   }
//   isAIWriting.value = true;

//   loading();
//   scrollToBottom();


//   const emailsLinkedSelected = emailsLinked.value.map(e => e.email)


//   const requestOptions = {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({
//       emails: emailsLinkedSelected,
//       query: textareaValue.value
//     }),
//   };

//   textareaValue.value = "";
//   const result = await fetchWithToken(`${API_BASE_URL}user/search_emails_ai/`, requestOptions);
//   searchResult.value = result;
//   hideLoading();
//   isAIWriting.value = false;
// }

// THIS FUNCTION IS USED TO ANSWER A USER QUESTION WITH TREE KNOWLEDGE
async function handleAIClick() {
  if (isAIWriting.value) {
    return;
  }
  isAIWriting.value = true;

  loading();
  scrollToBottom();

  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      question: textareaValue.value
    }),
  };

  textareaValue.value = "";

  try {
    const result = await fetchWithToken(`${API_BASE_URL}user/search_tree_knowledge/`, requestOptions);

    const aiIcon = '<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />';

    let message = '';
    if (result.error) {
      // Show the pop-up
      backgroundColor = 'bg-red-300';
      notificationTitle = 'Erreur answer tree knowledge a trad en fr et fo faire court';
      notificationMessage = result.error;
      displayPopup();
    } else if (result.message) {
      message = "You do not have enough data to answer the question";
    } else {
      const { sure, answer, emails } = result.answer;
      message = answer;

      if (!sure) {
        message += "\n\nVoici les emails pour que vous vérifier par vous-même: " + emails.join(', ');
      }
    }

    await displayMessage(message, aiIcon);
  } catch (error) {
    console.error('Error fetching AI response:', error);
    await displayMessage('An error occurred while processing your request. Please try again later.', aiIcon);
  } finally {
    hideLoading();
    isAIWriting.value = false;
  }
}

async function searchEmails() {
  // TODO: add a list choice and not a UNIQUE choice
  let fileExt = "";
  for (const key in attachmentSelected.value) {
    if (key === "extension") {
      fileExt = attachmentSelected.value[key];
    }
  }

  // TODO
  // une case par compte à cocher (email)
  // un bouton cocher TOUS (email)
  const toAddressesSelected = selectedRecipients.value.map(recipient => recipient.email);
  const from_addressesSelected = selectedFromAddresses.value.map(recipient => recipient.email);
  const emailsLinkedSelected = emailsLinked.value.map(e => e.email)

  loading();
  scrollToBottom();

  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      emails: emailsLinkedSelected,
      from_addresses: from_addressesSelected,
      to_addresses: toAddressesSelected,
      subject: "",
      body: "",
      date_from: "",
      file_extensions: [fileExt],
      advanced: false,
      search_in: {},
      query: query.value,
      max_results: 100
    }),
  };

  const result = await fetchWithToken(`${API_BASE_URL}user/search_emails/`, requestOptions);
  searchResult.value = result;
  hideLoading();
}


















async function displayMessage(message, ai_icon) {
  // Function to display a message from the AI Assistant

  isAIWriting.value = true;
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
  await animateText(message, animatedParagraph);
  scrollToBottom();
}
async function waitForAIWriting() {
  while (isAIWriting.value) {
    await new Promise(resolve => setTimeout(resolve, 500));
  }
}
async function animateText(text, target) {
  let characters = text.split("");
  let currentIndex = 0;
  const interval = setInterval(() => {
    if (currentIndex < characters.length) {
      target.textContent += characters[currentIndex];
      currentIndex++;
    } else {
      clearInterval(interval);
      isAIWriting.value = false;
    }
  }, 30);
}

async function askQueryUser() {
  // const message = "Bonjour, quel email recherchez vous. Pouvez vous me donner un contexte ?";
  // const ai_icon = '<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />';
  // await displayMessage(message, ai_icon);

  // Wait for isAIWriting to become false
  await waitForAIWriting();

  //const message1 = "Cette page est non fonctionnelle et en cours de développement";
  const message1 = "Recherche avec IA désactivée ❌ | Connaissance arborescente activée ✅";
  const ai_icon1 = '<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />';
  await displayMessage(message1, ai_icon1);
}

// To handle the input going to wide 
const adjustHeight = (event) => {
  const textarea = event.target;
  const maxHeight = 250; // Set your desired max height in pixels

  // Reset height to auto to correctly calculate the new scrollHeight
  textarea.style.height = 'auto';

  if (textarea.scrollHeight > maxHeight) {
    textarea.style.height = `${maxHeight}px`;
    textarea.style.overflowY = 'auto'; // Enable scrolling when content exceeds maxHeight.
  } else {
    textarea.style.height = `${textarea.scrollHeight}px`;
    textarea.style.overflowY = 'hidden'; // Hide the scrollbar when content is below maxHeight.
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




function dismissPopup() {
  showNotification = false;
  clearTimeout(timerId);
}

function displayPopup() {
  showNotification = true;
  timerId = setTimeout(() => {
    dismissPopup();
  }, 4000);
}
</script>
