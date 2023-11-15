<template>
    <div v-if="loading">
        <Loading class=""></Loading>
    </div>
    <div v-else>
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
                            <div class="grid grid-cols-10 gap-6 items-center divide-x divide-gray-300">
                                <div class="col-span-3 h-full justify-center">
                                    <!-- Assistant Up -->
                                    <div class="flex pt-6 pb-6">
                                        <div class="mr-4 flex-shrink-0 self-center">
                                            <!--
                                            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-[conic-gradient(at_left,_var(--tw-gradient-stops))] from-rose-400 via-amber-400 to-rose-200">
                                                <span class="text-lg font-medium leading-none text-white">AO</span>
                                            </span>-->   
                                            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-700">
                                                <span class="text-lg font-medium leading-none text-white">AO</span>
                                            </span>     
                                        </div>
                                        <div>
                                            <p class="mt-1" id="animated-text" ref="animatedText"></p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-span-7 h-full flex items-center pb-5">
                                    <div class="w-full flex items-center justify-center pt-5">
                                        <div class="sm:hidden">
                                            <label for="tabs" class="sr-only">Select a tab</label>
                                            <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
                                            <select id="tabs" name="tabs" class="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500" v-model="selectedTopic">
                                                <option v-for="category in categories" :key="category">{{ category }}</option>
                                            </select>
                                        </div>
                                        <div class="hidden sm:block w-full">
                                            <nav class="flex justify-center space-x-4 w-full" aria-label="Tabs">
                                                <a v-for="category in categories" :key="category" href="#" @click="selectCategory(category)" class="flex text-gray-600 rounded-md px-8 py-2 text-sm font-medium" :class="{'bg-gray-500 bg-opacity-10 text-gray-800': selectedTopic === category, 'text-gray-600 hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800': selectedTopic !== category}">
                                                    {{ category }}
                                                    <span v-if="emails[category] && emails[category].length > 0" class="bg-gray-100 text-gray-900 ml-3 hidden rounded-full py-0.5 px-2.5 text-xs font-medium md:inline-block">{{ emails[category].length }}</span>
                                                </a>
                                            </nav>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </main>
                    <div class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm ring-black ring-opacity-5">
                        <!-- Content goes here -->
                        <div v-if="!emails[selectedTopic]" class="flex flex-col w-full h-full rounded-xl">
                            <div class="flex flex-col justify-center items-center h-full mx-4 my-4 rounded-lg border-2 border-dashed border-gray-300 p-12 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1" stroke="currentColor" class="mx-auto h-14 w-14 text-gray-400">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                                </svg>
                                <span class="mt-2 block text-md font-semibold text-gray-900">Aucun nouveau mail</span>
                            </div>
                        </div>
                        <ul role="list" class="flex flex-col w-full h-full rounded-xl">
                            <li v-if="emails[selectedTopic] && emails[selectedTopic]['Important'] && emails[selectedTopic]['Important'].length > 0" class="py-10 px-8 mx-4 my-4 rounded-xl bg-red-100 bg-opacity-50 hover:border border-red-700 border-opacity-20"> <!-- ring-1 ring-red-700 ring-opacity-20 -->
                                <div class="float-right mt-[-25px] mr-[-10px]">
                                    <exclamation-triangle-icon class="w-6 h-6 text-red-500" />
                                </div>
                                <!-- Your content -->
                                <div class="flex">
                                    <div class="flex">
                                        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-red-400 dark:bg-red-200">
                                            <span class="text-lg font-medium leading-none text-white dark:text-red-400">AO</span>
                                        </span>
                                        <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-500" />-->
                                    </div>
                                    <div class="ml-6 flex-grow">
                                        <div class="overflow-hidden border-l-4 border-red-500  hover:rounded-l-xl dark:border-red-300">
                                            <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                                <li v-for="item in emails[selectedTopic]['Important']" :key="item.id" class="px-6 py-4 hover:bg-opacity-70 dark:hover:bg-red-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center" @click="toggleHiddenParagraph(item.id)">
                                                    <div class="col-span-8">
                                                        <div class="flex-auto">
                                                            <div class="flex items-baseline justify-between gap-x-4">
                                                                <p class="text-sm font-semibold leading-6 text-red-700 dark:text-white">{{ item.name }}</p>
                                                            </div>
                                                            <p class="mt-1 text-md text-gray-700 leading-relaxed dark:text-red-50">{{ item.description }}</p>
                                                        </div>
                                                        <ul v-show="showHiddenParagraphs[item.id]" role="list" class="text-black text-sm/6 pt-2" :ref="'parentElement' + item.id">
                                                            <li v-for="detail in item.details" :key="detail.id" class="pl-8" :ref="'hiddenText' + item.id" :data-text="detail.text">
                                                            </li>
                                                        </ul>
                                                    </div>
                                                    <div class="col-span-2">
                                                        <div class="flex justify-center">
                                                            <span class="isolate inline-flex rounded-2xl">
                                                                <div class="group">
                                                                    <button @click="openModal(item)" type="button" class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                                        <eye-icon class="w-5 h-5 text-red-500 group-hover:text-white" />
                                                                    </button>
                                                                </div>
                                                                <div class="group">
                                                                    <button type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                                        <check-icon class="w-5 h-5 text-red-500 group-hover:text-white" />
                                                                    </button>
                                                                </div>
                                                                <div class="group">
                                                                    <button type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                                        <arrow-uturn-left-icon class="w-5 h-5 text-red-500 group-hover:text-white" />
                                                                    </button>
                                                                </div>
                                                                <div class="group">
                                                                    <button type="button" class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                                        <ellipsis-horizontal-icon class="w-5 h-5 text-red-500 group-hover:text-white" />                                                        
                                                                    </button>
                                                                </div>
                                                            </span> 
                                                        </div>
                                                        <!--
                                                        <span class="isolate inline-flex rounded-2xl">
                                                            <button type="button" class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 border-r border-red-300 hover:bg-gray-50 focus:z-10">
                                                                <span class="sr-only">Previous</span>
                                                                <eye-icon class="w-5 h-5 text-red-500" />
                                                            </button>
                                                            <button type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 border-l border-red-300 hover:bg-gray-50 focus:z-10">
                                                                <check-icon class="w-5 h-5 text-red-500" />
                                                            </button>
                                                            <button type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 border-l border-red-300 hover:bg-gray-50 focus:z-10">
                                                                <arrow-uturn-left-icon class="w-5 h-5 text-red-500" />
                                                            </button>
                                                            <button type="button" class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-gray-400 border-l border-red-300 hover:bg-gray-50 focus:z-10">
                                                                <ellipsis-horizontal-icon class="w-5 h-5 text-red-500" />                                                        
                                                            </button>
                                                        </span>-->
                                                        
                                                    </div>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </li>
                            <!-- More items... -->
                            <li v-if="emails[selectedTopic] && emails[selectedTopic]['Information'] && emails[selectedTopic]['Information'].length > 0" class="py-10 px-8 mx-4 my-4 rounded-xl bg-blue-100 bg-opacity-50 hover:border border-blue-700 border-opacity-20 w-full"> <!-- ring-1 ring-blue-700 ring-opacity-20 -->
                                <div class="float-right mt-[-25px] mr-[-10px]">
                                    <information-circle-icon class="w-6 h-6 text-blue-500" />
                                </div>
                                <!-- Your content -->
                                <div class="flex">
                                    <div class="flex">
                                        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-blue-500 dark:bg-blue-200">
                                            <span class="text-lg font-medium leading-none text-white dark:text-gray-800">AO</span>
                                        </span>
                                        <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-blue-800" />-->
                                    </div>
                                    <div class="ml-6 flex-grow">
                                        <div class="overflow-hidden border-l-4 hover:rounded-l-xl border-blue-300 dark:bg-blue-500">
                                            <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                                <li v-for="item in emails[selectedTopic]['Information']" :key="item.id" class="px-6 py-4 hover:bg-opacity-70 dark:hover:bg-blue-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center" @click="toggleHiddenParagraph(item.id)">
                                                    <div >
                                                        <div class="col-span-8">
                                                            <div class="flex-auto">
                                                                <div class="flex items-baseline justify-between gap-x-4">
                                                                    <p class="text-sm font-semibold leading-6 text-blue-800 dark:text-white">{{ item.name }}</p>
                                                                </div>
                                                                <p class="mt-1 text-md text-gray-700 leading-relaxed dark:text-blue-50">{{ item.description }}</p>
                                                            </div>
                                                            <ul v-show="showHiddenParagraphs[item.id]" role="list" class="text-black text-sm/6 pt-2" :ref="'parentElement' + item.id">
                                                                <li v-for="detail in item.details" :key="detail.id" class="pl-8" :ref="'hiddenText' + item.id" :data-text="detail.text">
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </li>
                            <div v-if="emails[selectedTopic] && emails[selectedTopic]['Useless'] && emails[selectedTopic]['Useless'].length" class="flex-1 mx-4 my-4 rounded-xl bg-gray-100 hover:border border-gray-700 border-opacity-20 w-full">
                                <li class="py-10 px-8"> <!-- ring-1 ring-red-700 ring-opacity-20 --> <!-- BUG A CORRIGER : ESPACE BLANC BOTTOM -->
                                    <div class="float-right mt-[-25px] mr-[-10px]">
                                        <trash-icon class="w-6 h-6 text-gray-500" />
                                    </div>
                                    <!-- Your content -->
                                    <div class="flex">
                                        <div class="flex">
                                            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-400 dark:bg-red-200">
                                                <span class="text-lg font-medium leading-none text-white dark:text-red-400">AO</span>
                                            </span>
                                            <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-500" />-->
                                        </div>
                                        <div class="ml-6 ">
                                            <div class="overflow-hidden border-l-4 hover:rounded-l-xl border-gray-500 dark:border-red-300" @click="toggleHiddenParagraph(3)">
                                                <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                                    <li class="px-6 py-4 dark:bg-red-500 hover:bg-opacity-70 dark:hover:bg-opacity-100">
                                                        <div class="flex-auto">
                                                            Vous avez reçu <span class="font-semibold text-gray-800 dark:text-white hover:text-gray-700">4</span> mails inutiles. Cliquez pour voir.
                                                        </div>
                                                        <ul role="list" v-show="showHiddenParagraphs[3]" class="text-gray-800 text-sm/6 pt-2" ref="parentElement3">
                                                            <li class="pl-8" ref="hiddenText3" data-text="- Fabien Huet est en vacances dans les Alpes."></li>
                                                            <li class="pl-8" ref="hiddenText3" data-text="- Il demande à recevoir les différentes informations pour le BP afin d'avancer rapidement sur le sujet."></li>
                                                            <li class="pl-8" ref="hiddenText3" data-text="- Il souhaite également prendre rendez-vous avec son expert-comptable d'ici la fin du mois."></li>
                                                        </ul>
                                                    </li>
                                                    <!-- More items... -->
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </div>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <ModalSeeMail :isOpen="showModal" :email="selectedEmail" @update:isOpen="updateModalStatus" />
    </div>
