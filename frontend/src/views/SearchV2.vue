<template>
  <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
    :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" />
  <div class="flex flex-col justify-center items-center h-screen" :class="bgColor">
    <div class="flex h-full w-full">

      <!-- navbar-->
      <div class="w-[90px] bg-white ring-1 shadow-sm ring-black ring-opacity-5 2xl:w-[100px]">
        <navbar></navbar>
      </div>

      <div id="firstMainColumn"
        class="flex flex-col bg-gray-50 lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[700px]">
        <!--xl:h-[750px] xl:w-[625px] => 26/12/2023 DATA SAVE : xl:h-[95vh] xl:w-[43vw] 2xl:h-[825px] 2xl:w-[700px] -->
        
       <!-- Title --> 
        <div
          class="flex items-center justify-center h-[65px] 2xl:h-[80px]">
          <div class="flex gap-x-3 items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                stroke="currentColor" class="w-6 h-6 2xl:w-7 2xl:h-7">
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
            </svg>
            <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ $t('constants.aiAssistant') }}</h1>
          </div>
        </div>

        <!-- AO AI Assistant -->
        <div class="flex flex-1 flex-col divide-y overflow-y-auto">
          <div class="overflow-y-auto flex-1" style="margin-right: 2px;" ref="scrollableDiv">
            <div class="px-10 py-4 2xl:px-13.5 2xl:py-6">
              <div class="flex-grow">
                <div id="AIContainer">
                </div>
              </div>
            </div>
          </div>
          <div class="flex flex-col h-[22vh] 2xl:h-[23vh]">
            <textarea id="dynamicTextarea"
                @input="adjustHeight" v-model="textareaValue"
                class="overflow-y-hidden pt-4 pl-6 flex-1 w-full border-transparent bg-transparent text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 focus:border-transparent focus:bg-transparent focus:ring-0 2xl:pt-5 2xl:pl-7 2xl:text-base"
                placeholder="Instruction">
            </textarea>
            <div v-if="stepcontainer == 0" class="flex justify-end m-3 2xl:m-5">
              <div class="flex space-x-2 items-center">
                <!-- TO KEEP : ONLY IF OLD MAIL NEEDS TO BE ACTIVATED (ask user before implementation) 
                <div class="relative">
                  <select
                    v-model="selectedOption"
                    @change="updateOption"
                    class="form-select appearance-none block w-full h-[38px] 2xl:h-[46px] px-1 pr-6 rounded-md bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white focus:bg-gray-900 focus:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900 text-center text-sm 2xl:text-base">
                    <option :value="$t('searchPage.choiceAomail')">{{ $t('searchPage.choiceAomail') }}</option>
                    <option :value="$t('searchPage.choiceOldMailDisplay')">{{ $t('searchPage.choiceOldMail') }}</option>
                  </select>
                </div>-->
                <div class="flex items-center">
                  <button type="button" @click="handleAIClick" class="h-[38px] 2xl:h-[46px] w-[80px] 2xl:w-[100px] rounded-md bg-gray-700 px-2 text-sm 2xl:text-base text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">Envoyer</button> 
                </div>
              </div>
            </div>
            <div v-else class="flex justify-end m-3 2xl:m-5">
              <button type="button" @click="handleAIClick" class="2xl:w-[100px] w-[80px] rounded-md bg-gray-700 px-5.5 py-2.5 2xl:px-6.5 2xl:py-3 2xl:text-base text-sm text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">Envoyer</button> 
            </div>
          </div>
        </div>

      </div>

      <div id="secondMainColumn" 
      class="flex flex-col bg-white lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[700px] overflow-y-auto">

        <!--xl:h-[695px] xl:w-[560px]-->

        <!--titre -->
        <div class="flex items-center h-[65px] justify-center lg:py-5 2xl:h-[80px] min-h-6">
          <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
          <div class="flex gap-x-3 items-center ">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                stroke-width="1" stroke="currentColor" class="w-6 h-6 2xl:w-7 2xl:h-7">
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672ZM12 2.25V4.5m5.834.166-1.591 1.591M20.25 10.5H18M7.757 14.743l-1.59 1.59M6 10.5H3.75m4.007-4.243-1.59-1.59" />
            </svg>
            <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ $t('constants.manualSearch') }}</h1> 
          </div>
        </div>

        <div class="flex-1 flex flex-col w-full px-6 pt-2 mb-4">

            
              <!--??? -->
              <div class="flex space-x-1 items-center mb-4">
              <!--  <magnifying-glass-icon class="w-4 h-4" />
                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">{{
                  $t('Search_vue.manual_Search') }}</label>-->
              </div>

               <!-- searchbar and buttons -->
               <div class="flex space-x-1 2xl:space-x-2 items-stretch w-full mb-4">

                <!-- searchbar and buttons old version. If picke has to be fixed !!!-->
                <!--<div class="relative flex-grow">
                  <SearchbarV2 @input="updateSearchQuery" class="h-[5px]"></SearchbarV2>
                </div>-->

                <!-- searchbar and buttons old version. If picke has to be fixed !!!-->
                <!-- <div class="relative w-full">
                    <div class="absolute inset-y-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 ml-2 2xl:ml-3 items-center">
                    <magnifying-glass-icon class="w-4 h-4 pointer-events-none 2xl:w-5 2xl:h-5" />
                    <label for="search" class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none 2xl:text-base">
                    {{ $t('searchPage.searchPlaceholder') }}
                    </label>
                    </div>
                  <Combobox as="div">
                  <ComboboxInput id="search" 
                  class="w-full h-10 2xl:h-11 rounded-md border-0 bg-white py-2 pl-10 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 2xl:py-3 2xl:pl-14 2xl:pr-14 2xl:text-base text-center" />
                  </Combobox>
                </div>-->

                <div class="relative w-full">
                  <div class="flex w-full">
                    <div class="relative flex-grow">
                      <div v-if="!isFocused && !inputValue"
                        class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 2xl:ml-3">
                        <magnifying-glass-icon class="w-4 h-4 pointer-events-none 2xl:w-5 2xl:h-5" />
                        <label for="search" class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none 2xl:text-base">
                          {{ $t('searchPage.searchPlaceholder') }}
                        </label>
                      </div>
                      <input id="searchInput" v-model="inputValue" type="text"
                        class="block rounded-l-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 h-10 2xl:h-11 flex-1 border-0 bg-transparent py-2 pl-3 text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 w-full z-20 relative 2xl:py-3 2xl:pl-4 2xl:text-base"
                        @focus="handleFocusSearch" @blur="handleBlur2($event)"
                        @input="handleInputUpdateSearch"
                        @change="query = $event.target.value" />
                    </div>

                    <div class="relative">
                      <button type="button" class="group w-full h-full bg-gray-100 rounded-r-md p-2 text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 flex items-center justify-center 2xl:px-3 2xl:py-3 ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm" @click="Hide_filtres()">
                        <svg class="w-6 h-5 text-gray-400 group-hover:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" stroke="none" viewBox="0 0 24 24">
                          <path d="M10.83 5a3.001 3.001 0 0 0-5.66 0H4a1 1 0 1 0 0 2h1.17a3.001 3.001 0 0 0 5.66 0H20a1 1 0 1 0 0-2h-9.17ZM4 11h9.17a3.001 3.001 0 0 1 5.66 0H20a1 1 0 1 1 0 2h-1.17a3.001 3.001 0 0 1-5.66 0H4a1 1 0 1 1 0-2Zm1.17 6H4 a1 1 0 1 0 0 2h1.17a3.001 3.001 0 0 0 5.66 0H20a1 1 0 1 0 0-2h-9.17a3.001 3.001 0 0 0-5.66 0Z"/>
                        </svg>
                      </button>
                    </div>

                    <!-- TO KEEP : ONLY IF OLD MAIL NEEDS TO BE ACTIVATED (ask user before implementation) 
                    <div class="relative inline-block dropdown-container">
                      <button
                        type="button"
                        @click="toggleDropdown"
                        class="inline-flex justify-center items-center h-full rounded-r-md border border-l-0 border-gray-300 shadow-sm px-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-inset focus:ring-gray-500 focus:border-gray-500 relative"
                      >
                        {{ selectedOption }}
                        <chevron-down-icon class="ml-1 h-4 w-4" />
                      </button>

                      <div v-if="isOpen" class="absolute right-0 mt-2 w-32 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-10">
                        <div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
                          <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem" @click="selectOption($t('searchPage.choiceAomail'))">{{ $t('searchPage.choiceAomail') }}</a>
                          <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem" @click="selectOption($t('searchPage.choiceOldMailDisplay'))">{{ $t('searchPage.choiceOldMail') }}</a>
                        </div>
                      </div>
                    </div>-->
                  </div>
                </div>              
                            

                <!--<div class="flex-grow w-full h-full">
                  <div class="relative flex flex-grow items-stretch h-full">
                    <input v-model="query"
                      type="text"
                      :placeholder="$t('searchPage.searchPlaceholder')"
                      autocomplete="given-name"
                      class="block w-full h-full rounded-md border-0 bg-white pl-10 py-2 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 2xl:py-3 2xl:pl-14 2xl:pr-14 2xl:text-base"
                      style="vertical-align: middle;">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <magnifying-glass-icon class="w-4 h-4 pointer-events-none 2xl:w-5 2xl:h-5" />
                    </div>
                  </div>
                </div>-->

                <div class="flex-grow h-full">
                  <button type="button" @click="searchEmails"
                    class="w-full h-full bg-gray-700 rounded-md px-2 2xl:px-4 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center justify-between 2xl:px-7 2xl:text-lg">
                    {{ $t('searchPage.searchButton') }}
                    <magnifying-glass-icon class="w-4 2xl:w-5" />
                  </button>
                </div>
              </div>

              <!-- filters -->
              <div class="flex space-x-2 hidden pr-2 w-full mb-4" id="filtres">
              <div class="flex flex-col gap-4">


                <div class="flex gap-4 gap-y-2 w-full flex-wrap">

                     <!-- Premier input Combobox toAddressesSelected -->
                      <div class="flex-1 min-w-[150px] mt-2 relative">
                        <Combobox as="div" v-model="selectedPerson">
                          <div class="relative flex items-center w-full">
                            <user-icon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                            <ComboboxInput
                              class="w-full rounded-md border-0 bg-white py-3 pl-10 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 truncate"
                              @input="query = $event.target.value"
                              :display-value="(person) => person?.username"
                              placeholder="À"
                              style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;"
                            />
                            <ComboboxButton class="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center focus:outline-none">
                              <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </ComboboxButton>
                          </div>
                          <ComboboxOptions v-if="filteredPeople.length > 0"
                            class="absolute z-10 max-h-60  w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm left-0 right-0">
                            <ComboboxOption v-for="person in filteredPeople" :value="person" :key="person" as="template"
                              v-slot="{ active, selected }">
                              <li @click="toggleSelection(person)"
                                :class="['relative cursor-default select-none py-2 pl-3 pr-9', active ? 'bg-gray-500 text-white' : 'text-gray-900']">
                                <div class="flex">
                                  <span :class="['truncate', selected && 'font-semibold']">
                                    {{ person.username }}
                                  </span>
                                  <span
                                    :class="['ml-2 truncate hidden text-gray-500', active ? 'text-indigo-200' : 'text-gray-500']">
                                    &lt;{{ person.email }}&gt;
                                  </span>
                                </div>
                                <span v-if="selected"
                                  :class="['absolute inset-y-0 right-0 flex items-center pr-4', active ? 'text-white' : 'text-gray-500']">
                                  <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                </span>
                              </li>
                            </ComboboxOption>
                          </ComboboxOptions>
                        </Combobox>
                      </div>

                       <!-- Deuxième input Listbox  TODO : Type de pièce jointe-->
                       <div class="flex-1 min-w-[150px] mt-2">
                          <Listbox as="div" v-model="attachmentSelected">
                              <div class="relative">
                                  <ListboxButton
                                      class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-12 text-left flex items-center text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6">
                                      <adjustments-horizontal-icon class="w-5 h-5 mr-2 mt-2 mb-2 text-gray-400" />
                                      <span class="block truncate text-gray-700">
                                        {{ attachmentSelected ? attachmentSelected.name : $t('searchPage.attachmentSelectedPlaceholder') }}

                                      </span>
                                      <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                          <ChevronUpDownIcon class="h-5 w-5 text-gray-400 mt-2 mb-2" aria-hidden="true" />
                                      </span>
                                  </ListboxButton>
                                  <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
                                      <ListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                                          <ListboxOption as="template" v-for="type in attachmentTypes" :key="type.extension" :value="type" v-slot="{ active, attachmentSelected }">
                                              <li :class="[active ? 'bg-gray-500 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                                                  <span :class="[attachmentSelected ? 'font-semibold' : 'font-normal', 'block truncate ml-7 mr-2']">
                                                      {{ type.name }} {{ type.extension }}
                                                  </span>
                                                  <span v-if="attachmentSelected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                                      <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                                  </span>
                                              </li>
                                          </ListboxOption>
                                      </ListboxOptions>
                                  </transition>
                              </div>
                          </Listbox>
                      </div>

                      <!-- Troisième input Combobox  fromAddressesSelected -->
                      <div class="flex-1 min-w-[150px] mt-2 relative">
                        <Combobox as="div" v-model="selectedPerson">
                          <div class="relative flex items-center w-full">
                            <user-icon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                            <ComboboxInput
                              class="w-full rounded-md border-0 bg-white py-3 pl-10 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 truncate"
                              @input="query = $event.target.value"
                              :display-value="(person) => person?.username"
                              placeholder="De"
                              style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;"
                            />
                            <ComboboxButton class="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center focus:outline-none">
                              <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </ComboboxButton>
                          </div>
                          <ComboboxOptions v-if="filteredPeople.length > 0"
                            class="absolute z-10 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm left-0 right-0">
                            <ComboboxOption v-for="person in filteredPeople" :value="person" :key="person" as="template"
                              v-slot="{ active, selected }">
                              <li @click="toggleSelection(person)"
                                :class="['relative cursor-default select-none py-2 pl-3 pr-9', active ? 'bg-gray-500 text-white' : 'text-gray-900']">
                                <div class="flex">
                                  <span :class="['truncate', selected && 'font-semibold']">
                                    {{ person.username }}
                                  </span>
                                  <span
                                    :class="['ml-2 truncate text-gray-500', active ? 'text-indigo-200' : 'text-gray-500']">
                                    &lt;{{ person.email }}&gt;
                                  </span>
                                </div>
                                <span v-if="selected"
                                  :class="['absolute inset-y-0 right-0 flex items-center pr-4', active ? 'text-white' : 'text-gray-500']">
                                  <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                </span>
                              </li>
                            </ComboboxOption>
                          </ComboboxOptions>
                        </Combobox>
                      </div>

                      <!-- Quatrième input Combobox -->
                      <div class="flex-1 min-w-[150px] mt-2 relative">
                        <Combobox as="div" v-model="selectedPerson">
                          <div class="relative flex items-center w-full">
                            <user-icon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                            <ComboboxInput
                              class="w-full rounded-md border-0 bg-white py-3 pl-10 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 truncate"
                              @input="query = $event.target.value"
                              :display-value="(person) => person?.username"
                              placeholder="Résultats maximums"
                              style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;"
                            />
                            <ComboboxButton class="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center focus:outline-none">
                              <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </ComboboxButton>
                          </div>
                        
                        </Combobox>
                      </div>

                      <!-- Cinquième input Listbox emails Linked for search -->
                      <div class="flex-1 min-w-[150px] mt-2">
                          <Listbox as="div" v-model="attachmentSelected">
                              <div class="relative">
                                  <ListboxButton
                                      class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-12 text-left flex items-center text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6">
                                      <adjustments-horizontal-icon class="w-5 h-5 mr-2 mt-2 mb-2 text-gray-400" />
                                      <span class="block truncate text-gray-700">
                                          {{ attachmentSelected ? attachmentSelected.name : 'Email lié' }}
                                      </span>
                                      <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                          <ChevronUpDownIcon class="h-5 w-5 text-gray-400 mt-2 mb-2" aria-hidden="true" />
                                      </span>
                                  </ListboxButton>
                                  <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
                                      <ListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                                          <ListboxOption as="template" v-for="type in attachmentTypes" :key="type.extension" :value="type" v-slot="{ active, attachmentSelected }">
                                              <li :class="[active ? 'bg-gray-500 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                                                  <span :class="[attachmentSelected ? 'font-semibold' : 'font-normal', 'block truncate ml-7 mr-2']">
                                                      {{ type.name }} {{ type.extension }}
                                                  </span>
                                                  <span v-if="attachmentSelected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                                      <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                                  </span>
                                              </li>
                                          </ListboxOption>
                                      </ListboxOptions>
                                  </transition>
                              </div>
                          </Listbox>
                      </div>

                      <!-- Sixième input Combobox subject-->
                      <div class="flex-1 min-w-[150px] mt-2 relative">
                        <Combobox as="div" v-model="selectedPerson">
                          <div class="relative flex items-center w-full">
                            <user-icon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                            <ComboboxInput
                              class="w-full rounded-md border-0 bg-white py-3 pl-10 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 truncate"
                              @input="query = $event.target.value"
                              :display-value="(person) => person?.username"
                              placeholder="Sujet"
                              style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;"
                            />
                            <ComboboxButton class="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center focus:outline-none">
                              <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </ComboboxButton>
                          </div>
                        
                        </Combobox>
                      </div>

                      <!-- Septième input Combobox body -->
                      <div class="flex-1 min-w-[150px] mt-2 relative">
                        <Combobox as="div" v-model="selectedPerson">
                          <div class="relative flex items-center w-full">
                            <user-icon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                            <ComboboxInput
                              class="w-full rounded-md border-0 bg-white py-3 pl-10 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 truncate"
                              @input="query = $event.target.value"
                              :display-value="(person) => person?.username"
                              placeholder="Objet"
                              style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;"
                            />
                            <ComboboxButton class="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center focus:outline-none">
                              <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </ComboboxButton>
                          </div>
                        
                        </Combobox>
                      </div>


                      <!-- Huitième input Combobox date_from -->
                      <div class="flex-1 min-w-[150px] mt-2 relative">
                        <Combobox as="div" v-model="selectedPerson">
                          <div class="relative flex items-center w-full">
                            <user-icon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                            <ComboboxInput
                              class="w-full rounded-md border-0 bg-white py-3 pl-10 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 truncate"
                              @input="query = $event.target.value"
                              :display-value="(person) => person?.username"
                              placeholder="Tailles"
                              style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;"
                            />
                            <ComboboxButton class="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center focus:outline-none">
                              <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </ComboboxButton>
                          </div>
                        
                        </Combobox>
                      </div>


                      <!-- neuxième input Listbox  1month, 2 weeks, 90days A REVOIR --> 
                      <div class="flex-1 min-w-[150px] mt-2">
                          <Listbox as="div" v-model="attachmentSelected">
                            <div class="relative">

                              <ListboxButton
                                class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-12 text-left flex items-center text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6">
                                <adjustments-horizontal-icon class="w-5 h-5 mr-2 mt-2 mb-2 text-gray-400" />
                                <span class="block truncate text-gray-700">
                                  {{ attachmentSelected ? attachmentSelected.name : 'Plage de dates' }}
                                </span>
                                <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                  <ChevronUpDownIcon class="h-5 w-5 text-gray-400 mt-2 mb-2" aria-hidden="true" />
                                </span>
                              </ListboxButton>

                              <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
                                <ListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                                  
                                  <ListboxOption as="template" :value="{ name: '1 day', extension: '' }" v-slot="{ active, selected }">
                                    <li :class="[active ? 'bg-gray-500 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                                      <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate ml-7 mr-2']">
                                        1 day
                                      </span>
                                      <span v-if="selected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                      </span>
                                    </li>
                                  </ListboxOption>

                                  <ListboxOption as="template" :value="{ name: '3 days', extension: '' }" v-slot="{ active, selected }">
                                    <li :class="[active ? 'bg-gray-500 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                                      <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate ml-7 mr-2']">
                                        3 days
                                      </span>
                                      <span v-if="selected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                      </span>
                                    </li>
                                  </ListboxOption>

                                  <ListboxOption as="template" :value="{ name: '1 week', extension: '' }" v-slot="{ active, selected }">
                                    <li :class="[active ? 'bg-gray-500 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                                      <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate ml-7 mr-2']">
                                        1 week
                                      </span>
                                      <span v-if="selected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                      </span>
                                    </li>
                                  </ListboxOption>

                                  <ListboxOption as="template" :value="{ name: '2 weeks', extension: '' }" v-slot="{ active, selected }">
                                    <li :class="[active ? 'bg-gray-500 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                                      <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate ml-7 mr-2']">
                                        2 weeks
                                      </span>
                                      <span v-if="selected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                      </span>
                                    </li>
                                  </ListboxOption>

                                  <ListboxOption as="template" :value="{ name: '1 month', extension: '' }" v-slot="{ active, selected }">
                                    <li :class="[active ? 'bg-gray-500 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                                      <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate ml-7 mr-2']">
                                        1 month
                                      </span>
                                      <span v-if="selected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                      </span>
                                    </li>
                                  </ListboxOption>

                                  <ListboxOption as="template" :value="{ name: '2 months', extension: '' }" v-slot="{ active, selected }">
                                    <li :class="[active ? 'bg-gray-500 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                                      <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate ml-7 mr-2']">
                                        2 months
                                      </span>
                                      <span v-if="selected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                      </span>
                                    </li>
                                  </ListboxOption>

                                  <ListboxOption as="template" :value="{ name: '6 months', extension: '' }" v-slot="{ active, selected }">
                                    <li :class="[active ? 'bg-gray-500 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                                      <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate ml-7 mr-2']">
                                        6 months
                                      </span>
                                      <span v-if="selected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                      </span>
                                    </li>
                                  </ListboxOption>

                                  <ListboxOption as="template" :value="{ name: '1 year', extension: '' }" v-slot="{ active, selected }">
                                    <li :class="[active ? 'bg-gray-500 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                                      <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate ml-7 mr-2']">
                                        1 year
                                      </span>
                                      <span v-if="selected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                      </span>
                                    </li>
                                  </ListboxOption>

                                </ListboxOptions>
                              </transition>
                            </div>
                          </Listbox>
                      </div>


                </div>


                     <!-- <div class="relative items-stretch mt-2">
                      <Combobox as="div" v-model="selectedPerson">
                        <div class="relative">
                          <ComboboxInput
                            class="flex items-center rounded-md border-0 bg-white py-3 pl-10 pr-3 text-gray-900 shadow-sm ring-1 ring-inset
                            ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                            @input="query = $event.target.value"
                            :display-value="(person) => person?.username"
                            placeholder="1month, 2 weeks, 90days"/>
                          Date range TODO: custom list of choices:
                            
                            Gmail choices (you can add more or less if its relevant)
                            1 day
                            3 days
                            1 week
                            2 weeks
                            1 month
                            2 months
                            6 months
                            1 year
                           
                          <user-icon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                          <ComboboxButton
                            class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
                            <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                          </ComboboxButton>
                        </div>
                      </Combobox>
                    </div>  -->


                      <!-- <div class="col-span-1">
                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Tout les fields doivent
                    être ds advanced à part recherche</label>

                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">INT FIELD:
                    max_results</label>

                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">BOOL FIELD:
                    advanced</label>
                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">LIST FIELD: emails
                    Linked for search</label>
                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">INPUT FIELD:
                    subject</label>
                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">INPUT FIELD:
                    body</label>
                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">INPUT FIELD:
                    date_from</label>
                  <label for="email" class="block text-sm font-medium leading-6 text-gray-900">INPUT FIELD:
                    search_in</label>
                </div>-->

              </div>
              </div>

          
              <!-- email List -->
              <div class="flex-1 flex flex-col py-2" id="liste_email">
                <div class="h-full overflow-y-auto">
                  <!-- OLD ASK THEO BEFORE DELETE 
                  <template v-if="emailList.length > 0">
                    <ul class="space-y-4 pr-4">
                      <template v-for="(email, index) in emailList" :key="email.email_id">
                        <li class="flex justify-between items-center py-4 email-item">
                          <div class="flex flex-col justify-center">
                            <span class="font-bold text-sm">
                              {{ email.from_info && email.from_info[0] ? email.from_info[0] : 'Unknown' }}
                              ({{ email.from_info && email.from_info[1] ? email.from_info[1] : 'No email' }})
                            </span>
                            <span class="text-sm">{{ email.subject }} - {{ email.snippet }}...</span>
                          </div>

                          <span class="isolate inline-flex items-center rounded-2xl">
                            <div class="relative group">
                              <button class="border border-black text-black rounded-full px-2 py-1 hover:bg-gray-200 focus:outline-none focus:border-gray-500 flex items-center gap-x-2 justify-center">
                                <EyeIcon class="w-5 h-5" />
                                Voir
                              </button>
                            </div>
                          </span>
                        </li>

                        <li v-if="index < emailList.length - 1" class="flex relative pt-2">
                          <div class="absolute inset-0 flex items-center" aria-hidden="true">
                            <div class="w-full border-t border-gray-300"></div>
                          </div>
                        </li>
                      </template>
                    </ul>
                  </template>-->
                  <template v-if="sortedEmailList.length > 0">
                    <ul class="space-y-4 pr-4">
                      <template v-for="(email, index) in sortedEmailList" :key="email.id">
                        <li class="group flex justify-between items-center py-2 email-item"  @click="toggleHiddenParagraph(index)">
                          <div class="flex flex-col justify-center">
                            <span class="font-semibold text-sm leading-6">
                              {{ email.sender.name }}
                              - {{ email.sender.email }} <span class="font-normal ml-2 text-gray-600 text-xs">  {{ email.sentDate }} </span>
                            </span>
                            <span class="text-sm gray-600">{{ email.subject }} - {{ email.oneLineSummary }}</span>
                            <div v-if="email.showSummary" class="py-1">
                              <p class="text-xs">{{ email.shortSummary }}</p>
                            </div>
                            <div class="mt-1 flex space-x-2">
                              <!-- Priority flag -->
                              <span v-if="email.priority === 'important'" class="inline-flex items-center rounded-md bg-orange-50 px-2 py-1 text-xs font-medium text-orange-700 ring-1 ring-inset ring-orange-600/10">Important</span>
                              <span v-else-if="email.priority === 'informative'" class="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">Informative</span>
                              <span v-else class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10">Useless</span>
                              
                              <!-- Category flag (always gray) -->
                              <span class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10">{{ email.category }}</span>
                              
                              <!-- Optional hover UX info -->
                              <span
                                v-bind:class="{
                                  'hidden group-hover:block px-1.5 text-white shadow rounded-xl inline-flex': true,
                                  'bg-orange-300': email.priority === 'important',
                                  'bg-blue-300': email.priority === 'informative',
                                  'bg-gray-300': email.priority !== 'important' && email.priority !== 'informative'
                                }"
                              >
                                <div class="flex gap-x-1 items-center justify-center h-full">
                                  <svg xmlns="http://www.w3.org/2000/svg"
                                      fill="none" viewBox="0 0 24 24"
                                      stroke-width="1.5"
                                      stroke="currentColor"
                                      class="w-4 h-4">
                                    <path stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                                  </svg>
                                  <p class="text-xs">{{ $t('constants.userActions.clickToSeeTheSummary') }}</p>
                                </div>
                              </span>
                            </div>
                          </div>

                          <span class="isolate inline-flex items-center rounded-2xl">
                            <div class="relative group">
                              <button @click.stop="openMail(email.id)" class="border border-black text-black rounded-full px-2 py-1 hover:bg-gray-200 focus:outline-none focus:border-gray-500 flex items-center gap-x-2 justify-center">
                                <EyeIcon class="w-5 h-5" />
                                Voir
                              </button>
                            </div>
                          </span>
                        </li>

                        <li v-if="index < sortedEmailList.length - 1" class="flex relative pt-2">
                          <div class="absolute inset-0 flex items-center" aria-hidden="true">
                            <div class="w-full border-t border-gray-300"></div>
                          </div>
                        </li>
                      </template>
                    </ul>
                  </template>
                  <template v-else>
                    <div class="flex flex-col items-center justify-center h-full rounded-lg border-2 border-dashed border-gray-300">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                        stroke="currentColor" class="w-12 h-12 mx-auto text-gray-400">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="M15.182 16.318A4.486 4.486 0 0012.016 15a4.486 4.486 0 00-3.198 1.318M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
                      </svg>
                      <span class="mt-2 block text-sm font-semibold text-gray-900">
                        {{ $t('searchPage.noResults') }}
                      </span>
                    </div>
                  </template>
                </div>
              </div>


          </div>
        </div>

      </div>
    </div>
    <ModalSeeMail :isOpen="isModalSeeOpen" :email="selectedEmail" @closeSeeModal="closeSeeModal"
      @openAnswer="openAnswer" @openRuleEditor="openRuleEditor" @openNewRule="openNewRule" @markEmailAsRead="markEmailAsRead" @markEmailReplyLater="markEmailReplyLater" @transferEmail="transferEmail" />
