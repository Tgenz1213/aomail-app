<template>
    <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" />
    <div v-if="loading">
        <Loading class=""></Loading>
    </div>
    <div v-else>
        <!--
    <div class="pb-1 lg:pl-20 bg-gray-100">
        <div class="grid grid-cols-8 gap-6 h-72 items-center divide-x-8 divide-indigo-900 bg-blue-400">
            <div class="col-span-3 h-full bg-red-500">
                    
                    <div class="flex">
                        <div class="flex-shrink-0 self-center">
                            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-indigo-800">
                                <span class="text-lg font-medium leading-none text-white">AO</span>
                            </span>
                        </div>
                        <div>
                            <p class="mt-1" id="animated-text" ref="animatedText"></p>
                        </div>
                    </div>
                </div>
            <div class="col-span-5 h-full bg-red-500">
                <p>Test</p>
            </div>
        </div>
    </div>-->
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
                <div class="col-span-10 2xl:col-span-6">
                    <!-- <div class="flex flex-col xl:h-[calc(93vh)] xl:w-[86vw] 2xl:h-[6/7*100vh] 2xl:w-[calc(80vw)]"> WORKS FOR 1920*1200px screens-->
                    <div class="flex flex-col xl:h-[93vh] xl:w-[86vw] 2xl:h-[825px] 2xl:w-[1450px]">
                        <main class="rounded-xl bg-gray-100 bg-opacity-75 ring-1 shadow-sm ring-black ring-opacity-5">
                            <div class="w-full px-4 sm:px-6 lg:px-6">
                                <div class="grid grid-cols-11 gap-4 items-center divide-x divide-gray-300">
                                    <div class="col-span-3 h-full justify-center">
                                        <!-- Assistant Up -->
                                        <div class="flex pt-6 pb-6">
                                            <div class="mr-4 flex-shrink-0 self-center">
                                                <!--
                                            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-[conic-gradient(at_left,_var(--tw-gradient-stops))] from-rose-400 via-amber-400 to-rose-200">
                                                <span class="text-lg font-medium leading-none text-white">AO</span>
                                            </span>-->
                                                <span
                                                    class="inline-flex h-14 w-14 items-center justify-center rounded-full overflow-hidden">
                                                    <img :src="happy_icon" alt="New Emails Icon"
                                                        class="max-w-full max-h-full rounded-full">
                                                </span>
                                            </div>
                                            <div>
                                                <p class="mt-1" id="animated-text" ref="animatedText"></p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="pl-4 col-span-8 h-full flex items-center">
                                        <div class="w-full flex items-center justify-center pb-5 pt-5">
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
                                            <div class="hidden sm:block w-full">
                                                <nav class="flex flex-wrap space-x-2 justify-center items-center w-full"
                                                    aria-label="Tabs">
                                                    <div class="flex space-x-4">
                                                        <a v-for="category in categories" :key="category"
                                                            class="group items-center text-gray-600 text-sm font-medium"><!-- To FIX => put category.name and adapt the design -->
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
                                                            <div v-else class="flex pr-7">
                                                                <!-- TODO: var language and retrieve the good translation -->
                                                                <span class="px-3 py-2 cursor-pointer"
                                                                    @click="selectCategory(category)"
                                                                    :class="{ 'bg-gray-500 bg-opacity-10 text-gray-800': selectedTopic === category.name, 'group-hover:bg-gray-500 rounded-l-md group-hover:bg-opacity-10': selectedTopic !== category.name, 'rounded-md': totalEmailsInCategoryNotRead(category.name) === 0, 'rounded-l-md': totalEmailsInCategoryNotRead(category.name) > 0 }">{{
                                                                        "Autres" }}
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
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </main>
                        <div v-if="isEmptyTopic()"
                            class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm ring-black ring-opacity-5">
                            <!-- Content goes here -->
                            <div v-if="isEmptyTopic()" class="flex flex-col w-full h-full rounded-xl">
                                <div
                                    class="flex flex-col justify-center items-center h-full mx-4 my-4 rounded-lg border-2 border-dashed border-gray-300 p-12 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1" stroke="currentColor" class="mx-auto h-14 w-14 text-gray-400">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                                    </svg>
                                    <span class="mt-2 block text-md font-semibold text-gray-900">Aucun nouveau
                                        mail</span>
                                </div>
                            </div>
                        </div>
                        <div v-else
                            class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm ring-black ring-opacity-5 overflow-y-auto custom-scrollbar"
                            ref="scrollableDiv">
                            <ul role="list" class="flex flex-col w-full h-full rounded-xl">
                                <div class="pb-4">
                                    <!-- To check if there is one class allow the whitespace at the bottom -->
                                    <li v-if="emails[selectedTopic] && emails[selectedTopic]['Important'] && countEmailsInCategoryAndPriority(selectedTopic, 'Important') > 0"
                                        class="py-10 px-8 mx-4 mt-4 rounded-xl bg-red-100 bg-opacity-50 hover:ring-1 ring-offset-0 ring-red-700 ring-opacity-20">
                                        <!-- ring-1 ring-red-700 ring-opacity-20 -->
                                        <div class="float-right mt-[-25px] mr-[-10px]">
                                            <exclamation-triangle-icon class="w-6 h-6 text-red-500" />
                                        </div>
                                        <!-- Your content -->
                                        <div class="flex">
                                            <div class="flex">
                                                <span
                                                    class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-red-400 dark:bg-red-200">
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
                                                <div class="overflow-hidden border-l-4 border-red-500  hover:rounded-l-xl dark:border-red-300"
                                                    style="overflow: visible;">
                                                    <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                                        <li v-for="item in emails[selectedTopic]['Important'].filter(email => !email.read && !email.answer_later)"
                                                            :key="item.id"
                                                            class="px-6 md:py-6 2xl:py-6 hover:bg-opacity-70 dark:hover:bg-red-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center"
                                                            @mouseover="setHoveredItem(item.id)"
                                                            @mouseleave="clearHoveredItem">
                                                            <!-- SAVE DO NOT DELETE : px-6 md:py-2 2xl:py-4 -->
                                                            <div class="col-span-8 cursor-pointer"
                                                                @click="toggleHiddenParagraph(item.id)">
                                                                <div class="flex-auto group">
                                                                    <div class="flex gap-x-4">
                                                                        <p
                                                                            class="text-sm font-semibold leading-6 text-red-700 dark:text-white">
                                                                            {{ item.name }}</p>
                                                                        <div
                                                                            class="hidden group-hover:block px-2 py-0.5 bg-red-300 text-white text-sm shadow rounded-xl">
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
                                                                                <p>Cliquez pour voir le résumé</p>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                    <p
                                                                        class="mt-1 text-md text-gray-700 leading-relaxed dark:text-red-50">
                                                                        {{ item.description }}</p>
                                                                </div>
                                                                <ul v-show="showHiddenParagraphs[item.id]" role="list"
                                                                    class="text-black text-sm/6 pt-2"
                                                                    :ref="el => setParentRef(el, item.id)">
                                                                    <!-- Potential design update : bg-white shadow rounded-xl -->
                                                                    <li v-for="detail in item.details" :key="detail.id"
                                                                        class="pl-8" :ref="'hiddenText' + item.id"
                                                                        :data-text="detail.text">
                                                                    </li>
                                                                </ul>
                                                            </div>
                                                            <div class="col-span-2">
                                                                <div class="flex justify-center">
                                                                    <span class="isolate inline-flex rounded-2xl">
                                                                        <div v-show="hoveredItemId === item.id"
                                                                            class="group action-buttons">
                                                                            <div class="relative group">
                                                                                <div
                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4">
                                                                                    Ouvrir
                                                                                </div>
                                                                                <button
                                                                                    @click="openInNewWindow(item.web_link)"
                                                                                    type="button"
                                                                                    class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                                                    <eye-icon
                                                                                        class="w-5 h-5 text-red-400 group-hover:text-white" />
                                                                                </button>
                                                                            </div>
                                                                        </div>
                                                                        <div v-show="hoveredItemId === item.id"
                                                                            class="group action-buttons">
                                                                            <div class="relative group">
                                                                                <div
                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-2">
                                                                                    Lu
                                                                                </div>
                                                                                <button
                                                                                    @click="markEmailAsRead(item.id)"
                                                                                    type="button"
                                                                                    class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                                                    <check-icon
                                                                                        class="w-5 h-5 text-red-400 group-hover:text-white" />
                                                                                </button>
                                                                            </div>
                                                                        </div>
                                                                        <div v-show="hoveredItemId === item.id"
                                                                            class="group action-buttons">
                                                                            <div class="relative group">
                                                                                <div
                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                                                                    Répondre
                                                                                </div>
                                                                                <button @click="openAnswer(item)"
                                                                                    type="button"
                                                                                    class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                                                    <arrow-uturn-left-icon
                                                                                        class="w-5 h-5 text-red-400 group-hover:text-white" />
                                                                                </button>
                                                                            </div>
                                                                        </div>
                                                                        <div v-show="hoveredItemId === item.id"
                                                                            class="group action-buttons">
                                                                            <div class="relative group">
                                                                                <div
                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-20 w-[185px]">
                                                                                    Actions supplémentaires
                                                                                </div>
                                                                                <Menu as="div"
                                                                                    class="relative inline-block text-left">
                                                                                    <div>
                                                                                        <MenuButton
                                                                                            @click="toggleTooltip"
                                                                                            class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-red-400 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                                                            <ellipsis-horizontal-icon
                                                                                                class="w-5 h-5 group-hover:text-white text-red-400 group-active:text-red-400 group-focus:text-red focus:text-red-400" />
                                                                                        </MenuButton>
                                                                                    </div>
                                                                                    <transition
                                                                                        enter-active-class="transition ease-out duration-100"
                                                                                        enter-from-class="transform opacity-0 scale-95"
                                                                                        enter-to-class="transform opacity-100 scale-100"
                                                                                        leave-active-class="transition ease-in duration-75"
                                                                                        leave-from-class="transform opacity-100 scale-100"
                                                                                        leave-to-class="transform opacity-0 scale-95">
                                                                                        <MenuItems v-show="isMenuOpen"
                                                                                            class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none cursor-pointer">
                                                                                            <div class="py-1">
                                                                                                <div v-if="item.rule">
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
                                                                                                            <span>Changer
                                                                                                                la
                                                                                                                règle</span>
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
                                                                                                            <span>Créer
                                                                                                                une
                                                                                                                règle</span>
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
                                                                                                        <span>Répondre
                                                                                                            plus
                                                                                                            tard</span>
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
                                                                                                        <span>Transférer</span>
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
                                    </li>
                                    <!-- More items... -->
                                    <li v-if="emails[selectedTopic] && emails[selectedTopic]['Information'] && countEmailsInCategoryAndPriority(selectedTopic, 'Information') > 0"
                                        class="py-10 px-8 mx-4 mt-4 rounded-xl bg-blue-100 bg-opacity-50 hover:ring-1 ring-offset-0 ring-blue-700 ring-opacity-20">
                                        <!-- ring-1 ring-blue-700 ring-opacity-20 -->
                                        <div class="float-right mt-[-25px] mr-[-10px]">
                                            <information-circle-icon class="w-6 h-6 text-blue-500" />
                                        </div>
                                        <!-- Your content -->
                                        <div class="flex">
                                            <div class="flex">
                                                <span
                                                    class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-blue-500 dark:bg-blue-200">
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
                                                <div class="overflow-hidden border-l-4 hover:rounded-l-xl border-blue-300 dark:bg-blue-500"
                                                    style="overflow: visible;">
                                                    <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                                        <li v-for="item in emails[selectedTopic]['Information'].filter(email => !email.read && !email.answer_later)"
                                                            :key="item.id"
                                                            class="px-6 md:py-6 2xl:py-6 hover:bg-opacity-70 dark:hover:bg-blue-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center"
                                                            @mouseover="setHoveredItem(item.id)"
                                                            @mouseleave="clearHoveredItem">
                                                            <div class="col-span-8 cursor-pointer"
                                                                @click="toggleHiddenParagraph(item.id)">
                                                                <div class="flex-auto group">
                                                                    <div class="flex gap-x-4">
                                                                        <p
                                                                            class="text-sm font-semibold leading-6 text-blue-800 dark:text-white">
                                                                            {{ item.name }}</p>
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
                                                                                <p>Cliquez pour voir le résumé</p>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                    <p
                                                                        class="mt-1 text-md text-gray-700 leading-relaxed dark:text-blue-50">
                                                                        {{ item.description }}</p>
                                                                </div>
                                                                <ul v-show="showHiddenParagraphs[item.id]" role="list"
                                                                    class="text-black text-sm/6 pt-2"
                                                                    :ref="el => setParentRef(el, item.id)">
                                                                    <!-- Potential design update : bg-white shadow rounded-xl -->
                                                                    <li v-for="detail in item.details" :key="detail.id"
                                                                        class="pl-8" :ref="'hiddenText' + item.id"
                                                                        :data-text="detail.text">
                                                                    </li>
                                                                </ul>
                                                            </div>
                                                            <div class="col-span-2">
                                                                <div class="flex justify-center">
                                                                    <span class="isolate inline-flex rounded-2xl">
                                                                        <div v-show="hoveredItemId === item.id"
                                                                            class="group action-buttons">
                                                                            <div class="relative group">
                                                                                <div
                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4 z-40">
                                                                                    Ouvrir
                                                                                </div>
                                                                                <button
                                                                                    @click="openInNewWindow(item.web_link)"
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
                                                                                    Lu
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
                                                                                    Répondre
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
                                                                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-20 w-[185px]">
                                                                                    Actions supplémentaires
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
                                                                                        <MenuItems v-show="isMenuOpen"
                                                                                            class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none cursor-pointer">
                                                                                            <div class="py-1">
                                                                                                <div v-if="item.rule">
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
                                                                                                            <span>Changer
                                                                                                                la
                                                                                                                règle</span>
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
                                                                                                            <span>Créer
                                                                                                                une
                                                                                                                règle</span>
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
                                                                                                        <span>Répondre
                                                                                                            plus
                                                                                                            tard</span>
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
                                                                                                        <span>Transférer</span>
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
                                    </li>
                                    <!-- add @click="toggleEmailVisibility"-->
                                    <div v-if="emails[selectedTopic] && emails[selectedTopic]['Useless'].filter(email => !email.answer_later) && countEmailsInCategoryAndPriority(selectedTopic, 'Useless') > 0"
                                        class="group/main flex-1 mx-4 mt-4 rounded-xl bg-gray-100 hover:ring-1 ring-offset-0 ring-gray-700 ring-opacity-20">
                                        <li class="py-10 px-8"> <!-- ring-1 ring-red-700 ring-opacity-20 -->
                                            <!-- BUG A CORRIGER : ESPACE BLANC BOTTOM -->
                                            <div class="float-right mt-[-25px] mr-[-10px]">
                                                <trash-icon class="w-6 h-6 text-gray-500" />
                                            </div>
                                            <!-- Your content -->
                                            <div class="flex">
                                                <div class="flex">
                                                    <span
                                                        class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-400">
                                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                            viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                                            class="w-6 h-6 text-white">
                                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                                d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                                                        </svg>
                                                    </span>
                                                    <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-500" />-->
                                                </div>
                                                <div class="ml-6 w-full">
                                                    <div class="overflow-hidden border-l-4 group-hover/main:rounded-l-xl border-gray-500 w-full"
                                                        style="overflow: visible;">
                                                        <ul role="list"
                                                            class="divide-y divide-gray-200 dark:divide-white w-full">
                                                            <li
                                                                class="px-6 py-4 hover:bg-opacity-70 dark:hover:bg-opacity-100 w-full">
                                                                <div class="flex gap-x-2">
                                                                    <!-- remove @click="toggleEmailVisibility"-->
                                                                    <p @click="toggleEmailVisibility"
                                                                        class="cursor-pointer">Vous avez reçu
                                                                        <span class="font-semibold text-gray-900 dark:text-white hover:text-gray-700 w-full">{{ emails[selectedTopic]['Useless'].filter(email => !email.answer_later).length }}</span>
                                                                        <span
                                                                            v-if="emails[selectedTopic]['Useless'].filter(email => !email.answer_later).length === 1">
                                                                            mail inutile.
                                                                        </span>
                                                                        <span v-else>
                                                                            mails inutiles.
                                                                        </span>
                                                                    </p>
                                                                    <div
                                                                        class="hidden group-hover/main:block px-2 py-0.5 bg-gray-500 text-white text-sm shadow rounded-xl">
                                                                        <div class="flex gap-x-1 items-center">
                                                                            <svg xmlns="http://www.w3.org/2000/svg"
                                                                                fill="none" viewBox="0 0 24 24"
                                                                                stroke-width="1.5" stroke="currentColor"
                                                                                class="w-4 h-4">
                                                                                <path stroke-linecap="round"
                                                                                    stroke-linejoin="round"
                                                                                    d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                                                                            </svg>
                                                                            <!-- remove @click="toggleEmailVisibility"-->
                                                                            <p @click="toggleEmailVisibility"
                                                                                class="cursor-pointer">Cliquez pour voir
                                                                                les mails</p>
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
                                                                                <p
                                                                                    class="text-sm font-semibold leading-6 text-gray-800 dark:text-white">
                                                                                    {{ item.name }}</p>
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
                                                                                                Ouvrir
                                                                                            </div>
                                                                                            <button
                                                                                                @click.stop="openInNewWindow(item.web_link)"
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
                                                                                                Bloquer
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
                                                                                                Supprimer
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
                                                                                                Répondre
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
                                                                                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-20 w-[185px]">
                                                                                                Actions supplémentaires
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
                                                                                                                        <span>Changer
                                                                                                                            la
                                                                                                                            règle</span>
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
                                                                                                                        <span>Créer
                                                                                                                            une
                                                                                                                            règle</span>
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
                                                                                                                    <span>Répondre
                                                                                                                        plus
                                                                                                                        tard</span>
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
                                                                                                                    <span>Transférer</span>
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
                                        </li>
                                    </div>
                                    <div v-if="readEmailsInSelectedTopic().length > 0"
                                        class="group/main flex-1 mx-4 mt-4 rounded-xl bg-emerald-100 hover:ring-1 ring-offset-0 ring-emerald-700 ring-opacity-30">
                                        <li class="py-10 px-8"> <!-- ring-1 ring-red-700 ring-opacity-20 -->
                                            <!-- BUG A CORRIGER : ESPACE BLANC BOTTOM -->
                                            <div class="float-right mt-[-25px] mr-[-10px]">
                                                <CheckIcon class="w-6 h-6 text-emerald-500" />
                                            </div>
                                            <!-- Your content -->
                                            <div class="flex">
                                                <div class="flex">
                                                    <span
                                                        class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-emerald-400">
                                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none"
                                                            viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                                                            class="w-6 h-6 text-white">
                                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                                d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                                                        </svg>
                                                    </span>
                                                    <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-500" />-->
                                                </div>
                                                <div class="ml-6 w-full">
                                                    <!-- To check : strange w-full not necessary in grey but it must be here to have the correct space for readEmailsInSelectedTopic -->
                                                    <div class="overflow-hidden border-l-4 group-hover/main:rounded-l-xl border-emerald-500 w-full"
                                                        style="overflow: visible;">
                                                        <ul role="list"
                                                            class="divide-y divide-gray-200 dark:divide-white w-full">
                                                            <li
                                                                class="px-6 py-4 hover:bg-opacity-70 dark:hover:bg-opacity-100 w-full">
                                                                <div class="flex group gap-x-2">
                                                                    <p @click="toggleReadEmailVisibility"
                                                                        class="cursor-pointer">Vous avez récemment lu
                                                                        <span
                                                                            class="font-semibold text-gray-900 dark:text-white hover:text-gray-700">
                                                                            {{ readEmailsInSelectedTopic().length }}
                                                                        </span>
                                                                        <span
                                                                            v-if="readEmailsInSelectedTopic().length === 1">
                                                                            mail</span>
                                                                        <span v-else> mails</span>. Je
                                                                        <span class="font-medium">vais nettoyer
                                                                            automatiquement</span> les mails lus.
                                                                    </p>
                                                                    <div
                                                                        class="hidden group-hover/main:block px-2 py-0.5 bg-emerald-400 text-white text-sm shadow rounded-xl">
                                                                        <div class="flex gap-x-1 items-center">
                                                                            <svg xmlns="http://www.w3.org/2000/svg"
                                                                                fill="none" viewBox="0 0 24 24"
                                                                                stroke-width="1.5" stroke="currentColor"
                                                                                class="w-4 h-4">
                                                                                <path stroke-linecap="round"
                                                                                    stroke-linejoin="round"
                                                                                    d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                                                                            </svg>
                                                                            <p @click="toggleReadEmailVisibility"
                                                                                class="cursor-pointer">Cliquez pour voir
                                                                                les mails</p>
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
                                                                                    <p
                                                                                        class="text-sm font-semibold leading-6 text-emerald-500 dark:text-white">
                                                                                        {{ item.name }}</p>
                                                                                    <div
                                                                                        class="hidden group-hover:block px-2 py-0.5 bg-emerald-400 text-white text-sm shadow rounded-xl">
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
                                                                                            <p>Cliquez pour voir le
                                                                                                résumé</p>
                                                                                        </div>
                                                                                    </div>
                                                                                </div>
                                                                                <p
                                                                                    class="mt-1 text-md text-gray-700 leading-relaxed dark:text-emerald-500">
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
                                                                                                Ouvrir
                                                                                            </div>
                                                                                            <button
                                                                                                @click.stop="openInNewWindow(item.web_link)"
                                                                                                type="button"
                                                                                                class="inline-flex items-center px-2 py-1.5 rounded-l-2xl text-emerald-400 ring-1 ring-inset ring-emerald-400 hover:bg-emerald-400 focus:z-10">
                                                                                                <eye-icon
                                                                                                    class="w-5 h-5 text-emerald-500 group-hover:text-white" />
                                                                                            </button>
                                                                                        </div>
                                                                                    </div>
                                                                                    <div v-show="hoveredItemId === item.id"
                                                                                        class="group action-buttons">
                                                                                        <div class="relative group">
                                                                                            <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-25 w-[80px]">
                                                                                                Non Lu
                                                                                            </div>
                                                                                            <button
                                                                                                @click="markEmailAsUnread(item.id)"
                                                                                                type="button"
                                                                                                class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-emerald-400 hover:bg-emerald-400 focus:z-10">
                                                                                                <check-icon
                                                                                                class="w-5 h-5 text-emerald-500 group-hover:text-white" />
                                                                                            </button>
                                                                                        </div>
                                                                                    </div>
                                                                                    <div v-show="hoveredItemId === item.id"
                                                                                        class="group action-buttons">
                                                                                        <div class="relative group">
                                                                                            <div
                                                                                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-6">
                                                                                                Supprimer
                                                                                            </div>
                                                                                            <button type="button"
                                                                                                class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-emerald-400 hover:bg-emerald-400 focus:z-10">
                                                                                                <TrashIcon
                                                                                                    @click.stop="deleteEmail(item.id)"
                                                                                                    class="w-5 h-5 text-emerald-500 group-hover:text-white" />
                                                                                            </button>
                                                                                        </div>
                                                                                    </div>
                                                                                    <div v-show="hoveredItemId === item.id"
                                                                                        class="group action-buttons">
                                                                                        <div class="relative group">
                                                                                            <div
                                                                                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                                                                                Répondre
                                                                                            </div>
                                                                                            <button
                                                                                                @click.stop="openAnswer(item)"
                                                                                                type="button"
                                                                                                class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-emerald-400 hover:bg-emerald-400 focus:z-10">
                                                                                                <arrow-uturn-left-icon
                                                                                                    class="w-5 h-5 text-emerald-500 group-hover:text-white" />
                                                                                            </button>
                                                                                        </div>
                                                                                    </div>
                                                                                    <div v-show="hoveredItemId === item.id"
                                                                                        class="group action-buttons">
                                                                                        <div
                                                                                            class="cursor-pointer relative group">
                                                                                            <div
                                                                                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-20 w-[185px]">
                                                                                                Actions supplémentaires
                                                                                            </div>
                                                                                            <Menu as="div"
                                                                                                class="relative inline-block text-left">
                                                                                                <div>
                                                                                                    <MenuButton
                                                                                                        @click="toggleTooltip"
                                                                                                        class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-emerald-500 ring-1 ring-inset ring-emerald-400 hover:bg-emerald-400 focus:z-10">
                                                                                                        <ellipsis-horizontal-icon
                                                                                                            class="w-5 h-5 group-hover:text-white text-emerald-500 group-active:text-emerald-500 group-focus:text-red focus:text-emerald-500" />
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
                                                                                                                        <span>Changer
                                                                                                                            la
                                                                                                                            règle</span>
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
                                                                                                                        <span>Créer
                                                                                                                            une
                                                                                                                            règle</span>
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
                                                                                                                    <span>Répondre
                                                                                                                        plus
                                                                                                                        tard</span>
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
                                                                                                                    <span>Transférer</span>
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
                                        </li>
                                    </div>
                                </div>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Category Modal -->
        <NewCategoryModal :isOpen="isModalOpen" :errorMessage="modalErrorMessage" @closeModal="closeModal"
            @addCategory="handleAddCategory" />
        <UpdateCategoryModal :isOpen="isModalUpdateOpen" :errorMessage="modalUpdateErrorMessage"
            :category="categoryToUpdate" @closeModal="closeUpdateModal" @updateCategory="handleUpdateCategory"
            @deleteCategory="handleCategoryDelete" />
        <ModalSeeMail :isOpen="showModal" :email="selectedEmail" @update:isOpen="updateModalStatus" />
    </div>
