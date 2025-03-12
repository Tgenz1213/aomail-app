<template>
    <SeeMailModal
        v-if="isSeeMailOpen"
        :isOpen="isSeeMailOpen"
        :email="localEmail"
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
    <ApiEmailModal
        v-if="isApiEmailOpen"
        :isOpen="isApiEmailOpen"
        :email="localEmail"
        @closeModal="closeApiEmailModal"
    />
    <li class="py-4 hover:bg-gray-50 transition-colors duration-150" @click="toggleShowShortSummary()">
        <div class="group flex px-2 justify-between items-center email-item">
            <div class="flex flex-col justify-center">
                <span class="font-semibold text-sm leading-6">
                    {{ localEmail.sender.name }}
                    - {{ localEmail.sender.email }}
                    <span class="font-normal ml-2 text-gray-600 text-xs">
                        {{ formatSentDateAndTime(localEmail.sentDate, localEmail.sentTime) }}
                    </span>
                </span>
                <span class="text-sm gray-600">{{ localEmail.subject }} - {{ localEmail.oneLineSummary }}</span>
                <div v-if="showShortSummary" class="py-1">
                    <p class="text-xs">{{ localEmail.shortSummary }}</p>
                </div>
                <div class="mt-1 flex space-x-2">
                    <div v-if="localEmail.priority">
                        <span
                            v-if="localEmail.priority === IMPORTANT"
                            class="inline-flex items-center rounded-md bg-orange-50 px-2 py-1 text-xs font-medium text-orange-700 ring-1 ring-inset ring-orange-600/10"
                        >
                            {{ $t("constants.ruleModalConstants.important") }}
                        </span>
                        <span
                            v-else-if="localEmail.priority === INFORMATIVE"
                            class="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10"
                        >
                            {{ $t("constants.ruleModalConstants.informative") }}
                        </span>
                        <span
                            v-else
                            class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10"
                        >
                            {{ $t("constants.ruleModalConstants.useless") }}
                        </span>
                    </div>
                    <span
                        v-if="localEmail.category"
                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10"
                    >
                        {{ localEmail.category }}
                    </span>
                    <span
                        v-if="localEmail.read"
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
                            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                        </svg>
                        {{ $t("searchPage.searchIn.read") }}
                    </span>
                    <span
                        v-if="localEmail.shortSummary"
                        v-bind:class="{
                            'hidden group-hover:block px-1.5 shadow rounded-md inline-flex ring-1 ring-inset': true,
                            'bg-orange-50 text-orange-700 ring-orange-600/10': localEmail.priority === IMPORTANT,
                            'bg-blue-50 text-blue-700 ring-blue-700/10': localEmail.priority === INFORMATIVE,
                            'bg-gray-50 text-gray-600 ring-gray-500/10':
                                localEmail.priority !== IMPORTANT && localEmail.priority !== INFORMATIVE,
                        }"
                    >
                        <div class="flex gap-x-1 items-center justify-center h-full">
                            <SparklesIcon class="w-4 h-4"></SparklesIcon>
                            <p class="text-xs">
                                {{ $t("constants.userActions.clickToSeeTheSummary") }}
                            </p>
                        </div>
                    </span>
                </div>
            </div>
            <span class="isolate inline-flex items-center rounded-2xl pr-3">
                <div class="relative group">
                    <button
                        @click.stop="openSeeMailModal()"
                        class="hidden group-hover:flex text-gray-600 hover:text-gray-800 rounded-full p-2.5 hover:bg-gray-200/80 focus:outline-none items-center justify-center"
                    >
                        <EyeIcon class="w-5 h-5" />
                    </button>
                </div>
            </span>
        </div>
    </li>
</template>

<script setup lang="ts">
import { deleteData, getData, postData, putData } from "@/global/fetchData";
import { inject, Ref, ref, watch } from "vue";
import { EyeIcon, SparklesIcon } from "@heroicons/vue/24/outline";
import { Email } from "@/global/types";
import SeeMailModal from "@/global/components/SeeMailModal.vue";
import router from "@/router/router";
import { i18n } from "@/global/preferences";
import { formatSentDateAndTime } from "@/global/formatters";
import { INFORMATIVE, IMPORTANT, AOMAIL_SEARCH_KEY } from "@/global/const";
import ApiEmailModal from "./ApiEmailModal.vue";

const props = defineProps<{
    email: Email;
    searchMode: string;
    provider_email?: string;
}>();

