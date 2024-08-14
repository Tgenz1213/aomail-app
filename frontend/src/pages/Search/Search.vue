<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
    />
    <SeeMailModal
        :isOpen="isModalSeeOpen"
        :email="selectedEmail"
        :category="category"
        :htmlContent="htmlContent"
        @closeSeeModal="closeSeeModal"
        @openAnswer="openAnswer"
        @openRuleEditor="openRuleEditor"
        @openNewRule="openNewRule"
        @markEmailAsRead="markEmailAsRead"
        @markEmailReplyLater="markEmailReplyLater"
        @transferEmail="transferEmail"
    />
    <div class="flex flex-col justify-center items-center h-screen">
        <div class="flex h-full w-full">
            <div class="w-[90px] bg-white ring-1 shadow-sm ring-black ring-opacity-5 2xl:w-[100px]">
                <NavBarSmall />
            </div>
            <div
                id="firstMainColumn"
                class="flex flex-col bg-gray-50 lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[700px]"
            >
                <div class="flex items-center justify-center h-[65px] 2xl:h-[80px]">
                    <div class="flex gap-x-3 items-center">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1"
                            stroke="currentColor"
                            class="w-6 h-6 2xl:w-7 2xl:h-7"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z"
                            />
                        </svg>
                        <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500">
                            {{ $t("constants.aiAssistant") }}
                        </h1>
                    </div>
                </div>
                <div class="flex flex-1 flex-col divide-y overflow-y-auto">
                    <div class="overflow-y-auto flex-1" style="margin-right: 2px" ref="scrollableDiv">
                        <div class="px-10 py-4 2xl:px-13.5 2xl:py-6">
                            <div class="flex-grow">
                                <div id="AIContainer"></div>
                            </div>
                        </div>
                    </div>
                    <div class="flex flex-col h-[22vh] 2xl:h-[23vh]">
                        <textarea
                            id="dynamicTextarea"
                            @input="adjustHeight"
                            v-model="textareaValue"
                            class="overflow-y-hidden pt-4 pl-6 flex-1 w-full border-transparent bg-transparent text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 focus:border-transparent focus:bg-transparent focus:ring-0 2xl:pt-5 2xl:pl-7 2xl:text-base"
                            placeholder="Instruction"
                        ></textarea>
                        <div v-if="stepcontainer == 0" class="flex justify-end m-3 2xl:m-5">
                            <div class="flex space-x-2 items-center">
                                <div class="flex items-center">
                                    <button
                                        type="button"
                                        @click="handleAIClick"
                                        class="h-[38px] 2xl:h-[46px] w-[80px] 2xl:w-[100px] rounded-md bg-gray-700 px-2 text-sm 2xl:text-base text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                                    >
                                        Envoyer
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div v-else class="flex justify-end m-3 2xl:m-5">
                            <button
                                type="button"
                                @click="handleAIClick"
                                class="2xl:w-[100px] w-[80px] rounded-md bg-gray-700 px-5.5 py-2.5 2xl:px-6.5 2xl:py-3 2xl:text-base text-sm text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                            >
                                Envoyer
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div
                id="secondMainColumn"
                class="flex flex-col bg-white lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[700px] overflow-y-auto"
            >
                <div class="flex items-center h-[65px] justify-center lg:py-5 2xl:h-[80px] min-h-6">
                    <div class="flex gap-x-3 items-center">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1"
                            stroke="currentColor"
                            class="w-6 h-6 2xl:w-7 2xl:h-7"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672ZM12 2.25V4.5m5.834.166-1.591 1.591M20.25 10.5H18M7.757 14.743l-1.59 1.59M6 10.5H3.75m4.007-4.243-1.59-1.59"
                            />
                        </svg>
                        <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500">
                            {{ $t("constants.manualSearch") }}
                        </h1>
                    </div>
                </div>
                <div class="flex-1 flex flex-col w-full px-6 pt-2 mb-4">
                    <SearchMenu />
                    <div class="flex-1 flex flex-col py-2" id="emailList">
                        <div class="h-full overflow-y-auto">
                            <template v-if="sortedEmailList.length > 0">
                                <ul class="space-y-4 pr-4">
                                    <template v-for="(email, index) in sortedEmailList" :key="email.id">
                                        <li
                                            class="group flex justify-between items-center py-2 email-item"
                                            @click="toggleHiddenParagraph(index)"
                                        >
                                            <div class="flex flex-col justify-center">
                                                <span class="font-semibold text-sm leading-6">
                                                    {{ email.sender.name }}
                                                    - {{ email.sender.email }}
                                                    <span class="font-normal ml-2 text-gray-600 text-xs">
                                                        {{ email.sentDate }}
                                                    </span>
                                                </span>
                                                <span class="text-sm gray-600">
                                                    {{ email.subject }} - {{ email.oneLineSummary }}
                                                </span>
                                                <div v-if="showSummary" class="py-1">
                                                    <p class="text-xs">{{ email.shortSummary }}</p>
                                                </div>
                                                <div class="mt-1 flex space-x-2">
                                                    <span
                                                        v-if="email.priority === 'important'"
                                                        class="inline-flex items-center rounded-md bg-orange-50 px-2 py-1 text-xs font-medium text-orange-700 ring-1 ring-inset ring-orange-600/10"
                                                    >
                                                        Important
                                                    </span>
                                                    <span
                                                        v-else-if="email.priority === 'informative'"
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
                                                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10"
                                                    >
                                                        {{ email.category }}
                                                    </span>

                                                    <span
                                                        v-if="email.read"
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
                                                        Lu
                                                    </span>
                                                    <span
                                                        v-bind:class="{
                                                            'hidden group-hover:block px-1.5 text-white shadow rounded-xl inline-flex': true,
                                                            'bg-orange-300': email.priority === 'important',
                                                            'bg-blue-300': email.priority === 'informative',
                                                            'bg-gray-300':
                                                                email.priority !== 'important' &&
                                                                email.priority !== 'informative',
                                                        }"
                                                    >
                                                        <div class="flex gap-x-1 items-center justify-center h-full">
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
                                                            <p class="text-xs">
                                                                {{ $t("constants.userActions.clickToSeeTheSummary") }}
                                                            </p>
                                                        </div>
                                                    </span>
                                                </div>
                                            </div>
                                            <span class="isolate inline-flex items-center rounded-2xl">
                                                <div class="relative group">
                                                    <button
                                                        @click.stop="openMail(email.id)"
                                                        class="border border-black text-black rounded-full px-2 py-1 hover:bg-gray-200 focus:outline-none focus:border-gray-500 flex items-center gap-x-2 justify-center"
                                                    >
                                                        <EyeIcon class="w-5 h-5" />
                                                        Voir
                                                    </button>
                                                </div>
                                            </span>
                                        </li>
                                        <li v-if="index < sortedEmailList.length - 1" class="flex relative pt-2">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="w-full border-t border-gray-300"></div>
                                            </div>
                                        </li>
                                    </template>
                                </ul>
                            </template>
                            <template v-else>
                                <div
                                    class="flex flex-col items-center justify-center h-full rounded-lg border-2 border-dashed border-gray-300"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        fill="none"
                                        viewBox="0 0 24 24"
                                        stroke-width="1"
                                        stroke="currentColor"
                                        class="w-12 h-12 mx-auto text-gray-400"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            d="M15.182 16.318A4.486 4.486 0 0012.016 15a4.486 4.486 0 00-3.198 1.318M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z"
                                        />
                                    </svg>
                                    <span class="mt-2 block text-sm font-semibold text-gray-900">
                                        {{ $t("searchPage.noResults") }}
                                    </span>
                                </div>
                            </template>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted, provide } from "vue";
