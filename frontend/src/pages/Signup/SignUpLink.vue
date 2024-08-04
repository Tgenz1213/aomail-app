<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />
    <div class="h-screen flex flex-col px-6 2xl:py-12 lg:px-8 overflow-y-auto">
        <div class="flex-grow flex flex-col justify-center py-4">
            <div class="w-full flex flex-col items-center">
                <div class="flex flex-col 2xl:mt-0 gap-y-1">
                    <img class="mx-auto h-10 w-auto" :src="logo" alt="Aomail" />
                    <h2 class="text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                        {{ $t("signUpPart1Page.signUp") }}
                    </h2>
                </div>
                <div class="2xl:mt-6 sm:mt-4 sm:mx-auto sm:w-full sm:max-w-[545px]">
                    <div class="flex flex-col">
                        <div class="">
                            <div class="flex items-center justify-center h-[65px]">
                                <nav aria-label="Progress">
                                    <ol role="list" class="flex items-center" v-if="step === 0">
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                                aria-current="step"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-gray-700"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                        <li class="relative">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                    </ol>
                                    <ol role="list" class="flex items-center" v-if="step === 1">
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                                            >
                                                <svg
                                                    class="h-5 w-5 text-gray-700"
                                                    viewBox="0 0 20 20"
                                                    fill="currentColor"
                                                    aria-hidden="true"
                                                >
                                                    <path
                                                        fill-rule="evenodd"
                                                        d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                                        clip-rule="evenodd"
                                                    />
                                                </svg>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-400 bg-white"
                                                aria-current="step"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-gray-400"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                        <li class="relative">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                    </ol>
                                    <ol role="list" class="flex items-center" v-if="step === 2">
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                                            >
                                                <svg
                                                    class="h-5 w-5 text-gray-400"
                                                    viewBox="0 0 20 20"
                                                    fill="currentColor"
                                                    aria-hidden="true"
                                                >
                                                    <path
                                                        fill-rule="evenodd"
                                                        d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                                        clip-rule="evenodd"
                                                    />
                                                </svg>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                                            >
                                                <svg
                                                    class="h-5 w-5 text-gray-400"
                                                    viewBox="0 0 20 20"
                                                    fill="currentColor"
                                                    aria-hidden="true"
                                                >
                                                    <path
                                                        fill-rule="evenodd"
                                                        d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                                        clip-rule="evenodd"
                                                    />
                                                </svg>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-400 bg-white"
                                                aria-current="step"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-gray-400"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                        <li class="relative">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                    </ol>
                                    <ol role="list" class="flex items-center" v-if="step === 3">
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                                            >
                                                <svg
                                                    class="h-5 w-5 text-gray-700"
                                                    viewBox="0 0 20 20"
                                                    fill="currentColor"
                                                    aria-hidden="true"
                                                >
                                                    <path
                                                        fill-rule="evenodd"
                                                        d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                                        clip-rule="evenodd"
                                                    />
                                                </svg>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                                            >
                                                <svg
                                                    class="h-5 w-5 text-gray-700"
                                                    viewBox="0 0 20 20"
                                                    fill="currentColor"
                                                    aria-hidden="true"
                                                >
                                                    <path
                                                        fill-rule="evenodd"
                                                        d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                                        clip-rule="evenodd"
                                                    />
                                                </svg>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                                            >
                                                <svg
                                                    class="h-5 w-5 text-gray-700"
                                                    viewBox="0 0 20 20"
                                                    fill="currentColor"
                                                    aria-hidden="true"
                                                >
                                                    <path
                                                        fill-rule="evenodd"
                                                        d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                                        clip-rule="evenodd"
                                                    />
                                                </svg>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                                aria-current="step"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-gray-700"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                        <li class="relative">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                @click="nextStep3"
                                                class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                    </ol>
                                    <ol role="list" class="flex items-center" v-if="step === 4">
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                                            >
                                                <svg
                                                    class="h-5 w-5 text-gray-700"
                                                    viewBox="0 0 20 20"
                                                    fill="currentColor"
                                                    aria-hidden="true"
                                                >
                                                    <path
                                                        fill-rule="evenodd"
                                                        d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                                        clip-rule="evenodd"
                                                    />
                                                </svg>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                                            >
                                                <svg
                                                    class="h-5 w-5 text-gray-700"
                                                    viewBox="0 0 20 20"
                                                    fill="currentColor"
                                                    aria-hidden="true"
                                                >
                                                    <path
                                                        fill-rule="evenodd"
                                                        d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                                        clip-rule="evenodd"
                                                    />
                                                </svg>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                                            >
                                                <svg
                                                    class="h-5 w-5 text-gray-700"
                                                    viewBox="0 0 20 20"
                                                    fill="currentColor"
                                                    aria-hidden="true"
                                                >
                                                    <path
                                                        fill-rule="evenodd"
                                                        d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                                        clip-rule="evenodd"
                                                    />
                                                </svg>
                                            </a>
                                        </li>
                                        <li class="relative pr-6 sm:pr-16">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200 border-2 border-gray-700"
                                            >
                                                <svg
                                                    class="h-5 w-5 text-gray-700"
                                                    viewBox="0 0 20 20"
                                                    fill="currentColor"
                                                    aria-hidden="true"
                                                >
                                                    <path
                                                        fill-rule="evenodd"
                                                        d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                                        clip-rule="evenodd"
                                                    />
                                                </svg>
                                            </a>
                                        </li>
                                        <li class="relative">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a
                                                class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                                                aria-current="step"
                                            >
                                                <span
                                                    class="h-2.5 w-2.5 rounded-full bg-gray-700"
                                                    aria-hidden="true"
                                                ></span>
                                            </a>
                                        </li>
                                    </ol>
                                </nav>
                            </div>
                            <div class="bg-white px-6 py-4 sm:px-12">
                                <form class="space-y-6">
                                    <div v-if="step === 3">
                                        <div class="flex flex-col">
                                            <div class="relative">
                                                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                    <div class="w-full border-t border-gray-300"></div>
                                                </div>
                                                <div class="relative flex justify-center">
                                                    <span class="bg-white px-2 text-sm text-gray-500">
                                                        {{ $t("signUpPart2Page.linkAGmailAccount") }}
                                                    </span>
                                                </div>
                                            </div>
                                            <div class="py-4">
                                                <div
                                                    class="relative items-stretch mt-2 flex justify-center items-center"
                                                >
                                                    <button
                                                        type="button"
                                                        class="inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                                        @click="authorizeGoogle"
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
                                                        {{ $t("signUpPart2Page.linkYourGmailAccount") }}
                                                    </button>
                                                </div>
                                            </div>
                                            <div class="relative">
                                                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                    <div class="w-full border-t border-gray-300"></div>
                                                </div>
                                                <div class="relative flex justify-center">
                                                    <span class="bg-white px-2 text-sm text-gray-500">
                                                        {{ $t("signUpPart2Page.linkAnOutlookAccount") }}
                                                    </span>
                                                </div>
                                            </div>
                                            <div class="pt-4">
                                                <div
                                                    class="relative items-stretch mt-2 flex justify-center items-center"
                                                >
                                                    <button
                                                        type="button"
                                                        class="inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                                        @click="authorizeMicrosoft"
                                                    >
                                                        <svg
                                                            xmlns="http://www.w3.org/2000/svg"
                                                            width="21"
                                                            height="21"
                                                            viewBox="0 0 21 21"
                                                        >
                                                            <title>MS-SymbolLockup</title>
                                                            <rect x="1" y="1" width="9" height="9" fill="#f25022" />
                                                            <rect x="1" y="11" width="9" height="9" fill="#00a4ef" />
                                                            <rect x="11" y="1" width="9" height="9" fill="#7fba00" />
                                                            <rect x="11" y="11" width="9" height="9" fill="#ffb900" />
                                                        </svg>
                                                        {{ $t("signUpPart2Page.linkYourOutlookAccount") }}
                                                    </button>
                                                </div>
                                            </div>
                                            <div>
                                                <div class="pt-10">
                                                    <button
                                                        @click="nextStep3"
                                                        class="flex w-full justify-center rounded-md bg-gray-800 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800"
                                                    >
                                                        {{ $t("signUpPart1Page.continue") }}
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div v-if="step === 4">
                                        <div class="flex flex-col">
                                            <div class="relative">
                                                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                    <div class="w-full border-t border-gray-300"></div>
                                                </div>
                                                <div class="relative flex justify-center">
                                                    <span class="bg-white px-2 text-sm text-gray-500">
                                                        {{ $t("signUpPart2Page.toolsPresentation") }}
                                                    </span>
                                                </div>
                                            </div>
                                            <div class="py-6">
                                                <div class="relative items-stretch mt-2">
                                                    <p class="font-semibold">{{ $t("constants.workInProgress") }}</p>
                                                    <!-- To add : A video that explain the tool -->
                                                </div>
                                            </div>
                                            <div class="relative">
                                                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                    <div class="w-full border-t border-gray-300"></div>
                                                </div>
                                                <div class="relative flex justify-center">
                                                    <span class="bg-white px-2 text-sm text-gray-500">
                                                        {{ $t("signUpPart2Page.informationOnDataConfidentiality") }}
                                                    </span>
                                                </div>
                                            </div>
                                            <div class="pt-4">
                                                <div class="relative items-stretch mt-2">
                                                    <p class="font-semibold">{{ $t("constants.workInProgress") }}</p>
                                                    <!-- To add : A video that explain how data is saved and used -->
                                                </div>
                                            </div>
                                            <div>
                                                <div class="pt-8">
                                                    <button
                                                        id="submit-button"
                                                        @click="submitSignupData"
                                                        class="flex w-full justify-center rounded-md bg-gray-800 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800"
                                                    >
                                                        {{ $t("signUpPart2Page.finalizeRegistration") }}
                                                    </button>
                                                </div>
                                            </div>
                                            <div class="space-y-5 pt-3">
                                                <div class="relative flex items-start">
                                                    <div class="flex h-6 items-center">
                                                        <input
                                                            id="comments"
                                                            aria-describedby="comments-description"
                                                            name="comments"
                                                            type="checkbox"
                                                            class="h-4 w-4 rounded border-gray-300 text-black focus:ring-black"
                                                        />
                                                    </div>
                                                    <div class="ml-3 text-sm leading-6 w-full">
                                                        <label for="comments" class="text-gray-500 font-normal">
                                                            {{ $t("signUpPart2Page.iAcceptThe") }}
                                                            <a
                                                                href="URL_DES_CONDITIONS"
                                                                class="font-medium text-black hover:underline"
                                                                target="_blank"
                                                            >
                                                                {{ $t("signUpPart2Page.conditionsAndPrivacyPolicyOf") }}
                                                            </a>
                                                            Aomail
                                                        </label>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                    <p class="mt-6 text-center text-sm text-gray-500">
                        {{ $t("signUpPart1Page.youHaveAnAccount") }}
                        <a href="/" class="font-semibold leading-6 text-gray-900 hover:text-black">
                            {{ $t("constants.userActions.login") }}
                        </a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { API_BASE_URL } from "@/global/const";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import NotificationTimer from "@/components/NotificationTimer.vue";
