<template>
    <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" @dismiss-popup="dismissPopup" />
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
    <!-- Modal for Account Deletion -->
    <transition name="modal-fade">
        <div @click.self="closeModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center "
            v-if="isModalOpen">
            <div class="bg-white rounded-lg relative w-[450px] ">
                <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
                    <button @click="closeModal" type="button"
                        class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                        <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                    </button>
                </div>
                <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
                    <div class="ml-8 flex items-center space-x-1">
                        <p class="block font-semibold leading-6 text-gray-900">{{
                            $t('settingsPage.accountPage.deleteAccount') }}
                        </p>
                    </div>
                </div>
                <div class="flex flex-col gap-4 px-8 py-6">
                    <div>
                        <label class="block text-sm font-medium leading-6 text-gray-900">
                            {{ $t('settingsPage.accountPage.confirmDeleteAccount') }}
                        </label>
                    </div>
                    <div class="mt-2 sm:mt-2 sm:flex sm:flex-row justify-between">
                        <button type="button"
                            class="ml-auto rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                            @click="closeModal">{{ $t('constants.userActions.cancel') }}</button>
                        <div class="flex-grow"></div> <!-- Flexible spacer -->
                        <button type="button"
                            class="inline-flex w-full justify-cente items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto"
                            @click="deleteAccount">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                            </svg>
                            {{ $t('settingsPage.accountPage.deleteAccount') }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </transition>

    <!-- Modal for Unlink Email -->
    <transition name="modal-fade">
        <div @click.self="closeUnlinkModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            v-if="isUnlinkModalOpen">
            <div class="bg-white rounded-lg relative w-[450px]">
                <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
                    <button @click="closeUnlinkModal" type="button"
                        class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                        <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                    </button>
                </div>
                <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
                    <div class="ml-8 flex items-center space-x-1">
                        <p class="block font-semibold leading-6 text-gray-900">{{
                            $t('settingsPage.accountPage.unlinkMyEmail') }}
                        </p>
                    </div>
                </div>
                <div class="flex flex-col gap-4 px-8 py-6">
                    <div>
                        <label class="block text-sm font-medium leading-6 text-gray-900">
                            {{ $t('settingsPage.accountPage.thisFeatureIsUnderTest') }}
                        </label>
                    </div>
                    <div class="mt-2 sm:mt-2 sm:flex sm:flex-row">
                        <button type="button"
                            class="inline-flex w-full rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:w-auto"
                            @click="closeUnlinkModal">{{ $t('constants.userActions.cancel') }}</button>
                        <div class="flex-grow"></div>
                        <button type="button"
                            class="inline-flex w-full justify-cente items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto"
                            @click="unLinkAccount">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                            </svg>
                            {{ $t('settingsPage.accountPage.unlinkMyEmail') }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </transition>

    <!-- Modal for User Description update -->
    <transition name="modal-fade">
        <div @click.self="closeUserDescriptionModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            v-if="isModalUserDescriptionOpen">
            <div class="bg-white rounded-lg relative w-[450px]">
                <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
                    <button @click="closeUserDescriptionModal" type="button"
                        class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                        <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                    </button>
                </div>
                <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
                    <div class="ml-8 flex items-center space-x-1">
                        <p class="block font-semibold leading-6 text-gray-900">{{
                            $t('settingsPage.accountPage.updateMyDescription')
                            }}</p>
                    </div>
                </div>
                <div class="flex flex-col gap-4 px-8 py-6">
                    <div>
                        <div class="flex space-x-1 items-center">
                            <envelope-icon class="w-4 h-4" />
                            <label class="block text-sm font-medium leading-6 text-gray-900">{{ emailSelected }}</label>
                        </div>
                        <div class="relative items-stretch mt-2 pb-6">
                            <input v-model="userDescription" type="text"
                                placeholder="Résumez-vous pour aider l'assistant"
                                class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6">
                        </div>
                    </div>
                    <div class="mt-2 sm:mt-2 sm:flex sm:flex-row">
                        <button type="button"
                            class="ml-auto rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                            @click="updateUserDescription">{{ $t('constants.userActions.update') }}</button>
                    </div>
                </div>
            </div>
        </div>
    </transition>


    <!-- Modal for User Description add -->
    <transition name="modal-fade">
        <div @click.self="closeAddUserDescriptionModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            v-if="isModalAddUserDescriptionOpen">
            <div class="bg-white rounded-lg relative w-[450px]">
                <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
                    <button @click="closeAddUserDescriptionModal" type="button"
                        class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                        <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                    </button>
                </div>
                <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
                    <div class="ml-8 flex items-center space-x-1">
                        <p class="block font-semibold leading-6 text-gray-900">{{
                            $t('settingsPage.accountPage.linkANewEmailAddress')
                            }}</p>
                    </div>
                </div>
                <div class="flex flex-col gap-4 px-8 py-6">
                    <div>
                        <div class="flex space-x-1 items-center">
                            <envelope-icon class="w-4 h-4" />
                            <label class="block text-sm font-medium leading-6 text-gray-900">{{
                            $t('settingsPage.accountPage.optionalDescription')
                            }}</label>
                        </div>
                        <div class="relative items-stretch mt-2 pb-6">
                            <input v-model="userDescription" type="text"
                               :placeholder="$t('signUpPart1Page.summaryUserPlaceholder')" 
                                class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6">
                        </div>
                    </div>
                    <div class="mt-2 sm:mt-2 sm:flex sm:flex-row">
                        <button type="button"
                            class="ml-auto rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                            @click="linkNewEmail">{{ $t('settingsPage.accountPage.link') }}</button>
                    </div>
                </div>
            </div>
        </div>
    </transition>

    <div class="flex flex-col justify-center items-center h-screen ">
        <div class="flex h-full w-full">
            <div class="w-[90px] 2xl:w-[100px] bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <navbar></navbar>
            </div>
            <div class="flex-1 bg-white ring-1 ring-black ring-opacity-5">
                <div class="flex flex-col h-full">
                    <main class="bg-gray-50 ring-1 ring-black ring-opacity-5">
                        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                            <div class="flex items-center">
                                <div class="w-full flex items-center justify-center py-6 2xl:py-7">
                                    <div class="sm:hidden">
                                        <!-- <label for="tabs" class="sr-only">Select a tab</label>
                                        <-- Use an "onChange" listener to redirect the user to the selected tab URL. ->
                                        <select id="tabs" name="tabs"
                                            class="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500">
                                            <option>Ecole ESAIP</option>
                                            <option>Entrepreneuriat</option>
                                            <option selected>Administratif</option>
                                            <option>Autres</option>
                                        </select> -->
                                    </div>
                                    <div class="hidden sm:block w-full">
                                        <nav class="flex justify-center space-x-4 w-full" aria-label="Tabs">
                                            <!-- Current: "bg-gray-200 text-gray-800", Default: "text-gray-600 hover:text-gray-800" -->
                                            <div class="text-sm font-medium cursor-pointer"
                                                :class="['flex space-x-2 items-center rounded-md py-2', { 'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'account', 'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'account' }]"
                                                @click="setActiveSection('account')">
                                                <user-icon class="w-4 h-4" />
                                                <a :class="{ 'text-gray-800': activeSection === 'account', 'text-gray-600': activeSection !== 'account' }"
                                                    class="text-sm font-medium">{{ $t('settingsPage.accountPage.myAccountTitle')
                                                    }}</a>
                                            </div>
                                            <div class="text-sm font-medium cursor-pointer"
                                                :class="['flex space-x-2 items-center rounded-md py-2', { 'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'preferences', 'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'preferences' }]"
                                                @click="setActiveSection('preferences')">
                                                <adjustments-vertical-icon class="w-4 h-4" />
                                                <a
                                                    :class="{ 'text-gray-800': activeSection === 'preferences', 'text-gray-600': activeSection !== 'preferences' }">{{
                                                        $t('settingsPage.preferencesPage.preferencesTitle') }}</a>
                                            </div>
                                            <div class="text-sm font-medium cursor-pointer"
                                                :class="['flex space-x-2 items-center rounded-md py-2', { 'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'subscription', 'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'subscription' }]"
                                                @click="setActiveSection('subscription')">
                                                <credit-card-icon class="w-4 h-4" />
                                                <a :class="{ 'text-gray-800': activeSection === 'subscription', 'text-gray-600': activeSection !== 'subscription' }"
                                                    class="text-sm font-medium">{{
                                                        $t('settingsPage.subscriptionPage.subscriptionTitle')
                                                    }}</a>
                                            </div>

                                            <div class="text-sm font-medium cursor-pointer"
                                                :class="['flex space-x-2 items-center rounded-md py-2', { 'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12': activeSection === 'data', 'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8': activeSection !== 'data' }]"
                                                @click="setActiveSection('data')">
                                                <circle-stack-icon class="w-4 h-4" />
                                                <a :class="{ 'text-gray-800': activeSection === 'data', 'text-gray-600': activeSection !== 'data' }"
                                                    class="text-sm font-medium">{{ $t('settingsPage.dataPage.myData')
                                                    }}</a>
                                            </div>
                                        </nav>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </main>
                    <div v-if="activeSection === 'account'" class="flex-1 h-full">
                        <!-- TO DO : CENTER -->
                        <div class="h-full w-full flex items-center justify-center">
                            <!-- We've used 3xl here, but feel free to try other max-widths based on your needs -->
                            <div class="flex gap-x-10 h-full w-full py-10 px-8 2xl:py-14 2xl:px-12">
                                <div class="flex-1 flex-col h-full flex-grow px-4">
                                    <div class="flex-col w-full pt-6">
                                        <div class="relative w-full">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="w-full border-t border-gray-300"></div>
                                            </div>
                                            <div class="relative flex justify-center">
                                                <span class="bg-white px-2 text-sm text-gray-500">{{
                                                    $t('settingsPage.accountPage.changeMyUsernameOrMyPassword')
                                                    }}</span>
                                            </div>
                                        </div>
                                        <div class="pt-6 pb-10">
                                            <div class="flex space-x-1 items-center">
                                                <envelope-icon class="w-4 h-4" />
                                                <label class="block text-sm font-medium leading-6 text-gray-900">{{
                                                    $t('constants.username') }}</label>
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
                                                                class="block text-sm font-medium leading-6 text-gray-900">{{
                                                                    $t('settingsPage.accountPage.newPassword') }}</label>
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
                                                                        <path stroke-linecap="round"
                                                                            stroke-linejoin="round"
                                                                            d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                                                        <path stroke-linecap="round"
                                                                            stroke-linejoin="round"
                                                                            d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                                                    </svg>
                                                                    <svg v-else xmlns="http://www.w3.org/2000/svg"
                                                                        fill="none" viewBox="0 0 24 24"
                                                                        stroke-width="1.5" stroke="currentColor"
                                                                        class="w-6 h-6">
                                                                        <path stroke-linecap="round"
                                                                            stroke-linejoin="round"
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
                                                                class="block text-sm font-medium leading-6 text-gray-900">{{
                                                                    $t('settingsPage.accountPage.confirmYourNewPassword') }}</label>
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
                                            </div>
                                            <div class="flex justify-end pt-4">
                                                <button @click="handleSubmit"
                                                    class="rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600">{{
                                                        $t('constants.userActions.modify') }}</button>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="flex-col flex-grow w-full py-12 2xl:py-20">
                                        <div class="relative">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="w-full border-t border-gray-300"></div>
                                            </div>
                                            <div class="relative flex justify-center">
                                                <span class="bg-white px-2 text-sm text-gray-500">{{
                                                    $t('constants.userActions.delete') }}</span>
                                            </div>
                                        </div>
                                        <div class="pt-6">
                                            <div class="flex space-x-1 items-center justify-between">
                                                <div class="flex items-center gap-2">
                                                    <input type="radio"
                                                        class="form-radio text-red-600 border-red-400 focus:border-red-500 focus:ring-red-200 h-5 w-5"
                                                        name="choice">
                                                    <label for="push-everything"
                                                        class="block text-sm font-medium leading-6">
                                                        {{ $t('settingsPage.accountPage.confirmDeleteAccount') }}</label>
                                                </div>
                                                <button @click="openModal" type="submit"
                                                    class="inline-flex w-full justify-cente items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto">
                                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                        viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                                        class="w-6 h-6">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                                    </svg>

                                                    {{ $t('constants.userActions.delete') }}</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex-1 flex-col h-full flex-grow px-4 py-6">
                                    <div class="relative">
                                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                            <div class="w-full border-t border-gray-300"></div>
                                        </div>
                                        <div class="relative flex justify-center">
                                            <span class="bg-white px-2 text-sm text-gray-500">{{
                                                $t('settingsPage.accountPage.linkANewEmailAddress') }}</span>
                                        </div>
                                    </div>
                                    <div class="pt-[52px]">
                                        <div class="overflow-y-auto w-full"><!--max-h-[120px]-->
                                            <div class="max-h-20 sm:max-h-24 md:max-h-32 lg:max-h-40 w-full">
                                                <ul role="list" class="space-y-1 w-full">
                                                    <li v-for="email in emailsLinked" :key="email.email"
                                                        class="border border-black w-full overflow-hidden font-semibold rounded-md bg-gray-10 px-6 py-0 shadow hover:shadow-md text-gray-700 relative">
                                                        <div class="flex items-center justify-center w-full">
                                                            <svg v-if="email.type_api === 'microsoft'"
                                                                xmlns="http://www.w3.org/2000/svg" width="21"
                                                                height="21" viewBox="0 0 21 21">
                                                                <rect x="1" y="1" width="9" height="9" fill="#f25022" />
                                                                <rect x="1" y="11" width="9" height="9"
                                                                    fill="#00a4ef" />
                                                                <rect x="11" y="1" width="9" height="9"
                                                                    fill="#7fba00" />
                                                                <rect x="11" y="11" width="9" height="9"
                                                                    fill="#ffb900" />
                                                            </svg>
                                                            <svg v-if="email.type_api === 'google'"
                                                                class="-ml-0.5 h-5 w-5" aria-hidden="true"
                                                                viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"
                                                                fill="currentColor">
                                                                <path
                                                                    d="M23.4392061,12.2245191 C23.4392061,11.2412519 23.3594198,10.5237252 23.1867481,9.77963359 L11.9587786,9.77963359 L11.9587786,14.2176183 L18.5493435,14.2176183 C18.4165191,15.3205191 17.6989924,16.9814656 16.104458,18.0975573 L16.0821069,18.2461374 L19.6321832,20.9963359 L19.8781374,21.0208855 C22.1369771,18.9347176 23.4392061,15.8652824 23.4392061,12.2245191"
                                                                    id="Shape" fill="#4285F4"></path>
                                                                <path
                                                                    d="M11.9587786,23.9175573 C15.1876031,23.9175573 17.898229,22.8545038 19.8781374,21.0208855 L16.104458,18.0975573 C15.094626,18.8018015 13.7392672,19.2934351 11.9587786,19.2934351 C8.79636641,19.2934351 6.11230534,17.2073588 5.15551145,14.3239695 L5.01526718,14.3358779 L1.32384733,17.1927023 L1.27557252,17.3269008 C3.24210687,21.2334046 7.28152672,23.9175573 11.9587786,23.9175573"
                                                                    id="Shape" fill="#34A853"></path>
                                                                <path
                                                                    d="M5.15551145,14.3239695 C4.90305344,13.5798779 4.75694656,12.7825649 4.75694656,11.9587786 C4.75694656,11.1349008 4.90305344,10.3376794 5.14222901,9.59358779 L5.13554198,9.4351145 L1.3978626,6.53239695 L1.27557252,6.59056489 C0.465068702,8.21166412 0,10.0320916 0,11.9587786 C0,13.8854656 0.465068702,15.7058015 1.27557252,17.3269008 L5.15551145,14.3239695"
                                                                    id="Shape" fill="#FBBC05"></path>
                                                                <path
                                                                    d="M11.9587786,4.62403053 C14.2043359,4.62403053 15.719084,5.59401527 16.5828092,6.40461069 L19.9578321,3.10928244 C17.8850382,1.18259542 15.1876031,0 11.9587786,0 C7.28152672,0 3.24210687,2.68406107 1.27557252,6.59056489 L5.14222901,9.59358779 C6.11230534,6.71019847 8.79636641,4.62403053 11.9587786,4.62403053"
                                                                    id="Shape" fill="#EB4335"></path>
                                                            </svg>
                                                            <div class="flex-grow"></div>
                                                            <span>{{ email.email }}</span>
                                                            <div class="flex-grow"></div>
                                                            <div>
                                                                <button type="button"
                                                                    class="inline-flex justify-center items-center rounded-md px-3 py-2 text-sm font-semibold text-gray-800 hover:text-black"
                                                                    @click.stop="openUserDescriptionModal(email.email)">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                                        viewBox="0 0 24 24" stroke-width="1.5"
                                                                        stroke="currentColor" class="w-6 h-6">
                                                                        <path stroke-linecap="round"
                                                                            stroke-linejoin="round"
                                                                            d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                                                                    </svg>
                                                                </button>
                                                                <button type="button"
                                                                    class="inline-flex justify-center items-center rounded-md px-3 py-2 text-sm font-semibold text-red-600 hover:text-red-700 hover:bg-transparent"
                                                                    @click="openUnLinkModal(email.email)">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                                        viewBox="0 0 24 24" stroke-width="1.5"
                                                                        stroke="currentColor" class="w-6 h-6">
                                                                        <path stroke-linecap="round"
                                                                            stroke-linejoin="round"
                                                                            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                                                    </svg>
                                                                </button>
                                                            </div>
                                                        </div>
                                                    </li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="relative py-4">
                                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                            <div class="w-full border-t border-gray-300"></div>
                                        </div>
                                        <div class="relative flex justify-center">
                                            <span class="bg-white px-2 text-sm text-gray-500">
                                                {{$t('settingsPage.accountPage.chooseTheEmailServiceProvider') }}
                                            </span>
                                        </div>
                                    </div>
                                    <div class="flex gap-x-4 justify-center">
                                        <div class="pt-4">
                                            <div class="relative items-stretch mt-2 flex justify-center items-center">
                                                <button type="button"
                                                    class="relative group inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                                    @click="authorize_microsoft">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21"
                                                        viewBox="0 0 21 21">
                                                        <rect x="1" y="1" width="9" height="9" fill="#f25022" />
                                                        <rect x="1" y="11" width="9" height="9" fill="#00a4ef" />
                                                        <rect x="11" y="1" width="9" height="9" fill="#7fba00" />
                                                        <rect x="11" y="11" width="9" height="9" fill="#ffb900" />
                                                    </svg>
                                                    <span
                                                        class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden w-max px-2 py-1 text-xs text-white bg-black rounded-md group-hover:block">
                                                        {{ $t('settingsPage.accountPage.securelyLinkOutlookAccount') }}</span>
                                                </button>
                                            </div>
                                        </div>
                                        <div class="py-4">
                                            <div class="relative items-stretch mt-2 flex justify-center items-center">
                                                <button type="button"
                                                    class="relative group inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                                    @click="authorize_google">
                                                    <svg class="-ml-0.5 h-5 w-5" aria-hidden="true" viewBox="0 0 24 24"
                                                        xmlns="http://www.w3.org/2000/svg" fill="currentColor">
                                                        <path
                                                            d="M23.4392061,12.2245191 C23.4392061,11.2412519 23.3594198,10.5237252 23.1867481,9.77963359 L11.9587786,9.77963359 L11.9587786,14.2176183 L18.5493435,14.2176183 C18.4165191,15.3205191 17.6989924,16.9814656 16.104458,18.0975573 L16.0821069,18.2461374 L19.6321832,20.9963359 L19.8781374,21.0208855 C22.1369771,18.9347176 23.4392061,15.8652824 23.4392061,12.2245191"
                                                            id="Shape" fill="#4285F4"></path>
                                                        <path
                                                            d="M11.9587786,23.9175573 C15.1876031,23.9175573 17.898229,22.8545038 19.8781374,21.0208855 L16.104458,18.0975573 C15.094626,18.8018015 13.7392672,19.2934351 11.9587786,19.2934351 C8.79636641,19.2934351 6.11230534,17.2073588 5.15551145,14.3239695 L5.01526718,14.3358779 L1.32384733,17.1927023 L1.27557252,17.3269008 C3.24210687,21.2334046 7.28152672,23.9175573 11.9587786,23.9175573"
                                                            id="Shape" fill="#34A853"></path>
                                                        <path
                                                            d="M5.15551145,14.3239695 C4.90305344,13.5798779 4.75694656,12.7825649 4.75694656,11.9587786 C4.75694656,11.1349008 4.90305344,10.3376794 5.14222901,9.59358779 L5.13554198,9.4351145 L1.3978626,6.53239695 L1.27557252,6.59056489 C0.465068702,8.21166412 0,10.0320916 0,11.9587786 C0,13.8854656 0.465068702,15.7058015 1.27557252,17.3269008 L5.15551145,14.3239695"
                                                            id="Shape" fill="#FBBC05"></path>
                                                        <path
                                                            d="M11.9587786,4.62403053 C14.2043359,4.62403053 15.719084,5.59401527 16.5828092,6.40461069 L19.9578321,3.10928244 C17.8850382,1.18259542 15.1876031,0 11.9587786,0 C7.28152672,0 3.24210687,2.68406107 1.27557252,6.59056489 L5.14222901,9.59358779 C6.11230534,6.71019847 8.79636641,4.62403053 11.9587786,4.62403053"
                                                            id="Shape" fill="#EB4335"></path>
                                                    </svg>
                                                    <span
                                                        class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden w-max px-2 py-1 text-xs text-white bg-black rounded-md group-hover:block">
                                                        {{ $t('settingsPage.accountPage.securelyLinkGmailAccount') }}</span>
                                                </button>
                                            </div>
                                        </div>

                                        <!-- UNDER DEVELOPMENT -->
                                        <div class="py-4">
                                            <div class="relative items-stretch mt-2 flex justify-center items-center">
                                                <button type="button"
                                                    class="relative group inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                                    @click="authorize_apple">
                                                    <svg class="css-10aieaf eu4oa1w0" width="16pt" height="16pt"
                                                        viewBox="0 0 16 16" version="1.1">
                                                        <path
                                                            style="stroke: none; fill-rule: nonzero; fill: rgb(0, 0, 0); fill-opacity: 1;"
                                                            d="M 14.152344 12.257812 C 13.921875 12.792969 13.648438 13.28125 13.332031 13.734375 C 12.902344 14.347656 12.546875 14.773438 12.277344 15.007812 C 11.855469 15.398438 11.402344 15.59375 10.917969 15.605469 C 10.570312 15.605469 10.152344 15.507812 9.664062 15.308594 C 9.175781 15.109375 8.726562 15.007812 8.316406 15.007812 C 7.886719 15.007812 7.421875 15.109375 6.929688 15.308594 C 6.433594 15.507812 6.035156 15.613281 5.730469 15.621094 C 5.265625 15.640625 4.804688 15.4375 4.339844 15.007812 C 4.046875 14.753906 3.679688 14.3125 3.238281 13.6875 C 2.761719 13.019531 2.375 12.25 2.070312 11.367188 C 1.742188 10.414062 1.578125 9.496094 1.578125 8.601562 C 1.578125 7.582031 1.800781 6.699219 2.242188 5.960938 C 2.589844 5.367188 3.050781 4.898438 3.628906 4.554688 C 4.207031 4.210938 4.835938 4.039062 5.507812 4.027344 C 5.875 4.027344 6.359375 4.140625 6.960938 4.363281 C 7.558594 4.589844 7.941406 4.703125 8.113281 4.703125 C 8.238281 4.703125 8.664062 4.570312 9.390625 4.304688 C 10.074219 4.058594 10.652344 3.957031 11.125 3.996094 C 12.40625 4.097656 13.371094 4.605469 14.011719 5.515625 C 12.863281 6.210938 12.296875 7.183594 12.308594 8.433594 C 12.320312 9.40625 12.671875 10.214844 13.367188 10.859375 C 13.679688 11.15625 14.03125 11.386719 14.421875 11.550781 C 14.335938 11.796875 14.246094 12.03125 14.152344 12.257812 Z M 11.210938 0.679688 C 11.210938 1.445312 10.933594 2.15625 10.375 2.816406 C 9.707031 3.597656 8.894531 4.050781 8.015625 3.980469 C 8.003906 3.886719 8 3.792969 8 3.691406 C 8 2.957031 8.316406 2.175781 8.882812 1.535156 C 9.167969 1.210938 9.527344 0.941406 9.960938 0.726562 C 10.394531 0.511719 10.808594 0.394531 11.195312 0.375 C 11.207031 0.476562 11.210938 0.582031 11.210938 0.679688 Z M 11.210938 0.679688 ">
                                                        </path>
                                                    </svg>
                                                    <span
                                                        class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden w-max px-2 py-1 text-xs text-white bg-black rounded-md group-hover:block"> {{ $t('constants.underDevelopment') }}</span>
                                                </button>
                                            </div>
                                        </div>
                                        
                                        <!-- UNDER DEVELOPMENT -->
                                        <div class="py-4">
                                            <div class="relative items-stretch mt-2 flex justify-center items-center">
                                                <button type="button"
                                                    class="relative group inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                                    @click="authorize_yahoo">
                                                    <svg xmlns="http://www.w3.org/2000/svg" aria-label="Yahoo!"
                                                        role="img" viewBox="0 0 512 512" fill="#ffffff" width="16pt"
                                                        height="16pt">
                                                        <rect width="512" height="512" rx="15%" fill="#5f01d1" />
                                                        <g fill="#ffffff">
                                                            <path
                                                                d="M203 404h-62l25-59-69-165h63l37 95 37-95h62m58 76h-69l62-148h69" />
                                                            <circle cx="303" cy="308" r="38" />
                                                        </g>
                                                    </svg>
                                                    <span
                                                        class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden w-max px-2 py-1 text-xs text-white bg-black rounded-md group-hover:block">{{ $t('constants.underDevelopment') }}</span>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-if="activeSection === 'subscription'" class="flex-1 section mx-8 my-8 2xl:mx-12 2xl:my-12">
                        <subscription @openBillingModal="openBillingModal"></subscription>
                    </div>
                    <div v-if="activeSection === 'data'" class="flex flex-col h-full section">
                        <!--
                        <div class="flex">
                            <div class="flex-1">
                                <div class="flex px-6 py-6">
                                    <h1 class="text-2xl" style="font-family: 'Poppins', sans-serif; font-weight: 500;">
                                        {{ $t('settings_navigation.my_data') }}</h1>
                                </div>
                                <div class="float-right mt-[-70px] mr-[10px]">
                                    <circle-stack-icon class="w-6 h-6 text-gray-500" />
                                </div>
                            </div>
                        </div>-->
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
                                    <span class="mt-2 block text-sm font-semibold text-gray-900">
                                        {{ $t('constants.underDevelopment') }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-if="activeSection === 'preferences'" class="flex-1 section">
                        <!-- TO DO : CENTER -->
                        <div class="mx-auto w-full h-full px-8 2xl:px-12 pt-10">
                            <!-- Content goes here -->
                            <div class="flex flex-col h-full pb-6">
                                <div class="flex gap-x-10 w-full">
                                    <div class="flex-1 flex flex-col">
                                        <div class="relative">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="w-full border-t border-gray-300"></div>
                                            </div>
                                            <div class="relative flex justify-center">
                                                <span class="bg-white px-2 text-sm text-gray-500">{{
                                                    $t('constants.language') }}</span>
                                            </div>
                                        </div>
                                        <div class="pt-10 pb-10">
                                            <LanguageChange></LanguageChange>
                                        </div>
                                    </div>
                                    <div class="flex-1 flex flex-col">
                                        <div class="relative">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="w-full border-t border-gray-300"></div>
                                            </div>
                                            <div class="relative flex justify-center">
                                                <span class="bg-white px-2 text-sm text-gray-500">{{
                                                    $t('constants.theme') }}</span>
                                            </div>
                                        </div>
                                        <div class="pt-10 pb-10">
                                            <div class="relative items-stretch dark:bg-gray-800">
                                                <theme></theme>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex gap-x-10 w-full">
                                    <div class="flex-1 flex flex-col">
                                        <div class="relative">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="w-full border-t border-gray-300"></div>
                                            </div>
                                            <div class="relative flex justify-center">
                                                <span
                                                    class="bg-white px-2 text-sm text-gray-500">{{
                                                    $t('constants.timezone') }}</span>
                                            </div>
                                        </div>
                                        <div class="pt-10 pb-10">
                                            <SettingsTimeZone></SettingsTimeZone>
                                        </div>
                                    </div>
                                </div>
                                <div
                                    class="flex-1 w-full h-full rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 text-center">
                                    <div class="flex flex-col h-full items-center justify-center">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                            stroke-width="1" stroke="currentColor"
                                            class="w-12 h-12 mx-auto text-gray-400">
                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                d="M11.42 15.17 17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 0 0 4.486-6.336l-3.276 3.277a3.004 3.004 0 0 1-2.25-2.25l3.276-3.276a4.5 4.5 0 0 0-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437 1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008Z" />
                                        </svg>
                                        <span class="mt-2 block text-sm font-semibold text-gray-900">
                                            {{ $t('constants.underDevelopment') }}
                                        </span>
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
import { useRouter } from 'vue-router';

//import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/vue'
//import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'

// TODO: REMOVE OR COMMENT EVERYTHING RELATED WITH BACKGROUND COLOR


// Variables to display a notification
let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
let timerId = ref(null);
let activeSection = ref('account'); // Default active section
let bgColor = ref(localStorage.getItem('bgColor') || '');
let userData = ref('');
let userEmailDescription = ref('');
let emailsLinked = ref('');
let newPassword = ref('');
let confirmPassword = ref('');
let isModalOpen = ref(false);
let isModalUserDescriptionOpen = ref(false);
let isUnlinkModalOpen = ref(false);
let isModalAddUserDescriptionOpen = ref(false);
let emailSelected = ref('');
let userDescription = ref('');
const router = useRouter();
const intervalId = setInterval(checkAuthorizationCode, 1000);

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
    fetchEmailLinked();
    fetchUserData();
    // TODO: fetch ONLY if the var bgColor is empty
    // Vérifier si bgColor est vide, et si c'est le cas, récupérer la couleur de fond
    if (!bgColor.value) {
        getBackgroundColor();
    }
})


async function openUnLinkModal(email) {
    emailSelected.value = email;
    isUnlinkModalOpen.value = true;

    if (emailsLinked.value.length == 1) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('settingsPage.accountPage.unableToDeletePrimaryEmail');
        notificationMessage.value = t('settingsPage.accountPage.deleteAccountInstruction');
        displayPopup();
        closeUnlinkModal();
        return;
    }
}

