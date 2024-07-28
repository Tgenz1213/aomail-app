<template>
    <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" />
    <div v-if="loading">
        <Loading class=""></Loading>
    </div>

    <div v-else>
        <!-- Modal for Warning Category (rules linked) -->
        <transition name="modal-fade">
            <div @click.self="closeWarningCategoryModal"
                class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
                v-if="isModalWarningCategoryOpen">
                <div class="bg-white rounded-lg relative w-[450px]">
                    <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
                        <button @click="closeWarningCategoryModal" type="button"
                            class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                        </button>
                    </div>
                    <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
                        <div class="ml-8 flex items-center space-x-1">
                            <p class="block font-semibold leading-6 text-gray-900">{{ $t('homePage.modals.warningRulesLinkedModal.deleteCategory') }} {{
                                categoryToUpdate.name }}</p>
                        </div>
                    </div>
                    <div class="flex flex-col gap-4 px-8 py-6">
                        <div>
                            <div class="flex space-x-1 items-center">
                                <label class="block text-sm font-medium leading-6 text-gray-900">
                                    <template v-if="nbRulesAssociated <= 1">
                                        {{ $t('homePage.youHave') }} {{ nbRulesAssociated }} {{ $t('homePage.rule') }}
                                        {{ $t('homePage.linked') }} {{ $t('homePage.toThisCategory') }}
                                    </template>
                                    <template v-else>
                                        {{ $t('homePage.youHave') }} {{ nbRulesAssociated }} {{ $t('homePage.rules') }}
                                        {{ $t('homePage.linked') }} {{ $t('homePage.toThisCategory') }}
                                    </template>
                                    {{ $t('homePage.warningForDeletingTheCategory') }}
                                </label>
                            </div>
                        </div>
                        <div class="mt-2 sm:mt-2 sm:flex sm:flex-row justify-between">
                            <button type="button"
                                class="inline-flex w-full rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:w-auto"
                                @click="closeWarningCategoryModal">{{ $t('constants.userActions.cancel') }} </button>
                            <button type="button"
                                class="inline-flex w-full justify-cente items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto"
                                @click="deleteCategory(categoryToUpdate.name)">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                </svg>{{ $t('constants.userActions.delete') }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </transition>

        <div class="flex flex-col justify-center items-center h-screen"><!-- DO NOT DELETE : 'bg-gray-900'-->

            <div class="flex h-full w-full">

                <!--NAVBAR verticale-->
                <div class="w-[90px] 2xl:w-[100px] bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                    <navbar></navbar>
                </div>

                 <!--Colonne 1-->
                <div class="flex-1">
                    <!-- <div class="flex flex-col xl:h-[calc(93vh)] xl:w-[86vw] 2xl:h-[6/7*100vh] 2xl:w-[calc(80vw)]"> WORKS FOR 1920*1200px screens-->
                    <div class="flex flex-col h-full w-full">

                         <!--ligne 1 : navbar horizontale -->
                        <main class="bg-gray-50 ring-1 shadow-sm ring-black ring-opacity-5 border-b border-black shadow-sm border-opacity-10">
                            <div class="w-full py-2 2xl:py-3 px-4 2xl:px-8 lg:px-2">
                                <div class="grid grid-cols-11 gap-4 items-center divide-x divide-gray-300">
                                    <div class="pl-4 col-span-11 h-full flex items-center">
                                        <div class="w-full flex items-center justify-center">

                                            <!--selection des tabs-->
                                            <div class="sm:hidden">
                                                <label for="tabs" class="sr-only">Select a tab</label>
                                                <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
                                                <select id="tabs" name="tabs"
                                                    class="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
                                                    v-model="selectedTopic">
                                                    <option v-for="category in categories" :key="category">
                                                        {{ category.name }}
                                                    </option>
                                                </select>
                                            </div>
                                            
                                             <!--categories list-->
                                            <div class="hidden sm:block w-full py-5">
                                                <nav class="flex flex-wrap space-x-2 2xl:space-x-4 justify-center items-center w-full"
                                                    aria-label="Tabs">

                                                    <div class="flex space-x-4 2xl:space-x-6">
                                                        <!--On parcours la liste decategories -->
                                                        <a v-for="category in categories" :key="category"
                                                            class="group items-center text-gray-600 text-sm font-medium"><!-- To FIX => put category.name and adapt the design -->
                                                            
                                                             <!--catégories que l'utilisateur a créer-->
                                                            <div v-if="category.name !== 'Others'"
                                                                class="flex cursor-pointer"
                                                                @click="selectCategory(category)">
                                                                <span class="px-3 py-2 group-hover:rounded-r-none"
                                                                    :class="{ 'bg-gray-500 bg-opacity-10 text-gray-800': selectedTopic === category.name, 'group-hover:bg-gray-500 rounded-l-md group-hover:bg-opacity-10': selectedTopic !== category.name, 'rounded-md': totalEmailsInCategoryNotRead(category.name) === 0, 'rounded-l-md': totalEmailsInCategoryNotRead(category.name) > 0 }">{{
                                                                        category.name }}
                                                                </span>
                                                                <div class="group-hover:bg-gray-500 group-hover:rounded-r-none group-hover:bg-opacity-10 flex items-center"
                                                                    :class="{ 'bg-gray-500 bg-opacity-10 rounded-r-md': selectedTopic === category.name }">
                                                                    <span
                                                                        v-if="totalEmailsInCategoryNotRead(category.name) > 0"
                                                                        class="group-hover:bg-transparent group-hover:text-gray-800 rounded-full py-0.5 px-2.5 text-xs font-medium"
                                                                        :class="{ 'text-gray-800': selectedTopic === category.name, 'text-white bg-gray-800': selectedTopic !== category.name }">
                                                                        {{ totalEmailsInCategoryNotRead(category.name)
                                                                        }}
                                                                    </span>
                                                                </div>
                                                                <span
                                                                    class="opacity-0 group-hover:opacity-100 pr-2 py-2 group-hover:bg-gray-500 rounded-r-md group-hover:bg-opacity-10">
                                                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                                        viewBox="0 0 24 24" stroke-width="1.5"
                                                                        stroke="currentColor"
                                                                        class="w-5 h-5 hover:text-black"
                                                                        @click.stop="openUpdateModal(category)">
                                                                        <path stroke-linecap="round"
                                                                            stroke-linejoin="round"
                                                                            d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                                                                    </svg>
                                                                </span>
                                                            </div>

                                                             <!--categories Autres,Others-->
                                                            <div v-else class="flex pr-7">
                                                                <!-- TODO: var language and retrieve the good translation -->
                                                                <span class="px-3 py-2 cursor-pointer"
                                                                    @click="selectCategory(category)"
                                                                    :class="{ 'bg-gray-500 bg-opacity-10 text-gray-800': selectedTopic === category.name, 'group-hover:bg-gray-500 rounded-l-md group-hover:bg-opacity-10': selectedTopic !== category.name, 'rounded-md': totalEmailsInCategoryNotRead(category.name) === 0, 'rounded-l-md': totalEmailsInCategoryNotRead(category.name) > 0 }">
                                                                    {{ $t('homePage.otherCategory') }}
                                                                </span>
                                                                <div @click="selectCategory(category)"
                                                                    class="group-hover:bg-gray-500 group-hover:rounded-r group-hover:bg-opacity-10 flex items-center cursor-pointer"
                                                                    :class="{ 'bg-gray-500 bg-opacity-10 rounded-r-md': selectedTopic === category.name }">
                                                                    <span
                                                                        v-if="totalEmailsInCategoryNotRead(category.name) > 0"
                                                                        class="group-hover:bg-transparent group-hover:text-gray-800 rounded-full py-0.5 px-2.5 text-xs font-medium"
                                                                        :class="{ 'text-gray-800': selectedTopic === category.name, 'text-white bg-gray-800': selectedTopic !== category.name }">
                                                                        {{ totalEmailsInCategoryNotRead(category.name)
                                                                        }}
                                                                    </span>
                                                                </div>
                                                            </div>
                                                        </a>
                                                    </div>

                                                    <a class="flex text-gray-600 rounded-md px-8 py-2 text-sm font-medium hover:bg-gray-900 hover:text-white"
                                                        @click="openModal">
                                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                            viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                                            class="w-6 h-6">
                                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                                d="M12 4.5v15m7.5-7.5h-15" />
                                                        </svg>
                                                    </a>

                                                </nav>
                                            </div>

                                            <!--bouton pour l'onglet à droite-->
                                            <div class="flex justify-end h-full">
                                                <button @click="toggleVisibility" class="bg-gray-200 text-gray-500 p-2 rounded-full items-center inline-flex">
                                                    <svg v-if="isHidden" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="m18.75 4.5-7.5 7.5 7.5 7.5m-6-15L5.25 12l7.5 7.5" />
                                                    </svg>
                                                    <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="m5.25 4.5 7.5 7.5-7.5 7.5m6-15 7.5 7.5-7.5 7.5" />
                                                    </svg>
                                                </button>
                                            </div> 

                                        </div>
                                    </div>
                                </div>
                            </div>
                        </main>

                        <div class="w-full relative">
                            <SearchbarV2 
                            @input="updateSearchQuery" 
                            height="3rem"
                            :showFilterButton="true"
                            :filterFields="[
                                { name: 'from', label: 'De', type: 'text', placeholder: 'De' },
                                { name: 'to', label: 'À', type: 'text', placeholder: 'À' },
                                { name: 'subject', label: 'Objet', type: 'text', placeholder: 'Objet' },
                                { name: 'contains', label: 'Contient les mots', type: 'text', placeholder: 'Contient les mots' },
                                { name: 'doesNotContain', label: 'Ne contient pas', type: 'text', placeholder: 'Ne contient pas' },
                                { name: 'size', label: 'Taille', type: 'select', options: [{ value: 'greater', label: 'supérieure à' }, { value: 'less', label: 'inférieure à' }] },
                                { name: 'dateRange', label: 'Plage de dates', type: 'select', options: [{ value: '1day', label: '1 jour' }, { value: '1week', label: '1 semaine' }, { value: '1month', label: '1 mois' }, { value: '1year', label: '1 an' }] },
                                { name: 'searchIn', label: 'Rechercher', type: 'select', options: [{ value: 'all', label: 'Tous les messages' }, { value: 'read', label: 'Messages lus' }, { value: 'unread', label: 'Messages non lus' }] },
                                { name: 'hasAttachment', label: 'Contenant une pièce jointe', type: 'checkbox' },
                                { name: 'excludeChats', label: 'Ne pas inclure les chats', type: 'checkbox' }
                            ]"
                            />
                        </div>

                        <!--<div class="w-full bg-white flex flex-col sm:flex-row items-center">
                            <div class="w-full sm:flex-grow sm:mr-4 mb-4 sm:mb-0">
                                <SearchbarV2 @input="updateSearchQuery" height="3rem" class="w-full"></SearchbarV2>
                            </div>

                            <div class="flex items-center">
                                <div class="hidden sm:block w-px h-8 bg-gray-400 mr-4"></div>
                                <select 
                                    @change="applyFilter"
                                    class="border-none text-gray-900 text-sm focus:ring-0 focus:outline-none"
                                >
                                    <option disabled value="">Aucun filtre</option>
                                    <option value="important">Important</option>
                                    <option value="informatif">Informatif</option>
                                    <option value="inutile">Inutile</option>
                                </select>
                            </div>
                        </div>-->

                        <!-- HIDE 
                        <div class="rounded-t-xl lg:mt-4 bg-gray-100 py-3 px-2 ring-1 shadow-sm ring-black ring-opacity-5">
                            <p>En cours de dev</p>
                        </div>--><!-- DO NOT DELETE bg-opacity-90 -->
                        <!--L'utilisateur n'a pas de nouveau mail-->
                        <div v-if="isEmptyTopic()" class="flex-1 bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                            <!-- Content goes here -->
                            <div v-if="isEmptyTopic()" class="flex flex-col w-full h-full rounded-xl">
                                <div
                                    class="flex flex-col justify-center items-center h-full m-5 rounded-lg border-2 border-dashed border-gray-400 p-12 text-center hover:border-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1" stroke="currentColor" class="mx-auto h-14 w-14 text-gray-400">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                                    </svg>
                                    <span class="mt-2 block text-md font-semibold text-gray-900">{{ $t('homePage.noNewEmail')
                                        }}</span>
                                </div>
                            </div>
                            
                        </div>

                        <!--L'utilisateur a des nouveaux mails-->
                        <div v-else
                            class="flex-1 bg-white bg-opacity-100 ring-1 shadow-sm ring-black ring-opacity-5 overflow-y-auto custom-scrollbar"
                            ref="scrollableDiv">

                            <!--Liste emails-->
                            <ul role="list" class="flex mx-2 flex-col w-auto h-full rounded-xl">
                                <!--DO NOT DELETE : old value reference : without mx-autout and w-[]-->
                                <div class="pt-6">

                                    <!--emails importants-->
                                    <!-- To check if there is one class allow the whitespace at the bottom -->
                                    <li v-if="emails[selectedTopic] && emails[selectedTopic]['Important'] && countEmailsInCategoryAndPriority(selectedTopic, 'Important') > 0"
                                        class="">
                                        <div class="px-6 pb-6">
                                            <div class="bg-orange-100 bg-opacity-90 rounded-md">
                                                <div class="flex px-3 py-2">
                                                    <p class="flex-1 text-sm font-semibold leading-6 text-orange-600">
                                                        {{ $t('constants.ruleModalConstants.important') }}</p>
                                                    <!-- ring-1 ring-red-700 ring-opacity-20 -->
                                                    <div class="ml-auto">
                                                        <exclamation-triangle-icon class="w-6 h-6 text-orange-500" />
                                                    </div>
                                                </div>
                                            </div>
                                            <div v-for="(emailsByDate, date) in groupedEmailsByCategoryAndDate('Important')" :key="date">
                                                <div class="pt-3 px-4">
                                                    <div class="relative">
                                                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                            <div class="w-full border-t border-gray-200"></div>
                                                        </div>
                                                        <div class="relative flex justify-center">
                                                            <span class="bg-white px-2 text-xs text-gray-500">{{ date }}</span>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="flex px-4 pt-4">
                                                    <div class="flex">
                                                        <span
                                                            class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-orange-300"><!--OLD DO NOT DELETE : bg-orange-400-->
                                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                                viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                                                class="w-6 h-6 text-white">
                                                                <path stroke-linecap="round" stroke-linejoin="round"
                                                                    d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                                                            </svg>
                                                        </span>
                                                        <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-500" />-->
                                                    </div>
                                                    <div class="ml-6 flex-grow">
                                                        <div class="overflow-hidden border-l-4 border-orange-300  hover:rounded-l-xl" style="overflow: visible;">
                                                            <ul role="list" class="divide-y divide-gray-200">
                                                                <li v-for="item in emailsByDate" :key="item.id" class="px-6 md:py-5 2xl:py-6 hover:bg-opacity-70 grid grid-cols-10 gap-4 items-center" @mouseover="setHoveredItem(item.id)" @mouseleave="clearHoveredItem">
                                                                    <div class="col-span-8 cursor-pointer">
                                                                        <div @click="toggleHiddenParagraph(item.id)">
                                                                            <div class="flex-auto group">
                                                                                <div class="flex gap-x-4">
                                                                                    <div class="flex items-center">
                                                                                        <p class="text-sm font-semibold leading-6 text-orange-700 mr-2">{{ item.name }}</p>
                                                                                        <p class="text-sm leading-6 text-orange-700">{{ item.time }}</p>   
                                                                                    </div> 
                                                                                    <div
                                                                                        class="hidden group-hover:block px-2 py-0.5 bg-orange-300 text-white text-sm shadow rounded-xl">
                                                                                        <div class="flex gap-x-1 items-center">
                                                                                            <svg xmlns="http://www.w3.org/2000/svg"
                                                                                                fill="none" viewBox="0 0 24 24"
                                                                                                stroke-width="1.5"
                                                                                                stroke="currentColor"
                                                                                                class="w-4 h-4">
                                                                                                <path stroke-linecap="round"
                                                                                                    stroke-linejoin="round"
                                                                                                    d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                                                                                            </svg>
                                                                                            <p>{{ $t('constants.userActions.clickToSeeTheSummary') }}</p>
                                                                                        </div>
                                                                                    </div>
                                                                                </div>
                                                                                <p
                                                                                    class="mt-1 text-md text-gray-700 leading-relaxed">
                                                                                    {{ item.description }}</p>
                                                                            </div>
                                                                            <ul v-show="showHiddenParagraphs[item.id]"
                                                                                role="list" class="text-black text-sm/6 pt-2"
                                                                                :ref="el => setParentRef(el, item.id)">
                                                                                <!-- Potential design update : bg-white shadow rounded-xl -->
                                                                                <li v-for="detail in item.details"
                                                                                    :key="detail.id" class="pl-8"
                                                                                    :ref="'hiddenText' + item.id"
                                                                                    :data-text="detail.text">
                                                                                </li>
                                                                            </ul>
                                                                        </div>
                                                                        <div v-if="item.has_attachments" class="flex pt-2.5 gap-x-2">
                                                                            <div
                                                                                v-for="attachment in item.attachments"
                                                                                :key="attachment.attachmentId"
                                                                                class="group flex items-center gap-x-1 bg-gray-100 px-2 py-2 rounded-md hover:bg-gray-600"
                                                                                @click.prevent="() => downloadAttachment(item.id, attachment.attachmentName)"
                                                                            >
                                                                                <component :is="getIconComponent(attachment.attachmentName)" class="w-5 h-5 text-gray-600 group-hover:text-white" />
                                                                                <p class="text-sm text-gray-600 group-hover:text-white">{{ attachment.attachmentName }}</p>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                    <div class="col-span-2">
                                                                        <div class="flex justify-center">
                                                                            <span class="isolate inline-flex rounded-2xl">
                                                                                <div v-show="hoveredItemId === item.id"
                                                                                    class="group action-buttons">
                                                                                    <div class="relative group">
                                                                                        <div
                                                                                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4">
                                                                                            {{ $t('constants.userActions.open') }}
                                                                                        </div>
                                                                                        <button @click="openSeeModal(item)"
                                                                                            type="button"
                                                                                            class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-orange-300 hover:bg-orange-300 focus:z-10">
                                                                                            <eye-icon
                                                                                                class="w-5 h-5 text-orange-400 group-hover:text-white" />
                                                                                        </button>
                                                                                    </div>
                                                                                </div>
                                                                                <div v-show="hoveredItemId === item.id"
                                                                                    class="group action-buttons">
                                                                                    <div class="relative group">
                                                                                        <div
                                                                                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-2">
                                                                                            {{ $t('homePage.read') }}
                                                                                        </div>
                                                                                        <button
                                                                                            @click="markEmailAsRead(item.id)"
                                                                                            type="button"
                                                                                            class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-orange-300 hover:bg-orange-300 focus:z-10">
                                                                                            <check-icon
                                                                                                class="w-5 h-5 text-orange-400 group-hover:text-white" />
                                                                                        </button>
                                                                                    </div>
                                                                                </div>
                                                                                <div v-show="hoveredItemId === item.id"
                                                                                    class="group action-buttons">
                                                                                    <div class="relative group">
                                                                                        <div
                                                                                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                                                                            {{ $t('homePage.answer') }}
                                                                                        </div>
                                                                                        <button @click="openAnswer(item)"
                                                                                            type="button"
                                                                                            class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-orange-300 hover:bg-orange-300 focus:z-10">
                                                                                            <arrow-uturn-left-icon
                                                                                                class="w-5 h-5 text-orange-400 group-hover:text-white" />
                                                                                        </button>
                                                                                    </div>
                                                                                </div>
                                                                                <div v-show="hoveredItemId === item.id"
                                                                                    class="group action-buttons">
                                                                                    <div class="relative group">
                                                                                        <div
                                                                                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-[90px] w-[185px]">
                                                                                            {{ $t('constants.additionalActions') }}
                                                                                        </div>
                                                                                        <Menu as="div"
                                                                                            class="relative inline-block text-left">
                                                                                            <div>
                                                                                                <MenuButton
                                                                                                    @click="toggleTooltip"
                                                                                                    class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-orange-400 ring-1 ring-inset ring-orange-300 hover:bg-orange-300 focus:z-10">
                                                                                                    <ellipsis-horizontal-icon
                                                                                                        class="w-5 h-5 group-hover:text-white text-orange-400 group-active:text-orange-400 group-focus:text-orange focus:text-orange-400" />
                                                                                                </MenuButton>
                                                                                            </div>
                                                                                            <transition
                                                                                                enter-active-class="transition ease-out duration-100"
                                                                                                enter-from-class="transform opacity-0 scale-95"
                                                                                                enter-to-class="transform opacity-100 scale-100"
                                                                                                leave-active-class="transition ease-in duration-75"
                                                                                                leave-from-class="transform opacity-100 scale-100"
                                                                                                leave-to-class="transform opacity-0 scale-95">
                                                                                                <MenuItems
                                                                                                    v-show="isMenuOpen"
                                                                                                    class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none cursor-pointer">
                                                                                                    <div class="py-1">
                                                                                                        <div
                                                                                                            v-if="item.rule">
                                                                                                            <MenuItem
                                                                                                                v-slot="{ active }">
                                                                                                            <a @click.prevent="openRuleEditor(item.rule_id)"
                                                                                                                :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                                <span
                                                                                                                    class="flex gap-x-2 items-center">
                                                                                                                    <svg xmlns="http://www.w3.org/2000/svg"
                                                                                                                        fill="none"
                                                                                                                        viewBox="0 0 24 24"
                                                                                                                        stroke-width="1.5"
                                                                                                                        stroke="currentColor"
                                                                                                                        class="w-4 h-4">
                                                                                                                        <path
                                                                                                                            stroke-linecap="round"
                                                                                                                            stroke-linejoin="round"
                                                                                                                            d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                                                                                    </svg>
                                                                                                                    <span>{{ $t('constants.userAction.changeTheRule') }}</span>
                                                                                                                </span>
                                                                                                            </a>
                                                                                                            </MenuItem>
                                                                                                        </div>
                                                                                                        <div v-else>
                                                                                                            <MenuItem
                                                                                                                v-slot="{ active }">
                                                                                                            <a @click.prevent="openNewRule(item.name, item.email)"
                                                                                                                :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                                <span
                                                                                                                    class="flex gap-x-2 items-center">
                                                                                                                    <svg xmlns="http://www.w3.org/2000/svg"
                                                                                                                        fill="none"
                                                                                                                        viewBox="0 0 24 24"
                                                                                                                        stroke-width="1.5"
                                                                                                                        stroke="currentColor"
                                                                                                                        class="w-4 h-4">
                                                                                                                        <path
                                                                                                                            stroke-linecap="round"
                                                                                                                            stroke-linejoin="round"
                                                                                                                            d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                                                                                    </svg>
                                                                                                                    <span>{{ $t('constants.userActions.createARule') }}</span>
                                                                                                                </span>
                                                                                                            </a>
                                                                                                            </MenuItem>
                                                                                                        </div>
                                                                                                    </div>
                                                                                                    <div class="py-1">
                                                                                                        <MenuItem
                                                                                                            v-slot="{ active }">
                                                                                                        <a @click.prevent="markEmailReplyLater(item)"
                                                                                                            :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                            <span
                                                                                                                class="flex gap-x-2 items-center">
                                                                                                                <svg class="w-4 h-4"
                                                                                                                    viewBox="0 0 28 28"
                                                                                                                    version="1.1"
                                                                                                                    stroke="currentColor"
                                                                                                                    xmlns="http://www.w3.org/2000/svg"
                                                                                                                    xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                                                                    xml:space="preserve"
                                                                                                                    xmlns:serif="http://www.serif.com/"
                                                                                                                    style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                                                                                                                    <path
                                                                                                                        d="M13.435,17.391l-6.783,-6.782m0,0l6.783,-6.783m-6.783,6.783l13.565,0c3.721,0 6.783,3.061 6.783,6.782c0,3.721 -3.062,6.783 -6.783,6.783l-3.391,0"
                                                                                                                        style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                    <path
                                                                                                                        d="M7.783,17.391l-6.783,-6.782m0,0l6.783,-6.783"
                                                                                                                        style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                </svg>
                                                                                                                <span>{{ $t('constants.userActions.replyLater') }}</span>
                                                                                                            </span>
                                                                                                        </a>
                                                                                                        </MenuItem>
                                                                                                    </div>
                                                                                                    <div class="py-1">
                                                                                                        <MenuItem
                                                                                                            v-slot="{ active }">
                                                                                                        <a @click.prevent="transferEmail(item)"
                                                                                                            :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                            <span
                                                                                                                class="flex gap-x-2 items-center">
                                                                                                                <svg class="w-4 h-4"
                                                                                                                    viewBox="0 0 28 28"
                                                                                                                    version="1.1"
                                                                                                                    stroke="currentColor"
                                                                                                                    xmlns="http://www.w3.org/2000/svg"
                                                                                                                    xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                                                                    xml:space="preserve"
                                                                                                                    xmlns:serif="http://www.serif.com/"
                                                                                                                    style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                                                                                                                    <path
                                                                                                                        d="M13.435,10.609l6.783,6.782m0,0l-6.783,6.783m6.783-6.783L6.85,17.391c-3.721,0-6.783-3.061-6.783-6.782c0-3.721,3.062-6.783,6.783-6.783l3.391,0"
                                                                                                                        style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                    <path
                                                                                                                        d="M21.197,10.609l6.783,6.782m0,0l-6.783,6.783"
                                                                                                                        style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                </svg>
                                                                                                                <span>{{ $t('constants.userActions.transfer') }}</span>
                                                                                                            </span>
                                                                                                        </a>
                                                                                                        </MenuItem>
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
                                        </div>
                                    </li>

                                    <!--email informatif-->
                                    <li v-if="emails[selectedTopic] && emails[selectedTopic]['Information'] && countEmailsInCategoryAndPriority(selectedTopic, 'Information') > 0" class="">
                                        <div class="px-6 pb-6">
                                            <div class="bg-blue-100 bg-opacity-90 rounded-md">
                                                <div class="flex px-2 py-2">
                                                    <p class="flex-1 text-sm font-semibold leading-6 text-blue-600">
                                                        {{ $t('constants.ruleModalConstants.informative') }}
                                                    </p>
                                                    <div class="ml-auto">
                                                    <information-circle-icon class="w-6 h-6 text-blue-500" />
                                                    </div>
                                                </div>
                                            </div>
                                            <!-- Emails grouped by date -->
                                            <div v-for="(emailsByDate, date) in groupedEmailsByCategoryAndDate('Information')" :key="date">
                                                <div class="pt-3 px-4">
                                                    <div class="relative">
                                                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                            <div class="w-full border-t border-gray-200"></div>
                                                        </div>
                                                        <div class="relative flex justify-center">
                                                            <span class="bg-white px-2 text-xs text-gray-500">{{ date }}</span>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="flex px-4 pt-4">
                                                    <div class="flex">
                                                        <span
                                                            class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-blue-400 dark:bg-blue-200">
                                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                                viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                                                class="w-6 h-6 text-white">
                                                                <path stroke-linecap="round" stroke-linejoin="round"
                                                                    d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                                                            </svg>
                                                        </span>
                                                        <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-blue-800" />-->
                                                    </div>
                                                    <div class="ml-6 flex-grow">
                                                        <div class="overflow-hidden border-l-4 hover:rounded-l-xl border-blue-300" style="overflow: visible;">
                                                            <ul role="list" class="divide-y divide-gray-200">
                                                                <li v-for="item in emailsByDate" :key="item.id" class="px-6 py-4 2xl:py-5 hover:bg-opacity-70 grid grid-cols-10 gap-4 items-center" @mouseover="setHoveredItem(item.id)" @mouseleave="clearHoveredItem">
                                                                    <!-- Your content -->
                                                                    <div class="col-span-8 cursor-pointer">
                                                                        <div @click="toggleHiddenParagraph(item.id)">
                                                                            <div class="flex-auto group">
                                                                                <div class="flex gap-x-4">
                                                                                    <div class="flex items-center">
                                                                                        <p class="text-sm font-semibold leading-6 text-blue-800 dark:text-white mr-2">{{ item.name }}</p>
                                                                                        <p class="text-sm leading-6 text-blue-800 dark:text-white">{{ item.time }}</p>   
                                                                                    </div> 
                                                                                    <div
                                                                                        class="hidden group-hover:block px-2 py-0.5 bg-blue-300 text-white text-sm shadow rounded-xl">
                                                                                        <div class="flex gap-x-1 items-center">
                                                                                            <svg xmlns="http://www.w3.org/2000/svg"
                                                                                                fill="none" viewBox="0 0 24 24"
                                                                                                stroke-width="1.5"
                                                                                                stroke="currentColor"
                                                                                                class="w-4 h-4">
                                                                                                <path stroke-linecap="round"
                                                                                                    stroke-linejoin="round"
                                                                                                    d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                                                                                            </svg>
                                                                                            <p>{{ $t('constants.userActions.clickToSeeTheSummary') }}</p>
                                                                                        </div>
                                                                                    </div>
                                                                                </div>
                                                                                <p
                                                                                    class="mt-1 text-md text-gray-700 leading-relaxed dark:text-blue-50">
                                                                                    {{ item.description }}</p>
                                                                            </div>
                                                                            <ul v-show="showHiddenParagraphs[item.id]"
                                                                                role="list" class="text-black text-sm/6 pt-2"
                                                                                :ref="el => setParentRef(el, item.id)">
                                                                                <!-- Potential design update : bg-white shadow rounded-xl -->
                                                                                <li v-for="detail in item.details"
                                                                                    :key="detail.id" class="pl-8"
                                                                                    :ref="'hiddenText' + item.id"
                                                                                    :data-text="detail.text">
                                                                                </li>
                                                                            </ul>
                                                                        </div>
                                                                        <div v-if="item.has_attachments" class="flex pt-2.5 gap-x-2">
                                                                            <div
                                                                                v-for="attachment in item.attachments"
                                                                                :key="attachment.attachmentId"
                                                                                class="group flex items-center gap-x-1 bg-gray-100 px-2 py-2 rounded-md hover:bg-gray-600"
                                                                                @click.prevent="() => downloadAttachment(item.id, attachment.attachmentId, attachment.attachmentName)"
                                                                            >
                                                                                <component :is="getIconComponent(attachment.attachmentName)" class="w-5 h-5 text-gray-600 group-hover:text-white" />
                                                                                <p class="text-sm text-gray-600 group-hover:text-white">{{ attachment.attachmentName }}</p>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                    <div class="col-span-2">
                                                                        <div class="flex justify-center">
                                                                            <span class="isolate inline-flex rounded-2xl">
                                                                                <div v-show="hoveredItemId === item.id"
                                                                                    class="group action-buttons">
                                                                                    <div class="relative group">
                                                                                        <div
                                                                                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4 z-40">
                                                                                            {{ $t('constants.userActions.open') }}
                                                                                        </div>
                                                                                        <button @click="openSeeModal(item)"
                                                                                            type="button"
                                                                                            class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                                                                            <eye-icon
                                                                                                class="w-5 h-5 text-blue-400 group-hover:text-white" />
                                                                                        </button>
                                                                                    </div>
                                                                                </div>
                                                                                <div v-show="hoveredItemId === item.id"
                                                                                    class="group action-buttons">
                                                                                    <div class="relative group">
                                                                                        <div
                                                                                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-2">
                                                                                            {{ $t('homePage.read') }}
                                                                                        </div>
                                                                                        <button type="button"
                                                                                            class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                                                                            <check-icon
                                                                                                @click="markEmailAsRead(item.id)"
                                                                                                class="w-5 h-5 text-blue-400 group-hover:text-white" />
                                                                                        </button>
                                                                                    </div>
                                                                                </div>
                                                                                <div v-show="hoveredItemId === item.id"
                                                                                    class="group action-buttons">
                                                                                    <div class="relative group">
                                                                                        <div
                                                                                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                                                                            {{ $t('homePage.answer') }}
                                                                                        </div>
                                                                                        <button @click="openAnswer(item)"
                                                                                            type="button"
                                                                                            class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                                                                            <arrow-uturn-left-icon
                                                                                                class="w-5 h-5 text-blue-400 group-hover:text-white" />
                                                                                        </button>
                                                                                    </div>
                                                                                </div>
                                                                                <div v-show="hoveredItemId === item.id"
                                                                                    class="group action-buttons">
                                                                                    <div class="relative group">
                                                                                        <div
                                                                                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-center text-sm rounded shadow-lg mt-[-45px] -ml-[125px] w-[185px]">
                                                                                            {{ $t('constants.additionalActions') }}
                                                                                        </div>
                                                                                        <Menu as="div"
                                                                                            class="relative inline-block text-left">
                                                                                            <div>
                                                                                                <MenuButton
                                                                                                    @click="toggleTooltip"
                                                                                                    class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-blue-400 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                                                                                    <ellipsis-horizontal-icon
                                                                                                        class="w-5 h-5 group-hover:text-white text-blue-400 group-active:text-blue-400 group-focus:text-red focus:text-blue-400" />
                                                                                                </MenuButton>
                                                                                            </div>
                                                                                            <transition
                                                                                                enter-active-class="transition ease-out duration-100"
                                                                                                enter-from-class="transform opacity-0 scale-95"
                                                                                                enter-to-class="transform opacity-100 scale-100"
                                                                                                leave-active-class="transition ease-in duration-75"
                                                                                                leave-from-class="transform opacity-100 scale-100"
                                                                                                leave-to-class="transform opacity-0 scale-95">
                                                                                                <MenuItems
                                                                                                    v-show="isMenuOpen"
                                                                                                    class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none cursor-pointer">
                                                                                                    <div class="py-1">
                                                                                                        <div
                                                                                                            v-if="item.rule">
                                                                                                            <MenuItem
                                                                                                                v-slot="{ active }">
                                                                                                            <a @click.prevent="openRuleEditor(item.rule_id)"
                                                                                                                :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                                <span
                                                                                                                    class="flex gap-x-2 items-center">
                                                                                                                    <svg xmlns="http://www.w3.org/2000/svg"
                                                                                                                        fill="none"
                                                                                                                        viewBox="0 0 24 24"
                                                                                                                        stroke-width="1.5"
                                                                                                                        stroke="currentColor"
                                                                                                                        class="w-4 h-4">
                                                                                                                        <path
                                                                                                                            stroke-linecap="round"
                                                                                                                            stroke-linejoin="round"
                                                                                                                            d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                                                                                    </svg>
                                                                                                                    <span> {{ $t('constants.userAction.changeTheRule') }}</span>
                                                                                                                </span>
                                                                                                            </a>
                                                                                                            </MenuItem>
                                                                                                        </div>
                                                                                                        <div v-else>
                                                                                                            <MenuItem
                                                                                                                v-slot="{ active }">
                                                                                                            <a @click.prevent="openNewRule(item.name, item.email)"
                                                                                                                :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                                <span
                                                                                                                    class="flex gap-x-2 items-center">
                                                                                                                    <svg xmlns="http://www.w3.org/2000/svg"
                                                                                                                        fill="none"
                                                                                                                        viewBox="0 0 24 24"
                                                                                                                        stroke-width="1.5"
                                                                                                                        stroke="currentColor"
                                                                                                                        class="w-4 h-4">
                                                                                                                        <path
                                                                                                                            stroke-linecap="round"
                                                                                                                            stroke-linejoin="round"
                                                                                                                            d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                                                                                    </svg>
                                                                                                                    <span>{{ $t('constants.userActions.createARule') }}</span>
                                                                                                                </span>
                                                                                                            </a>
                                                                                                            </MenuItem>
                                                                                                        </div>
                                                                                                    </div>
                                                                                                    <div class="py-1">
                                                                                                        <MenuItem
                                                                                                            v-slot="{ active }">
                                                                                                        <a @click.prevent="markEmailReplyLater(item)"
                                                                                                            :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                            <span
                                                                                                                class="flex gap-x-2 items-center">
                                                                                                                <svg class="w-4 h-4"
                                                                                                                    viewBox="0 0 28 28"
                                                                                                                    version="1.1"
                                                                                                                    stroke="currentColor"
                                                                                                                    xmlns="http://www.w3.org/2000/svg"
                                                                                                                    xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                                                                    xml:space="preserve"
                                                                                                                    xmlns:serif="http://www.serif.com/"
                                                                                                                    style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                                                                                                                    <path
                                                                                                                        d="M13.435,17.391l-6.783,-6.782m0,0l6.783,-6.783m-6.783,6.783l13.565,0c3.721,0 6.783,3.061 6.783,6.782c0,3.721 -3.062,6.783 -6.783,6.783l-3.391,0"
                                                                                                                        style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                    <path
                                                                                                                        d="M7.783,17.391l-6.783,-6.782m0,0l6.783,-6.783"
                                                                                                                        style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                </svg>
                                                                                                                <span>{{ $t('constants.userActions.replyLater') }}</span>
                                                                                                            </span>
                                                                                                        </a>
                                                                                                        </MenuItem>
                                                                                                    </div>
                                                                                                    <div class="py-1">
                                                                                                        <MenuItem
                                                                                                            v-slot="{ active }">
                                                                                                        <a @click.prevent="transferEmail(item)"
                                                                                                            :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                            <span
                                                                                                                class="flex gap-x-2 items-center">
                                                                                                                <svg class="w-4 h-4"
                                                                                                                    viewBox="0 0 28 28"
                                                                                                                    version="1.1"
                                                                                                                    stroke="currentColor"
                                                                                                                    xmlns="http://www.w3.org/2000/svg"
                                                                                                                    xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                                                                    xml:space="preserve"
                                                                                                                    xmlns:serif="http://www.serif.com/"
                                                                                                                    style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                                                                                                                    <path
                                                                                                                        d="M13.435,10.609l6.783,6.782m0,0l-6.783,6.783m6.783-6.783L6.85,17.391c-3.721,0-6.783-3.061-6.783-6.782c0-3.721,3.062-6.783,6.783-6.783l3.391,0"
                                                                                                                        style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                    <path
                                                                                                                        d="M21.197,10.609l6.783,6.782m0,0l-6.783,6.783"
                                                                                                                        style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                </svg>
                                                                                                                <span>{{ $t('constants.userActions.transfer') }}</span>
                                                                                                            </span>
                                                                                                        </a>
                                                                                                        </MenuItem>
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
                                        </div>
                                    </li>

                                    <!--email inutiles-->
                                    <!-- add @click="toggleEmailVisibility"-->
                                    <div v-if="emails[selectedTopic] && emails[selectedTopic]['Useless'].filter(email => !email.answer_later) && countEmailsInCategoryAndPriority(selectedTopic, 'Useless') > 0"
                                        class="group/main">
                                        <li class="">
                                            <div class="px-6 pb-6">
                                                <div class="bg-gray-200 bg-opacity-90 rounded-md">
                                                    <div class="flex px-2 py-2">
                                                        <p class="flex-1 text-sm font-semibold leading-6 text-gray-600">
                                                            {{ $t('constants.ruleModalConstants.useless') }}</p>
                                                        <!-- ring-1 ring-red-700 ring-opacity-20 -->
                                                        <div class="ml-auto">
                                                            <trash-icon class="w-6 h-6 text-gray-500" />
                                                        </div>
                                                    </div>
                                                </div>
                                                <!-- Your content -->
                                                <div class="flex px-4 pt-4">
                                                    <div class="flex">
                                                        <span
                                                            class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-400">
                                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                                viewBox="0 0 24 24" stroke-width="1.5"
                                                                stroke="currentColor" class="w-6 h-6 text-white">
                                                                <path stroke-linecap="round" stroke-linejoin="round"
                                                                    d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                                                            </svg>
                                                        </span>
                                                        <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-500" />-->
                                                    </div>
                                                    <div class="ml-6 w-full">
                                                        <div class="overflow-hidden border-l-4 group-hover/main:rounded-l-xl border-gray-400 w-full"
                                                            style="overflow: visible;">
                                                            <ul role="list"
                                                                class="divide-y divide-gray-200 dark:divide-white w-full">
                                                                <li
                                                                    class="px-6 py-5 hover:bg-opacity-70 dark:hover:bg-opacity-100 w-full">
                                                                    <div class="flex gap-x-2">
                                                                        <!-- remove @click="toggleEmailVisibility"-->
                                                                        <p @click="toggleEmailVisibility"
                                                                            class="cursor-pointer"> {{ $t('homePage.youReceived') }}
                                                                            <span
                                                                                class="font-semibold text-gray-900 dark:text-white hover:text-gray-700 w-full">
                                                                                {{
                                                                                    emails[selectedTopic]['Useless'].filter(e =>
                                                                                        !e.answer_later).length }}
                                                                            </span>
                                                                            <span
                                                                                v-if="emails[selectedTopic]['Useless'].filter(email => !email.answer_later).length === 1">
                                                                                {{ $t('homePage.uselessEmail') }}
                                                                            </span>
                                                                            <span v-else>
                                                                                {{ $t('homePage.uselessEmails') }}
                                                                            </span>
                                                                        </p>
                                                                        <div
                                                                            class="hidden group-hover/main:block px-2 py-0.5 bg-gray-400 text-white text-sm shadow rounded-xl">
                                                                            <div class="flex gap-x-1 items-center">
                                                                                <svg xmlns="http://www.w3.org/2000/svg"
                                                                                    fill="none" viewBox="0 0 24 24"
                                                                                    stroke-width="1.5"
                                                                                    stroke="currentColor"
                                                                                    class="w-4 h-4">
                                                                                    <path stroke-linecap="round"
                                                                                        stroke-linejoin="round"
                                                                                        d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                                                                                </svg>
                                                                                <!-- remove @click="toggleEmailVisibility"-->
                                                                                <p @click="toggleEmailVisibility"
                                                                                    class="cursor-pointer">{{ $t('homePage.clickToSeeTheEmail') }}</p>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                    <ul v-if="showEmailDescriptions"
                                                                        class="text-gray-900 text-sm/6 pl-8 divide-y divide-gray-200">
                                                                        <li class="py-5 grid grid-cols-10 w-full"
                                                                            v-for="item in emails[selectedTopic]['Useless'].filter(email => !email.answer_later)"
                                                                            :key="item.id"
                                                                            @mouseover="setHoveredItem(item.id)"
                                                                            @mouseleave="clearHoveredItem">
                                                                            <div class="col-span-8 flex-auto">
                                                                                <div
                                                                                    class="flex items-baseline justify-between gap-x-4">
                                                                                    <div class="flex items-center">
                                                                                        <p class="text-sm font-semibold leading-6 text-gray-800 mr-2">{{ item.name }}</p>
                                                                                        <p class="text-sm leading-6 text-gray-800 mr-2">{{ item.time }}</p>
                                                                                        <p class="text-xs leading-6 text-gray-800 mr-2">{{ item.date }}</p>   
                                                                                    </div>
                                                                                </div>
                                                                                <p>{{ item.description }}</p>
                                                                            </div>
                                                                            <div class="col-span-2 pt-2">
                                                                                <div class="flex justify-center">
                                                                                    <span
                                                                                        class="isolate inline-flex rounded-2xl">
                                                                                        <div v-show="hoveredItemId === item.id"
                                                                                            class="group action-buttons">
                                                                                            <div class="relative group">
                                                                                                <div
                                                                                                    class="absolute hidden group-hover:block bg-black text-white text-sm py-2 px-4 rounded shadow-lg mt-[-45px] -ml-4">
                                                                                                    {{ $t('constants.userActions.open') }}
                                                                                                </div>
                                                                                                <button
                                                                                                    @click.stop="openSeeModal(item)"
                                                                                                    type="button"
                                                                                                    class="inline-flex items-center px-2 py-1.5 rounded-l-2xl text-gray-400 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                                                                                    <eye-icon
                                                                                                        class="w-5 h-5 text-gray-500 group-hover:text-white" />
                                                                                                </button>
                                                                                            </div>
                                                                                        </div>
                                                                                        <div v-show="hoveredItemId === item.id"
                                                                                            class="group action-buttons">
                                                                                            <div class="relative group">
                                                                                                <div
                                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-6">
                                                                                                    {{ $t('homePage.block') }}
                                                                                                </div>
                                                                                                <button type="button"
                                                                                                    class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                                                                                    <HandRaisedIcon
                                                                                                        @click.stop="setRuleBlockForSender(item)"
                                                                                                        class="w-5 h-5 text-gray-500 group-hover:text-white" />
                                                                                                </button>
                                                                                            </div>
                                                                                        </div>
                                                                                        <div v-show="hoveredItemId === item.id"
                                                                                            class="group action-buttons">
                                                                                            <div class="relative group">
                                                                                                <div
                                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-6">
                                                                                                    {{ $t('constants.userActions.archive') }}
                                                                                                </div>
                                                                                                <button type="button"
                                                                                                    class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                                                                                    <TrashIcon
                                                                                                        @click.stop="deleteEmail(item.id)"
                                                                                                        class="w-5 h-5 text-gray-500 group-hover:text-white" />
                                                                                                </button>
                                                                                            </div>
                                                                                        </div>
                                                                                        <div v-show="hoveredItemId === item.id"
                                                                                            class="group action-buttons">
                                                                                            <div class="relative group">
                                                                                                <div
                                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                                                                                    {{ $t('homePage.answer') }}
                                                                                                </div>
                                                                                                <button
                                                                                                    @click.stop="openAnswer(item)"
                                                                                                    type="button"
                                                                                                    class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                                                                                    <arrow-uturn-left-icon
                                                                                                        class="w-5 h-5 text-gray-500 group-hover:text-white" />
                                                                                                </button>
                                                                                            </div>
                                                                                        </div>
                                                                                        <div v-show="hoveredItemId === item.id"
                                                                                            class="group action-buttons cursor-pointer">
                                                                                            <div class="relative group">
                                                                                                <div
                                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-[125px] w-[185px]">
                                                                                                    {{ $t('constants.additionalActions') }}
                                                                                                </div>
                                                                                                <Menu as="div"
                                                                                                    class="relative inline-block text-left">
                                                                                                    <div>
                                                                                                        <MenuButton
                                                                                                            @click="toggleTooltip"
                                                                                                            class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-gray-500 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                                                                                            <ellipsis-horizontal-icon
                                                                                                                class="w-5 h-5 group-hover:text-white text-gray-500 group-active:text-gray-500 group-focus:text-red focus:text-gray-500" />
                                                                                                        </MenuButton>
                                                                                                    </div>
                                                                                                    <transition
                                                                                                        enter-active-class="transition ease-out duration-100"
                                                                                                        enter-from-class="transform opacity-0 scale-95"
                                                                                                        enter-to-class="transform opacity-100 scale-100"
                                                                                                        leave-active-class="transition ease-in duration-75"
                                                                                                        leave-from-class="transform opacity-100 scale-100"
                                                                                                        leave-to-class="transform opacity-0 scale-95">
                                                                                                        <MenuItems
                                                                                                            v-show="isMenuOpen"
                                                                                                            class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none">
                                                                                                            <div
                                                                                                                class="py-1">
                                                                                                                <div
                                                                                                                    v-if="item.rule">
                                                                                                                    <MenuItem
                                                                                                                        v-slot="{ active }">
                                                                                                                    <a @click.prevent="openRuleEditor(item.rule_id)"
                                                                                                                        :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                                        <span
                                                                                                                            class="flex gap-x-2 items-center">
                                                                                                                            <svg xmlns="http://www.w3.org/2000/svg"
                                                                                                                                fill="none"
                                                                                                                                viewBox="0 0 24 24"
                                                                                                                                stroke-width="1.5"
                                                                                                                                stroke="currentColor"
                                                                                                                                class="w-4 h-4">
                                                                                                                                <path
                                                                                                                                    stroke-linecap="round"
                                                                                                                                    stroke-linejoin="round"
                                                                                                                                    d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                                                                                            </svg>
                                                                                                                            <span>{{ $t('constants.userAction.changeTheRule') }}</span>
                                                                                                                        </span>
                                                                                                                    </a>
                                                                                                                    </MenuItem>
                                                                                                                </div>
                                                                                                                <div
                                                                                                                    v-else>
                                                                                                                    <MenuItem
                                                                                                                        v-slot="{ active }">
                                                                                                                    <a @click.prevent="openNewRule(item.name, item.email)"
                                                                                                                        :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                                        <span
                                                                                                                            class="flex gap-x-2 items-center">
                                                                                                                            <svg xmlns="http://www.w3.org/2000/svg"
                                                                                                                                fill="none"
                                                                                                                                viewBox="0 0 24 24"
                                                                                                                                stroke-width="1.5"
                                                                                                                                stroke="currentColor"
                                                                                                                                class="w-4 h-4">
                                                                                                                                <path
                                                                                                                                    stroke-linecap="round"
                                                                                                                                    stroke-linejoin="round"
                                                                                                                                    d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                                                                                            </svg>
                                                                                                                            <span>{{ $t('constants.userActions.createARule') }}</span>
                                                                                                                        </span>
                                                                                                                    </a>
                                                                                                                    </MenuItem>
                                                                                                                </div>
                                                                                                            </div>
                                                                                                            <div
                                                                                                                class="py-1">
                                                                                                                <MenuItem
                                                                                                                    v-slot="{ active }">
                                                                                                                <a @click.prevent="markEmailReplyLater(item)"
                                                                                                                    :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                                    <span
                                                                                                                        class="flex gap-x-2 items-center">
                                                                                                                        <svg class="w-4 h-4"
                                                                                                                            viewBox="0 0 28 28"
                                                                                                                            version="1.1"
                                                                                                                            stroke="currentColor"
                                                                                                                            xmlns="http://www.w3.org/2000/svg"
                                                                                                                            xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                                                                            xml:space="preserve"
                                                                                                                            xmlns:serif="http://www.serif.com/"
                                                                                                                            style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                                                                                                                            <path
                                                                                                                                d="M13.435,17.391l-6.783,-6.782m0,0l6.783,-6.783m-6.783,6.783l13.565,0c3.721,0 6.783,3.061 6.783,6.782c0,3.721 -3.062,6.783 -6.783,6.783l-3.391,0"
                                                                                                                                style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                            <path
                                                                                                                                d="M7.783,17.391l-6.783,-6.782m0,0l6.783,-6.783"
                                                                                                                                style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                        </svg>
                                                                                                                        <span>{{ $t('constants.userActions.replyLater') }}</span>
                                                                                                                    </span>
                                                                                                                </a>
                                                                                                                </MenuItem>
                                                                                                            </div>

                                                                                                            <div
                                                                                                                class="py-1">
                                                                                                                <MenuItem
                                                                                                                    v-slot="{ active }">
                                                                                                                <a @click.prevent="transferEmail(item)"
                                                                                                                    :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                                    <span
                                                                                                                        class="flex gap-x-2 items-center">
                                                                                                                        <svg class="w-4 h-4"
                                                                                                                            viewBox="0 0 28 28"
                                                                                                                            version="1.1"
                                                                                                                            stroke="currentColor"
                                                                                                                            xmlns="http://www.w3.org/2000/svg"
                                                                                                                            xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                                                                            xml:space="preserve"
                                                                                                                            xmlns:serif="http://www.serif.com/"
                                                                                                                            style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                                                                                                                            <path
                                                                                                                                d="M13.435,10.609l6.783,6.782m0,0l-6.783,6.783m6.783-6.783L6.85,17.391c-3.721,0-6.783-3.061-6.783-6.782c0-3.721,3.062-6.783,6.783-6.783l3.391,0"
                                                                                                                                style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                            <path
                                                                                                                                d="M21.197,10.609l6.783,6.782m0,0l-6.783,6.783"
                                                                                                                                style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                        </svg>
                                                                                                                        <span>{{ $t('constants.userActions.transfer') }}</span>
                                                                                                                    </span>
                                                                                                                </a>
                                                                                                                </MenuItem>
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
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </li>
                                    </div>

                                    <!--Actions sur les mails open,read,answer,more -->
                                    <div v-if="readEmailsInSelectedTopic().length > 0" class="group/main">
                                        <li class="">
                                            <div class="px-6 pb-6"><!--bg-emerald-50 bg-opacity-60-->
                                                <div class="bg-stone-200 bg-opacity-90 rounded-md">
                                                    <div class="flex px-2 py-2">
                                                        <p
                                                            class="flex-1 text-sm font-semibold leading-6 text-stone-600 px-4">
                                                            Lu</p>
                                                        <!-- ring-1 ring-red-700 ring-opacity-20 -->
                                                        <div class="ml-auto">
                                                            <CheckIcon class="w-6 h-6 text-stone-500" />
                                                        </div>
                                                    </div>
                                                </div>

                                                <!-- Your content -->
                                                <div class="flex px-4 pt-4">
                                                    <div class="flex">
                                                        <span
                                                            class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-stone-400">
                                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                                viewBox="0 0 24 24" stroke-width="1.5"
                                                                stroke="currentColor" class="w-6 h-6 text-white">
                                                                <path stroke-linecap="round" stroke-linejoin="round"
                                                                    d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                                                            </svg>
                                                        </span>
                                                        <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-500" />-->
                                                    </div>

                                                    <div class="ml-6 w-full">
                                                        <!-- To check : strange w-full not necessary in grey but it must be here to have the correct space for readEmailsInSelectedTopic -->
                                                        <div class="overflow-hidden border-l-4 group-hover/main:rounded-l-xl border-stone-400 w-full"
                                                            style="overflow: visible;">
                                                            <ul role="list"
                                                                class="divide-y divide-gray-200 dark:divide-white w-full">
                                                                <li
                                                                    class="px-6 py-5 hover:bg-opacity-70 dark:hover:bg-opacity-100 w-full">

                                                                    <div class="flex group gap-x-2">

                                                                        <p @click="toggleReadEmailVisibility"
                                                                            class="cursor-pointer">
                                                                            {{ $t('homePage.youReadRecently') }}
                                                                            <span
                                                                                class="font-semibold text-gray-900 dark:text-white hover:text-gray-700">
                                                                                {{ readEmailsInSelectedTopic().length }}
                                                                            </span>
                                                                            <span
                                                                                v-if="readEmailsInSelectedTopic().length === 1">
                                                                                {{ $t('homePage.email') }}
                                                                            </span>
                                                                            <span v-else>{{ $t('homePage.emails') }}</span> {{ $t('homePage.iAm') }}
                                                                            <span class="font-medium">{{ $t('homePage.goingToCleanAutomatically') }}</span> {{ $t('homePage.theEmailsYouHaveRead') }}
                                                                        </p>

                                                                        <div
                                                                            class="hidden group-hover/main:block px-2 py-0.5 bg-stone-400 text-white text-sm shadow rounded-xl">
                                                                            <div class="flex gap-x-1 items-center">
                                                                                <svg xmlns="http://www.w3.org/2000/svg"
                                                                                    fill="none" viewBox="0 0 24 24"
                                                                                    stroke-width="1.5"
                                                                                    stroke="currentColor"
                                                                                    class="w-4 h-4">
                                                                                    <path stroke-linecap="round"
                                                                                        stroke-linejoin="round"
                                                                                        d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                                                                                </svg>
                                                                                <p @click="toggleReadEmailVisibility"
                                                                                    class="cursor-pointer">{{ $t('homePage.clickToSeeTheEmail') }}</p>
                                                                            </div>
                                                                        </div>

                                                                    </div>
                                                                    
                                                                    <ul v-if="showEmailReadDescriptions"
                                                                        class="text-gray-900 text-sm/6 pl-8 divide-y divide-gray-300 w-full">
                                                                        <li class="py-5 grid grid-cols-10 w-full"
                                                                            v-for="item in readEmailsInSelectedTopic()"
                                                                            :key="item.id"
                                                                            @mouseover="setHoveredItem(item.id)"
                                                                            @mouseleave="clearHoveredItem">

                                                                            <div class="col-span-8 cursor-pointer"
                                                                                @click="toggleHiddenParagraph(item.id)">
                                                                                <div class="flex-auto group">
                                                                                    <div class="flex gap-x-4">
                                                                                        <div class="flex items-center">
                                                                                            <p class="text-sm font-semibold leading-6 text-stone-700 mr-2">{{ item.name }}</p>
                                                                                            <p class="text-sm leading-6 text-stone-700 mr-2">{{ item.time }}</p>   
                                                                                            <p class="text-xs leading-6 text-stone-700">{{ item.date }}</p> 
                                                                                        </div>
                                                                                        <div
                                                                                            class="hidden group-hover:block px-2 py-0.5 bg-stone-400 text-white text-sm shadow rounded-xl">
                                                                                            <div
                                                                                                class="flex gap-x-1 items-center">
                                                                                                <svg xmlns="http://www.w3.org/2000/svg"
                                                                                                    fill="none"
                                                                                                    viewBox="0 0 24 24"
                                                                                                    stroke-width="1.5"
                                                                                                    stroke="currentColor"
                                                                                                    class="w-4 h-4">
                                                                                                    <path
                                                                                                        stroke-linecap="round"
                                                                                                        stroke-linejoin="round"
                                                                                                        d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                                                                                                </svg>
                                                                                                <p>{{ $t('constants.userActions.clickToSeeTheSummary') }}</p>
                                                                                            </div>
                                                                                        </div>
                                                                                    </div>
                                                                                    <p
                                                                                        class="mt-1 text-md text-gray-700 leading-relaxed">
                                                                                        {{ item.description }}</p>
                                                                                </div>
                                                                                <ul v-show="showHiddenParagraphs[item.id]"
                                                                                    role="list"
                                                                                    class="text-black text-sm/6 pt-2"
                                                                                    :ref="el => setParentRef(el, item.id)">
                                                                                    <!-- Potential design update : bg-white shadow rounded-xl -->
                                                                                    <li v-for="detail in item.details"
                                                                                        :key="detail.id" class="pl-8"
                                                                                        :ref="'hiddenText' + item.id"
                                                                                        :data-text="detail.text">
                                                                                    </li>
                                                                                </ul>
                                                                            </div>

                                                                            <div class="col-span-2 pt-2">
                                                                                <div class="flex justify-center">
                                                                                    <span
                                                                                        class="isolate inline-flex rounded-2xl">
                                                                                        <div v-show="hoveredItemId === item.id"
                                                                                            class="group action-buttons">
                                                                                            <div class="relative group">
                                                                                                <div
                                                                                                    class="absolute hidden group-hover:block bg-black text-white text-sm py-2 px-4 rounded shadow-lg mt-[-45px] -ml-4">
                                                                                                    {{ $t('constants.userActions.open') }}
                                                                                                </div>
                                                                                                <button
                                                                                                    @click.stop="openSeeModal(item)"
                                                                                                    type="button"
                                                                                                    class="inline-flex items-center px-2 py-1.5 rounded-l-2xl text-stone-400 ring-1 ring-inset ring-stone-400 hover:bg-stone-400 focus:z-10">
                                                                                                    <eye-icon
                                                                                                        class="w-5 h-5 text-stone-500 group-hover:text-white" />
                                                                                                </button>
                                                                                            </div>
                                                                                        </div>
                                                                                        <div v-show="hoveredItemId === item.id"
                                                                                            class="group action-buttons">
                                                                                            <div class="relative group">
                                                                                                <div
                                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-25 w-[80px]">
                                                                                                    {{ $t('homePage.unread') }}
                                                                                                </div>
                                                                                                <button
                                                                                                    @click="markEmailAsUnread(item.id)"
                                                                                                    type="button"
                                                                                                    class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-stone-400 hover:bg-stone-400 focus:z-10">
                                                                                                    <check-icon
                                                                                                        class="w-5 h-5 text-stone-500 group-hover:text-white" />
                                                                                                </button>
                                                                                            </div>
                                                                                        </div>
                                                                                        <div v-show="hoveredItemId === item.id"
                                                                                            class="group action-buttons">
                                                                                            <div class="relative group">
                                                                                                <div
                                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-6">
                                                                                                    {{ $t('constants.userActions.archive') }}
                                                                                                </div>
                                                                                                <button type="button"
                                                                                                    class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-stone-400 hover:bg-stone-400 focus:z-10">
                                                                                                    <TrashIcon
                                                                                                        @click.stop="deleteEmail(item.id)"
                                                                                                        class="w-5 h-5 text-stone-500 group-hover:text-white" />
                                                                                                </button>
                                                                                            </div>
                                                                                        </div>
                                                                                        <div v-show="hoveredItemId === item.id"
                                                                                            class="group action-buttons">
                                                                                            <div class="relative group">
                                                                                                <div
                                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                                                                                    {{ $t('homePage.answer') }}
                                                                                                </div>
                                                                                                <button
                                                                                                    @click.stop="openAnswer(item)"
                                                                                                    type="button"
                                                                                                    class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-stone-400 hover:bg-stone-400 focus:z-10">
                                                                                                    <arrow-uturn-left-icon
                                                                                                        class="w-5 h-5 text-stone-500 group-hover:text-white" />
                                                                                                </button>
                                                                                            </div>
                                                                                        </div>
                                                                                        <div v-show="hoveredItemId === item.id"
                                                                                            class="group action-buttons">
                                                                                            <div
                                                                                                class="cursor-pointer relative group">
                                                                                                <div
                                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-[125px] w-[185px]">
                                                                                                    {{ $t('constants.additionalActions') }}
                                                                                                </div>
                                                                                                <Menu as="div"
                                                                                                    class="relative inline-block text-left">
                                                                                                    <div>
                                                                                                        <MenuButton
                                                                                                            @click="toggleTooltip"
                                                                                                            class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-stone-500 ring-1 ring-inset ring-stone-400 hover:bg-stone-400 focus:z-10">
                                                                                                            <ellipsis-horizontal-icon
                                                                                                                class="w-5 h-5 group-hover:text-white text-stone-500 group-active:text-stone-500 group-focus:text-red focus:text-stone-500" />
                                                                                                        </MenuButton>
                                                                                                    </div>
                                                                                                    <transition
                                                                                                        enter-active-class="transition ease-out duration-100"
                                                                                                        enter-from-class="transform opacity-0 scale-95"
                                                                                                        enter-to-class="transform opacity-100 scale-100"
                                                                                                        leave-active-class="transition ease-in duration-75"
                                                                                                        leave-from-class="transform opacity-100 scale-100"
                                                                                                        leave-to-class="transform opacity-0 scale-95">
                                                                                                        <MenuItems
                                                                                                            v-show="isMenuOpen"
                                                                                                            class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none">
                                                                                                            <div
                                                                                                                class="py-1">
                                                                                                                <div
                                                                                                                    v-if="item.rule">
                                                                                                                    <MenuItem
                                                                                                                        v-slot="{ active }">
                                                                                                                    <a @click.prevent="openRuleEditor(item.rule_id)"
                                                                                                                        :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                                        <span
                                                                                                                            class="flex gap-x-2 items-center">
                                                                                                                            <svg xmlns="http://www.w3.org/2000/svg"
                                                                                                                                fill="none"
                                                                                                                                viewBox="0 0 24 24"
                                                                                                                                stroke-width="1.5"
                                                                                                                                stroke="currentColor"
                                                                                                                                class="w-4 h-4">
                                                                                                                                <path
                                                                                                                                    stroke-linecap="round"
                                                                                                                                    stroke-linejoin="round"
                                                                                                                                    d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                                                                                            </svg>
                                                                                                                            <span>{{ $t('constants.userAction.changeTheRule') }}</span>
                                                                                                                        </span>
                                                                                                                    </a>
                                                                                                                    </MenuItem>
                                                                                                                </div>
                                                                                                                <div
                                                                                                                    v-else>
                                                                                                                    <MenuItem
                                                                                                                        v-slot="{ active }">
                                                                                                                    <a @click.prevent="openNewRule(item.name, item.email)"
                                                                                                                        :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                                        <span
                                                                                                                            class="flex gap-x-2 items-center">
                                                                                                                            <svg xmlns="http://www.w3.org/2000/svg"
                                                                                                                                fill="none"
                                                                                                                                viewBox="0 0 24 24"
                                                                                                                                stroke-width="1.5"
                                                                                                                                stroke="currentColor"
                                                                                                                                class="w-4 h-4">
                                                                                                                                <path
                                                                                                                                    stroke-linecap="round"
                                                                                                                                    stroke-linejoin="round"
                                                                                                                                    d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                                                                                                            </svg>
                                                                                                                            <span>{{ $t('constants.userActions.createARule') }}</span>
                                                                                                                        </span>
                                                                                                                    </a>
                                                                                                                    </MenuItem>
                                                                                                                </div>
                                                                                                            </div>
                                                                                                            <div
                                                                                                                class="py-1">
                                                                                                                <MenuItem
                                                                                                                    v-slot="{ active }">
                                                                                                                <a @click.prevent="markEmailReplyLater(item)"
                                                                                                                    :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                                    <span
                                                                                                                        class="flex gap-x-2 items-center">
                                                                                                                        <svg class="w-4 h-4"
                                                                                                                            viewBox="0 0 28 28"
                                                                                                                            version="1.1"
                                                                                                                            stroke="currentColor"
                                                                                                                            xmlns="http://www.w3.org/2000/svg"
                                                                                                                            xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                                                                            xml:space="preserve"
                                                                                                                            xmlns:serif="http://www.serif.com/"
                                                                                                                            style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                                                                                                                            <path
                                                                                                                                d="M13.435,17.391l-6.783,-6.782m0,0l6.783,-6.783m-6.783,6.783l13.565,0c3.721,0 6.783,3.061 6.783,6.782c0,3.721 -3.062,6.783 -6.783,6.783l-3.391,0"
                                                                                                                                style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                            <path
                                                                                                                                d="M7.783,17.391l-6.783,-6.782m0,0l6.783,-6.783"
                                                                                                                                style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                        </svg>
                                                                                                                        <span>{{ $t('constants.userActions.replyLater') }}</span>
                                                                                                                    </span>
                                                                                                                </a>
                                                                                                                </MenuItem>
                                                                                                            </div>
                                                                                                            <div
                                                                                                                class="py-1">
                                                                                                                <MenuItem
                                                                                                                    v-slot="{ active }">
                                                                                                                <a @click.prevent="transferEmail(item)"
                                                                                                                    :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                                                                                    <span
                                                                                                                        class="flex gap-x-2 items-center">
                                                                                                                        <svg class="w-4 h-4"
                                                                                                                            viewBox="0 0 28 28"
                                                                                                                            version="1.1"
                                                                                                                            stroke="currentColor"
                                                                                                                            xmlns="http://www.w3.org/2000/svg"
                                                                                                                            xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                                                                            xml:space="preserve"
                                                                                                                            xmlns:serif="http://www.serif.com/"
                                                                                                                            style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                                                                                                                            <path
                                                                                                                                d="M13.435,10.609l6.783,6.782m0,0l-6.783,6.783m6.783-6.783L6.85,17.391c-3.721,0-6.783-3.061-6.783-6.782c0-3.721,3.062-6.783,6.783-6.783l3.391,0"
                                                                                                                                style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                            <path
                                                                                                                                d="M21.197,10.609l6.783,6.782m0,0l-6.783,6.783"
                                                                                                                                style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                                                                        </svg>
                                                                                                                        <span>{{ $t('constants.userActions.transfer') }}</span>
                                                                                                                    </span>
                                                                                                                </a>
                                                                                                                </MenuItem>
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
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </li>
                                    </div>
                                </div>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- UNCOMMENT TO SEPARATE BUTTON FROM DIV TO FOLD/UNFOLD -->
               <div class="bg-gray-50 ring-1 shadow-sm ring-black ring-opacity-5 h-full flex flex-col relative"> 
               <!--<div class="bg-gray-50 ring-1 shadow-sm ring-black ring-opacity-5 h-full flex flex-col"> -->
                        
                            <!--Bouton de transition style 1 -->
                    <!--    <div class="p-4 flex justify-end">
                                <button @click="toggleVisibility" class="bg-gray-200 text-gray-500 p-2 rounded-full items-center inline-flex">
                                    <svg v-if="isHidden" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="m18.75 4.5-7.5 7.5 7.5 7.5m-6-15L5.25 12l7.5 7.5" />
                                    </svg>
                                    <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="m5.25 4.5 7.5 7.5-7.5 7.5m6-15 7.5 7.5-7.5 7.5" />
                                    </svg>
                                </button>
                            </div> -->

                        <!--Bouton de transition style 2 -->
                        
                        <!-- <div class="p-4 flex w-full">
                                <button @click="toggleVisibility"
                                    class="bg-gray-200 text-gray-500 px-4 py-2 rounded w-full items-center inline-flex pr-10">
                                    <svg v-if="isHidden" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="m18.75 4.5-7.5 7.5 7.5 7.5m-6-15L5.25 12l7.5 7.5" />
                                    </svg>
                                    <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="m5.25 4.5 7.5 7.5-7.5 7.5m6-15 7.5 7.5-7.5 7.5" />
                                    </svg>
                                </button>
                            </div> -->

                    <!--<transition name="slide">-->
                        <div v-show="!isHidden" class="w-[325px] 2xl:w-[525px] flex-grow">
                            <div class="flex flex-col h-full">
                                <div class="flex-grow">
                                    <div class="flex p-5">
                                        <div class="mr-4 flex-shrink-0 self-center">
                                            <span
                                                class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                                    stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                                    <path stroke-linecap="round" stroke-linejoin="round"
                                                        d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                                                </svg>
                                            </span>
                                        </div>
                                        <div>
                                            <p class="mt-1" id="animated-text" ref="animatedText"></p>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex flex-col justify-end h-[160px] border-t">
                                    <textarea id="dynamicTextarea" @keydown.enter="handleEnterKey"
                                            @input="adjustHeight" v-model="textareaValue"
                                            class="overflow-y-hidden flex flex-1 pt-3 pl-5 w-full border-transparent bg-transparent text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 focus:border-transparent focus:bg-transparent focus:ring-0"
                                            :placeholder="$t('constants.instruction')">
                                    </textarea>
                                    <div class="flex justify-end m-3">
                                        <button type="button" class="w-[80px] rounded bg-gray-700 px-2.5 py-1.5 text-sm text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">{{ $t('constants.userActions.send') }}</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    <!--</transition>-->
                </div>

            </div>
        </div>

        <!-- Category Modal -->
        <NewCategoryModal :isOpen="isModalOpen" :errorMessage="modalErrorMessage" @closeModal="closeModal"
            @addCategory="handleAddCategory" />
        <UpdateCategoryModal :isOpen="isModalUpdateOpen" :errorMessage="modalUpdateErrorMessage"
            :category="categoryToUpdate" @closeModal="closeUpdateModal" @updateCategory="handleUpdateCategory"
            @deleteCategory="handleCategoryDelete" />
        <ModalSeeMail :isOpen="isModalSeeOpen" :email="selectedEmail" @closeSeeModal="closeSeeModal"
            @openAnswer="openAnswer" @openRuleEditor="openRuleEditor" @openNewRule="openNewRule" @markEmailAsRead="markEmailAsRead" @markEmailReplyLater="markEmailReplyLater" @transferEmail="transferEmail" />
    </div>