</template>

<script setup>
import { API_BASE_URL } from '@/main';

// Variables to display a notification
let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
let timerId = ref(null);

const router = useRouter();
let animatedText = ref('');
let showHiddenParagraphs = ref({});
let showModal = ref(false);
let isModalOpen = ref(false);
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
const happy_icon = ref(require('@/assets/happy.png'));

onMounted(async () => {
    getBackgroundColor();

    // Wait for fetchData completion
    await new Promise(resolve => {
        fetchData().then(() => {
            resolve();
        });
        animateText("Calcul des mails non lus en cours");
    });

    setInterval(async () => {
        try {
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
            fetchEmails();
        } catch (error) {
            console.log("An error occured", error)
        }
    }, 5000);
});

function getNumberUnreadMail(emailData) {
    let totalUnread = 0;

    for (const category in emailData) {
        for (const subcategory in emailData[category]) {
            const emailsInSubcategory = emailData[category][subcategory];

            for (const email of emailsInSubcategory) {
                if (!email.read && !email.answer_later) {
                    totalUnread++;
                }
            }
        }
    }
    return totalUnread;
}

function getTextNumberUnreadMail(totalUnread) {
    if (totalUnread === 0) {
        return 'Vous n\'avez pas reçu de nouveau mail';
    } else if (totalUnread === 1) {
        return `Vous avez reçu ${totalUnread} nouveau mail`;
    } else {
        return `Vous avez reçu ${totalUnread} nouveaux mails`;
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
    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/mark-unread/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.read == false) {
            updateEmailUnreadStatus(emailId);
        } else {
            console.log("RESPONSE markEmailAsUnread", response);
            backgroundColor = 'bg-red-300';
            notificationTitle = 'Échec de marquage de l\'email comme non lu';
            notificationMessage = response;
            displayPopup();
        }
    } catch (error) {
        console.error('Error in markEmailAsUnread:', error.message);
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Échec de marquage de l\'email comme non lu';
        notificationMessage = error.message;
        displayPopup();
    }
}
async function markEmailAsRead(emailId) {
    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/mark-read/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.read) {
            updateEmailReadStatus(emailId);
        } else {
            console.log("RESPONSE", response);
            backgroundColor = 'bg-red-300';
            notificationTitle = 'Échec de marquage de l\'email comme lu';
            notificationMessage = response;
            displayPopup();
        }
    } catch (error) {
        console.error('Error in markEmailAsRead:', error.message);
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Échec de marquage de l\'email comme lu';
        notificationMessage = error.message;
        displayPopup();
    }
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
                        return;
                    }
                }
            }
        }
    }
}

