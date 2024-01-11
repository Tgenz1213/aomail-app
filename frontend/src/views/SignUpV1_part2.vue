<!-- V1 -->
<!-- TO FIX : Color background -->
<template>
  <transition name="modal-fade">
    <div class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center" v-if="isOpen">
      <div class="bg-white rounded-lg relative w-[450px]">
        <slot></slot>
          <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
              <button @click="closeModal" type="button" class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                  <span class="sr-only">Close</span>
                  <XMarkIcon class="h-6 w-6" aria-hidden="true" />
              </button>
          </div>
          <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
              <div class="ml-8 flex items-center space-x-1">
                  <p class="block font-semibold leading-6 text-gray-900">Nouvelle catégorie</p>
              </div>
          </div>
          <div class="flex flex-col gap-4 px-8 py-6">
            <p class="text-red-500"  v-if="errorMessage">{{ errorMessage }}</p>
            <div>
              <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Nom de la catégorie</label>
              <div class="mt-2">
                <input v-model="categoryName" name="email" id="email" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6" placeholder="Administratifs">
              </div>
            </div>
            <div>
              <label for="about" class="block text-sm font-medium leading-6 text-gray-900">Description brève de la catégorie</label>
              <div class="mt-2">
                <textarea v-model="categoryDescription" id="about" name="about" rows="3" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"></textarea>
              </div>
              <p class="mt-3 text-sm leading-6 text-gray-600">Cette description permettra à l'assitant à comprendre la catégorie</p>
            </div>
            <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
              <button type="button" class="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto" @click="addCategory">Créer</button>
            </div>
          </div>
      </div>
    </div>
  </transition>
  <div class="h-screen flex flex-col 2xl:justify-center 2xl:items-center px-6 2xl:py-12 sm:pt-6 lg:px-8" :class="bgColor">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=black" alt="Your Company" />
      <h2 class="2xl:mt-6 sm:mt-2 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Inscrivez-vous</h2>
    </div>
    <div class="2xl:mt-10 sm:mt-8 sm:mx-auto sm:w-full sm:max-w-[545px]"><!-- 480px sm:max-w-[545px] -->
      <div class="flex flex-col bg-slate-200 bg-opacity-80 rounded-lg"> 
        <div class="divide-y divide-slate-200">
          <div class="flex items-center justify-center h-[65px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-lg bg-gray-400 bg-opacity-10"> 
            <nav aria-label="Progress">
              <!--<div class="absolute right-4 left-4">-->
              <ol role="list" class="flex items-center" v-if="step === 0">
                <li class="relative pr-6 sm:pr-16">
                  <!-- Current Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-400 bg-white" aria-current="step">
                    <span class="h-2.5 w-2.5 rounded-full bg-gray-400" aria-hidden="true"></span>
                    <span class="sr-only">Step 3</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                    <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300" aria-hidden="true"></span>
                    <span class="sr-only">Step 5</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                    <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300" aria-hidden="true"></span>
                    <span class="sr-only">Step 5</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                    <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300" aria-hidden="true"></span>
                    <span class="sr-only">Step 5</span>
                  </a>
                </li>
                <li class="relative">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                    <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300" aria-hidden="true"></span>
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
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">Step 1</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Current Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-400 bg-white" aria-current="step">
                    <span class="h-2.5 w-2.5 rounded-full bg-gray-400" aria-hidden="true"></span>
                    <span class="sr-only">Step 3</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                    <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300" aria-hidden="true"></span>
                    <span class="sr-only">Step 5</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                    <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300" aria-hidden="true"></span>
                    <span class="sr-only">Step 5</span>
                  </a>
                </li>
                <li class="relative">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                    <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300" aria-hidden="true"></span>
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
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">Step 1</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">Step 2</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Current Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-400 bg-white" aria-current="step">
                    <span class="h-2.5 w-2.5 rounded-full bg-gray-400" aria-hidden="true"></span>
                    <span class="sr-only">Step 3</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                    <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300" aria-hidden="true"></span>
                    <span class="sr-only">Step 5</span>
                  </a>
                </li>
                <li class="relative">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                    <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300" aria-hidden="true"></span>
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
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">Step 1</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">Step 2</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">Step 3</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Current Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-400 bg-white" aria-current="step">
                    <span class="h-2.5 w-2.5 rounded-full bg-gray-400" aria-hidden="true"></span>
                    <span class="sr-only">Step 3</span>
                  </a>
                </li>
                <li class="relative">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                    <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300" aria-hidden="true"></span>
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
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">Step 1</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Current Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">Step 1</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">Step 1</span>
                  </a>
                </li>
                <li class="relative pr-6 sm:pr-16">
                  <!-- Upcoming Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full bg-white hover:bg-gray-200">
                    <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">Step 1</span>
                  </a>
                </li>
                <li class="relative">
                  <!-- Current Step -->
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="h-0.5 w-full bg-white"></div>
                  </div>
                  <a href="#" class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-400 bg-white" aria-current="step">
                    <span class="h-2.5 w-2.5 rounded-full bg-gray-400" aria-hidden="true"></span>
                    <span class="sr-only">Step 3</span>
                  </a>
                </li>
              </ol>
              <!--</div>-->
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
                      <!--<GoogleLogin :callback="callback"/>-->
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
                      <button @click="nextStep3" class="flex w-full justify-center rounded-md bg-gray-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Continuer</button>
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
                      <p class="font-semibold">En cours de construction</p> <!-- To add : A video that explain the tool -->
                    </div>
                  </div>
                  <div class="relative">
                    <div class="absolute inset-0 flex items-center" aria-hidden="true">
                      <div class="w-full border-t border-gray-300"></div>
                    </div>
                    <div class="relative flex justify-center">
                      <span class="bg-white px-2 text-sm text-gray-500">Un point sur la confidentialité des données</span>
                    </div>
                  </div>
                  <div class="pt-4">
                    <div class="relative items-stretch mt-2">
                      <p class="font-semibold">En cours de construction</p> <!-- To add : A video that explain how data is saved and used -->
                    </div>
                  </div>
                  <div>
                    <div class="pt-8">
                      <button @click="submitSignupData" class="flex w-full justify-center rounded-md bg-gray-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Finaliser votre inscription</button>
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
      <p class="mt-10 text-center text-sm text-gray-500">
        Vous avez un compte?
        {{ ' ' }}
        <a href="/" class="font-semibold leading-6 text-gray-900 hover:text-black">Connectez-vous</a>
      </p>
    </div>
  </div>