import { i18n } from "@/global/Settings/preferences";
import logo from "@/assets/logo-aomail.png";

const showNotification = ref<boolean>(false);
const notificationTitle = ref<string>("");
const notificationMessage = ref<string>("");
const backgroundColor = ref<string>("");
const timerId = ref<number | null>(null);
const step = ref(3);
const router = useRouter();

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Enter") {
        event.preventDefault();
        if (step.value === 3) {
            nextStep3(event);
        }
    }
}

function authorizeGoogle(event: Event) {
    event.preventDefault();
    sessionStorage.setItem("typeApi", "google");
    window.location.replace(`${API_BASE_URL}google/auth_url/`);
}

function authorizeMicrosoft(event: Event) {
    event.preventDefault();
    sessionStorage.setItem("typeApi", "microsoft");
    window.location.replace(`${API_BASE_URL}microsoft/auth_url/`);
}

async function nextStep3(event: Event) {
    event.preventDefault();
    const urlParams = new URLSearchParams(window.location.search);
    const authorizationCode = urlParams.get("code");

    if (authorizationCode) {
        sessionStorage.setItem("code", authorizationCode);
        step.value++;
    } else {
        displayPopup(
            "error",
            i18n.global.t("signUpPart2Page.authorizationError"),
            i18n.global.t("signUpPart2Page.authorizationCodeNotFound")
        );
    }
}

