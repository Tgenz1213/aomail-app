<template>
    <div
        class="col-span-8 cursor-pointer"
        @click="toggleHiddenParagraph(email.id)"
        @mouseover="setHoveredItem(email.id)"
        @mouseleave="clearHoveredItem"
    >
        <div class="flex-auto group">
            <div class="flex gap-x-4">
                <p class="text-sm font-semibold leading-6 text-gray-800 dark:text-white">
                    {{ email.name }}
                </p>
                <div class="hidden group-hover:block px-2 py-0.5 bg-gray-300 text-white text-sm shadow rounded-xl">
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
            <p class="mt-1 text-md text-gray-700 leading-relaxed dark:text-blue-50">
                {{ email.description }}
            </p>
        </div>
        <ul
            v-show="showHiddenParagraphs[email.id]"
            role="list"
            class="text-black text-sm/6 pt-2"
            :ref="'parentElement' + email.id"
        >
            <li
                v-for="detail in email.details"
                :key="detail.id"
                class="pl-8"
                :ref="'hiddenText' + email.id"
                :data-text="detail.text"
            ></li>
        </ul>
    </div>
    <div class="col-span-2">
        <div class="flex justify-center">
            <span class="isolate inline-flex rounded-2xl">
                <div v-show="hoveredItemId === email.id" class="group action-buttons">
                    <div class="relative group">
                        <div
                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4 z-40"
                        >
                            {{ $t("constants.userActions.open") }}
                        </div>
                        <button
                            @click="openInNewWindow(email.providerId)"
                            type="button"
                            class="relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10"
                        >
                            <eye-icon class="w-5 h-5 text-gray-500 group-hover:text-white" />
                        </button>
                    </div>
                </div>
                <div v-show="hoveredItemId === email.id" class="group action-buttons">
                    <div class="relative group">
                        <div
                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7"
                        >
                            {{ $t("constants.userActions.reply") }}
                        </div>
                        <button
                            @click="openAnswer(item)"
                            type="button"
                            class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10"
                        >
                            <arrow-uturn-left-icon class="w-5 h-5 text-gray-500 group-hover:text-white" />
                        </button>
                    </div>
                </div>
                <div v-show="hoveredItemId === email.id" class="group action-buttons">
                    <div class="relative group">
                        <div
                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7"
                        >
                            {{ $t("replyLaterPage.removeFromReplyLater") }}
                        </div>
                        <button
                            @click="unmarkReplyLater(email.id)"
                            type="button"
                            class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10"
                        >
                            <ChatBubbleOvalLeftEllipsisIcon class="w-5 h-5 text-gray-500 group-hover:text-white" />
                        </button>
                    </div>
                </div>
                <div v-show="hoveredItemId === email.id" class="group action-buttons">
                    <div class="relative group">
                        <div
                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-8"
                        >
                            {{ $t("constants.userActions.archive") }}
                        </div>
                        <button
                            type="button"
                            class="relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10"
                        >
                            <TrashIcon
                                @click.stop="deleteEmail(email.id)"
                                class="w-5 h-5 text-gray-500 group-hover:text-white"
                            />
                        </button>
                    </div>
                </div>
                <div v-show="hoveredItemId === email.id" class="group action-buttons">
                    <div class="relative group">
                        <div
                            v-if="showTooltip"
                            class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-20 w-[185px]"
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
                            <transition
                                enter-active-class="transition ease-out duration-100"
                                enter-from-class="transform opacity-0 scale-95"
                                enter-to-class="transform opacity-100 scale-100"
                                leave-active-class="transition ease-in duration-75"
                                leave-from-class="transform opacity-100 scale-100"
                                leave-to-class="transform opacity-0 scale-95"
                            >
                                <MenuItems
                                    v-show="isMenuOpen"
                                    class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none cursor-pointer"
                                >
                                    <div class="py-1">
                                        <div v-if="email.rule">
                                            <MenuItem v-slot="{ active }">
                                                <a
                                                    @click.prevent="openRuleEditor(email.rule_id)"
                                                    href="#"
                                                    :class="[
                                                        active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                                                        'block px-4 py-1 text-sm',
                                                    ]"
                                                >
                                                    <span class="flex gap-x-2 items-center">
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
                                                            {{ $t("constants.userActions.changeTheRule") }}
                                                        </span>
                                                    </span>
                                                </a>
                                            </MenuItem>
                                        </div>
                                        <div v-else>
                                            <MenuItem v-slot="{ active }">
                                                <a
                                                    @click.prevent="openNewRule(email.name, email.email)"
                                                    href="#"
                                                    :class="[
                                                        active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                                                        'block px-4 py-1 text-sm',
                                                    ]"
                                                >
                                                    <span class="flex gap-x-2 items-center">
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
                                                            {{ $t("constants.userActions.createARule") }}
                                                        </span>
                                                    </span>
                                                </a>
                                            </MenuItem>
                                        </div>
                                    </div>
                                    <div class="py-1">
                                        <MenuItem v-slot="{ active }">
                                            <a
                                                @click.prevent="transferEmail(item)"
                                                :class="[
                                                    active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                                                    'block px-4 py-1 text-sm',
                                                ]"
                                            >
                                                <span class="flex gap-x-2 items-center">
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
                                                            style="fill: none; stroke: #000; stroke-width: 1.7px"
                                                        />
                                                        <path
                                                            d="M21.197,10.609l6.783,6.782m0,0l-6.783,6.783"
                                                            style="fill: none; stroke: #000; stroke-width: 1.7px"
                                                        />
                                                    </svg>
                                                    <span>
                                                        {{ $t("constants.userActions.transfer") }}
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
</template>