</template>
<script>
import {
  XMarkIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'UserSignUpPart2',
  components: {
    XMarkIcon
  },
  created() {
    console.log('Login:', sessionStorage.getItem('login'));
    console.log('Password:', sessionStorage.getItem('password'));
    console.log('Theme:', localStorage.getItem('theme'));
    console.log('Color:', localStorage.getItem('color'));
    console.log('Categories:', localStorage.getItem('categories'));
  },
  data() {
    return {
      step: 3,
      login: "",
      password: "",
      confirmPassword: "",
      passwordError: '',
      theme: "",
      color: "",
      googleToken: '',
      isOpen: false,
      categoryName: '',      // Pour le champ "Nom de la catégorie"
      categoryDescription: '', // Pour le champ "Description brève de la catégorie"
      categories: [],
      errorMessage: '',
    }
  },
  methods: {
    authorize_google(event) {
      event.preventDefault();
      sessionStorage.setItem("type_api", "google");

      // Redirect the user to the authorization URL
      window.location.replace("http://localhost:9000/MailAssistant/google/auth_url/");
    },
    authorize_microsoft(event) {
      event.preventDefault();
      sessionStorage.setItem("type_api", "microsoft");

      // Redirect the user to the authorization URL
      window.location.replace("http://localhost:9000/MailAssistant/microsoft/auth_url/");
    },    
    closeModal() {
      this.isOpen = false;
    },
    async nextStep3(event) {
      event.preventDefault();
      // After redirection, get the authorization code from the current URL
      const urlParams = new URLSearchParams(window.location.search);
      const authorizationCode = urlParams.get('code');

      if (authorizationCode) {
        // The authorization code is available, you can use it as needed
        console.log('Authorization Code:', authorizationCode);
        sessionStorage.setItem("code", authorizationCode);
        this.step++;
      } else {
        // TODO: display an error pop up
        console.error('Authorization Code not found in the URL');
      }
    },
    async submitSignupData(event) {
      event.preventDefault();
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
            color: localStorage.getItem('color'),
            categories: localStorage.getItem('categories'),
            code: sessionStorage.getItem('code'),
            type_api: sessionStorage.getItem("type_api")
          })
        };
        
        // READY TO REGISTER THE USER IN DATABASE
        const response = await fetch('http://localhost:9000/MailAssistant/signup/', requestOptions);      

        if (response.status === 201) {
          // Registration successful
          const data = await response.json();
          localStorage.setItem('user_id', data.user_id);
          // JWT access token
          localStorage.setItem('access_token', data.access_token);

          console.log('Signup successful');
          sessionStorage.clear();
          // Redirect to the home page once signed in
          this.$router.push({ name: 'home' });
        } else {
          // TODO: Display a screen to show the error to the user
          console.error("Signup unsuccessful");
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }
  }
}
</script>