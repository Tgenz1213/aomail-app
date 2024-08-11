<template>
    <AddUserDescriptionModal :isOpen="isAddUserDescriptionModalOpen" @close-modal="closeAddUserDescriptionModal" />
    <div class="flex-1 h-full">
        <div class="h-full w-full flex items-center justify-center">
            <div class="flex gap-x-10 h-full w-full py-10 px-8 2xl:py-14 2xl:px-12">
                <div class="flex-1 flex-col h-full flex-grow px-4">
                    <div class="flex-col w-full pt-6">
                        <div class="relative w-full">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t border-gray-300"></div>
                            </div>
                            <div class="relative flex justify-center">
                                <span class="bg-white px-2 text-sm text-gray-500">
                                    {{ $t("settingsPage.accountPage.changeMyUsernameOrMyPassword") }}
                                </span>
                            </div>
                        </div>
                        <div class="pt-6 pb-10">
                            <div class="flex space-x-1 items-center">
                                <envelope-icon class="w-4 h-4" />
                                <label class="block text-sm font-medium leading-6 text-gray-900">
                                    {{ $t("constants.username") }}
                                </label>
                            </div>
                            <div class="relative items-stretch mt-2">
                                <input
                                    v-model="username"
                                    type="text"
                                    name="username"
                                    id="username"
                                    autocomplete="username"
                                    class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                />
                            </div>
                            <div class="pt-4">
                                <div class="grid grid-cols-2 gap-6">
                                    <div class="flex flex-col">
                                        <div class="flex space-x-1 items-center">
                                            <key-icon class="w-4 h-4" />
                                            <label class="block text-sm font-medium leading-6 text-gray-900">
                                                {{ $t("settingsPage.accountPage.newPassword") }}
                                            </label>
                                        </div>
                                        <div class="relative items-stretch mt-2 flex">
                                            <input
                                                v-if="!showPassword"
                                                type="password"
                                                class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                v-model="newPassword"
                                            />
                                            <input
                                                v-else
                                                type="text"
                                                class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                v-model="newPassword"
                                            />
                                            <div class="flex items-center">
                                                <button
                                                    @click="togglePasswordVisibility"
                                                    class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300"
                                                >
                                                    <svg
                                                        v-if="!showPassword"
                                                        xmlns="http://www.w3.org/2000/svg"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke-width="1.5"
                                                        stroke="currentColor"
                                                        class="w-6 h-6"
                                                    >
                                                        <path
                                                            stroke-linecap="round"
                                                            stroke-linejoin="round"
                                                            d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
                                                        />
                                                        <path
                                                            stroke-linecap="round"
                                                            stroke-linejoin="round"
                                                            d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                                                        />
                                                    </svg>
                                                    <svg
                                                        v-else
                                                        xmlns="http://www.w3.org/2000/svg"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke-width="1.5"
                                                        stroke="currentColor"
                                                        class="w-6 h-6"
                                                    >
                                                        <path
                                                            stroke-linecap="round"
                                                            stroke-linejoin="round"
                                                            d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
                                                        />
                                                    </svg>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="flex flex-col">
                                        <div class="flex space-x-1 items-center">
                                            <key-icon class="w-4 h-4" />
                                            <label class="block text-sm font-medium leading-6 text-gray-900">
                                                {{ $t("settingsPage.accountPage.confirmYourNewPassword") }}
                                            </label>
                                        </div>
                                        <div class="relative items-stretch mt-2 flex">
                                            <input
                                                v-if="!showConfirmPassword"
                                                type="password"
                                                class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                v-model="confirmPassword"
                                            />
                                            <input
                                                v-else
                                                type="text"
                                                class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                v-model="confirmPassword"
                                            />
                                            <button
                                                @click="toggleConfirmPasswordVisibility"
                                                class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300"
                                            >
                                                <svg
                                                    v-if="!showConfirmPassword"
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    fill="none"
                                                    viewBox="0 0 24 24"
                                                    stroke-width="1.5"
                                                    stroke="currentColor"
                                                    class="w-6 h-6"
                                                >
                                                    <path
                                                        stroke-linecap="round"
                                                        stroke-linejoin="round"
                                                        d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
                                                    />
                                                    <path
                                                        stroke-linecap="round"
                                                        stroke-linejoin="round"
                                                        d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                                                    />
                                                </svg>
                                                <svg
                                                    v-else
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    fill="none"
                                                    viewBox="0 0 24 24"
                                                    stroke-width="1.5"
                                                    stroke="currentColor"
                                                    class="w-6 h-6"
                                                >
                                                    <path
                                                        stroke-linecap="round"
                                                        stroke-linejoin="round"
                                                        d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
                                                    />
                                                </svg>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="flex justify-end pt-4">
                                <button
                                    @click="handleSubmit"
                                    class="rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
                                >
                                    {{ $t("constants.userActions.modify") }}
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="flex-col flex-grow w-full py-12 2xl:py-20">
                        <div class="relative">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t border-gray-300"></div>
                            </div>
                            <div class="relative flex justify-center">
                                <span class="bg-white px-2 text-sm text-gray-500">
                                    {{ $t("constants.userActions.delete") }}
                                </span>
                            </div>
                        </div>
                        <div class="pt-6">
                            <div class="flex space-x-1 items-center justify-between">
                                <div class="flex items-center gap-2">
                                    <input
                                        type="radio"
                                        class="form-radio text-red-600 border-red-400 focus:border-red-500 focus:ring-red-200 h-5 w-5"
                                        name="choice"
                                    />
                                    <label for="push-everything" class="block text-sm font-medium leading-6">
                                        {{ $t("settingsPage.accountPage.confirmDeleteAccount") }}
                                    </label>
                                </div>
                                <button
                                    @click="openAccountDeletionModal"
                                    type="submit"
                                    class="inline-flex w-full justify-cente items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke-width="1.5"
                                        stroke="currentColor"
                                        class="w-6 h-6"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                                        />
                                    </svg>

                                    {{ $t("constants.userActions.delete") }}
                                </button>
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
                            <span class="bg-white px-2 text-sm text-gray-500">
                                {{ $t("settingsPage.accountPage.linkANewEmailAddress") }}
                            </span>
                        </div>
                    </div>
                    <div class="pt-[52px]">
                        <div class="overflow-y-auto w-full">
                            <div class="max-h-20 sm:max-h-24 md:max-h-32 lg:max-h-40 w-full">
                                <ul role="list" class="space-y-1 w-full">
                                    <li
                                        v-for="email in emailsLinked"
                                        :key="email.email"
                                        class="border border-black w-full overflow-hidden font-semibold rounded-md bg-gray-10 px-6 py-0 shadow hover:shadow-md text-gray-700 relative"
                                    >
                                        <div class="flex items-center justify-center w-full">
                                            <svg
                                                v-if="email.typeApi === 'microsoft'"
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="21"
                                                height="21"
                                                viewBox="0 0 21 21"
                                            >
                                                <rect x="1" y="1" width="9" height="9" fill="#f25022" />
                                                <rect x="1" y="11" width="9" height="9" fill="#00a4ef" />
                                                <rect x="11" y="1" width="9" height="9" fill="#7fba00" />
                                                <rect x="11" y="11" width="9" height="9" fill="#ffb900" />
                                            </svg>
                                            <svg
                                                v-if="email.typeApi === 'google'"
                                                class="-ml-0.5 h-5 w-5"
                                                aria-hidden="true"
                                                viewBox="0 0 24 24"
                                                xmlns="http://www.w3.org/2000/svg"
                                                fill="currentColor"
                                            >
                                                <path
                                                    d="M23.4392061,12.2245191 C23.4392061,11.2412519 23.3594198,10.5237252 23.1867481,9.77963359 L11.9587786,9.77963359 L11.9587786,14.2176183 L18.5493435,14.2176183 C18.4165191,15.3205191 17.6989924,16.9814656 16.104458,18.0975573 L16.0821069,18.2461374 L19.6321832,20.9963359 L19.8781374,21.0208855 C22.1369771,18.9347176 23.4392061,15.8652824 23.4392061,12.2245191"
                                                    id="Shape"
                                                    fill="#4285F4"
                                                ></path>
                                                <path
                                                    d="M11.9587786,23.9175573 C15.1876031,23.9175573 17.898229,22.8545038 19.8781374,21.0208855 L16.104458,18.0975573 C15.094626,18.8018015 13.7392672,19.2934351 11.9587786,19.2934351 C8.79636641,19.2934351 6.11230534,17.2073588 5.15551145,14.3239695 L5.01526718,14.3358779 L1.32384733,17.1927023 L1.27557252,17.3269008 C3.24210687,21.2334046 7.28152672,23.9175573 11.9587786,23.9175573"
                                                    id="Shape"
                                                    fill="#34A853"
                                                ></path>
                                                <path
                                                    d="M5.15551145,14.3239695 C4.90305344,13.5798779 4.75694656,12.7825649 4.75694656,11.9587786 C4.75694656,11.1349008 4.90305344,10.3376794 5.14222901,9.59358779 L5.13554198,9.4351145 L1.3978626,6.53239695 L1.27557252,6.59056489 C0.465068702,8.21166412 0,10.0320916 0,11.9587786 C0,13.8854656 0.465068702,15.7058015 1.27557252,17.3269008 L5.15551145,14.3239695"
                                                    id="Shape"
                                                    fill="#FBBC05"
                                                ></path>
                                                <path
                                                    d="M11.9587786,4.62403053 C14.2043359,4.62403053 15.719084,5.59401527 16.5828092,6.40461069 L19.9578321,3.10928244 C17.8850382,1.18259542 15.1876031,0 11.9587786,0 C7.28152672,0 3.24210687,2.68406107 1.27557252,6.59056489 L5.14222901,9.59358779 C6.11230534,6.71019847 8.79636641,4.62403053 11.9587786,4.62403053"
                                                    id="Shape"
                                                    fill="#EB4335"
                                                ></path>
                                            </svg>
                                            <div class="flex-grow"></div>
                                            <span>{{ email.email }}</span>
                                            <div class="flex-grow"></div>
                                            <div>
                                                <button
                                                    type="button"
                                                    class="inline-flex justify-center items-center rounded-md px-3 py-2 text-sm font-semibold text-gray-800 hover:text-black"
                                                    @click.stop="openUserDescriptionModal(email.email)"
                                                >
                                                    <svg
                                                        xmlns="http://www.w3.org/2000/svg"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke-width="1.5"
                                                        stroke="currentColor"
                                                        class="w-6 h-6"
                                                    >
                                                        <path
                                                            stroke-linecap="round"
                                                            stroke-linejoin="round"
                                                            d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
                                                        />
                                                    </svg>
                                                </button>
                                                <button
                                                    type="button"
                                                    class="inline-flex justify-center items-center rounded-md px-3 py-2 text-sm font-semibold text-red-600 hover:text-red-700 hover:bg-transparent"
                                                    @click="openUnLinkModal(email.email)"
                                                >
                                                    <svg
                                                        xmlns="http://www.w3.org/2000/svg"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke-width="1.5"
                                                        stroke="currentColor"
                                                        class="w-6 h-6"
                                                    >
                                                        <path
                                                            stroke-linecap="round"
                                                            stroke-linejoin="round"
                                                            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                                                        />
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
                                {{ $t("settingsPage.accountPage.chooseTheEmailServiceProvider") }}
                            </span>
                        </div>
                    </div>
                    <div class="flex gap-x-4 justify-center">
                        <div class="pt-4">
                            <div class="relative items-stretch mt-2 flex justify-center items-center">
                                <button
                                    type="button"
                                    class="relative group inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                    @click="authorize(MICROSOFT)"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21">
                                        <rect x="1" y="1" width="9" height="9" fill="#f25022" />
                                        <rect x="1" y="11" width="9" height="9" fill="#00a4ef" />
                                        <rect x="11" y="1" width="9" height="9" fill="#7fba00" />
                                        <rect x="11" y="11" width="9" height="9" fill="#ffb900" />
                                    </svg>
                                    <span
                                        class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden w-max px-2 py-1 text-xs text-white bg-black rounded-md group-hover:block"
                                    >
                                        {{ $t("settingsPage.accountPage.securelyLinkOutlookAccount") }}
                                    </span>
                                </button>
                            </div>
                        </div>
                        <div class="py-4">
                            <div class="relative items-stretch mt-2 flex justify-center items-center">
                                <button
                                    type="button"
                                    class="relative group inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                    @click="authorize(GOOGLE)"
                                >
                                    <svg
                                        class="-ml-0.5 h-5 w-5"
                                        aria-hidden="true"
                                        viewBox="0 0 24 24"
                                        xmlns="http://www.w3.org/2000/svg"
                                        fill="currentColor"
                                    >
                                        <path
                                            d="M23.4392061,12.2245191 C23.4392061,11.2412519 23.3594198,10.5237252 23.1867481,9.77963359 L11.9587786,9.77963359 L11.9587786,14.2176183 L18.5493435,14.2176183 C18.4165191,15.3205191 17.6989924,16.9814656 16.104458,18.0975573 L16.0821069,18.2461374 L19.6321832,20.9963359 L19.8781374,21.0208855 C22.1369771,18.9347176 23.4392061,15.8652824 23.4392061,12.2245191"
                                            id="Shape"
                                            fill="#4285F4"
                                        ></path>
                                        <path
                                            d="M11.9587786,23.9175573 C15.1876031,23.9175573 17.898229,22.8545038 19.8781374,21.0208855 L16.104458,18.0975573 C15.094626,18.8018015 13.7392672,19.2934351 11.9587786,19.2934351 C8.79636641,19.2934351 6.11230534,17.2073588 5.15551145,14.3239695 L5.01526718,14.3358779 L1.32384733,17.1927023 L1.27557252,17.3269008 C3.24210687,21.2334046 7.28152672,23.9175573 11.9587786,23.9175573"
                                            id="Shape"
                                            fill="#34A853"
                                        ></path>
                                        <path
                                            d="M5.15551145,14.3239695 C4.90305344,13.5798779 4.75694656,12.7825649 4.75694656,11.9587786 C4.75694656,11.1349008 4.90305344,10.3376794 5.14222901,9.59358779 L5.13554198,9.4351145 L1.3978626,6.53239695 L1.27557252,6.59056489 C0.465068702,8.21166412 0,10.0320916 0,11.9587786 C0,13.8854656 0.465068702,15.7058015 1.27557252,17.3269008 L5.15551145,14.3239695"
                                            id="Shape"
                                            fill="#FBBC05"
                                        ></path>
                                        <path
                                            d="M11.9587786,4.62403053 C14.2043359,4.62403053 15.719084,5.59401527 16.5828092,6.40461069 L19.9578321,3.10928244 C17.8850382,1.18259542 15.1876031,0 11.9587786,0 C7.28152672,0 3.24210687,2.68406107 1.27557252,6.59056489 L5.14222901,9.59358779 C6.11230534,6.71019847 8.79636641,4.62403053 11.9587786,4.62403053"
                                            id="Shape"
                                            fill="#EB4335"
                                        ></path>
                                    </svg>
                                    <span
                                        class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden w-max px-2 py-1 text-xs text-white bg-black rounded-md group-hover:block"
                                    >
                                        {{ $t("settingsPage.accountPage.securelyLinkGmailAccount") }}
                                    </span>
                                </button>
                            </div>
                        </div>

                        <!-- UNDER DEVELOPMENT -->
                        <div class="py-4">
                            <div class="relative items-stretch mt-2 flex justify-center items-center">
                                <button
                                    type="button"
                                    class="relative group inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                    @click="authorize(APPLE)"
                                >
                                    <svg
                                        class="css-10aieaf eu4oa1w0"
                                        width="16pt"
                                        height="16pt"
                                        viewBox="0 0 16 16"
                                        version="1.1"
                                    >
                                        <path
                                            style="
                                                stroke: none;
                                                fill-rule: nonzero;
                                                fill: rgb(0, 0, 0);
                                                fill-opacity: 1;
                                            "
                                            d="M 14.152344 12.257812 C 13.921875 12.792969 13.648438 13.28125 13.332031 13.734375 C 12.902344 14.347656 12.546875 14.773438 12.277344 15.007812 C 11.855469 15.398438 11.402344 15.59375 10.917969 15.605469 C 10.570312 15.605469 10.152344 15.507812 9.664062 15.308594 C 9.175781 15.109375 8.726562 15.007812 8.316406 15.007812 C 7.886719 15.007812 7.421875 15.109375 6.929688 15.308594 C 6.433594 15.507812 6.035156 15.613281 5.730469 15.621094 C 5.265625 15.640625 4.804688 15.4375 4.339844 15.007812 C 4.046875 14.753906 3.679688 14.3125 3.238281 13.6875 C 2.761719 13.019531 2.375 12.25 2.070312 11.367188 C 1.742188 10.414062 1.578125 9.496094 1.578125 8.601562 C 1.578125 7.582031 1.800781 6.699219 2.242188 5.960938 C 2.589844 5.367188 3.050781 4.898438 3.628906 4.554688 C 4.207031 4.210938 4.835938 4.039062 5.507812 4.027344 C 5.875 4.027344 6.359375 4.140625 6.960938 4.363281 C 7.558594 4.589844 7.941406 4.703125 8.113281 4.703125 C 8.238281 4.703125 8.664062 4.570312 9.390625 4.304688 C 10.074219 4.058594 10.652344 3.957031 11.125 3.996094 C 12.40625 4.097656 13.371094 4.605469 14.011719 5.515625 C 12.863281 6.210938 12.296875 7.183594 12.308594 8.433594 C 12.320312 9.40625 12.671875 10.214844 13.367188 10.859375 C 13.679688 11.15625 14.03125 11.386719 14.421875 11.550781 C 14.335938 11.796875 14.246094 12.03125 14.152344 12.257812 Z M 11.210938 0.679688 C 11.210938 1.445312 10.933594 2.15625 10.375 2.816406 C 9.707031 3.597656 8.894531 4.050781 8.015625 3.980469 C 8.003906 3.886719 8 3.792969 8 3.691406 C 8 2.957031 8.316406 2.175781 8.882812 1.535156 C 9.167969 1.210938 9.527344 0.941406 9.960938 0.726562 C 10.394531 0.511719 10.808594 0.394531 11.195312 0.375 C 11.207031 0.476562 11.210938 0.582031 11.210938 0.679688 Z M 11.210938 0.679688 "
                                        ></path>
                                    </svg>
                                    <span
                                        class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden w-max px-2 py-1 text-xs text-white bg-black rounded-md group-hover:block"
                                    >
                                        {{ $t("constants.underDevelopment") }}
                                    </span>
                                </button>
                            </div>
                        </div>

                        <!-- UNDER DEVELOPMENT -->
                        <div class="py-4">
                            <div class="relative items-stretch mt-2 flex justify-center items-center">
                                <button
                                    type="button"
                                    class="relative group inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                    @click="authorize(YAHOO)"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        aria-label="Yahoo!"
                                        role="img"
                                        viewBox="0 0 512 512"
                                        fill="#ffffff"
                                        width="16pt"
                                        height="16pt"
                                    >
                                        <rect width="512" height="512" rx="15%" fill="#5f01d1" />
                                        <g fill="#ffffff">
                                            <path d="M203 404h-62l25-59-69-165h63l37 95 37-95h62m58 76h-69l62-148h69" />
                                            <circle cx="303" cy="308" r="38" />
                                        </g>
                                    </svg>
                                    <span
                                        class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden w-max px-2 py-1 text-xs text-white bg-black rounded-md group-hover:block"
                                    >
                                        {{ $t("constants.underDevelopment") }}
                                    </span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, provide, inject } from "vue";
