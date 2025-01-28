<template>
    <SeeMailModal
        :isOpen="isSeeMailModalVisible"
        :email="updatedEmail"
        @closeModal="closeSeeMailModal"
        @openRule="openRule"
        @markEmailAsRead="markEmailAsRead"
        @markEmailAsUnread="markEmailAsUnread"
        @archiveEmail="archiveEmail"
        @unarchiveEmail="unarchiveEmail"
        @deleteEmail="deleteEmail"
        @markEmailReplyLater="markEmailReplyLater"
        @markEmailAsUnreplyLater="markEmailAsUnreplyLater"
        @openAnswer="openAnswer"
        @transferEmail="transferEmail"
    />
    <div class="grid grid-cols-10 gap-4 items-center" @mouseenter="isHovered = true" @mouseleave="isHovered = false">
        <div class="col-span-8 cursor-pointer">
            <div @click="toggleShortSummary">
                <div class="flex-auto group">
                    <div class="flex gap-x-4">
                        <div class="flex items-center">
                            <p :class="`text-sm font-semibold leading-6 text-${color}-900 mr-2`">
                                {{ email.sender.name }}
                            </p>
                            <p :class="`text-sm leading-6 text-${color}-700 mr-2`">
                                {{ formatSentTime(email.sentDate, email.sentTime) }}
                            </p>
                        </div>
                        <div
                            :class="`hidden group-hover:block px-2 py-0.5 bg-${color}-300 text-white text-sm shadow rounded-xl`"
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
                                <p>{{ $t("constants.userActions.clickToSeeTheSummary") }}</p>
                            </div>
                        </div>
                    </div>
                    <p class="mt-1 text-md text-gray-700 leading-relaxed">{{ email.oneLineSummary }}</p>
                </div>
                <div v-show="isShortSummaryVisible">
                    <p class="text-black text-sm/6 pt-1.5">{{ email.shortSummary }}</p>
                </div>
                <div class="flex gap-x-2 pt-1.5">
                    <span
                        v-if="email?.flags?.meeting"
                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10"
                    >
                        {{ $t("homePage.flag.meeting") }}
                    </span>
                    <span
                        v-if="email?.flags?.newsletter"
                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10"
                    >
                        {{ $t("homePage.flag.newsletter") }}
                    </span>
                    <span
                        v-if="email?.flags?.notification"
                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10"
                    >
                        {{ $t("homePage.flag.notification") }}
                    </span>
                    <span
                        v-if="email?.flags?.scam"
                        class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10"
                    >
                        {{ $t("homePage.flag.scam") }}
                    </span>
                    <span
                        v-if="email?.flags?.spam"
                        class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10"
                    >
                        {{ $t("homePage.flag.spam") }}
                    </span>
                </div>
            </div>
            <div
                v-if="email.hasAttachments"
                class="attachments-container overflow-y-auto max-h-32 flex flex-wrap gap-x-2 pt-2.5"
            >
                <div
                    v-for="attachment in email.attachments"
                    :key="attachment.attachmentId"
                    class="group flex items-center gap-x-1 bg-gray-100 px-2 py-2 rounded-md hover:bg-gray-600"
                    @click.prevent="downloadAttachment(email.id as number, attachment.attachmentName)"
                >
                    <component
                        :is="getIconComponent(attachment.attachmentName)"
                        class="w-5 h-5 text-gray-600 group-hover:text-white"
                    />
                    <p class="text-sm text-gray-600 group-hover:text-white">{{ attachment.attachmentName }}</p>
                </div>
            </div>
        </div>
        <div class="col-span-2 z-10">
            <div class="flex justify-center">
                <span class="isolate inline-flex rounded-2xl">
                    <div v-show="isHovered" class="group action-buttons">
                        <div class="relative group">
                            <div
                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4"
                            >
                                {{ $t("constants.userActions.open") }}
                            </div>
                            <button
                                @click="openEmail"
                                type="button"
                                :class="`relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-${color}-400 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`"
                            >
                                <eye-icon :class="`w-5 h-5 text-${color}-400 group-hover:text-white`" />
                            </button>
                        </div>
                    </div>
                    <div v-if="block" v-show="isHovered" class="group action-buttons">
                        <div class="relative group">
                            <div
                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-6"
                            >
                                {{ $t("homePage.block") }}
                            </div>
                            <button
                                type="button"
                                :class="`relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-${color}-900 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`"
                            >
                                <HandRaisedIcon
                                    @click.stop="setRuleBlockForSender"
                                    :class="`w-5 h-5 text-${color}-400 group-hover:text-white`"
                                />
                            </button>
                        </div>
                    </div>
                    <div v-if="!replyLater" v-show="isHovered" class="group action-buttons">
                        <div class="relative group">
                            <div
                                v-if="!email.read"
                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4"
                            >
                                {{ $t("homePage.read") }}
                            </div>
                            <div
                                v-else
                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-5"
                            >
                                {{ $t("homePage.unread") }}
                            </div>
                            <button
                                @click="email.read ? markEmailAsUnread() : markEmailAsRead()"
                                type="button"
                                :class="`relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-${color}-900 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`"
                            >
                                <check-icon
                                    v-if="!email.read"
                                    :class="`w-5 h-5 text-${color}-400 group-hover:text-white`"
                                />
                                <svg
                                    v-else
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    :class="`w-5 h-5 stroke-${color}-400 group-hover:stroke-white`"
                                >
                                    <path d="M5 9l5 5 9-9"></path>
                                    <path d="M5 16l5 5 9-9"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                    <div v-else v-show="isHovered" class="group action-buttons">
                        <div class="relative group">
                            <div
                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-center text-sm rounded shadow-lg mt-[-45px] -ml-[60px] w-[140px]"
                            >
                                {{ $t("constants.userActions.unreplyLater") }}
                            </div>
                            <button
                                @click="markEmailAsUnreplyLater"
                                type="button"
                                :class="`relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-${color}-900 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1.5"
                                    stroke="currentColor"
                                    :class="`w-5 h-5 text-${color}-400 group-hover:text-white`"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M12 9.75 14.25 12m0 0 2.25 2.25M14.25 12l2.25-2.25M14.25 12 12 14.25m-2.58 4.92-6.374-6.375a1.125 1.125 0 0 1 0-1.59L9.42 4.83c.21-.211.497-.33.795-.33H19.5a2.25 2.25 0 0 1 2.25 2.25v10.5a2.25 2.25 0 0 1-2.25 2.25h-9.284c-.298 0-.585-.119-.795-.33Z"
                                    />
                                </svg>
                            </button>
                        </div>
                    </div>
                    <div v-show="isHovered" class="group action-buttons">
                        <div class="relative group">
                            <div
                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7"
                            >
                                {{ $t("homePage.answer") }}
                            </div>
                            <button
                                @click="openAnswer"
                                type="button"
                                :class="`relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-${color}-900 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`"
                            >
                                <arrow-uturn-left-icon :class="`w-5 h-5 text-${color}-400 group-hover:text-white`" />
                            </button>
                        </div>
                    </div>
                    <div v-show="isHovered" class="group action-buttons">
                        <div class="relative group">
                            <div
                                class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-center text-sm rounded shadow-lg mt-[-45px] -ml-[115px] w-[185px]"
                            >
                                {{ $t("constants.additionalActions") }}
                            </div>
                            <Menu as="div" class="relative inline-block text-left">
                                <MenuButton
                                    @click="toggleMenu"
                                    :class="`relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-${color}-400 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`"
                                >
                                    <ellipsis-horizontal-icon
                                        :class="`w-5 h-5 group-hover:text-white text-${color}-400 group-active:text-${color}-400 group-focus:text-${color} focus:text-${color}-400`"
                                    />
                                </MenuButton>
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
                                            <div v-if="email?.rule?.hasRule">
                                                <MenuItem v-slot="{ active }">
                                                    <a
                                                        @click.prevent="openRuleEditor"
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
                                                            <span>{{ $t("constants.userActions.changeTheRule") }}</span>
                                                        </span>
                                                    </a>
                                                </MenuItem>
                                            </div>
                                            <div v-else>
                                                <MenuItem v-slot="{ active }">
                                                    <a
                                                        @click.prevent="openNewRule"
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
                                                            <span>{{ $t("constants.userActions.createARule") }}</span>
                                                        </span>
                                                    </a>
                                                </MenuItem>
                                            </div>
                                        </div>
                                        <div class="py-1">
                                            <MenuItem v-slot="{ active }">
                                                <a
                                                    @click.prevent="archiveEmail"
                                                    :class="[
                                                        active ? `bg-gray-100 text-gray-900` : `text-gray-700`,
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
                                                        <span>{{ $t("constants.userActions.archive") }}</span>
                                                    </span>
                                                </a>
                                            </MenuItem>
                                        </div>
                                        <div class="py-1">
                                            <MenuItem v-slot="{ active }">
                                                <a
                                                    @click.prevent="deleteEmail"
                                                    :class="[
                                                        active ? `bg-gray-100 text-gray-900` : `text-gray-700`,
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
                                                        <span>{{ $t("constants.userActions.delete") }}</span>
                                                    </span>
                                                </a>
                                            </MenuItem>
                                        </div>
                                        <div class="py-1" v-if="!email.answerLater">
                                            <MenuItem v-slot="{ active }">
                                                <a
                                                    @click.prevent="markEmailReplyLater()"
                                                    :class="[
                                                        active ? `bg-gray-100 text-gray-900` : `text-gray-700`,
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
                                                                style="fill: none; stroke: #000; stroke-width: 1.7px"
                                                            />
                                                            <path
                                                                d="M7.783,17.391l-6.783,-6.782m0,0l6.783,-6.783"
                                                                style="fill: none; stroke: #000; stroke-width: 1.7px"
                                                            />
                                                        </svg>
                                                        <span>{{ $t("constants.userActions.replyLater") }}</span>
                                                    </span>
                                                </a>
                                            </MenuItem>
                                        </div>
                                        <div class="py-1">
                                            <MenuItem v-slot="{ active }">
                                                <a
                                                    @click.prevent="transferEmail"
                                                    :class="[
                                                        active ? `bg-gray-100 text-gray-900` : `text-gray-700`,
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
                                                        <span>{{ $t("constants.userActions.transfer") }}</span>
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
</template>

