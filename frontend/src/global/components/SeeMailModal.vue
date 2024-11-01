<template>
    <transition name="modal-fade">
        <div
            @click.self="closeModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            v-if="isOpen"
        >
            <div class="bg-white rounded-lg relative w-[800px] h-[600px] 2xl:w-[900px] 2xl:h-[800px]">
                <slot></slot>
                <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
                    <button
                        @click="closeModal"
                        type="button"
                        class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                    >
                        <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                    </button>
                </div>
                <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
                    <div class="ml-8 flex items-center space-x-2">
                        <EnvelopeOpenIcon class="w-6 h-6" />
                        <p class="block font-semibold leading-6 text-gray-900">{{ email?.subject }}</p>
                    </div>
                </div>
                <div class="overflow-auto h-[535px] 2xl:h-[736px]">
                    <div class="flex flex-col px-8 py-4">
                        <div class="mb-3">
                            <div class="flex">
                                <div class="flex flex-col gap-y-0">
                                    <div class="flex items-center gap-x-2">
                                        <p class="text-gray-600 font-semibold">{{ email?.sender.name }}</p>
                                        <p class="text-gray-600 text-sm">&lt;{{ email?.sender.email }}&gt;</p>
                                    </div>
                                </div>
                                <div class="flex items-center ml-auto">
                                    <div
                                        class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-2"
                                    >
                                        {{ $t("homePage.seeEmailModal.moreActions") }}
                                    </div>
                                    <div class="flex gap-x-1 justify-center">
                                        <span
                                            v-if="email?.priority === 'important'"
                                            class="inline-flex items-center rounded-md bg-orange-50 px-2 py-1 text-xs font-medium text-orange-700 ring-1 ring-inset ring-orange-600/10"
                                        >
                                            Important
                                        </span>
                                        <span
                                            v-else-if="email?.priority === 'informative'"
                                            class="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10"
                                        >
                                            Informative
                                        </span>
                                        <span
                                            v-else
                                            class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10"
                                        >
                                            Useless
                                        </span>
                                        <span
                                            v-if="email?.category"
                                            class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10"
                                        >
                                            {{ email?.category }}
                                        </span>
                                        <span
                                            v-if="email?.read"
                                            class="inline-flex items-center rounded-md bg-stone-50 px-2 py-1 text-xs font-medium text-stone-600 ring-1 ring-inset ring-stone-500/10"
                                        >
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                fill="none"
                                                viewBox="0 0 24 24"
                                                stroke-width="1.5"
                                                stroke="currentColor"
                                                class="h-4 w-4 mr-1"
                                            >
                                                <path
                                                    stroke-linecap="round"
                                                    stroke-linejoin="round"
                                                    d="M4.5 12.75l6 6 9-13.5"
                                                />
                                            </svg>
                                            {{ $t("homePage.modals.seeEmailModal.read") }}
                                        </span>
                                        <span class="isolate inline-flex">
                                            <div class="group action-buttons">
                                                <div class="relative group">
                                                    <div
                                                        v-if="!email?.read"
                                                        class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg top-full left-[-10px] translate-y-2"
                                                    >
                                                        {{ $t("homePage.modals.seeEmailModal.read") }}
                                                    </div>
                                                    <div
                                                        v-else
                                                        class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg top-full left-[-20px] translate-y-2"
                                                    >
                                                        {{ $t("homePage.unread") }}
                                                    </div>
                                                    <button
                                                        @click="email?.read ? markEmailAsUnread() : markEmailAsRead()"
                                                        type="button"
                                                        class="relative inline-flex items-center rounded-l-md px-1.5 py-1 text-sm font-semibold text-gray-400 border border-gray-600 hover:bg-gray-600 focus:z-10"
                                                    >
                                                        <check-icon
                                                            v-if="!email?.read"
                                                            class="w-5 h-5 group-hover:text-white text-gray-600 group-active:text-gray-600 group-focus:text-grey focus:text-gray-600"
                                                        />
                                                        <svg
                                                            v-else
                                                            xmlns="http://www.w3.org/2000/svg"
                                                            viewBox="0 0 24 24"
                                                            fill="none"
                                                            stroke-width="2"
                                                            stroke-linecap="round"
                                                            stroke-linejoin="round"
                                                            :class="`w-5 h-5 stroke-gray-600 group-hover:stroke-white`"
                                                        >
                                                            <path d="M5 9l5 5 9-9"></path>
                                                            <path d="M5 16l5 5 9-9"></path>
                                                        </svg>
                                                    </button>
                                                </div>
                                            </div>
                                            <div class="group action-buttons">
                                                <div class="relative group">
                                                    <div
                                                        class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg top-full left-[-30px] translate-y-2"
                                                    >
                                                        {{ $t("homePage.answer") }}
                                                    </div>
                                                    <button
                                                        @click="openAnswer"
                                                        type="button"
                                                        class="relative inline-flex items-center px-1.5 py-1 text-sm font-semibold text-gray-400 border-r border-t border-b border-gray-600 hover:bg-gray-600 focus:z-10"
                                                    >
                                                        <arrow-uturn-left-icon
                                                            class="w-5 h-5 group-hover:text-white text-gray-600 group-active:text-gray-600 group-focus:text-grey focus:text-gray-600"
                                                        />
                                                    </button>
                                                </div>
                                            </div>
                                            <div class="group action-buttons">
                                                <div class="relative group">
                                                    <div
                                                        class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg top-full left-[-25px] w-[90px] translate-y-2"
                                                    >
                                                        {{ $t("homePage.modals.seeEmailModal.manageRules") }}
                                                    </div>
                                                    <button
                                                        @click="openRule"
                                                        type="button"
                                                        class="relative inline-flex items-center px-1.5 py-1 text-sm font-semibold text-gray-400 border-t border-b border-gray-600 hover:bg-gray-600 focus:z-10"
                                                    >
                                                        <BeakerIcon
                                                            class="w-5 h-5 group-hover:text-white text-gray-600 group-active:text-gray-600 group-focus:text-grey focus:text-gray-600"
                                                        />
                                                    </button>
                                                </div>
                                            </div>
                                            <div class="group action-buttons">
                                                <div class="relative group">
                                                    <div
                                                        class="absolute hidden group-hover:block px-2 py-2 bg-black text-white text-sm rounded shadow-lg top-full left-[-5px] translate-y-2 -translate-x-3"
                                                    >
                                                        {{ $t("homePage.modals.seeEmailModal.moreActions") }}
                                                    </div>
                                                    <Menu as="div" class="relative inline-block text-left">
                                                        <div>
                                                            <MenuButton
                                                                @click="toggleTooltip"
                                                                class="relative inline-flex items-center rounded-r-md px-1.5 py-1 font-semibold text-gray-400 border border-gray-600 hover:bg-gray-600 focus:z-10"
                                                            >
                                                                <ellipsis-horizontal-icon
                                                                    class="w-5 h-5 group-hover:text-white text-gray-600 group-active:text-gray-600 group-focus:text-grey focus:text-gray-600"
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
                                                                    <MenuItem
                                                                        v-if="!email?.archive"
                                                                        v-slot="{ active }"
                                                                    >
                                                                        <a
                                                                            @click.prevent="archiveEmail"
                                                                            :class="[
                                                                                active
                                                                                    ? `bg-gray-100 text-gray-900`
                                                                                    : `text-gray-700`,
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
                                                                                        d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5m8.25 3v6.75m0 0-3-3m3 3 3-3M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z"
                                                                                    />
                                                                                </svg>
                                                                                <span>
                                                                                    {{
                                                                                        $t(
                                                                                            "constants.userActions.archive"
                                                                                        )
                                                                                    }}
                                                                                </span>
                                                                            </span>
                                                                        </a>
                                                                    </MenuItem>
                                                                    <MenuItem v-else v-slot="{ active }">
                                                                        <a
                                                                            @click.prevent="unarchiveEmail"
                                                                            :class="[
                                                                                active
                                                                                    ? `bg-gray-100 text-gray-900`
                                                                                    : `text-gray-700`,
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
                                                                                        d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5m8.25 3v6.75m0 0-3-3m3 3 3-3M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z"
                                                                                    />
                                                                                </svg>
                                                                                <span>
                                                                                    {{
                                                                                        $t(
                                                                                            "constants.userActions.unarchive"
                                                                                        )
                                                                                    }}
                                                                                </span>
                                                                            </span>
                                                                        </a>
                                                                    </MenuItem>
                                                                </div>
                                                                <div class="py-1">
                                                                    <MenuItem v-slot="{ active }">
                                                                        <a
                                                                            @click.prevent="deleteEmail"
                                                                            :class="[
                                                                                active
                                                                                    ? `bg-gray-100 text-gray-900`
                                                                                    : `text-gray-700`,
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
                                                                                        d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                                                                                    />
                                                                                </svg>
                                                                                <span>
                                                                                    {{
                                                                                        $t(
                                                                                            "constants.userActions.delete"
                                                                                        )
                                                                                    }}
                                                                                </span>
                                                                            </span>
                                                                        </a>
                                                                    </MenuItem>
                                                                </div>
                                                                <div class="py-1">
                                                                    <MenuItem
                                                                        v-if="!email?.answerLater"
                                                                        v-slot="{ active }"
                                                                    >
                                                                        <a
                                                                            @click.prevent="markEmailReplyLater"
                                                                            :class="[
                                                                                active
                                                                                    ? 'bg-gray-100 text-gray-600'
                                                                                    : 'text-gray-700',
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
                                                                    <MenuItem v-else v-slot="{ active }">
                                                                        <a
                                                                            @click.prevent="markEmailAsUnreplyLater"
                                                                            :class="[
                                                                                active
                                                                                    ? 'bg-gray-100 text-gray-600'
                                                                                    : 'text-gray-700',
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
                                                                                            "constants.userActions.unreplyLater"
                                                                                        )
                                                                                    }}
                                                                                </span>
                                                                            </span>
                                                                        </a>
                                                                    </MenuItem>
                                                                </div>
                                                                <div class="py-1">
                                                                    <MenuItem v-slot="{ active }">
                                                                        <a
                                                                            @click.prevent="transferEmail"
                                                                            :class="[
                                                                                active
                                                                                    ? 'bg-gray-100 text-gray-600'
                                                                                    : 'text-gray-700',
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
                            </div>
                        </div>
                        <div class="mb-4">
                            <div v-html="email?.htmlContent"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import {
    ArrowUturnLeftIcon,
    CheckIcon,
    EllipsisHorizontalIcon,
    EnvelopeOpenIcon,
    XMarkIcon,
    BeakerIcon,
} from "@heroicons/vue/24/outline";
import { Email } from "../types";

