<template>
    <div class="h-screen bg-white flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company">
        <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Connectez-vous à votre compte</h2>
        </div>

        <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form class="space-y-6">
            <div>
            <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Adresse email</label>
            <div class="mt-2">
                <input id="email" name="email" v-model="username" autocomplete="email" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            </div>
            </div>

            <div>
            <div class="flex items-center justify-between">
                <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Mot de passe</label>
                <div class="text-sm">
                <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">Mot de passe oublié ?</a>
                </div>
            </div>
            <div class="mt-2">
                <input id="password" v-model="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
            </div>
            </div>

            <div>
            <button type="button" @click="login" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Se connecter</button>
            </div>
        </form>

        <p class="mt-10 text-center text-sm text-gray-500">
            Vous n'êtes pas inscrit ?
            <a href="#" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Commencer votre essai gratuit</a>
        </p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserLogin',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:9000/MailAssistant/api/login/', {
          username: this.username,
          password: this.password
        });
        const token = response.data.access;
        localStorage.setItem('userToken', token);
        
        // Store the token in Vuex store or in-memory for later use

        // Redirect to home13 after successful login
        this.$router.push({ name: 'home' });

      } catch (error) {
        console.error("Error during login:", error.response ? error.response.data : error.message);
      }
    }
  }
}
</script>