import SeeMailModal from "@/global/components/SeeMailModal.vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { EyeIcon } from "@heroicons/vue/24/outline";
import { IMPORTANT, INFORMATIVE, USELESS } from "@/global/const";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import router from "@/router/router";
import { Contact, Email, Recipient } from "@/global/types";
import { i18n } from "@/global/preferences";
import { getData, postData } from "@/global/fetchData";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import SearchMenu from "./components/SearchMenu.vue";
import { AttachmentType } from "./utils/types";

const people = ref<Recipient[]>([]);
const selectedPeople = ref<Recipient[]>([]);

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

const AIContainer = ref<HTMLElement | null>(null);
let counter_display = 0;
let stepcontainer = 0;
const scrollableDiv = ref<HTMLDivElement | null>(null);

let isAIWriting = ref(false);
let isEmailhere = ref(false);
const textareaValue = ref("");
let lockEmailsAccess = ref(false);

const startDate = ref("");
const selectedInterval = ref("");
const selectedSearchIn = ref(null);
const selectedPerson = ref<Recipient[]>([]);
const fromSelectedPerson = ref<Recipient[]>([]);
const selectedRecipients = ref<Recipient[]>([]);
const attachmentsSelected = ref<AttachmentType[]>([]);

let emailsLinked = ref("");

