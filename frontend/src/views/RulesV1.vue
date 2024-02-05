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
        class="col-span-10 2xl:col-span-6 bg-white rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg h-[750px] w-[1250px] 2xl:h-[850px] 2xl:w-[1400px]">
        <div class="flex flex-col">
          <div class="divide-y divide-gray-300">
            <div
              class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-400 bg-opacity-10">
              <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
              <h1 class="font-semibold">Règles de l'Assistant</h1>
            </div>
            <SearchbarV2></SearchbarV2>
          </div>
          <div class="overflow-y-auto" style="margin-right: 2px;">
            <div class="flex-grow p-6">
              <div
                class="flex items-center justify-center w-full lg:h-[555px] 2xl:h-[655px] rounded-lg border-2 border-dashed border-gray-300 text-center">
                <div class="flex-col">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                    stroke="currentColor" class="w-12 h-12 mx-auto text-gray-400">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                  </svg>
                  <span class="mt-2 block text-sm font-semibold text-gray-900">Cliquez pour créer une règle</span>
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
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon } from '@heroicons/vue/20/solid'

const items = [
  { name: 'Envoyer à une heure', href: '#' },
]
</script>

<script>
import Navbar from './components/Navbar7.vue';
import Navbar2 from './components/Navbar8.vue';
import SearchbarV2 from './components/SearchbarV2.vue'

import {
  ChatBubbleOvalLeftEllipsisIcon,
  FaceFrownIcon,
  MagnifyingGlassIcon,
  UserIcon,
  AdjustmentsHorizontalIcon,
} from '@heroicons/vue/24/outline'

export default {
  components: {
    Navbar,
    Navbar2,
    SearchbarV2,
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
