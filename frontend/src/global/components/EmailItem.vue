<template>
    <SeeMailModal
        :isOpen="isSeeMailModalVisible"
        :email="updatedEmail"
        @closeModal="closeSeeMailModal"
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
                            :class="`hidden group-hover:block px-2 bg-${color}-100 border border-${color}-200 bg-opacity-90 rounded-md text-sm`"
                        >
                            <div class="flex gap-x-1 items-center">
                                <SparklesIcon :class="`w-4 h-4 text-${color}-500`" />
                                <p :class="`text-${color}-600`">
                                    {{ $t("constants.userActions.clickToSeeTheSummary") }}
                                </p>
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
                        📅 {{ $t("homePage.flag.meeting") }}
                    </span>
                    <span
                        v-if="email?.flags?.newsletter"
                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10"
                    >
                        📰 {{ $t("homePage.flag.newsletter") }}
                    </span>
                    <span
                        v-if="email?.flags?.notification"
                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10"
                    >
                        🔔 {{ $t("homePage.flag.notification") }}
                    </span>
                    <span
                        v-if="email?.flags?.scam"
                        class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10"
                    >
                        🚨 {{ $t("homePage.flag.scam") }}
                    </span>
                    <span
                        v-if="email?.flags?.spam"
                        class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10"
                    >
                        🚫 {{ $t("homePage.flag.spam") }}
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
        <div class="col-span-2">
            <div class="flex justify-end">
                <span class="isolate inline-flex items-center rounded-2xl pr-6">
                    <div class="flex items-center space-x-1" :class="{ 'hidden': !isHovered }">
                        <!-- See Email Button -->
                        <div class="relative group">
                            <button
                                @click="openEmail"
                                class="flex text-gray-600 hover:text-gray-800 rounded-full p-2.5 hover:bg-gray-200/80 focus:outline-none items-center justify-center"
                            >
                                <eye-icon class="w-5 h-5" />
                            </button>
                            <div class="absolute hidden group-hover:block px-3 py-1.5 bg-gray-800 text-white text-xs rounded shadow-lg -top-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
                                {{ $t("constants.userActions.open") }}
                            </div>
                        </div>

                        <!-- Block Button -->
                        <div v-if="block" class="relative group">
                            <button
                                @click="setRuleBlockForSender"
                                class="flex text-gray-600 hover:text-gray-800 rounded-full p-2.5 hover:bg-gray-200/80 focus:outline-none items-center justify-center"
                            >
                                <hand-raised-icon class="w-5 h-5" />
                            </button>
                            <div class="absolute hidden group-hover:block px-3 py-1.5 bg-gray-800 text-white text-xs rounded shadow-lg -top-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
                                {{ $t("homePage.block") }}
                            </div>
                        </div>

                        <!-- Read/Unread Button -->
                        <div class="relative group">
                            <div class="absolute hidden group-hover:block px-3 py-1.5 bg-gray-800 text-white text-xs rounded shadow-lg -top-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
                                {{ email.read ? $t("homePage.unread") : $t("homePage.read") }}
                            </div>
                            <button
                                @click="email.read ? markEmailAsUnread() : markEmailAsRead()"
                                class="flex text-gray-600 hover:text-gray-800 rounded-full p-2.5 hover:bg-gray-200/80 focus:outline-none items-center justify-center"
                            >
                                <check-icon v-if="!email.read" class="w-5 h-5 text-gray-600" />
                                <svg
                                    v-else
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    class="w-5 h-5 text-gray-600"
                                >
                                    <path d="M5 9l5 5 9-9"></path>
                                    <path d="M5 16l5 5 9-9"></path>
                                </svg>
                            </button>
                        </div>

                        <!-- Answer Button -->
                        <div class="relative group">
                            <button
                                @click="openAnswer"
                                class="flex text-gray-600 hover:text-gray-800 rounded-full p-2.5 hover:bg-gray-200/80 focus:outline-none items-center justify-center"
                            >
                                <arrow-uturn-left-icon class="w-5 h-5" />
                            </button>
                            <div class="absolute hidden group-hover:block px-3 py-1.5 bg-gray-800 text-white text-xs rounded shadow-lg -top-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
                                {{ $t("homePage.answer") }}
                            </div>
                        </div>

                        <!-- More Actions Menu -->
                        <Menu as="div" class="relative">
                            <MenuButton
                                @click="toggleMenu"
                                @mouseenter="isHovered = true"
                                @mouseleave="handleButtonMouseLeave"
                                class="flex text-gray-600 hover:text-gray-800 rounded-full p-2.5 hover:bg-gray-200/80 focus:outline-none items-center justify-center"
                            >
                                <ellipsis-horizontal-icon class="w-5 h-5" />
                            </MenuButton>

                            <Teleport to="body">
                                <MenuItems
                                    v-show="isMenuOpen"
                                    @mouseenter="isHovered = true"
                                    @mouseleave="handleMenuMouseLeave"
                                    class="fixed z-[100] mt-1 w-48 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none cursor-pointer"
                                    :style="{
                                        top: `${menuPosition.y}px`,
                                        left: `${menuPosition.x}px`
                                    }"
                                >
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
                            </Teleport>
                        </Menu>
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
    SparklesIcon,
    ArchiveBoxIcon,
    TrashIcon,
    ClockIcon,
    ArrowPathRoundedSquareIcon,
} from "@heroicons/vue/24/outline";
import { Email } from "@/global/types";
import { getData, getDataRawResponse, postData, deleteData, putData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import SeeMailModal from "./SeeMailModal.vue";
import router from "../../router/router";
import { formatSentTime } from "@/global/formatters";
import { Teleport } from "vue";

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
const isMarking = ref(false);
const menuPosition = ref({ x: 0, y: 0 });

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
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.noHtmlContent"),
            result.error as string
        );
    }
};