import { getData, postData } from "@/global/fetchData";
import { API_BASE_URL, YAHOO, GOOGLE, MICROSOFT, APPLE } from "@/global/const";
import AddUserDescriptionModal from "./AddUserDescriptionModal.vue";
import { i18n } from "@/global/preferences";

const username = ref("");
const emailsLinked = ref<EmailLinked[]>([]);
const emailSelected = ref("");
const isUnlinkModalOpen = ref(false);
const isAddUserDescriptionModalOpen = ref(false);
const isUpdateUserDescriptionModalOpen = ref(false);
const isAccountDeletionModalOpen = ref(false);
const userDescription = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const typeApi = ref("");
const showPassword = ref(false);
const showConfirmPassword = ref(false);

provide("emailSelected", emailSelected);
provide("typeApi", typeApi);
provide("fetchEmailLinked", fetchEmailLinked);
const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

interface EmailLinked {
    email: string;
    typeApi: string;
}

onMounted(() => {
    checkAuthorizationCode();
    fetchEmailLinked();
    fetchUsername();
    document.addEventListener("keydown", handleKeyDown);
});

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Escape") {
        if (isAddUserDescriptionModalOpen.value) {
            closeAddUserDescriptionModal();
        }
    }
}

function authorize(provider: string) {
    typeApi.value = provider;

    if (provider === MICROSOFT || provider === GOOGLE) {
        openAddUserDescriptionModal();
    }

    return;
}

