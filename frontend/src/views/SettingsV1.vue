<template>
  <!--
  <div class="pb-1 lg:pl-20 bg-gray-100">
      <div class="grid grid-cols-8 gap-6 h-72 items-center divide-x-8 divide-indigo-900 bg-blue-400">
          <div class="col-span-3 h-full bg-red-500">
                  
                  <div class="flex">
                      <div class="flex-shrink-0 self-center">
                          <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-indigo-800">
                              <span class="text-lg font-medium leading-none text-white">AO</span>
                          </span>
                      </div>
                      <div>
                          <p class="mt-1" id="animated-text" ref="animatedText"></p>
                      </div>
                  </div>
              </div>
          <div class="col-span-5 h-full bg-red-500">
              <p>Test</p>
          </div>
      </div>
  </div>-->
  <div class="flex flex-col justify-center items-center h-screen" :class="bgColor">
      <div class="grid grid-cols-11 2xl:grid-cols-7 gap-8 2xl:gap-6">
          <div class="col-span-1 2xl:col-span-1">
            <div class="2xl:hidden h-full">
              <navbar></navbar>
            </div>
            <div class="hidden 2xl:block h-full">
              <navbar2></navbar2>
            </div>
          </div>
          <div class="col-span-10 2xl:col-span-6">
              <div class="flex flex-col xl:h-[93vh] xl:w-[86vw] 2xl:h-[825px] 2xl:w-[1450px]">
                  <main class="rounded-xl bg-gray-100 bg-opacity-75 ring-1 shadow-sm ring-black ring-opacity-5">
                      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                      <div class="flex items-center pb-5">
                          <div class="w-full flex items-center justify-center pt-5">
                              <div class="sm:hidden">
                                  <label for="tabs" class="sr-only">Select a tab</label>
                                  <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
                                  <select id="tabs" name="tabs" class="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500">
                                  <option>Ecole ESAIP</option>
                                  <option>Entrepreneuriat</option>
                                  <option selected>Administratif</option>
                                  <option>Autres</option>
                                  </select>
                              </div>
                              <div class="hidden sm:block w-full">
                                  <nav class="flex justify-center space-x-4 w-full" aria-label="Tabs">
                                      <!-- Current: "bg-gray-200 text-gray-800", Default: "text-gray-600 hover:text-gray-800" -->
                                      <div 
                                        :class="['flex space-x-2 items-center rounded-md py-2', 
                                                {'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'preferences', 
                                                  'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'preferences'}]"
                                        @click="setActiveSection('preferences')">
                                        <adjustments-vertical-icon class="w-4 h-4" />
                                        <a :class="{'text-gray-800': activeSection === 'preferences', 'text-gray-600': activeSection !== 'preferences'}" class="text-sm font-medium">Préférences</a>
                                      </div>

                                      <div 
                                        :class="['flex space-x-2 items-center rounded-md py-2', 
                                                {'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'account', 
                                                  'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'account'}]"
                                        @click="setActiveSection('account')">
                                        <user-icon class="w-4 h-4" />
                                        <a :class="{'text-gray-800': activeSection === 'account', 'text-gray-600': activeSection !== 'account'}" class="text-sm font-medium">Mon Compte</a>
                                      </div>
                                      <div 
                                        :class="['flex space-x-2 items-center rounded-md py-2', 
                                                {'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'subscription', 
                                                  'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'subscription'}]"
                                        @click="setActiveSection('subscription')">
                                        <adjustments-vertical-icon class="w-4 h-4" />
                                        <a :class="{'text-gray-800': activeSection === 'subscription', 'text-gray-600': activeSection !== 'subscription'}" class="text-sm font-medium">Abonnement</a>
                                      </div>

                                      <div 
                                        :class="['flex space-x-2 items-center rounded-md py-2', 
                                                {'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'data', 
                                                  'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'data'}]"
                                        @click="setActiveSection('data')">
                                        <user-icon class="w-4 h-4" />
                                        <a :class="{'text-gray-800': activeSection === 'data', 'text-gray-600': activeSection !== 'data'}" class="text-sm font-medium">Mes données</a>
                                      </div>
                                  </nav>
                              </div>
                          </div>
                      </div>
                      </div>
                  </main>
                  <div v-if="activeSection === 'account'" class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm hover:shadow-lg ring-black ring-opacity-5 section">
                      <div class="flex px-6 py-6 shadow-sm border-b border-gray-200 bg-gray-50 rounded-t-2xl">
                        <h1 class="text-2xl" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Mon compte</h1>         
                      </div>
                      <div class="float-right mt-[-70px] mr-[10px]">
                        <user-icon class="w-6 h-6 text-gray-500" />
                      </div>
                      <!-- TO DO : CENTER -->
                      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-10">
                          <!-- We've used 3xl here, but feel free to try other max-widths based on your needs -->
                          <div class="mx-auto max-w-lg">
                            <!-- Content goes here -->
                            <div class="flex flex-col">
                              <div class="relative">
                                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                  <div class="w-full border-t border-gray-300"></div>
                                </div>
                                <div class="relative flex justify-center">
                                  <span class="bg-white px-2 text-sm text-gray-500">Changement d'Email ou Mot de Passe</span>
                                </div>
                              </div>
                              <div class="pt-6 pb-10">
                                <div class="flex space-x-1 items-center">
                                  <envelope-icon class="w-4 h-4" />
                                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Login</label>
                                </div>
                                <div class="relative items-stretch mt-2">
                                  <input v-model="userData.username" type="text" name="username" id="username" autocomplete="username" class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6">                                </div>
                                <div class="pt-4">
                                  <div class="grid grid-cols-2 gap-4">
                                    <div>
                                      <div class="flex space-x-1 items-center">
                                        <key-icon class="w-4 h-4" />
                                        <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Nouveau mot de passe</label>
                                      </div>
                                      <div class="relative items-stretch mt-2">
                                        <input v-model="newPassword" type="text" name="first-name" id="first-name" autocomplete="given-name" class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6">
                                      </div>
                                    </div>
                                    <div>
                                      <div class="flex space-x-1 items-center">
                                        <key-icon class="w-4 h-4" />
                                        <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Confirmer le mot de passe</label>
                                      </div>
                                      <div class="relative items-stretch mt-2">
                                        <input v-model="confirmPassword" type="text" name="first-name" id="first-name" autocomplete="given-name" class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6">
                                      </div>
                                    </div>
                                  </div>
                                </div>
                                <div class="flex justify-end pt-4">
                                  <button @click="handleSubmit" class="rounded-md bg-gray-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Modifier</button> <!-- TO CODE : Notification system that worn the user when the notification appears -->
                                </div>
                              </div>
                              <div class="relative">
                                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                  <div class="w-full border-t border-gray-300"></div>
                                </div>
                                <div class="relative flex justify-center">
                                  <span class="bg-white px-2 text-sm text-gray-500">Suppression du compte</span>
                                </div>
                              </div>
                              <div class="pt-6">
                                <div class="flex space-x-1 items-center">
                                  <input type="radio" class="form-radio text-red-600 border-red-400 focus:border-red-500 focus:ring-red-200 h-5 w-5" name="choice">
                                  <label for="push-everything" class="block text-sm font-medium leading-6">Je confirme la supression de mon compte (action irréversible)</label>
                                </div>
                                <div class="flex justify-end pt-4">
                                  <button type="submit" class="rounded-md bg-red-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500">Supprimer</button>
                                </div>
                              </div>
                            </div>
                          </div>
                      </div>    
                  </div>
                  <div v-if="activeSection === 'preferences'" class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm hover:shadow-lg ring-black ring-opacity-5 section"> 
                      <div class="flex px-6 py-6 shadow-sm border-b border-gray-200 bg-gray-50 rounded-t-2xl">
                        <h1 class="text-2xl" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Mes préférences</h1>         
                      </div>
                      <div class="float-right mt-[-70px] mr-[10px]">
                        <adjustments-vertical-icon class="w-6 h-6 text-gray-500" />
                      </div>
                      <!-- TO DO : CENTER -->
                      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-10">
                          <!-- We've used 3xl here, but feel free to try other max-widths based on your needs -->
                          <div class="mx-auto max-w-lg">
                            <!-- Content goes here -->
                            <div class="flex flex-col">
                              <div class="relative">
                                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                  <div class="w-full border-t border-gray-300"></div>
                                </div>
                                <div class="relative flex justify-center">
                                  <span class="bg-white px-2 text-sm text-gray-500">Thème</span>
                                </div>
                              </div>
                              <div class="pt-6 pb-10">
                                <div class="relative items-stretch mt-2">
                                  <theme></theme>
                                </div>
                              </div>
                              <div class="relative">
                                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                  <div class="w-full border-t border-gray-300"></div>
                                </div>
                                <div class="relative flex justify-center">
                                  <span class="bg-white px-2 text-sm text-gray-500">Couleurs</span>
                                </div>
                              </div>
                              <div class="pt-6">
                                <color :initialColor="bgColor" @colorSelected="handleColorChange"></color>
                              </div>
                            </div>
                          </div>
                      </div>    
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';
import Theme from '../components/SettingsTheme.vue';
import Color from '../components/SettingsColor.vue';
import {
  AdjustmentsVerticalIcon,
  UserIcon,
  EnvelopeIcon,
  KeyIcon
} from '@heroicons/vue/24/outline'

export default {
  components: {
    Navbar,
    Navbar2,
    Theme,
    Color,
    AdjustmentsVerticalIcon,
    UserIcon,
    EnvelopeIcon,
    KeyIcon
  },
  data() {
    return {
      activeSection: 'preferences', // Default active section
      bgColor: 'bg-gradient-to-r from-sky-300 to-blue-300',
      userData: {
        username: ''
      },
      newPassword: '',
      confirmPassword: ''
    };
  },
  methods: {
    setActiveSection(section) {
      this.activeSection = section;
    },
    handleColorChange(newColor) {
      this.bgColor = newColor;

      // Prepare the data to be sent in the request
      const data = {
        bg_color: newColor
      };

      // Define the URL of your Django API endpoint
      const apiUrl = 'http://localhost:9000/MailAssistant/user/preferences/set_bg_color/';

      // Make the POST request using fetch
      fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('userToken')}` // Replace with your token retrieval logic
        },
        body: JSON.stringify(data)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Background color updated successfully', data);
        // Handle successful response here
      })
      .catch(error => {
        console.error('Error updating background color:', error);
        // Handle error here
      });
    },
    fetchUserData() {
      fetch('http://localhost:9000/MailAssistant/user/preferences/username/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('userToken')}` // Use the correct auth header depending on your setup
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log(data.username);
        this.userData.username = data.username;
      })
      .catch(error => {
        console.error('Fetch error:', error);
      });
    },
    handleSubmit() {
      // Check if passwords are provided and match
      if (this.newPassword && this.newPassword === this.confirmPassword) {
        // Update password
        this.updatePassword();
      }

      // Always update username
      this.updateUsername();
    },
    updatePassword() {
      fetch('http://localhost:9000/MailAssistant/user/preferences/update-password/', { // Replace with your actual API URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('userToken')}`
        },
        body: JSON.stringify({ password: this.newPassword })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Password updated successfully', data);
        // Handle successful password update
      })
      .catch(error => {
        console.error('Error updating password:', error);
        // Handle error
      });
    },
    updateUsername() {
      fetch('http://localhost:9000/MailAssistant/user/preferences/update-username/', { // Replace with your actual API URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('userToken')}`
        },
        body: JSON.stringify({ username: this.userData.username })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Username updated successfully', data);
        // Handle successful username update
      })
      .catch(error => {
        console.error('Error updating username:', error);
        // Handle error
      });
    },
    async refreshToken() {
      // Get the refresh token from local storage
      const refresh_token = localStorage.getItem('refreshToken');

      if (!refresh_token) {
          throw new Error('No refresh token found');
      }

      // Set up the request options for the fetch call
      const requestOptions = {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refresh: refresh_token }),
      };

      try {
          // Make the POST request to the refresh token endpoint
          const response = await fetch('http://localhost:9000/MailAssistant/api/token/refresh/', requestOptions);

          // Check if the response status is OK (200)
          if (!response.ok) {
              throw new Error(`Failed to refresh token: ${response.statusText}`);
          }

          // Parse the JSON response to get the new access token
          const data = await response.json();
          const new_access_token = data.access;

          // Save the new access token to local storage
          localStorage.setItem('userToken', new_access_token);

          return new_access_token;
      } catch (error) {
          console.error('Error refreshing token: ', error.message);
          // Handle the error (e.g., by redirecting the user to a login page)
          throw error;
      }
    },
    async getUserBgColor() {
      try {
          const response = await fetch('http://localhost:9000/MailAssistant/user/preferences/bg_color/', {
          method: 'GET',
          headers: {
              'Authorization': `Bearer ${localStorage.getItem('userToken')}`,
              'Content-Type': 'application/json'
          }
          });

          if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
          }

          const data = await response.json();
          console.log(data);
          this.bgColor = data.bg_color;
          // Do something with the response data (e.g., update component state)
      } catch (error) {
          console.error("Error fetching user background color:", error.message);
          // Handle the error (e.g., show an error message to the user)
      }
    },
  },
  async mounted() {
    this.refreshToken();
    this.getUserBgColor();
    this.fetchUserData();
  }
}
</script>