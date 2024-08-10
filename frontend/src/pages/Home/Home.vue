<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
    />
    <div class="flex flex-col justify-center items-center h-screen">
        <div class="flex h-full w-full">
            <div class="w-[90px] 2xl:w-[100px] bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <NavBarSmall />
            </div>

            <div class="flex-1">
                <div class="flex flex-col h-full w-full">
                    <main
                        class="bg-gray-50 ring-1 shadow-sm ring-black ring-opacity-5 border-b border-black shadow-sm border-opacity-10"
                    >
                        <div class="w-full py-2 2xl:py-3 px-4 2xl:px-8 lg:px-2">
                            <div class="grid grid-cols-11 gap-4 items-center divide-x divide-gray-300">
                                <div class="pl-4 col-span-11 h-full flex items-center">
                                    <div class="w-full flex items-center justify-center">
                                        <!--selection des tabs-->
                                        <div class="sm:hidden">
                                            <label for="tabs" class="sr-only">Select a tab</label>
                                            <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
                                            <select
                                                id="tabs"
                                                name="tabs"
                                                class="block w-full rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
                                                v-model="selectedTopic"
                                            >
                                                <option v-for="category in categories" :key="category">
                                                    {{ category.name }}
                                                </option>
                                            </select>
                                        </div>

                                        <!--categories list-->
                                        <div class="hidden sm:block w-full py-5">
                                            <nav
                                                class="flex flex-wrap space-x-2 2xl:space-x-4 justify-center items-center w-full"
                                                aria-label="Tabs"
                                            >
                                                <div class="flex space-x-4 2xl:space-x-6">
                                                    <!--On parcours la liste decategories -->
                                                    <a
                                                        v-for="category in categories"
                                                        :key="category"
                                                        class="group items-center text-gray-600 text-sm font-medium"
                                                    >
                                                        <!-- To FIX => put category.name and adapt the design -->

                                                        <!--catégories que l'utilisateur a créer-->
                                                        <div
                                                            v-if="category.name !== 'Others'"
                                                            class="flex cursor-pointer"
                                                            @click="selectCategory(category)"
                                                        >
                                                            <span
                                                                class="px-3 py-2 group-hover:rounded-r-none"
                                                                :class="{
                                                                    'bg-gray-500 bg-opacity-10 text-gray-800':
                                                                        selectedTopic === category.name,
                                                                    'group-hover:bg-gray-500 rounded-l-md group-hover:bg-opacity-10':
                                                                        selectedTopic !== category.name,
                                                                    'rounded-md':
                                                                        totalEmailsInCategoryNotRead(category.name) ===
                                                                        0,
                                                                    'rounded-l-md':
                                                                        totalEmailsInCategoryNotRead(category.name) > 0,
                                                                }"
                                                            >
                                                                {{ category.name }}
                                                            </span>
                                                            <div
                                                                class="group-hover:bg-gray-500 group-hover:rounded-r-none group-hover:bg-opacity-10 flex items-center"
                                                                :class="{
                                                                    'bg-gray-500 bg-opacity-10 rounded-r-md':
                                                                        selectedTopic === category.name,
                                                                }"
                                                            >
                                                                <span
                                                                    v-if="
                                                                        totalEmailsInCategoryNotRead(category.name) > 0
                                                                    "
                                                                    class="group-hover:bg-transparent group-hover:text-gray-800 rounded-full py-0.5 px-2.5 text-xs font-medium"
                                                                    :class="{
                                                                        'text-gray-800':
                                                                            selectedTopic === category.name,
                                                                        'text-white bg-gray-800':
                                                                            selectedTopic !== category.name,
                                                                    }"
                                                                >
                                                                    {{ totalEmailsInCategoryNotRead(category.name) }}
                                                                </span>
                                                            </div>
                                                            <span
                                                                class="opacity-0 group-hover:opacity-100 pr-2 py-2 group-hover:bg-gray-500 rounded-r-md group-hover:bg-opacity-10"
                                                            >
                                                                <svg
                                                                    xmlns="http://www.w3.org/2000/svg"
                                                                    fill="none"
                                                                    viewBox="0 0 24 24"
                                                                    stroke-width="1.5"
                                                                    stroke="currentColor"
                                                                    class="w-5 h-5 hover:text-black"
                                                                    @click.stop="openUpdateModal(category)"
                                                                >
                                                                    <path
                                                                        stroke-linecap="round"
                                                                        stroke-linejoin="round"
                                                                        d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
                                                                    />
                                                                </svg>
                                                            </span>
                                                        </div>

                                                        <!--categories Autres,Others-->
                                                        <div v-else class="flex pr-7">
                                                            <span
                                                                class="px-3 py-2 cursor-pointer"
                                                                @click="selectCategory(category)"
                                                                :class="{
                                                                    'bg-gray-500 bg-opacity-10 text-gray-800':
                                                                        selectedTopic === category.name,
                                                                    'group-hover:bg-gray-500 rounded-l-md group-hover:bg-opacity-10':
                                                                        selectedTopic !== category.name,
                                                                    'rounded-md':
                                                                        totalEmailsInCategoryNotRead(category.name) ===
                                                                        0,
                                                                    'rounded-l-md':
                                                                        totalEmailsInCategoryNotRead(category.name) > 0,
                                                                }"
                                                            >
                                                                {{ $t("homePage.otherCategory") }}
                                                            </span>
                                                            <div
                                                                @click="selectCategory(category)"
                                                                class="group-hover:bg-gray-500 group-hover:rounded-r group-hover:bg-opacity-10 flex items-center cursor-pointer"
                                                                :class="{
                                                                    'bg-gray-500 bg-opacity-10 rounded-r-md':
                                                                        selectedTopic === category.name,
                                                                }"
                                                            >
                                                                <span
                                                                    v-if="
                                                                        totalEmailsInCategoryNotRead(category.name) > 0
                                                                    "
                                                                    class="group-hover:bg-transparent group-hover:text-gray-800 rounded-full py-0.5 px-2.5 text-xs font-medium"
                                                                    :class="{
                                                                        'text-gray-800':
                                                                            selectedTopic === category.name,
                                                                        'text-white bg-gray-800':
                                                                            selectedTopic !== category.name,
                                                                    }"
                                                                >
                                                                    {{ totalEmailsInCategoryNotRead(category.name) }}
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </a>
                                                </div>

                                                <a
                                                    class="flex text-gray-600 rounded-md px-8 py-2 text-sm font-medium hover:bg-gray-900 hover:text-white"
                                                    @click="openModal"
                                                >
                                                    <svg
                                                        xmlns="http://www.w3.org/2000/svg"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke-width="1.5"
                                                        stroke="currentColor"
                                                        class="w-6 h-6"
                                                    >
                                                        <path
                                                            stroke-linecap="round"
                                                            stroke-linejoin="round"
                                                            d="M12 4.5v15m7.5-7.5h-15"
                                                        />
                                                    </svg>
                                                </a>
                                            </nav>
                                        </div>

                                        <div class="flex justify-end h-full">
                                            <button
                                                @click="toggleVisibility"
                                                class="bg-gray-200 text-gray-500 p-2 rounded-full items-center inline-flex"
                                            >
                                                <svg
                                                    v-if="isHidden"
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    fill="none"
                                                    viewBox="0 0 24 24"
                                                    stroke-width="1.5"
                                                    stroke="currentColor"
                                                    class="w-6 h-6"
                                                >
                                                    <path
                                                        stroke-linecap="round"
                                                        stroke-linejoin="round"
                                                        d="m18.75 4.5-7.5 7.5 7.5 7.5m-6-15L5.25 12l7.5 7.5"
                                                    />
                                                </svg>
                                                <svg
                                                    v-else
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    fill="none"
                                                    viewBox="0 0 24 24"
                                                    stroke-width="1.5"
                                                    stroke="currentColor"
                                                    class="w-6 h-6"
                                                >
                                                    <path
                                                        stroke-linecap="round"
                                                        stroke-linejoin="round"
                                                        d="m5.25 4.5 7.5 7.5-7.5 7.5m6-15 7.5 7.5-7.5 7.5"
                                                    />
                                                </svg>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </main>

                    <div class="w-full relative">
                        <Searchbar @input="updateSearchQuery" :showFilterButton="true" />
                    </div>

                    <!--L'utilisateur n'a pas de nouveau mail-->
                    <div v-if="isEmptyTopic()" class="flex-1 bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                        <div v-if="isEmptyTopic()" class="flex flex-col w-full h-full rounded-xl">
                            <div
                                class="flex flex-col justify-center items-center h-full m-5 rounded-lg border-2 border-dashed border-gray-400 p-12 text-center hover:border-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1"
                                    stroke="currentColor"
                                    class="mx-auto h-14 w-14 text-gray-400"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
                                    />
                                </svg>
                                <span class="mt-2 block text-md font-semibold text-gray-900">
                                    {{ $t("homePage.noNewEmail") }}
                                </span>
                            </div>
                        </div>
                    </div>

                    <!--L'utilisateur a des nouveaux mails-->
                    <div
                        v-else
                        class="flex-1 bg-white bg-opacity-100 ring-1 shadow-sm ring-black ring-opacity-5 overflow-y-auto custom-scrollbar"
                        ref="scrollableDiv"
                    >
                        <ul role="list" class="flex mx-2 flex-col w-auto h-full rounded-xl">
                            <div class="pt-6">
                                <li
                                    v-if="
                                        emails[selectedTopic] &&
                                        emails[selectedTopic][IMPORTANT] &&
                                        countEmailsInCategoryAndPriority(selectedTopic, IMPORTANT) > 0
                                    "
                                    class=""
                                >
                                    <ImportantEmails />
                                </li>
                                <li
                                    v-if="
                                        emails[selectedTopic] &&
                                        emails[selectedTopic][INFORMATIVE] &&
                                        countEmailsInCategoryAndPriority(selectedTopic, INFORMATIVE) > 0
                                    "
                                    class=""
                                >
                                    <InformativeEmails />
                                </li>
                                <div
                                    v-if="
                                        emails[selectedTopic] &&
                                        emails[selectedTopic][USELESS] &&
                                        countEmailsInCategoryAndPriority(selectedTopic, USELESS) > 0
                                    "
                                    class="group/main"
                                >
                                    <UselessEmails />
                                </div>

                                <!-- read emails should be sorted by date, importance not in a separate section-->
                                <!--
                                <div v-if="readEmailsInSelectedTopic().length > 0" class="group/main">
                                    <li class="">
                                        <div class="px-6 pb-6">
                                            <div class="bg-stone-200 bg-opacity-90 rounded-md">
                                                <div class="flex px-2 py-2">
                                                    <p
                                                        class="flex-1 text-sm font-semibold leading-6 text-stone-600 px-4"
                                                    >
                                                        Lu
                                                    </p>

                                                    <div class="ml-auto">
                                                        <CheckIcon class="w-6 h-6 text-stone-500" />
                                                    </div>
                                                </div>
                                            </div>

                                            <div class="flex px-4 pt-4">
                                                <div class="flex">
                                                    <span
                                                        class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-stone-400"
                                                    >
                                                        <svg
                                                            xmlns="http://www.w3.org/2000/svg"
                                                            fill="none"
                                                            viewBox="0 0 24 24"
                                                            stroke-width="1.5"
                                                            stroke="currentColor"
                                                            class="w-6 h-6 text-white"
                                                        >
                                                            <path
                                                                stroke-linecap="round"
                                                                stroke-linejoin="round"
                                                                d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z"
                                                            />
                                                        </svg>
                                                    </span>
                                                </div>

                                                <div class="ml-6 w-full">
                                                    <div
                                                        class="overflow-hidden border-l-4 group-hover/main:rounded-l-xl border-stone-400 w-full"
                                                        style="overflow: visible"
                                                    >
                                                        <ul
                                                            role="list"
                                                            class="divide-y divide-gray-200 dark:divide-white w-full"
                                                        >
                                                            <li
                                                                class="px-6 py-5 hover:bg-opacity-70 dark:hover:bg-opacity-100 w-full"
                                                            >
                                                                <div class="flex group gap-x-2">
                                                                    <p
                                                                        @click="toggleReadEmailVisibility"
                                                                        class="cursor-pointer"
                                                                    >
                                                                        {{ $t("homePage.youReadRecently") }}
                                                                        <span
                                                                            class="font-semibold text-gray-900 dark:text-white hover:text-gray-700"
                                                                        >
                                                                            {{ readEmailsInSelectedTopic().length }}
                                                                        </span>
                                                                        <span
                                                                            v-if="
                                                                                readEmailsInSelectedTopic().length === 1
                                                                            "
                                                                        >
                                                                            {{ $t("homePage.email") }}
                                                                        </span>
                                                                        <span v-else>{{ $t("homePage.emails") }}</span>
                                                                        {{ $t("homePage.iAm") }}
                                                                        <span class="font-medium">
                                                                            {{
                                                                                $t("homePage.goingToCleanAutomatically")
                                                                            }}
                                                                        </span>
                                                                        {{ $t("homePage.theEmailsYouHaveRead") }}
                                                                    </p>

                                                                    <div
                                                                        class="hidden group-hover/main:block px-2 py-0.5 bg-stone-400 text-white text-sm shadow rounded-xl"
                                                                    >
                                                                        <div class="flex gap-x-1 items-center">
                                                                            <svg
                                                                                xmlns="http://www.w3.org/2000/svg"
                                                                                fill="none"
                                                                                viewBox="0 0 24 24"
                                                                                stroke-width="1.5"
                                                                                stroke="currentColor"
                                                                                class="w-4 h-4"
                                                                            >
                                                                                <path
                                                                                    stroke-linecap="round"
                                                                                    stroke-linejoin="round"
                                                                                    d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5"
                                                                                />
                                                                            </svg>
                                                                            <p
                                                                                @click="toggleReadEmailVisibility"
                                                                                class="cursor-pointer"
                                                                            >
                                                                                {{ $t("homePage.clickToSeeTheEmail") }}
                                                                            </p>
                                                                        </div>
                                                                    </div>
                                                                </div>

                                                                <ul
                                                                    v-if="showEmailReadDescriptions"
                                                                    class="text-gray-900 text-sm/6 pl-8 divide-y divide-gray-300 w-full"
                                                                >
                                                                    <li
                                                                        class="py-5 grid grid-cols-10 w-full"
                                                                        v-for="item in readEmailsInSelectedTopic()"
                                                                        :key="item.id"
                                                                        @mouseover="setHoveredItem(item.id)"
                                                                        @mouseleave="clearHoveredItem"
                                                                    >
                                                                        <div
                                                                            class="col-span-8 cursor-pointer"
                                                                            @click="toggleHiddenParagraph(item.id)"
                                                                        >
                                                                            <div class="flex-auto group">
                                                                                <div class="flex gap-x-4">
                                                                                    <div class="flex items-center">
                                                                                        <p
                                                                                            class="text-sm font-semibold leading-6 text-stone-700 mr-2"
                                                                                        >
                                                                                            {{ item.name }}
                                                                                        </p>
                                                                                        <p
                                                                                            class="text-sm leading-6 text-stone-700 mr-2"
                                                                                        >
                                                                                            {{ item.time }}
                                                                                        </p>
                                                                                        <p
                                                                                            class="text-xs leading-6 text-stone-700"
                                                                                        >
                                                                                            {{ item.date }}
                                                                                        </p>
                                                                                    </div>
                                                                                    <div
                                                                                        class="hidden group-hover:block px-2 py-0.5 bg-stone-400 text-white text-sm shadow rounded-xl"
                                                                                    >
                                                                                        <div
                                                                                            class="flex gap-x-1 items-center"
                                                                                        >
                                                                                            <svg
                                                                                                xmlns="http://www.w3.org/2000/svg"
                                                                                                fill="none"
                                                                                                viewBox="0 0 24 24"
                                                                                                stroke-width="1.5"
                                                                                                stroke="currentColor"
                                                                                                class="w-4 h-4"
                                                                                            >
                                                                                                <path
                                                                                                    stroke-linecap="round"
                                                                                                    stroke-linejoin="round"
                                                                                                    d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5"
                                                                                                />
                                                                                            </svg>
                                                                                            <p>
                                                                                                {{
                                                                                                    $t(
                                                                                                        "constants.userActions.clickToSeeTheSummary"
                                                                                                    )
                                                                                                }}
                                                                                            </p>
                                                                                        </div>
                                                                                    </div>
                                                                                </div>
                                                                                <p
                                                                                    class="mt-1 text-md text-gray-700 leading-relaxed"
                                                                                >
                                                                                    {{ item.description }}
                                                                                </p>
                                                                            </div>
                                                                            <ul
                                                                                v-show="showHiddenParagraphs[item.id]"
                                                                                role="list"
                                                                                class="text-black text-sm/6 pt-2"
                                                                                :ref="(el) => setParentRef(el, item.id)"
                                                                            >
                                                                                <li
                                                                                    v-for="detail in item.details"
                                                                                    :key="detail.id"
                                                                                    class="pl-8"
                                                                                    :ref="'hiddenText' + item.id"
                                                                                    :data-text="detail.text"
                                                                                ></li>
                                                                            </ul>
                                                                        </div>

                                                                        <div class="col-span-2 pt-2">
                                                                            <div class="flex justify-center">
                                                                                <span
                                                                                    class="isolate inline-flex rounded-2xl"
                                                                                >
                                                                                    <div
                                                                                        v-show="
                                                                                            hoveredItemId === item.id
                                                                                        "
                                                                                        class="group action-buttons"
                                                                                    >
                                                                                        <div class="relative group">
                                                                                            <div
                                                                                                class="absolute hidden group-hover:block bg-black text-white text-sm py-2 px-4 rounded shadow-lg mt-[-45px] -ml-4"
                                                                                            >
                                                                                                {{
                                                                                                    $t(
                                                                                                        "constants.userActions.open"
                                                                                                    )
                                                                                                }}
                                                                                            </div>
                                                                                            <button
                                                                                                @click.stop="
                                                                                                    openSeeModal(item)
                                                                                                "
                                                                                                type="button"
                                                                                                class="inline-flex items-center px-2 py-1.5 rounded-l-2xl text-stone-400 ring-1 ring-inset ring-stone-400 hover:bg-stone-400 focus:z-10"
                                                                                            >
                                                                                                <eye-icon
                                                                                                    class="w-5 h-5 text-stone-500 group-hover:text-white"
                                                                                                />
                                                                                            </button>
                                                                                        </div>
                                                                                    </div>
                                                                                    <div
                                                                                        v-show="
                                                                                            hoveredItemId === item.id
                                                                                        "
                                                                                        class="group action-buttons"
                                                                                    >
                                                                                        <div class="relative group">
                                                                                            <div
                                                                                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-25 w-[80px]"
                                                                                            >
                                                                                                {{
                                                                                                    $t(
                                                                                                        "homePage.unread"
                                                                                                    )
                                                                                                }}
                                                                                            </div>
                                                                                            <button
                                                                                                @click="
                                                                                                    markEmailAsUnread(
                                                                                                        item.id
                                                                                                    )
                                                                                                "
                                                                                                type="button"
                                                                                                class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-stone-400 hover:bg-stone-400 focus:z-10"
                                                                                            >
                                                                                                <check-icon
                                                                                                    class="w-5 h-5 text-stone-500 group-hover:text-white"
                                                                                                />
                                                                                            </button>
                                                                                        </div>
                                                                                    </div>
                                                                                    <div
                                                                                        v-show="
                                                                                            hoveredItemId === item.id
                                                                                        "
                                                                                        class="group action-buttons"
                                                                                    >
                                                                                        <div class="relative group">
                                                                                            <div
                                                                                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-6"
                                                                                            >
                                                                                                {{
                                                                                                    $t(
                                                                                                        "constants.userActions.archive"
                                                                                                    )
                                                                                                }}
                                                                                            </div>
                                                                                            <button
                                                                                                type="button"
                                                                                                class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-stone-400 hover:bg-stone-400 focus:z-10"
                                                                                            >
                                                                                                <TrashIcon
                                                                                                    @click.stop="
                                                                                                        deleteEmail(
                                                                                                            item.id
                                                                                                        )
                                                                                                    "
                                                                                                    class="w-5 h-5 text-stone-500 group-hover:text-white"
                                                                                                />
                                                                                            </button>
                                                                                        </div>
                                                                                    </div>
                                                                                    <div
                                                                                        v-show="
                                                                                            hoveredItemId === item.id
                                                                                        "
                                                                                        class="group action-buttons"
                                                                                    >
                                                                                        <div class="relative group">
                                                                                            <div
                                                                                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7"
                                                                                            >
                                                                                                {{
                                                                                                    $t(
                                                                                                        "homePage.answer"
                                                                                                    )
                                                                                                }}
                                                                                            </div>
                                                                                            <button
                                                                                                @click.stop="
                                                                                                    openAnswer(item)
                                                                                                "
                                                                                                type="button"
                                                                                                class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-stone-400 hover:bg-stone-400 focus:z-10"
                                                                                            >
                                                                                                <arrow-uturn-left-icon
                                                                                                    class="w-5 h-5 text-stone-500 group-hover:text-white"
                                                                                                />
                                                                                            </button>
                                                                                        </div>
                                                                                    </div>
                                                                                    <div
                                                                                        v-show="
                                                                                            hoveredItemId === item.id
                                                                                        "
                                                                                        class="group action-buttons"
                                                                                    >
                                                                                        <div
                                                                                            class="cursor-pointer relative group"
                                                                                        >
                                                                                            <div
                                                                                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-[125px] w-[185px]"
                                                                                            >
                                                                                                {{
                                                                                                    $t(
                                                                                                        "constants.additionalActions"
                                                                                                    )
                                                                                                }}
                                                                                            </div>
                                                                                            <Menu
                                                                                                as="div"
                                                                                                class="relative inline-block text-left"
                                                                                            >
                                                                                                <div>
                                                                                                    <MenuButton
                                                                                                        @click="
                                                                                                            toggleTooltip
                                                                                                        "
                                                                                                        class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-stone-500 ring-1 ring-inset ring-stone-400 hover:bg-stone-400 focus:z-10"
                                                                                                    >
                                                                                                        <ellipsis-horizontal-icon
                                                                                                            class="w-5 h-5 group-hover:text-white text-stone-500 group-active:text-stone-500 group-focus:text-red focus:text-stone-500"
                                                                                                        />
                                                                                                    </MenuButton>
                                                                                                </div>
                                                                                                 <transition
                                                                                                    enter-active-class="transition ease-out duration-100"
                                                                                                    enter-from-class="transform opacity-0 scale-95"
                                                                                                    enter-to-class="transform opacity-100 scale-100"
                                                                                                    leave-active-class="transition ease-in duration-75"
                                                                                                    leave-from-class="transform opacity-100 scale-100"
                                                                                                    leave-to-class="transform opacity-0 scale-95"
                                                                                                >
                                                                                                    <MenuItems
                                                                                                        v-show="
                                                                                                            isMenuOpen
                                                                                                        "
                                                                                                        class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none"
                                                                                                    >
                                                                                                        <div
                                                                                                            class="py-1"
                                                                                                        >
                                                                                                            <div
                                                                                                                v-if="
                                                                                                                    item.rule
                                                                                                                "
                                                                                                            >
                                                                                                                <MenuItem
                                                                                                                    v-slot="{
                                                                                                                        active,
                                                                                                                    }"
                                                                                                                >
                                                                                                                    <a
                                                                                                                        @click.prevent="
                                                                                                                            openRuleEditor(
                                                                                                                                item.rule_id
                                                                                                                            )
                                                                                                                        "
                                                                                                                        :class="[
                                                                                                                            active
                                                                                                                                ? 'bg-gray-100 text-gray-900'
                                                                                                                                : 'text-gray-700',
                                                                                                                            'block px-4 py-1 text-sm',
                                                                                                                        ]"
                                                                                                                    >
                                                                                                                        <span
                                                                                                                            class="flex gap-x-2 items-center"
                                                                                                                        >
                                                                                                                            <svg
                                                                                                                                xmlns="http://www.w3.org/2000/svg"
                                                                                                                                fill="none"
                                                                                                                                viewBox="0 0 24 24"
                                                                                                                                stroke-width="1.5"
                                                                                                                                stroke="currentColor"
                                                                                                                                class="w-4 h-4"
                                                                                                                            >
                                                                                                                                <path
                                                                                                                                    stroke-linecap="round"
                                                                                                                                    stroke-linejoin="round"
                                                                                                                                    d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
                                                                                                                                />
                                                                                                                            </svg>
                                                                                                                            <span>
                                                                                                                                {{
                                                                                                                                    $t(
                                                                                                                                        "constants.userAction.changeTheRule"
                                                                                                                                    )
                                                                                                                                }}
                                                                                                                            </span>
                                                                                                                        </span>
                                                                                                                    </a>
                                                                                                                </MenuItem>
                                                                                                            </div>
                                                                                                            <div v-else>
                                                                                                                <MenuItem
                                                                                                                    v-slot="{
                                                                                                                        active,
                                                                                                                    }"
                                                                                                                >
                                                                                                                    <a
                                                                                                                        @click.prevent="
                                                                                                                            openNewRule(
                                                                                                                                item.name,
                                                                                                                                item.email
                                                                                                                            )
                                                                                                                        "
                                                                                                                        :class="[
                                                                                                                            active
                                                                                                                                ? 'bg-gray-100 text-gray-900'
                                                                                                                                : 'text-gray-700',
                                                                                                                            'block px-4 py-1 text-sm',
                                                                                                                        ]"
                                                                                                                    >
                                                                                                                        <span
                                                                                                                            class="flex gap-x-2 items-center"
                                                                                                                        >
                                                                                                                            <svg
                                                                                                                                xmlns="http://www.w3.org/2000/svg"
                                                                                                                                fill="none"
                                                                                                                                viewBox="0 0 24 24"
                                                                                                                                stroke-width="1.5"
                                                                                                                                stroke="currentColor"
                                                                                                                                class="w-4 h-4"
                                                                                                                            >
                                                                                                                                <path
                                                                                                                                    stroke-linecap="round"
                                                                                                                                    stroke-linejoin="round"
                                                                                                                                    d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
                                                                                                                                />
                                                                                                                            </svg>
                                                                                                                            <span>
                                                                                                                                {{
                                                                                                                                    $t(
                                                                                                                                        "constants.userActions.createARule"
                                                                                                                                    )
                                                                                                                                }}
                                                                                                                            </span>
                                                                                                                        </span>
                                                                                                                    </a>
                                                                                                                </MenuItem>
                                                                                                            </div>
                                                                                                        </div>
                                                                                                        <div
                                                                                                            class="py-1"
                                                                                                        >
                                                                                                            <MenuItem
                                                                                                                v-slot="{
                                                                                                                    active,
                                                                                                                }"
                                                                                                            >
                                                                                                                <a
                                                                                                                    @click.prevent="
                                                                                                                        markEmailReplyLater(
                                                                                                                            item
                                                                                                                        )
                                                                                                                    "
                                                                                                                    :class="[
                                                                                                                        active
                                                                                                                            ? 'bg-gray-100 text-gray-900'
                                                                                                                            : 'text-gray-700',
                                                                                                                        'block px-4 py-1 text-sm',
                                                                                                                    ]"
                                                                                                                >
                                                                                                                    <span
                                                                                                                        class="flex gap-x-2 items-center"
                                                                                                                    >
                                                                                                                        <svg
                                                                                                                            class="w-4 h-4"
                                                                                                                            viewBox="0 0 28 28"
                                                                                                                            version="1.1"
                                                                                                                            stroke="currentColor"
                                                                                                                            xmlns="http://www.w3.org/2000/svg"
                                                                                                                            xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                                                                            xml:space="preserve"
                                                                                                                            xmlns:serif="http://www.serif.com/"
                                                                                                                            style="
                                                                                                                                fill-rule: evenodd;
                                                                                                                                clip-rule: evenodd;
                                                                                                                                stroke-linecap: round;
                                                                                                                                stroke-linejoin: round;
                                                                                                                            "
                                                                                                                        >
                                                                                                                            <path
                                                                                                                                d="M13.435,17.391l-6.783,-6.782m0,0l6.783,-6.783m-6.783,6.783l13.565,0c3.721,0 6.783,3.061 6.783,6.782c0,3.721 -3.062,6.783 -6.783,6.783l-3.391,0"
                                                                                                                                style="
                                                                                                                                    fill: none;
                                                                                                                                    stroke: #000;
                                                                                                                                    stroke-width: 1.7px;
                                                                                                                                "
                                                                                                                            />
                                                                                                                            <path
                                                                                                                                d="M7.783,17.391l-6.783,-6.782m0,0l6.783,-6.783"
                                                                                                                                style="
                                                                                                                                    fill: none;
                                                                                                                                    stroke: #000;
                                                                                                                                    stroke-width: 1.7px;
                                                                                                                                "
                                                                                                                            />
                                                                                                                        </svg>
                                                                                                                        <span>
                                                                                                                            {{
                                                                                                                                $t(
                                                                                                                                    "constants.userActions.replyLater"
                                                                                                                                )
                                                                                                                            }}
                                                                                                                        </span>
                                                                                                                    </span>
                                                                                                                </a>
                                                                                                            </MenuItem>
                                                                                                        </div>
                                                                                                        <div
                                                                                                            class="py-1"
                                                                                                        >
                                                                                                            <MenuItem
                                                                                                                v-slot="{
                                                                                                                    active,
                                                                                                                }"
                                                                                                            >
                                                                                                                <a
                                                                                                                    @click.prevent="
                                                                                                                        transferEmail(
                                                                                                                            item
                                                                                                                        )
                                                                                                                    "
                                                                                                                    :class="[
                                                                                                                        active
                                                                                                                            ? 'bg-gray-100 text-gray-900'
                                                                                                                            : 'text-gray-700',
                                                                                                                        'block px-4 py-1 text-sm',
                                                                                                                    ]"
                                                                                                                >
                                                                                                                    <span
                                                                                                                        class="flex gap-x-2 items-center"
                                                                                                                    >
                                                                                                                        <svg
                                                                                                                            class="w-4 h-4"
                                                                                                                            viewBox="0 0 28 28"
                                                                                                                            version="1.1"
                                                                                                                            stroke="currentColor"
                                                                                                                            xmlns="http://www.w3.org/2000/svg"
                                                                                                                            xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                                                                            xml:space="preserve"
                                                                                                                            xmlns:serif="http://www.serif.com/"
                                                                                                                            style="
                                                                                                                                fill-rule: evenodd;
                                                                                                                                clip-rule: evenodd;
                                                                                                                                stroke-linecap: round;
                                                                                                                                stroke-linejoin: round;
                                                                                                                            "
                                                                                                                        >
                                                                                                                            <path
                                                                                                                                d="M13.435,10.609l6.783,6.782m0,0l-6.783,6.783m6.783-6.783L6.85,17.391c-3.721,0-6.783-3.061-6.783-6.782c0-3.721,3.062-6.783,6.783-6.783l3.391,0"
                                                                                                                                style="
                                                                                                                                    fill: none;
                                                                                                                                    stroke: #000;
                                                                                                                                    stroke-width: 1.7px;
                                                                                                                                "
                                                                                                                            />
                                                                                                                            <path
                                                                                                                                d="M21.197,10.609l6.783,6.782m0,0l-6.783,6.783"
                                                                                                                                style="
                                                                                                                                    fill: none;
                                                                                                                                    stroke: #000;
                                                                                                                                    stroke-width: 1.7px;
                                                                                                                                "
                                                                                                                            />
                                                                                                                        </svg>
                                                                                                                        <span>
                                                                                                                            {{
                                                                                                                                $t(
                                                                                                                                    "constants.userActions.transfer"
                                                                                                                                )
                                                                                                                            }}
                                                                                                                        </span>
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
                            -->
                            </div>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="bg-gray-50 ring-1 shadow-sm ring-black ring-opacity-5 h-full flex flex-col relative">
                <div v-show="!isHidden" class="w-[325px] 2xl:w-[525px] flex-grow">
                    <div class="flex flex-col h-full">
                        <div class="flex-grow">
                            <div class="flex p-5">
                                <div class="mr-4 flex-shrink-0 self-center">
                                    <span
                                        class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke-width="1.5"
                                            stroke="currentColor"
                                            class="w-6 h-6"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z"
                                            />
                                        </svg>
                                    </span>
                                </div>
                                <div>
                                    <p class="mt-1" id="animated-text" ref="animatedText"></p>
                                </div>
                            </div>
                        </div>
                        <div class="flex flex-col justify-end h-[160px] border-t">
                            <textarea
                                id="dynamicTextarea"
                                @keydown.enter="handleEnterKey"
                                @input="adjustHeight"
                                v-model="textareaValue"
                                class="overflow-y-hidden flex flex-1 pt-3 pl-5 w-full border-transparent bg-transparent text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 focus:border-transparent focus:bg-transparent focus:ring-0"
                                :placeholder="$t('constants.instruction')"
                            ></textarea>
                            <div class="flex justify-end m-3">
                                <button
                                    type="button"
                                    class="w-[80px] rounded bg-gray-700 px-2.5 py-1.5 text-sm text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                                >
                                    {{ $t("constants.userActions.send") }}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
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
    <SeeMailModal
        :isOpen="isModalSeeOpen"
        :email="selectedEmail"
        @closeSeeModal="closeSeeModal"
        @openAnswer="openAnswer"
        @openRuleEditor="openRuleEditor"
        @openNewRule="openNewRule"
        @markEmailAsRead="markEmailAsRead"
        @markEmailReplyLater="markEmailReplyLater"
        @transferEmail="transferEmail"
    />
