<template>
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
              class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-400 bg-opacity-10">
              <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
              <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">Assistant IA</h1>
            </div>
            <div class="flex flex-col divide-y xl:h-[85vh] 2xl:h-[785px]">
              <div class="overflow-y-auto xl:h-[75vh] 2xl:h-[700px]" style="margin-right: 2px;" ref="scrollableDiv">
                <div class="px-10 py-4">
                  <div class="flex-grow">
                    <div id="AIContainer">
                    </div>
                  </div>
                </div>
              </div>
              <div class="flex-grow">
                <div class="flex px-6 2xl:py-10 pb-6 pt-4 relative w-full"><!-- Old value (26/12/2023) -->
                  <div class="flex flex-grow items-stretch">
                    <textarea id="dynamicTextarea" @input="adjustHeight" v-model="textareaValue"
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
            class="flex flex-col flex-grow divide-y divide-gray-200 bg-white rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg h-full xl:w-[43vw] 2xl:w-[700px]">
            <!--xl:h-[695px] xl:w-[560px]-->
            <div
              class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-400 bg-opacity-10">
              <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
              <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">Recherche Manuelle</h1>
            </div>
            <div class="flex flex-col flex-grow">
              <div class="flex flex-col w-full px-6 pt-6">
                <div class="flex space-x-1 items-center">
                  <magnifying-glass-icon class="w-4 h-4" />
                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Recherche</label>
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
                      class="w-28 rounded-md bg-gray-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Rechercher</button>
                  </div>
                </div>
              </div>
              <div class="flex flex-col w-full px-6 pt-4">
                <div class="grid grid-cols-2 gap-4">
                  <div class="col-span-1 shadow-sm">
                    <div class="flex space-x-1 items-center">
                      <user-icon class="w-4 h-4" />
                      <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Contacts
                        (optionnel)</label>
                    </div>
                    <div class="relative items-stretch mt-2">
                      <search-contact></search-contact>
                    </div>
                  </div>
                  <div class="col-span-1 shadow-sm">
                    <div class="flex space-x-1 items-center">
                      <adjustments-horizontal-icon class="w-4 h-4" />
                      <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Type de recherche
                        (optionnel)</label>
                    </div>
                    <div class="relative items-stretch mt-2">
                      <search-type></search-type>
                    </div>
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
                          <li v-if="searchResult.Gmail" v-for="item in searchResult.Gmail" :key="item"
                            class="px-6 md:py-6 2xl:py-6 hover:bg-opacity-70 dark:hover:bg-red-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center">
                            <p class="text-sm font-semibold leading-6 text-red-700 dark:text-white">{{ item }}</p>
                          </li>
                          <li v-if="searchResult.Outlook" v-for="item in searchResult.Outlook" :key="item"
                            class="px-6 md:py-6 2xl:py-6 hover:bg-opacity-70 dark:hover:bg-red-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center">
                            <p class="text-sm font-semibold leading-6 text-red-700 dark:text-white">{{ item }}</p>
                          </li>
                        </ul>
                        <div v-else>
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                            stroke="currentColor" class="w-12 h-12 mx-auto text-gray-400">
                            <path stroke-linecap="round" stroke-linejoin="round"
                              d="M15.182 16.318A4.486 4.486 0 0012.016 15a4.486 4.486 0 00-3.198 1.318M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
                          </svg>
                          <span class="mt-2 block text-sm font-semibold text-gray-900">Aucun résultat</span>
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
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, nextTick } from 'vue';
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';
import SearchContact from '../components/SearchContact.vue';
import SearchType from '../components/SearchType.vue';
import { fetchWithToken, getBackgroundColor } from '../router/index.js';
import { API_BASE_URL } from '@/main';
import {
  MagnifyingGlassIcon,
  UserIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/vue/24/outline';

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

// Mounted lifecycle hook
onMounted(async () => {
  getBackgroundColor();
  bgColor.value = localStorage.getItem('bgColor');

  AIContainer.value = document.getElementById('AIContainer');

  await askQueryUser();
});

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
  const message = "Bonjour, quel email recherchez vous. Pouvez vous me donner un contexte ?";
  const ai_icon = '<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />';
  await displayMessage(message, ai_icon);

  // Wait for isAIWriting to become false
  await waitForAIWriting();

  const message1 = "Cette page est non fonctionnelle et en cours de développement";
  const ai_icon1 = '<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />';
  await displayMessage(message1, ai_icon1);
}

async function searchEmails() {
  loading();
  scrollToBottom();

  // TODO
  // une case par compte à cocher (email)
  // un bouton cocher TOUS (email)
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      emails: ["augustin.rolet.pro@gmail.com", "augustin@MailAssistant.onmicrosoft.com"],
      query: query.value
    }),
  };

  const result = await fetchWithToken(`${API_BASE_URL}user/search_emails/`, requestOptions);
  console.log(result);
  searchResult.value = result;
  hideLoading();
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
};


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
</script>