</template>


<script setup>
import { ref, computed, nextTick, onMounted } from 'vue';
import Navbar from '../components/AppNavbar7.vue';
import ModalSeeMail from '../components/SeeMailV2.vue';
import { fetchWithToken, getBackgroundColor } from '../router/index.js';
import { useRouter } from 'vue-router';
import { API_BASE_URL } from '@/main';
import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
} from '@headlessui/vue';
import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from '@headlessui/vue';
import { CheckIcon, ChevronUpDownIcon, ChevronDownIcon,PaperAirplaneIcon, MagnifyingGlassIcon, UserIcon, AdjustmentsHorizontalIcon } from '@heroicons/vue/24/outline';
import { useI18n } from 'vue-i18n';

// Use i18n
const { t } = useI18n();

// Router
const router = useRouter();

// Variables to display a notification
let showNotification = ref(false);
let selectedEmailId = ref('');
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
let timerId = ref(null);

// Main variables
const AIContainer = ref(null);
const bgColor = ref('');
let counter_display = 0;
let query = ref('');
let stepcontainer = 0;
const scrollableDiv = ref(null);
const scrollToBottom = async () => {
  await nextTick();
  const element = scrollableDiv.value;
  element.scrollTop = element.scrollHeight;
};
let isAIWriting = ref(false);
let isEmailhere = ref(false);
let searchResult = ref({});
const textareaValue = ref('');