let isModalSeeOpen = ref(false);
let selectedEmail = ref<Email>();

const contacts: Contact[] = [];
const queryGetContacts = ref("");
const emailList = ref<Email[]>([]);

const aiIcon =
    '<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" /> ';

const sortedEmailList = computed(() => {
    const priorityOrder: Record<string, number> = {
        [IMPORTANT]: 0,
        [INFORMATIVE]: 1,
        [USELESS]: 2,
    };

    return [...emailList.value].sort((a, b) => {
        return priorityOrder[a.priority] - priorityOrder[b.priority];
    });
});

onMounted(() => {
    checkLoginStatus();
    document.addEventListener("click", closeDropdown);
});

onMounted(async () => {
    fetchEmailLinked();
    fetchContacts();

    AIContainer.value = document.getElementById("AIContainer");

    await askQueryUser();
});

const filteredPeople = computed(() => {
    if (!contacts || queryGetContacts.value === "") {
        return contacts || [];
    }
    return contacts.filter((person) => {
        const username = person?.username || "";
        return username.toLowerCase().includes(queryGetContacts.value.toLowerCase());
    });
});

provide("displayPopup", displayPopup);
provide("loading", loading);
provide("scrollToBottom", scrollToBottom);
provide("fetchEmailDetails", fetchEmailDetails);
provide("hideLoading", hideLoading);
provide("displayMessage", displayMessage);
provide("aiIcon", aiIcon);
provide("filteredPeople", filteredPeople);
provide("people", people);
provide("selectedPeople", selectedPeople);
provide("attachmentsSelected", attachmentsSelected);
provide("startDate", startDate);
provide("selectedInterval", selectedInterval);
provide("selectedRecipients", selectedRecipients);
provide("fromSelectedPerson", fromSelectedPerson);
provide("selectedPerson", selectedPerson);
provide("selectedSearchIn", selectedSearchIn);

async function scrollToBottom() {
    await nextTick();
    const element = scrollableDiv.value;
    if (element) {
        element.scrollTop = element.scrollHeight;
    }
}

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

async function openMail(emailId: number) {
    const result = await postData("user/get_email_content/", {
        id: emailId,
    });

    if (!result.success) {
        displayPopup("error", "Failed to open the email", result.error as string);
    }

    // todo: find the category and update the variable category
    const emailIndex = emailList.value.findIndex((email: Email) => email.id === emailId);

    if (emailIndex !== -1) {
        emailList.value[emailIndex] = {
            ...emailList.value[emailIndex],
            htmlContent: result.data.htmlContent,
            category: "",
        };

        selectedEmail.value = emailList.value[emailIndex];
        isModalSeeOpen.value = true;
    }
}

function closeSeeModal() {
    isModalSeeOpen.value = false;
}

