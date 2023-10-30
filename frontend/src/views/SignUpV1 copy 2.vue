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
              <div class="flex flex-col gap-y-4" v-if="step === 0">
                <div v-if="passwordError" class="mt-2 text-sm text-red-600">
                  {{ passwordError }}
                </div>
                <div>
                  <label for="login" class="block text-sm font-medium leading-6 text-gray-900">Identifiant</label>
                  <div class="mt-2">
                    <input v-model="login" id="login" type="login" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" />
                  </div>
                </div>

                <div>
                  <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Mot de passe</label>
                  <div class="mt-2">
                    <input v-model="password" id="password" type="password" autocomplete="current-password" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" />
                  </div>
                </div>

                <div>
                  <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Confirmer le mot de passe</label>
                  <div class="mt-2">
                    <input v-model="confirmPassword" id="confirm_password" type="password" @input="clearError()" autocomplete="current-password" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" />
                  </div>
                </div>

                <div>
                  <div class="pt-6">
                    <button @click="nextStep" class="flex w-full justify-center rounded-md bg-slate-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Continuer</button>
                  </div>
                </div>
              </div>
              <div v-if="step === 1">
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
                    <color @colorSelected="updateBgColor"></color>
                  </div>
                </div>
                <div>
                  <div class="pt-6">
                    <button @click="nextStep1" class="flex w-full justify-center rounded-md bg-gray-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Continuer</button>
                  </div>
                </div>
              </div>
              <div v-if="step === 2">
                <div class="flex flex-col">
                  <div class="relative">
                    <div class="absolute inset-0 flex items-center" aria-hidden="true">
                      <div class="w-full border-t border-gray-300"></div>
                    </div>
                    <div class="relative flex justify-center">
                      <span class="bg-white px-2 text-sm text-gray-500">Catégories</span>
                    </div>
                  </div>
                  <div class="pt-2">
                    <div class="relative items-stretch mt-2">
                      <div class="flex flex-col gap-y-4">
                        <p>Créer vos différentes catégories dans lesquelles vous souhaitez que l'assistant place automatiquement vos emails.</p>
                        <a href="#" class="underline text-gray-500">En savoir plus</a>
                        <div v-if="categories.length === 0">
                          <button @click="isOpen = !isOpen" type="button" class="relative block w-full rounded-lg border-2 border-dashed border-gray-300 p-12 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                            <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v20c0 4.418 7.163 8 16 8 1.381 0 2.721-.087 4-.252M8 14c0 4.418 7.163 8 16 8s16-3.582 16-8M8 14c0-4.418 7.163-8 16-8s16 3.582 16 8m0 0v14m0-4c0 4.418-7.163 8-16 8S8 28.418 8 24m32 10v6m0 0v6m0-6h6m-6 0h-6" />
                            </svg>
                            <span class="mt-2 block text-sm font-semibold text-gray-900">Ajouter une catégorie</span>
                          </button>
                        </div>
                        <div v-else class="max-h-64 overflow-y-auto flex flex-col gap-y-4">
                          <ul role="list" class="space-y-3">
                            <li v-for="category in categories" :key="category.name" class="overflow-hidden font-semibold rounded-md bg-gray-50 px-6 py-4 shadow hover:shadow-md text-gray-700">
                                {{ category.name }}
                            </li>
                            <!-- More items... -->
                          </ul>
                          <button @click="isOpen = !isOpen" type="button"  class="flex w-full justify-center rounded-md px-3 py-1.5 text-sm font-semibold border-2 border-dashed border-gray-300 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">Ajouter une autre catégorie</button>
                          <!--<button @click="isOpen = !isOpen" type="button" class="h-[25px] w-full rounded-lg border-2 border-dashed border-gray-300 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                            <span class="text-sm font-semibold text-gray-900">Ajouter une autre catégorie</span>
                          </button>-->
                          <!--
                          <button @click="isOpen = !isOpen" type="button"  class="flex w-full justify-center rounded-md bg-gray-400 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-slate-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Ajouter une autre catégorie</button>-->
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div>
                  <div class="pt-6">
                    <button @click="nextStep" class="flex w-full justify-center rounded-md bg-gray-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Continuer</button>
                  </div>
                </div>
              </div>
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
                      <p class="font-semibold">En cours de construction</p>
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
import { ref } from 'vue';
import Theme from '../components/SettingsTheme.vue';
import Color from '../components/SettingsColor.vue';
import axios from 'axios';