const attachmentTypes = [
  { extension: ".docx", name: "Word Document" },
  { extension: ".xlsx", name: "Excel Spreadsheet" },
  { extension: ".pptx", name: "PowerPoint Presentation" },
  { extension: ".pdf", name: "PDF Document" },
  { extension: ".jpg", name: "JPEG Image" },
  { extension: ".png", name: "PNG Image" },
  { extension: ".gif", name: "GIF Image" },
  { extension: ".txt", name: "Text Document" },
  { extension: ".zip", name: "ZIP Archive" },
  { extension: ".mp3", name: "MP3 Audio" },
  { extension: ".mp4", name: "MP4 Video" },
  { extension: ".html", name: "HTML Document" },
  { extension: null, name: "Aucune" },
]

const attachmentSelected = ref(null)

let emailsLinked = ref('');


const contacts = [];
const isFocused2 = ref(false);
const isFocused = ref(false);
const queryGetContacts = ref('')
const selectedPerson = ref(null)
const selectedRecipients = ref([])
const emailList = ref([]);

const selectedFromPerson = ref(null)
const selectedFromAddresses = ref([])

// To sort the emailList corretly
const sortedEmailList = computed(() => {
  return [...emailList.value].sort((a, b) => {
    const priorityOrder = { important: 0, informative: 1, useless: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });
});

// Modal SeeMail
let isModalSeeOpen = ref(false);
let selectedEmail = ref(null);

/******************************************************** See Modal *********************************************************/
function dismissPopup() {
    showNotification = false;
    // Cancel the timer
    clearTimeout(timerId);
}

function displayPopup() {
    showNotification = true;

    timerId = setTimeout(() => {
        dismissPopup();
    }, 4000);
}

async function openMail(emailId) {
  try {
    const htmlContent = await fetchEmailContent(emailId);
    const emailIndex = emailList.value.findIndex(email => email.id === emailId);
    
    if (emailIndex !== -1) {
      emailList.value[emailIndex] = {
        ...emailList.value[emailIndex],
        html_content: htmlContent
      };
      
      selectedEmail.value = emailList.value[emailIndex];
      console.log("EMAIL", selectedEmail.value)
      isModalSeeOpen.value = true;
    } else {
      console.error(`Email with id ${emailId} not found.`);
    }
  } catch (error) {
    console.error(`Error fetching email content: ${error}`);
  }
}
function closeSeeModal() {
    isModalSeeOpen.value = false;
}
async function openAnswer(email) {
    // THIS IS NOT NEEDED => TO UPDATE (wee do not need to fetch here => but a solution must be found for emailReceiver)
    const url = `${API_BASE_URL}api/get_mail_by_id?email_id=${email.id_provider}`;

    try {
        const data = await fetchWithToken(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });


        sessionStorage.setItem("subject", JSON.stringify(data.email.subject));
        sessionStorage.setItem("cc", data.email.cc);
        sessionStorage.setItem("bcc", data.email.bcc);
        sessionStorage.setItem("decoded_data", JSON.stringify(data.email.decoded_data));
        sessionStorage.setItem("email", JSON.stringify(email.email));
        sessionStorage.setItem("id_provider", JSON.stringify(email.id_provider));
        sessionStorage.setItem("details", JSON.stringify(email.details));
        sessionStorage.setItem("emailReceiver", data.email.email_receiver);

        console.log("_____________data.email.cc______________", data.email.cc)
        console.log("_____________data.email.bcc______________", data.email.bcc)

        router.push({
            name: 'answer'
        });
    } catch (error) {
        console.error("There was a problem with the fetch operation:", error.message);
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('constants.popUpConstants.openReplyPageFailure');
        notificationMessage = error.message;
        displayPopup();
    }
}
function openRuleEditor(ruleId) {
    if (ruleId) {
        router.push({ name: 'rules', query: { id_rule: ruleId, edit_rule: true } });
    }
}
function openNewRule(ruleName, ruleEmail) {
    if (ruleName && ruleEmail) {
        router.push({ name: 'rules', query: { rule_name: ruleName, rule_email: ruleEmail, edit_rule: false } });
    }
}
async function markEmailAsRead(emailId) {
    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/mark_read/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.read != true) {
            console.log("RESPONSE", response);
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle = t('homepage.markEmailReadFailure');
            notificationMessage = response;
            displayPopup();
        }
    } catch (error) {
        console.error('Error in markEmailAsRead:', error.message);
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('homepage.markEmailReadFailure');
        notificationMessage = error.message;
        displayPopup();
    }
}
async function markEmailReplyLater(email) {
    const emailId = email.id

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/mark_reply_later/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        console.log("RESPONSE", response)
        if (response.answer_later) {
            console.log("Email marked for reply later successfully");
        } else {
            console.error('Failed to mark email for reply later', response);
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle = t('homepage.markEmailReplyLaterFailure');
            notificationMessage = response;
            displayPopup();
        }
    } catch (error) {
        console.error('Error in markEmailReplyLater:', error.message);
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('homepage.markEmailReplyLaterFailure');
        notificationMessage = error.message;
        displayPopup();
    }
}
async function transferEmail(email) {
    const url = `${API_BASE_URL}api/get_mail_by_id?email_id=${email.id_provider}`;

    try {
        const data = await fetchWithToken(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        sessionStorage.setItem("subject", JSON.stringify(data.email.subject));
        sessionStorage.setItem("cc", data.email.cc);
        sessionStorage.setItem("bcc", data.email.bcc);
        sessionStorage.setItem("decoded_data", JSON.stringify(data.email.decoded_data));
        sessionStorage.setItem("email", JSON.stringify(email.email));
        sessionStorage.setItem("id_provider", JSON.stringify(email.id_provider));
        sessionStorage.setItem("details", JSON.stringify(email.details));
        sessionStorage.setItem("emailReceiver", data.email.email_receiver);
        sessionStorage.setItem("date", JSON.stringify(data.email.date));


        console.log("_____________data.email.cc______________", data.email.cc)
        console.log("_____________data.email.bcc______________", data.email.bcc)

        router.push({
            name: 'transfer'
        });

    } catch (error) {
        console.error("There was a problem with the fetch operation:", error.message);
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('homepage.transferEmailFailure');
        notificationMessage = error.message;
        displayPopup();
    }
}

/************************************* For dropdown button next to manual search input **************************************/
const isOpen = ref(false)
const selectedOption = ref('aomail')

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const selectOption = (option) => {
  selectedOption.value = option
  isOpen.value = false
  if (option == t('searchPage.choiceOldMailDisplay')) {
    displayMessage( t('searchPage.oldChoiceSelected'), aiIcon)
  }
  else {
    displayMessage( t('searchPage.aomailChoiceSelected'), aiIcon)
  }
}

const updateOption = (event) => {
  selectedOption.value = event.target.value
  isOpen.value = false
  if (selectedOption.value == t('searchPage.choiceOldMailDisplay')) {
    displayMessage( t('searchPage.oldChoiceSelected'), aiIcon)
  }
  else {
    displayMessage( t('searchPage.aomailChoiceSelected'), aiIcon)
  }
}

const closeDropdown = (event) => {
  if (isOpen.value && !event.target.closest('.dropdown-container')) {
    isOpen.value = false
  }
}

/*****************************************************************************************************************************/

const filteredFromPeople = computed(() =>
  queryGetContacts.value === ''
    ? contacts
    : contacts.filter((person) => {
      return person.username.toLowerCase().includes(queryGetContacts.value.toLowerCase())
    })
)

const checkLoginStatus = () => {
  const emailList = document.getElementById('liste_email');
  const hasEmails = emailList.getElementsByClassName('email-item').length > 0;
  isEmailhere.value = hasEmails;
};



onMounted(() => {
  checkLoginStatus();
  document.addEventListener('click', closeDropdown);
});

const filteredPeople = computed(() =>
  queryGetContacts.value === ''
    ? contacts
    : contacts.filter((person) => {
      return person.username.toLowerCase().includes(queryGetContacts.value.toLowerCase())
    })
)


const toggleSelection = (person) => {
  const index = selectedRecipients.value.findIndex((recipient) => recipient.email === person.email)
  if (index === -1) {
    selectedRecipients.value.push(person)
  } else {
    selectedRecipients.value.splice(index, 1)
  }
}

const removeRecipient = (recipient) => {
  const index = selectedRecipients.value.findIndex((r) => r.email === recipient.email)
  if (index !== -1) {
    selectedRecipients.value.splice(index, 1)
  }
}


const toggleSelectionFromAddress = (person) => {
  const index = selectedFromAddresses.value.findIndex((recipient) => recipient.email === person.email)
  if (index === -1) {
    selectedFromAddresses.value.push(person)
  } else {
    selectedFromAddresses.value.splice(index, 1)
  }
}

const removeRecipientFromAddress = (recipient) => {
  const index = selectedFromAddresses.value.findIndex((r) => r.email === recipient.email)
  if (index !== -1) {
    selectedFromAddresses.value.splice(index, 1)
  }
}

const requestOptions = {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
  },
}
fetchWithToken(`${API_BASE_URL}user/contacts/`, requestOptions)
  .then(response => {
    contacts.push(...response);
  })
  .catch(error => {
    backgroundColor = 'bg-red-200/[.89] border border-red-400';
    notificationTitle.value = t('constants.popUpConstants.errorMessages.contactFetchError');
    notificationMessage.value = error;
    displayPopup();
  });


