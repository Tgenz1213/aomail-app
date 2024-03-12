<template>
    <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" />
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
                                        <select id="tabs" name="tabs"
                                            class="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500">
                                            <option>Ecole ESAIP</option>
                                            <option>Entrepreneuriat</option>
                                            <option selected>Administratif</option>
                                            <option>Autres</option>
                                        </select>
                                    </div>
                                    <div class="hidden sm:block w-full">
                                        <nav class="flex justify-center space-x-4 w-full" aria-label="Tabs">
                                            <!-- Current: "bg-gray-200 text-gray-800", Default: "text-gray-600 hover:text-gray-800" -->
                                            <div class="text-sm font-medium cursor-pointer"
                                                :class="['flex space-x-2 items-center rounded-md py-2', { 'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'preferences', 'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'preferences' }]"
                                                @click="setActiveSection('preferences')">
                                                <adjustments-vertical-icon class="w-4 h-4" />
                                                <a
                                                    :class="{ 'text-gray-800': activeSection === 'preferences', 'text-gray-600': activeSection !== 'preferences' }">Préférences</a>
                                            </div>
                                            <div class="text-sm font-medium cursor-pointer"
                                                :class="['flex space-x-2 items-center rounded-md py-2', { 'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'account', 'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'account' }]"
                                                @click="setActiveSection('account')">
                                                <user-icon class="w-4 h-4" />
                                                <a :class="{ 'text-gray-800': activeSection === 'account', 'text-gray-600': activeSection !== 'account' }"
                                                    class="text-sm font-medium">Mon Compte</a>
                                            </div>
                                            <div class="text-sm font-medium cursor-pointer"
                                                :class="['flex space-x-2 items-center rounded-md py-2', { 'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'subscription', 'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'subscription' }]"
                                                @click="setActiveSection('subscription')">
                                                <credit-card-icon class="w-4 h-4" />
                                                <a :class="{ 'text-gray-800': activeSection === 'subscription', 'text-gray-600': activeSection !== 'subscription' }"
                                                    class="text-sm font-medium">Abonnement</a>
                                            </div>

                                            <div class="text-sm font-medium cursor-pointer"
                                                :class="['flex space-x-2 items-center rounded-md py-2', { 'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'data', 'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'data' }]"
                                                @click="setActiveSection('data')">
                                                <circle-stack-icon class="w-4 h-4" />
                                                <a :class="{ 'text-gray-800': activeSection === 'data', 'text-gray-600': activeSection !== 'data' }"
                                                    class="text-sm font-medium">Mes données</a>
                                            </div>
                                        </nav>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </main>
                    <div v-if="activeSection === 'account'"
                        class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm hover:shadow-lg ring-black ring-opacity-5 section">
                        <div class="flex px-6 py-6 shadow-sm border-b border-gray-200 bg-gray-50 rounded-t-2xl">
                            <h1 class="text-2xl" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Mon
                                compte
                            </h1>
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
                                            <span class="bg-white px-2 text-sm text-gray-500">Changement d'identifiant
                                                ou de
                                                mot de passe</span>
                                        </div>
                                    </div>
                                    <div class="pt-6 pb-10">
                                        <div class="flex space-x-1 items-center">
                                            <envelope-icon class="w-4 h-4" />
                                            <label
                                                class="block text-sm font-medium leading-6 text-gray-900">Identifiant</label>
                                        </div>
                                        <div class="relative items-stretch mt-2">
                                            <input v-model="userData" type="text" name="username" id="username"
                                                autocomplete="username"
                                                class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6">
                                        </div>
                                        <div class="pt-4">
                                            <div class="grid grid-cols-2 gap-6">
                                                <div class="flex flex-col">
                                                    <div class="flex space-x-1 items-center">
                                                        <key-icon class="w-4 h-4" />
                                                        <label
                                                            class="block text-sm font-medium leading-6 text-gray-900">Nouveau
                                                            mot de passe</label>
                                                    </div>
                                                    <div class="relative items-stretch mt-2 flex">
                                                        <input v-if="!showPassword" type="password"
                                                            class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                            v-model="newPassword" />
                                                        <input v-else type="text"
                                                            class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                            v-model="newPassword" />
                                                        <div class="flex items-center">
                                                            <button @click="togglePasswordVisibility"
                                                                class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300">
                                                                <svg v-if="!showPassword"
                                                                    xmlns="http://www.w3.org/2000/svg" fill="none"
                                                                    viewBox="0 0 24 24" stroke-width="1.5"
                                                                    stroke="currentColor" class="w-6 h-6">
                                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                                        d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                                        d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                                                </svg>
                                                                <svg v-else xmlns="http://www.w3.org/2000/svg"
                                                                    fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                                                    stroke="currentColor" class="w-6 h-6">
                                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                                        d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                                                                </svg>
                                                            </button>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="flex flex-col">
                                                    <div class="flex space-x-1 items-center">
                                                        <key-icon class="w-4 h-4" />
                                                        <label
                                                            class="block text-sm font-medium leading-6 text-gray-900">Confirmer
                                                            le mot de passe</label>
                                                    </div>
                                                    <div class="relative items-stretch mt-2 flex">
                                                        <input v-if="!showConfirmPassword" type="password"
                                                            class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                            v-model="confirmPassword" />
                                                        <input v-else type="text"
                                                            class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                            v-model="confirmPassword" />
                                                        <button @click="toggleConfirmPasswordVisibility"
                                                            class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300">
                                                            <svg v-if="!showConfirmPassword"
                                                                xmlns="http://www.w3.org/2000/svg" fill="none"
                                                                viewBox="0 0 24 24" stroke-width="1.5"
                                                                stroke="currentColor" class="w-6 h-6">
                                                                <path stroke-linecap="round" stroke-linejoin="round"
                                                                    d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                                                <path stroke-linecap="round" stroke-linejoin="round"
                                                                    d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                                            </svg>
                                                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none"
                                                                viewBox="0 0 24 24" stroke-width="1.5"
                                                                stroke="currentColor" class="w-6 h-6">
                                                                <path stroke-linecap="round" stroke-linejoin="round"
                                                                    d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                                                            </svg>
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="flex justify-end pt-4">
                                            <button @click="handleSubmit"
                                                class="rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600">Modifier</button>
                                            <!-- TO CODE : Notification system that worn the user when the notification appears -->
                                        </div>
                                    </div>
                                    <div class="relative">
                                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                            <div class="w-full border-t border-gray-300"></div>
                                        </div>
                                        <div class="relative flex justify-center">
                                            <span class="bg-white px-2 text-sm text-gray-500">Suppression du
                                                compte</span>
                                        </div>
                                    </div>
                                    <div class="pt-6">
                                        <div class="flex space-x-1 items-center">
                                            <input type="radio"
                                                class="form-radio text-red-600 border-red-400 focus:border-red-500 focus:ring-red-200 h-5 w-5"
                                                name="choice">
                                            <label for="push-everything" class="block text-sm font-medium leading-6">Je
                                                confirme la supression
                                                de mon compte (action irréversible)</label>
                                        </div>
                                        <div class="flex justify-end pt-4">
                                            <button @click="deleteAccount" type="submit"
                                                class="rounded-md bg-red-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500">Supprimer</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-if="activeSection === 'subscription'"
                        class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm hover:shadow-lg ring-black ring-opacity-5 section">
                        <div class="flex px-6 py-6 shadow-sm border-b border-gray-200 bg-gray-50 rounded-t-2xl">
                            <h1 class="text-2xl" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Mon
                                abonnement</h1>
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
                    <div v-if="activeSection === 'data'"
                        class="flex flex-col h-full rounded-xl bg-white lg:mt-4 ring-1 shadow-sm hover:shadow-lg ring-black ring-opacity-5 section">
                        <div class="flex">
                            <div class="flex-1">
                                <div class="flex px-6 py-6 shadow-sm border-b border-gray-200 bg-gray-50 rounded-t-2xl">
                                    <h1 class="text-2xl" style="font-family: 'Poppins', sans-serif; font-weight: 500;">
                                        Mes
                                        données</h1>
                                </div>
                                <div class="float-right mt-[-70px] mr-[10px]">
                                    <circle-stack-icon class="w-6 h-6 text-gray-500" />
                                </div>
                            </div>
                        </div>
                        <!-- We've used 3xl here, but feel free to try other max-widths based on your needs -->
                        <div class="m-6 2xl:m-8 flex-grow">
                            <div
                                class="flex items-center justify-center w-full h-full rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 text-center">
                                <div class="flex flex-col">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1" stroke="currentColor" class="w-12 h-12 mx-auto text-gray-400">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M11.42 15.17 17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 0 0 4.486-6.336l-3.276 3.277a3.004 3.004 0 0 1-2.25-2.25l3.276-3.276a4.5 4.5 0 0 0-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437 1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008Z" />
                                    </svg>
                                    <span class="mt-2 block text-sm font-semibold text-gray-900">En cours de
                                        construction</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-if="activeSection === 'preferences'"
                        class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm hover:shadow-lg ring-black ring-opacity-5 section">
                        <div class="flex px-6 py-6 shadow-sm border-b border-gray-200 bg-gray-50 rounded-t-2xl">
                            <h1 class="text-2xl" style="font-family: 'Poppins', sans-serif; font-weight: 500;">Mes
                                préférences</h1>
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