</template>

<script setup>
import { API_BASE_URL } from '@/main.jts';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import {
  Combobox,
  ComboboxButton,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
} from '@headlessui/vue';

// Use i18n
const { t } = useI18n();


// Variables to display a notification
let showNotification = ref(false);
let selectedEmailId = ref('');
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
let timerId = ref(null);

const router = useRouter();
let animatedText = ref('');
let showHiddenParagraphs = ref({});
let showModal = ref(false);
let isModalOpen = ref(false);
let isModalSeeOpen = ref(false);
let isModalUpdateOpen = ref(false);
let modalErrorMessage = ref('');
let modalUpdateErrorMessage = ref('');
let categoryToUpdate = ref(null);
let categories = ref([]);
let selectedEmail = ref(null);
let hoveredItemId = ref(null);
let oldCategoryName = ref('');
let showEmailDescriptions = ref(false);
let showEmailReadDescriptions = ref(false);
let isMenuOpen = ref(true);
let emails = ref({});
let scrollableDiv = ref(null);
let selectedTopic = ref('');
let animationTriggered = ref([false, false, false]);
let bgColor = ref('');
bgColor = localStorage.getItem('bgColor');
let parentElementRefs = ref({});
let totalUnread = ref(0);
let initialAnimationDone = ref(false);
let isModalWarningCategoryOpen = ref(false)
let nbRulesAssociated = ref(null);
const happy_icon = ref(require('@/assets/happy.png'));
let lockEmailsAccess = ref(false);


