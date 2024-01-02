<template>
    <transition name="modal-fade">
      <div class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center" v-if="isOpen">
        <div class="bg-white rounded-lg relative w-[450px]">
          <slot></slot>
            <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
                <button @click="closeModal" type="button" class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                    <span class="sr-only">Close</span>
                    <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                </button>
            </div>
            <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
                <div class="ml-8 flex items-center space-x-1">
                    <p class="block font-semibold leading-6 text-gray-900">Nouvelle règle</p>
                </div>
            </div>
            <div class="flex flex-col gap-4 px-8 py-6">
                <Combobox as="div" v-model="selectedPerson">
                  <div class="flex space-x-1 items-center">
                    <UserIcon class="w-4 h-4" />
                    <ComboboxLabel class="block text-sm font-medium leading-6 text-gray-900">Contact</ComboboxLabel>
                  </div>
                  <div class="relative mt-2">
                    <ComboboxInput class="w-full rounded-md border-0 bg-white py-1.5 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" @change="query = $event.target.value" :display-value="(person) => person?.name" />
                    <ComboboxButton class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
                      <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                    </ComboboxButton>

                    <ComboboxOptions v-if="filteredPeople.length > 0" class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                      <ComboboxOption v-for="person in filteredPeople" :key="person.username" :value="person" as="template" v-slot="{ active, selected }">
                        <li :class="['relative cursor-default select-none py-2 pl-3 pr-9', active ? 'bg-gray-500 text-white' : 'text-gray-900']">
                          <div class="flex">
                            <span :class="['truncate', selected && 'font-semibold']">
                              {{ person.name }}
                            </span>
                            <span :class="['ml-2 truncate text-gray-500', active ? 'text-gray-200' : 'text-gray-500']">
                              {{ person.username }}
                            </span>
                          </div>
                          <span v-if="selected" :class="['absolute inset-y-0 right-0 flex items-center pr-4', active ? 'text-white' : 'text-gray-500']">
                            <CheckIcon class="h-5 w-5" aria-hidden="true" />
                          </span>
                        </li>
                      </ComboboxOption>
                    </ComboboxOptions>
                  </div>
                </Combobox>
                <div>
                  <div class="flex space-x-1 items-center">
                    <ArchiveBoxIcon class="w-4 h-4" />
                    <label for="category" class="block text-sm font-medium leading-6 text-gray-900">Catégorie</label>
                  </div>
                  <select id="category" name="category" v-model="formData.category" class="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-gray-500 sm:text-sm sm:leading-6">
                    <option value="">Aucune catégorie définie</option>
                    <option v-for="category in categories" :key="category.name" :value="category.name">{{ category.name }}</option>
                  </select>
                </div>
              <div>
                <div class="flex space-x-1 items-center">
                  <ExclamationCircleIcon class="w-4 h-4" />
                  <label for="priority" class="block text-sm font-medium leading-6 text-gray-900">Priorité</label>
                </div>
                <select id="priority" name="priority" v-model="formData.priority" class="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-gray-500 sm:text-sm sm:leading-6">
                  <option value="">Aucune priorité définie</option>
                  <option value="Important">Important</option>
                  <option value="Informatif">Informatif</option>
                  <option value="Inutile">Inutile</option>
                </select>
              </div>
              <SwitchGroup as="div" class="flex items-center pt-2">
                <Switch v-model="formData.block" :class="[formData.block ? 'bg-gray-500' : 'bg-gray-200', 'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2']">
                  <span aria-hidden="true" :class="[formData.block ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out']" />
                </Switch>
                <SwitchLabel as="span" class="ml-3 text-sm">
                  <span class="font-medium text-gray-900">Bloquer les mails</span>
                  {{ ' ' }}
                  <!--<span class="text-gray-500"></span>-->
                </SwitchLabel>
                <ShieldCheckIcon class="ml-1 w-4 h-4" />
              </SwitchGroup>
              <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
                <button type="button" class="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto" @click="createUserRule">Créer</button>
                <!--<button type="button" class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto" @click="open = false" ref="cancelButtonRef">Annuler</button>-->
              </div>
           </div>
        </div>
      </div>
    </transition>
  </template>
  
<script setup>
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'
import { Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'
import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxLabel,
  ComboboxOption,
  ComboboxOptions,
} from '@headlessui/vue'

/*const people = [
  { name: 'Leslie Alexander', username: '@lesliealexander' },
  // More users...
]*/

