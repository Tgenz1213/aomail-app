<!-- V1 -->
<template>
  <div class="flex min-h-full flex-1 flex-col justify-center py-12 sm:px-6 lg:px-8" :class="bgColor">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=black" alt="Your Company" />
      <h2 class="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Inscrivez-vous</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-[580px]"><!-- 480px -->
      <div class="flex flex-col h-full bg-slate-200 bg-opacity-80 rounded-lg"> 
        <div class="divide-y divide-slate-200">
          <div class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-lg bg-gray-400 bg-opacity-10"> 
            <nav aria-label="Progress">
              <!--<div class="absolute right-4 left-4">-->
              <ol role="list" class="flex items-center">
                <li class="relative pr-6 sm:pr-32">
                  <!-- Completed Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">Step 1</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-32">
                  <!-- Current Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-400 bg-white" aria-current="step">
                    <span class="h-2.5 w-2.5 rounded-full bg-gray-400" aria-hidden="true"></span>
                    <span class="sr-only">Step 3</span>
                  </a>
                </li>
                <li class="relative">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                    <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300" aria-hidden="true"></span>
                    <span class="sr-only">Step 5</span>
                  </a>
                </li>
              </ol>
              <!--</div>-->
            </nav>
          </div>
          <div class="bg-white px-6 py-10 shadow sm:rounded-b-lg sm:px-12 hover:shadow-lg">
            <form class="space-y-6">
              <div v-if="step === 0">
                <div v-if="passwordError" class="mt-2 text-sm text-red-600">
                  {{ passwordError }}
                </div>
                <div>
                  <label for="login" class="block text-sm font-medium leading-6 text-gray-900">Identifiant</label>
                  <div class="mt-2">
                    <input v-model="login" id="login" type="login" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" />
                  </div>
                </div>

                <div>
                  <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Mot de passe</label>
                  <div class="mt-2">
                    <input v-model="password" id="password" type="password" @input="passwordError = ''" autocomplete="current-password" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" />
                  </div>
                </div>

                <div>
                  <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Confirmer le mot de passe</label>
                  <div class="mt-2">
                    <input v-model="confirmPassword" id="confirm_password" type="password" autocomplete="current-password" @input="passwordError = ''" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" />
                  </div>
                </div>

                <div>
                  <div class="pt-6">
                    <button @click="nextStep0" class="flex w-full justify-center rounded-md bg-slate-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Continuer</button>
                  </div>
                </div>
              </div>
              <div v-if="step === 1">
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
                    <color @colorSelected="updateBgColor"></color>
                  </div>
                </div>
                <div>
                  <div class="pt-6">
                    <button @click="nextStep" class="flex w-full justify-center rounded-md bg-gray-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Continuer</button>
                  </div>
                </div>
              </div>
            </form>
            <!--<form class="space-y-6" action="#" method="POST">
              <div>
                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Identifiant</label>
                <div class="mt-2">
                  <input id="email" name="email" type="email" autocomplete="email" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" />
                </div>
              </div>

              <div>
                <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Mot de passe</label>
                <div class="mt-2">
                  <input id="password" name="password" type="password" autocomplete="current-password" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" />
                </div>
              </div>

              <div>
                <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Confirmer le mot de passe</label>
                <div class="mt-2">
                  <input id="password" name="password" type="password" autocomplete="current-password" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" />
                </div>
              </div>

              <div>
                <div class="pt-6">
                  <button type="submit" class="flex w-full justify-center rounded-md bg-slate-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Continuer</button>
                </div>
              </div>
            </form>-->
            <div>
          </div>
        </div>
      </div>
    </div>
      <p class="mt-10 text-center text-sm text-gray-500">
        Vous avez un compte?
        {{ ' ' }}
        <a href="#" class="font-semibold leading-6 text-gray-900 hover:text-black">Connectez-vous</a>
      </p>
    </div>
  </div>
</template>
<script>
import { ref } from 'vue';
import Theme from '../components/SettingsTheme.vue';
import Color from '../components/SettingsColor.vue';

export default {
  name: 'UserSignUp',
  components: {
    Theme,
    Color
  },
  setup() {
    const bgColor = ref('') // default background color

    const updateBgColor = (newBgColor) => {
      bgColor.value = newBgColor
    }

    return {
      bgColor,
      updateBgColor
    }
  },
  data() {
    return {
      step: 0,
      login: "",
      password: "",
      passwordError: '',
      theme: "",
      color: "",
    }
  },
  methods: {
    nextStep0() {
      if (this.password !== this.confirmPassword) {
        this.passwordError = 'Passwords do not match. Please try again.';
        return; 
      }  
      this.step++;
    },
    nextStep() {
      this.step++;
    }
  }
}
</script>