let isHidden = ref(false);

const toggleVisibility = () => {
    isHidden.value = !isHidden.value;
};

const downloadAttachment = async (emailId, attachmentName) => {
    try {
        const response = await fetchWithTokenv2(`${API_BASE_URL}user/emails/${emailId}/attachments/${attachmentName}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const attachmentData = await response.blob(); // Use response.blob() for binary data
        const url = window.URL.createObjectURL(attachmentData);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', attachmentName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error('Failed to download attachment:', error.message);
        backgroundColor.value = 'bg-red-300';
        notificationTitle.value = 'Échec de téléchargement de la pièce jointe';
        notificationMessage.value = error.message;
        displayPopup();
    }
};

const getIconComponent = (fileName) => {
  const extension = fileName.split('.').pop().toLowerCase();
  if (['png', 'jpg', 'jpeg', 'gif'].includes(extension)) {
    return CameraIcon;
  } else if (['pdf', 'doc', 'docx', 'xls', 'xlsx'].includes(extension)) {
    return DocumentIcon;
  } else {
    return DocumentIcon; // Default icon for other file types
  }
};

onMounted(async () => {
    document.addEventListener("keydown", handleKeyDown);
    getBackgroundColor();

    // Wait for fetchData completion
    await new Promise(resolve => {
        fetchData().then(() => {
            resolve();
        });
        //animateText("Calcul des mails non lus en cours");
    });

    setInterval(async () => {
        try {
            fetchEmails();
        } catch (error) {
            console.log("An error occured", error)
        }
    }, 15000);
});

function handleKeyDown(event) {
    if (event.key === 'Escape' && isModalWarningCategoryOpen.value) {
        closeWarningCategoryModal();
    }
}

function getNumberUnreadMail(emailData) {
    let totalUnread = 0;

    for (const category in emailData) {
        for (const subcategory in emailData[category]) {
            const emailsInSubcategory = emailData[category][subcategory];
            if (subcategory != 'Useless') {
                for (const email of emailsInSubcategory) {
                    if (!email.read && !email.answer_later) {
                        totalUnread++;
                    }
                }
            }
        }
    }
    return totalUnread;
}

function getTextNumberUnreadMail(totalUnread) {
    if (totalUnread === 0) {
        return `${t('homePage.youDidNotReceiveNewEmail')}`;
    } else if (totalUnread === 1) {
        return `${t('homePage.youReceived')} ${totalUnread} ${t('homePage.newEmail')}`;
    } else {
        return `${t('homePage.youReceived')} ${totalUnread} ${t('homePage.newEmails')}`;
    }
}


function animateText(text) {
    // Clear text
    try {
        animatedText.value.textContent = '';
        let target = animatedText.value;
        let characters = text.split("");
        let currentIndex = 0;

        // Used to create an animation
        const interval = setInterval(() => {
            if (currentIndex < characters.length) {
                target.textContent += characters[currentIndex];
                currentIndex++;
            } else {
                clearInterval(interval);
            }
        }, 30);
    } catch (error) {
        // TODO: Remove this try-catch with a cleaner method
        console.error('An error occurred:', error);
    }
}

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

function setParentRef(el, itemId) {
    // Ensure the object exists before trying to set a property
    if (el) {
        parentElementRefs.value[itemId] = el;
    }
}

// To redirect to the page rules to edit a rule
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

function setHoveredItem(id) {
    hoveredItemId.value = id;
    //scrollToBottom();
}

function clearHoveredItem() {
    hoveredItemId.value = null;
}

function toggleTooltip() {
    isMenuOpen.value = true;
}

async function markEmailAsUnread(emailId) {
    lockEmailsAccess.value = true;
    updateEmailUnreadStatus(emailId);

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/mark_unread/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.read != false) {
            console.log("RESPONSE markEmailAsUnread", response);
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle =  t('homePage.markEmailUnreadFailure');
            notificationMessage = response;
            displayPopup();
        }
    } catch (error) {
        console.error('Error in markEmailAsUnread:', error.message);
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('homePage.markEmailUnreadFailure');
        notificationMessage = error.message;
        displayPopup();
    }
    lockEmailsAccess.value = false;
}
async function markEmailAsRead(emailId) {
    lockEmailsAccess.value = true;
    updateEmailReadStatus(emailId);

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
    lockEmailsAccess.value = false;
}

function updateEmailReadStatus(emailId) {
    // Iterate over each category in the emails object
    for (const category in emails.value) {
        if (Object.hasOwnProperty.call(emails.value, category)) {
            // Iterate over each subcategory within the category
            for (const subcategory in emails.value[category]) {
                if (Array.isArray(emails.value[category][subcategory])) {
                    // Find the index of the email with the given ID in the current subcategory's array
                    const emailIndex = emails.value[category][subcategory].findIndex(email => email.id === emailId);
                    if (emailIndex !== -1) {
                        // Email found, update its read status
                        emails.value[category][subcategory][emailIndex].read = true;
                        updateNumberUnreadEmails();
                        return; // Stop the function as we've found and updated the email
                    }
                }
            }
        }
    }
}

function updateEmailUnreadStatus(emailId) {
    for (const category in emails.value) {
        if (Object.hasOwnProperty.call(emails.value, category)) {
            for (const subcategory in emails.value[category]) {
                if (Array.isArray(emails.value[category][subcategory])) {
                    const emailIndex = emails.value[category][subcategory].findIndex(email => email.id === emailId);
                    if (emailIndex !== -1) {
                        emails.value[category][subcategory][emailIndex].read = false;
                        updateNumberUnreadEmails();
                        return;
                    }
                }
            }
        }
    }
}

function updateNumberUnreadEmails() {
    const newTotalUnread = getNumberUnreadMail(emails.value);

    if (initialAnimationDone.value === false) {
        animateText(getTextNumberUnreadMail(newTotalUnread));
        totalUnread.value = newTotalUnread;
        initialAnimationDone.value = true;
    } else if (newTotalUnread !== totalUnread.value) {
        totalUnread.value = newTotalUnread;

        if (totalUnread.value > 0 && totalUnread.value <= 2) {
            animateText(getTextNumberUnreadMail(totalUnread.value));
        } else {
            animatedText.value.textContent = getTextNumberUnreadMail(totalUnread.value);
        }
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

async function markEmailReplyLater(email) {
    lockEmailsAccess.value = true;
    const emailId = email.id
    email.answer_later = true;
    isMenuOpen.value = false;

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/mark_reply-later/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
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
    lockEmailsAccess.value = false;
}

function deleteEmailFromState(emailId) {
    // Iterate over each category in the emails object
    for (const category in emails.value) {
        if (Object.prototype.hasOwnProperty.call(emails.value, category)) {
            // Iterate over each subcategory within the category
            for (const subcategory in emails.value[category]) {
                if (Array.isArray(emails.value[category][subcategory])) {
                    // Find the index of the email with the given ID in the current subcategory's array
                    const emailIndex = emails.value[category][subcategory].findIndex(email => email.id === emailId);
                    if (emailIndex !== -1) {
                        // Email found, delete it from the array
                        emails.value[category][subcategory].splice(emailIndex, 1);
                        return; // Stop the function as we've found and deleted the email
                    }
                }
            }
        }
    }
}

async function setRuleBlockForSender(email) {
    lockEmailsAccess.value = true;
    const emailId = email.id;

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/block_sender/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.block) {
            deleteEmail(emailId);
        } else {
            console.error('Failed to set block rule for sender', response);
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle = t('homepage.blockEmailAddressFailure');
            notificationMessage = response;
            displayPopup();
        }
    } catch (error) {
        console.error('Error in setRuleBlockForSender:', error.message);
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('homepage.blockEmailAddressFailure');
        notificationMessage = error.message;
        displayPopup();
    }
    lockEmailsAccess.value = false;
}

async function deleteEmail(emailId) {
    lockEmailsAccess.value = true;
    deleteEmailFromState(emailId);

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/delete/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.message) {
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle = t('constants.popUpConstants.deleteEmailFailure');
            notificationMessage = response.error;
            displayPopup();
        }
    } catch (error) {
        console.error('Error in deleteEmail:', error.message);
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('constants.popUpConstants.deleteEmailFailure');
        notificationMessage = error.message;
        displayPopup();
    }
    lockEmailsAccess.value = false;
}

async function openAnswer(email) {
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

function updateModalStatus(status) {
    showModal.value = status;
}

function openSeeModal(emailItem) {
    selectedEmail.value = emailItem;
    isModalSeeOpen.value = true;
}
function closeSeeModal() {
    isModalSeeOpen.value = false;
}

function openModal() {
    isModalOpen.value = true;
}
function closeModal() {
    isModalOpen.value = false;
}
function openUpdateModal(category) {
    //console.log("CATEGORY TO UPDATE : ", category);
    oldCategoryName.value = category.name;
    categoryToUpdate.value = category;
    isModalUpdateOpen.value = true;
}
function closeUpdateModal() {
    isModalUpdateOpen.value = false;
}
function openWarningCategoryModal(nb_rules) {
    isModalWarningCategoryOpen.value = true;
    nbRulesAssociated.value = nb_rules;
}
function closeWarningCategoryModal() {
    isModalWarningCategoryOpen.value = false;
}

async function handleAddCategory(categoryData) {

    if (Object.hasOwnProperty.call(categoryData, 'error')) {
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = categoryData.error;
        notificationMessage = categoryData.description;
        displayPopup();

        closeModal();
        return;
    }

    try {
        const response = await fetchWithToken(`${API_BASE_URL}api/create_category/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: categoryData.name,
                description: categoryData.description,
            }),
        });

        if ('error' in response) {
            // Show the pop-up
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle = t('constants.popUpConstants.addCategoryError');
            notificationMessage = response.error;
            displayPopup();

            closeModal();
        } else if (response) {
            // Show the pop-up
            backgroundColor = 'bg-green-200/[.89] border border-green-400';
            notificationTitle = t('constants.popUpConstants.successMessages.success');
            notificationMessage = t('constants.popUpConstants.successMessages.categoryAddedSuccess');
            displayPopup();

            closeModal();
            const fetchedCategories = await fetchWithToken(`${API_BASE_URL}user/categories/`);

            categories.value = fetchedCategories.map(category => ({
                name: category.name,
                description: category.description
            }));
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle =  t('constants.popUpConstants.errorMessages.addCategoryError');
        notificationMessage = error.message;
        displayPopup();

        closeModal();
    }
}

