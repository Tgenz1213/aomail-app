<template>
  <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
    :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" />
  <!-- Update Category modal -->
  <transition name="modal-fade">
    <div class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
      v-if="isModalUpdateOpen">
      <div class="bg-white rounded-lg relative w-[450px]">
        <slot></slot>
        <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
          <button @click="closeUpdateModal" type="button"
            class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
            <span class="sr-only">Close</span>
            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
        <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
          <div class="ml-8 flex items-center space-x-1">
            <p class="block leading-6 text-gray-900" style="font-family: 'Poppins', sans-serif; font-weight: 500;">
              Modifier une catégorie</p>
          </div>
        </div>
        <div class="flex flex-col gap-4 px-8 py-6">
          <p class="text-red-500" v-if="errorUpdateMessage">{{ errorUpdateMessage }}</p>
          <div>
            <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Nom de la catégorie</label>
            <div class="mt-2">
              <input id="updateCategoryName" v-model="updateCategoryName"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"
                placeholder="Administratifs">
            </div>
          </div>
          <div>
            <label for="about" class="block text-sm font-medium leading-6 text-gray-900">Description brève de la
              catégorie</label>
            <div class="mt-2">
              <textarea id="updateCategoryDescription" v-model="updateCategoryDescription" rows="3"
                style="min-height: 60px"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"></textarea>
            </div>
            <p class="mt-3 text-sm leading-6 text-gray-600">Cette description permettra à l'assitant à comprendre la
              catégorie</p>
          </div>
          <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
            <button type="button"
              class="inline-flex w-full justify-center rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:ml-3 sm:w-auto"
              @click="updateCategoryHandler">Mettre à jour</button>
            <button type="button"
              class="inline-flex w-full justify-cente items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto"
              @click="deleteCategoryOnUpdate">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
              </svg>
              Supprimer
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
  <!-- Create Category modal -->
  <transition name="modal-fade">
    <div class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
      v-if="isModalOpen">
      <div class="bg-white rounded-lg relative w-[450px]">
        <slot></slot>
        <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
          <button @click="closeModal" type="button"
            class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
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
          <p class="text-red-500" v-if="errorMessage">{{ errorMessage }}</p>
          <div>
            <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Nom de la
              catégorie</label>
            <div class="mt-2">
              <input v-model="categoryName" name="email" id="categoryName"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"
                placeholder="Administratifs">
            </div>
          </div>
          <div>
            <label for="about" class="block text-sm font-medium leading-6 text-gray-900">Description brève
              de la
              catégorie</label>
            <div class="mt-2">
              <textarea v-model="categoryDescription" id="categoryDescription" name="about" rows="3"
                style="min-height: 60px"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"></textarea>
            </div>
            <p class="mt-3 text-sm leading-6 text-gray-600">Cette description permettra à l'assitant à
              comprendre la
              catégorie</p>
          </div>
          <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
            <button type="button"
              class="inline-flex w-full justify-center rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:ml-3 sm:w-auto"
              @click="addCategory">Créer</button>
          </div>
        </div>
      </div>
    </div>
  </transition>
  <div class="h-screen flex flex-col px-6 2xl:py-12 lg:px-8 overflow-y-auto" :class="bgColor">
    <!--OLD VALUE TO SAVE : 27/01/2024 => 2xl:justify-center 2xl:items-center-->
    <div class="flex-grow flex flex-col justify-center py-4">
      <div class="w-full flex flex-col items-center">
        <div class="flex flex-col 2xl:mt-0 gap-y-1">
          <img class="mx-auto h-10 w-auto" :src="logo" alt="Your Company">
          <h2 class="text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Inscrivez-vous
          </h2>
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
                        <span class="sr-only">Step 0</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a @click="nextStep0"
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 1</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a @click="goStep2"
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 2</span>
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
                      <a @click="goStep0"
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
                      <a class="relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-700 bg-white"
                        aria-current="step">
                        <span class="h-2.5 w-2.5 rounded-full bg-gray-700" aria-hidden="true"></span>
                        <span class="sr-only">Step 2</span>
                      </a>
                    </li>
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Upcoming Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a @click="nextStep1"
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
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
                  <ol role="list" class="flex items-center" v-if="step === 2">
                    <li class="relative pr-6 sm:pr-16">
                      <!-- Completed Step -->
                      <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="h-0.5 w-full bg-white"></div>
                      </div>
                      <a @click="goStep0"
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
                      <a @click="goStep1"
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
                      <a @click="submitSignupData"
                        class="group relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-white hover:border-gray-300">
                        <span class="h-2.5 w-2.5 rounded-full bg-transparent group-hover:bg-gray-300"
                          aria-hidden="true"></span>
                        <span class="sr-only">Step 4</span>
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
                      <a
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
                  <!--</div>-->
                </nav>
              </div>
              <div class="bg-white px-6 py-10 shadow sm:rounded-b-lg sm:px-12 hover:shadow-lg">
                <form class="space-y-6">
                  <div class="flex flex-col gap-y-4" v-if="step === 0">
                    <div v-if="credentialError" class="mt-2 text-sm text-red-600">
                      {{ credentialError }}
                    </div>
                    <div>
                      <div class="flex gap-x-1 items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                          stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                        </svg>
                        <label for="login" class="block text-sm font-medium leading-6 text-gray-900">Identifiant</label>
                      </div>
                      <div class="mt-2">
                        <input v-model="login" id="login" type="login"
                          class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6" />
                      </div>
                    </div>
                    <div>
                      <div class="flex gap-x-1 items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                          stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="M15.75 5.25a3 3 0 0 1 3 3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1 1 21.75 8.25Z" />
                        </svg>
                        <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Mot de
                          passe</label>
                      </div>
                      <div class="relative items-stretch mt-2 flex">
                        <input id="password" v-if="!showPassword" type="password"
                          class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                          v-model="password" />
                        <input id="password" v-else type="text"
                          class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                          v-model="password" />
                        <div class="flex items-center">
                          <button @click.prevent="togglePasswordVisibility"
                            class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300">
                            <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                              stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                              <path stroke-linecap="round" stroke-linejoin="round"
                                d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                              <path stroke-linecap="round" stroke-linejoin="round"
                                d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                            </svg>
                            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                              stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                              <path stroke-linecap="round" stroke-linejoin="round"
                                d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                    <div>
                      <div class="flex gap-x-1 items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                          stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="M15.75 5.25a3 3 0 0 1 3 3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1 1 21.75 8.25Z" />
                        </svg>
                        <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Confirmer
                          le mot
                          de passe</label>
                      </div>
                      <div class="relative items-stretch mt-2 flex">
                        <input id="confirmPassword" v-if="!showConfirmPassword" type="password"
                          v-model="confirmPassword" @input="clearError()" autocomplete="current-password"
                          class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6" />
                        <input id="confirmPassword" v-else type="text"
                          class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                          v-model="confirmPassword" />
                        <button @click.prevent="toggleConfirmPasswordVisibility"
                          class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300">
                          <svg v-if="!showConfirmPassword" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                              d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                            <path stroke-linecap="round" stroke-linejoin="round"
                              d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                          </svg>
                          <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                            stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                              d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                          </svg>
                        </button>
                      </div>
                    </div>
                    <div>
                      <div class="pt-6">
                        <button @click.prevent="nextStep0"
                          class="flex w-full justify-center rounded-md bg-gray-800 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Continuer</button>
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
                        <button @click.prevent="nextStep1"
                          class="flex w-full justify-center rounded-md bg-gray-800 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800">Continuer</button>
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
                            <p>Créer vos différentes catégories dans lesquelles vous
                              souhaitez que l'assistant place
                              automatiquement vos emails.</p>
                            <div v-if="categories.length === 0">
                              <button @click="isModalOpen = !isModalOpen" type="button"
                                class="relative block w-full rounded-lg border-2 border-dashed border-gray-300 p-12 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                                <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none"
                                  viewBox="0 0 48 48" aria-hidden="true">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M8 14v20c0 4.418 7.163 8 16 8 1.381 0 2.721-.087 4-.252M8 14c0 4.418 7.163 8 16 8s16-3.582 16-8M8 14c0-4.418 7.163-8 16-8s16 3.582 16 8m0 0v14m0-4c0 4.418-7.163 8-16 8S8 28.418 8 24m32 10v6m0 0v6m0-6h6m-6 0h-6" />
                                </svg>
                                <span class="mt-2 block text-sm font-semibold text-gray-900">Ajouter
                                  une
                                  catégorie</span>
                              </button>
                            </div>
                            <div v-else class="max-h-64 overflow-y-auto flex flex-col gap-y-4">
                              <ul role="list" class="space-y-3">
                                <li v-for="category in categories" :key="category.name"
                                  class="flex items-center justify-between overflow-hidden font-semibold rounded-md bg-gray-50 px-6 py-4 shadow hover:shadow-md text-gray-700 relative">
                                  <span>{{ category.name }}</span>
                                  <div class="flex gap-1">
                                    <button type="button"
                                      class="inline-flex justify-center items-center gap-x-1 rounded-md px-3 py-2 text-sm font-semibold text-gray-800 hover:text-black"
                                      @click.stop="openUpdateModal(category)">
                                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                          d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                                      </svg>
                                    </button>
                                    <button type="button"
                                      class="inline-flex justify-center items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700"
                                      @click="deleteCategoryHandler(category)">
                                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                          d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                      </svg>
                                    </button>
                                  </div>
                                </li>
                              </ul>
                              <button @click="isModalOpen = !isModalOpen" type="button"
                                class="flex w-full justify-center rounded-md px-3 py-1.5 text-sm font-semibold border-2 border-dashed border-gray-300 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">Ajouter
                                une autre catégorie</button>
                              <!--<button @click="isModalOpen = !isModalOpen" type="button" class="h-[25px] w-full rounded-lg border-2 border-dashed border-gray-300 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                                <span class="text-sm font-semibold text-gray-900">Ajouter une autre catégorie</span>
                              </button>-->
                              <!--
                              <button @click="isModalOpen = !isModalOpen" type="button"  class="flex w-full justify-center rounded-md bg-gray-400 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-slate-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500">Ajouter une autre catégorie</button>-->
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div>
                      <div class="pt-6">
                        <button @click.prevent="submitSignupData"
                          class="flex w-full justify-center rounded-md bg-gray-800 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-gray-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800">Continuer</button>
                      </div>
                    </div>
                  </div>
                </form>
                <div>
                </div>
              </div>
            </div>
          </div>
          <p class="mt-6 text-center text-sm text-gray-600">
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
import Theme from '../components/SettingsTheme.vue';
import Color from '../components/SettingsColor.vue';
import { API_BASE_URL } from '@/main';
import { XMarkIcon } from '@heroicons/vue/24/outline'
import { useRouter } from 'vue-router';
import ShowNotification from '../components/ShowNotification.vue';

