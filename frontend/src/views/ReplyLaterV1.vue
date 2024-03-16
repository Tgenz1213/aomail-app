<template>
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
      <div
        class="col-span-10 2xl:col-span-6 bg-white rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg xl:h-[93vh] xl:w-[86vw] 2xl:h-[825px] 2xl:w-[1450px]">
        <!-- WORKS FOR 1920*1200px screens <div
        class="col-span-10 2xl:col-span-6 bg-white rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg xl:h-[calc(93vh)] xl:w-[86vw] 2xl:h-[6/7*100vh] 2xl:w-[calc(80vw)]"> -->
        <!-- OLD VALUE w : 1400px or 1424px h : 825px -->
        <div class="flex flex-col h-full divide-y divide-gray-200">
          <div
            class="flex items-center justify-center h-[65px] 2xl:h-[75px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-50">
            <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
            <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">Répondre plus tard</h1>
          </div>
          <div class="flex-grow overflow-y-auto" style="margin-right: 2px;">
            <div class="px-4 py-2 h-full">
              <div v-if="nbr_reply_answer == 0" class="py-2 w-full h-full">
                <div
                  class="flex items-center justify-center w-full h-full rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 text-center"
                  @click="showModal = true">
                  <div class="flex-col">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="w-12 h-12 mx-auto text-gray-400">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M9 15 3 9m0 0 6-6M3 9h12a6 6 0 0 1 0 12h-3" />
                    </svg>
                    <span class="mt-2 block text-sm font-semibold text-gray-900">Aucun mail à répondre plus tard</span>
                  </div>
                </div>
              </div>
              <div v-if="nbr_reply_answer > 0">
                <ul role="list" class="flex flex-col w-full h-full rounded-xl">
                  <li v-if="emails['Important'] && emails['Important'].length > 0"
                    class="py-10 px-8 mt-2 rounded-xl bg-red-100 bg-opacity-50 hover:ring-1 ring-offset-0 ring-red-700 ring-opacity-20">
                    <div class="float-right mt-[-25px] mr-[-10px]">
                      <exclamation-triangle-icon class="w-6 h-6 text-red-500" />
                    </div>
                    <div class="flex">
                      <div class="flex">
                        <span
                          class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-red-400 dark:bg-red-200">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="w-6 h-6 text-white">
                            <path stroke-linecap="round" stroke-linejoin="round"
                              d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                          </svg>
                        </span>
                      </div>
                      <div class="ml-6 flex-grow">
                        <div class="overflow-hidden border-l-4 border-red-500  hover:rounded-l-xl"
                          style="overflow: visible;">
                          <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                            <li v-for="item in emails['Important']" :key="item.id"
                              class="px-6 md:py-2 2xl:py-4 hover:bg-opacity-70 grid grid-cols-10 gap-4 items-center"
                              @mouseover="setHoveredItem(item.id)" @mouseleave="clearHoveredItem">
                              <div class="col-span-8" @click="toggleHiddenParagraph(item.id)">
                                <div class="flex-auto group">
                                  <div class="flex gap-x-4">
                                    <p class="text-sm font-semibold leading-6 text-red-700 dark:text-white">{{ item.name
                                      }}</p>
                                    <div
                                      class="hidden group-hover:block px-2 py-0.5 bg-red-300 text-white text-sm shadow rounded-xl">
                                      <div class="flex gap-x-1 items-center">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                          stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                          <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                                        </svg>
                                        <p>Cliquez pour voir le résumé</p>
                                      </div>
                                    </div>
                                  </div>
                                  <p class="mt-1 text-md text-gray-700 leading-relaxed dark:text-blue-50">{{
    item.description }}</p>
                                </div>
                                <ul v-show="showHiddenParagraphs[item.id]" role="list" class="text-black text-sm/6 pt-2"
                                  :ref="'parentElement' + item.id">
                                  <!-- Potential design update : bg-white shadow rounded-xl -->
                                  <li v-for="detail in item.details" :key="detail.id" class="pl-8"
                                    :ref="'hiddenText' + item.id" :data-text="detail.text">
                                  </li>
                                </ul>
                              </div>
                              <div class="col-span-2">
                                <div class="flex justify-center">
                                  <span class="isolate inline-flex rounded-2xl">
                                    <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                      <div class="relative group">
                                        <div
                                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4 z-40">
                                          Ouvrir
                                        </div>
                                        <button @click="openInNewWindow(item.id_provider)" type="button"
                                          class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                          <eye-icon class="w-5 h-5 text-red-400 group-hover:text-white" />
                                        </button>
                                      </div>
                                    </div>
                                    <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                      <div class="relative group">
                                        <div
                                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                          Répondre
                                        </div>
                                        <button @click="openAnswer(item)" type="button"
                                          class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                          <arrow-uturn-left-icon class="w-5 h-5 text-red-400 group-hover:text-white" />
                                        </button>
                                      </div>
                                    </div>
                                    <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                      <div class="relative group">
                                        <div
                                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-8">
                                          Supprimer
                                        </div>
                                        <button type="button"
                                          class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                          <TrashIcon @click.stop="deleteEmail(item.id)"
                                            class="w-5 h-5 text-red-400 group-hover:text-white" />
                                        </button>
                                      </div>
                                    </div>
                                    <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                      <div class="relative group">
                                        <div v-if="showTooltip"
                                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-20 w-[185px]">
                                          Actions supplémentaires
                                        </div>
                                        <Menu as="div" class="relative inline-block text-left">
                                          <div>
                                            <MenuButton @click="toggleTooltip"
                                              class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-red-400 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                              <ellipsis-horizontal-icon
                                                class="w-5 h-5 group-hover:text-white text-red-400 group-active:text-red-400 group-focus:text-red focus:text-red-400" />
                                            </MenuButton>
                                          </div>
                                          <transition enter-active-class="transition ease-out duration-100"
                                            enter-from-class="transform opacity-0 scale-95"
                                            enter-to-class="transform opacity-100 scale-100"
                                            leave-active-class="transition ease-in duration-75"
                                            leave-from-class="transform opacity-100 scale-100"
                                            leave-to-class="transform opacity-0 scale-95">
                                            <MenuItems v-show="isMenuOpen"
                                              class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none">
                                              <div class="py-1">
                                                <div v-if="item.rule">
                                                  <MenuItem v-slot="{ active }">
                                                  <a @click.prevent="openRuleEditor(item.rule_id)" href="#"
                                                    :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                    <span class="flex gap-x-2 items-center">
                                                      <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                        viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                                        class="w-4 h-4">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                          d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                      </svg>
                                                      <span>Changer la règle</span>
                                                    </span>
                                                  </a>
                                                  </MenuItem>
                                                </div>
                                                <div v-else>
                                                  <MenuItem v-slot="{ active }">
                                                  <a @click.prevent="openNewRule(item.name, item.email)" href="#"
                                                    :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                    <span class="flex gap-x-2 items-center">
                                                      <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                        viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                                        class="w-4 h-4">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                          d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                      </svg>
                                                      <span>Créer une règle</span>
                                                    </span>
                                                  </a>
                                                  </MenuItem>
                                                </div>
                                              </div>
                                            </MenuItems>
                                          </transition>
                                        </Menu>
                                      </div>
                                    </div>
                                    <!--
                                          <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                              <div class="relative group">
                                                  <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-10">
                                                      Paramétrer
                                                  </div>
                                                  <Menu as="div" class="relative inline-block text-left">
                                                      <div>
                                                          <MenuButton @click="toggleTooltip" class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-blue-400 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                                              <ellipsis-horizontal-icon class="w-5 h-5 group-hover:text-white text-blue-400 group-active:text-blue-400 group-focus:text-red focus:text-blue-400" />
                                                          </MenuButton>
                                                      </div>
                                                      <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                                                      <MenuItems v-show="isMenuOpen" class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none">
                                                          <div class="py-1">
                                                              <div v-if="item.rule">
                                                                  <MenuItem v-slot="{ active }">
                                                                      <a @click.prevent="openRuleEditor(item.rule_id)" href="#" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                          <span class="flex gap-x-2 items-center">
                                                                              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                                                                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                                              </svg>
                                                                              <span>Changer la règle</span>
                                                                          </span>
                                                                      </a>
                                                                  </MenuItem>
                                                              </div>
                                                              <div v-else>
                                                                  <MenuItem v-slot="{ active }">
                                                                      <a @click.prevent="openNewRule(item.name, item.email)" href="#" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                          <span class="flex gap-x-2 items-center">
                                                                              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                                                                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                                              </svg>
                                                                              <span>Créer une règle</span>
                                                                          </span>
                                                                      </a>
                                                                  </MenuItem>
                                                              </div>
                                                          </div>
                                                          <div class="py-1">
                                                          <MenuItem v-slot="{ active }">
                                                              <a @click.prevent="markEmailReplyLater(item.id)" href="#" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                  <span class="flex gap-x-2 items-center">
                                                                      <svg class="w-4 h-4" viewBox="0 0 28 28" version="1.1" stroke="currentColor" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                                                                          <path d="M13.435,17.391l-6.783,-6.782m0,0l6.783,-6.783m-6.783,6.783l13.565,0c3.721,0 6.783,3.061 6.783,6.782c0,3.721 -3.062,6.783 -6.783,6.783l-3.391,0" style="fill:none;stroke:#000;stroke-width:1.7px;"/><path d="M7.783,17.391l-6.783,-6.782m0,0l6.783,-6.783" style="fill:none;stroke:#000;stroke-width:1.7px;"/>
                                                                      </svg>
                                                                      <span>Répondre plus tard</span>
                                                                  </span>
                                                              </a>
                                                          </MenuItem>
                                                          </div>
                                                      </MenuItems>
                                                      </transition>
                                                  </Menu>
                                              </div>
                                          </div>-->
                                  </span>
                                </div>
                              </div>
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </li>
                  <li v-if="emails['Information'] && emails['Information'].length > 0"
                    class="py-10 px-8 mt-2 rounded-xl bg-blue-100 bg-opacity-50 hover:ring-1 ring-offset-0 ring-blue-700 ring-opacity-20">
                    <!-- ring-1 ring-blue-700 ring-opacity-20 -->
                    <div class="float-right mt-[-25px] mr-[-10px]">
                      <information-circle-icon class="w-6 h-6 text-blue-500" />
                    </div>
                    <div class="flex">
                      <div class="flex">
                        <span
                          class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-blue-500 dark:bg-blue-200">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="w-6 h-6 text-white">
                            <path stroke-linecap="round" stroke-linejoin="round"
                              d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                          </svg>
                        </span>
                        <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-blue-800" />-->
                      </div>
                      <div class="ml-6 flex-grow">
                        <div class="overflow-hidden border-l-4 hover:rounded-l-xl border-blue-300"
                          style="overflow: visible;">
                          <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                            <li v-for="item in emails['Information']" :key="item.id"
                              class="px-6 md:py-2 2xl:py-4 hover:bg-opacity-70 dark:hover:bg-blue-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center"
                              @mouseover="setHoveredItem(item.id)" @mouseleave="clearHoveredItem">
                              <div class="col-span-8" @click="toggleHiddenParagraph(item.id)">
                                <div class="flex-auto group">
                                  <div class="flex gap-x-4">
                                    <p class="text-sm font-semibold leading-6 text-blue-800 dark:text-white">{{
    item.name
  }}</p>
                                    <div
                                      class="hidden group-hover:block px-2 py-0.5 bg-blue-300 text-white text-sm shadow rounded-xl">
                                      <div class="flex gap-x-1 items-center">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                          stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                          <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                                        </svg>
                                        <p>Cliquez pour voir le résumé</p>
                                      </div>
                                    </div>
                                  </div>
                                  <p class="mt-1 text-md text-gray-700 leading-relaxed dark:text-blue-50">{{
      item.description }}</p>
                                </div>
                                <ul v-show="showHiddenParagraphs[item.id]" role="list" class="text-black text-sm/6 pt-2"
                                  :ref="'parentElement' + item.id">
                                  <!-- Potential design update : bg-white shadow rounded-xl -->
                                  <li v-for="detail in item.details" :key="detail.id" class="pl-8"
                                    :ref="'hiddenText' + item.id" :data-text="detail.text">
                                  </li>
                                </ul>
                              </div>
                              <div class="col-span-2">
                                <div class="flex justify-center">
                                  <span class="isolate inline-flex rounded-2xl">
                                    <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                      <div class="relative group">
                                        <div
                                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4 z-40">
                                          Ouvrir
                                        </div>
                                        <button @click="openInNewWindow(item.id_provider)" type="button"
                                          class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                          <eye-icon class="w-5 h-5 text-blue-400 group-hover:text-white" />
                                        </button>
                                      </div>
                                    </div>
                                    <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                      <div class="relative group">
                                        <div
                                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                          Répondre
                                        </div>
                                        <button @click="openAnswer(item)" type="button"
                                          class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                          <arrow-uturn-left-icon class="w-5 h-5 text-blue-400 group-hover:text-white" />
                                        </button>
                                      </div>
                                    </div>
                                    <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                      <div class="relative group">
                                        <div
                                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-8">
                                          Supprimer
                                        </div>
                                        <button type="button"
                                          class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                          <TrashIcon @click.stop="deleteEmail(item.id)"
                                            class="w-5 h-5 text-blue-400 group-hover:text-white" />
                                        </button>
                                      </div>
                                    </div>
                                    <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                      <div class="relative group">
                                        <div v-if="showTooltip"
                                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-20 w-[185px]">
                                          Actions supplémentaires
                                        </div>
                                        <Menu as="div" class="relative inline-block text-left">
                                          <div>
                                            <MenuButton @click="toggleTooltip"
                                              class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-blue-400 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                              <ellipsis-horizontal-icon
                                                class="w-5 h-5 group-hover:text-white text-blue-400 group-active:text-blue-400 group-focus:text-red focus:text-blue-400" />
                                            </MenuButton>
                                          </div>
                                          <transition enter-active-class="transition ease-out duration-100"
                                            enter-from-class="transform opacity-0 scale-95"
                                            enter-to-class="transform opacity-100 scale-100"
                                            leave-active-class="transition ease-in duration-75"
                                            leave-from-class="transform opacity-100 scale-100"
                                            leave-to-class="transform opacity-0 scale-95">
                                            <MenuItems v-show="isMenuOpen"
                                              class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none">
                                              <div class="py-1">
                                                <div v-if="item.rule">
                                                  <MenuItem v-slot="{ active }">
                                                  <a @click.prevent="openRuleEditor(item.rule_id)" href="#"
                                                    :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                    <span class="flex gap-x-2 items-center">
                                                      <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                        viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                                        class="w-4 h-4">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                          d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                      </svg>
                                                      <span>Changer la règle</span>
                                                    </span>
                                                  </a>
                                                  </MenuItem>
                                                </div>
                                                <div v-else>
                                                  <MenuItem v-slot="{ active }">
                                                  <a @click.prevent="openNewRule(item.name, item.email)" href="#"
                                                    :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                    <span class="flex gap-x-2 items-center">
                                                      <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                        viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                                        class="w-4 h-4">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                          d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                      </svg>
                                                      <span>Créer une règle</span>
                                                    </span>
                                                  </a>
                                                  </MenuItem>
                                                </div>
                                              </div>
                                            </MenuItems>
                                          </transition>
                                        </Menu>
                                      </div>
                                    </div>
                                    <!--
                                          <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                              <div class="relative group">
                                                  <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-10">
                                                      Paramétrer
                                                  </div>
                                                  <Menu as="div" class="relative inline-block text-left">
                                                      <div>
                                                          <MenuButton @click="toggleTooltip" class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-blue-400 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                                              <ellipsis-horizontal-icon class="w-5 h-5 group-hover:text-white text-blue-400 group-active:text-blue-400 group-focus:text-red focus:text-blue-400" />
                                                          </MenuButton>
                                                      </div>
                                                      <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                                                      <MenuItems v-show="isMenuOpen" class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none">
                                                          <div class="py-1">
                                                              <div v-if="item.rule">
                                                                  <MenuItem v-slot="{ active }">
                                                                      <a @click.prevent="openRuleEditor(item.rule_id)" href="#" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                          <span class="flex gap-x-2 items-center">
                                                                              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                                                                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                                              </svg>
                                                                              <span>Changer la règle</span>
                                                                          </span>
                                                                      </a>
                                                                  </MenuItem>
                                                              </div>
                                                              <div v-else>
                                                                  <MenuItem v-slot="{ active }">
                                                                      <a @click.prevent="openNewRule(item.name, item.email)" href="#" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                          <span class="flex gap-x-2 items-center">
                                                                              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                                                                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                                              </svg>
                                                                              <span>Créer une règle</span>
                                                                          </span>
                                                                      </a>
                                                                  </MenuItem>
                                                              </div>
                                                          </div>
                                                          <div class="py-1">
                                                          <MenuItem v-slot="{ active }">
                                                              <a @click.prevent="markEmailReplyLater(item.id)" href="#" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                  <span class="flex gap-x-2 items-center">
                                                                      <svg class="w-4 h-4" viewBox="0 0 28 28" version="1.1" stroke="currentColor" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                                                                          <path d="M13.435,17.391l-6.783,-6.782m0,0l6.783,-6.783m-6.783,6.783l13.565,0c3.721,0 6.783,3.061 6.783,6.782c0,3.721 -3.062,6.783 -6.783,6.783l-3.391,0" style="fill:none;stroke:#000;stroke-width:1.7px;"/><path d="M7.783,17.391l-6.783,-6.782m0,0l6.783,-6.783" style="fill:none;stroke:#000;stroke-width:1.7px;"/>
                                                                      </svg>
                                                                      <span>Répondre plus tard</span>
                                                                  </span>
                                                              </a>
                                                          </MenuItem>
                                                          </div>
                                                      </MenuItems>
                                                      </transition>
                                                  </Menu>
                                              </div>
                                          </div>-->
                                  </span>
                                </div>
                              </div>
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </li>
                  <div v-if="emails['Useless'] && emails['Useless'].length > 0"
                    class="py-10 px-8 mt-2 rounded-xl bg-gray-100 hover:border border-gray-700 border-opacity-20 w-full">
                    <div class="float-right mt-[-25px] mr-[-10px]">
                      <TrashIcon class="w-6 h-6 text-gray-500" />
                    </div>
                    <div class="flex">
                      <div class="flex">
                        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-500">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="w-6 h-6 text-white">
                            <path stroke-linecap="round" stroke-linejoin="round"
                              d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                          </svg>
                        </span>
                        <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-blue-800" />-->
                      </div>
                      <div class="ml-6 flex-grow">
                        <div class="overflow-hidden border-l-4 hover:rounded-l-xl border-gray-500"
                          style="overflow: visible;">
                          <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                            <li v-for="item in emails['Useless']" :key="item.id"
                              class="px-6 md:py-2 2xl:py-4 hover:bg-opacity-70 grid grid-cols-10 gap-4 items-center"
                              @mouseover="setHoveredItem(item.id)" @mouseleave="clearHoveredItem">
                              <div class="col-span-8" @click="toggleHiddenParagraph(item.id)">
                                <div class="flex-auto group">
                                  <div class="flex gap-x-4">
                                    <p class="text-sm font-semibold leading-6 text-gray-800">{{ item.name }}</p>
                                    <div
                                      class="hidden group-hover:block px-2 py-0.5 bg-gray-500 text-white text-sm shadow rounded-xl">
                                      <div class="flex gap-x-1 items-center">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                          stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                          <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                                        </svg>
                                        <p>Cliquez pour voir le résumé</p>
                                      </div>
                                    </div>
                                  </div>
                                  <p class="mt-1 text-md text-gray-700 leading-relaxed dark:text-blue-50">{{
    item.description }}</p>
                                </div>
                                <ul v-show="showHiddenParagraphs[item.id]" role="list" class="text-black text-sm/6 pt-2"
                                  :ref="'parentElement' + item.id">
                                  <!-- Potential design update : bg-white shadow rounded-xl -->
                                  <li v-for="detail in item.details" :key="detail.id" class="pl-8"
                                    :ref="'hiddenText' + item.id" :data-text="detail.text">
                                  </li>
                                </ul>
                              </div>
                              <div class="col-span-2">
                                <div class="flex justify-center">
                                  <span class="isolate inline-flex rounded-2xl">
                                    <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                      <div class="relative group">
                                        <div
                                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4 z-40">
                                          Ouvrir
                                        </div>
                                        <button @click="openInNewWindow(item.id_provider)" type="button"
                                          class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                          <eye-icon class="w-5 h-5 text-gray-500 group-hover:text-white" />
                                        </button>
                                      </div>
                                    </div>
                                    <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                      <div class="relative group">
                                        <div
                                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                          Répondre
                                        </div>
                                        <button @click="openAnswer(item)" type="button"
                                          class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                          <arrow-uturn-left-icon class="w-5 h-5 text-gray-500 group-hover:text-white" />
                                        </button>
                                      </div>
                                    </div>
                                    <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                      <div class="relative group">
                                        <div
                                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-8">
                                          Supprimer
                                        </div>
                                        <button type="button"
                                          class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                          <TrashIcon @click.stop="deleteEmail(item.id)"
                                            class="w-5 h-5 text-gray-500 group-hover:text-white" />
                                        </button>
                                      </div>
                                    </div>
                                    <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                      <div class="relative group">
                                        <div v-if="showTooltip"
                                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-20 w-[185px]">
                                          Actions supplémentaires
                                        </div>
                                        <Menu as="div" class="relative inline-block text-left">
                                          <div>
                                            <MenuButton @click.stop="toggleTooltip"
                                              class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-gray-500 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                              <ellipsis-horizontal-icon
                                                class="w-5 h-5 group-hover:text-white text-gray-500 group-active:text-gray-500 group-focus:text-red focus:text-gray-500" />
                                            </MenuButton>
                                          </div>
                                          <transition enter-active-class="transition ease-out duration-100"
                                            enter-from-class="transform opacity-0 scale-95"
                                            enter-to-class="transform opacity-100 scale-100"
                                            leave-active-class="transition ease-in duration-75"
                                            leave-from-class="transform opacity-100 scale-100"
                                            leave-to-class="transform opacity-0 scale-95">
                                            <MenuItems v-show="isMenuOpen"
                                              class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none">
                                              <div class="py-1">
                                                <div v-if="item.rule">
                                                  <MenuItem v-slot="{ active }">
                                                  <a @click.prevent="openRuleEditor(item.rule_id)" href="#"
                                                    :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                    <span class="flex gap-x-2 items-center">
                                                      <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                        viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                                        class="w-4 h-4">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                          d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                      </svg>
                                                      <span>Changer la règle</span>
                                                    </span>
                                                  </a>
                                                  </MenuItem>
                                                </div>
                                                <div v-else>
                                                  <MenuItem v-slot="{ active }">
                                                  <a @click.prevent="openNewRule(item.name, item.email)" href="#"
                                                    :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                    <span class="flex gap-x-2 items-center">
                                                      <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                        viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                                        class="w-4 h-4">
                                                        <path stroke-linecap="round" stroke-linejoin="round"
                                                          d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                      </svg>
                                                      <span>Créer une règle</span>
                                                    </span>
                                                  </a>
                                                  </MenuItem>
                                                </div>
                                              </div>
                                            </MenuItems>
                                          </transition>
                                        </Menu>
                                      </div>
                                    </div>
                                  </span>
                                </div>
                              </div>
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <ModalSeeRule :isOpen="showModal" @update:isOpen="updateModalStatus" :emailSenders="emailSenders"
    :categories="categories" />
