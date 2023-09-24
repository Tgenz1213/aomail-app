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
        <div class="grid grid-cols-10 2xl:grid-cols-6 gap-4 2xl:gap-6">
            <div class="col-span-2 2xl:col-span-1">
                <navbar></navbar>
            </div>
            <div class="col-span-8 2xl:col-span-5">
                <div class="flex flex-col h-[750px] w-[1125px] 2xl:h-[850px] 2xl:w-[1424px]">
                    <main class="rounded-xl bg-gray-100 bg-opacity-75 ring-1 shadow-sm ring-black ring-opacity-5">
                        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                        <div class="flex items-center pb-5">
                            <div class="w-full flex items-center justify-center pt-5">
                                <div class="sm:hidden">
                                    <label for="tabs" class="sr-only">Select a tab</label>
                                    <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
                                    <select id="tabs" name="tabs" class="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500">
                                    <option>Ecole ESAIP</option>
                                    <option>Entrepreneuriat</option>
                                    <option selected>Administratif</option>
                                    <option>Autres</option>
                                    </select>
                                </div>
                                <div class="hidden sm:block w-full">
                                    <nav class="flex justify-center space-x-4 w-full" aria-label="Tabs">
                                        <!-- Current: "bg-gray-200 text-gray-800", Default: "text-gray-600 hover:text-gray-800" -->
                                        <div class="flex space-x-2 items-center hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 rounded-md px-8 py-2 ">
                                            <adjustments-vertical-icon class="w-4 h-4" />
                                            <a href="#" class=" text-gray-600 text-sm font-medium">Préférences</a>
                                        </div>
                                        <div class="flex space-x-2 items-center hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 rounded-md px-8 py-2 ">
                                            <user-icon class="w-4 h-4" />
                                            <a href="#" class=" text-gray-600 text-sm font-medium">Mon Compte</a>
                                        </div>
                                        <div class="flex space-x-2 items-center hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 rounded-md px-8 py-2 ">
                                            <credit-card-icon class="w-4 h-4" />
                                            <a href="#" class=" text-gray-600 text-sm font-medium">Abonnement</a>
                                        </div>
                                        <div class="flex space-x-2 items-center bg-gray-500 bg-opacity-10 hover:text-gray-800 rounded-md px-12 py-2 ">
                                            <circle-stack-icon class="w-4 h-4" />
                                            <a href="#" class="text-gray-800 text-sm font-medium" aria-current="page">Mes données</a>
                                        </div>
                                    </nav>
                                </div>
                            </div>
                        </div>
                        </div>
                    </main>
                    <div class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm hover:shadow-lg ring-black ring-opacity-5 hidden"> <!-- DESACTIVATE HIDDEN TO DISPLAY-->
                        <div class="flex px-6 py-6 shadow-sm border-b border-gray-200 bg-gray-50 rounded-t-2xl">
                          <h1 class="text-2xl" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Mon compte</h1>         
                        </div>
                        <div class="float-right mt-[-70px] mr-[10px]">
                          <user-icon class="w-6 h-6 text-gray-500" />
                        </div>
                        <!-- TO DO : CENTER -->
                        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-10">
                            <!-- We've used 3xl here, but feel free to try other max-widths based on your needs -->
                            <div class="mx-auto max-w-lg">
                              <!-- Content goes here -->
                              <div class="flex flex-col">
                                <div class="relative">
                                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                    <div class="w-full border-t border-gray-300"></div>
                                  </div>
                                  <div class="relative flex justify-center">
                                    <span class="bg-white px-2 text-sm text-gray-500">Changement d'Email ou Mot de Passe</span>
                                  </div>
                                </div>
                                <div class="pt-6 pb-10">
                                  <div class="flex space-x-1 items-center">
                                    <envelope-icon class="w-4 h-4" />
                                    <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email</label>
                                  </div>
                                  <div class="relative items-stretch mt-2">
                                    <input type="text" name="first-name" id="first-name" value="theohubert3@gmx.com" autocomplete="given-name" class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6">
                                  </div>
                                  <div class="pt-4">
                                    <div class="flex space-x-1 items-center">
                                      <key-icon class="w-4 h-4" />
                                      <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Nouveau mot de passe</label>
                                    </div>
                                    <div class="relative items-stretch mt-2">
                                      <input type="text" name="first-name" id="first-name" autocomplete="given-name" class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6">
                                    </div>
                                  </div>
                                  <div class="pt-4">
                                    <div class="flex space-x-1 items-center">
                                      <key-icon class="w-4 h-4" />
                                      <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Confirmer le mot de passe</label>
                                    </div>
                                    <div class="relative items-stretch mt-2">
                                      <input type="text" name="first-name" id="first-name" autocomplete="given-name" class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6">
                                    </div>
                                  </div>
                                  <div class="flex justify-end pt-4">
                                    <button type="submit" class="rounded-md bg-gray-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Modifier</button>
                                  </div>
                                </div>
                                <div class="relative">
                                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                    <div class="w-full border-t border-gray-300"></div>
                                  </div>
                                  <div class="relative flex justify-center">
                                    <span class="bg-white px-2 text-sm text-gray-500">Suppression du compte</span>
                                  </div>
                                </div>
                                <div class="pt-6">
                                  <div class="flex space-x-1 items-center">
                                    <input type="radio" class="form-radio text-red-600 border-red-400 focus:border-red-500 focus:ring-red-200 h-5 w-5" name="choice">
                                    <label for="push-everything" class="block text-sm font-medium leading-6">Je confirme la supression de mon compte (action irréversible)</label>
                                  </div>
                                  <div class="flex justify-end pt-4">
                                    <button type="submit" class="rounded-md bg-red-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500">Supprimer</button>
                                  </div>
                                </div>
                              </div>
                            </div>
                        </div>    
                    </div>
                    <div class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm hover:shadow-lg ring-black ring-opacity-5"> 
                        <div class="flex px-6 py-6 shadow-sm border-b border-gray-200 bg-gray-50 rounded-t-2xl">
                          <h1 class="text-2xl" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Mes préférences</h1>         
                        </div>
                        <div class="float-right mt-[-70px] mr-[10px]">
                          <adjustments-vertical-icon class="w-6 h-6 text-gray-500" />
                        </div>
                        <!-- TO DO : CENTER -->
                        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-10">
                            <!-- We've used 3xl here, but feel free to try other max-widths based on your needs -->
                            <div class="mx-auto max-w-lg">
                              <!-- Content goes here -->
                              <div class="flex flex-col">
                                <div class="relative">
                                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                    <div class="w-full border-t border-gray-300"></div>
                                  </div>
                                  <div class="relative flex justify-center">
                                    <span class="bg-white px-2 text-sm text-gray-500">Thème</span>
                                  </div>
                                </div>
                                <div class="pt-6 pb-10">
                                  <div class="relative items-stretch mt-2">
                                    <theme></theme>
                                  </div>
                                </div>
                                <div class="relative">
                                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                    <div class="w-full border-t border-gray-300"></div>
                                  </div>
                                  <div class="relative flex justify-center">
                                    <span class="bg-white px-2 text-sm text-gray-500">Couleurs</span>
                                  </div>
                                </div>
                                <div class="pt-6">
                                  <color></color>
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
import Navbar from './components/Navbar8.vue';
import Theme from './components/SettingsTheme.vue';
import Color from './components/SettingsColor.vue';
import {
  ChatBubbleOvalLeftEllipsisIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  TrashIcon,
  ArrowUturnLeftIcon,
  CheckIcon,
  AdjustmentsVerticalIcon,
  UserIcon,
  CreditCardIcon,
  CircleStackIcon,
  EnvelopeIcon,
  KeyIcon
} from '@heroicons/vue/24/outline'

export default {
  components: {
    Navbar,
    Theme,
    Color,
    ChatBubbleOvalLeftEllipsisIcon,
    ExclamationTriangleIcon,
    InformationCircleIcon,
    TrashIcon,
    ArrowUturnLeftIcon,
    CheckIcon,
    AdjustmentsVerticalIcon,
    UserIcon,
    CreditCardIcon,
    CircleStackIcon,
    EnvelopeIcon,
    KeyIcon
  },
  methods: {
    animateText() {
      let text = "Bonjour ! Vous avez reçu 4 nouveaux mails.";
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
  },
  data() {
    return {
      showHiddenParagraphs: [false, false, false],
      animationTriggered: [false, false, false]
    }
  }
}
</script>