const router = useRouter();

let bgColor = ref('bg-gradient-to-r from-sky-300 to-blue-300');
let showPassword = ref(false);
let showConfirmPassword = ref(false);
let step = ref(0);
let login = ref('');
let password = ref('');
let confirmPassword = ref('');
let credentialError = ref('');
let theme = ref('');
let isModalOpen = ref(false);
let isModalUpdateOpen = ref(false);
let categoryName = ref('');
let categoryDescription = ref('');
let updateCategoryName = ref('');
let updateOldCategoryName = ref('');
let updateCategoryDescription = ref('');
let categoryOpened = ref(null);
let categories = ref([]);
let errorMessage = ref('');
let errorUpdateMessage = ref('');

// Variables to display a notification
let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
let timerId = ref(null);


onMounted(() => {
  document.addEventListener("keydown", handleKeyDown);
});

function openUpdateModal(category) {
  updateCategoryName.value = category.name;
  updateOldCategoryName.value = category.name;
  updateCategoryDescription.value = category.description;
  categoryOpened.value = category;
  isModalUpdateOpen.value = true;
}
function closeUpdateModal() {
  isModalUpdateOpen.value = false;
}
function deleteCategoryHandler(category) {
  const indexToRemove = categories.value.indexOf(category);
  if (indexToRemove !== -1) {
    categories.value.splice(indexToRemove, 1);
  }
}
function deleteCategoryOnUpdate() {
  const indexToRemove = categories.value.indexOf(categoryOpened.value);
  if (indexToRemove !== -1) {
    categories.value.splice(indexToRemove, 1);
  }
  closeUpdateModal();
}
function updateCategoryHandler() {

  if (/[,;:/\\.]/.test(updateCategoryName.value)) {
    errorUpdateMessage.value = 'Le nom de la catégorie contient un caractère interdit : , ; : / \\';
  } else if (!updateCategoryName.value.trim() || !updateCategoryDescription.value.trim()) {
    errorUpdateMessage.value = "Veuillez remplir tous les champs";
  } else if (categories.value.some(cat => cat.name === updateCategoryName.value && cat.name != updateOldCategoryName.value)) {
    errorUpdateMessage.value = "Le nom de la catégorie existe déjà";
  } else {
    categoryOpened.value.name = updateCategoryName.value;
    categoryOpened.value.description = updateCategoryDescription.value;
    closeUpdateModal();
  }
}
function handleKeyDown(event) {
  if (event.key === 'Tab') {
    event.preventDefault();

    if (step.value == 0) {
      if (document.activeElement.id === 'login') {
        document.getElementById('password').focus();
      } else if (document.activeElement.id === 'password') {
        document.getElementById('confirmPassword').focus();
      } else {
        document.getElementById('login').focus();
      }
    } else if (step.value == 1) {
      //TODO select next color with tab
    } else if (step.value == 2) {
      if (isModalOpen.value == true) {
        if (categoryName.value == '' && document.activeElement.id != 'categoryName') {
          document.getElementById('categoryName').focus();
        } else if (categoryDescription.value == '' && document.activeElement.id != 'categoryDescription') {
          document.getElementById('categoryDescription').focus();
        } else if (document.activeElement.id === 'categoryName') {
          document.getElementById('categoryDescription').focus();
        } else {
          document.getElementById('categoryName').focus();
        }
      } else if (isModalUpdateOpen.value == true) {
        if (updateCategoryName.value == '' && document.activeElement.id != 'updateCategoryName') {
          document.getElementById('updateCategoryName').focus();
        } else if (updateCategoryDescription.value == '' && document.activeElement.id != 'updateCategoryDescription') {
          document.getElementById('updateCategoryDescription').focus();
        } else if (document.activeElement.id === 'updateCategoryName') {
          document.getElementById('updateCategoryDescription').focus();
        } else {
          document.getElementById('updateCategoryName').focus();
        }
      }
    }
  } else if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();

    if (step.value == 0) {
      nextStep0();
    } else if (step.value == 1) {
      nextStep1();
    } else if (step.value === 2) {
      if (isModalOpen.value) {
        event.preventDefault();
        addCategory();
      } else if (isModalUpdateOpen.value) {
        event.preventDefault();
        updateCategoryHandler();
      } else {
        nextStep0();
        nextStep1();
        submitSignupData();
      }
    }
  } else if (event.key === 'Escape') {
    if (isModalUpdateOpen.value == true) {
      closeUpdateModal();
    } else if (isModalOpen.value == true) {
      closeModal();
    }
  } else if (event.key === 'Delete') {
    deleteCategoryOnUpdate();
  }
}
function updateBgColor(newBgColor) {
  bgColor.value = newBgColor;
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
function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}
function toggleConfirmPasswordVisibility() {
  showConfirmPassword.value = !showConfirmPassword.value;
}
function clearError() {
  credentialError.value = '';
}
async function nextStep0() {
  // Handles user registration for the first step, validating username, checking availability, and validating passwords

  // Checks username requirements
  if (!login.value) {
    credentialError.value = 'Veuillez saisir un identifiant';
    return false;
  }
  if (login.value.includes(" ")) {
    credentialError.value = 'L\'identifiant ne doit pas contenir d\'espaces';
    return false;
  }

  // Backend request to check if username is available
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'username': login.value
    }
  };

  try {
    const response = await fetch(`${API_BASE_URL}check_username/`, requestOptions);
    const responseData = await response.json();

    if (responseData.available === false) {
      credentialError.value = 'L\'identifiant est déjà utilisé';
      return false;
    }
  } catch (error) {
    // Show the pop-up
    backgroundColor.value = 'bg-red-300';
    notificationTitle.value = 'Erreur vérification identifiant';
    notificationMessage.value = error;
    displayPopup();
    return false;
  }

  // Checks passwords requirements
  const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()-=_+]+$/;
  const minLength = 8;
  const maxLength = 32;

  if (!password.value.trim()) {
    credentialError.value = 'Veuillez saisir un mot de passe';
    return false;
  }
  else if (!confirmPassword.value.trim()) {
    credentialError.value = 'Veuillez confirmer votre mot de passe';
    return false;
  }
  else if (password.value.length < minLength || password.value.length > maxLength) {
    credentialError.value = 'La longueur du mot de passe doit être entre 8 et 32 caractères';
    return false;
  }
  else if (password.value.includes(" ")) {
    credentialError.value = 'Le mot de passe ne doit pas contenir d\'espaces';
    return false;
  }
  else if (!passwordRegex.test(password.value)) {
    credentialError.value = 'Le mot de passe contient des caractères invalides';
    return false;
  }
  else if (password.value !== confirmPassword.value) {
    credentialError.value = 'Les mots de passe ne correspondent pas';
    return false;
  }

  sessionStorage.setItem('login', login.value);
  sessionStorage.setItem('password', password.value);

  clearError();
  step.value++;
}
function nextStep1() {
  localStorage.setItem('bgColor', bgColor.value);
  localStorage.setItem('theme', 'light');
  step.value++;
}
function goStep0() {
  step.value = 0;
}
function goStep1() {
  step.value = 1;
}
async function goStep2() {
  // go to step 2 from step 0
  const valid = await nextStep0();
  if (valid == false) {
    return;
  }
  nextStep1();
}
function closeModal() {
  isModalOpen.value = false;
}
function addCategory() {

  if (!categoryName.value.trim() || !categoryDescription.value.trim()) {
    errorMessage.value = "Veuillez remplir tous les champs";
  } else if (categories.value.some(cat => cat.name === categoryName.value)) {
    errorMessage.value = "Le nom de la catégorie existe déjà";
  } else if (/[,;:/\\.]/.test(categoryName.value)) {
    errorMessage.value = 'Le nom de la catégorie contient un caractère interdit : , ; : / \\';
  }
  else {
    categories.value.push({
      name: categoryName.value,
      description: categoryDescription.value
    });

    categoryName.value = '';
    categoryDescription.value = '';
    errorMessage.value = '';
    isModalOpen.value = false;
  }
}
async function submitSignupData() {
  try {
    // save categories
    localStorage.setItem('categories', JSON.stringify(categories.value));
    // Registration first part complete
    router.push({ name: 'signup_part2' });
  }
  catch (error) {
    // Show the pop-up
    backgroundColor.value = 'bg-red-300';
    notificationTitle.value = 'Erreur lors de l\'envoi des données';
    notificationMessage.value = error;
    displayPopup();
  }
}
</script>

<script>
export default {
  components: {
    Theme,
    Color,
    XMarkIcon
  },
  data() {
    return {
      logo: require('@/assets/LogoAugmentAI_export4.png')
    };
  }
}
</script>