<!-- V1 -->

<template>
  <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
    :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" />
  <div class="h-screen flex flex-col px-6 2xl:py-12 lg:px-8 overflow-y-auto" :class="bgColor">
    <div class="flex-grow flex flex-col justify-center py-4">
      <div class="w-full flex flex-col items-center">
        <div class="flex flex-col 2xl:mt-0 gap-y-1">
          <img class="mx-auto h-10 w-auto" :src="logo" alt="Your Company">
          <h2 class="text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Inscrivez-vous</h2>
        </div>
        <div class="2xl:mt-10 sm:mt-8 sm:mx-auto sm:w-full sm:max-w-[545px]"><!-- 480px sm:max-w-[545px] -->
          <div class="flex flex-col bg-slate-200 bg-opacity-80 rounded-lg">
            <div class="divide-y divide-slate-200">
              <div
                class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-lg bg-gray-400 bg-opacity-10">
                <nav aria-label="Progress">
                  <!--<div class="absolute right-4 left-4">-->
                  <ol role="list" class="flex items-center" v-if="step === 0">
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Current Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                        aria-current="step">
                        <span class="h-2.5 w-2.5 rounded-full bg-gray-700" aria-hidden="true"></span>
                        <span class="sr-only">Step 3</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 5</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 5</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 5</span>
                      </a>
                    </li>
                    <li class="relative">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 5</span>
                      </a>
                    </li>
                  </ol>
                  <ol role="list" class="flex items-center" v-if="step === 1">
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Completed Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                        <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd" />
                        </svg>
                        <span class="sr-only">Step 1</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Current Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-400 bg-white"
                        aria-current="step">
                        <span class="h-2.5 w-2.5 rounded-full bg-gray-400" aria-hidden="true"></span>
                        <span class="sr-only">Step 3</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 5</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 5</span>
                      </a>
                    </li>
                    <li class="relative">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 5</span>
                      </a>
                    </li>
                  </ol>
                  <ol role="list" class="flex items-center" v-if="step === 2">
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Completed Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                        <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd" />
                        </svg>
                        <span class="sr-only">Step 1</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                        <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd" />
                        </svg>
                        <span class="sr-only">Step 2</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Current Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-400 bg-white"
                        aria-current="step">
                        <span class="h-2.5 w-2.5 rounded-full bg-gray-400" aria-hidden="true"></span>
                        <span class="sr-only">Step 3</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 5</span>
                      </a>
                    </li>
                    <li class="relative">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 5</span>
                      </a>
                    </li>
                  </ol>
                  <ol role="list" class="flex items-center" v-if="step === 3">
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Completed Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                        <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd" />
                        </svg>
                        <span class="sr-only">Step 1</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                        <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd" />
                        </svg>
                        <span class="sr-only">Step 2</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                        <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd" />
                        </svg>
                        <span class="sr-only">Step 3</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Current Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                        aria-current="step">
                        <span class="h-2.5 w-2.5 rounded-full bg-gray-700" aria-hidden="true"></span>
                        <span class="sr-only">Step 3</span>
                      </a>
                    </li>
                    <li class="relative">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a @click="nextStep3"
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 5</span>
                      </a>
                    </li>
                  </ol>
                  <ol role="list" class="flex items-center" v-if="step === 4">
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Completed Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                        <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd" />
                        </svg>
                        <span class="sr-only">Step 1</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Current Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                        <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd" />
                        </svg>
                        <span class="sr-only">Step 1</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                        <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd" />
                        </svg>
                        <span class="sr-only">Step 1</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a
                        class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                        <svg class="h-5 w-5 text-gray-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                          <path fill-rule="evenodd"
                            d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                            clip-rule="evenodd" />
                        </svg>
                        <span class="sr-only">Step 1</span>
                      </a>
                    </li>
                    <li class="relative">
                      <!-- Current Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                        aria-current="step">
                        <span class="h-2.5 w-2.5 rounded-full bg-gray-700" aria-hidden="true"></span>
                        <span class="sr-only">Step 3</span>
                      </a>
                    </li>
                  </ol>
                </nav>
              </div>
              <div class="bg-white px-6 py-10 shadow sm:rounded-b-lg sm:px-12 hover:shadow-lg">
                <form class="space-y-6">
                  <div v-if="step === 3">
                    <div class="flex flex-col">
                      <div class="relative">
                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                          <div class="w-full border-t border-gray-300"></div>
                        </div>
                        <div class="relative flex justify-center">
                          <span class="bg-white px-2 text-sm text-gray-500">Lier un compte Gmail</span>
                        </div>
                      </div>
                      <div class="py-6">
                        <div class="relative items-stretch mt-2 flex justify-center items-center">
                          <button type="button"
                            class="inline-flex items-center gap-x-1.5 rounded-md bg-indigo-600 px-2.5 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
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
                            Lier mon compte Google
                          </button>
                        </div>
                      </div>
                      <div class="relative">
                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                          <div class="w-full border-t border-gray-300"></div>
                        </div>
                        <div class="relative flex justify-center">
                          <span class="bg-white px-2 text-sm text-gray-500">Lier un compte Outlook</span>
                        </div>
                      </div>
                      <div class="pt-4">
                        <div class="relative items-stretch mt-2 flex justify-center items-center">
                          <button type="button"
                            class="inline-flex items-center gap-x-1.5 rounded-md bg-indigo-600 px-2.5 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                            @click="authorize_microsoft">
                            <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21">
                              <title>MS-SymbolLockup</title>
                              <rect x="1" y="1" width="9" height="9" fill="#f25022" />
                              <rect x="1" y="11" width="9" height="9" fill="#00a4ef" />
                              <rect x="11" y="1" width="9" height="9" fill="#7fba00" />
                              <rect x="11" y="11" width="9" height="9" fill="#ffb900" />
                            </svg>
                            Lier mon compte Outlook
                          </button>
                        </div>
                      </div>
                      <div>
                        <div class="pt-8">
                          <button @click="nextStep3"
                            class="flex w-full justify-center rounded-md bg-gray-800 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800">Continuer</button>
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
                          <span class="bg-white px-2 text-sm text-gray-500">Présentation de l'outil</span>
                        </div>
                      </div>
                      <div class="py-6">
                        <div class="relative items-stretch mt-2">
                          <p class="font-semibold">En cours de construction</p>
                          <!-- To add : A video that explain the tool -->
                        </div>
                      </div>
                      <div class="relative">
                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                          <div class="w-full border-t border-gray-300"></div>
                        </div>
                        <div class="relative flex justify-center">
                          <span class="bg-white px-2 text-sm text-gray-500">Un point sur la confidentialité des
                            données</span>
                        </div>
                      </div>
                      <div class="pt-4">
                        <div class="relative items-stretch mt-2">
                          <p class="font-semibold">En cours de construction</p>
                          <!-- To add : A video that explain how data is saved and used -->
                        </div>
                      </div>
                      <div>
                        <div class="pt-8">
                          <button @click="submitSignupData"
                            class="flex w-full justify-center rounded-md bg-gray-800 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800">Finaliser
                            votre inscription</button>
                        </div>
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
          <p class="mt-6 text-center text-sm text-gray-500">
            Vous avez un compte?
            {{ ' ' }}
            <a href="/" class="font-semibold leading-6 text-gray-900 hover:text-black">Connectez-vous</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ShowNotification from '../components/ShowNotification.vue';