// User pressed the object input
function handleFocusSearch() {
    isFocused.value = true;
}
function handleBlurSearch() {
    isFocused.value = false;
}

// User click on short summary
function toggleHiddenParagraph(index) {
  sortedEmailList.value[index].showSummary = !sortedEmailList.value[index].showSummary;
}

function handleBlur2(event) {
  // Checks for a valid input email and adds it to the recipients list
  isFocused.value = false;
  const inputValue = event.target.value.trim().toLowerCase();
  const emailFormat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (inputValue && emailFormat.test(inputValue)) {
      if (!people.find(person => person.email === inputValue)) {
          const newPerson = { username: '', email: inputValue };
          people.push(newPerson);
          selectedPeople.value.push(newPerson);
      }
  } else if (!filteredPeople.value.length && inputValue) {
      // Show the pop-up
      backgroundColor = 'bg-red-200/[.89] border border-red-400';
      notificationTitle.value = t('constants.popUpConstants.errorMessages.invalidEmail');
      notificationMessage.value = t('constants.popUpConstants.errorMessages.emailFormatIncorrect');
      displayPopup();
  }
}


// function linked to ENTER key listeners
function handleEnterKey(event) {
    // Allow pressing Enter with Shift to create a line break
    if (event.target.id === 'dynamicTextarea' && event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        handleAIClick();
    }
    else if (isFocused2.value) {
        event.preventDefault();
        handleBlur2(event);
        // the user is still on the input
        handleFocusDestinary();
    }
}