async function handleUpdateCategory(updatedCategory) {

    if (Object.hasOwnProperty.call(updatedCategory, 'error')) {
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = updatedCategory.error;
        notificationMessage = updatedCategory.description;
        displayPopup();

        closeUpdateModal();
        return;
    }

    if (!updatedCategory.name.trim()) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle =  t('constants.popUpConstants.errorMessages.updateCategoryError');
        notificationMessage = t('constants.popUpConstants.errorMessages.emptyCategoryNameError');
        displayPopup();

        closeUpdateModal();
        return;
    }
    const updateData = {
        name: updatedCategory.name,
        description: updatedCategory.description,
        categoryName: oldCategoryName.value
    };
    try {
        const url = `${API_BASE_URL}api/update_category/`;
        const options = {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updateData)
        };
        const response = await fetchWithToken(url, options);

        if (response) {
            // Show the pop-up
            backgroundColor = 'bg-green-200/[.89] border border-green-400';
            notificationTitle = t('constants.popUpConstants.successMessages.success');
            notificationMessage = t('constants.popUpConstants.successMessages.updateCategorySuccess');
            displayPopup();

            closeUpdateModal();
            const fetchedCategories = await fetchWithToken(`${API_BASE_URL}user/categories/`);
            console.log("CategoryData", fetchedCategories);
            categories.value = fetchedCategories.map(category => ({
                name: category.name,
                description: category.description
            }));
            console.log("Assigned categories:", categories.value);
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('constants.popUpConstants.errorMessages.updateCategoryError');
        notificationMessage = error.message;
        displayPopup();

        closeUpdateModal();
    }
}
async function handleCategoryDelete(categoryNameToDelete) {

    if (!categoryNameToDelete.trim()) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('constants.popUpConstants.errorMessages.openTransferPageFailure');
        notificationMessage = t('constants.popUpConstants.errorMessages.emptyCategoryNameError');
        displayPopup();
        return;
    }

    try {
        const url = `${API_BASE_URL}api/get_rules_linked/`;

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "categoryName": categoryNameToDelete
            })
        };

        const response = await fetchWithToken(url, options);

        if (response.nb_rules > 0) {
            closeUpdateModal();
            openWarningCategoryModal(response.nb_rules);
        } else {
            deleteCategory(categoryNameToDelete);
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('constants.popUpConstants.errorMessages.recuperationRules');
        notificationMessage = error.message;
        displayPopup();

        closeUpdateModal();
    }
}