async function unLinkAccount() {
    const requestOptions = {
        headers: {
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({
            email: emailSelected.value
        })
    };

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/social_api/unlink/`, requestOptions);

        if ("error" in response) {
            // Show the pop-up
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle.value = t('settingsPage.accountPage.errorUnlinkingEmailAddress');
            notificationMessage.value = response.error;
            displayPopup();
        } else if (response.message == "Email unlinked successfully!") {
            fetchEmailLinked();
            // Show the pop-up
            backgroundColor = 'bg-green-200/[.89] border border-green-400';
            notificationTitle.value = t('constants.popUpConstants.successMessages.success');
            notificationMessage.value = t('settingsPage.accountPage.emailUnlinkedSuccess');
            displayPopup();
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('settingsPage.accountPage.errorUnlinkingEmailAddress');
        notificationMessage.value = error.message;
        displayPopup();
    }
    closeUnlinkModal();
}
function linkNewEmail() {
    const type_api = sessionStorage.getItem("type_api");

    if (type_api == "google") {
        caches.keys().then((keyList) => Promise.all(keyList.map((key) => caches.delete(key))))
        window.location.replace(`${API_BASE_URL}google/auth_url_link_email/`);
    } else if (type_api == "microsoft") {
        window.location.replace(`${API_BASE_URL}microsoft/auth_url_link_email/`);
    }
}
function authorize_google() {
    saveVariables("google");
    isModalAddUserDescriptionOpen.value = true;
}
function authorize_microsoft() {
    saveVariables("microsoft");
    isModalAddUserDescriptionOpen.value = true;
}
function saveVariables(type_api) {
    sessionStorage.setItem("type_api", type_api);
    sessionStorage.setItem("userDescription", userEmailDescription.value);
}
function checkAuthorizationCode() {
    const urlParams = new URLSearchParams(window.location.search);
    const authorizationCode = urlParams.get('code');

    if (authorizationCode) {
        clearInterval(intervalId);
        linkEmail(authorizationCode);
    }
}
async function linkEmail(authorizationCode) {
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            code: authorizationCode,
            type_api: sessionStorage.getItem("type_api"),
            user_description: sessionStorage.getItem("userDescription")
        })
    };
    const response = await fetchWithToken(`${API_BASE_URL}user/social_api/link/`, requestOptions);

    if (response.message == "Email linked to account successfully!") {
        fetchEmailLinked();
        // Show the pop-up
        backgroundColor.value = 'bg-green-200/[.89] border border-green-400';
        notificationTitle.value = t('constants.popUpConstants.successMessages.success');
        notificationMessage.value = t('settingsPage.accountPage.emailLinkedSuccess');
        displayPopup();
    } else {
        // Show the pop-up
        backgroundColor.value = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('settingsPage.accountPage.emailLinkingFailure');
        notificationMessage.value = response.error;
        displayPopup();
    }
    sessionStorage.clear();
    // Remove '?code' and '?state' from url
    var currentUrl = window.location.href;
    var modifiedUrl = currentUrl.replace(/(\?)code=.*(&|$)/, '?').replace(/(\?)state=.*(&|$)/, '?');
    window.history.replaceState({}, document.title, modifiedUrl);
}

async function fetchEmailLinked() {
    const requestOptions = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails_linked/`, requestOptions);

        if ("error" in response) {
            // Show the pop-up
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle = t('constants.popUpConstants.primaryEmailFetchError');
            notificationMessage = response.error;
            displayPopup();
        } else {
            emailsLinked.value = response;
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('constants.popUpConstants.primaryEmailFetchError');
        notificationMessage = error.message;
        displayPopup();
    }
}
function openModal() {
    const isChecked = document.querySelector('input[name="choice"]:checked');

    if (isChecked) {
        isModalOpen.value = true;
    } else {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('settingsPage.accountPage.confirmationRequired');
        notificationMessage = t('settingsPage.accountPage.checkBoxApprovalDeletion');
        displayPopup();
    }
}
function closeAddUserDescriptionModal() {
    isModalAddUserDescriptionOpen.value = false;
}
function closeUnlinkModal() {
    isUnlinkModalOpen.value = false;
}
function closeUserDescriptionModal() {
    isModalUserDescriptionOpen.value = false;
}
async function openUserDescriptionModal(email) {
    emailSelected.value = email;

    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "email": email
        })
    };

    const response = await fetchWithToken(`${API_BASE_URL}user/social_api/get_user_description/`, requestOptions);

    if (response.data || !response.data.trim()) {
        isModalUserDescriptionOpen.value = true;
        userDescription.value = response.data;
    } else {
        backgroundColor.value = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('settingsPage.accountPage.errorUnlinkingEmailAddress');
        notificationMessage.value = response.error;
        displayPopup();
    }
}
async function updateUserDescription() {
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "email": emailSelected.value,
            "user_description": userDescription.value.trim() ? userDescription.value.trim() : ""
        })
    };

    const response = await fetchWithToken(`${API_BASE_URL}user/social_api/update_user_description/`, requestOptions)

    if (response.message == "User description updated") {
        backgroundColor = 'bg-green-200/[.89] border border-green-400';
        notificationTitle.value = t('constants.popUpConstants.successMessages.success');
        notificationMessage.value = t('settingsPage.accountPage.emailDescriptionUpdated');
        displayPopup();
    } else {
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = t('settingsPage.accountPage.errorUpdatingDescription');
        notificationMessage.value = response.error;
        displayPopup();
    }
    closeUserDescriptionModal();
}