// Mounted lifecycle hook
onMounted(async () => {
  getBackgroundColor();
  fetchEmailLinked();
  bgColor.value = localStorage.getItem('bgColor');

  AIContainer.value = document.getElementById('AIContainer');

  await askQueryUser();
});


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
      notificationTitle = t('constants.popUpConstants.errorMessages.emailLinkedFetchError');
      notificationMessage = response.error;
      displayPopup();
    } else {
      emailsLinked.value = response;
    }
  } catch (error) {
    // Show the pop-up
    backgroundColor = 'bg-red-200/[.89] border border-red-400';
    notificationTitle = t('constants.popUpConstants.errorMessages.emailLinkedFetchError');
    notificationMessage = error.message;
    displayPopup();
  }
}

// ULTRA IMPORTANT: THIS FUNCTION IS LIKE SEARCH MANUALLY BUT WITH USER STRING INPUT
// async function handleAIClick() {

//   if (isAIWriting.value) {
//     return;
//   }
//   isAIWriting.value = true;

//   loading();
//   scrollToBottom();


//   const emailsLinkedSelected = emailsLinked.value.map(e => e.email)


//   const requestOptions = {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({
//       emails: emailsLinkedSelected,
//       query: textareaValue.value
//     }),
//   };

//   textareaValue.value = "";
//   const result = await fetchWithToken(`${API_BASE_URL}api/search_emails_ai/`, requestOptions);
//   searchResult.value = result;
//   hideLoading();
//   isAIWriting.value = false;
// }

