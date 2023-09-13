<template>
    <navbar></navbar>
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
    <div class="fixed lg:top-4 lg:left-28 lg:right-4 lg:bottom-4 lg:z-50 rounded border bg-white">
    <main class="rounded bg-white border-b">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-8 gap-6 items-center divide-x divide-gray-300">
                <div class="col-span-3 h-full justify-center">
                    <!-- Assistant Up -->
                    <div class="flex pt-6 pb-6">
                        <div class="mr-4 flex-shrink-0 self-center">
                            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-indigo-600">
                                <span class="text-lg font-medium leading-none text-white">AO</span>
                            </span>     
                        </div>
                        <div>
                            <p class="mt-1" id="animated-text" ref="animatedText"></p>
                        </div>
                    </div>
                </div>
                <div class="col-span-5 h-full flex items-center pb-5">
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
                            <a href="#" class=" text-gray-500 hover:bg-gray-200 hover:text-gray-800 rounded-md px-8 py-2 text-sm font-medium">Ecole ESAIP</a>
                            <a href="#" class=" text-gray-500 hover:bg-gray-200 hover:text-gray-800 rounded-md px-8 py-2 text-sm font-medium">Entrepreneuriat</a>
                            <a href="#" class=" text-gray-500 hover:bg-gray-200 hover:text-gray-800 rounded-md px-8 py-2 text-sm font-medium">Administratifs</a>
                            <a href="#" class=" bg-indigo-100 text-indigo-700 rounded-md px-16 py-2 text-sm font-medium" aria-current="page">Autres</a>
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    <div class="lg:pl-20">
            <div class="inline-block w-full px-12 pt-3 pb-3">
                <!-- Content goes here -->
                <ul role="list" class="">
                    <li class="py-10">
                        <!-- Your content -->
                        <div class="grid grid-cols-12 gap-0">
                            <div class="col-span-1">
                                <div class="flex">
                                    <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-red-400 dark:bg-red-200">
                                        <span class="text-lg font-medium leading-none text-white dark:text-gray-800">AO</span>
                                    </span>
                                    <ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-700" />    
                                </div>
                            </div>
                            <div class="col-span-9">
                                <div class="overflow-hidden rounded-md bg-red-50 dark:bg-red-500" @click="toggleHiddenParagraph(0)">
                                    <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                        <li class="px-6 py-4 bg-red-50 dark:bg-red-500 hover:bg-opacity-70 dark:hover:bg-opacity-100">
                                            <div class="flex-auto">
                                                <div class="flex items-baseline justify-between gap-x-4">
                                                    <p class="text-sm font-semibold leading-6 text-red-700">Christophe Rouvrais</p>
                                                </div>
                                                <p class="mt-1 text-md leading-6 text-red-600">Parle de l'aventure entrepreneuriale de Malcom Morel.</p>
                                            </div>
                                            <ul role="list" v-show="showHiddenParagraphs[0]" class="text-gray-800 text-sm/6 pt-2" ref="parentElement0">
                                                <li class="pl-8" ref="hiddenText0" data-text="- Malcom MOREL, un futur étudiant de l'IR4, participe à une aventure entrepreneuriale sur le territoire."></li>
                                                <li class="pl-8" ref="hiddenText0" data-text="- Il est demandé de mettre en place un dispositif d'accompagnement et d'aménagement adapté pour lui."></li>
                                            </ul>
                                        </li>
                                        <!-- More items... -->
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </li>
                    <!-- More items... -->
                    <li class="py-10">
                        <!-- Your content -->
                        <div class="grid grid-cols-12 gap-0">
                            <div class="col-span-1">
                                <div class="flex">
                                    <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-blue-500 dark:bg-blue-200">
                                        <span class="text-lg font-medium leading-none text-white dark:text-gray-800">AO</span>
                                    </span>
                                    <ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-blue-800" />   
                                </div>
                            </div>
                            <div class="col-span-9">
                                <div class="overflow-hidden rounded-md bg-blue-50 dark:bg-blue-500">
                                    <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                        <li class="px-6 py-4 hover:bg-blue-50 dark:hover:bg-blue-500 dark:hover:bg-opacity-100" @click="toggleHiddenParagraph(1)">
                                            <div class="flex-auto">
                                                <div class="flex items-baseline justify-between gap-x-4">
                                                    <p class="text-sm font-semibold leading-6 text-blue-800 dark:text-white">Fabien Huet</p>
                                                </div>
                                                <p class="mt-1 text-md leading-6 text-blue-600 dark:text-blue-50">Parle de ses vacances et son projet d'enteprise</p>
                                            </div>
                                            <ul role="list" v-show="showHiddenParagraphs[1]" class="text-black text-sm/6 pt-2" ref="parentElement1">
                                                <li class="pl-8" ref="hiddenText1" data-text="- Fabien Huet est en vacances dans les Alpes."></li>
                                                <li class="pl-8" ref="hiddenText1" data-text="- Il demande à recevoir les différentes informations pour le BP afin d'avancer rapidement sur le sujet."></li>
                                                <li class="pl-8" ref="hiddenText1" data-text="- Il souhaite également prendre rendez-vous avec son expert-comptable d'ici la fin du mois."></li>
                                            </ul>
                                        </li>
                                        <li class="px-6 py-4 hover:bg-blue-50 dark:hover:bg-blue-500 dark:hover:bg-opacity-100" @click="toggleHiddenParagraph(2)">
                                            <div class="flex-auto">
                                                <div class="flex items-baseline justify-between gap-x-4">
                                                    <p class="text-sm font-semibold leading-6 text-blue-800 dark:text-white">Hannah Williams</p>
                                                </div>
                                                <p class="mt-1 text-md leading-6 text-blue-600 dark:text-blue-50">Donne des conseils pour votre rapport d'étonnement</p>
                                            </div>
                                            <ul role="list" v-show="showHiddenParagraphs[2]" class="text-black text-sm/6 pt-2" ref="parentElement2">
                                                <li class="pl-8" ref="hiddenText2" data-text="- Le message concerne le rapport d'étonnement de Théo à l'Esaip."></li>
                                                <li class="pl-8" ref="hiddenText2" data-text="- L'expéditeur conseille à Théo de s'éloigner d'un rapport d'étonnement traditionnel à la française."></li>
                                                <li class="pl-8" ref="hiddenText2" data-text="- L'expéditeur souhaite lire des informations sur le contexte des stages, comment Théo a trouvé le partenaire/entreprise, leur emplacement et des faits sur l'endroit."></li>
                                                <li class="pl-8" ref="hiddenText2" data-text="- Théo doit également parler de ses tâches et projets, sans entrer dans les détails quotidiens."></li>
                                                <li class="pl-8" ref="hiddenText2" data-text="- L'aspect humain et culturel est également important, en particulier pour la Belgique où il y a une forte identité culturelle séparant la Wallonie francophone et la Flandre néerlandophone."></li>
                                                <li class="pl-8" ref="hiddenText2" data-text="- Enfin, Théo doit faire un résumé et donner un bref retour d'expérience."></li>
                                                <li class="pl-8" ref="hiddenText2" data-text="- Des photos et illustrations sont les bienvenues, ainsi que des sources et références si pertinentes."></li>
                                            </ul>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </li>
                    <li class="py-10">
                        <!-- Your content -->
                        <div class="grid grid-cols-12 gap-0">
                            <div class="col-span-1">
                                <div class="flex">
                                    <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-400 dark:bg-gray-200">
                                        <span class="text-lg font-medium leading-none text-white dark:text-gray-800">AO</span>
                                    </span>
                                    <ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-gray-600" /> 
                                </div>
                            </div>
                            <div class="col-span-9">
                                <div class="overflow-hidden rounded-md bg-gray-100 dark:bg-gray-500" @click="toggleHiddenParagraph(3)">
                                    <ul role="list" class="divide-y divide-gray-200">
                                        <li class="px-6 py-4 hover:bg-gray-100 dark:hover:bg-gray-500 dark:hover:bg-opacity-100">
                                            <p class="text-gray-500 dark:text-gray-50">
                                                Vous avez reçu <span class="font-semibold text-gray-600 dark:text-white hover:text-gray-700">4</span> mails inutiles
                                            </p>
                                            <ul role="list" v-show="showHiddenParagraphs[3]" class="text-black pt-2" ref="parentElement3">
                                                <li class="pl-8" ref="hiddenText3" data-text="- Fabien Huet est en vacances dans les Alpes."></li>
                                                <li class="pl-8" ref="hiddenText3" data-text="- Il demande à recevoir les différentes informations pour le BP afin d'avancer rapidement sur le sujet."></li>
                                                <li class="pl-8" ref="hiddenText3" data-text="- Il souhaite également prendre rendez-vous avec son expert-comptable d'ici la fin du mois."></li>
                                            </ul>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import Navbar from './components/Navbar.vue';
import {
  ChatBubbleOvalLeftEllipsisIcon,
} from '@heroicons/vue/24/outline'

export default {
  components: {
    Navbar,
    ChatBubbleOvalLeftEllipsisIcon,
  },
  methods: {
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
  },
  data() {
    return {
      showHiddenParagraphs: [false, false, false],
      animationTriggered: [false, false, false]
    }
  }
}
</script>