function openAddUserDescriptionModal() {
    isAddUserDescriptionModalOpen.value = true;
}

function closeAddUserDescriptionModal() {
    isAddUserDescriptionModalOpen.value = false;
}

function togglePasswordVisibility(event: Event) {
    event.preventDefault();
    showPassword.value = !showPassword.value;
}

function toggleConfirmPasswordVisibility() {
    showConfirmPassword.value = !showConfirmPassword.value;
}

async function handleSubmit() {
    const result = await getData(`${API_BASE_URL}check_username/`);

    if (!result.success) {
        displayPopup?.("error", "Failed to submit data", result.error as string);
        return;
    }

    if (result.data.available === false) {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.accountPage.usernameAlreadyExists"),
            i18n.global.t("settingsPage.accountPage.pleaseChooseDifferentUsername")
        );
        return;
    }

    if (username.value.length <= 150 && !/\s/.test(username.value)) {
        await updateUsername();
    } else {
        if (username.value.length > 150) {
            displayPopup?.(
                "error",
                i18n.global.t(
                    "settingsPage.preferencesPage.popUpConstants.errorMessages.usernameMustNotExceed150Characters"
                ),
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.chooseAShorterUsername")
            );
        } else if (/\s/.test(username.value)) {
            displayPopup?.(
                "error",
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.usernameMustNotContainSpaces"),
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.chooseAUsernameWithoutSpaces")
            );
        }
    }

    if (
        newPassword.value &&
        newPassword.value === confirmPassword.value &&
        newPassword.value.length >= 8 &&
        newPassword.value.length <= 32
    ) {
        await updatePassword();
    } else {
        if (!newPassword.value || newPassword.value !== confirmPassword.value) {
            displayPopup?.(
                "error",
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.errorPasswordDontCorrespond"),
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.checkPassword")
            );
        } else if (newPassword.value.length < 8 || newPassword.value.length > 32) {
            displayPopup?.(
                "error",
                i18n.global.t(
                    "settingsPage.preferencesPage.popUpConstants.errorMessages.passwordMustBeBetween8And32Characters"
                ),
                i18n.global.t(
                    "settingsPage.preferencesPage.popUpConstants.errorMessages.chooseAPasswordWithTheAppropriateLength"
                )
            );
        }
    }
}