// WHAT IS THIS ? TO FIX ?
const aiIcon = '<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" /> ';

// THIS FUNCTION IS USED TO ANSWER A USER QUESTION WITH TREE KNOWLEDGE
async function handleAIClick() {
  if (isAIWriting.value) {
    return;
  }
  isAIWriting.value = true;

  loading();
  scrollToBottom();

  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      question: textareaValue.value
    }),
  };

  textareaValue.value = "";

  try {
    const result = await fetchWithToken(`${API_BASE_URL}api/search_tree_knowledge/`, requestOptions);

    //const aiIcon = '<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />';

    let message = '';
    if (result.error) {
      // Show the pop-up
      backgroundColor = 'bg-red-200/[.89] border border-red-400';
      notificationTitle = t('searchPage.popUpConstants.successMessages.smartSearchError');
      notificationMessage = result.error;
      displayPopup();
    } else if (result.message) {
      message = t('searchPage.notEnoughDataToAnswer');
    } else {
      const { sure, answer, ids } = result.answer;
      console.log(result.answer);
      message = answer;

      // Limit to 25 results
      const limitedEmails = ids.slice(0, 25);
      const emailDetails = await fetchEmailDetails(limitedEmails);
      console.log(emailDetails);
      emailList.value = Object.entries(emailDetails.data).flatMap(([category, priorities]) => 
        Object.entries(priorities).flatMap(([priority, emails]) => 
          emails.map(email => ({
            ...email,
            category: category,
            priority: priority
          }))
        )
      );
      //emailList.value = emailDetails;
    }

    await displayMessage(message, aiIcon);
  } catch (error) {
    console.error('Error fetching AI response:', error);
    await displayMessage(t('searchPage.anErrorOccuredDuringSmartSearch') , aiIcon);
  } finally {
    hideLoading();
    isAIWriting.value = false;
  }
}

