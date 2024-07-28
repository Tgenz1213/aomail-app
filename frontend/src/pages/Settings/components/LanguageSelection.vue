<template>
  <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
    :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" @dismiss-popup="dismissPopup" />

  <div class="relative">
    <Listbox as="div" v-model="selectedLanguage">
      <ListboxButton
        class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6">
        <span class="block truncate">{{ $t(selectedLanguage.value) }}</span>
        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </span>
      </ListboxButton>

      <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
        leave-to-class="opacity-0">
        <ListboxOptions
          class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
          <ListboxOption as="template" v-for="language in languages" :key="language.key" :value="language"
            v-slot="{ active, selected }">
            <li
              :class="[active ? 'bg-gray-800 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
              <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{ $t(language.value)
                }}</span>
              <span v-if="selected"
                :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                <CheckIcon class="h-5 w-5" aria-hidden="true" />
              </span>
            </li>
          </ListboxOption>
        </ListboxOptions>
      </transition>
    </Listbox>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import ShowNotification from '../components/ShowNotification.vue';
import { fetchWithToken } from '../router/index.js';
<<<<<<< HEAD
import { API_BASE_URL } from '@/main';
import i18n from '@/main';
=======
import { API_BASE_URL } from '@/main.jts';
import i18n from '@/main.jts';
>>>>>>> d03fc83b (🔃 refactor: add tsconfig.json + fix packages dependencies)
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, ChevronUpDownIcon, CheckIcon } from '@headlessui/vue';
import { useI18n } from 'vue-i18n';



// Language options
const languages = ref([
  { key: 'french', value: 'constants.languagesList.french' },
  { key: 'american', value: 'constants.languagesList.american' },
  { key: 'german', value: 'constants.languagesList.german' },
  { key: 'russian', value: 'constants.languagesList.russian' },
  { key: 'spanish', value: 'constants.languagesList.spanish' },
  { key: 'chinese', value: 'constants.languagesList.chinese' },
  { key: 'indian', value: 'constants.languagesList.indian' },
]);

// Use i18n
const { t } = useI18n();


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
    const response = await fetchWithToken(`${API_BASE_URL}user/preferences/set_language/`, {
      headers: { 'Content-Type': 'application/json' },
      method: "POST",
      body: JSON.stringify({ language: newLanguageKey }),
    });

    if (response.error) {
      setNotification('bg-red-200/[.89] border border-red-400', t('settingsPage.preferencesPage.popUpConstants.errorMessages.errorGettingLanguage'), response.error);
    } else if (response.message === "Language updated successfully") {
      i18n.global.locale = newLanguageKey;
      setNotification('bg-green-200/[.89] border border-green-400', t('settingsPage.preferencesPage.popUpConstants.successMessages.languageUpdatedSuccessfully'));
    }
  } catch (error) {
    setNotification('bg-red-200/[.89] border border-red-400', t('settingsPage.preferencesPage.popUpConstants.errorMessages.errorGettingLanguage'), error.message);
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
</script>