</template>

<script setup lang="ts">
/* eslint-disable */
import { ref, nextTick, onMounted } from "vue";
import { useRouter } from "vue-router";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import NavBarLarge from "@/global/components/NavBarLarge.vue";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
// import SearchbarV2 from "../components/SearchbarV2.vue"
import SeeMailModal from "./components/SeeMailModal.vue";
import NewCategoryModal from "./components/NewCategoryModal.vue";
import UpdateCategoryModal from "./components/UpdateCategoryModal.vue";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import {
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
} from "@heroicons/vue/24/outline";
import { API_BASE_URL, USELESS, INFORMATIVE, IMPORTANT } from "@/global/const";
import { getData, postData } from "@/global/fetchData";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { Category } from "@/global/types";
import InformativeEmails from "./components/InformativeEmails.vue";
import ImportantEmails from "./components/ImportantEmails.vue";

interface Email {
    id: number;
    answerLater: boolean;
    read: boolean;
    date: string;
    time: string;

    id_provider: string;
    email: any;
    details: any;
}

const showNotification = ref<boolean>(false);
const notificationTitle = ref<string>("");
const notificationMessage = ref<string>("");
const backgroundColor = ref<string>("");
const timerId = ref<number | null>(null);

const router = useRouter();
const animatedText = ref<HTMLElement | null>(null);
const showHiddenParagraphs = ref<Record<string, boolean>>({});
const isModalOpen = ref(false);
const isModalSeeOpen = ref(false);
const isModalUpdateOpen = ref(false);
const modalErrorMessage = ref("");
const modalUpdateErrorMessage = ref("");
const categoryToUpdate = ref<Category | null>(null);
const categories = ref<Category[]>([]);
const selectedEmail = ref<Email | null>(null);
const hoveredItemId = ref<number | null>(null);
const oldCategoryName = ref("");
const showEmailDescriptions = ref(false);
const showEmailReadDescriptions = ref(false);
const isMenuOpen = ref(true);
const emails = ref<Record<string, any>>({});
const scrollableDiv = ref<HTMLElement | null>(null);
const selectedTopic = ref("");
const animationTriggered = ref([false, false, false]);
const searchQuery = ref("");

