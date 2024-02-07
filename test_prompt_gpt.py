######################## GPT - 3.5 turbo API SETTINGS ########################
import json
from colorama import Fore
import openai


ORGANIZATION = "org-YSlFvq9rM1qPzM15jewopUUt"
API_KEY = "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"



def get_prompt_response(formatted_prompt):
    """Returns the prompt response"""
    client = openai.OpenAI(organization=ORGANIZATION, api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "assistant",
            "content": formatted_prompt
        }]
    )
    return response


def extract_contacts_recipients(query):
    template = """I am not able to fix this error. Provide me a valid code please

ERROR in [eslint]
/home/arolet/MailAssistant/frontend/src/views/Login.vue
  101:11  error  'showNotification' is not defined     no-undef
  102:11  error  'backgroundColor' is not defined      no-undef
  103:11  error  'notificationTitle' is not defined    no-undef
  104:11  error  'notificationMessage' is not defined  no-undef
  108:9   error  'showNotification' is not defined     no-undef
  109:9   error  'backgroundColor' is not defined      no-undef
  110:9   error  'notificationTitle' is not defined    no-undef
  111:9   error  'notificationMessage' is not defined  no-undef   
    """
    formatted_prompt = template.format(query=query)
    response = get_prompt_response(formatted_prompt)
    response_text = response.choices[0].message.content.strip()    
    print(response_text)


query = """


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
            <input id="password" v-model="password" name="password" type="password" autocomplete="current-password"
              required
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
import ShowNotification from '../components/ShowNotification.vue';


// Variables pour afficher une notification
let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
</script>

<script>
import axios from 'axios';
import { ref } from 'vue';


export default {
  name: 'UserLogin',
  setup() {
    const username = ref('');
    const password = ref('');
    const logo = require('@/assets/LogoAugmentAI_export4.png');

    const login = async (event) => {
      event.preventDefault();
      try {
        const response = await axios.post('http://localhost:9000/MailAssistant/api/login/', {
          username: username,
          password: password
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
          this.$router.push({ name: 'home' });
        } else {
          // Show the pop-up
          showNotification = true;
          backgroundColor = 'bg-red-300';
          notificationTitle = 'Erreur lors de la connexion';
          notificationMessage = response.error;
        }
      } catch (error) {
          // Show the pop-up
        showNotification = true;
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Erreur lors de la connexion';
        notificationMessage = error;
      }
    };

    return { username, password, logo, login };
  }
};
</script>

"""


extract_contacts_recipients(query)