<script setup lang="ts">
import { Ref, ref, inject } from "vue";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import {
    EyeIcon,
    CheckIcon,
    ArrowUturnLeftIcon,
    EllipsisHorizontalIcon,
    DocumentIcon,
    CameraIcon,
    HandRaisedIcon,
} from "@heroicons/vue/24/outline";
import { Email } from "@/global/types";
import { getData, getDataRawResponse, postData, deleteData, putData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import SeeMailModal from "./SeeMailModal.vue";
import router from "../../router/router";
import { formatSentTime } from "@/global/formatters";

const props = withDefaults(
    defineProps<{
        email: Email;
        color?: string;
        block?: boolean;
        replyLater?: boolean;
    }>(),
    {
        color: "gray",
        block: false,
        replyLater: false,
    }
);

const selectedCategory = inject("selectedCategory") as Ref<string>;
const localEmail = ref({ ...props.email });
const isHovered = ref(false);
const isMenuOpen = ref(false);
const isShortSummaryVisible = ref(false);
const isSeeMailModalVisible = ref(false);
const updatedEmail = ref<Email | undefined>(undefined);

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const fetchEmailsData = inject("fetchEmailsData") as (categoryName: string) => Promise<void>;
const fetchCategoriesAndTotals = inject("fetchCategoriesAndTotals") as () => Promise<void>;
const emails = inject("emails") as Ref<{ [key: string]: { [key: string]: Email[] } }>;
const readCount = inject("readCount") as Ref<number>;
const uselessCount = inject("uselessCount") as Ref<number>;

const toggleShortSummary = () => {
    isShortSummaryVisible.value = !isShortSummaryVisible.value;
};

const openEmail = async () => {
    const result = await postData(`user/get_email_content/`, { id: props.email.id });

    if (result.success && result.data.content) {
        updatedEmail.value = { ...props.email, htmlContent: result.data.content };
        isSeeMailModalVisible.value = true;
    } else {
        displayPopup?.("error", "No HTML content received", result.error as string);
    }
};

async function setRuleBlockForSender() {
    localEmail.value.read = true;

    const resultBlock = await postData(`user/emails/${localEmail.value.id}/block_sender/`, {});
    if (!resultBlock.success) {
        displayPopup?.("error", i18n.global.t("homepage.blockEmailAddressFailure"), resultBlock.error as string);
    }

    markEmailAsRead();
    fetchEmailsData(selectedCategory.value);
}

const closeSeeMailModal = () => {
    isSeeMailModalVisible.value = false;
};

function openRule() {
    if (localEmail?.value?.rule?.hasRule) {
        openRuleEditor();
    } else {
        openNewRule();
    }
}

function openRuleEditor() {
    router.push({ name: "rules", query: { idRule: localEmail?.value?.rule?.ruleId, editRule: "true" } });
}

function openNewRule() {
    router.push({
        name: "rules",
        query: { ruleName: localEmail.value.sender.name, ruleEmail: localEmail.value.sender.email, editRule: "false" },
    });
}

async function markEmailAsRead() {
    for (const category in emails.value) {
        for (const subCategory in emails.value[category]) {
            const index = emails.value[category][subCategory].findIndex((email) => email.id === localEmail.value.id);
            if (index !== -1) {
                emails.value[category][subCategory][index].read = true;
                if (emails.value[category][subCategory][index].priority === "useless") {
                    uselessCount.value--;
                }
                break;
            }
        }
    }
    const result = await putData("user/emails/update/", { ids: [localEmail.value.id], action: "read" });
    fetchCategoriesAndTotals();
    readCount.value++;
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailReadFailure"), result.error as string);
    }
}