const parentElementRefs = ref<Record<string, HTMLElement>>({});
const totalUnread = ref(0);
const initialAnimationDone = ref(false);
const isModalWarningCategoryOpen = ref(false);
const nbRulesAssociated = ref<number>(0);
const lockEmailsAccess = ref(false);

const isHidden = ref(false);

function displayPopup(type: "success" | "error", title: string, message: string) {
    if (type === "error") {
        displayErrorPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    } else {
        displaySuccessPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    }
    timerId.value = setTimeout(dismissPopup, 4000);
}

function dismissPopup() {
    showNotification.value = false;
    if (timerId.value !== null) {
        clearTimeout(timerId.value);
    }
}

const toggleVisibility = () => {
    isHidden.value = !isHidden.value;
};

const downloadAttachment = async (emailId: string, attachmentName: string) => {
    try {
        const response = await getData(`user/emails/${emailId}/attachments/${attachmentName}/`);

        if (response.success && response.data) {
            const attachmentData = await response.data.blob();

            const url = window.URL.createObjectURL(attachmentData);
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", attachmentName);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            throw new Error("Failed to download attachment");
        }
    } catch (error: unknown) {
        displayPopup("success", "Échec de téléchargement de la pièce jointe", (error as Error).message);
    }
};

function getIconComponent(fileName: string): typeof CameraIcon | typeof DocumentIcon {
    const extension = fileName.split(".").pop()?.toLowerCase() || "";

    if (["png", "jpg", "jpeg", "gif"].includes(extension)) {
        return CameraIcon;
    } else if (["pdf", "doc", "docx", "xls", "xlsx"].includes(extension)) {
        return DocumentIcon;
    } else {
        return DocumentIcon;
    }
}
onMounted(async () => {
    document.addEventListener("keydown", handleKeyDown);

    await new Promise<void>((resolve) => {
        fetchData().then(() => {
            resolve();
        });
    });

    setInterval(async () => {
        try {
            await fetchEmails();
        } catch (error) {
            console.log("An error occurred", error);
        }
    }, 15000);
});

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Escape" && isModalWarningCategoryOpen.value) {
        closeWarningCategoryModal();
    }
}