async function submitSignupData(event: Event) {
    event.preventDefault();
    const checkbox = document.getElementById("comments") as HTMLInputElement;
    const label = document.querySelector('label[for="comments"]') as HTMLLabelElement;
    const link = document.querySelector('label[for="comments"] a') as HTMLAnchorElement;

    if (!checkbox.checked) {
        label.classList.add("text-red-500");
        label.classList.remove("text-gray-500");
        link.classList.add("text-red-500");
        link.classList.remove("text-black");

        displayPopup(
            "error",
            i18n.global.t("signUpPart2Page.acceptTerms"),
            i18n.global.t("signUpPart2Page.termsNotAccepted")
        );
        return;
    } else {
        label.classList.remove("text-red-500");
        label.classList.add("text-gray-500");
        link.classList.remove("text-red-500");
        link.classList.add("text-black");
    }

    displayPopup("success", "Account creation in progress...", "Waiting for database response");

    try {
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                login: sessionStorage.getItem("login"),
                password: sessionStorage.getItem("password"),
                timezone: localStorage.getItem("timezone"),
                language: localStorage.getItem("language"),
                theme: localStorage.getItem("theme"),
                categories: localStorage.getItem("categories"),
                code: sessionStorage.getItem("code"),
                typeApi: sessionStorage.getItem("typeApi"),
                userDescription: sessionStorage.getItem("userDescription"),
            }),
        };

        const response = await fetch(`${API_BASE_URL}signup/`, requestOptions);
        const data = await response.json();

        if (response.status === 201) {
            localStorage.setItem("accessToken", data.access_token);
            sessionStorage.clear();
            localStorage.removeItem("categories");
            router.push({ name: "home" });
        } else if (data.error === "Email address already used") {
            displayPopup(
                "error",
                i18n.global.t("signUpPart2Page.accountCreationError"),
                i18n.global.t("constants.popUpConstants.errorMessages.emailAlreadyUsed")
            );
        } else {
            displayPopup("error", i18n.global.t("signUpPart2Page.accountCreationError"), data.error);
        }
    } catch (error) {
        displayPopup(
            "error",
            i18n.global.t("signUpPart2Page.accountCreationError"),
            error instanceof Error ? error.message : String(error)
        );
    }
}

function displayPopup(type: "success" | "error", title: string, message: string) {
    if (type === "error") {
        displayErrorPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    } else {
        displaySuccessPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    }
    timerId.value = setTimeout(dismissPopup, 4000);
}

function dismissPopup() {
    showNotification.value = false;
    if (timerId.value !== null) {
        clearTimeout(timerId.value);
    }
}
</script>

<!-- TODO:
- use arrays to build the HTML instead of hardcoding (there are a lot of duplicates)
- rename the function (nextStep0, etc) to a relevant name like nextPasswordForm, nextLinkEmailForm, nextSomething -->
