<template>
    <navbar></navbar>
    <main class="py-7 lg:pl-20">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-6 gap-6">
                <div class="col-span-2">
                    <!-- Assistant Up -->
                    <div class="flex pb-6">
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
                <div class="col-span-4 pt-8">
                    <div>
                        <div class="sm:hidden">
                            <label for="tabs" class="sr-only">Select a tab</label>
                            <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
                            <select id="tabs" name="tabs" class="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500">
                            <option selected>My Account</option>
                            <option>Company</option>
                            <option>Team Members</option>
                            <option>Billing</option>
                            </select>
                        </div>
                        <div class="hidden sm:block">
                            <nav class="isolate flex divide-x divide-gray-200 rounded-t-lg" aria-label="Tabs">
                                <!-- Current: "text-gray-900", Default: "text-gray-500 hover:text-gray-700" -->
                                <a href="#" class="text-indigo-600 dark:text-indigo-400 rounded-tl-lg group relative min-w-0 flex-1 overflow-hidden bg-white dark:bg-gray-800 py-4 px-4 text-center text-sm font-medium hover:bg-gray-50 focus:z-10" aria-current="page">
                                    <span>ESAIP</span>
                                    <span aria-hidden="true" class="bg-indigo-600 absolute inset-x-0 bottom-0 h-0.5 z-20"></span>
                                </a>
                                <a href="#" class="text-gray-500 dark:text-white hover:text-gray-700 group relative min-w-0 flex-1 overflow-hidden bg-white dark:bg-gray-800 py-4 px-4 text-center text-sm font-medium hover:bg-gray-50 focus:z-10">
                                    <span>Entrepreneurial</span>
                                    <span aria-hidden="true" class="bg-indigo-600/20 absolute inset-x-0 bottom-0 h-[1px]"></span>
                                </a>
                                <a href="#" class="text-gray-500 dark:text-white hover:text-gray-700 group relative min-w-0 flex-1 overflow-hidden bg-white dark:bg-gray-800 py-4 px-4 text-center text-sm font-medium hover:bg-gray-50 focus:z-10">
                                    <span>Autres</span>
                                    <span aria-hidden="true" class="bg-indigo-600/20 absolute inset-x-0 bottom-0 h-[1px]"></span>
                                </a>
                                <a href="#" class="text-gray-500 dark:text-white hover:text-gray-700 rounded-tr-lg group relative min-w-0 flex-1 overflow-hidden bg-white dark:bg-gray-800 py-4 px-4 text-center text-sm font-medium hover:bg-gray-50 focus:z-10">
                                    <span>Nouveau</span>
                                    <span aria-hidden="true" class="bg-indigo-600/20 absolute inset-x-0 bottom-0 h-[1px]"></span>
                                </a>
                                <a href="#" class="text-gray-500 dark:text-white hover:text-gray-700 rounded-tr-lg group relative min-w-0 flex-1 overflow-hidden bg-white dark:bg-gray-800 py-4 px-4 text-center text-sm font-medium hover:bg-gray-50 focus:z-10">
                                    <span>Nouveau</span>
                                    <span aria-hidden="true" class="bg-indigo-600/20 absolute inset-x-0 bottom-0 h-[1px]"></span>
                                </a>
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
            <div class="inline-block min-h-[81vh] w-full px-8 pb-8 rounded-lg rounded-tr-none bg-white dark:bg-gray-800 ring-1 ring-indigo-600/20 dark:border-indigo-600 dark:border-2">
                <!-- Content goes here -->
                <ul role="list" class="divide-y divide-gray-200">
                    <li class="py-10">
                        <!-- Your content -->
                        <div class="grid grid-cols-12 gap-0">
                            <div class="col-span-1">
                                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-red-400 dark:bg-red-200">
                                    <span class="text-lg font-medium leading-none text-white dark:text-gray-800">AO</span>
                                </span>
                            </div>
                            <div class="col-span-9">
                                <div class="overflow-hidden rounded-md bg-red-50 dark:bg-red-500 shadow" @click="toggleHiddenParagraph(0)">
                                    <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                        <li class="px-6 py-4 bg-red-50 dark:bg-red-500 hover:bg-opacity-70 dark:hover:bg-opacity-100">
                                            <p class="text-red-500 dark:text-red-50">
                                                <a href="#" class="underline font-semibold text-red-600 dark:text-white hover:text-red-700">Cristophe Rouvrais</a> qui parle de l'aventure entrepreneuriale de Malcom Morel.
                                            </p>
                                            <ul role="list" v-show="showHiddenParagraphs[0]" class="text-black text-sm/6 pt-2" ref="parentElement0">
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
                                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-blue-700 dark:bg-blue-200">
                                    <span class="text-lg font-medium leading-none text-white dark:text-gray-800">AO</span>
                                </span>
                            </div>
                            <div class="col-span-9">
                                <div class="overflow-hidden rounded-md bg-blue-50 dark:bg-blue-500 shadow">
                                    <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                        <li class="px-6 py-4 hover:bg-blue-50 dark:hover:bg-blue-500 dark:hover:bg-opacity-100" @click="toggleHiddenParagraph(1)">
                                            <p class="text-blue-500 dark:text-blue-50">
                                                <a href="#" class="underline font-semibold text-blue-600 dark:text-white hover:text-blue-700">Fabien Huet</a> qui parle de ses vacances et son projet d'enteprise.
                                            </p>
                                            <ul role="list" v-show="showHiddenParagraphs[1]" class="text-black text-sm/6 pt-2" ref="parentElement1">
                                                <li class="pl-8" ref="hiddenText1" data-text="- Fabien Huet est en vacances dans les Alpes."></li>
                                                <li class="pl-8" ref="hiddenText1" data-text="- Il demande à recevoir les différentes informations pour le BP afin d'avancer rapidement sur le sujet."></li>
                                                <li class="pl-8" ref="hiddenText1" data-text="- Il souhaite également prendre rendez-vous avec son expert-comptable d'ici la fin du mois."></li>
                                            </ul>
                                        </li>
                                        <li class="px-6 py-4 hover:bg-blue-50 dark:hover:bg-blue-500 dark:hover:bg-opacity-100" @click="toggleHiddenParagraph(2)">
                                            <p class="text-blue-500 dark:text-blue-50">
                                                <a href="#" class="underline font-semibold text-blue-600 dark:text-white hover:text-blue-700">Hannah Williams</a> qui vous donne des conseils pour votre rapport d'étonnement.
                                            </p>
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
                                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-600 dark:bg-gray-200">
                                    <span class="text-lg font-medium leading-none text-white dark:text-gray-800">AO</span>
                                </span>
                            </div>
                            <div class="col-span-9">
                                <div class="overflow-hidden rounded-md bg-gray-100 dark:bg-gray-500 shadow" @click="toggleHiddenParagraph(3)">
                                    <ul role="list" class="divide-y divide-gray-200">
                                        <li class="px-6 py-4 hover:bg-gray-100 dark:hover:bg-gray-500 dark:hover:bg-opacity-100">
                                            <p class="text-gray-500 dark:text-gray-50">
                                                Vous avez reçu <span class="underline font-semibold text-gray-600 dark:text-white hover:text-gray-700">4</span> mails inutiles
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
    </main>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  components: {
    Navbar,
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
