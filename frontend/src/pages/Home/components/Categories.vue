<template>
  <div class="hidden sm:block w-full py-5">
    <nav class="flex flex-wrap space-x-2 2xl:space-x-4 justify-center items-center w-full" aria-label="Tabs">
      <div class="flex space-x-4 2xl:space-x-6">
        <a v-for="category in categories" :key="category.name" class="group items-center text-gray-600 text-sm font-medium">
          <div v-if="category.name !== 'Others'" class="flex cursor-pointer" @click="selectCategory(category)">
            <span class="px-3 py-2 group-hover:rounded-r-none"
              :class="getCategoryClass(category)">
              {{ category.name }}
            </span>
            <div class="group-hover:bg-gray-500 group-hover:rounded-r-none group-hover:bg-opacity-10 flex items-center"
              :class="{ 'bg-gray-500 bg-opacity-10 rounded-r-md': selectedCategory === category.name }">
              <span v-if="getTotalEmailsInCategory(category.name) > 0"
                class="group-hover:bg-transparent group-hover:text-gray-800 rounded-full py-0.5 px-2.5 text-xs font-medium"
                :class="{ 'text-gray-800': selectedCategory === category.name, 'text-white bg-gray-800': selectedCategory !== category.name }">
                {{ getTotalEmailsInCategory(category.name) }}
              </span>
            </div>
            <span class="opacity-0 group-hover:opacity-100 pr-2 py-2 group-hover:bg-gray-500 rounded-r-md group-hover:bg-opacity-10">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="w-5 h-5 hover:text-black" @click.stop="openUpdateModal(category)">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
              </svg>
            </span>
          </div>
          <div v-else class="flex pr-7">
            <span class="px-3 py-2 cursor-pointer" @click="selectCategory(category)"
              :class="getCategoryClass(category)">
              {{ $t('homePage.otherCategory') }}
            </span>
            <div @click="selectCategory(category)"
              class="group-hover:bg-gray-500 group-hover:rounded-r group-hover:bg-opacity-10 flex items-center cursor-pointer"
              :class="{ 'bg-gray-500 bg-opacity-10 rounded-r-md': selectedCategory === category.name }">
              <span v-if="getTotalEmailsInCategory(category.name) > 0"
                class="group-hover:bg-transparent group-hover:text-gray-800 rounded-full py-0.5 px-2.5 text-xs font-medium"
                :class="{ 'text-gray-800': selectedCategory === category.name, 'text-white bg-gray-800': selectedCategory !== category.name }">
                {{ getTotalEmailsInCategory(category.name) }}
              </span>
            </div>
          </div>
        </a>
      </div>
      <a class="flex text-gray-600 rounded-md px-8 py-2 text-sm font-medium hover:bg-gray-900 hover:text-white"
        @click="openNewCategoryModal">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
      </a>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { Category } from '@/global/types';

const { t } = useI18n();

const props = defineProps<{
  categories: Category[];
  selectedCategory: string;
  getTotalEmailsInCategory: (categoryName: string) => number;
}>();

const emit = defineEmits<{
  (e: 'select-category', category: Category): void;
  (e: 'open-new-category-modal'): void;
  (e: 'open-update-category-modal', category: Category): void;
}>();

const selectCategory = (category: Category) => {
  emit('select-category', category);
};

const openNewCategoryModal = () => {
  emit('open-new-category-modal');
};

const openUpdateModal = (category: Category) => {
  emit('open-update-category-modal', category);
};

const getCategoryClass = (category: Category) => {
  const baseClass = 'group-hover:bg-gray-500 rounded-l-md group-hover:bg-opacity-10';
  return {
    [baseClass]: true,
    'bg-gray-500 bg-opacity-10 text-gray-800': props.selectedCategory === category.name,
    'rounded-md': props.getTotalEmailsInCategory(category.name) === 0,
    'rounded-l-md': props.getTotalEmailsInCategory(category.name) > 0
  };
};
</script>

  