async function transferEmail(email) {
    console.log(email.id_provider)
    const url = `${API_BASE_URL}api/get_mail_by_id?email_id=${email.id_provider}`;

    try {
        const data = await fetchWithToken(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        // Clean CC data
        let cleanedCc = '';
        if (data.email.cc && data.email.cc.length > 0) {
            let ccEmails = data.email.cc[0].split(',').map(email => email.trim());
            cleanedCc = JSON.stringify(ccEmails);
        } else {
            cleanedCc = '[]';
        }

        router.push({
            name: 'transfer',
            query: {
                subject: JSON.stringify(data.email.subject),
                cc: cleanedCc,
                decoded_data: JSON.stringify(data.email.decoded_data),
                email: JSON.stringify(email.email),
                details: JSON.stringify(email.details),
                date: JSON.stringify(data.email.date)
            }
        });

    } catch (error) {
        console.error("There was a problem with the fetch operation:", error.message);
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Échec de transfer d\'email';
        notificationMessage = error.message;
        displayPopup();
    }
}

async function markEmailReplyLater(email) {
    const emailId = email.id
    email.answer_later = true;
    isMenuOpen.value = false;

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/mark-reply-later/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (response.answer_later) {
            console.log("Email marked for reply later successfully");
        } else {
            console.error('Failed to mark email for reply later', response);
            backgroundColor = 'bg-red-300';
            notificationTitle = 'Échec de marquage d\'email pour répondre pour plus tard';
            notificationMessage = response;
            displayPopup();
        }
    } catch (error) {
        console.error('Error in markEmailReplyLater:', error.message);
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Échec de marquage d\'email pour répondre pour plus tard';
        notificationMessage = error.message;
        displayPopup();
    }
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
    const emailId = email.id;

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/block-sender/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        console.log("RESPONSE", response);
        if (response.block) {
            deleteEmail(emailId);
        } else {
            console.error('Failed to set block rule for sender', response);
            backgroundColor = 'bg-red-300';
            notificationTitle = 'Échec du bloquage de l\'addresse email';
            notificationMessage = response;
            displayPopup();
        }
    } catch (error) {
        console.error('Error in setRuleBlockForSender:', error.message);
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Échec du bloquage de l\'addresse email';
        notificationMessage = error.message;
        displayPopup();
    }
}

