<template>
    <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" />
    <div class="h-screen bg-white flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <img class="mx-auto h-12 w-auto" :src="logo" alt="Your Company">
            <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Connectez-vous à votre
                compte</h2>
        </div>

        <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form class="space-y-6">
                <div>
                    <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Identifiant</label>
                    <div class="mt-2">
                        <input id="email" name="email" v-model="username" autocomplete="email" required
                            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6">
                    </div>
                </div>

                <div>
                    <div class="flex items-center justify-between">
                        <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Mot de passe</label>
                        <div class="text-sm">
                            <a href="#" class="font-semibold text-gray-900 hover:text-gray-600">Mot de passe oublié ?</a>
                        </div>
                    </div>
                    <div class="mt-2">
                        <input id="password" v-model="password" name="password" type="password"
                            autocomplete="current-password" required
                            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6">
                    </div>
                </div>

                <div>
                    <button type="button" @click="login"
                        class="flex w-full justify-center rounded-md bg-gray-900 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-900">Se
                        connecter</button>
                </div>
            </form>

            <p class="mt-10 text-center text-sm text-gray-500">
                Vous n'êtes pas inscrit ?
                <a href="/signup" class="font-semibold leading-6 text-gray-900 hover:text-gray-600">Commencer votre essai
                    gratuit</a>
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import ShowNotification from '../components/ShowNotification.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';


const router = useRouter();
let username = ref('');
let password = ref('');
// Variables to display a notification
let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');

// Function to handle login
async function login() {
    try {
        const response = await axios.post('http://localhost:9000/MailAssistant/api/login/', {
            username: username.value,
            password: password.value
        });

        if (response.status === 200) {
            // Set access token and email for API calls
            const email = response.data.email;
            localStorage.setItem('email', email);
            const token = response.data.access_token;
            localStorage.setItem('access_token', token);

            // Fetch color
            const colorResponse = await axios.get("http://localhost:9000/MailAssistant/user/preferences/bg_color/", {
                headers: { Authorization: `Bearer ${token}` }
            });

            const bgColor = colorResponse.data.bg_color;
            localStorage.setItem('bgColor', bgColor);

            // Redirect to home page after successful login
            router.push({ name: 'home' });
        }
    } catch (error) {
        // Show the pop-up
        showNotification.value = true;
        backgroundColor.value = 'bg-red-300';
        notificationTitle.value = 'Erreur lors de la connexion';
        notificationMessage.value = 'Informations d\'identification invalides';
    }
}
</script>

<script>
export default {
  data() {
    return {
      logo: require('@/assets/LogoAugmentAI_export4.png')
    };
  }
}
</script>