<template>
  <transition name="modal-fade">
    <div class="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center" v-if="isOpen">
      <div class="bg-white rounded-lg relative">
        <slot></slot>
        <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
          <button @click="closeModal" type="button"
            class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
            <span class="sr-only">Close</span>
            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
        <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
          <div class="ml-8 flex items-center space-x-1">
            <UserGroupIcon class="w-6 h-6" />
            <p class="block font-semibold leading-6 text-gray-900">{{ email.name }}</p>
          </div>
        </div>
        <div class="flex flex-col px-8">
          <div class="mt-4 mb-8">
            <div class="sm:hidden">
              <label for="tabs" class="sr-only">Select a tab</label>
              <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
              <select id="tabs" name="tabs"
                class="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500">
                <option selected>Résumé du mail</option>
                <option>Mail complet</option>
              </select>
            </div>
            <div class="hidden sm:block">
              <div class="border-b border-gray-200">
                <nav class="-mb-px flex" aria-label="Tabs">
                  <!-- Current: "border-indigo-500 text-indigo-600", Default: "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700" -->
                  <a href="#"
                    class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 w-1/2 border-b-2 py-4 px-1 text-center text-sm font-medium">Résumé
                    du Mail</a>
                  <a href="#"
                    class="border-red-400 text-red-500 w-1/2 border-b-2 py-4 px-1 text-center text-sm font-medium">Mail
                    Complet</a>
                </nav>
              </div>
            </div>
          </div>
          <ul role="list" class="text-sm 2xl:max-w-3xl max-w-2xl">
            <li v-for="detail in email.details" :key="detail.id" class="pl-8 my-4 border-l-2 hover:border-l-4">
              {{ detail.text }}
            </li>
          </ul>
          <!--
                <p class="text-sm 2xl:max-w-3xl max-w-2xl">
                    Hi Theo and Antoine <br><br>
                    How are you both ? I’m back to Esaip this morning. <br><br>
                    For your report, my main piece of advice is to step away from a ‘traditional’ ‘rapport d’étonnement’ in the French way.! <br><br>
                    I would like to read about the context of your internships, how you found the partner/company/etc, where they are located (a map will be helpful) with some brief facts about the place (population, local economy, language spoken – important for Belgium) and why you chose the opportunity. <br><br>
                    Then, some info about your tasks and projects, but don’t give me in-depth detail, it’s not a day-to-day activity report. What you enjoyed, didn’t enjoy so much, what was challenging. <br><br>
                    Then the interesting part, the human and cultural aspects (especially for Belgium where there is such a strong cultural identity separating French-speaking Wallonia and Dutch-speaking Flanders). Talk about the people you interacted with and what this has brought you personally. <br><br>
                    Then a sum-up and brief feedback on the experience. <br><br>
                    Photos and illustrations will make it even more pleasant, and if relevant, of course, sources & references. <br><br>
                    Good luck! <br><br>
                    H <br><br>
                </p>-->
          <span class="isolate inline-flex rounded-2xl justify-center mb-8">
            <div class="group">
              <button type="button"
                class="relative -ml-px inline-flex items-center rounded-l-2xl px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                <check-icon class="w-5 h-5 text-red-500 group-hover:text-white" />
              </button>
            </div>
            <div class="group">
              <button type="button"
                class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                <arrow-uturn-left-icon class="w-5 h-5 text-red-500 group-hover:text-white" />
              </button>
            </div>
            <div class="group">
              <button type="button"
                class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                <ellipsis-horizontal-icon class="w-5 h-5 text-red-500 group-hover:text-white" />
              </button>
            </div>
          </span>
        </div>
      </div>
    </div>
  </transition>
</template>
  
<script setup>
//import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
//import { ExclamationTriangleIcon, XMarkIcon } from '@heroicons/vue/24/outline'
</script>
<script>
import {
  //ChatBubbleOvalLeftEllipsisIcon,
  //ExclamationTriangleIcon,
  //InformationCircleIcon,
  //TrashIcon,
  ArrowUturnLeftIcon,
  CheckIcon,
  EllipsisHorizontalIcon,
  //HandRaisedIcon,
  //EyeIcon,
  UserGroupIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

export default {
  components: {
    //ChatBubbleOvalLeftEllipsisIcon,
    //ExclamationTriangleIcon,
    //InformationCircleIcon,
    //TrashIcon,
    ArrowUturnLeftIcon,
    CheckIcon,
    EllipsisHorizontalIcon,
    //HandRaisedIcon,
    //EyeIcon,
    UserGroupIcon
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true
    },
    email: Object
  },
  methods: {
    closeModal() {
      this.$emit('update:isOpen', false);
    }
  }
}
</script>