<script setup>
import { API_BASE_URL } from '@/main';

// Variables to display a notification
let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
let timerId = ref(null);

let activeSection = ref('preferences'); // Default active section
let bgColor = ref(localStorage.getItem('bgColor') || '');
let userData = ref('');
let newPassword = ref('');
let confirmPassword = ref('');


onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
    fetchUserData();
    getBackgroundColor();
})

function dismissPopup() {
    showNotification.value = false;
    // Cancel the timer
    clearTimeout(timerId);
}

function displayPopup() {
    showNotification.value = true;

    timerId = setTimeout(() => {
        dismissPopup();
    }, 4000);
}

function handleKeyDown(event) {
    if (event.key === 'Tab') {
        event.preventDefault();
        switchActiveSection();
    }
}

function switchActiveSection() {
    const nextSection = {
        'preferences': 'account',
        'account': 'subscription',
        'subscription': 'data',
        'data': 'preferences'
    }

    setActiveSection(nextSection[activeSection.value]);
}

function setActiveSection(section) {
    if (section == 'account') {
        // Update the username in case it has been modified
        fetchUserData();
    }
    activeSection.value = section;
}

async function handleColorChange(newColor) {

    // this is directly linked to the ref bgColor in Vue template
    bgColor.value = newColor;

    const data = {
        bg_color: newColor
    };

    const apiUrl = `${API_BASE_URL}user/preferences/set_bg_color/`;

    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };

    try {
        const response = await fetchWithToken(apiUrl, requestOptions);

        if (response.bg_color) {
            localStorage.setItem('bgColor', newColor);
        }
    } catch (error) {
        console.error("Error updating background", error);
    }
}