async function fetchEmailDetails(emailIds) {
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      ids: emailIds
    }),
  };

  try {
    const result = await fetchWithToken(`${API_BASE_URL}user/get_emails_data/`, requestOptions);
    console.log("RESULT :", result);
    return result;
  } catch (error) {
    console.error('Error fetching email details:', error);
    return [];
  }
}

async function fetchEmailContent(emailId) {
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      id: emailId
    }),
  };

  try {
    const result = await fetchWithToken(`${API_BASE_URL}user/get_email_content/`, requestOptions);
    console.log("RESULT :", result);
    return result.content;
  } catch (error) {
    console.error('Error fetching email HTML content:', error);
    return [];
  }
}

async function searchEmails() {
  // TODO: add a list choice and not a UNIQUE choice
  let fileExt = "";
  for (const key in attachmentSelected.value) {
    if (key === "extension") {
      fileExt = attachmentSelected.value[key];
    }
  }

  // TODO
  // une case par compte à cocher (email)
  // un bouton cocher TOUS (email)
  const toAddressesSelected = selectedRecipients.value.map(recipient => recipient.email);
  const fromAddressesSelected = selectedFromAddresses.value.map(recipient => recipient.email);
  const emailsLinkedSelected = emailsLinked.value.map(e => e.email)

  loading();
  scrollToBottom();


  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      resultPerPage: 25,
      advanced: false,
      subject: query.value,
      senderEmail: query.value,
      senderName: query.value,
    }),
  };

  console.log("Sending request:", JSON.stringify(requestOptions.body));

  const result = await fetchWithToken(`${API_BASE_URL}user/emails/`, requestOptions);
  console.log(result);
  if (result.count > 0) {
    const limitedEmails = result.ids.slice(0, 25);
    const emailDetails = await fetchEmailDetails(limitedEmails);
    emailList.value = Object.entries(emailDetails.data).flatMap(([category, priorities]) => 
      Object.entries(priorities).flatMap(([priority, emails]) => 
        emails.map(email => ({
          ...email,
          category: category,
          priority: priority
        }))
      )
    );
  }
  hideLoading();

  if (result.count == 1) {
    await displayMessage(result.count+' email '+t('searchPage.oneDataFound'), aiIcon);
  } else if (result.count > 1) {
    await displayMessage(result.count+" emails "+t('searchPage.severalDataFound'), aiIcon);
  } else {
    await displayMessage(t('searchPage.noDataFound'), aiIcon);
  }
}