function closeModal() {
    isModalOpen.value = false;
    document.querySelector('input[name="choice"]').checked = false;
}
function dismissPopup() {
    showNotification.value = false;
    // Cancel the timer
    clearTimeout(timerId.value);
}
function displayPopup() {
    showNotification.value = true;

    timerId.value = setTimeout(() => {
        dismissPopup();
    }, 4000);
}

function handleKeyDown(event) {
    if (event.key === 'Tab' && !isModalOpen.value) {
        event.preventDefault();
        switchActiveSection();
    } else if (event.key === 'Escape') {
        if (isModalOpen.value) {
            closeModal();
        } else if (isModalUserDescriptionOpen.value) {
            closeUserDescriptionModal();
        } else if (isUnlinkModalOpen.value) {
            closeUnlinkModal();
        } else if (isModalAddUserDescriptionOpen.value) {
            closeAddUserDescriptionModal();
        }
    } else if (event.key === 'Enter') {
        if (isModalUserDescriptionOpen.value) {
            updateUserDescription();
        } else if (isModalAddUserDescriptionOpen.value) {
            linkNewEmail();
        }
    }
}

function switchActiveSection() {
    const nextSection = {
        'account': 'preferences',
        'preferences': 'subscription',
        'subscription': 'data',
        'data': 'account'
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
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('settingsPage.accountPage.errorRetrievingUsername');
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
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('settingsPage.accountPage.errorRetrievingUsername');
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
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('settingsPage.accountPage.usernameCheckError');
        notificationMessage = error;
        displayPopup();
        return;
    }


    let resultUpdateUsername;

    if (response.available == false) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('settingsPage.accountPage.usernameAlreadyExists');
        notificationMessage = t('settingsPage.accountPage.pleaseChooseDifferentUsername');
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
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle = t('settingsPage.accountPage.usernameCheckError');
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
            backgroundColor = 'bg-green-200/[.89] border border-green-400';
            notificationTitle = t('constants.popUpConstants.successMessages.success');
            notificationMessage = t('settingsPage.accountPage.credentialsUpdated');
            displayPopup();
        }
        else if (!resultUpdatePwd) {

            if (resultUpdateUsername == 'Username updated successfully') {
                // Show the pop-up
                backgroundColor = 'bg-green-200/[.89] border border-green-400';
                notificationTitle = t('constants.popUpConstants.successMessages.success');
                notificationMessage = t('settingsPage.accountPage.usernameUpdatedSuccess');
                displayPopup();
            }
            else {
                // Show the pop-up
                backgroundColor = 'bg-red-200/[.89] border border-red-400';
                notificationTitle = t('settingsPage.accountPage.errorUpdatingUsername');
                notificationMessage = resultUpdateUsername;
                displayPopup();
            }
        }
    }
    else if (resultUpdatePwd) {

        if (resultUpdatePwd == 'Password updated successfully') {
            // Show the pop-up
            backgroundColor = 'bg-green-200/[.89] border border-green-400';
            notificationTitle = t('constants.popUpConstants.successMessages.success');
            notificationMessage =  t('settingsPage.accountPage.passwordUpdatedSuccess');
            displayPopup();
        }
        else {
            // Show the pop-up
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle = t('settingsPage.accountPage.errorUpdatingPassword');
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
        const data = await fetchWithToken(`${API_BASE_URL}user/preferences/update_password/`, requestOptions);

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
        const data = await fetchWithToken(`${API_BASE_URL}user/preferences/update_username/`, requestOptions);

        return 'Username updated successfully';
    } catch (error) {
        return error;
    }
}
async function deleteAccount() {

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
            closeModal();
            // Show the pop-up
            backgroundColor = 'bg-green-200/[.89] border border-green-400';
            notificationTitle = t('settingsPage.accountPage.redirectionInProgress');
            notificationMessage = t('settingsPage.accountPage.accountDeletedSuccess');
            displayPopup();

            setTimeout(() => {
                // Redirect login page
                router.push({ name: 'login' })
            }, 4000);

        } else {
            // Show the pop-up
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle = t('settingsPage.accountPage.errorDeletingAccount');
            notificationMessage = responseData.error;
            displayPopup();
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('settingsPage.accountPage.errorDeletingAccount');
        notificationMessage = error;
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
import LanguageChange from '../components/LanguageChange';
import Color from '../components/SettingsColor.vue';
import { XMarkIcon } from '@heroicons/vue/24/outline'
import Subscription from '../components/SettingsSubscription.vue'
import {
    AdjustmentsVerticalIcon,
    UserIcon,
    EnvelopeIcon,
    KeyIcon,
    CreditCardIcon,
    CircleStackIcon
} from '@heroicons/vue/24/outline'
import SettingsTimeZone from '@/components/SettingsTimeZone.vue';


export default {
    components: {
        Navbar,
        Navbar2,
        Theme,
        Color,
        Subscription,
        XMarkIcon,
        AdjustmentsVerticalIcon,
        UserIcon,
        EnvelopeIcon,
        KeyIcon,
        CreditCardIcon,
        LanguageChange,
        SettingsTimeZone,
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