function getNumberUnreadMail(emailData: Record<string, any>): number {
    let totalUnread = 0;

    for (const category in emailData) {
        for (const subcategory in emailData[category]) {
            const emailsInSubcategory = emailData[category][subcategory];
            if (subcategory !== "Useless") {
                for (const email of emailsInSubcategory) {
                    if (!email.read && !email.answerLater) {
                        totalUnread++;
                    }
                }
            }
        }
    }
    return totalUnread;
}

function getTextNumberUnreadMail(totalUnread: number): string {
    if (totalUnread === 0) {
        return t("homePage.youDidNotReceiveNewEmail");
    } else if (totalUnread === 1) {
        return `${t("homePage.youReceived")} ${totalUnread} ${t("homePage.newEmail")}`;
    } else {
        return `${t("homePage.youReceived")} ${totalUnread} ${t("homePage.newEmails")}`;
    }
}

function animateText(text: string): void {
    try {
        const target = animatedText.value;

        if (target) {
            target.textContent = "";
            const characters = text.split("");
            let currentIndex = 0;

            const interval = setInterval(() => {
                if (currentIndex < characters.length) {
                    target.textContent += characters[currentIndex];
                    currentIndex++;
                } else {
                    clearInterval(interval);
                }
            }, 30);
        }
    } catch (error) {
        console.error("An error occurred during text animation:", error);
    }
}

