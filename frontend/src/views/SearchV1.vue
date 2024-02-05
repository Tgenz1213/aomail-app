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
  <div class="flex flex-col justify-center items-center h-full">
    <div class="grid grid-cols-11 2xl:grid-cols-7 gap-4 2xl:gap-6">
      <div class="col-span-1 2xl:col-span-1">
        <div class="2xl:hidden">
          <navbar></navbar>
        </div>
        <div class="hidden 2xl:block">
          <navbar2></navbar2>
        </div>
      </div>
      <div
        class="col-span-5 2xl:col-span-3 bg-gray-100 bg-opacity-75 rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg h-[750px] w-[625px] 2xl:h-[850px] 2xl:w-[700px]">
        <div class="flex flex-col divide-y divide-gray-300">
          <div
            class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-400 bg-opacity-10">
            <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
            <!--<h1 class="font-semibold">Assistant IA</h1>-->
            <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">Assistant IA</h1>
          </div>
          <div class="">
            <div class="overflow-y-auto h-[600px] 2xl:h-[700px]" style="margin-right: 2px;">
              <div class="px-10 py-4">
                <div class="flex-grow">
                  <div class="flex pb-12">
                    <div class="mr-4 flex">
                      <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-500">
                        <span class="text-lg font-medium leading-none text-white">AO</span>
                      </span>
                      <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-indigo-800" />-->
                    </div>
                    <div>
                      <p class="mt-1" id="animated-text" ref="animatedText"></p>
                    </div>
                  </div>
                  <div class="flex pb-12">
                    <div class="mr-4 flex">
                      <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-500">
                        <span class="text-lg font-medium leading-none text-white">AO</span>
                      </span>
                      <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-indigo-800" />-->
                    </div>
                    <div>
                      <p>Bonjour ceci est un test !</p>
                    </div>
                  </div>

                </div>
              </div>
            </div>
            <div class="pb-10">
              <div>
                <div class="flex flex-col items-center">
                  <div class="flex rounded-md shadow-sm w-[67vh]">
                    <div class="relative flex flex-grow items-stretch">
                      <textarea id="dynamicTextarea" @input="adjustHeight"
                        class="left-0 pl-3 only:block w-full rounded-none rounded-l-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                        placeholder="Instruction"></textarea>
                    </div>
                    <button type="button"
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
          </div>
        </div>
      </div>
      <div
        class="col-span-5 2xl:col-span-3 bg-white rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg h-[750px] w-[625px] 2xl:h-[850px] 2xl:w-[700px]">
        <div class="flex flex-col divide-y divide-gray-300">
          <div
            class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-400 bg-opacity-10">
            <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
            <!--<h1 class="font-semibold">Recherche Manuel</h1>-->
            <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">Recherche Manuel</h1>
          </div>
          <div class="">
            <div class="flex flex-col w-full px-6 pt-6">
              <div class="flex space-x-1 items-center">
                <magnifying-glass-icon class="w-4 h-4" />
                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Recherche</label>
              </div>
              <div class="flex space-x-2 items-center">
                <div class="flex-grow w-full">
                  <div class="relative flex flex-grow items-stretch mt-2">
                    <input type="text" name="first-name" id="first-name" placeholder="Rechercher"
                      autocomplete="given-name"
                      class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6">
                  </div>
                </div>
                <div class="flex-1 mt-2">
                  <button type="button"
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
            <div class="overflow-y-auto" style="margin-right: 2px;"> <!-- h-[600px] 2xl:h-[700px] -->
              <div class="flex-grow p-6">
                <div
                  class="flex items-center justify-center w-full lg:h-[455px] 2xl:h-[555px] rounded-lg border-2 border-dashed border-gray-300 text-center">
                  <div class="flex-col">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                      stroke="currentColor" class="w-12 h-12 mx-auto text-gray-400">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M15.182 16.318A4.486 4.486 0 0012.016 15a4.486 4.486 0 00-3.198 1.318M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
                    </svg>
                    <span class="mt-2 block text-sm font-semibold text-gray-900">Aucun résultats</span>
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

<script>
import Navbar from './components/Navbar7.vue';
import Navbar2 from './components/Navbar8.vue';
import SearchContact from './components/searchContact.vue'
import SearchType from './components/SearchType.vue'

import {
  ChatBubbleOvalLeftEllipsisIcon,
  FaceFrownIcon,
  MagnifyingGlassIcon,
  UserIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/vue/24/outline'

export default {
  components: {
    Navbar,
    Navbar2,
    SearchContact,
    SearchType,
    ChatBubbleOvalLeftEllipsisIcon,
    FaceFrownIcon,
    MagnifyingGlassIcon,
    UserIcon,
    AdjustmentsHorizontalIcon
  },
  methods: {
    adjustHeight(event) {
      const textarea = event.target;
      textarea.style.height = 'auto';
      textarea.style.height = textarea.scrollHeight + 'px';
    },
    animateText() {
      let text = "Bonjour ! Vous avez reçu 4 nouveaux mails. Rien d'urgent à signaler";
      let target = this.$refs.animatedText;
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
    },
    toggleHiddenParagraph(index) {
      this.showHiddenParagraphs[index] = !this.showHiddenParagraphs[index];
      this.$nextTick(() => {
        if (this.showHiddenParagraphs[index] && !this.animationTriggered[index]) {
          const parentElement = this.$refs['parentElement' + index];
          const elements = parentElement.children;
          console.log("Elements:", elements)

          const delays = [0];
          for (let i = 0; i < elements.length; i++) {
            const duration = this.animateHiddenText(elements[i], delays[i]);
            delays.push(delays[i] + duration + 20);
          }
          this.animationTriggered[index] = true;
        }
      });
    },
    animateHiddenText(element, delay = 0) {
      const characters = element.dataset.text.split('');
      const duration = characters.length * 5;
      setTimeout(() => {
        element.textContent = '';
        let currentIndex = 0;
        const interval = setInterval(() => {
          if (currentIndex < characters.length) {
            element.textContent += characters[currentIndex];
            currentIndex++;
          } else {
            clearInterval(interval);
          }
        }, 5);
      }, delay);
      return duration;
    }
  },
  mounted() {
    this.animateText();

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
    var quill = new Quill('#editor', {
      theme: 'snow',
      modules: {
        toolbar: toolbarOptions
      }
    });
  },
  data() {
    return {
      showHiddenParagraphs: [false, false, false],
      animationTriggered: [false, false, false]
    }
  },
}
</script>
