<template>
    <li class="">
        <div class="px-6 pb-6">
            <div class="bg-gray-200 bg-opacity-90 rounded-md">
                <div class="flex px-2 py-2">
                    <p class="flex-1 text-sm font-semibold leading-6 text-gray-600">
                        {{ $t("constants.ruleModalConstants.useless") }}
                    </p>

                    <div class="ml-auto">
                        <trash-icon class="w-6 h-6 text-gray-500" />
                    </div>
                </div>
            </div>

            <div class="flex px-4 pt-4">
                <div class="flex">
                    <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-400">
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
                        class="overflow-hidden border-l-4 group-hover/main:rounded-l-xl border-gray-400 w-full"
                        style="overflow: visible"
                    >
                        <ul role="list" class="divide-y divide-gray-200 dark:divide-white w-full">
                            <li class="px-6 py-5 hover:bg-opacity-70 dark:hover:bg-opacity-100 w-full">
                                <div class="flex gap-x-2">
                                    <p @click="toggleEmailVisibility" class="cursor-pointer">
                                        {{ $t("homePage.youReceived") }}
                                        <span
                                            class="font-semibold text-gray-900 dark:text-white hover:text-gray-700 w-full"
                                        >
                                            {{ emails[selectedTopic]["Useless"].filter((e) => !e.answerLater).length }}
                                        </span>
                                        <span
                                            v-if="
                                                emails[selectedTopic][USELESS].filter((email) => !email.answerLater)
                                                    .length === 1
                                            "
                                        >
                                            {{ $t("homePage.uselessEmail") }}
                                        </span>
                                        <span v-else>
                                            {{ $t("homePage.uselessEmails") }}
                                        </span>
                                    </p>
                                    <div
                                        class="hidden group-hover/main:block px-2 py-0.5 bg-gray-400 text-white text-sm shadow rounded-xl"
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

                                            <p @click="toggleEmailVisibility" class="cursor-pointer">
                                                {{ $t("homePage.clickToSeeTheEmail") }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                <ul
                                    v-if="showEmailDescriptions"
                                    class="text-gray-900 text-sm/6 pl-8 divide-y divide-gray-200"
                                >
                                    <li
                                        class="py-5 grid grid-cols-10 w-full"
                                        v-for="item in emails[selectedTopic][USELESS].filter(
                                            (email) => !email.answerLater
                                        )"
                                        :key="item.id"
                                        @mouseover="setHoveredItem(item.id)"
                                        @mouseleave="clearHoveredItem"
                                    >
                                        <div class="col-span-8 flex-auto">
                                            <div class="flex items-baseline justify-between gap-x-4">
                                                <div class="flex items-center">
                                                    <p class="text-sm font-semibold leading-6 text-gray-800 mr-2">
                                                        {{ item.name }}
                                                    </p>
                                                    <p class="text-sm leading-6 text-gray-800 mr-2">
                                                        {{ item.time }}
                                                    </p>
                                                    <p class="text-xs leading-6 text-gray-800 mr-2">
                                                        {{ item.date }}
                                                    </p>
                                                </div>
                                            </div>
                                            <p>{{ item.description }}</p>
                                        </div>
                                        <div class="col-span-2 pt-2">
                                            <div class="flex justify-center">
                                                <span class="isolate inline-flex rounded-2xl">
                                                    <div
                                                        v-show="hoveredItemId === item.id"
                                                        class="group action-buttons"
                                                    >
                                                        <div class="relative group">
                                                            <div
                                                                class="absolute hidden group-hover:block bg-black text-white text-sm py-2 px-4 rounded shadow-lg mt-[-45px] -ml-4"
                                                            >
                                                                {{ $t("constants.userActions.open") }}
                                                            </div>
                                                            <button
                                                                @click.stop="openSeeModal(item)"
                                                                type="button"
                                                                class="inline-flex items-center px-2 py-1.5 rounded-l-2xl text-gray-400 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10"
                                                            >
                                                                <eye-icon
                                                                    class="w-5 h-5 text-gray-500 group-hover:text-white"
                                                                />
                                                            </button>
                                                        </div>
                                                    </div>
                                                    <div
                                                        v-show="hoveredItemId === item.id"
                                                        class="group action-buttons"
                                                    >
                                                        <div class="relative group">
                                                            <div
                                                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-6"
                                                            >
                                                                {{ $t("homePage.block") }}
                                                            </div>
                                                            <button
                                                                type="button"
                                                                class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10"
                                                            >
                                                                <HandRaisedIcon
                                                                    @click.stop="setRuleBlockForSender(item)"
                                                                    class="w-5 h-5 text-gray-500 group-hover:text-white"
                                                                />
                                                            </button>
                                                        </div>
                                                    </div>
                                                    <div
                                                        v-show="hoveredItemId === item.id"
                                                        class="group action-buttons"
                                                    >
                                                        <div class="relative group">
                                                            <div
                                                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-6"
                                                            >
                                                                {{ $t("constants.userActions.archive") }}
                                                            </div>
                                                            <button
                                                                type="button"
                                                                class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10"
                                                            >
                                                                <TrashIcon
                                                                    @click.stop="deleteEmail(item.id)"
                                                                    class="w-5 h-5 text-gray-500 group-hover:text-white"
                                                                />
                                                            </button>
                                                        </div>
                                                    </div>
                                                    <div
                                                        v-show="hoveredItemId === item.id"
                                                        class="group action-buttons"
                                                    >
                                                        <div class="relative group">
                                                            <div
                                                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7"
                                                            >
                                                                {{ $t("homePage.answer") }}
                                                            </div>
                                                            <button
                                                                @click.stop="openAnswer(item)"
                                                                type="button"
                                                                class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10"
                                                            >
                                                                <arrow-uturn-left-icon
                                                                    class="w-5 h-5 text-gray-500 group-hover:text-white"
                                                                />
                                                            </button>
                                                        </div>
                                                    </div>
                                                    <div
                                                        v-show="hoveredItemId === item.id"
                                                        class="group action-buttons cursor-pointer"
                                                    >
                                                        <div class="relative group">
                                                            <div
                                                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-[125px] w-[185px]"
                                                            >
                                                                {{ $t("constants.additionalActions") }}
                                                            </div>
                                                            <Menu as="div" class="relative inline-block text-left">
                                                                <div>
                                                                    <MenuButton
                                                                        @click="toggleTooltip"
                                                                        class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-gray-500 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10"
                                                                    >
                                                                        <ellipsis-horizontal-icon
                                                                            class="w-5 h-5 group-hover:text-white text-gray-500 group-active:text-gray-500 group-focus:text-red focus:text-gray-500"
                                                                        />
                                                                    </MenuButton>
                                                                </div>
                                                                <SeeMailModal />
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
</template>