function setParentRef(el: HTMLElement | null, itemId: string): void {
    if (el) {
        parentElementRefs.value[itemId] = el;
    }
}

function openRuleEditor(ruleId: string): void {
    if (ruleId) {
        router.push({ name: "rules", query: { idRule: ruleId, editRule: "true" } });
    }
}

function openNewRule(ruleName: string, ruleEmail: string): void {
    if (ruleName && ruleEmail) {
        router.push({ name: "rules", query: { ruleName, ruleEmail, editRule: "false" } });
    }
}

function setHoveredItem(id: number | null): void {
    hoveredItemId.value = id;
}

function clearHoveredItem(): void {
    hoveredItemId.value = null;
}

function toggleTooltip(): void {
    isMenuOpen.value = true;
}

async function markEmailAsUnread(emailId: number): Promise<void> {
    lockEmailsAccess.value = true;
    updateEmailStatus(emailId, false);

    const path = `user/emails/${emailId}/mark_unread/`;
    const response = await postData(path, {});

    if (response.success) {
        const data = response.data;

        if (data.read !== false) {
            displayPopup("error", t("homePage.markEmailUnreadFailure"), "Failed to mark email as unread.");
        }
    } else {
        displayPopup("error", t("homePage.markEmailUnreadFailure"), "Failed to communicate with the server.");
    }

    lockEmailsAccess.value = false;
}

