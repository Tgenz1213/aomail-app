<template>
  <transition name="modal-fade">
    <Modal v-if="props.isOpen" @click.self="closeModal" class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-lg relative w-[550px] max-h-[90vh] overflow-y-auto">
        <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
          <button @click="closeModal" type="button" class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
        <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
          <div class="ml-8 flex items-center space-x-1">
            <p class="block leading-6 text-gray-900 font-medium">
              {{ $t('homePage.modals.filterModal.addFilter') }}
            </p>
          </div>
        </div>
        <div class="flex flex-col gap-4 px-8 py-6">
          <p class="text-red-500" v-if="errorMessage">{{ errorMessage }}</p>
          
          <!-- Filter Name -->
          <div>
            <label for="filterName" class="block text-sm font-medium leading-6 text-gray-900">
              {{ $t('homePage.modals.filterModal.filterName') }}
            </label>
            <div class="mt-2">
              <input id="filterName" v-model="newFilter.name" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6" :placeholder="$t('homePage.modals.filterModal.filterNamePlaceholder')">
            </div>
          </div>

          <!-- Priority Section -->
          <div>
            <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">{{ $t('homePage.modals.filterModal.priority') }}</h3>
            <div class="flex justify-between items-center">
              <div class="flex items-center space-x-2">
                <input type="checkbox" id="important" v-model="newFilter.important" class="rounded text-gray-600 focus:ring-gray-500">
                <label for="important" class="flex items-center">
                  <span class="bg-orange-100 text-orange-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full">
                    <ExclamationCircleIcon class="h-4 w-4 items-center inline mr-1" />
                    {{ $t('homePage.modals.filterModal.important') }}
                  </span>
                </label>
              </div>
              <div class="flex items-center space-x-2">
                <input type="checkbox" id="informative" v-model="newFilter.informative" class="rounded text-gray-600 focus:ring-gray-500">
                <label for="informative" class="flex items-center">
                  <span class="bg-blue-100 text-blue-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full">
                    <InformationCircleIcon class="h-4 w-4 inline mr-1" />
                    {{ $t('homePage.modals.filterModal.informative') }}
                  </span>
                </label>
              </div>
              <div class="flex items-center space-x-2">
                <input type="checkbox" id="useless" v-model="newFilter.useless" class="rounded text-gray-600 focus:ring-gray-500">
                <label for="useless" class="flex items-center">
                  <span class="bg-gray-100 text-gray-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full">
                    <TrashIcon class="h-4 w-4 inline mr-1" />
                    {{ $t('homePage.modals.filterModal.useless') }}
                  </span>
                </label>
              </div>
            </div>
          </div>

          <!-- Read Status -->
          <div>
            <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">{{ $t('homePage.modals.filterModal.readStatus') }}</h3>
            <div class="flex items-center space-x-2">
              <input type="checkbox" id="read" v-model="newFilter.read" class="rounded text-gray-600 focus:ring-gray-500">
              <label for="read" class="flex items-center  rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="h-4 w-4 mr-1"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M4.5 12.75l6 6 9-13.5"
                    />
                </svg>
                {{ $t('homePage.modals.filterModal.read') }}
              </label>
            </div>
          </div>

          <!-- Flags -->
          <div>
            <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">{{ $t('homePage.modals.filterModal.flags') }}</h3>
            <div class="grid grid-cols-2 gap-2">
              <div class="flex items-center space-x-2">
                <input type="checkbox" id="notification" v-model="newFilter.notification" class="rounded text-gray-600 focus:ring-gray-500">
                <label for="notification" class="flex items-center">
                  <span class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10">
                    {{ $t('homePage.modals.filterModal.notification') }}
                  </span>
                </label>
              </div>
              <div class="flex items-center space-x-2">
                <input type="checkbox" id="newsletter" v-model="newFilter.newsletter" class="rounded text-gray-600 focus:ring-gray-500">
                <label for="newsletter" class="flex items-center">
                  <span class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10">
                    {{ $t('homePage.modals.filterModal.newsletter') }}
                  </span>
                </label>
              </div>
              <div class="flex items-center space-x-2">
                <input type="checkbox" id="meeting" v-model="newFilter.meeting" class="rounded text-gray-600 focus:ring-gray-500">
                <label for="meeting" class="flex items-center">
                  <span class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10">
                    {{ $t('homePage.modals.filterModal.meeting') }}
                  </span>
                </label>
              </div>
              <div class="flex items-center space-x-2">
                <input type="checkbox" id="spam" v-model="newFilter.spam" class="rounded text-gray-600 focus:ring-gray-500">
                <label for="spam" class="flex items-center">
                  <span class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10">
                    {{ $t('homePage.modals.filterModal.spam') }}
                  </span>
                </label>
              </div>
              <div class="flex items-center space-x-2">
                <input type="checkbox" id="scams" v-model="newFilter.scams" class="rounded text-gray-600 focus:ring-gray-500">
                <label for="scams" class="flex items-center">
                  <span class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10">
                    {{ $t('homePage.modals.filterModal.scams') }}
                  </span>
                </label>
              </div>
            </div>
          </div>


          <!-- Relevance and Answer -->
          <div>
            <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">{{ $t('homePage.modals.filterModal.additionalSettings') }}</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="relevance" class="block text-xs font-medium text-gray-700">{{ $t('homePage.modals.filterModal.relevance') }}</label>
                <select id="relevance" v-model="newFilter.relevance" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm">
                  <option value="high">{{ $t('homePage.modals.filterModal.high') }}</option>
                  <option value="medium">{{ $t('homePage.modals.filterModal.medium') }}</option>
                  <option value="low">{{ $t('homePage.modals.filterModal.low') }}</option>
                </select>
              </div>
              <div>
                <label for="answer" class="block text-xs font-medium text-gray-700">{{ $t('homePage.modals.filterModal.answer') }}</label>
                <select id="answer" v-model="newFilter.answer" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm">
                  <option value="might_want_to_answer">{{ $t('homePage.modals.filterModal.mightWantToAnswer') }}</option>
                </select>
              </div>
            </div>
          </div>

          <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
            <button type="button" class="inline-flex w-full rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:w-auto" @click="addFilter">
              {{ $t('constants.userActions.create') }}
            </button>
          </div>
        </div>
      </div>
    </Modal>
  </transition>