async function setRuleBlockForSender() {
    localEmail.value.read = true;

    const result = await postData("user/rules/", {
        senderEmails: [localEmail.value.sender.email],
        actionDelete: true,
    });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.blockEmailAddressFailure"), result.error as string);
    }

    markEmailAsRead();
    fetchEmailsData(selectedCategory.value);
}

const closeSeeMailModal = () => {
    isSeeMailModalVisible.value = false;
};

async function markEmailAsRead() {
    if (isMarking.value) return;
    isMarking.value = true;

    try {
        localEmail.value.read = true;
        readCount.value++;

        for (const category in emails.value) {
            for (const subCategory in emails.value[category]) {
                const index = emails.value[category][subCategory].findIndex(
                    (email) => email.id === props.email.id
                );
                if (index !== -1) {
                    emails.value[category][subCategory][index].read = true;
                    break;
                }
            }
        }

        const result = await putData("user/emails/update/", { 
            ids: [props.email.id], 
            action: "read" 
        });

        if (!result.success) {
            localEmail.value.read = false;
            readCount.value--;
            for (const category in emails.value) {
                for (const subCategory in emails.value[category]) {
                    const index = emails.value[category][subCategory].findIndex(
                        (email) => email.id === props.email.id
                    );
                    if (index !== -1) {
                        emails.value[category][subCategory][index].read = false;
                        break;
                    }
                }
            }
            throw new Error(result.error);
        }

        fetchCategoriesAndTotals?.();
        
    } catch (error) {
        displayPopup?.(
            "error",
            i18n.global.t("homepage.markEmailReadFailure"),
            error as string
        );
    } finally {
        isMarking.value = false;
    }
}

async function markEmailAsUnread() {
    if (isMarking.value) return;
    isMarking.value = true;

    try {
        localEmail.value.read = false;
        readCount.value--;

        for (const category in emails.value) {
            for (const subCategory in emails.value[category]) {
                const index = emails.value[category][subCategory].findIndex(
                    (email) => email.id === props.email.id
                );
                if (index !== -1) {
                    emails.value[category][subCategory][index].read = false;
                    break;
                }
            }
        }

        const result = await putData("user/emails/update/", { 
            ids: [props.email.id], 
            action: "unread" 
        });

        if (!result.success) {
            localEmail.value.read = true;
            readCount.value++;
            for (const category in emails.value) {
                for (const subCategory in emails.value[category]) {
                    const index = emails.value[category][subCategory].findIndex(
                        (email) => email.id === props.email.id
                    );
                    if (index !== -1) {
                        emails.value[category][subCategory][index].read = true;
                        break;
                    }
                }
            }
            throw new Error(result.error);
        }

        fetchCategoriesAndTotals?.();
        
    } catch (error) {
        displayPopup?.(
            "error",
            i18n.global.t("homepage.markEmailUnreadFailure"),
            error as string
        );
    } finally {
        isMarking.value = false;
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
    const result = await deleteData(`user/emails/delete_emails/`, { emailIds: [localEmail.value.id] });
    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.deleteEmailFailure"),
            result.error as string
        );
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

const toggleMenu = (event: MouseEvent) => {
    const button = (event.target as HTMLElement)?.closest('button')
    if (button) {
        const rect = button.getBoundingClientRect()
        menuPosition.value = {
            x: rect.left - 150,
            y: rect.bottom + window.scrollY
        }
    }
    if (!isMenuOpen.value) {
        isMenuOpen.value = true
    }
}

const handleButtonMouseLeave = () => {
    setTimeout(() => {
        if (!isHovered.value) {
            isMenuOpen.value = false
        }
    }, 100)
}

const handleMenuMouseLeave = () => {
    isHovered.value = false
    setTimeout(() => {
        if (!isHovered.value) {
            isMenuOpen.value = false
        }
    }, 100)
}

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
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.failedToFetchAttachment"),
            response.error as string
        );
    }
};
</script>
