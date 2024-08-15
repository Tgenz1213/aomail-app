<template>
  <transition name="modal-fade">
    <Modal v-if="props.isOpen" @click.self="closeModal" class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white rounded-lg relative w-[450px]">
          <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
            <button @click="closeModal" type="button"
                class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                <XMarkIcon class="h-6 w-6" aria-hidden="true" />
            </button>
          </div>
          <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
            <div class="ml-8 flex items-center space-x-1">
              <p class="block leading-6 text-gray-900 font-medium">
                {{ $t('constants.categoryModalConstants.modifyTheCategory') }}
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
                class="ml-auto rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                @click="updateCategory">
                {{ $t('constants.userActions.update') }}
              </button>
              <button type="button"
                class="inline-flex w-full justify-cente items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto"
                @click="deleteCategory">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09
  1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
              </svg>
              {{ $t('constants.userActions.delete') }}
            </button>
          </div>
        </div>
      </div>
    </Modal>
  </transition>
</template>

<script setup lang="ts">
import { Ref, ref, watch, inject } from 'vue';
import { i18n } from "@/global/preferences";
import { Category } from '@/global/types';
import { XMarkIcon } from '@heroicons/vue/20/solid';
import { postData, deleteData, putData } from '@/global/fetchData';

const props = defineProps<{
  isOpen: boolean;
  category: Category | null;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
}>();

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const fetchEmailsData = inject('fetchEmailsData') as (categoryName: string) => Promise<void>;
const fetchCategoriesAndTotals = inject('fetchCategoriesAndTotals') as () => Promise<void>;
const categories = inject('categories') as Ref<Category[]>;
const selectedCategory = inject('selectedCategory') as Ref<string>;

const categoryName = ref('');
const categoryDescription = ref('');
const errorMessage = ref('');

watch(() => props.category, (newCategory) => {
  if (newCategory) {
    categoryName.value = newCategory.name;
    categoryDescription.value = newCategory.description;
  }
}, { immediate: true });

const closeModal = () => {
  emit('close');
  resetForm();
};

const resetForm = () => {
  categoryName.value = '';
  categoryDescription.value = '';
  errorMessage.value = '';
};

const updateCategory = async () => {
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
  
  const result = await putData(`api/update_category/`, { newCategoryName: categoryName.value, description: categoryDescription.value, categoryName: props.category?.name });
  if (result.success) {
    const oldCategoryName = props.category?.name || '';
    const newCategoryName = categoryName.value;
    const updatedCategories = categories.value.map(category => {
      if (category.name === props.category?.name) {
        return {
          name: categoryName.value,
          description: categoryDescription.value
        };
      }
      return category;
    });
    categories.value = updatedCategories;
    fetchCategoriesAndTotals();
    fetchEmailsData(selectedCategory.value);
    closeModal();
    displayPopup?.("success", i18n.global.t('constants.popUpConstants.successMessages.success'), i18n.global.t('constants.popUpConstants.successMessages.updateCategorySuccess'));
  } else {
    closeModal();
    displayPopup?.("error", i18n.global.t('constants.popUpConstants.addCategoryError'), i18n.global.t('constants.popUpConstants.errorMessages.updateCategoryError'));
  }

  closeModal();
};

const deleteCategory = async () => {
  const result = await postData(`api/get_rules_linked/`, { categoryName: categoryName.value });
  // TO UPDATE with warning
  if (!result.success || result.data.nb_rules > 0) {
    closeModal();
    displayPopup?.("error", i18n.global.t('constants.popUpConstants.errorMessages.error'), i18n.global.t('constants.popUpConstants.errorMessages.deleteCategoryError'));  
  } else {
    await deleteData(`api/delete_category/`, { categoryName: categoryName.value });
    const index = categories.value.findIndex(category => category.name === categoryName.value);
    if (index !== -1) {
      categories.value.splice(index, 1);
    }
    closeModal();
    displayPopup?.("success", i18n.global.t('constants.popUpConstants.successMessages.success'), i18n.global.t('constants.popUpConstants.successMessages.deleteCategorySuccess'));
  }
};
</script>  