async function openAnswer(email: Email) {
    const result = await getData(`api/get_mail_by_id?email_id=${email.providerId}`);

    if (!result.success) {
        displayPopup("error", i18n.global.t("constants.popUpConstants.openReplyPageFailure"), result.error as string);
        return;
    }

    sessionStorage.setItem("subject", JSON.stringify(result.data.email.subject));
    sessionStorage.setItem("cc", result.data.email.cc);
    sessionStorage.setItem("bcc", result.data.email.bcc);
    sessionStorage.setItem("decoded_data", JSON.stringify(result.data.email.decoded_data));
    sessionStorage.setItem("email", JSON.stringify(email.sender.email));
    sessionStorage.setItem("providerId", JSON.stringify(email.providerId));
    sessionStorage.setItem("shortSummary", JSON.stringify(email.shortSummary));
    // sessionStorage.setItem("emailReceiver", data.email.email_receiver);

    router.push({
        name: "answer",
    });
}

function openRuleEditor(ruleId: number) {
    router.push({ name: "rules", query: { idRule: ruleId, editRule: "true" } });
}

function openNewRule(ruleName: string, ruleEmail: string) {
    router.push({ name: "rules", query: { ruleName: ruleName, ruleEmail: ruleEmail, editRule: "false" } });
}

async function markEmailAsRead(emailId: number) {
    lockEmailsAccess.value = true;
    const result = await postData(`user/emails/${emailId}/mark_read/`, {});

    if (!result.success) {
        displayPopup("error", i18n.global.t("homepage.markEmailReadFailure"), result.error as string);
    }
}

async function markEmailReplyLater(emailId: number) {
    lockEmailsAccess.value = true;

    const result = await postData(`user/emails/${emailId}/mark_reply_later/`, {});

    if (!result.success) {
        displayPopup("error", i18n.global.t("homepage.markEmailReplyLaterFailure"), result.error as string);
    }
}

async function transferEmail(email: Email) {
    const result = await getData(`api/get_mail_by_id?email_id=${email.providerId}`);

    if (!result.success) {
        displayPopup("error", i18n.global.t("homepage.transferEmailFailure"), result.error as string);
        return;
    }

    sessionStorage.setItem("subject", JSON.stringify(result.data.email.subject));
    sessionStorage.setItem("cc", result.data.email.cc);
    sessionStorage.setItem("bcc", result.data.email.bcc);
    sessionStorage.setItem("decoded_data", JSON.stringify(result.data.email.decoded_data));
    // sessionStorage.setItem("emailReceiver", result.data.email.email_receiver);
    sessionStorage.setItem("date", JSON.stringify(result.data.email.date));
    sessionStorage.setItem("providerId", JSON.stringify(email.providerId));
    sessionStorage.setItem("email", JSON.stringify(email.sender.email));

    router.push({
        name: "transfer",
    });
}

const isOpen = ref(false);

const closeDropdown = (event: MouseEvent) => {
    const target = event.target as HTMLElement;
    if (isOpen.value && !target.closest(".dropdown-container")) {
        isOpen.value = false;
    }
};

const checkLoginStatus = () => {
    const emailList = document.getElementById("emailList");
    if (!emailList) {
        return;
    }
    const hasEmails = emailList.getElementsByClassName("email-item").length > 0;
    isEmailhere.value = hasEmails;
};

async function fetchContacts() {
    const result = await getData(`user/contacts/`);

    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.contactFetchError"),
            result.error as string
        );
        return;
    }

    contacts.push(...result.data);
}

function toggleHiddenParagraph(index: any) {
    // fixable if email displayed is scoped alone => create a var cosnt showSummary = ref(false)
    // sortedEmailList.value[index].showSummary = !sortedEmailList.value[index].showSummary;
}

async function fetchEmailLinked() {
    const result = await getData(`user/emails_linked/`);

    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailLinkedFetchError"),
            result.error as string
        );
        return;
    }

    emailsLinked.value = result.data;
}