async function markEmailAsRead(emailId: number): Promise<void> {
    lockEmailsAccess.value = true;
    updateEmailStatus(emailId, true);

    const path = `user/emails/${emailId}/mark_read/`;
    const response = await postData(path, {});

    if (response.success) {
        const data = response.data;

        if (data.read !== true) {
            displayPopup("error", t("homepage.markEmailReadFailure"), "Failed to mark email as read.");
        }
    } else {
        displayPopup("error", t("homepage.markEmailReadFailure"), "Failed to communicate with the server.");
    }

    lockEmailsAccess.value = false;
}

function updateEmailStatus(emailId: number, readStatus: boolean): void {
    for (const category in emails.value) {
        if (Object.prototype.hasOwnProperty.call(emails.value, category)) {
            for (const subcategory in emails.value[category]) {
                if (Array.isArray(emails.value[category][subcategory])) {
                    const emailIndex = emails.value[category][subcategory].findIndex(
                        (email: Email) => email.id === emailId
                    );
                    if (emailIndex !== -1) {
                        emails.value[category][subcategory][emailIndex].read = readStatus;
                        updateNumberUnreadEmails();
                        return;
                    }
                }
            }
        }
    }
}

function updateNumberUnreadEmails(): void {
    const newTotalUnread = getNumberUnreadMail(emails.value);

    if (!initialAnimationDone.value) {
        animateText(getTextNumberUnreadMail(newTotalUnread));
        totalUnread.value = newTotalUnread;
        initialAnimationDone.value = true;
    } else if (newTotalUnread !== totalUnread.value) {
        totalUnread.value = newTotalUnread;

        if (totalUnread.value > 0 && totalUnread.value <= 2) {
            animateText(getTextNumberUnreadMail(totalUnread.value));
        } else {
            if (animatedText.value) {
                animatedText.value.textContent = getTextNumberUnreadMail(totalUnread.value);
            }
        }
    }
}