async function deleteEmail(emailId) {
    deleteEmailFromState(emailId);

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/delete/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.message) {
            backgroundColor = 'bg-red-300';
            notificationTitle = 'Échec de suppression d\'email';
            notificationMessage = response.error;
            displayPopup();
        }
    } catch (error) {
        console.error('Error in deleteEmail:', error.message);
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Échec de suppression d\'email';
        notificationMessage = error.message;
        displayPopup();
    }
}

function openInNewWindow(web_link) {
    console.log(web_link)
    window.open(web_link, '_blank');
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
        // Clean CC data
        let cleanedCc = '';
        if (data.email.cc && data.email.cc.length > 0) {
            let ccEmails = data.email.cc[0].split(',').map(email => email.trim());
            cleanedCc = JSON.stringify(ccEmails);
        } else {
            cleanedCc = '[]';
        }

        router.push({
            name: 'answer',
            query: {
                subject: JSON.stringify(data.email.subject),
                cc: cleanedCc,
                bcc: JSON.stringify(data.email.bcc),
                decoded_data: JSON.stringify(data.email.decoded_data),
                email: JSON.stringify(email.email),
                id_provider: JSON.stringify(email.id_provider),
                details: JSON.stringify(email.details)
            }
        });
    } catch (error) {
        console.error("There was a problem with the fetch operation:", error.message);
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Échec d\'ouverture de la page de réponse';
        notificationMessage = error.message;
        displayPopup();
    }
}