async function handleAIClick() {
    if (isAIWriting.value) {
        return;
    }
    isAIWriting.value = true;

    loading();
    scrollToBottom();

    textareaValue.value = "";

    const result = await postData(`api/search_tree_knowledge/`, {
        question: textareaValue.value,
    });

    let message = "";
    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("searchPage.popUpConstants.successMessages.smartSearchError"),
            result.error as string
        );
    } else if (result.data.message) {
        message = i18n.global.t("searchPage.notEnoughDataToAnswer");
    } else {
        const { sure, answer, ids } = result.data.answer;
        message = answer;

        // Limit to 25 results
        const limitedEmails = ids.slice(0, 25);
        const emailDetails = await fetchEmailDetails(limitedEmails);
        // emailList.value = Object.entries(emailDetails.data).flatMap(([category, priorities]) =>
        //     Object.entries(priorities).flatMap(([priority, emails]) =>
        //         emails.map((email) => ({
        //             ...email,
        //             category: category,
        //             priority: priority,
        //         }))
        //     )
        // );
    }

    await displayMessage(message, aiIcon);
    hideLoading();
    isAIWriting.value = false;
}

async function fetchEmailDetails(emailIds: number[]) {
    const result = await postData(`user/get_emails_data/`, {
        ids: emailIds,
    });

    if (!result.success) {
        displayPopup("error", "Failed to fetch email details", result.error as string);
        return [];
    }
    return result;
}

async function displayMessage(message: string, aiIcon: string) {
    if (!AIContainer.value) return;

    isAIWriting.value = true;
    const messageHTML = `
        <div class="flex pb-12">
          <div class="mr-4 flex">
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                ${aiIcon}
              </svg>
            </span>   
          </div>
          <div>
            <p ref="animatedText${counter_display}"></p>
          </div>
        </div>
      `;
    AIContainer.value.innerHTML += messageHTML;
    const animatedParagraph = document.querySelector(`p[ref="animatedText${counter_display}"]`);
    counter_display += 1;
    await animateText(message, animatedParagraph);
    scrollToBottom();
}

async function waitForAIWriting() {
    while (isAIWriting.value) {
        await new Promise((resolve) => setTimeout(resolve, 500));
    }
}

async function animateText(text: string, target: Element | null) {
    let characters = text.split("");
    let currentIndex = 0;
    const interval = setInterval(() => {
        if (currentIndex < characters.length) {
            if (!target) return;
            target.textContent += characters[currentIndex];
            currentIndex++;
        } else {
            clearInterval(interval);
            isAIWriting.value = false;
        }
    }, 30);
}

async function askQueryUser() {
    const message = i18n.global.t("searchPage.searchInfoPrompt");
    const aiIcon =
        '<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />';
    await displayMessage(message, aiIcon);

    await waitForAIWriting();
}

const adjustHeight = (event: { target: any }) => {
    const textarea = event.target;
    const maxHeight = 250;

    textarea.style.height = "auto";

    if (textarea.scrollHeight > maxHeight) {
        textarea.style.height = `${maxHeight}px`;
        textarea.style.overflowY = "auto";
    } else {
        textarea.style.height = `${textarea.scrollHeight}px`;
        textarea.style.overflowY = "hidden";
    }
};

function loading() {
    if (!AIContainer.value) return;

    const messageHTML = `
        <div id="dynamicLoadingIndicator" class="pb-12">
          <div class="flex">
              <div class="mr-4">
                  <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900">
                      <span class="text-lg font-medium leading-none text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15a4.5 4.5 0 0 0 4.5 4.5H18a3.75 3.75 0 0 0 1.332-7.257 3 3 0 0 0-3.758-3.848 5.25 5.25 0 0 0-10.233 2.33A4.502 4.502 0 0 0 2.25 15Z" />
                        </svg>
                      </span>
                  </span>
              </div>
              <div>
                <div class="loading-spinner"></div>
              </div>
          </div>
        </div>
      `;

    AIContainer.value.innerHTML += messageHTML;
}

function hideLoading() {
    const loadingElement = document.getElementById("dynamicLoadingIndicator");
    if (loadingElement) {
        loadingElement.remove();
    }
}
</script>