async function Hide_filtres() {
    var toggleDiv = document.getElementById('filtres');
    var emailListDiv = document.getElementById('liste_email');

    if (toggleDiv.classList.contains('hidden')) {
        toggleDiv.classList.remove('hidden');
        setTimeout(function () {
            toggleDiv.classList.remove('opacity-0');
            toggleDiv.classList.add('opacity-100');
        }, 10);
        
        // Réduire la hauteur de la liste des emails
        adjustHeight2(emailListDiv, -185);
    } else {
        toggleDiv.classList.remove('opacity-100');
        toggleDiv.classList.add('opacity-0');
        setTimeout(function () {
            toggleDiv.classList.add('hidden');
        }, 250);
        
        // Augmenter la hauteur de la liste des emails
        adjustHeight2(emailListDiv, 185);
    }
}

function adjustHeight2(element, adjustment) {
    const currentHeight = parseInt(window.getComputedStyle(element).height, 10);

    // Si la hauteur actuelle est supérieure à 350px et que l'ajustement est négatif, ajuster de 200px
    if (currentHeight > 500 && adjustment < 0) {
        adjustment = -200;
    }

    const newHeight = currentHeight + adjustment;
    element.style.height = newHeight + 'px';
}


async function displayMessage(message, ai_icon) {
  // Function to display a message from the AI Assistant

  isAIWriting.value = true;
  const messageHTML = `
      <div class="flex pb-12">
        <div class="mr-4 flex">
          <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              ${ai_icon}
            </svg>
          </span>   
        </div>
        <div>
          <p ref="animatedText${counter_display}"></p>
        </div>
      </div>
    `;
  AIContainer.value.innerHTML += messageHTML;
  const animatedParagraph = document.querySelector(`p[ref="animatedText${counter_display}"]`);
  counter_display += 1;
  await animateText(message, animatedParagraph);
  scrollToBottom();
}
async function waitForAIWriting() {
  while (isAIWriting.value) {
    await new Promise(resolve => setTimeout(resolve, 500));
  }
}
async function animateText(text, target) {
  let characters = text.split("");
  let currentIndex = 0;
  const interval = setInterval(() => {
    if (currentIndex < characters.length) {
      target.textContent += characters[currentIndex];
      currentIndex++;
    } else {
      clearInterval(interval);
      isAIWriting.value = false;
    }
  }, 30);
}

async function askQueryUser() {
  // const message = "Bonjour, quel email recherchez vous. Pouvez vous me donner des informations sur l'email ?"; THIS IS FOR AI SEARCH NOT TREE KNOWLEDGE
  const message = "Bonjour, quelle information souhaitez vous chercher ?"; // THIS IS FOR TREE KNOWLEDGE
  const ai_icon = '<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />';
  await displayMessage(message, ai_icon);

  // Wait for isAIWriting to become false
  await waitForAIWriting();

  // TO DELETE AFTER feature/searchPage is valid
  //const message1 = "Cette page est non fonctionnelle et en cours de développement";
  //const message1 = "Recherche avec IA désactivée ❌ | Connaissance arborescente activée ✅";
  //const ai_icon1 = '<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />';
  //await displayMessage(message1, ai_icon1);
}

// To handle the input going to wide 
const adjustHeight = (event) => {
  const textarea = event.target;
  const maxHeight = 250; // Set your desired max height in pixels

  // Reset height to auto to correctly calculate the new scrollHeight
  textarea.style.height = 'auto';

  if (textarea.scrollHeight > maxHeight) {
    textarea.style.height = `${maxHeight}px`;
    textarea.style.overflowY = 'auto'; // Enable scrolling when content exceeds maxHeight.
  } else {
    textarea.style.height = `${textarea.scrollHeight}px`;
    textarea.style.overflowY = 'hidden'; // Hide the scrollbar when content is below maxHeight.
  }
}

function loading() {
  // Use `nbr` in the template literal to set the reference dynamically
  const messageHTML = `
      <div id="dynamicLoadingIndicator" class="pb-12">
        <div class="flex">
            <div class="mr-4">
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900">
                    <span class="text-lg font-medium leading-none text-white">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15a4.5 4.5 0 0 0 4.5 4.5H18a3.75 3.75 0 0 0 1.332-7.257 3 3 0 0 0-3.758-3.848 5.25 5.25 0 0 0-10.233 2.33A4.502 4.502 0 0 0 2.25 15Z" />
                      </svg>
                    </span>
                </span>
            </div>
            <div>
              <div class="loading-spinner"></div>
            </div>
        </div>
      </div>
    `;

  AIContainer.value.innerHTML += messageHTML;
}

function hideLoading() {
  const loadingElement = document.getElementById('dynamicLoadingIndicator');
  if (loadingElement) {
    loadingElement.remove();
  }
}
</script>

<script>
import {
    EyeIcon
} from '@heroicons/vue/24/outline'

export default {
    name: 'UserHome',
    components: { 
        EyeIcon
    }
}
</script>