const isMenuOpen = ref(false);

defineProps<{
    isOpen: boolean;
    email: Email | undefined;
}>();

const emits = defineEmits([
    "closeModal",
    "markEmailAsRead",
    "markEmailAsUnread",
    "openRule",
    "markEmailReplyLater",
    "markEmailAsUnreplyLater",
    "openAnswer",
    "transferEmail",
    "archiveEmail",
    "unarchiveEmail",
    "deleteEmail",
]);

const closeModal = () => {
    emits("closeModal");
};

function toggleTooltip() {
    isMenuOpen.value = true;
}

const openAnswer = () => {
    emits("openAnswer");
};

const markEmailAsRead = () => {
    emits("markEmailAsRead");
    closeModal();
};

const markEmailAsUnread = () => {
    emits("markEmailAsUnread");
    closeModal();
};

const transferEmail = () => {
    emits("transferEmail");
    closeModal();
};

const markEmailReplyLater = () => {
    emits("markEmailReplyLater");
    closeModal();
};

const markEmailAsUnreplyLater = () => {
    emits("markEmailAsUnreplyLater");
    closeModal();
};

const openRule = () => {
    emits("openRule");
};

const archiveEmail = () => {
    emits("archiveEmail");
    closeModal();
};

const unarchiveEmail = () => {
    emits("unarchiveEmail");
    closeModal();
};

const deleteEmail = () => {
    emits("deleteEmail");
    closeModal();
};

onMounted(() => {
    document.addEventListener("keydown", (event: KeyboardEvent) => {
        if (event.key === "Escape") {
            closeModal();
        }
    });
});
</script>
