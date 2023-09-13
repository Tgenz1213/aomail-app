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
        <div class="col-span-5 2xl:col-span-3 bg-gray-100 bg-opacity-75 rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg h-[750px] w-[625px] 2xl:h-[850px] 2xl:w-[700px]">
          <div class="flex flex-col divide-y divide-gray-300">
            <div class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-400 bg-opacity-10"> <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
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
                    <div class="flex pb-12">
                      <div class="mr-4 flex">
                          <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-indigo-500">
                              <span class="text-lg font-medium leading-none text-white">AO</span>
                          </span>   
                          <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-indigo-800" />-->
                      </div>
                      <div>
                          <p>Bonjour ceci est un test !</p>
                      </div>
                    </div>
                    <div class="flex pb-12">
                      <div class="mr-4 flex">
                          <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-indigo-500">
                              <span class="text-lg font-medium leading-none text-white">AO</span>
                          </span>   
                          <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-indigo-800" />-->
                      </div>
                      <div>
                          <p>Bonjour ceci est un test !</p>
                      </div>
                    </div>
                    <div class="flex pb-12">
                      <div class="mr-4 flex">
                          <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-indigo-500">
                              <span class="text-lg font-medium leading-none text-white">AO</span>
                          </span>   
                          <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-indigo-800" />-->
                      </div>
                      <div>
                          <p>Bonjour ceci est un test !Bonjour ceci est un test ! Bonjour ceci est un test ! Bonjour ceci est un test ! Bonjour ceci est un test !</p>
                      </div>
                    </div>
                    <div class="flex pb-12">
                      <div class="mr-4 flex">
                          <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-indigo-500">
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
                          <textarea id="dynamicTextarea" @input="adjustHeight" class="left-0 pl-3 only:block w-full rounded-none rounded-l-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" placeholder="Instruction"></textarea>
                        </div>
                        <button type="button" class="relative -ml-px inline-flex items-center gap-x-1.5 rounded-r-md px-3 py-2.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 bg-gray-50 hover:bg-gray-50 z-50">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" stroke-width="1.5" stroke="rgb(243 244 246)" class="w-6 h-6 text-gray-400">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-span-5 2xl:col-span-3 bg-white rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg h-[750px] w-[625px] 2xl:h-[850px] 2xl:w-[700px]">
         <div class="flex flex-col divide-y divide-gray-200">
            <div class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-50">
              <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">Saisi manuel</h1>
            </div>
            <div class="space-y-12 px-10">
              <form>
                <div class="mt-10 2xl:mt-24 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                    <div class="sm:col-span-full">
                        <div class="flex space-x-1 items-center">
                          <UserGroupIcon class="w-4 h-4" />
                          <label for="username" class="block text-sm font-medium leading-6 text-gray-900">Destinaire(s)</label>
                        </div>
                        <div class="mt-2">
                          <div class="flex items-stretch gap-1">
                            <div class="flex-grow">
                              <div class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 w-full max-w-2xl">
                                  <input type="text" name="username" id="username" autocomplete="username" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="janesmith">
                              </div>
                            </div>
                            <div class="flex">
                              <button type="button" class="inline-flex items-center gap-x-1.5 rounded-md bg-gray-100 px-2.5 py-1.5 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-300 shadow-sm hover:ring-gray-800 hover:bg-gray-500 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                                CC
                              </button>
                            </div>
                            <div class="flex">
                              <button type="button" class="inline-flex items-center gap-x-1.5 rounded-md bg-gray-100 px-2.5 py-1.5 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-300 shadow-sm hover:ring-gray-800 hover:bg-gray-500 hover:text-white  focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                                CCI
                              </button>
                            </div>
                          </div>
                        </div>
                    </div>
                    <div class="sm:col-span-full">
                        <div class="flex space-x-1 items-center">
                          <Bars2Icon class="w-4 h-4" />
                          <label for="username" class="block text-sm font-medium leading-6 text-gray-900">Objet</label>
                        </div>
                        <div class="mt-2">
                          <div class="flex items-stretch gap-1">
                            <div class="flex-grow">
                              <div class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 w-full max-w-2xl">
                                <input type="text" name="username" id="username" autocomplete="username" class="block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6" placeholder="janesmith">
                              </div>
                            </div>
                            <div class="flex">
                              <button type="button" class="inline-flex items-center gap-x-1.5 rounded-md bg-gray-100 px-2.5 py-1.5 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-300 shadow-sm hover:ring-gray-800 hover:bg-gray-500 hover:text-white  focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13" />
                                </svg>
                              </button>
                            </div>
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
                    <div class="col-span-full h-full">
                      <div class="flex space-x-1 items-center">
                          <Bars3BottomLeftIcon class="w-4 h-4" />
                          <label for="username" class="block text-sm font-medium leading-6 text-gray-900">Message</label>
                        </div>
                        <div class="mt-2">
                            <div id="editor" class="w-full max-w-2xl mx-auto h-60 max-h-60 overflow-y-auto"></div> 
                        </div>
                    </div>
                    <div class="col-span-full h-full">
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
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'

const items = [
  { name: 'Envoyer à une heure', href: '#' },
]
</script>

<script>
import Navbar from './components/Navbar7.vue';
import Navbar2 from './components/Navbar8.vue';

import {
  ChatBubbleOvalLeftEllipsisIcon,
  UserGroupIcon,
  Bars2Icon,
  Bars3BottomLeftIcon
} from '@heroicons/vue/24/outline'

export default {
  components: {
    Navbar,
    Navbar2,
    ChatBubbleOvalLeftEllipsisIcon,
    UserGroupIcon,
    Bars2Icon,
    Bars3BottomLeftIcon
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
  },
  data() {
    return {
      showHiddenParagraphs: [false, false, false],
      animationTriggered: [false, false, false]
    }
  },
}
</script>