async function markEmailAsUnread() {
    for (const category in emails.value) {
        for (const subCategory in emails.value[category]) {
            const index = emails.value[category][subCategory].findIndex((email) => email.id === localEmail.value.id);
            if (index !== -1) {
                emails.value[category][subCategory][index].read = false;
                if (emails.value[category][subCategory][index].priority === "useless") {
                    uselessCount.value++;
                }
                break;
            }
        }
    }
    const result = await putData("user/emails/update/", { ids: [localEmail.value.id], action: "unread" });
    fetchCategoriesAndTotals();
    readCount.value--;
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailUnreadFailure"), result.error as string);
    }
}

async function markEmailReplyLater() {
    for (const category in emails.value) {
        for (const subCategory in emails.value[category]) {
            const index = emails.value[category][subCategory].findIndex((email) => email.id === localEmail.value.id);
            if (index !== -1) {
                emails.value[category][subCategory][index].answerLater = true;
                break;
            }
        }
    }
    const result = await putData("user/emails/update/", { ids: [localEmail.value.id], action: "replyLater" });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailReplyLaterFailure"), result.error as string);
        return;
    }
    markEmailAsUnread();
}

async function markEmailAsUnreplyLater() {
    for (const category in emails.value) {
        for (const subCategory in emails.value[category]) {
            const index = emails.value[category][subCategory].findIndex((email) => email.id === localEmail.value.id);
            if (index !== -1) {
                emails.value[category][subCategory][index].answerLater = false;
                break;
            }
        }
    }
    let result = await putData("user/emails/update/", { ids: [localEmail.value.id], action: "unreplyLater" });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailReplyLaterFailure"), result.error as string);
    }
}