async function updatePassword() {
    const result = await postData(`user/preferences/update_password/`, { password: newPassword.value });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.accountPage.errorUpdatingPassword"),
            result.error as string
        );
        return;
    }

    displayPopup?.(
        "success",
        i18n.global.t("constants.popUpConstants.successMessages.success"),
        i18n.global.t("settingsPage.accountPage.passwordUpdatedSuccess")
    );
}

async function updateUsername() {
    const result = await postData(`user/preferences/update_username/`, { username: username.value });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.accountPage.errorUpdatingUsername"),
            result.error as string
        );
        return;
    }

    displayPopup?.(
        "success",
        i18n.global.t("constants.popUpConstants.successMessages.success"),
        i18n.global.t("settingsPage.accountPage.usernameUpdatedSuccess")
    );
}

function openAccountDeletionModal() {
    const isChecked = document.querySelector('input[name="choice"]:checked');

    if (isChecked) {
        isAccountDeletionModalOpen.value = true;
    } else {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.accountPage.confirmationRequired"),
            i18n.global.t("settingsPage.accountPage.checkBoxApprovalDeletion")
        );
    }
}

async function openUserDescriptionModal(email: string) {
    emailSelected.value = email;

    const result = await postData(`user/social_api/get_user_description/`, { email: email });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.accountPage.errorUnlinkingEmailAddress"),
            result.error as string
        );
        return;
    }

    isUpdateUserDescriptionModalOpen.value = true;
    userDescription.value = result.data.description;
}

