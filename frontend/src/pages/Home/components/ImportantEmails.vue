<template>
    <div class="px-6 pb-6">
        <div class="bg-orange-100 bg-opacity-90 rounded-md">
            <div class="flex px-3 py-2">
                <p class="flex-1 text-sm font-semibold leading-6 text-orange-600">
                    {{ $t("constants.ruleModalConstants.important") }}
                </p>
                <div class="ml-auto">
                    <exclamation-triangle-icon class="w-6 h-6 text-orange-500" />
                </div>
            </div>
        </div>
        <div v-for="(emailsByDate, date) in groupedEmailsByCategoryAndDate(IMPORTANT)" :key="date">
            <div class="pt-3 px-4">
                <div class="relative">
                    <div class="absolute inset-0 flex items-center" aria-hidden="true">
                        <div class="w-full border-t border-gray-200"></div>
                    </div>
                    <div class="relative flex justify-center">
                        <span class="bg-white px-2 text-xs text-gray-500">
                            {{ date }}
                        </span>
                    </div>
                </div>
            </div>
            <div class="flex px-4 pt-4">
                <div class="flex">
                    <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-orange-300">
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
                <div class="ml-6 flex-grow">
                    <div
                        class="overflow-hidden border-l-4 border-orange-300 hover:rounded-l-xl"
                        style="overflow: visible"
                    >
                        <ul role="list" class="divide-y divide-gray-200">
                            <li
                                v-for="item in emailsByDate"
                                :key="item.id"
                                class="px-6 md:py-5 2xl:py-6 hover:bg-opacity-70 grid grid-cols-10 gap-4 items-center"
                                @mouseover="setHoveredItem(item.id)"
                                @mouseleave="clearHoveredItem"
                            >
                                <div class="col-span-8 cursor-pointer">
                                    <div @click="toggleHiddenParagraph(item.id)">
                                        <div class="flex-auto group">
                                            <div class="flex gap-x-4">
                                                <div class="flex items-center">
                                                    <p class="text-sm font-semibold leading-6 text-orange-700 mr-2">
                                                        {{ item.name }}
                                                    </p>
                                                    <p class="text-sm leading-6 text-orange-700">
                                                        {{ item.time }}
                                                    </p>
                                                </div>
                                                <div
                                                    class="hidden group-hover:block px-2 py-0.5 bg-orange-300 text-white text-sm shadow rounded-xl"
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
                                                        <p>
                                                            {{ $t("constants.userActions.clickToSeeTheSummary") }}
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
                                            <p class="mt-1 text-md text-gray-700 leading-relaxed">
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
                                    <div v-if="item.has_attachments" class="flex pt-2.5 gap-x-2">
                                        <div
                                            v-for="attachment in item.attachments"
                                            :key="attachment.attachmentId"
                                            class="group flex items-center gap-x-1 bg-gray-100 px-2 py-2 rounded-md hover:bg-gray-600"
                                            @click.prevent="
                                                () => downloadAttachment(item.id, attachment.attachmentName)
                                            "
                                        >
                                            <component
                                                :is="getIconComponent(attachment.attachmentName)"
                                                class="w-5 h-5 text-gray-600 group-hover:text-white"
                                            />
                                            <p class="text-sm text-gray-600 group-hover:text-white">
                                                {{ attachment.attachmentName }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-span-2">
                                    <div class="flex justify-center">
                                        <span class="isolate inline-flex rounded-2xl">
                                            <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                <div class="relative group">
                                                    <div
                                                        class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4"
                                                    >
                                                        {{ $t("constants.userActions.open") }}
                                                    </div>
                                                    <button
                                                        @click="openSeeModal(item)"
                                                        type="button"
                                                        class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-orange-300 hover:bg-orange-300 focus:z-10"
                                                    >
                                                        <eye-icon
                                                            class="w-5 h-5 text-orange-400 group-hover:text-white"
                                                        />
                                                    </button>
                                                </div>
                                            </div>
                                            <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                <div class="relative group">
                                                    <div
                                                        class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-2"
                                                    >
                                                        {{ $t("homePage.read") }}
                                                    </div>
                                                    <button
                                                        @click="markEmailAsRead(item.id)"
                                                        type="button"
                                                        class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-orange-300 hover:bg-orange-300 focus:z-10"
                                                    >
                                                        <check-icon
                                                            class="w-5 h-5 text-orange-400 group-hover:text-white"
                                                        />
                                                    </button>
                                                </div>
                                            </div>
                                            <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                <div class="relative group">
                                                    <div
                                                        class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7"
                                                    >
                                                        {{ $t("homePage.answer") }}
                                                    </div>
                                                    <button
                                                        @click="openAnswer(item)"
                                                        type="button"
                                                        class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-orange-300 hover:bg-orange-300 focus:z-10"
                                                    >
                                                        <arrow-uturn-left-icon
                                                            class="w-5 h-5 text-orange-400 group-hover:text-white"
                                                        />
                                                    </button>
                                                </div>
                                            </div>
                                            <div v-show="hoveredItemId === item.id" class="group action-buttons">
                                                <div class="relative group">
                                                    <div
                                                        class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-[90px] w-[185px]"
                                                    >
                                                        {{ $t("constants.additionalActions") }}
                                                    </div>
                                                    <Menu as="div" class="relative inline-block text-left">
                                                        <div>
                                                            <MenuButton
                                                                @click="toggleTooltip"
                                                                class="relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-orange-400 ring-1 ring-inset ring-orange-300 hover:bg-orange-300 focus:z-10"
                                                            >
                                                                <ellipsis-horizontal-icon
                                                                    class="w-5 h-5 group-hover:text-white text-orange-400 group-active:text-orange-400 group-focus:text-orange focus:text-orange-400"
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
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
