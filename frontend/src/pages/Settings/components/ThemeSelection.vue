<template>
  <ShowNotification :showNotification="showThemeNotification" :notificationTitle="themeNotificationTitle"
    :notificationMessage="themeNotificationMessage" :backgroundColor="themeBackgroundColor"
    @dismiss-popup="dismissThemePopup" />

  <div class="relative">
    <Listbox as="div" v-model="selectedTheme">
      <ListboxButton
        class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6">
        <span class="block truncate">{{ $t(selectedTheme.value) }}</span>
        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </span>
      </ListboxButton>
      <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100"
        leave-to-class="opacity-0">
        <ListboxOptions
          class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
          <ListboxOption as="template" v-for="theme in themes" :key="theme.key" :value="theme"
            v-slot="{ active, selected }">
            <li
              :class="[active ? 'bg-gray-800 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
              <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{ $t(theme.value) }}</span>
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
=======
import { API_BASE_URL } from '@/main.jts';
>>>>>>> d03fc83b (🔃 refactor: add tsconfig.json + fix packages dependencies)
import { Listbox, ListboxButton, ListboxOptions, ListboxOption, ChevronUpDownIcon, CheckIcon } from '@headlessui/vue';
import { useI18n } from 'vue-i18n';

// Use i18n
const { t } = useI18n();

// Theme options
const themes = ref([
  { key: 'light', value: 'constants.themeList.lightTheme' },
  { key: 'dark', value: 'constants.themeList.darkTheme' },
]);

// Selected theme
const storedThemeKey = localStorage.getItem("theme");
const themeIndex = themes.value.findIndex(theme => theme.key === storedThemeKey);
const selectedTheme = ref(themes.value[themeIndex] || themes.value[0]);

// Notification state
const showThemeNotification = ref(false);
const themeNotificationTitle = ref('');
const themeNotificationMessage = ref('');
const themeBackgroundColor = ref('');
let themeTimerId = null;

// Functions
const dismissThemePopup = () => {
  showThemeNotification.value = false;
  clearTimeout(themeTimerId);
};

const displayThemePopup = () => {
  showThemeNotification.value = true;
  themeTimerId = setTimeout(dismissThemePopup, 4000);
};

const updateThemeSelection = async (newTheme) => {
  selectedTheme.value = newTheme;
  const newThemeKey = newTheme.key;
  const currentTheme = localStorage.getItem('theme');

  if (newThemeKey === currentTheme) return;

  localStorage.setItem('theme', newThemeKey);

  try {
    const response = await fetchWithToken(`${API_BASE_URL}user/preferences/set_theme/`, {
      headers: { 'Content-Type': 'application/json' },
      method: "POST",
      body: JSON.stringify({ theme: newThemeKey }),
    });


    // TODO    
    if (response.error) {
      setThemeNotification('bg-red-300', t('settingsPage.preferencesPage.popUpConstants.errorMessages.errorUpdatingTheme'), response.error);
    } else if (response.message === "Theme updated successfully") {
      setThemeNotification('bg-green-300', t('constants.popUpConstants.successMessages.success'), t('settingsPage.preferencesPage.popUpConstants.successMessages.themeUpdatedSuccessfully'));
    }
  } catch (error) {
    setThemeNotification('bg-red-300', t('settingsPage.preferencesPage.popUpConstants.errorMessages.errorUpdatingTheme'), error.message);
  }
};

const setThemeNotification = (color, title, message) => {
  themeBackgroundColor.value = color;
  themeNotificationTitle.value = title;
  themeNotificationMessage.value = message;
  displayThemePopup();
};

// Watchers
watch(selectedTheme, updateThemeSelection);
</script>