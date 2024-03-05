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
                        <div class="relative items-stretch mt-2">
                          <button @click="authorize_google">Lier votre compte Google</button>
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
                        <div class="relative items-stretch mt-2">
                          <button @click="authorize_microsoft">Lier votre compte Outlook</button>
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
import { ref } from 'vue';
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
      console.log('Signup successful');
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