const showShortSummary = ref(false);
const isSeeMailOpen = ref(false);
const isApiEmailOpen = ref(false);
const localEmail = ref({ ...props.email });
const emailList = inject<Ref<Email[]>>("emailList") || ref([]);
const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

watch(
    () => props.email,
    (newEmail) => {
        localEmail.value = { ...newEmail };
    },
    { deep: true }
);

function toggleShowShortSummary() {
    showShortSummary.value = !showShortSummary.value;
}

function closeSeeMailModal() {
    isSeeMailOpen.value = false;
}

function closeApiEmailModal() {
    isApiEmailOpen.value = false;
}

async function openSeeMailModal() {
    console.log(props.searchMode);
    if (props.searchMode === AOMAIL_SEARCH_KEY) {
        const result = await postData("user/get_email_content/", { id: props.email.id });
        if (!result.success) {
            displayPopup?.("error", i18n.global.t("constants.popUpConstants.errorMessages.noHtmlContent"), result.error as string);
            return;
        }
        localEmail.value.htmlContent = result.data.content;
        isSeeMailOpen.value = true;
    } else {
        console.log(props.email);
        const result = await getData(
            `user/emails/content/?email_id=${props.email.providerId}&provider_email=${props.provider_email}`
        );
        console.log(result);
        if (!result.success) {
            displayPopup?.("error", i18n.global.t("constants.popUpConstants.errorMessages.noHtmlContent"), result.error as string);
            return;
        }
        localEmail.value.htmlContent = result.data.htmlContent;
        isApiEmailOpen.value = true;
    }
}

async function markEmailAsRead() {
    localEmail.value.read = true;

    const result = await putData("user/emails/update/", { ids: [localEmail.value.id], action: "read" });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailReadFailure"), result.error as string);
    }
}

async function markEmailAsUnread() {
    localEmail.value.read = false;

    const result = await putData("user/emails/update/", { ids: [localEmail.value.id], action: "unread" });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailUnreadFailure"), result.error as string);
    }
}

async function archiveEmail() {
    localEmail.value.archive = true;
    localEmail.value.read = true;

    const result = await putData("user/emails/update/", {
        ids: [localEmail.value.id],
        action: "archive",
    });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("constants.popUpConstants.archiveEmailFailure"), result.error as string);
    }
}

async function unarchiveEmail() {
    localEmail.value.archive = false;

    const result = await putData("user/emails/update/", { ids: [localEmail.value.id], action: "unarchive" });
    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.unarchiveEmailFailure"),
            result.error as string
        );
    }
}

async function deleteEmail() {
    const emailId = localEmail.value.id;
    const index = emailList.value.findIndex((email) => email.id === emailId);

    if (index !== -1) {
        emailList.value.splice(index, 1);
    } else {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.deleteEmailFailure"),
            i18n.global.t("constants.popUpConstants.errorMessages.emailIdNotFound")
        );
        return;
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

async function markEmailReplyLater() {
    localEmail.value.answerLater = true;

    let result = await putData("user/emails/update/", { ids: [localEmail.value.id], action: "replyLater" });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailReplyLaterFailure"), result.error as string);
        return;
    }

    markEmailAsUnread();
}

async function markEmailAsUnreplyLater() {
    localEmail.value.answerLater = false;

    let result = await putData("user/emails/update/", { ids: [localEmail.value.id], action: "unreplyLater" });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.unmarkEmailReplyLaterFailure"), result.error as string);
    }
}

async function openAnswer() {
    const result = await getData(`get_mail_by_id?email_id=${localEmail.value.providerId}`);
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("constants.popUpConstants.openReplyPageFailure"), result.error as string);
        return;
    }

    sessionStorage.setItem("subject", JSON.stringify(result.data.subject));
    sessionStorage.setItem("cc", result.data.cc);
    sessionStorage.setItem("bcc", result.data.bcc);
    sessionStorage.setItem("decodedData", JSON.stringify(result.data.decodedData));
    sessionStorage.setItem("emailUser", JSON.stringify(result.data.emailUser));
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
    sessionStorage.setItem("decodedData", JSON.stringify(result.data.decodedData));
    sessionStorage.setItem("emailUser", JSON.stringify(result.data.emailUser));
    sessionStorage.setItem("senderEmail", JSON.stringify(localEmail.value.sender.email));
    sessionStorage.setItem("providerId", JSON.stringify(localEmail.value.providerId));
    sessionStorage.setItem("shortSummary", JSON.stringify(localEmail.value.shortSummary));
    sessionStorage.setItem("date", JSON.stringify(result.data.date));

    router.push({ name: "transfer" });
}
</script>