async function fetchUserData() {
    const requestOptions = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const data = await fetchWithToken(`${API_BASE_URL}user/preferences/username/`, requestOptions);
        userData.value = data.username;
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Erreur récupération de votre identifiant';
        notificationMessage = error;
        displayPopup();
    }
}

async function getUsername() {

    const requestOptions = {
        headers: {
            'Content-Type': 'application/json'
        }
    }

    try {
        const data = await fetchWithToken(`${API_BASE_URL}user/preferences/username/`, requestOptions);
        return data.username;
    }
    catch (error) {
        console.error(error);
        // Show the pop-up
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Erreur récupération nom d\'utilisateur';
        notificationMessage = error;
        displayPopup();
        return;
    }
}
async function handleSubmit() {

    const requestOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        var response = await fetchWithToken(`${API_BASE_URL}check_username/`, requestOptions);
    }
    catch (error) {
        console.log("An error occured while checking the username", error);
        // Show the pop-up
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Erreur vérification nom d\'utilisateur';
        notificationMessage = error;
        displayPopup();
        return;
    }


    let resultUpdateUsername;

    if (response.available == false) {
        // Show the pop-up
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Nom d\'utilisateur déjà existant';
        notificationMessage = 'Veuillez choisir un autre nom';
        displayPopup();
        return;
    }
    else {
        try {
            let currentUsername = await getUsername();

            if (userData.value != currentUsername) {
                resultUpdateUsername = await updateUsername();
            }
        } catch (error) {
            console.error("Error occurre while retrieving data about username", error);
            // Show the pop-up
            backgroundColor = 'bg-red-300';
            notificationTitle = 'Erreur lors d\'une vérification du nom d\'utilisateur';
            notificationMessage = error;
            displayPopup();
        }
    }



    // Check if passwords are provided and match
    if (newPassword.value && newPassword.value == confirmPassword.value) {
        var resultUpdatePwd = await updatePassword();
    }

    // Handle all cases with pop-ups
    if (resultUpdateUsername) {

        if (resultUpdateUsername == 'Username updated successfully' && resultUpdatePwd == 'Password updated successfully') {
            // Show the pop-up
            backgroundColor = 'bg-green-300';
            notificationTitle = 'Succès !';
            notificationMessage = 'Votre identifiant et mot de passe ont été modifiés';
            displayPopup();
        }
        else if (!resultUpdatePwd) {

            if (resultUpdateUsername == 'Username updated successfully') {
                // Show the pop-up
                backgroundColor = 'bg-green-300';
                notificationTitle = 'Succès !';
                notificationMessage = 'Votre identifiant a bien été mis à jour';
                displayPopup();
            }
            else {
                // Show the pop-up
                backgroundColor = 'bg-green-300';
                notificationTitle = 'Erreur mise à jour identifiant';
                notificationMessage = resultUpdateUsername;
                displayPopup();
            }
        }
    }
    else if (resultUpdatePwd) {

        if (resultUpdatePwd == 'Password updated successfully') {
            // Show the pop-up
            backgroundColor = 'bg-green-300';
            notificationTitle = 'Succès !';
            notificationMessage = 'Votre mot de passe a bien été modifié';
            displayPopup();
        }
        else {
            // Show the pop-up
            backgroundColor = 'bg-red-300';
            notificationTitle = 'Erreur mise à jour mot de passe';
            notificationMessage = resultUpdatePwd;
            displayPopup();
        }
    }
}
async function updatePassword() {

    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password: newPassword.value })
    };

    try {
        const data = await fetchWithToken(`${API_BASE_URL}user/preferences/update-password/`, requestOptions);

        return 'Password updated successfully';
    } catch (error) {
        return error;
    }
}
async function updateUsername() {

    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: userData.value })
    };

    try {
        const data = await fetchWithToken(`${API_BASE_URL}user/preferences/update-username/`, requestOptions);

        return 'Username updated successfully';
    } catch (error) {
        return error;
    }
}
async function deleteAccount() {

    const isChecked = document.querySelector('input[name="choice"]:checked');

    if (isChecked) {
        try {
            const access_token = localStorage.getItem('access_token');
            const url = `${API_BASE_URL}api/delete_account/`;

            const requestOptions = {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${access_token}`
                }
            };

            const responseData = await fetchWithToken(url, requestOptions);

            // Check the response data for success or failure
            if (responseData && responseData.message === 'User successfully deleted') {
                localStorage.clear();
                // Show the pop-up
                backgroundColor = 'bg-green-300';
                notificationTitle = 'Redirection en cours...';
                notificationMessage = 'Votre compte a bien été supprimé';
                displayPopup();

                setTimeout(() => {
                    // Redirect login page
                    window.location.href = 'http://localhost:8080';
                }, 4000);

            } else {
                // Show the pop-up
                backgroundColor = 'bg-red-300';
                notificationTitle = 'Erreur suppresion de votre compte';
                notificationMessage = responseData.error;
                displayPopup();
            }
        } catch (error) {
            // Show the pop-up
            backgroundColor = 'bg-red-300';
            notificationTitle = 'Erreur suppresion de votre compte';
            notificationMessage = error;
            displayPopup();
        }
    } else {
        // Show the pop-up
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Confirmation nécessaire';
        notificationMessage = 'Cochez la case pour approuver la suppression';
        displayPopup();
    }
}
</script>

<script>
import '@fortawesome/fontawesome-free/css/all.css';
import ShowNotification from '../components/ShowNotification.vue';
import { fetchWithToken, getBackgroundColor } from '../router/index.js';
import { ref, onMounted } from 'vue';
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
            showPassword: false,
            showConfirmPassword: false
        };
    },
    methods: {
        togglePasswordVisibility(event) {
            event.preventDefault();
            this.showPassword = !this.showPassword;
        },
        toggleConfirmPasswordVisibility() {
            this.showConfirmPassword = !this.showConfirmPassword;
        }
    }
}
</script>