async function transferEmail(email: Email): Promise<void> {
    try {
        const response = await getData(`api/get_mail_by_id?email_id=${email.id_provider}`);
        if (response.success && response.data) {
            const data = response.data;
            sessionStorage.setItem("subject", JSON.stringify(data.subject));
            sessionStorage.setItem("cc", data.cc);
            sessionStorage.setItem("bcc", data.bcc);
            sessionStorage.setItem("decoded_data", JSON.stringify(data.decoded_data));
            sessionStorage.setItem("email", JSON.stringify(email.email));
            sessionStorage.setItem("id_provider", JSON.stringify(email.id_provider));
            sessionStorage.setItem("details", JSON.stringify(email.details));
            sessionStorage.setItem("emailReceiver", data.email_receiver);
            sessionStorage.setItem("date", JSON.stringify(data.date));

            router.push({ name: "transfer" });
        } else {
            displayPopup("error", t("homepage.transferEmailFailure"), "Failed to transfer email.");
        }
    } catch (error: any) {
        displayPopup("error", t("homepage.transferEmailFailure"), error.message);
    }
}

async function markEmailReplyLater(email: Email): Promise<void> {
    lockEmailsAccess.value = true;
    email.answerLater = true;
    isMenuOpen.value = false;

    try {
        const response = await postData(`user/emails/${email.id}/mark_reply-later/`, {});
        if (!response.success) {
            displayPopup("error", t("homepage.markEmailReplyLaterFailure"), "Failed to mark email for reply later.");
        }
    } catch (error: any) {
        displayPopup("error", t("homepage.markEmailReplyLaterFailure"), error.message);
    } finally {
        lockEmailsAccess.value = false;
    }
}

function deleteEmailFromState(emailId: number): void {
    for (const category in emails.value) {
        if (Object.prototype.hasOwnProperty.call(emails.value, category)) {
            for (const subcategory in emails.value[category]) {
                if (Array.isArray(emails.value[category][subcategory])) {
                    const emailIndex = emails.value[category][subcategory].findIndex(
                        (email: Email) => email.id === emailId
                    );
                    if (emailIndex !== -1) {
                        emails.value[category][subcategory].splice(emailIndex, 1);
                        return;
                    }
                }
            }
        }
    }
}

async function setRuleBlockForSender(email: Email) {
    lockEmailsAccess.value = true;
    const emailId = email.id;

    try {
        const response = await postData(`user/emails/${emailId}/block_sender/`, {});
        if (response.success && response.data.block) {
            await deleteEmail(emailId);
        } else {
            displayPopup("error", t("homepage.blockEmailAddressFailure"), response.data);
        }
    } catch (error: any) {
        displayPopup("error", t("homepage.blockEmailAddressFailure"), error.message);
    } finally {
        lockEmailsAccess.value = false;
    }
}

async function deleteEmail(emailId: number) {
    lockEmailsAccess.value = true;
    deleteEmailFromState(emailId);

    try {
        const response = await postData(`user/emails/${emailId}/delete/`, {});
        if (!response.success) {
            displayPopup("error", t("constants.popUpConstants.deleteEmailFailure"), response.data?.error);
        }
    } catch (error: any) {
        displayPopup("error", t("constants.popUpConstants.deleteEmailFailure"), error.message);
    } finally {
        lockEmailsAccess.value = false;
    }
}

async function openAnswer(email: Email) {
    try {
        const response = await getData(`api/get_mail_by_id?email_id=${email.id_provider}`);
        if (response.success) {
            const data = response.data;
            sessionStorage.setItem("subject", JSON.stringify(data.email.subject));
            sessionStorage.setItem("cc", data.email.cc);
            sessionStorage.setItem("bcc", data.email.bcc);
            sessionStorage.setItem("decodedData", JSON.stringify(data.email.decoded_data));
            sessionStorage.setItem("email", JSON.stringify(email.email));
            sessionStorage.setItem("idProvider", JSON.stringify(email.id_provider));
            sessionStorage.setItem("details", JSON.stringify(email.details));
            sessionStorage.setItem("emailReceiver", data.email.email_receiver);

            router.push({ name: "answer" });
        } else {
            displayPopup("error", t("constants.popUpConstants.openReplyPageFailure"), "Failed to retrieve email data");
        }
    } catch (error: any) {
        displayPopup("error", t("constants.popUpConstants.openReplyPageFailure"), error.message);
    }
}

function openSeeModal(emailItem: Email): void {
    selectedEmail.value = emailItem;
    isModalSeeOpen.value = true;
}

function closeSeeModal(): void {
    isModalSeeOpen.value = false;
}

function openModal(): void {
    isModalOpen.value = true;
}

function closeModal(): void {
    isModalOpen.value = false;
}

function openUpdateModal(category: Category): void {
    oldCategoryName.value = category.name;
    categoryToUpdate.value = category;
    isModalUpdateOpen.value = true;
}

function closeUpdateModal(): void {
    isModalUpdateOpen.value = false;
}

function openWarningCategoryModal(nbRules: number): void {
    isModalWarningCategoryOpen.value = true;
    nbRulesAssociated.value = nbRules;
}

function closeWarningCategoryModal(): void {
    isModalWarningCategoryOpen.value = false;
}

async function handleAddCategory(
    categoryData: { name: string; description: string } & Partial<{ error: string; description: string }>
) {
    if (categoryData.error) {
        displayPopup("error", categoryData.error, categoryData.description || "Error occurred");
        closeModal();
        return;
    }

    try {
        const response = await postData("api/create_category/", categoryData);
        if (!response.success || "error" in response.data) {
            displayPopup(
                "error",
                t("constants.popUpConstants.addCategoryError"),
                response.data?.error || "Unknown error"
            );
            closeModal();
        } else {
            displayPopup(
                "success",
                t("constants.popUpConstants.successMessages.success"),
                t("constants.popUpConstants.successMessages.categoryAddedSuccess")
            );
            closeModal();

            const fetchedCategories = await getData("user/categories/");
            if (fetchedCategories.success) {
                categories.value = fetchedCategories.data.map((category: { name: string; description: string }) => ({
                    name: category.name,
                    description: category.description,
                }));
            }
        }
    } catch (error) {
        displayPopup("error", t("constants.popUpConstants.errorMessages.addCategoryError"), (error as Error).message);
        closeModal();
    }
}

async function handleUpdateCategory(
    updatedCategory: { name: string; description: string } & Partial<{ error: string; description: string }>
) {
    if (updatedCategory.error) {
        displayPopup("error", updatedCategory.error, updatedCategory.description || "Error occurred");
        closeUpdateModal();
        return;
    }

    if (!updatedCategory.name.trim()) {
        displayPopup(
            "error",
            t("constants.popUpConstants.errorMessages.updateCategoryError"),
            t("constants.popUpConstants.errorMessages.emptyCategoryNameError")
        );
        closeUpdateModal();
        return;
    }

    const updateData = {
        name: updatedCategory.name,
        description: updatedCategory.description,
        categoryName: oldCategoryName.value,
    };

    try {
        const response = await postData("api/update_category/", updateData);
        if (response.success) {
            displayPopup(
                "success",
                t("constants.popUpConstants.successMessages.success"),
                t("constants.popUpConstants.successMessages.updateCategorySuccess")
            );
            closeUpdateModal();

            const fetchedCategories = await getData("user/categories/");
            if (fetchedCategories.success) {
                categories.value = fetchedCategories.data.map((category: { name: string; description: string }) => ({
                    name: category.name,
                    description: category.description,
                }));
            }
        }
    } catch (error: unknown) {
        displayPopup(
            "error",
            t("constants.popUpConstants.errorMessages.updateCategoryError"),
            (error as Error).message
        );
        closeUpdateModal();
    }
}

