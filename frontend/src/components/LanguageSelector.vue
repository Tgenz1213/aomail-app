<template>
    <Listbox as="div" v-model="languageSelected" @click="handleLanguageChange">
      <ListboxButton class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6">
        <span class="block truncate">{{ languageDisplayed }}</span>
        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true"/>
        </span>
      </ListboxButton>
      <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <ListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
          <ListboxOption as="template" v-for="language in languages" :key="language.key" :value="language" v-slot="{ active, selected }">
            <li :class="[active ? 'bg-gray-800 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
              <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">{{ language.value }}</span>
              <span v-if="selected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                <CheckIcon class="h-5 w-5" aria-hidden="true"/>
              </span>
            </li>
          </ListboxOption>
        </ListboxOptions>
      </transition>
    </Listbox>
  </template>
  
  <script>
import { API_BASE_URL } from '@/main';
import { useRouter } from 'vue-router';

async function handleLanguageChange() {
    const newLanguageKey = languageSelected.value.key;
    const currentLanguage = localStorage.getItem('language');

    if (newLanguageKey === currentLanguage) {
        return;
    }
    localStorage.setItem('language', newLanguageKey);
    const storedLanguage = languages.find(lang => lang.key === newLanguageKey);
    languageDisplayed.value = storedLanguage.value;

    const requestOptions = {
        headers: { 'Content-Type': 'application/json' },
        method: "POST",
        body: JSON.stringify({ language: newLanguageKey })
    };

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/set_language/`, requestOptions);

        if ("error" in response) {
            // Show the pop-up
            backgroundColor = 'bg-red-300';
            notificationTitle.value = 'Error get language';
            notificationMessage.value = response.error;
            displayPopup();
        } else if (response.message == "Language updated successfully") {
            // Show the pop-up
            backgroundColor = 'bg-green-300';
            notificationTitle.value = 'Succès!';
            notificationMessage.value = 'Language updated successfully';
            displayPopup();
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-300';
        notificationTitle.value = 'Error get language';
        notificationMessage.value = error.message;
        displayPopup();
    }
}
  </script>