/*
const query = ref('');
const selectedPerson = ref(null);

const filteredPeople = computed(() => {
  // Transform emailSenders into an array of {name, username} objects
  const sendersArray = Object.entries(this.emailSenders).map(([email, name]) => {
    return {
      name: name || email,  // Use the name if available, otherwise use the email as the name
      username: email  // The email address
    };
  });

  // Filter the array based on the search query
  return query.value === '' ? sendersArray : sendersArray.filter(person =>
    person.name.toLowerCase().includes(query.value.toLowerCase()) ||
    person.username.toLowerCase().includes(query.value.toLowerCase())
  );
});*/

//const selectedPerson = ref(null);

//const enabled = ref(false)
</script>

<script>
import {
  XMarkIcon,
  UserIcon,
  ArchiveBoxIcon,
  ShieldCheckIcon,
  ExclamationCircleIcon
} from '@heroicons/vue/24/outline'

export default {
    components: {
        XMarkIcon,
        UserIcon,
        ArchiveBoxIcon,
        ShieldCheckIcon,
        ExclamationCircleIcon
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true
    },
    emailSenders: {
      type: Object,
      default: () => ({}),  // Providing a default empty object
    },
    categories: Array
  },
  data() {
    return {
      query: '',
      selectedPerson: null, 
      formData: {
        info_AI: '',
        priority: '',
        block: false,
        category: '',
      }, 
    };
  },
  computed: {
    filteredPeople() {
      const sendersArray = Object.entries(this.emailSenders).map(([email, name]) => {
        return {
          name: name || email,  // Use name if available, otherwise email
          username: email
        };
      });

      if (this.query === '') {
        return sendersArray;
      } else {
        return sendersArray.filter(person =>
          person.name.toLowerCase().includes(this.query.toLowerCase()) ||
          person.username.toLowerCase().includes(this.query.toLowerCase())
        );
      }
    },
  },
  mounted() {
    console.log("FilteredPeople", this.filteredPeople);
  },
  methods: {
    async postSender() {
      if (!this.selectedPerson) {
        throw new Error('No sender selected');
      }

      const senderData = {
        name: this.selectedPerson.name,
        email: this.selectedPerson.username,  // Assuming username is the email
      };

      try {
        const url = 'http://localhost:9000/MailAssistant/api/create_sender';

        // Use fetchWithToken for the POST request
        const responseData = await this.fetchWithToken(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(senderData),
        });

        return responseData.id;
      } catch (error) {
        console.error(`Error in postSender: ${error}`);
        throw error; // Rethrowing the error can be useful if this function is used in a context where the error needs to be handled further up the chain.
      }
    },
    async fetchWithToken(url, options = {}) {
      const accessToken = localStorage.getItem('userToken');
      if (!options.headers) {
          options.headers = {};
      }
      if (accessToken) {
          options.headers['Authorization'] = `Bearer ${accessToken}`;
      }

      try {
        let response = await fetch(url, options);

        if (response.status === 401) {
          const refreshResponse = await fetch('http://localhost:9000/MailAssistant/api/token/refresh/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ access_token: accessToken })
          });

          if (refreshResponse.ok) {
              const refreshData = await refreshResponse.json();
              const newAccessToken = refreshData.access_token;
              localStorage.setItem('userToken', newAccessToken);
              options.headers['Authorization'] = `Bearer ${newAccessToken}`;
              response = await fetch(url, options);
          } else {
              throw new Error('Unauthorized: Please log in again');
          }
        }

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return response.json();
      } catch (error) {
          console.error('Error in fetchWithToken:', error.message);
          throw error;
      }
    },
    async createUserRule() {
      try {
        console.log("CATEGORY", this.formData.category);

        // Fetch the category ID using fetchWithToken
        const categoryUrl = `http://localhost:9000/MailAssistant/api/get-category-id/${this.formData.category}`;
        const categoryData = await this.fetchWithToken(categoryUrl, {
          method: 'GET'
        });
        const categoryId = categoryData.id;
        console.log("CategoryId", categoryId);

        // First, POST the sender and get the ID
        const senderId = await this.postSender();
        console.log("SenderId", senderId);

        // Now, POST the rule with the sender's ID and category ID
        const ruleData = {
          ...this.formData,
          sender: senderId,  // Replace sender object with sender ID
          category: categoryId, // Use the fetched category ID
          info_AI: ''
        };

        console.log("RuleData", ruleData);

        // Use fetchWithToken for the POST request to create the rule
        const ruleResponseData = await this.fetchWithToken('http://localhost:9000/MailAssistant/user/create-rule/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(ruleData),
        });

        console.log('Rule created:', ruleResponseData);
        window.location.reload(); // To reload

      } catch (error) {
        console.error('Error in creating rule:', error);
        // Handle errors appropriately
      }
    },
    closeModal() {
      this.$emit('update:isOpen', false);
    }
  }
}
</script>