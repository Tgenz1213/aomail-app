<template>
  <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
    :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" @dismiss-popup="dismissPopup" />

  <Listbox as="div" v-model="selectedLanguage">
    <ListboxButton
      class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6">
      <span class="block truncate">{{ $t(selectedLanguage.i18nKey) }}</span>
      <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
      </span>
    </ListboxButton>

    <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
      leave-to-class="opacity-0">
      <ListboxOptions
        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
        <ListboxOption as="template" v-for="language in languages" :key="language.key" :value="language">
          <li :class="getOptionClasses(active, selected)">
            <span :class="getLabelClasses(selected)">{{ $t(language.i18nKey) }}</span>
            <span v-if="selected" :class="getCheckIconClasses(active)">
              <CheckIcon class="h-5 w-5" aria-hidden="true" />
            </span>
          </li>
        </ListboxOption>
      </ListboxOptions>
    </transition>
  </Listbox>
</template>

<script setup>
import { ref, watch } from 'vue';
import ShowNotification from '../components/ShowNotification.vue';
import { fetchWithToken } from '../router/index.js';
import { API_BASE_URL } from '@/main';
import i18n from '@/main';
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, ChevronUpDownIcon, CheckIcon } from '@headlessui/vue';

// Language options
const languages = ref([
  { key: 'french', i18nKey: 'languages.french' },
  { key: 'american', i18nKey: 'languages.american' },
  { key: 'german', i18nKey: 'languages.german' },
  { key: 'russian', i18nKey: 'languages.russian' },
  { key: 'spanish', i18nKey: 'languages.spanish' },
  { key: 'chinese', i18nKey: 'languages.chinese' },
  { key: 'indian', i18nKey: 'languages.indian' },
]);

// Selected language
const storedLanguageKey = localStorage.getItem("language");
const languageIndex = languages.value.findIndex(lang => lang.key === storedLanguageKey);
const selectedLanguage = ref(languages.value[languageIndex] || languages.value[1]);

// Notification state
const showNotification = ref(false);
const notificationTitle = ref('');
const notificationMessage = ref('');
const backgroundColor = ref('');
let timerId = ref(null);

// Functions
const dismissPopup = () => {
  showNotification.value = false;
  clearTimeout(timerId.value);
};

const displayPopup = () => {
  showNotification.value = true;
  timerId.value = setTimeout(dismissPopup, 4000);
};

const updateLanguageSelection = async (newLanguage) => {
  selectedLanguage.value = newLanguage;
  const newLanguageKey = newLanguage.key;
  const currentLanguage = localStorage.getItem('language');

  if (newLanguageKey === currentLanguage) return;

  localStorage.setItem('language', newLanguageKey);

  try {
    const response = await fetchWithToken(`${API_BASE_URL}user/set_language/`, {
      headers: { 'Content-Type': 'application/json' },
      method: "POST",
      body: JSON.stringify({ language: newLanguageKey }),
    });

    if (response.error) {
      setNotification('bg-red-300', 'Error getting language', response.error);
    } else if (response.message === "Language updated successfully") {
      i18n.global.locale = newLanguageKey;
      setNotification('bg-green-300', 'Success!', 'Language updated successfully');
    }
  } catch (error) {
    setNotification('bg-red-300', 'Error getting language', error.message);
  }
};

const setNotification = (color, title, message) => {
  backgroundColor.value = color;
  notificationTitle.value = title;
  notificationMessage.value = message;
  displayPopup();
};

// Watchers
watch(selectedLanguage, updateLanguageSelection);

// Utility functions for class bindings
const getOptionClasses = (active, selected) => ({
  'bg-gray-800 text-white': active,
  'text-gray-900': !active,
  'relative cursor-default select-none py-2 pl-3 pr-9': true,
});

const getLabelClasses = (selected) => ({
  'font-semibold': selected,
  'font-normal': !selected,
  'block truncate': true,
});

const getCheckIconClasses = (active) => ({
  'text-white': active,
  'text-gray-500': !active,
  'absolute inset-y-0 right-0 flex items-center pr-4': true,
});
</script>