async function openUnLinkModal(email: string) {
    emailSelected.value = email;
    isUnlinkModalOpen.value = true;

    if (emailsLinked.value.length === 1) {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.accountPage.unableToDeletePrimaryEmail"),
            i18n.global.t("settingsPage.accountPage.deleteAccountInstruction")
        );
        closeUnlinkModal();
        return;
    }
}

const intervalId = setInterval(checkAuthorizationCode, 1000);

function checkAuthorizationCode() {
    const urlParams = new URLSearchParams(window.location.search);
    const authorizationCode = urlParams.get("code");

    if (authorizationCode) {
        clearInterval(intervalId);
        linkEmail(authorizationCode);
    }
}

function closeUnlinkModal() {
    isUnlinkModalOpen.value = false;
}

async function linkEmail(authorizationCode: string) {
    const result = await postData("user/social_api/link/", {
        code: authorizationCode,
        typeApi: sessionStorage.getItem("typeApi"),
        user_description: sessionStorage.getItem("userDescription"),
    });

    if (!result.success) {
        displayPopup?.("error", i18n.global.t("settingsPage.accountPage.emailLinkingFailure"), result.error as string);
    } else {
        await fetchEmailLinked();
        displayPopup?.(
            "success",
            i18n.global.t("constants.popUpConstants.successMessages.success"),
            i18n.global.t("settingsPage.accountPage.emailLinkedSuccess")
        );
    }

    sessionStorage.clear();
    const currentUrl = window.location.href;
    const modifiedUrl = currentUrl.replace(/(\?)code=.*(&|$)/, "?").replace(/(\?)state=.*(&|$)/, "?");
    window.history.replaceState({}, document.title, modifiedUrl);
}

async function fetchEmailLinked() {
    const result = await getData("user/emails_linked/");
    if (!result) return;

    emailsLinked.value = result.data;
}

async function fetchUsername() {
    const result = await getData(`user/preferences/username/`);

    if (!result.success) {
        displayPopup?.("error", "Failed to fetch username", result.error as string);
        return;
    }

    username.value = result.data.username;
}
</script>