async function openAnswer() {
    const result = await getData(`get_mail_by_id?email_id=${localEmail.value.providerId}`);
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("constants.popUpConstants.openReplyPageFailure"), result.error as string);
        return;
    }

    const result_mail_content = await postData(`user/get_email_content/`, { id: props.email.id });
    if (!result_mail_content.success) {
        displayPopup?.("error", i18n.global.t("constants.popUpConstants.openReplyPageFailure"), result.error as string);
        return;
    }

    sessionStorage.setItem("subject", JSON.stringify(result.data.subject));
    sessionStorage.setItem("cc", result.data.cc);
    sessionStorage.setItem("bcc", result.data.bcc);
    sessionStorage.setItem("decodedData", JSON.stringify(result.data.decodedData));
    sessionStorage.setItem("emailUser", JSON.stringify(result.data.emailUser));
    sessionStorage.setItem("htmlContent", result_mail_content.data.content);
    sessionStorage.setItem("senderEmail", JSON.stringify(localEmail.value.sender.email));
    sessionStorage.setItem("providerId", JSON.stringify(localEmail.value.providerId));
    sessionStorage.setItem("shortSummary", JSON.stringify(localEmail.value.shortSummary));
    sessionStorage.setItem("importance", JSON.stringify(localEmail.value.priority));

    router.push({ name: "answer" });
}