async function handleCategoryDelete(categoryNameToDelete: string) {
    if (!categoryNameToDelete.trim()) {
        displayPopup(
            "error",
            t("constants.popUpConstants.errorMessages.openTransferPageFailure"),
            t("constants.popUpConstants.errorMessages.emptyCategoryNameError")
        );
        return;
    }

    try {
        const response = await postData("api/get_rules_linked/", { categoryName: categoryNameToDelete });
        if (response.success && response.data.nb_rules > 0) {
            closeUpdateModal();
            openWarningCategoryModal(response.data.nb_rules);
        } else {
            await deleteCategory(categoryNameToDelete);
        }
    } catch (error: unknown) {
        displayPopup("error", t("constants.popUpConstants.errorMessages.recuperationRules"), (error as Error).message);
        closeUpdateModal();
    }
}

async function deleteCategory(categoryNameToDelete: string) {
    try {
        const response = await postData("api/delete_category/", { categoryName: categoryNameToDelete });
        if (response.success) {
            displayPopup(
                "success",
                t("constants.popUpConstants.successMessages.success"),
                t("constants.popUpConstants.successMessages.deleteCategorySuccess")
            );

            const categoryData = await getData("user/categories/");
            if (categoryData.success) {
                categories.value = categoryData.data.map((category: { name: string; description: string }) => ({
                    name: category.name,
                    description: category.description,
                }));
            }
        }
    } catch (error: unknown) {
        displayPopup(
            "error",
            t("constants.popUpConstants.errorMessages.deleteCategoryError"),
            (error as Error).message
        );
    }
    closeUpdateModal();
    closeWarningCategoryModal();
}

function readEmailsInSelectedTopic(): Email[] {
    return (Object.values(emails.value[selectedTopic.value] || {}) as Email[][])
        .flat()
        .filter((email): email is Email => !email.answerLater && email.read);
}

function toggleReadEmailVisibility(): void {
    showEmailReadDescriptions.value = !showEmailReadDescriptions.value;
    scrollToBottom();
}

function toggleEmailVisibility(): void {
    showEmailDescriptions.value = !showEmailDescriptions.value;
    readEmailsInSelectedTopic().length === 0 ? scrollToBottom() : scrollAlmostToBottom();
}

function scrollToBottom(): void {
    nextTick(() => {
        if (scrollableDiv.value) {
            scrollableDiv.value.scrollTop = scrollableDiv.value.scrollHeight;
        }
    });
}

function scrollAlmostToBottom(): void {
    nextTick(() => {
        if (scrollableDiv.value) {
            const offset = 100;
            scrollableDiv.value.scrollTop = scrollableDiv.value.scrollHeight - offset;
        }
    });
}

function toggleHiddenParagraph(index: number): void {
    showHiddenParagraphs.value[index] = !showHiddenParagraphs.value[index];
    nextTick(() => {
        if (showHiddenParagraphs.value[index] && !animationTriggered.value[index]) {
            const parentElement = parentElementRefs.value[index];
            if (parentElement) {
                const elements = Array.from(parentElement.children);
                let delay = 0;
                elements.forEach((element) => {
                    const duration = animateHiddenText(element as HTMLElement, delay);
                    delay += duration + 20;
                });
                animationTriggered.value[index] = true;
            }
        }
    });
}

function animateHiddenText(element: HTMLElement, delay = 0): number {
    const characters = element.dataset.text?.split("") || [];
    const duration = characters.length * 5;
    setTimeout(() => {
        element.textContent = "";
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

function selectCategory(category: { name: string }): void {
    selectedTopic.value = category.name;
    localStorage.setItem("selectedTopic", category.name);
}

function countEmailsInCategoryAndPriority(categoryName: string, priority: string): number {
    return (
        emails.value[categoryName]?.[priority]?.filter(
            (email: { read: any; answerLater: any }) =>
                "read" in email && "answerLater" in email && !email.read && !email.answerLater
        ).length || 0
    );
}

function isEmptyTopic(): boolean {
    return totalEmailsInCategory(selectedTopic.value) === 0;
}

function totalEmailsInCategory(categoryName: string): number {
    return (Object.values(emails.value[categoryName] || {}) as Email[][])
        .flat()
        .filter((email): email is Email => !("answerLater" in email) || !email.answerLater).length;
}

function totalEmailsInCategoryNotRead(categoryName: string): number {
    return (Object.values(emails.value[categoryName] || {}) as Email[][])
        .flat()
        .filter(
            (email): email is Email => "read" in email && "answerLater" in email && !email.read && !email.answerLater
        ).length;
}

function groupedEmailsByCategoryAndDate(category: string): Record<string, Email[]> {
    const emailsInCategory: Email[] = (emails.value[selectedTopic.value]?.[category] || []) as Email[];

    const grouped = emailsInCategory
        .filter((email: Email) => !email.read && !email.answerLater)
        .reduce((acc: Record<string, Email[]>, email: Email) => {
            if (!acc[email.date]) {
                acc[email.date] = [];
            }
            acc[email.date].push(email);
            return acc;
        }, {} as Record<string, Email[]>);

    return Object.entries(grouped)
        .sort(([dateA], [dateB]) => new Date(dateB).getTime() - new Date(dateA).getTime())
        .reduce((acc, [date, emailsForDate]) => {
            acc[date] = emailsForDate.sort(
                (a: Email, b: Email) =>
                    new Date(`1970/01/01 ${b.time}`).getTime() - new Date(`1970/01/01 ${a.time}`).getTime()
            );
            return acc;
        }, {} as Record<string, Email[]>);
}

async function fetchEmails(): Promise<void> {
    const response = await postData("user/emails/", {
        subject: "",
        resultPerPage: 25,
        category: "Others",
    });

    if (response.success && !lockEmailsAccess.value) {
        emails.value = response.data;
    }
    updateNumberUnreadEmails();
}

async function fetchData(): Promise<void> {
    try {
        const categoryResponse = await getData("user/categories/");

        if (categoryResponse.success) {
            categories.value = categoryResponse.data as Category[];
        }

        const storedTopic = localStorage.getItem("selectedTopic");

        if (storedTopic) {
            selectedTopic.value = storedTopic;
        } else if (categories.value.length > 0) {
            selectedTopic.value = categories.value[0].name;
        }

        await fetchEmails();
    } catch (error) {
        console.error("Failed to fetch data:", error);
    }
}

function updateSearchQuery(event: Event) {
    const target = event.target as HTMLInputElement;
    searchQuery.value = target.value;
}
</script>

<!-- 
TODO: 
- remove the commented lines AFTER coding the component EmailActionButtons.vue
- move the functions inside the right components
- use strictly camelCase nothing else
 -->