async function deleteCategory(categoryNameToDelete) {
    try {
        const url = `${API_BASE_URL}api/delete_category/`;

        const options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "categoryName": categoryNameToDelete
            })
        };

        const response = await fetchWithToken(url, options);

        if (response) {
            // Show the pop-up
            backgroundColor = 'bg-green-200/[.89] border border-green-400';
            notificationTitle =  t('constants.popUpConstants.successMessages.success');
            notificationMessage = t('constants.popUpConstants.successMessages.deleteCategorySuccess');
            displayPopup();

            // Fetch the categories
            const categoryData = await fetchWithToken(`${API_BASE_URL}user/categories/`);
            categories.value = categoryData.map(category => ({
                name: category.name,
                description: category.description
            }));
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = t('constants.popUpConstants.errorMessages.deleteCategoryError');
        notificationMessage = error.message;
        displayPopup();
    }
    closeUpdateModal();
    closeWarningCategoryModal();
}

function readEmailsInSelectedTopic() {
    let combinedEmails = [];
    for (let category in emails.value[selectedTopic.value]) {
        combinedEmails = combinedEmails.concat(emails.value[selectedTopic.value][category]);
    }

    return combinedEmails.filter(email => email.answer_later == false && email.read);
}

function toggleReadEmailVisibility() {
    showEmailReadDescriptions.value = !showEmailReadDescriptions.value;
    scrollToBottom();
}