</template>

<script>
import { onMounted, ref } from 'vue';
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';
import { fetchWithToken, getBackgroundColor } from '../router/index.js';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue';
import { API_BASE_URL } from '@/main';
import {
  //ChatBubbleOvalLeftEllipsisIcon,
  TrashIcon,
  ArrowUturnLeftIcon,
  EllipsisHorizontalIcon,
  EyeIcon,
  InformationCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline';

export default {
  components: {
    Navbar,
    Navbar2,
    MenuItem,
    MenuItems,
    Menu,
    MenuButton,
    TrashIcon,
    ArrowUturnLeftIcon,
    EllipsisHorizontalIcon,
    EyeIcon,
    InformationCircleIcon,
    ExclamationTriangleIcon
  },
  setup() {
    // Main variables
    const bgColor = ref('');
    const answerLaterEmails = ref([]);
    const emails = ref({});
    const nbr_reply_answer = ref(0);

    // Mounted lifecycle hook
    onMounted(() => {

      getBackgroundColor();
      bgColor.value = localStorage.getItem('bgColor');
      fetchAnswerLaterEmails();
    });

    // To fetch the email to reply later
    async function fetchAnswerLaterEmails() {
      try {
        const data = await fetchWithToken(`${API_BASE_URL}api/get_answer_later_emails/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        console.log("DATA", data);
        emails.value = data; // Assuming emails is a reactive variable
        console.log("Length", Object.keys(emails.value).length);
        nbr_reply_answer.value = Object.keys(emails.value).length; // Assuming nbr_reply_answer is a reactive variable
        answerLaterEmails.value = data; // Update the reactive variable with the fetched emails
      } catch (error) {
        console.error("Error fetching answer-later emails:", error.message);
      }
    }

    return {
      // Expose variables/functions to the template if needed
      bgColor,
      answerLaterEmails,
      emails,
      nbr_reply_answer,
    };
  },
  methods: {
    toggleHiddenParagraph(index) {
      console.log("Item ID:", index)
      console.log("All refs:", this.$refs)
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
    openRuleEditor(ruleId) {
      if (ruleId) {
        this.$router.push({ name: 'rules', query: { id_rule: ruleId, edit_rule: true } });
      }
    },
    openNewRule(ruleName, ruleEmail) {
      if (ruleName && ruleEmail) {
        this.$router.push({ name: 'rules', query: { rule_name: ruleName, rule_email: ruleEmail, edit_rule: false } });
      }
    },
    setHoveredItem(id) {
      this.hoveredItemId = id;
    },
    clearHoveredItem() {
      this.hoveredItemId = null;
    },
    toggleTooltip() {
      this.showTooltip = false;
      this.isDropdownOpen = true;
    },
    openInNewWindow(id_provider) {
      console.log("EMAIL", id_provider);
      const gmailBaseUrl = 'https://mail.google.com/mail/u/0/#inbox/';
      // Construct the URL with the Gmail message ID
      const urlToOpen = `${gmailBaseUrl}${id_provider}`;

      window.open(urlToOpen, '_blank');
    },
    async openAnswer(email) {
      console.log("EMAIL", email.id_provider);

      // Define the API endpoint URL
      const url = `http://localhost:9000/MailAssistant/api/get_mail_by_id?email_id=${email.id_provider}`;

      try {
        const data = await fetchWithToken(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'email': localStorage.getItem('email')
          }
        });
        console.log("Received data:", data);
        this.$router.push({
          name: 'answer',
          query: {
            subject: JSON.stringify(data.email.subject),
            cc: JSON.stringify(data.email.cc),
            bcc: JSON.stringify(data.email.bcc),
            decoded_data: JSON.stringify(data.email.decoded_data),
            email: JSON.stringify(email.email),
            id_provider: JSON.stringify(email.id_provider),
            details: JSON.stringify(email.details)
          }
        });
      } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
      }
    },
    async deleteEmail(emailId) {
      try {
        const response = await fetchWithToken(`http://localhost:9000/MailAssistant/user/emails/${emailId}/delete/`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          }
        });

        console.log("RESPONSE ------------> ", response);
        console.log("EMAIL ---------------> ", this.emails);

        if (response.message) {
          console.log("Email deleted successfully", response);
          this.nbr_reply_answer -= 1;
          this.deleteEmailFromState(emailId);
        } else {
          console.error('Failed to delete email', response);
        }
      } catch (error) {
        console.error('Error in deleteEmail:', error.message);
      }
    },
    deleteEmailFromState(emailId) {
      // Iterate over each category in the emails object
      for (const category in this.emails) {
        if (Object.prototype.hasOwnProperty.call(this.emails, category)) {
          // Directly iterate over the array of emails in the category
          const emailIndex = this.emails[category].findIndex(email => email.id === emailId);
          if (emailIndex !== -1) {
            // Email found, delete it from the array
            this.emails[category].splice(emailIndex, 1);
            return; // Stop the function as we've found and deleted the email
          }
        }
      }
    }
  },
  data() {
    return {
      showHiddenParagraphs: {},
      animationTriggered: [false, false, false],
      hoveredItemId: null,
      showTooltip: true,
      isDropdownOpen: false,
      isMenuOpen: true,
    }
  }
};
</script>