import {
  XMarkIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'UserSignUp',
  components: {
    Theme,
    Color,
    XMarkIcon
  },
  setup() {
    const bgColor = ref('#ffffff') // default background color

    const updateBgColor = (newBgColor) => {
      bgColor.value = newBgColor;
    }

    /*
    const callback = (response) => {
      // This callback will be triggered when the user selects or logs in to
      // his Google account from the popup
      console.log("Handle the response", response);
    }*/
    const handleSuccess = (googleUser) => {
      const idToken = googleUser.credential;
      authenticateWithDjango(idToken);
    }

    const handleError = (error) => {
      console.error("Erreur lors de la connexion avec Google:", error);
    }

    const authenticateWithDjango = (googleToken) => {
      console.log(googleToken);
      axios.post('http://localhost:9000/google-login/', { credential: googleToken })
        .then(response => {
          console.log(response);
          const receivedGoogleToken = response.data.googleToken; // Google Token received from the backend

          console.log("Successful Login");
          console.log("Google Token:", receivedGoogleToken);

          localStorage.setItem('googleToken', receivedGoogleToken);
        })
        .catch(error => {
          console.error("Erreur d'authentification avec Django:", error);
        });
    }

    const callback = (response) => {
      if (response) {
        console.log(response);
        handleSuccess(response);
      } else {
        handleError(response);
      }
    }

    return {
      bgColor,
      updateBgColor,
      callback
    }
  },
  data() {
    return {
      step: 0,
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
      errorMessage: '' 
    }
  },
  methods: {
    clearError() {
      console.log(this.passwordError);
      //this.passwordError = '';
    },
    nextStep0(event) {
      event.preventDefault();
      if (this.password !== this.confirmPassword) {
        this.passwordError = 'Les mots de passes ne correspondent pas';
        console.log(this.passwordError);
        return; 
      }
      else if (!this.password.trim() || !this.confirmPassword.trim()) {
        this.passwordError = 'Veuillez saisir un mot de passe';
        console.log(this.passwordError);
        return; 
      }    
      this.step++;
    },
    nextStep1() {
      this.color = this.bgColor;
      this.step++;
    },
    nextStep() {
      console.log(`Step: ${this.step}`);
      console.log(`Login: ${this.login}`);
      console.log(`Password: ${this.password}`);
      console.log(`Confirm Password: ${this.confirmPassword}`);
      console.log(`Password Error: ${this.passwordError}`);
      console.log(`Theme: ${this.theme}`);
      console.log(`Color: ${this.color}`);
      console.log(`Google Token: ${this.googleToken}`);
      console.log(`Is Open: ${this.isOpen}`);
      console.log(`Category Name: ${this.categoryName}`);
      console.log(`Category Description: ${this.categoryDescription}`);
      console.log(`Categories: ${JSON.stringify(this.categories)}`);
      console.log(`Error Message: ${this.errorMessage}`);
      this.step++;
    },
    nextStep3() {
      this.googleToken = localStorage.getItem('userToken');
      console.log(`Step: ${this.step}`);
      console.log(`Login: ${this.login}`);
      console.log(`Password: ${this.password}`);
      console.log(`Confirm Password: ${this.confirmPassword}`);
      console.log(`Password Error: ${this.passwordError}`);
      console.log(`Theme: ${this.theme}`);
      console.log(`Color: ${this.color}`);
      console.log(`Google Token: ${this.googleToken}`);
      console.log(`Is Open: ${this.isOpen}`);
      console.log(`Category Name: ${this.categoryName}`);
      console.log(`Category Description: ${this.categoryDescription}`);
      console.log(`Categories: ${JSON.stringify(this.categories)}`);
      console.log(`Error Message: ${this.errorMessage}`);
      this.step++;
    },
    closeModal() {
      this.isOpen = false;
    },
    addCategory() {
        // Vérification basique de la validité des champs
        if (!this.categoryName.trim() || !this.categoryDescription.trim()) {
            this.errorMessage = "Veuillez remplir tous les champs.";
            return;
        } else if (this.categories.some(cat => cat.name === this.categoryName)) {
            this.errorMessage = "Le nom de la catégorie existe déjà.";
            return;
        } else {
          this.categories.push({
                name: this.categoryName,
                description: this.categoryDescription
            });
            
            // Réinitialiser les champs et le message d'erreur
            this.categoryName = '';
            this.categoryDescription = '';
            this.errorMessage = '';
            
            // Fermer la modale
            this.isOpen = false;
        }
    },
    async submitSignupData(event) {
      event.preventDefault();
      try {
          const response = await axios.post('http://localhost:9000/MailAssistant/register/', {
              login: this.login,
              password: this.password,
              theme: this.theme,
              color: this.color,
              categories: this.categories,
              googletoken: this.googleToken
          });

          if (response.data && 'success' in response.data) {
              this.$router.push({ name: 'home' });
          } else {
            console.log("ERROR Signup No DATA"); // TO UPDATE : Display a screen to show the error to the user
          }
      } catch (error) {
          // Handle other errors like network issues or server being down
          console.error("Error during signup:", error);
      }
    }
  }
}
</script>