function toggleEmailVisibility() {
    showEmailDescriptions.value = !showEmailDescriptions.value;
    if (readEmailsInSelectedTopic() == 0) {
        scrollToBottom();
    } else {
        scrollAlmostToBottom();
    }
}

function scrollToBottom() {
    nextTick(() => {
        const element = scrollableDiv.value;
        element.scrollTop = element.scrollHeight;
    });
}

function scrollAlmostToBottom() {
    nextTick(() => {
        const element = scrollableDiv.value;
        const offset = 100; // Adjust this value as needed
        element.scrollTop = element.scrollHeight - offset;
    });
}

function toggleHiddenParagraph(index) {
    // console.log("Item ID:", index)
    // console.log("All refs:", parentElementRefs.value)
    // console.log('parentElement: ', parentElementRefs.value[index])
    // console.log("Test: ", parentElementRefs.value[index].children)

    showHiddenParagraphs.value[index] = !showHiddenParagraphs.value[index];
    nextTick(() => {
        if (showHiddenParagraphs.value[index] && !animationTriggered.value[index]) {
            const parentElement = parentElementRefs.value[index];
            const elements = parentElement.children;
            //console.log("Elements:", elements)

            const delays = [0];
            for (let i = 0; i < elements.length; i++) {
                const duration = animateHiddenText(elements[i], delays[i]);
                delays.push(delays[i] + duration + 20);
            }
            animationTriggered.value[index] = true;
        }
    });
}