</template>
<script setup lang="ts">
import { ref, inject } from 'vue';
import { XMarkIcon, ExclamationCircleIcon, InformationCircleIcon, TrashIcon, EnvelopeOpenIcon } from '@heroicons/vue/20/solid';
import { postData } from '@/global/fetchData';
import { Filter } from '../utils/types';

const props = defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'filterCreated', filter: Filter): void;
}>();

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const filters = ref<Filter[]>;

const newFilter = ref<Filter>({
  name: '',
  important: true,
  informative: true,
  useless: true,
  read: true,
  notification: true,
  newsletter: true,
  spam: true,
  scams: true,
  meeting: true,
  relevance: 'medium',
  answer: 'might_want_to_answer'
});

const errorMessage = ref('');

const closeModal = () => {
  emit('close');
};

const addFilter = async () => {
  /*try {
    const response = await postData('/api/create_filter/', newFilter.value);
    if (response.ok) {
      const createdFilter = await response.json();
      filters.value.push(createdFilter);
      emit('filterCreated', createdFilter);
      displayPopup("success", "Succès", "Le filtre a été créé avec succès.");
      closeModal();
    } else {
      const error = await response.json();
      errorMessage.value = error.message || "Une erreur est survenue lors de la création du filtre.";
    }
  } catch (error) {
    console.error('Error creating filter:', error);
    errorMessage.value = "Une erreur est survenue lors de la création du filtre.";
  }*/
};
</script>