function updateModalStatus(status) {
    showModal.value = status;
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

async function handleAddCategory(categoryData) {

    if (Object.hasOwnProperty.call(categoryData, 'error')) {
        backgroundColor = 'bg-red-300';
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
            backgroundColor = 'bg-red-300';
            notificationTitle = 'Erreur lors de l\'ajout de la catégorie';
            notificationMessage = response.error;
            displayPopup();

            closeModal();
        } else if (response) {
            // Show the pop-up
            backgroundColor = 'bg-green-300';
            notificationTitle = 'Succès !';
            notificationMessage = 'La catégorie a été ajoutée';
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
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Erreur lors de l\'ajout de la catégorie';
        notificationMessage = error.message;
        displayPopup();

        closeModal();
    }
}

async function handleUpdateCategory(updatedCategory) {

    if (Object.hasOwnProperty.call(updatedCategory, 'error')) {
        backgroundColor = 'bg-red-300';
        notificationTitle = updatedCategory.error;
        notificationMessage = updatedCategory.description;
        displayPopup();

        closeUpdateModal();
        return;
    }

    if (!updatedCategory.name.trim()) {
        // Show the pop-up
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Erreur lors de la mise à jour de la catégorie';
        notificationMessage = 'Le nom de la catégorie ne peut pas être vide';
        displayPopup();

        closeUpdateModal();
        return;
    }
    const updateData = {
        name: updatedCategory.name,
        description: updatedCategory.description
    };
    try {
        const url = `${API_BASE_URL}api/update_category/${oldCategoryName.value}/`; // Adjust the URL as needed
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
            backgroundColor = 'bg-green-300';
            notificationTitle = 'Succès !';
            notificationMessage = 'La catégorie a été mise à jour';
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
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Erreur lors de la mise à jour de la catégorie';
        notificationMessage = error.message;
        displayPopup();

        closeUpdateModal();
    }
}
async function handleCategoryDelete(categoryNameToDelete) {

    if (!categoryNameToDelete.trim()) {
        // Show the pop-up
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Erreur lors de la suppression de la catégorie';
        notificationMessage = 'Le nom de la catégorie ne peut pas être vide';
        displayPopup();
        return;
    }

    try {
        const url = `${API_BASE_URL}api/delete_category/${categoryNameToDelete}/`;

        const options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        };

        const response = await fetchWithToken(url, options);

        if (response) {
            // Show the pop-up
            backgroundColor = 'bg-green-300';
            notificationTitle = 'Succès !';
            notificationMessage = 'Votre catégorie a été supprimée';
            displayPopup();

            closeUpdateModal();
            // Fetch the categories
            const categoryData = await fetchWithToken(`${API_BASE_URL}user/categories/`);
            console.log("CategoryData", categoryData);
            categories.value = categoryData.map(category => ({
                name: category.name,
                description: category.description
            }));
            console.log("Assigned categories:", categories.value);
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Erreur lors de la suppression de la catégorie';
        notificationMessage = error.message;
        displayPopup();

        closeUpdateModal();
    }




    try {
        const url = `${API_BASE_URL}api/delete_category/${categoryNameToDelete}/`;

        const options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        };

        const response = await fetchWithToken(url, options);

        if (response) {
            // Show the pop-up
            backgroundColor = 'bg-green-300';
            notificationTitle = 'Succès !';
            notificationMessage = 'Votre catégorie a été supprimée';
            displayPopup();

            closeUpdateModal();
            // Fetch the categories
            const categoryData = await fetchWithToken(`${API_BASE_URL}user/categories/`);
            console.log("CategoryData", categoryData);
            categories.value = categoryData.map(category => ({
                name: category.name,
                description: category.description
            }));
            console.log("Assigned categories:", categories.value);
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-300';
        notificationTitle = 'Erreur lors de la suppression de la catégorie';
        notificationMessage = error.message;
        displayPopup();

        closeUpdateModal();
    }
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
    if (emails.value[categoryName]) {
        for (let subcategory of Object.values(emails.value[categoryName])) {
            for (let email of subcategory) {
                if (email.answer_later == false) {
                    totalCount++;
                }
            }
        }
    }
    return totalCount;
}

function totalEmailsInCategoryNotRead(categoryName) {
    let totalCount = 0;
    if (emails.value[categoryName]) {
        for (let subcategory of Object.values(emails.value[categoryName])) {
            for (let email of subcategory) {
                if (!email.read && !email.answer_later) {
                    totalCount++;
                }
            }
        }
    }
    return totalCount;
}
async function fetchEmails() {
    const emailData = await fetchWithToken(`${API_BASE_URL}user/emails/`);
    console.log("ALL DATA WITH ATTACHEMENTS!!!", emailData)
    emails.value = emailData;
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
</script>

<script>
import ShowNotification from '../components/ShowNotification.vue';
import { useRouter } from 'vue-router';
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';
import ModalSeeMail from '../components/SeeMail.vue';
import NewCategoryModal from '../components/NewCategoryModal.vue';
import UpdateCategoryModal from '../components/UpdateCategoryModal.vue';
import { ref, nextTick, onMounted } from 'vue';
import { fetchWithToken, getBackgroundColor } from '../router/index.js';
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
    EyeIcon
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
        Menu,
        MenuButton,
        MenuItem,
        MenuItems,
        ModalSeeMail,
        NewCategoryModal,
        UpdateCategoryModal
    }
}
</script>