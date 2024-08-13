<template>
    <Modal :show="isOpen" @close="closeModal">
      <div class="bg-white rounded-lg relative w-[450px]">
        <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
          <div class="ml-8 flex items-center space-x-1">
            <p class="block leading-6 text-gray-900 font-medium">
              {{ $t('constants.categoryModalConstants.addCategory') }}
            </p>
          </div>
        </div>
        <div class="flex flex-col gap-4 px-8 py-6">
          <p class="text-red-500" v-if="errorMessage">{{ errorMessage }}</p>
          <div>
            <label for="categoryName" class="block text-sm font-medium leading-6 text-gray-900">
              {{ $t('constants.categoryModalConstants.categoryName') }}
            </label>
            <div class="mt-2">
              <input id="categoryName" v-model="categoryName"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"
                :placeholder="$t('constants.categoryModalConstants.administrative')">
            </div>
          </div>
          <div>
            <label for="categoryDescription" class="block text-sm font-medium leading-6 text-gray-900">
              {{ $t('constants.categoryModalConstants.categoryDescription') }}
            </label>
            <div class="mt-2">
              <textarea id="categoryDescription" v-model="categoryDescription" rows="3" style="min-height: 60px"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6">
              </textarea>
            </div>
            <p class="mt-3 text-sm leading-6 text-gray-600">
              {{ $t('constants.categoryModalConstants.categoryDescriptionExplanation') }}
            </p>
          </div>
          <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
            <button type="button"
              class="inline-flex w-full rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:w-auto"
              @click="addCategory">
              {{ $t('constants.userActions.create') }}
            </button>
          </div>
        </div>
      </div>
    </Modal>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  import { i18n } from "@/global/preferences";
  import { Category } from '@/global/types';
    
  const props = defineProps<{
    isOpen: boolean;
  }>();
  
  const emit = defineEmits<{
    (e: 'close'): void;
    (e: 'add-category', category: Category): void;
  }>();
  
  const categoryName = ref('');
  const categoryDescription = ref('');
  const errorMessage = ref('');
  
  const closeModal = () => {
    emit('close');
    resetForm();
  };
  
  const resetForm = () => {
    categoryName.value = '';
    categoryDescription.value = '';
    errorMessage.value = '';
  };
  
  const addCategory = () => {
    if (!categoryName.value.trim() || !categoryDescription.value.trim()) {
      errorMessage.value = i18n.global.t('homePage.modals.pleaseFillAllFields');
      return;
    }
  
    if (categoryName.value.length > 50) {
      errorMessage.value = i18n.global.t('homePage.modals.newCategoryModal.maxNameCharacters');
      return;
    }
  
    if (categoryDescription.value.length > 300) {
      errorMessage.value = i18n.global.t('homePage.modals.newCategoryModal.maxDescriptionCharacters');
      return;
    }
  
    emit('add-category', {
      name: categoryName.value,
      description: categoryDescription.value
    });
  
    closeModal();
  };
  </script>
  