function animateHiddenText(element, delay = 0) {
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
}
function selectCategory(category) {
    selectedTopic.value = category.name;
    localStorage.setItem('selectedTopic', category.name);
    //console.log("CHANGE CATEGORY");
}
function countEmailsInCategoryAndPriority(categoryName, priority) {
    let count = 0;
    if (emails.value[categoryName] && emails.value[categoryName][priority]) {
        for (let email of emails.value[categoryName][priority]) {
            if (!email.read && !email.answer_later) {
                count++;
            }
        }
    }
    return count;
}

// To check if there is emails or not in the category
function isEmptyTopic() {
    //console.log("----> DEBUG isEmpty", selectedTopic.value);
    if (totalEmailsInCategory(selectedTopic.value) == 0) {
        //console.log("Topic not found for selectedTopic:", selectedTopic.value); // Debugging log
        return true; // or true, based on how you want to handle this case
    }
    else {
        return false;
    }
}

// Updated to work only with the the email not red by the user
function totalEmailsInCategory(categoryName) {
    let totalCount = 0;
    const category = emails.value[categoryName];

    if (category) {
        for (const subcategory of Object.values(category)) {
            totalCount += subcategory.filter(email => !email.answer_later).length;
        }
    }

    return totalCount;
}


function totalEmailsInCategoryNotRead(categoryName) {
    let totalCount = 0;
    const category = emails.value[categoryName];

    if (category) {
        for (const subcategory of Object.values(category)) {
            totalCount += subcategory.filter(email => !email.read && !email.answer_later).length;
        }
    }

    return totalCount;
}