async function transferEmail() {
    const result = await getData(`get_mail_by_id?email_id=${localEmail.value.providerId}`);
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.transferEmailFailure"), result.error as string);
        return;
    }

    sessionStorage.setItem("subject", JSON.stringify(result.data.subject));
    sessionStorage.setItem("cc", result.data.cc);
    sessionStorage.setItem("attachments", JSON.stringify(localEmail.value.attachments));
    sessionStorage.setItem("emailId", JSON.stringify(localEmail.value.id));
    sessionStorage.setItem("decodedData", JSON.stringify(result.data.decodedData));
    sessionStorage.setItem("emailUser", JSON.stringify(result.data.emailUser));
    sessionStorage.setItem("senderEmail", JSON.stringify(localEmail.value.sender.email));
    sessionStorage.setItem("shortSummary", JSON.stringify(localEmail.value.shortSummary));
    sessionStorage.setItem("date", JSON.stringify(result.data.date));

    router.push({ name: "transfer" });
}

async function deleteEmail() {
    for (const category in emails.value) {
        for (const subCategory in emails.value[category]) {
            const index = emails.value[category][subCategory].findIndex((email) => email.id === localEmail.value.id);
            if (index !== -1) {
                emails.value[category][subCategory].splice(index, 1);
                break;
            }
        }
    }
    const result = await deleteData(`user/emails/${localEmail.value.id}/delete/`);
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("constants.popUpConstants.deleteEmailFailure"), result.error as string);
    }
}

async function archiveEmail() {
    for (const category in emails.value) {
        for (const subCategory in emails.value[category]) {
            const index = emails.value[category][subCategory].findIndex((email) => email.id === localEmail.value.id);
            if (index !== -1) {
                emails.value[category][subCategory][index].archive = true;
                break;
            }
        }
    }
    const result = await putData("user/emails/update/", {
        ids: [localEmail.value.id],
        action: "archive",
    });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("constants.popUpConstants.archiveEmailFailure"), result.error as string);
    }
}

async function unarchiveEmail() {
    for (const category in emails.value) {
        for (const subCategory in emails.value[category]) {
            const index = emails.value[category][subCategory].findIndex((email) => email.id === localEmail.value.id);
            if (index !== -1) {
                emails.value[category][subCategory][index].archive = false;
                break;
            }
        }
    }
    const result = await putData("user/emails/update/", { ids: [localEmail.value.id], action: "unarchive" });
    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.unarchiveEmailFailure"),
            result.error as string
        );
    }
}

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value;
};

const getIconComponent = (fileName: string) => {
    const extension = fileName.split(".").pop()?.toLowerCase();
    if (["png", "jpg", "jpeg", "gif"].includes(extension || "")) {
        return CameraIcon;
    } else {
        return DocumentIcon;
    }
};

const downloadAttachment = async (emailId: number, attachmentName: string) => {
    const response = await getDataRawResponse(`user/emails/${emailId}/attachments/${attachmentName}/`, {
        "Content-Type": "application/json",
    });

    if (response instanceof Response) {
        const attachmentData = await response.blob();
        const url = window.URL.createObjectURL(attachmentData);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", attachmentName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } else {
        displayPopup?.("error", "Failed to fetch attachment", response.error as string);
    }
};
</script>