import { useRouter } from 'vue-router';
import { API_BASE_URL } from '@/main';

// Variables to display a notification
let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
let timerId = ref(null);

let bgColor = ref('');
bgColor = localStorage.getItem('bgColor');
const router = useRouter();
let step = ref(3);

onMounted(() => {
  document.addEventListener("keydown", handleKeyDown);
});

function handleKeyDown(event) {
  if (event.key === 'Enter') {
    event.preventDefault();

    if (step.value == 3) {
      nextStep3(event);
    }
  }
}
function authorize_google(event) {
  event.preventDefault();
  sessionStorage.setItem("type_api", "google");

  // Redirect the user to the authorization URL
  window.location.replace(`${API_BASE_URL}google/auth_url/`);
}
function authorize_microsoft(event) {
  event.preventDefault();
  sessionStorage.setItem("type_api", "microsoft");

  // Redirect the user to the authorization URL
  window.location.replace(`${API_BASE_URL}microsoft/auth_url/`);
}

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
async function nextStep3(event) {
  event.preventDefault();
  // After redirection, get the authorization code from the current URL
  const urlParams = new URLSearchParams(window.location.search);
  const authorizationCode = urlParams.get('code');

  if (authorizationCode) {
    sessionStorage.setItem("code", authorizationCode);
    step.value++;
  } else {
    // Show the pop-up
    backgroundColor.value = 'bg-red-300';
    notificationTitle.value = 'Erreur d\'autorisation';
    notificationMessage.value = 'Code d\'autorisation introuvable dans l\'URL';
    displayPopup();
  }
}

async function submitSignupData(event) {
  event.preventDefault();
  // TODO: checkbox I read all the infos and accept the terms
  console.log("The user has read and accepted our terms");

  try {
    // Prepare the data for registration
    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        login: sessionStorage.getItem('login'),
        password: sessionStorage.getItem('password'),
        theme: localStorage.getItem('theme'),
        color: localStorage.getItem('bgColor'),
        categories: localStorage.getItem('categories'),
        code: sessionStorage.getItem('code'),
        type_api: sessionStorage.getItem("type_api")
      })
    };

    // READY TO REGISTER THE USER IN DATABASE
    const response = await fetch(`${API_BASE_URL}signup/`, requestOptions);
    const data = await response.json();

    if (response.status === 201) {
      // Registration successful
      localStorage.setItem('user_id', data.user_id);
      // Django access token
      localStorage.setItem('access_token', data.access_token);
      // Store the email and use it in request headers
      localStorage.setItem('email', data.email);

      sessionStorage.clear();
      localStorage.removeItem("categories");
      // Redirect to the home page once signed in
      router.push({ name: 'home' });
    } else if (data.error == 'Email address already used') {
      // Show the pop-up      
      backgroundColor.value = 'bg-red-300';
      notificationTitle.value = 'Erreur lors de la création du compte';
      notificationMessage.value = 'Adresse e-mail déjà utilisée';
      displayPopup();

    } else {
      // Show the pop-up      
      backgroundColor.value = 'bg-red-300';
      notificationTitle.value = 'Erreur lors de la création du compte';
      notificationMessage.value = data.error;
      displayPopup();
    }
  } catch (error) {
    // Show the pop-up    
    backgroundColor.value = 'bg-red-300';
    notificationTitle.value = 'Erreur lors de la création du compte';
    notificationMessage.value = error;
    displayPopup();
  }
}
</script>

<script>
export default {
  data() {
    return {
      isOpen: false,
      logo: require('@/assets/LogoAugmentAI_export4.png')
    }
  },
  methods: {
    closeModal() {
      this.isOpen = false;
    }
  }
}
</script>