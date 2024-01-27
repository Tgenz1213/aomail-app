<template>
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
                                            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                                                </svg>
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
                                            <select id="tabs" name="tabs" class="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500" v-model="selectedTopic">
                                                <option v-for="category in categories" :key="category">{{ category.name }}</option>
                                            </select>
                                        </div>
                                        <div class="hidden sm:block w-full">
                                            <nav class="flex flex-wrap space-x-2 justify-center items-center w-full" aria-label="Tabs">
                                                <div class="flex space-x-4">
                                                    <a v-for="category in categories" :key="category" href="#" @click="selectCategory(category)" class="group items-center text-gray-600 text-sm font-medium"><!-- To FIX => put category.name and adapt the design -->
                                                        <div class="flex">
                                                            <span class="px-4 py-2" :class="{'bg-gray-500 group-hover:rounded-r-none rounded-md bg-opacity-10 text-gray-800': selectedTopic === category.name, 'group-hover:bg-gray-500 rounded-l-md group-hover:bg-opacity-10': selectedTopic !== category.name}">{{ category.name }}</span>
                                                            <span v-if="totalEmailsInCategory(category.name) > 0" class="bg-gray-800 text-white rounded-full py-0.5 px-2.5 text-xs font-medium">
                                                                {{ totalEmailsInCategory(category.name) }}
                                                            </span>
                                                            <span class="opacity-0 group-hover:opacity-100 pr-2 py-2 group-hover:bg-gray-500 rounded-r-md group-hover:bg-opacity-10">
                                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 hover:text-black" @click.stop="openUpdateModal(category)">
                                                                    <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                                                                </svg>
                                                            </span>
                                                        </div>
                                                    </a>
                                                </div>
                                                <a class="flex text-gray-600 rounded-md px-8 py-2 text-sm font-medium hover:bg-gray-900 hover:text-white" @click="openModal">
                                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                                    </svg>
                                                </a>
                                            </nav>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </main>
                    <div v-if="!emails[selectedTopic]" class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm ring-black ring-opacity-5">
                        <!-- Content goes here -->
                        <div v-if="!emails[selectedTopic]" class="flex flex-col w-full h-full rounded-xl">
                            <div class="flex flex-col justify-center items-center h-full mx-4 my-4 rounded-lg border-2 border-dashed border-gray-300 p-12 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1" stroke="currentColor" class="mx-auto h-14 w-14 text-gray-400">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                                </svg>
                                <span class="mt-2 block text-md font-semibold text-gray-900">Aucun nouveau mail</span>
                            </div>
                        </div>
                    </div>
                    <div v-else class="flex-1 rounded-xl bg-white lg:mt-4 ring-1 shadow-sm ring-black ring-opacity-5 overflow-y-auto custom-scrollbar" ref="scrollableDiv">
                        <ul role="list" class="flex flex-col w-full h-full rounded-xl">
                         <div class="pb-4"><!-- To check if there is one class allow the whitespace at the bottom -->
                            <li v-if="emails[selectedTopic] && emails[selectedTopic]['Important'] && emails[selectedTopic]['Important'].length > 0" class="py-10 px-8 mx-4 my-4 rounded-xl bg-red-100 bg-opacity-50 hover:border border-red-700 border-opacity-20"> <!-- ring-1 ring-red-700 ring-opacity-20 -->
                                <div class="float-right mt-[-25px] mr-[-10px]">
                                    <exclamation-triangle-icon class="w-6 h-6 text-red-500" />
                                </div>
                                <!-- Your content -->
                                <div class="flex">
                                    <div class="flex">
                                        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-red-400 dark:bg-red-200">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-white">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                                            </svg>
                                        </span>
                                        <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-500" />-->
                                    </div>
                                    <div class="ml-6 flex-grow">
                                        <div class="overflow-hidden border-l-4 border-red-500  hover:rounded-l-xl dark:border-red-300" style="overflow: visible;">
                                            <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                                <li v-for="item in emails[selectedTopic]['Important'].filter(email => !email.read)" :key="item.id" class="px-6 md:py-2 2xl:py-4 hover:bg-opacity-70 dark:hover:bg-red-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center" @mouseover="setHoveredItem(item.id)" @mouseleave="clearHoveredItem"><!-- SAVE DO NOT DELETE : px-6 md:py-2 2xl:py-4 -->
                                                    <div class="col-span-8" @click="toggleHiddenParagraph(item.id)">
                                                        <div class="flex-auto">
                                                            <div class="flex items-baseline justify-between gap-x-4">
                                                                <p class="text-sm font-semibold leading-6 text-red-700 dark:text-white">{{ item.name }}</p>
                                                            </div>
                                                            <p class="mt-1 text-md text-gray-700 leading-relaxed dark:text-red-50">{{ item.description }}</p>
                                                        </div>
                                                        <ul v-show="showHiddenParagraphs[item.id]" role="list" class="text-black text-sm/6 pt-2" :ref="'parentElement' + item.id">
                                                            <li v-for="detail in item.details" :key="detail.id" class="pl-8 my-2" :ref="'hiddenText' + item.id" :data-text="'- ' + detail.text">
                                                            </li>
                                                        </ul>
                                                    </div>
                                                    <div class="col-span-2">
                                                        <div class="flex justify-center">
                                                            <span class="isolate inline-flex rounded-2xl">
                                                                <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                    <div class="relative group">
                                                                        <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4">
                                                                            Ouvrir
                                                                        </div>
                                                                        <button @click="openInNewWindow(item.id_provider)" type="button" class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                                            <eye-icon class="w-5 h-5 text-red-400 group-hover:text-white" />
                                                                        </button>
                                                                    </div>
                                                                </div>
                                                                <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                    <div class="relative group">
                                                                        <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-2">
                                                                            Lu
                                                                        </div>
                                                                        <button @click="markEmailAsRead(item.id)" type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                                            <check-icon class="w-5 h-5 text-red-400 group-hover:text-white" />
                                                                        </button>
                                                                    </div>
                                                                </div>
                                                                <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                    <div class="relative group">
                                                                        <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                                                            Répondre
                                                                        </div>
                                                                        <button @click="openAnswer(item)" type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                                            <arrow-uturn-left-icon class="w-5 h-5 text-red-400 group-hover:text-white" />
                                                                        </button>
                                                                    </div>
                                                                </div>
                                                                <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                    <div class="relative group">
                                                                        <div v-if="showTooltip" class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-10">
                                                                            Paramétrer
                                                                        </div>
                                                                        <Menu as="div" class="relative inline-block text-left">
                                                                            <div>
                                                                                <MenuButton @click="toggleTooltip" class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-red-400 ring-1 ring-inset ring-red-300 hover:bg-red-300 focus:z-10">
                                                                                    <ellipsis-horizontal-icon class="w-5 h-5 group-hover:text-white text-red-400 group-active:text-red-400 group-focus:text-red focus:text-red-400" />
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
                            <li v-if="emails[selectedTopic] && emails[selectedTopic]['Information'] && emails[selectedTopic]['Information'].length > 0" class="py-10 px-8 mx-4 rounded-xl bg-blue-100 bg-opacity-50 hover:border border-blue-700 border-opacity-20"> <!-- ring-1 ring-blue-700 ring-opacity-20 -->
                                <div class="float-right mt-[-25px] mr-[-10px]">
                                    <information-circle-icon class="w-6 h-6 text-blue-500" />
                                </div>
                                <!-- Your content -->
                                <div class="flex">
                                    <div class="flex">
                                        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-blue-500 dark:bg-blue-200">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-white">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                                            </svg>
                                        </span>
                                        <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-blue-800" />-->
                                    </div>
                                    <div class="ml-6 flex-grow">
                                        <div class="overflow-hidden border-l-4 hover:rounded-l-xl border-blue-300 dark:bg-blue-500" style="overflow: visible;">
                                            <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                                <li v-for="item in emails[selectedTopic]['Information'].filter(email => !email.read)" :key="item.id" class="px-6 md:py-2 2xl:py-4 hover:bg-opacity-70 dark:hover:bg-blue-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center" @mouseover="setHoveredItem(item.id)" @mouseleave="clearHoveredItem">
                                                    <div class="col-span-8" @click="toggleHiddenParagraph(item.id)">
                                                        <div class="flex-auto">
                                                            <div class="flex items-baseline justify-between gap-x-4">
                                                                <p class="text-sm font-semibold leading-6 text-blue-800 dark:text-white">{{ item.name }}</p>
                                                            </div>
                                                            <p class="mt-1 text-md text-gray-700 leading-relaxed dark:text-blue-50">{{ item.description }}</p>
                                                        </div>
                                                        <ul v-show="showHiddenParagraphs[item.id]" role="list" class="text-black text-sm/6 pt-2" :ref="'parentElement' + item.id">
                                                            <li v-for="detail in item.details" :key="detail.id" class="pl-8" :ref="'hiddenText' + item.id" :data-text="detail.text">
                                                            </li>
                                                        </ul>
                                                    </div>
                                                    <div class="col-span-2">
                                                        <div class="flex justify-center">
                                                            <span class="isolate inline-flex rounded-2xl">
                                                                <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                    <div class="relative group">
                                                                        <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4 z-40">
                                                                            Ouvrir
                                                                        </div>
                                                                        <button @click="openInNewWindow(item.id_provider)" type="button" class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                                                            <eye-icon class="w-5 h-5 text-blue-400 group-hover:text-white" />
                                                                        </button>
                                                                    </div>
                                                                </div>
                                                                <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                    <div class="relative group">
                                                                        <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-2">
                                                                            Lu
                                                                        </div>
                                                                        <button type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                                                            <check-icon @click="markEmailAsRead(item.id)" class="w-5 h-5 text-blue-400 group-hover:text-white" />
                                                                        </button>
                                                                    </div>
                                                                </div>
                                                                <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                    <div class="relative group">
                                                                        <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                                                            Répondre
                                                                        </div>
                                                                        <button @click="openAnswer(item)" type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-blue-300 hover:bg-blue-300 focus:z-10">
                                                                            <arrow-uturn-left-icon class="w-5 h-5 text-blue-400 group-hover:text-white" />
                                                                        </button>
                                                                    </div>
                                                                </div>
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
                            <div v-if="emails[selectedTopic] && emails[selectedTopic]['Useless'] && emails[selectedTopic]['Useless'].length" class="flex-1 mx-4 mt-4 rounded-xl bg-gray-100 hover:border border-gray-700 border-opacity-20" @click="toggleEmailVisibility">
                                <li class="py-10 px-8"> <!-- ring-1 ring-red-700 ring-opacity-20 --> <!-- BUG A CORRIGER : ESPACE BLANC BOTTOM -->
                                    <div class="float-right mt-[-25px] mr-[-10px]">
                                        <trash-icon class="w-6 h-6 text-gray-500" />
                                    </div>
                                    <!-- Your content -->
                                    <div class="flex">
                                        <div class="flex">
                                            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-400 dark:bg-red-200">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-white">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                                                </svg>                                            
                                            </span>
                                            <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-500" />-->
                                        </div>
                                        <div class="ml-6 ">
                                            <div class="overflow-hidden border-l-4 hover:rounded-l-xl border-gray-500">
                                                <ul role="list" class="divide-y divide-gray-200 dark:divide-white">
                                                    <li class="px-6 py-4 hover:bg-opacity-70 dark:hover:bg-opacity-100">
                                                        <div class="flex-auto">
                                                            Vous avez reçu <span class="font-semibold text-gray-900 dark:text-white hover:text-gray-700">{{ emails[selectedTopic]['Useless'].length }}</span> <span v-if="emails[selectedTopic]['Useless'].length === 1">mail inutile</span><span v-else>mails inutiles</span>. Cliquez pour voir.
                                                        </div>
                                                        <ul v-if="showEmailDescriptions" class="text-gray-900 text-sm/6 pl-8 divide-y divide-gray-200">
                                                            <li class="py-5 grid grid-cols-10" v-for="item in emails[selectedTopic]['Useless']" :key="item.id" @mouseover="setHoveredItem(item.id)" @mouseleave="clearHoveredItem">
                                                               <div class="col-span-8 flex-auto">
                                                                    <div class="flex items-baseline justify-between gap-x-4">
                                                                        <p class="text-sm font-semibold leading-6 text-gray-800 dark:text-white">{{ item.name }}</p>
                                                                    </div>
                                                                    <p>{{ item.description }}</p>
                                                               </div>
                                                               <div class="col-span-2 pt-2">
                                                                    <div class="flex justify-center">
                                                                        <span class="isolate inline-flex rounded-2xl">
                                                                            <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                                <div class="relative group">
                                                                                    <div class="absolute hidden group-hover:block bg-black text-white text-sm py-2 px-4 rounded shadow-lg mt-[-45px] -ml-4">
                                                                                        Ouvrir
                                                                                    </div>
                                                                                    <button @click="openInNewWindow(item.id_provider)" type="button" class="inline-flex items-center px-2 py-1.5 rounded-l-2xl text-gray-400 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                                                                        <eye-icon class="w-5 h-5 text-gray-500 group-hover:text-white" />
                                                                                    </button>
                                                                                </div>
                                                                            </div>
                                                                            <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                                <div class="relative group">
                                                                                    <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-6">
                                                                                        Bloquer
                                                                                    </div>
                                                                                    <button type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                                                                        <HandRaisedIcon @click="setRuleBlockForSender(item.id)" class="w-5 h-5 text-gray-500 group-hover:text-white" />
                                                                                    </button>
                                                                                </div>
                                                                            </div>
                                                                            <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                                <div class="relative group">
                                                                                    <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                                                                        Répondre
                                                                                    </div>
                                                                                    <button @click="openAnswer(item)" type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                                                                        <arrow-uturn-left-icon class="w-5 h-5 text-gray-500 group-hover:text-white" />
                                                                                    </button>
                                                                                </div>
                                                                            </div>
                                                                            <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                                <div class="relative group">
                                                                                    <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-10">
                                                                                        Paramétrer
                                                                                    </div>
                                                                                    <Menu as="div" class="relative inline-block text-left">
                                                                                        <div>
                                                                                            <MenuButton @click="toggleTooltip" class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-gray-500 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                                                                                <ellipsis-horizontal-icon class="w-5 h-5 group-hover:text-white text-gray-500 group-active:text-gray-500 group-focus:text-red focus:text-gray-500" />
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
                                                                            </div>
                                                                        </span> 
                                                                    </div>
                                                                </div>
                                                            </li>
                                                        </ul>
                                                    </li>
                                                    <!-- More items... -->
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </div>
                            <div v-if="readEmailsInSelectedTopic.length" class="flex-1 mx-4 mt-4 rounded-xl bg-emerald-100 hover:border border-emerald-700 border-opacity-20" @click="toggleReadEmailVisibility">
                                <li class="py-10 px-8"> <!-- ring-1 ring-red-700 ring-opacity-20 --> <!-- BUG A CORRIGER : ESPACE BLANC BOTTOM -->
                                    <div class="float-right mt-[-25px] mr-[-10px]">
                                        <CheckIcon class="w-6 h-6 text-emerald-500" />
                                    </div>
                                    <!-- Your content -->
                                    <div class="flex">
                                        <div class="flex">
                                            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-emerald-400">
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-white">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                                                </svg>                                            
                                            </span>
                                            <!--<ChatBubbleOvalLeftEllipsisIcon class="w-6 h-6 text-red-500" />-->
                                        </div>
                                        <div class="ml-6 w-full"> <!-- To check : strange w-full not necessary in grey but it must be here to have the correct space for readEmailsInSelectedTopic -->
                                            <div class="overflow-hidden border-l-4 hover:rounded-l-xl border-emerald-500 w-full">
                                                <ul role="list" class="divide-y divide-gray-200 dark:divide-white w-full">
                                                    <li class="px-6 py-4 hover:bg-opacity-70 dark:hover:bg-opacity-100 w-full">
                                                        <div class="flex-auto">
                                                            Vous avez récemment lu <span class="font-semibold text-gray-900 dark:text-white hover:text-gray-700">{{ readEmailsInSelectedTopic.length }}</span> <span v-if="readEmailsInSelectedTopic.length === 1">mail</span><span v-else>mails</span>. Cliquez pour voir. Je <span class="font-medium">vais nettoyer automatiquement</span> les mails lus.
                                                        </div>
                                                        <ul v-if="showEmailReadDescriptions" class="text-gray-900 text-sm/6 pl-8 divide-y divide-gray-300 w-full">
                                                            <li class="py-5 grid grid-cols-10 w-full" v-for="item in readEmailsInSelectedTopic" :key="item.id" @mouseover="setHoveredItem(item.id)" @mouseleave="clearHoveredItem">
                                                               <div class="col-span-8">
                                                                    <div class="flex-auto">
                                                                        <div class="flex items-baseline justify-between gap-x-4">
                                                                            <p class="text-sm font-semibold leading-6 text-emerald-800 dark:text-white">{{ item.name }}</p>
                                                                        </div>
                                                                        <p>{{ item.description }}</p>
                                                                    </div>
                                                               </div>
                                                               <div class="col-span-2 pt-2">
                                                                    <div class="flex justify-center">
                                                                        <span class="isolate inline-flex rounded-2xl">
                                                                            <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                                <div class="relative group">
                                                                                    <div class="absolute hidden group-hover:block bg-black text-white text-sm py-2 px-4 rounded shadow-lg mt-[-45px] -ml-4">
                                                                                        Ouvrir
                                                                                    </div>
                                                                                    <button @click="openInNewWindow(item.id_provider)" type="button" class="inline-flex items-center px-2 py-1.5 rounded-l-2xl text-emerald-400 ring-1 ring-inset ring-emerald-400 hover:bg-emerald-400 focus:z-10">
                                                                                        <eye-icon class="w-5 h-5 text-emerald-500 group-hover:text-white" />
                                                                                    </button>
                                                                                </div>
                                                                            </div>
                                                                            <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                                <div class="relative group">
                                                                                    <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-6">
                                                                                        Supprimer
                                                                                    </div>
                                                                                    <button type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-emerald-400 hover:bg-emerald-400 focus:z-10">
                                                                                        <TrashIcon @click="deleteEmail(item.id)" class="w-5 h-5 text-emerald-500 group-hover:text-white" />
                                                                                    </button>
                                                                                </div>
                                                                            </div>
                                                                            <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                                <div class="relative group">
                                                                                    <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                                                                                        Répondre
                                                                                    </div>
                                                                                    <button @click="openAnswer(item)" type="button" class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-emerald-400 hover:bg-emerald-400 focus:z-10">
                                                                                        <arrow-uturn-left-icon class="w-5 h-5 text-emerald-500 group-hover:text-white" />
                                                                                    </button>
                                                                                </div>
                                                                            </div>
                                                                            <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                                                <div class="relative group">
                                                                                    <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-10">
                                                                                        Paramétrer
                                                                                    </div>
                                                                                    <Menu as="div" class="relative inline-block text-left">
                                                                                        <div>
                                                                                            <MenuButton @click="toggleTooltip" class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-green-500 ring-1 ring-inset ring-green-400 hover:bg-green-400 focus:z-10">
                                                                                                <ellipsis-horizontal-icon class="w-5 h-5 group-hover:text-white text-green-500 group-active:text-green-500 group-focus:text-red focus:text-green-500" />
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
                                                                            </div>
                                                                        </span> 
                                                                    </div>
                                                                </div>
                                                            </li>
                                                        </ul>
                                                    </li>
                                                    <!-- More items... -->
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
    <NewCategoryModal
      :isOpen="isModalOpen"
      :errorMessage="modalErrorMessage"
      @closeModal="closeModal"
      @addCategory="handleAddCategory"
    />
    <UpdateCategoryModal
    :isOpen="isModalUpdateOpen" 
    :errorMessage="modalUpdateErrorMessage"
    :category="categoryToUpdate"
    @closeModal="closeUpdateModal"
    @updateCategory="handleUpdateCategory"
    @deleteCategory="handleCategoryDelete"
    />
    <!-- Notification new category created -->
    <div aria-live="assertive" class="pointer-events-none fixed inset-0 flex items-end px-4 py-6 sm:p-6">
        <div class="flex w-full flex-col items-center space-y-4 sm:items-end">
        <transition
            enter-active-class="transform ease-out duration-300 transition"
            enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
            enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
            leave-active-class="transition ease-in duration-100"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0">
            <div v-if="showNewCategoryNotif" class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-green-300 shadow-lg ring-1 ring-black ring-opacity-5">
            <div class="p-4">
                <div class="flex items-start">
                <div class="flex-shrink-0">
                    <CheckCircleIcon class="h-6 w-6 text-gray-900" aria-hidden="true" />
                </div>
                <div class="ml-3 w-0 flex-1 pt-0.5">
                    <p class="text-sm font-medium text-gray-900">Categorie créée !</p>
                    <p class="mt-1 text-sm text-gray-900">Votre catégorie a été créée avec succès</p>
                </div>
                <div class="ml-4 flex flex-shrink-0">
                    <button type="button" @click="showNewCategoryNotif = false" class="inline-flex rounded-md text-gray-900 hover:text-black focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2">
                    <span class="sr-only">Close</span>
                    <XMarkIcon class="h-5 w-5 text-gray-900" aria-hidden="true" />
                    </button>
                </div>
                </div>
            </div>
            </div>
        </transition>
        </div>
    </div>
    <!-- Notification category updated -->
    <div aria-live="assertive" class="pointer-events-none fixed inset-0 flex items-end px-4 py-6 sm:p-6">
        <div class="flex w-full flex-col items-center space-y-4 sm:items-end">
        <transition
            enter-active-class="transform ease-out duration-300 transition"
            enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
            enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
            leave-active-class="transition ease-in duration-100"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0">
            <div v-if="showUpdateCategoryNotif" class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-green-300 shadow-lg ring-1 ring-black ring-opacity-5">
            <div class="p-4">
                <div class="flex items-start">
                <div class="flex-shrink-0">
                    <CheckCircleIcon class="h-6 w-6 text-gray-900" aria-hidden="true" />
                </div>
                <div class="ml-3 w-0 flex-1 pt-0.5">
                    <p class="text-sm font-medium text-gray-900">Categorie mis à jour !</p>
                    <p class="mt-1 text-sm text-gray-900">Votre catégorie a été mis à jour avec succès</p>
                </div>
                <div class="ml-4 flex flex-shrink-0">
                    <button type="button" @click="showUpdateCategoryNotif = false" class="inline-flex rounded-md text-gray-900 hover:text-black focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2">
                    <span class="sr-only">Close</span>
                    <XMarkIcon class="h-5 w-5 text-gray-900" aria-hidden="true" />
                    </button>
                </div>
                </div>
            </div>
            </div>
        </transition>
        </div>
    </div>
    <!-- Notification category deleted -->
    <div aria-live="assertive" class="pointer-events-none fixed inset-0 flex items-end px-4 py-6 sm:p-6">
        <div class="flex w-full flex-col items-center space-y-4 sm:items-end">
        <transition
            enter-active-class="transform ease-out duration-300 transition"
            enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
            enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
            leave-active-class="transition ease-in duration-100"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0">
            <div v-if="showDeleteCategoryNotif" class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-green-300 shadow-lg ring-1 ring-black ring-opacity-5">
            <div class="p-4">
                <div class="flex items-start">
                <div class="flex-shrink-0">
                    <CheckCircleIcon class="h-6 w-6 text-gray-900" aria-hidden="true" />
                </div>
                <div class="ml-3 w-0 flex-1 pt-0.5">
                    <p class="text-sm font-medium text-gray-900">Categorie supprimé !</p>
                    <p class="mt-1 text-sm text-gray-900">Votre catégorie a été supprimée avec succès</p>
                </div>
                <div class="ml-4 flex flex-shrink-0">
                    <button type="button" @click="showDeleteCategoryNotif = false" class="inline-flex rounded-md text-gray-900 hover:text-black focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2">
                    <span class="sr-only">Close</span>
                    <XMarkIcon class="h-5 w-5 text-gray-900" aria-hidden="true" />
                    </button>
                </div>
                </div>
            </div>
            </div>
        </transition>
        </div>
    </div>
    <ModalSeeMail :isOpen="showModal" :email="selectedEmail" @update:isOpen="updateModalStatus" />
    </div>
