<template>
  <div class="flex flex-col justify-center items-center h-screen" :class="bgColor">
    <div class="grid grid-cols-11 2xl:grid-cols-7 gap-8 2xl:gap-6">
      <div class="col-span-1 2xl:col-span-1">
        <div class="2xl:hidden h-full">
          <navbar></navbar>
        </div>
        <div class="hidden 2xl:block h-full">
          <navbar2></navbar2>
        </div>
      </div>
      <div class="col-span-10 2xl:col-span-6 bg-white rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg xl:h-[93vh] xl:w-[86vw] 2xl:h-[825px] 2xl:w-[1450px]"> <!-- OLD VALUE w : 1400px or 1424px h : 825px -->
        <div class="flex flex-col h-full divide-y divide-gray-200">
          <div class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-50"> <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
            <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">Répondre plus tard</h1>
          </div>
          <div class="flex-grow overflow-y-auto" style="margin-right: 2px;">
            <div class="p-6 h-full">
              <!-- IF AT LEAST ONE RULE EXIST -->
              <!--
              <ul v-if="rules.length > 0" category="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
                <li v-for="rule in rules" :key="rule.email" class="col-span-1 divide-y divide-gray-200 rounded-lg bg-white border-2 border-gray-100 hover:border-3 hover:border-gray-300 hover:shadow-sm relative">
                  <div class="absolute right-4 top-4">
                    <TrashIcon class="w-6 h-6 text-gray-300 hover:text-gray-400" />
                  </div>
                  <div class="flex w-full items-center justify-between space-x-6 p-6">
                    <div class="flex-1 truncate">
                      <div class="flex items-center space-x-3">
                        <h3 class="truncate text-sm font-medium text-gray-900">{{ rule.name }}</h3>
                      </div>
                      <p class="mt-1 mb-4 truncate text-sm text-gray-500">{{ rule.email }}</p>
                      <div v-if="rule.category !== ''" class="flex gap-1">
                        <div class="flex space-x-1 items-center">
                          <ArchiveBoxIcon class="w-4 h-4" />
                          <p class="font-semibold text-sm">Catégorie :</p>
                        </div>
                        <span class="inline-flex flex-shrink-0 items-center rounded-full bg-gray-50 px-1.5 py-0.5 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/20">{{ rule.category }}</span>
                      </div>
                      <div v-if="rule.priority !== ''" class="flex gap-1 mt-2">
                        <div class="flex space-x-1 items-center">
                          <ExclamationCircleIcon class="w-4 h-4" />
                          <p class="font-semibold text-sm">Priorité :</p>
                        </div>
                        <span v-if="rule.priority === 'Important'" class="inline-flex flex-shrink-0 items-center rounded-full bg-red-50 px-1.5 py-0.5 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/20">{{ rule.priority }}</span>
                        <span v-if="rule.priority === 'Informatif'" class="inline-flex flex-shrink-0 items-center rounded-full bg-blue-50 px-1.5 py-0.5 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-600/20">{{ rule.priority }}</span>
                        <span v-if="rule.priority === 'Inutile'" class="inline-flex flex-shrink-0 items-center rounded-full bg-gray-50 px-1.5 py-0.5 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/20">{{ rule.priority }}</span>
                      </div>
                      <div v-if="rule.mail_stop === 'true'" class="flex gap-1 mt-2">
                        <div class="flex space-x-1 items-center">
                          <ShieldCheckIcon class="w-4 h-4" />
                          <p class="font-semibold text-sm">Mail bloqués</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              </ul> -->
              <div v-if="nbr_reply_answer == 0" class="flex items-center justify-center w-full h-full rounded-lg border-2 border-dashed border-gray-300 text-center" @click="showModal = true">
                <div class="flex-col">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 mx-auto text-gray-400">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 15 3 9m0 0 6-6M3 9h12a6 6 0 0 1 0 12h-3" />
                  </svg>
                  <span class="mt-2 block text-sm font-semibold text-gray-900">Aucun mail à répondre plus tard</span>
                </div>
              </div>
              <div v-if="nbr_reply_answer > 0">
                <ul role="list" class="flex flex-col w-full h-full rounded-xl">
                  <li v-if="emails[selectedTopic] && emails[selectedTopic]['Important'] && emails[selectedTopic]['Important'].length > 0" class="py-10 px-8 mx-4 my-4 rounded-xl bg-red-100 bg-opacity-50 hover:border border-red-700 border-opacity-20"> <!-- ring-1 ring-red-700 ring-opacity-20 -->
                      <div class="float-right mt-[-25px] mr-[-10px]">
                          <exclamation-triangle-icon class="w-6 h-6 text-red-500" />
                      </div>
                      <!-- Your content -->
                      <div class="flex">
                          <div class="flex">
                              <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-red-400 dark:bg-red-200">
                                  <span class="text-lg font-medium leading-none text-white dark:text-red-400">AO</span>
                              </span>
                              <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-500" />-->
                          </div>
                          <div class="ml-6 flex-grow">
                              <div class="overflow-hidden border-l-4 border-red-500  hover:rounded-l-xl dark:border-red-300">
                                  <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                      <li v-for="item in emails[selectedTopic]['Important']" :key="item.id" class="px-6 py-4 hover:bg-opacity-70 dark:hover:bg-red-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center" @click="toggleHiddenParagraph(item.id)">
                                          <div class="col-span-8">
                                              <div class="flex-auto">
                                                  <div class="flex items-baseline justify-between gap-x-4">
                                                      <p class="text-sm font-semibold leading-6 text-red-700 dark:text-white">{{ item.name }}</p>
                                                  </div>
                                                  <p class="mt-1 text-md text-gray-700 leading-relaxed dark:text-red-50">{{ item.description }}</p>
                                              </div>
                                              <ul v-show="showHiddenParagraphs[item.id]" role="list" class="text-black text-sm/6 pt-2" :ref="'parentElement' + item.id">
                                                  <li v-for="detail in item.details" :key="detail.id" class="pl-8 my-2" :ref="'hiddenText' + item.id" :data-text="'- ' + detail.text">
                                                  </li>
                                              </ul>
                                          </div>
                                          <div class="col-span-2">
                                              <div class="flex justify-center">
                                                  <span class="isolate inline-flex rounded-2xl">
                                                      <div class="group">
                                                          <button @click="openInNewWindow(item.id_provider)" type="button" class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                              <eye-icon class="w-5 h-5 text-red-500 group-hover:text-white" />
                                                          </button>
                                                      </div>
                                                      <div class="group">
                                                          <button type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                              <check-icon class="w-5 h-5 text-red-500 group-hover:text-white" />
                                                          </button>
                                                      </div>
                                                      <div class="group">
                                                          <button @click="openAnswer(item)" type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                              <arrow-uturn-left-icon class="w-5 h-5 text-red-500 group-hover:text-white" />
                                                          </button>
                                                      </div>
                                                      <div class="group">
                                                          <button type="button" class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                              <ellipsis-horizontal-icon class="w-5 h-5 text-red-500 group-hover:text-white" />                                                        
                                                          </button>
                                                      </div>
                                                  </span> 
                                              </div>
                                              <!--
                                              <span class="isolate inline-flex rounded-2xl">
                                                  <button type="button" class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 border-r border-red-300 hover:bg-gray-50 focus:z-10">
                                                      <span class="sr-only">Previous</span>
                                                      <eye-icon class="w-5 h-5 text-red-500" />
                                                  </button>
                                                  <button type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 border-l border-red-300 hover:bg-gray-50 focus:z-10">
                                                      <check-icon class="w-5 h-5 text-red-500" />
                                                  </button>
                                                  <button type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 border-l border-red-300 hover:bg-gray-50 focus:z-10">
                                                      <arrow-uturn-left-icon class="w-5 h-5 text-red-500" />
                                                  </button>
                                                  <button type="button" class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-gray-400 border-l border-red-300 hover:bg-gray-50 focus:z-10">
                                                      <ellipsis-horizontal-icon class="w-5 h-5 text-red-500" />                                                        
                                                  </button>
                                              </span>-->
                                              
                                          </div>
                                      </li>
                                  </ul>
                              </div>
                          </div>
                      </div>
                  </li>
                  <!-- More items... -->
                  <li v-if="emails[selectedTopic] && emails[selectedTopic]['Information'] && emails[selectedTopic]['Information'].length > 0" class="py-10 px-8 mx-4 my-4 rounded-xl bg-blue-100 bg-opacity-50 hover:border border-blue-700 border-opacity-20 w-full"> <!-- ring-1 ring-blue-700 ring-opacity-20 -->
                      <div class="float-right mt-[-25px] mr-[-10px]">
                          <information-circle-icon class="w-6 h-6 text-blue-500" />
                      </div>
                      <!-- Your content -->
                      <div class="flex">
                          <div class="flex">
                              <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-blue-500 dark:bg-blue-200">
                                  <span class="text-lg font-medium leading-none text-white dark:text-gray-800">AO</span>
                              </span>
                              <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-blue-800" />-->
                          </div>
                          <div class="ml-6 flex-grow">
                              <div class="overflow-hidden border-l-4 hover:rounded-l-xl border-blue-300 dark:bg-blue-500">
                                  <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                      <li v-for="item in emails[selectedTopic]['Information']" :key="item.id" class="px-6 py-4 hover:bg-opacity-70 dark:hover:bg-blue-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center" @click="toggleHiddenParagraph(item.id)">
                                          <div >
                                              <div class="col-span-8">
                                                  <div class="flex-auto">
                                                      <div class="flex items-baseline justify-between gap-x-4">
                                                          <p class="text-sm font-semibold leading-6 text-blue-800 dark:text-white">{{ item.name }}</p>
                                                      </div>
                                                      <p class="mt-1 text-md text-gray-700 leading-relaxed dark:text-blue-50">{{ item.description }}</p>
                                                  </div>
                                                  <ul v-show="showHiddenParagraphs[item.id]" role="list" class="text-black text-sm/6 pt-2" :ref="'parentElement' + item.id">
                                                      <li v-for="detail in item.details" :key="detail.id" class="pl-8" :ref="'hiddenText' + item.id" :data-text="detail.text">
                                                      </li>
                                                  </ul>
                                              </div>
                                          </div>
                                      </li>
                                  </ul>
                              </div>
                          </div>
                      </div>
                  </li>
                  <div v-if="emails[selectedTopic] && emails[selectedTopic]['Useless'] && emails[selectedTopic]['Useless'].length" class="flex-1 mx-4 my-4 rounded-xl bg-gray-100 hover:border border-gray-700 border-opacity-20 w-full">
                      <li class="py-10 px-8"> <!-- ring-1 ring-red-700 ring-opacity-20 --> <!-- BUG A CORRIGER : ESPACE BLANC BOTTOM -->
                          <div class="float-right mt-[-25px] mr-[-10px]">
                              <trash-icon class="w-6 h-6 text-gray-500" />
                          </div>
                          <!-- Your content -->
                          <div class="flex">
                              <div class="flex">
                                  <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-400 dark:bg-red-200">
                                      <span class="text-lg font-medium leading-none text-white dark:text-red-400">AO</span>
                                  </span>
                                  <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-500" />-->
                              </div>
                              <div class="ml-6 ">
                                  <div class="overflow-hidden border-l-4 hover:rounded-l-xl border-gray-500 dark:border-red-300" @click="toggleHiddenParagraph(3)">
                                      <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                          <li class="px-6 py-4 dark:bg-red-500 hover:bg-opacity-70 dark:hover:bg-opacity-100">
                                              <div class="flex-auto">
                                                  Vous avez reçu <span class="font-semibold text-gray-800 dark:text-white hover:text-gray-700">4</span> mails inutiles. Cliquez pour voir.
                                              </div>
                                              <ul role="list" v-show="showHiddenParagraphs[3]" class="text-gray-800 text-sm/6 pt-2" ref="parentElement3">
                                                  <li class="pl-8" ref="hiddenText3" data-text="- Fabien Huet est en vacances dans les Alpes."></li>
                                                  <li class="pl-8" ref="hiddenText3" data-text="- Il demande à recevoir les différentes informations pour le BP afin d'avancer rapidement sur le sujet."></li>
                                                  <li class="pl-8" ref="hiddenText3" data-text="- Il souhaite également prendre rendez-vous avec son expert-comptable d'ici la fin du mois."></li>
                                              </ul>
                                          </li>
                                          <!-- More items... -->
                                      </ul>
                                  </div>
                              </div>
                          </div>
                      </li>
                  </div>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <ModalSeeRule :isOpen="showModal" @update:isOpen="updateModalStatus" :emailSenders="emailSenders" :categories="categories" />
</template>

<script setup>
import { onMounted, ref } from 'vue';
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';
import { fetchWithToken } from '../router/index.js';


// Main variables
const bgColor = ref('');
const answerLaterEmails = ref([]);
const emails = ref({});
const nbr_reply_answer = ref(0);

// Mounted lifecycle hook
onMounted(() => {

  bgColor.value = localStorage.getItem('bgColor');
  fetchAnswerLaterEmails();

});
// To fetch the email to reply later
async function fetchAnswerLaterEmails() {
  try {
    const data = await fetchWithToken('http://localhost:9000/MailAssistant/api/get_answer_later_emails/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    console.log("DATA", data);
    emails.value = data; // Assuming emails is a reactive variable
    console.log("Length", Object.keys(emails.value).length);
    nbr_reply_answer.value = Object.keys(emails.value).length; // Assuming nbr_reply_answer is a reactive variable
    answerLaterEmails.value = data; // Update the reactive variable with the fetched emails
  } catch (error) {
    console.error("Error fetching answer-later emails:", error.message);
  }
}
</script>