const groupedEmailsByCategoryAndDate = (category) => {
    const grouped = {};
    if (emails.value[selectedTopic.value] && emails.value[selectedTopic.value][category]) {
        emails.value[selectedTopic.value][category].forEach(email => {
            if (!email.read && !email.answer_later) {
                if (!grouped[email.date]) {
                grouped[email.date] = [];
                }
                grouped[email.date].push(email);
            }
        });
    }
    
    // Sort the grouped object by date keys in descending order
    const sortedGrouped = Object.keys(grouped)
    .sort((a, b) => new Date(b) - new Date(a))
    .reduce((acc, key) => {
      // Sort emails by time in descending order for each date
      acc[key] = grouped[key].sort((a, b) => new Date(`1970/01/01 ${b.time}`) - new Date(`1970/01/01 ${a.time}`));
      return acc;
    }, {});
  
  return sortedGrouped;
};

async function fetchEmails() {
    const emailData = await fetchWithToken(`${API_BASE_URL}user/emails/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            // JUST for information send ONLY subject if the user has ONLY used the search bar
            subject: "",
            resultPerPage: 25,
            category: "Others"
        }),
    });
    console.log(emailData);
    if (lockEmailsAccess.value == false) {
        emails.value = emailData;
    }
    updateNumberUnreadEmails();
}

async function fetchData() {
    try {
        // Fetch the categories
        const categoryData = await fetchWithToken(`${API_BASE_URL}user/categories/`);
        //console.log("VERY IMPORTANT: =======> CategoryData", categoryData);

        for (let i = 0; i < categoryData.length; i++) {
            categories.value.push(categoryData[i]);
        }
        //console.log("Assigned categories:", categories.value);

        const storedTopic = localStorage.getItem('selectedTopic');
        //console.log("selectedTopic", storedTopic)
        if (storedTopic) {
            selectedTopic.value = storedTopic;
        } else if (categories.value.length > 0) {
            selectedTopic.value = categories.value[0].name;
        }

        fetchEmails();
    } catch (error) {
        console.error('Failed to fetch data:', error);
    }
}


async function Hide_filtres() {
    var toggleDiv = document.getElementById('filtres');
    
    if (toggleDiv.classList.contains('hidden')) {
        toggleDiv.classList.remove('hidden');
        setTimeout(function () {
            toggleDiv.classList.remove('opacity-0');
            toggleDiv.classList.add('opacity-100');
        }, 10);
        
    } else {
        toggleDiv.classList.remove('opacity-100');
        toggleDiv.classList.add('opacity-0');
        setTimeout(function () {
            toggleDiv.classList.add('hidden');
        }, 250);
        
    }
}
</script>

<script>
import ShowNotification from '../components/ShowNotification.vue';
import { XMarkIcon } from '@heroicons/vue/20/solid';
import { useRouter } from 'vue-router';
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';
import SearchbarV2 from '../components/SearchbarV2.vue'
import ModalSeeMail from '../components/SeeMailV2.vue';
import NewCategoryModal from '../components/NewCategoryModal.vue';
import UpdateCategoryModal from '../components/UpdateCategoryModal.vue';
import { ref, nextTick, onMounted } from 'vue';
import { fetchWithToken, fetchWithTokenv2, getBackgroundColor } from '../router/index.js';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import {
//ChatBubbleOvalLeftEllipsisIcon,
ExclamationTriangleIcon,
InformationCircleIcon,
TrashIcon,
ArrowUturnLeftIcon,
CheckIcon,
EllipsisHorizontalIcon,
HandRaisedIcon,
EyeIcon,
DocumentIcon,
DocumentTextIcon,
CameraIcon,
} from '@heroicons/vue/24/outline'

export default {
name: 'UserHome',
components: {
Navbar,
Navbar2,
//ChatBubbleOvalLeftEllipsisIcon,
ExclamationTriangleIcon,
InformationCircleIcon,
TrashIcon,
ArrowUturnLeftIcon,
CheckIcon,
EllipsisHorizontalIcon,
HandRaisedIcon,
EyeIcon,
SearchbarV2,
Menu,
MenuButton,
MenuItem,
MenuItems,
ModalSeeMail,
NewCategoryModal,
UpdateCategoryModal,
DocumentIcon,
DocumentTextIcon,
CameraIcon,
},

methods: {
updateSearchQuery(event) {
this.searchQuery = event.target.value;
},
}
}
</script>