</template>

<script>
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';
import ModalSeeMail from '../components/SeeMail.vue';
import NewCategoryModal from '../components/NewCategoryModal.vue';
import UpdateCategoryModal from '../components/UpdateCategoryModal.vue';
import { ref } from 'vue';
import { fetchWithToken } from '../router/index.js';
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
    },
    methods: {
        // To redirect to the page rules to edit a rule
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
        toggleReadEmailVisibility() {
            this.showEmailReadDescriptions = !this.showEmailReadDescriptions;
            this.scrollToBottom();
        },
        toggleEmailVisibility() {
            this.showEmailDescriptions = !this.showEmailDescriptions;
            if (this.readEmailsInSelectedTopic.length == 0){
                this.scrollToBottom();
            } else {
                this.scrollAlmostToBottom();
            }
        },
        scrollToBottom() {
            this.$nextTick(() => {
                const element = this.$refs.scrollableDiv;
                element.scrollTop = element.scrollHeight;
            });
        },
        scrollAlmostToBottom() {
            this.$nextTick(() => {
                const element = this.$refs.scrollableDiv;
                const offset = 100; // Adjust this value as needed
                element.scrollTop = element.scrollHeight - offset;
            });
        },
        toggleTooltip() {
            this.showTooltip = false;
            this.isDropdownOpen = true;
        },
        toggleDropdown() {
            this.showDropdown = !this.showDropdown;
        },
        async markEmailAsRead(emailId) {
            try {
                const response = await fetchWithToken(`http://localhost:9000/MailAssistant/user/emails/${emailId}/mark-read/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
                });

                if (response.read) {
                    // Handle successful response
                    this.updateEmailReadStatus(emailId);
                } else {
                    console.log("RESPONSE", response);
                    console.error('Failed to mark email as read');
                }
            } catch (error) {
                console.error('Error in markEmailAsRead:', error.message);
            }
        },
        updateEmailReadStatus(emailId) {
            // Iterate over each category in the emails object
            for (const category in this.emails) {
                if (Object.hasOwnProperty.call(this.emails, category)) {
                // Iterate over each subcategory within the category
                for (const subcategory in this.emails[category]) {
                    if (Array.isArray(this.emails[category][subcategory])) {
                    // Find the index of the email with the given ID in the current subcategory's array
                    const emailIndex = this.emails[category][subcategory].findIndex(email => email.id === emailId);
                    if (emailIndex !== -1) {
                        // Email found, update its read status
                        this.emails[category][subcategory][emailIndex].read = true;
                        return; // Stop the function as we've found and updated the email
                    }
                    }
                }
                }
            }
        },
        async markEmailReplyLater(emailId) {
            try {
                const response = await fetchWithToken(`http://localhost:9000/MailAssistant/user/emails/${emailId}/mark-reply-later/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                if (response.answer_later) {
                    console.log("Email marked for reply later successfully");
                    this.isMenuOpen = false;
                } else {
                    console.error('Failed to mark email for reply later', response);
                }
            } catch (error) {
                console.error('Error in markEmailReplyLater:', error.message);
            }
        },
        deleteEmailFromState(emailId) {
            // Iterate over each category in the emails object
            for (const category in this.emails) {
                if (Object.prototype.hasOwnProperty.call(this.emails, category)) {
                    // Iterate over each subcategory within the category
                    for (const subcategory in this.emails[category]) {
                        if (Array.isArray(this.emails[category][subcategory])) {
                            // Find the index of the email with the given ID in the current subcategory's array
                            const emailIndex = this.emails[category][subcategory].findIndex(email => email.id === emailId);
                            if (emailIndex !== -1) {
                                // Email found, delete it from the array
                                this.emails[category][subcategory].splice(emailIndex, 1);
                                return; // Stop the function as we've found and deleted the email
                            }
                        }
                    }
                }
            }
        },
        async setRuleBlockForSender(emailId) {
            try {
                const response = await fetchWithToken(`http://localhost:9000/MailAssistant/user/emails/${emailId}/block-sender/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                console.log("RESPONSE", response);
                if (response.block) {
                    console.log("Rule set successfully");
                    // You can now update the UI or state to reflect this change
                    this.deleteEmail(emailId);
                } else {
                    console.error('Failed to set block rule for sender');
                }
            } catch (error) {
                console.error('Error in setRuleBlockForSender:', error.message);
            }
        },
        /*openModal(email) {
            this.selectedEmail = email; // Set the email data for the clicked email
            this.showModal = true; // Open the modal
        },*/
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
                        'Content-Type': 'application/json'
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
                        id_provider : JSON.stringify(email.id_provider),
                        details: JSON.stringify(email.details)
                    }
                });
            } catch (error) {
                console.error("There was a problem with the fetch operation:", error);
            }
        },
        updateModalStatus(status) {
            this.showModal = status;
        },
        async animateText() {
            try {
                const requestOptions = {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'email': localStorage.getItem('email')
                    },
                };

                const data = await fetchWithToken('http://localhost:9000/MailAssistant/api/unread_mails/', requestOptions);


                const unreadMailCount = data.unreadCount;
                let text = '';

                if (unreadMailCount === 0) {
                    text = `Bonjour ! Vous n'avez pas de nouveaux mails.`;
                } else if (unreadMailCount === 1) {
                    text = `Bonjour ! Vous avez reçu ${unreadMailCount} nouveau mail.`;
                } else {
                    text = `Bonjour ! Vous avez reçu ${unreadMailCount} nouveaux mails.`;
                }

                let target = this.$refs.animatedText;
                let characters = text.split("");
                let currentIndex = 0;
                const interval = setInterval(() => {
                    if (currentIndex < characters.length) {
                        target.textContent += characters[currentIndex];
                        currentIndex++;
                    } else {
                        clearInterval(interval);
                    }
                }, 30);
            } catch (error) {
                console.error('Error trying to get the number of unread emails:', error);
            }
        },
        toggleHiddenParagraph(index) {
            console.log("Item ID:",index)
            console.log("All refs:",this.$refs)
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
        selectCategory(category) {
            this.selectedTopic = category.name;
            console.log("CHANGE CATEGORY");
        },
        openModal() {
            this.isModalOpen = true;
        },
        closeModal() {
            this.isModalOpen = false;
        },
        openUpdateModal(category) {
            console.log("CATEGORY TO UPDATE : ", category);
            this.oldCategoryName = category.name;
            this.categoryToUpdate = category;
            this.isModalUpdateOpen = true;
        },
        closeUpdateModal() {
            this.isModalUpdateOpen = false;
        },
        async handleAddCategory(categoryData) {
            console.log('Category Added:', categoryData);
            try {
                const response = await fetchWithToken('http://localhost:9000/MailAssistant/api/set_category/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: categoryData.name,
                    description: categoryData.description,
                }),
                });

                if (response) {
                    console.log('Category added:', response);
                    this.showNewCategoryNotif = true;
                    this.closeModal();
                    const categoryData = await fetchWithToken(`http://localhost:9000/MailAssistant/user/categories/`);
                    console.log("CategoryData", categoryData);
                    this.categories = categoryData.map(category => ({
                        name: category.name,
                        description: category.description
                    }));
                    console.log("Assigned categories:", this.categories);
                    setTimeout(() => {
                        this.showNewCategoryNotif = false;
                    }, 2000);

                }
            } catch (error) {
                console.error('Error adding category:', error);
                this.showNewCategoryNotif = false; 
                // Handle the error
            }
        },
        async handleUpdateCategory(updatedCategory) {
            console.log('Category Data to Update:', updatedCategory);
            if (!updatedCategory.name.trim()) {
                console.error('Error: Category name cannot be empty');
                return;
            }
            const updateData = {
                name: updatedCategory.name,
                description: updatedCategory.description
            };
            try {
                const url = `http://localhost:9000/MailAssistant/api/update_category/${this.oldCategoryName}/`; // Adjust the URL as needed
                const options = {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updateData)
                };
                const response = await fetchWithToken(url, options);

                if (response) {
                    console.log('Category updated:', response);
                    this.showUpdateCategoryNotif = true;
                    this.closeUpdateModal();
                    const categoryData = await fetchWithToken(`http://localhost:9000/MailAssistant/user/categories/`);
                    console.log("CategoryData", categoryData);
                    this.categories = categoryData.map(category => ({
                        name: category.name,
                        description: category.description
                    }));
                    console.log("Assigned categories:", this.categories);
                    setTimeout(() => {
                        this.showUpdateCategoryNotif = false;
                    }, 2000);
                }
            } catch (error) {
                console.error('Error updating category:', error);
                this.showUpdateCategoryNotif = false;
                // Handle the error
            }
        },
        async handleCategoryDelete(categoryNameToDelete) {
            console.log("Category to delete", categoryNameToDelete);
            if (!categoryNameToDelete.trim()) {
                console.error('Error: Category name cannot be empty');
                return;
            }

            try {
                const url = `http://localhost:9000/MailAssistant/api/delete_category/${categoryNameToDelete}/`;

                const options = {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                };

                const response = await fetchWithToken(url, options);

                if (response) {
                    console.log('Category deleted:', response);
                    this.showDeleteCategoryNotif = true;
                    this.closeUpdateModal();
                    // Fetch the categories
                    const categoryData = await fetchWithToken(`http://localhost:9000/MailAssistant/user/categories/`);
                    console.log("CategoryData", categoryData);
                    this.categories = categoryData.map(category => ({
                        name: category.name,
                        description: category.description
                    }));
                    console.log("Assigned categories:", this.categories);
                    setTimeout(() => {
                        this.showDeleteCategoryNotif = false;
                    }, 2000)
                }
            } catch (error) {
                console.error('Error deleting category:', error);
                this.showDeleteCategoryNotif = false;
                // Handle the error
            }
        }
    },
    async mounted() {
        console.log("COOKIES",document.cookie);

        const showNotification = ref(false);
        this.bgColor = localStorage.getItem('bgColor');
        this.animateText();

        try {
            // Fetch the categories
            const categoryData = await fetchWithToken(`http://localhost:9000/MailAssistant/user/categories/`);
            console.log("CategoryData", categoryData);
            this.categories = categoryData.map(category => ({
                name: category.name,
                description: category.description
            }));
            console.log("Assigned categories:", this.categories);

            // Fetch emails
            const emailData = await fetchWithToken(`http://localhost:9000/MailAssistant/user/emails/`);
            //console.log('fetchData: ',emailData)
            this.emails = emailData;

            /* 
            // To test ONLY => select your category and inject this 
            var newInfo = {
                id: 10,
                "id_provider": "18b8c0673cea41ba",
                email: "hanna.williams@esaip.org",
                name: "Kraken",
                read: false,
                description: "Mettre en place un dispositif d'accompagnement pour Malcom MOREL, qui est impliqué dans un projet entrepreneurial.",
            };
            this.emails.Administrative.Information.push(newInfo);
            var newInfo2 = {
                id: 3,
                "id_provider": "18b8c0673cea41ba",
                email: "hanna.williams@esaip.org",
                name: "Christophe",
                read: true,
                description: "Participer au stage de formation des enseignants chercheurs en anglais la 1ère semaine de février",
            };
            this.emails.Administrative.Information.push(newInfo2);
            var newInfo3 = {
                id: 4,
                "id_provider": "18b8c0673cea41ba",
                email: "hanna.williams@esaip.org",
                name: "Christophe",
                read: true,
                description: "Participer au stage de formation des enseignants chercheurs en anglais la 1ère semaine de février",
            };
            this.emails.Administrative.Information.push(newInfo3);*/
            /*
            var newUseless = {
                id: 5,
                "id_provider": "18b8c0673cea41ba",
                email: "hanna.williams@esaip.org",
                name: "Blablacar",
                read: false,
                description: "Publicité de blablacar qui vous présente un bon de -10€ sur votre premier trajet, offre valable 2 mois et non remboursable",
            };
            this.emails.Administrative.Useless.push(newUseless);
            var newUseless2 = {
                id: 6,
                "id_provider": "18b8c0673cea41ba",
                email: "hanna.williams@esaip.org",
                name: "Blablacar",
                read: false,
                description: "Newsletter de castorama qui propose de découvrir des nouvelles cuisines intégrer dans leur catalogues",
            };
            this.emails.Administrative.Useless.push(newUseless2);*/
            console.log("EMAIL", this.emails);

        } catch (error) {
            console.error('Failed to fetch data:', error);
        }

        // To handle answer sent
        if (localStorage.getItem('Email_sent')){
            localStorage.setItem('Email_sent', '');
            showNotification.value = true;
            setTimeout(() => {
                showNotification.value = false;
            }, 5000);
        }
    },
    computed: {
        readEmailsInSelectedTopic() {
            let combinedEmails = [];
            for (let category in this.emails[this.selectedTopic]) {
                combinedEmails = combinedEmails.concat(this.emails[this.selectedTopic][category]);
            }

            return combinedEmails.filter(email => email.read);
        },
        totalEmailsInCategory() {
            return (categoryName) => {
            let totalCount = 0;
            if (this.emails[categoryName]) {
                for (let subcategory of Object.values(this.emails[categoryName])) {
                totalCount += subcategory.length;
                }
            }
            return totalCount;
            };
        }
    },
    data() {
        return {
            // showHiddenParagraphs: [false, false, false, false, false],
            showHiddenParagraphs: {},
            animationTriggered: [false, false, false],
            showModal: false,
            isModalOpen: false,
            isModalUpdateOpen: false,
            modalErrorMessage: '',
            modalUpdateErrorMessage: '',
            selectedCategory: null,
            categoryToUpdate: null,
            messageText: '',
            categories: [],
            selectedTopic: 'Administrative',
            bgColor: 'bg-gradient-to-r from-sky-300 to-blue-300',
            selectedEmail: null,
            showNewCategoryNotif: false,
            showUpdateCategoryNotif: false,
            showDeleteCategoryNotif: false,
            hoveredItemId: null,
            oldCategoryName: '',
            showEmailDescriptions: false, // To display useless mail
            showEmailReadDescriptions: false, // To display read mail
            showDropdown: false,
            showTooltip: true,
            isMenuOpen: true,
            isDropdownOpen: false,
            // emails: { "": {
            //     "Important": [],
            //     "Information": [],
            //     "Useless": []
            //     }
            // }
            emails: {}
            // items: [{id: 1, name: 'Jean', description: 'test', topic: 'ESAIP', importance: 'Information', details: [{id: 1, text: 'text'},{id: 3, text: 'bullet'},{id: 2, text: 'blabla'}]},
            // {id: 23, name: 'Marc', description: 'Premier test', topic: 'ESAIP', importance: 'Important', details: [{id: 4, text: 'bonjour'},{id: 6, text: 'ok'},{id: 5, text: 'enfin'}]}
            
            // ],
            // items: {
            //     "ESAIP": {
            //         "Important": [
            //             {
            //                 id: 1, 
            //                 name: 'Jean', 
            //                 description: 'test', 
            //                 details: [
            //                     {id: 1, text: 'text'},
            //                     {id: 3, text: 'bullet'},
            //                     {id: 2, text: 'blabla'}
            //                 ]
            //             }
            //         ],
            //         "Information": [
            //             {
            //                 id: 2, 
            //                 name: 'Marc', 
            //                 description: 'Premier test', 
            //                 details: [
            //                     {id: 4, text: 'bonjour'},
            //                     {id: 6, text: 'ok'},
            //                     {id: 5, text: 'enfin'}
            //                 ]
            //             }
            //         ]
            //     },
            //     "Autres": {
            //         "Important": [
            //             {
            //                 id: 3, 
            //                 name: 'Banque', 
            //                 description: 'test', 
            //                 details: [
            //                     {id: 7, text: 'prêt'},
            //                     {id: 8, text: 'argent'},
            //                     {id: 9, text: 'euro'}
            //                 ]
            //             }
            //         ],
            //         "Information": [
            //             {
            //                 id: 4, 
            //                 name: 'Avocat', 
            //                 description: 'Premier test', 
            //                 details: [
            //                     {id: 10, text: 'contrat'},
            //                     {id: 11, text: 'frais'},
            //                     {id: 12, text: 'fruit'}
            //                 ]
            //             }
            //         ]
            //     }
            //     // ... potentially other topics
            // }
        }
    }
}
</script>
