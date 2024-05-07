<template>
  <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
    :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" />
  <div class="relative">
    <Combobox as="div" v-model="selectedPerson">
      <ComboboxInput
        class="w-full rounded-md border-0 bg-white py-1.5 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
        @input="query = $event.target.value" :display-value="(person) => person?.username" />
      <ComboboxButton class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
      </ComboboxButton>

      <ComboboxOptions v-if="filteredPeople.length > 0"
        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
        <ComboboxOption v-for="person in filteredPeople" :value="person" :key="person" as="template" v-slot="{ active, selected }">
          <li @click="toggleSelection(person)"
            :class="['relative cursor-default select-none py-2 pl-3 pr-9', active ? 'bg-gray-500 text-white' : 'text-gray-900']">
            <div class="flex">
              <span :class="['truncate', selected && 'font-semibold']">
                {{ person.username }}
              </span>
              <span :class="['ml-2 truncate text-gray-500', active ? 'text-indigo-200' : 'text-gray-500']">
                &lt;{{ person.email }}&gt;
              </span>
            </div>
            <span v-if="selected"
              :class="['absolute inset-y-0 right-0 flex items-center pr-4', active ? 'text-white' : 'text-gray-500']">
              <CheckIcon class="h-5 w-5" aria-hidden="true" />
            </span>
          </li>
        </ComboboxOption>
      </ComboboxOptions>
    </Combobox>

    <div v-if="selectedRecipients.length > 0" class="mt-2 flex flex-wrap">
      <span v-for="recipient in selectedRecipients" :key="recipient.email"
        class="bg-gray-200 px-2 py-1.5 rounded-full text-sm font-semibold mr-2 mb-2">
        {{ recipient.username }}
        <button @click="removeRecipient(recipient)"
          class="ml-1 text-red-600 focus:outline-none hover:text-red-800">&times;</button>
      </span>
    </div>
  </div>
</template>

<script setup>
import ShowNotification from '../components/ShowNotification.vue';
import { computed, ref,provide } from 'vue'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'
import { fetchWithToken } from '../router/index.js';
import { API_BASE_URL } from '@/main';
import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
} from '@headlessui/vue'


let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
let timerId = ref(null);


const contacts = [];
const query = ref('')
const selectedPerson = ref(null)
const selectedRecipients = ref([])

const filteredPeople = computed(() =>
  query.value === ''
    ? contacts
    : contacts.filter((person) => {
      return person.username.toLowerCase().includes(query.value.toLowerCase())
    })
)

const toggleSelection = (person) => {
  const index = selectedRecipients.value.findIndex((recipient) => recipient.email === person.email)
  if (index === -1) {
    selectedRecipients.value.push(person)
  } else {
    selectedRecipients.value.splice(index, 1)
  }
}

const removeRecipient = (recipient) => {
  const index = selectedRecipients.value.findIndex((r) => r.email === recipient.email)
  if (index !== -1) {
    selectedRecipients.value.splice(index, 1)
  }
}

const requestOptions = {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
  },
}
fetchWithToken(`${API_BASE_URL}user/contacts/`, requestOptions)
  .then(response => {
    contacts.push(...response);
  })
  .catch(error => {
    backgroundColor = 'bg-red-300';
    notificationTitle.value = 'Erreur récupération des contacts';
    notificationMessage.value = error;
    displayPopup();
  });

</script>