</template>

<script>
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';
import ModalSeeMail from '../components/SeeMail.vue';
//import { ref } from 'vue';
import {
    //ChatBubbleOvalLeftEllipsisIcon,
    ExclamationTriangleIcon,
    InformationCircleIcon,
    TrashIcon,
    ArrowUturnLeftIcon,
    CheckIcon,
    EllipsisHorizontalIcon,
    //HandRaisedIcon,
    EyeIcon,
} from '@heroicons/vue/24/outline'

export default {
    name: 'UserHome',
    components: {
        Navbar,
        Navbar2,
        //ChatBubbleOvalLeftEllipsisIcon,
        ExclamationTriangleIcon,
        InformationCircleIcon,
        TrashIcon,
        ArrowUturnLeftIcon,
        CheckIcon,
        EllipsisHorizontalIcon,
        //HandRaisedIcon,
        EyeIcon,
        ModalSeeMail
    },
    methods: {
        openModal(email) {
            this.selectedEmail = email; // Set the email data for the clicked email
            this.showModal = true; // Open the modal
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
        updateModalStatus(status) {
            this.showModal = status;
        },
        animateText() {
            let text = "Bonjour ! Vous avez reçu 4 nouveaux mails.";
            let target = this.$refs.animatedText;
            let characters = text.split("");
            let currentIndex = 0;
            const interval = setInterval(() => {
                if (currentIndex < characters.length) {
                    target.textContent += characters[currentIndex];
                    currentIndex++;
                } else {
                    clearInterval(interval);
                }
            }, 30);
        },
        toggleHiddenParagraph(index) {
            console.log("Item ID:",index)
            console.log("All refs:",this.$refs)
            console.log('parentElement: ', this.$refs['parentElement' + index])
            console.log("Test: ", this.$refs['parentElement' + index][0].children)
            // if(this.$refs['parentElement' + index]) {
            //     console.log("Ref for current index:", this.$refs['parentElement' + index]);
            // } else {
            //     console.log(`Ref for index ${index} does not exist.`);
            // }
            this.showHiddenParagraphs[index] = !this.showHiddenParagraphs[index];
            this.$nextTick(() => {
                if (this.showHiddenParagraphs[index] && !this.animationTriggered[index]) {
                    const parentElement = this.$refs['parentElement' + index][0];
                    const elements = parentElement.children;
                    console.log("Elements:", elements)

                    const delays = [0];
                    for (let i = 0; i < elements.length; i++) {
                        const duration = this.animateHiddenText(elements[i], delays[i]);
                        delays.push(delays[i] + duration + 20);
                    }
                    this.animationTriggered[index] = true;
                }
            });
        },
        animateHiddenText(element, delay = 0) {
            const characters = element.dataset.text.split('');
            const duration = characters.length * 5;
            setTimeout(() => {
                element.textContent = '';
                let currentIndex = 0;
                const interval = setInterval(() => {
                    if (currentIndex < characters.length) {
                        element.textContent += characters[currentIndex];
                        currentIndex++;
                    } else {
                        clearInterval(interval);
                    }
                }, 5);
            }, delay);
            return duration;
        },
        selectCategory(category) {
            this.selectedTopic = category;
            console.log("CHANGE CATEGORY");
        }
    },
    async mounted() {
        this.getUserBgColor();
        this.animateText();
        // Fetch the token. This can be from a Vue data property, VueX store, or local storage
        const token = localStorage.getItem('userToken');
        const refresht = localStorage.getItem('refreshToken');

        console.log("TOKEN", token);
        console.log("TOKEN_r", refresht);

        const requestOptions = {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        };
        try {
            // Fetch the message
            const messageResponse = await fetch('http://localhost:9000/MailAssistant/message/');
            // If Unauthorized, handle accordingly
            if (messageResponse.status === 401) {
                // Handle token expiration or invalid token
                // Possibly refresh the token or redirect to login page
                return; // exit early or throw an error, based on your desired flow
            }
            const messageData = await messageResponse.json();
            this.messageText = messageData.text;
            console.log("TEXT",this.messageText);

            console.log("REQUEST OPTIONS", requestOptions);

            // Fetch the categories
            const categoryResponse = await fetch(`http://localhost:9000/MailAssistant/user/categories/`, requestOptions);
            // Again, check for Unauthorized
            if (categoryResponse.status === 401) {
                console.log("ERROR 401 : user categories")
                // Refresh the token
                this.refreshToken();
                // Update requestOptions with new token
                requestOptions.headers['Authorization'] = `Bearer ${token}`;
                // Retry the request
                const categoryRetryResponse = await fetch(`http://localhost:9000/MailAssistant/user/categories/`, requestOptions);
                const categoryData = await categoryRetryResponse.json();
                console.log("CategoryData", categoryData);
                this.categories = categoryData.map(category => category.name);
                console.log("Assigned categories:", this.categories);
                // Handle token expiration or invalid token
                return; // exit early or throw an error
            }
            const categoryData = await categoryResponse.json();
            console.log("CategoryData", categoryData);
            this.categories = categoryData.map(category => category.name);
            console.log("Assigned categories:", this.categories);

            // Fetch emails
            const emailResponse = await fetch(`http://localhost:9000/MailAssistant/user/emails/`, requestOptions);
            if (emailResponse.status === 401) {
                // Handle token expiration or invalid token
                return; // exit early or throw an error
            }
            const emailData = await emailResponse.json();
            console.log('fetchData: ',emailData)
            this.emails = emailData;

        } catch (error) {
            console.error('Failed to fetch data:', error);
        }
    },
    data() {
        return {
            // showHiddenParagraphs: [false, false, false, false, false],
            showHiddenParagraphs: {},
            animationTriggered: [false, false, false],
            showModal: false,
            messageText: '',
            categories: [],
            selectedTopic: 'Administrative',
            bgColor: 'bg-gradient-to-r from-sky-300 to-blue-300',
            selectedEmail: null,
            // emails: { "": {
            //     "Important": [],
            //     "Information": [],
            //     "Useless": []
            //     }
            // }
            emails: {}
            // items: [{id: 1, name: 'Jean', description: 'test', topic: 'ESAIP', importance: 'Information', details: [{id: 1, text: 'text'},{id: 3, text: 'bullet'},{id: 2, text: 'blabla'}]},
            // {id: 23, name: 'Marc', description: 'Premier test', topic: 'ESAIP', importance: 'Important', details: [{id: 4, text: 'bonjour'},{id: 6, text: 'ok'},{id: 5, text: 'enfin'}]}
            
            // ],
            // items: {
            //     "ESAIP": {
            //         "Important": [
            //             {
            //                 id: 1, 
            //                 name: 'Jean', 
            //                 description: 'test', 
            //                 details: [
            //                     {id: 1, text: 'text'},
            //                     {id: 3, text: 'bullet'},
            //                     {id: 2, text: 'blabla'}
            //                 ]
            //             }
            //         ],
            //         "Information": [
            //             {
            //                 id: 2, 
            //                 name: 'Marc', 
            //                 description: 'Premier test', 
            //                 details: [
            //                     {id: 4, text: 'bonjour'},
            //                     {id: 6, text: 'ok'},
            //                     {id: 5, text: 'enfin'}
            //                 ]
            //             }
            //         ]
            //     },
            //     "Autres": {
            //         "Important": [
            //             {
            //                 id: 3, 
            //                 name: 'Banque', 
            //                 description: 'test', 
            //                 details: [
            //                     {id: 7, text: 'prêt'},
            //                     {id: 8, text: 'argent'},
            //                     {id: 9, text: 'euro'}
            //                 ]
            //             }
            //         ],
            //         "Information": [
            //             {
            //                 id: 4, 
            //                 name: 'Avocat', 
            //                 description: 'Premier test', 
            //                 details: [
            //                     {id: 10, text: 'contrat'},
            //                     {id: 11, text: 'frais'},
            //                     {id: 12, text: 'fruit'}
            //                 ]
            //             }
            //         ]
            //     }
            //     // ... potentially other topics
            // }
        }
    }
}
</script>
