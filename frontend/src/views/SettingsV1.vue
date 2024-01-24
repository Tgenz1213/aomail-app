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
                                        <credit-card-icon class="w-4 h-4" />
                                        <a :class="{'text-gray-800': activeSection === 'subscription', 'text-gray-600': activeSection !== 'subscription'}" class="text-sm font-medium">Abonnement</a>
                                      </div>

                                      <div 
                                        :class="['flex space-x-2 items-center rounded-md py-2', 
                                                {'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'data', 
                                                  'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'data'}]"
                                        @click="setActiveSection('data')">
                                        <circle-stack-icon class="w-4 h-4" />
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
                                  <input v-model="userData.username" type="text" name="username" id="username" autocomplete="username" class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6">                                </div>
                                <div class="pt-4">
                                  <div class="grid grid-cols-2 gap-4">
                                    <div>
                                      <div class="flex space-x-1 items-center">
                                        <key-icon class="w-4 h-4" />
                                        <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Nouveau mot de passe</label>
                                      </div>
                                      <div class="relative items-stretch mt-2">
                                        <input v-model="newPassword" type="text" name="first-name" id="first-name" autocomplete="given-name" class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6">
                                      </div>
                                    </div>
                                    <div>
                                      <div class="flex space-x-1 items-center">
                                        <key-icon class="w-4 h-4" />
                                        <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Confirmer le mot de passe</label>
                                      </div>
                                      <div class="relative items-stretch mt-2">
                                        <input v-model="confirmPassword" type="text" name="first-name" id="first-name" autocomplete="given-name" class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6">
                                      </div>
                                    </div>
                                  </div>
                                </div>
                                <div class="flex justify-end pt-4">
                                  <button @click="handleSubmit" class="rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600">Modifier</button> <!-- TO CODE : Notification system that worn the user when the notification appears -->
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
                                  <button @click="deleteAccount" type="submit" class="rounded-md bg-red-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500">Supprimer</button>
                                </div>
                              </div>
                            </div>
                          </div>
                      </div>    
                  </div>
                  <div v-if="activeSection === 'subscription'" class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm hover:shadow-lg ring-black ring-opacity-5 section">
                    <div class="flex px-6 py-6 shadow-sm border-b border-gray-200 bg-gray-50 rounded-t-2xl">
                      <h1 class="text-2xl" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Mon abonnement</h1>         
                    </div>
                    <div class="float-right mt-[-70px] mr-[10px]">
                      <credit-card-icon class="w-6 h-6 text-gray-500" />
                    </div>
                    <!-- We've used 3xl here, but feel free to try other max-widths based on your needs -->
                    <div class="mx-8 2xl:mx-16">
                      <!-- Content goes here -->
                      <subscription></subscription>
                    </div> 
                  </div>
                  <div v-if="activeSection === 'data'" class="flex flex-col h-full rounded-xl bg-white lg:mt-4 ring-1 shadow-sm hover:shadow-lg ring-black ring-opacity-5 section">
                    <div class="flex">
                      <div class="flex-1">
                        <div class="flex px-6 py-6 shadow-sm border-b border-gray-200 bg-gray-50 rounded-t-2xl">
                          <h1 class="text-2xl" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Mes données</h1>         
                        </div>
                        <div class="float-right mt-[-70px] mr-[10px]">
                          <circle-stack-icon class="w-6 h-6 text-gray-500" />
                        </div>
                      </div>
                    </div>
                    <!-- We've used 3xl here, but feel free to try other max-widths based on your needs -->
                    <div class="m-6 2xl:m-8 flex-grow">
                      <div class="flex items-center justify-center w-full h-full rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 text-center">
                        <div class="flex flex-col">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1" stroke="currentColor" class="w-12 h-12 mx-auto text-gray-400">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17 17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 0 0 4.486-6.336l-3.276 3.277a3.004 3.004 0 0 1-2.25-2.25l3.276-3.276a4.5 4.5 0 0 0-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437 1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008Z" />
                          </svg>
                          <span class="mt-2 block text-sm font-semibold text-gray-900">En cours de construction</span>
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
import Subscription from '../components/SettingsSubscription.vue'
import {
  AdjustmentsVerticalIcon,
  UserIcon,
  EnvelopeIcon,
  KeyIcon,
  CreditCardIcon,
  CircleStackIcon
} from '@heroicons/vue/24/outline'

export default {
  components: {
    Navbar,
    Navbar2,
    Theme,
    Color,
    Subscription,
    AdjustmentsVerticalIcon,
    UserIcon,
    EnvelopeIcon,
    KeyIcon,
    CreditCardIcon,
    CircleStackIcon
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
    async handleColorChange(newColor) {
      this.bgColor = newColor;

      const data = {
        bg_color: newColor
      };

      const apiUrl = 'http://localhost:9000/MailAssistant/user/preferences/set_bg_color/';

      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      };

      try {
        const responseData = await this.fetchWithToken(apiUrl, requestOptions);
        console.log('Background color updated successfully', responseData);
        localStorage.setItem('bgColor', newColor);
        // Handle successful response here
      } catch (error) {
        console.error('Error updating background color:', error);
        // Handle error here
      }
    },
    async fetchUserData() {
      const requestOptions = {
        headers: {
          'Content-Type': 'application/json'
        }
      };

      try {
        const data = await this.fetchWithToken('http://localhost:9000/MailAssistant/user/preferences/username/', requestOptions);
        console.log(data.username);
        this.userData.username = data.username;
        // Handle the response data as needed
      } catch (error) {
        console.error('Fetch error:', error);
        // Handle the error appropriately
      }
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
    async updatePassword() {
      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password: this.newPassword })
      };

      try {
        const data = await this.fetchWithToken('http://localhost:9000/MailAssistant/user/preferences/update-password/', requestOptions);
        console.log('Password updated successfully', data);
        // Handle successful password update
      } catch (error) {
        console.error('Error updating password:', error);
        // Handle error
      }
    },
    async updateUsername() {
      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: this.userData.username })
      };

      try {
        const data = await this.fetchWithToken('http://localhost:9000/MailAssistant/user/preferences/update-username/', requestOptions);
        console.log('Username updated successfully', data);
        // Handle successful username update
      } catch (error) {
        console.error('Error updating username:', error);
        // Handle error
      }
    },
    async deleteAccount() {
      const isChecked = document.querySelector('input[name="choice"]:checked');

      if (isChecked) {
          try {
              const access_token = localStorage.getItem('access_token');
              const url = 'http://localhost:9000/MailAssistant/api/delete_account/';

              const requestOptions = {
                  method: 'DELETE',
                  headers: {
                      'Authorization': `Bearer ${access_token}`
                  }
              };

              const responseData = await this.fetchWithToken(url, requestOptions);

              // Check the response data for success or failure
              if (responseData && responseData.message === 'User successfully deleted') {
                  // Handle successful deletion
                  console.log('Account deleted successfully.');

                  // Redirect logic on the client-side (assuming a frontend framework like Vue or React)
                  window.location.href = 'http://localhost:8080'; // Redirect to desired URL
              } else {
                  // Handle other possible server responses or inform the user
                  console.error('Failed to delete account. Unexpected server response:', responseData);
              }

          } catch (error) {
              // Handle error or inform the user about the failure
              console.error('Error deleting account:', error);
          }
      } else {
          // TODO: Inform the user that the deletion is not confirmed
          alert('Please confirm deletion by checking the checkbox.');
          console.log('Please confirm deletion by checking the checkbox.');
      }
    },
    async fetchWithToken(url, options = {}) {
      const accessToken = localStorage.getItem('access_token');
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
              localStorage.setItem('access_token', newAccessToken);
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
  },
  async mounted() {
    this.bgColor = localStorage.getItem('bgColor');
    this.fetchUserData();
  }
}
</script>