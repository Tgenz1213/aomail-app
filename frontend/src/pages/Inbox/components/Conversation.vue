<template>
    <SeeMailModal
        v-if="isSeeMailOpen"
        :isOpen="isSeeMailOpen"
        :email="selectedEmail"
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
    <div class="flex-1 p-4 bg-white flex flex-col relative">
        <div class="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200">
            <div v-for="(message, index) in messages" :key="index" class="mb-4">
                <ChatBubble :message="message.textHtml" :isUser="message.isUser" :agentIcon="selectedAgent.icon_name" />
                <div v-if="message.buttonOptions" class="flex flex-col items-center">
                    <div class="flex-row space-x-5">
                        <button
                            v-for="(option, idx) in message.buttonOptions"
                            :key="idx"
                            @click="handleButtonClick(option, index)"
                            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none"
                        >
                            {{ option.value }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, Ref, ref } from "vue";
import ChatBubble from "@/global/components/Conversation/ChatBubble.vue";
import { Agent, Email, KeyValuePair, Message } from "@/global/types";
import { postData, getData, putData, deleteData } from "@/global/fetchData";
import { formatSentDate, formatSentTime } from "@/global/formatters";
import { i18n } from "@/global/preferences";
import router from "@/router/router";
import SeeMailModal from "@/global/components/SeeMailModal.vue";

const currentStep = ref("");

const selectedAgent =
    inject<Ref<Agent>>("selectedAgent") ||
    ref<Agent>({
        id: "",
        agent_name: i18n.global.t("agent.defaultAgent"),
        picture: "/assets/default-agent.png",
        ai_template: "",
        length: "",
        formality: "",
        icon_name: "default-agent.png",
    });

const messages = inject("messages") as Ref<Message[]>;
const waitForButtonClick = inject("waitForButtonClick") as Ref<boolean>;
const isSeeMailOpen = ref(false);
const selectedEmail = ref<Email | undefined>(undefined);
const emailList = ref<Email[]>([]);

const answerRequiredEmails = ref<Email[]>([]);
const mightRequireAnswerEmails = ref<Email[]>([]);
const missedImportantEmails = ref<Email[]>([]);

async function openSeeMailModal(id: number) {
    const emailFetched = await fetchEmailData(id);

    if (!emailFetched) {
        return;
    }
    selectedEmail.value = emailFetched;
    const result = await postData("user/get_email_content/", { id: id });
    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("conversation.errorMessages.failedToFetchEmailContent"),
            result.error as string
        );
        return;
    }

    selectedEmail.value.htmlContent = result.data.content;
    isSeeMailOpen.value = true;
}

const closeSeeMailModal = () => {
    isSeeMailOpen.value = false;
};

async function markEmailAsRead() {
    if (selectedEmail?.value) {
        selectedEmail.value.read = true;
    }

    const result = await putData("user/emails/update/", { ids: [selectedEmail?.value?.id], action: "read" });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailReadFailure"), result.error as string);
    }
}

async function markEmailAsUnread() {
    if (selectedEmail?.value) {
        selectedEmail.value.read = false;
    }

    const result = await putData("user/emails/update/", { ids: [selectedEmail?.value?.id], action: "unread" });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailUnreadFailure"), result.error as string);
    }
}

async function archiveEmail() {
    if (selectedEmail?.value) {
        selectedEmail.value.archive = true;
    }
    const result = await putData("user/emails/update/", {
        ids: [selectedEmail?.value?.id],
        action: "archive",
    });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("constants.popUpConstants.archiveEmailFailure"), result.error as string);
    }
}

async function unarchiveEmail() {
    if (selectedEmail?.value) {
        selectedEmail.value.archive = false;
    }

    const result = await putData("user/emails/update/", { ids: [selectedEmail?.value?.id], action: "unarchive" });
    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.unarchiveEmailFailure"),
            result.error as string
        );
    }
}

async function deleteEmail() {
    if (!selectedEmail.value) {
        return;
    }
    const emailId = selectedEmail?.value.id;
    const index = emailList.value.findIndex((email) => email.id === emailId);

    if (index !== -1) {
        emailList.value.splice(index, 1);
    } else {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.deleteEmailFailure"),
            i18n.global.t("constants.popUpConstants.errorMessages.emailIdNotFound")
        );
        return;
    }

    const result = await deleteData(`user/emails/delete_emails/`, { emailIds: [selectedEmail?.value.id] });
    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.deleteEmailFailure"),
            result.error as string
        );
    }
}

async function markEmailReplyLater() {
    if (!selectedEmail.value) {
        return;
    }
    selectedEmail.value.answerLater = true;

    let result = await putData("user/emails/update/", { ids: [selectedEmail?.value.id], action: "replyLater" });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailReplyLaterFailure"), result.error as string);
        return;
    }

    markEmailAsUnread();
}

async function markEmailAsUnreplyLater() {
    if (!selectedEmail.value) {
        return;
    }
    selectedEmail.value.answerLater = false;

    let result = await putData("user/emails/update/", { ids: [selectedEmail?.value.id], action: "unreplyLater" });
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.unmarkEmailReplyLaterFailure"), result.error as string);
    }
}

async function openAnswer() {
    if (!selectedEmail.value) {
        return;
    }
    const result = await getData(`get_mail_by_id?email_id=${selectedEmail?.value.providerId}`);
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("constants.popUpConstants.openReplyPageFailure"), result.error as string);
        return;
    }

    sessionStorage.setItem("subject", JSON.stringify(result.data.subject));
    sessionStorage.setItem("cc", result.data.cc);
    sessionStorage.setItem("bcc", result.data.bcc);
    sessionStorage.setItem("decodedData", JSON.stringify(result.data.decodedData));
    sessionStorage.setItem("emailUser", JSON.stringify(result.data.emailUser));
    sessionStorage.setItem("senderEmail", JSON.stringify(selectedEmail?.value.sender.email));
    sessionStorage.setItem("providerId", JSON.stringify(selectedEmail?.value.providerId));
    sessionStorage.setItem("shortSummary", JSON.stringify(selectedEmail?.value.shortSummary));
    sessionStorage.setItem("importance", JSON.stringify(selectedEmail?.value.priority));

    router.push({ name: "answer" });
}

async function transferEmail() {
    if (!selectedEmail.value) {
        return;
    }
    const result = await getData(`get_mail_by_id?email_id=${selectedEmail?.value.providerId}`);
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.transferEmailFailure"), result.error as string);
        return;
    }

    sessionStorage.setItem("subject", JSON.stringify(result.data.subject));
    sessionStorage.setItem("cc", result.data.cc);
    sessionStorage.setItem("decodedData", JSON.stringify(result.data.decodedData));
    sessionStorage.setItem("emailUser", JSON.stringify(result.data.emailUser));
    sessionStorage.setItem("senderEmail", JSON.stringify(selectedEmail?.value.sender.email));
    sessionStorage.setItem("providerId", JSON.stringify(selectedEmail?.value.providerId));
    sessionStorage.setItem("shortSummary", JSON.stringify(selectedEmail?.value.shortSummary));
    sessionStorage.setItem("date", JSON.stringify(result.data.date));

    router.push({ name: "transfer" });
}

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const displayUserMsg = inject<(message: string) => void>("displayUserMsg");
const waitForUserInput = inject<() => Promise<string>>("waitForUserInput");

const displayAIMsg = (message: string, options: KeyValuePair[] | undefined = undefined) => {
    messages.value.push({
        textHtml: message,
        isUser: false,
        buttonOptions: options,
    });
};

const handleButtonClick = async (option: KeyValuePair, index: number) => {
    waitForButtonClick.value = false;
    displayUserMsg?.(option.value);

    // Logic to handle sequential review steps
    switch (option.key) {
        case "mightRequireAnswer":
            currentStep.value = "mightRequireAnswer";
            displayNextEmails("mightRequireAnswerEmails");
            break;
        case "missedImportantEmailsNotRead":
            currentStep.value = "missedImportantEmailsNotRead";
            displayNextEmails("missedImportantEmails");
            break;
        case "finishReview":
            displayAIMsg(i18n.global.t("conversation.cleanInboxMessage"));
            break;
        default:
            console.error("Unknown option key:", option.key);
    }

    // Remove button options after clicking
    messages.value[index].buttonOptions = undefined;
};

function displayNextEmails(category: string) {
    const categoryMap: Record<string, Ref<Email[]>> = {
        mightRequireAnswerEmails: mightRequireAnswerEmails,
        missedImportantEmails: missedImportantEmails,
    };

    const emailsToDisplay = categoryMap[category]?.value || [];
    const messageIntro =
        emailsToDisplay.length > 0
            ? i18n.global.t("conversation.nextEmailsForReview")
            : i18n.global.t("conversation.noEmailsToReview");

    const emailListHtml = emailsToDisplay
        .map(
            (email) => `
            <li>
                <strong>${email.subject}</strong> from <em>${
                email.sender.name || email.sender.name
            }</em> on ${formatSentDate(email.sentDate)} ${formatSentTime(email.sentDate, email.sentTime)}
            </li>
        `
        )
        .join("");

    displayAIMsg(
        `
        <p><strong>${messageIntro}</strong></p>
        <ul>
            ${emailListHtml || `<li>${i18n.global.t("conversation.noEmailsToShow")}</li>`}
        </ul>
    `,
        [
            {
                key: "missedImportantEmailsNotRead",
                value: i18n.global.t("conversation.showMissedImportantEmails"),
            },
            {
                key: "finishReview",
                value: i18n.global.t("conversation.finishReviewingEmails"),
            },
        ]
    );
}

onMounted(async () => {
    await fetchAiEmails();
});

async function fetchAiEmails() {
    let result;
    result = await getData("user/answer_email_suggestion_ids/");

    answerRequiredEmails.value =
        (await postData("user/get_simple_email_data/", { ids: result.data.answerRequiredEmailIds })).data.emailsData ||
        [];

    mightRequireAnswerEmails.value =
        (await postData("user/get_simple_email_data/", { ids: result.data.mightRequireAnswerEmailIds })).data
            .emailsData || [];

    missedImportantEmails.value =
        (await postData("user/get_simple_email_data/", { ids: result.data.missedImportantEmailIds })).data.emailsData ||
        [];

    // Determine the highest-priority category to display
    let emailsToDisplay: Email[] = [];
    let messageIntro = "";
    let addButtons = false;

    if (answerRequiredEmails.value.length > 0) {
        emailsToDisplay = answerRequiredEmails.value;
        messageIntro = i18n.global.t("conversation.emailsToAnswer");
        addButtons = true; // Add buttons for "requiring an answer" emails
    } else if (mightRequireAnswerEmails.value.length > 0) {
        emailsToDisplay = mightRequireAnswerEmails.value;
        messageIntro = i18n.global.t("conversation.emailsThatMightRequireAnswer");
    } else if (missedImportantEmails.value.length > 0) {
        emailsToDisplay = missedImportantEmails.value;
        messageIntro = i18n.global.t("conversation.missedImportantEmails");
    } else {
        messageIntro = i18n.global.t("conversation.noPendingEmails");
    }

    // Generate the email list HTML
    const emailListHtml = emailsToDisplay
        .map(
            (email) => `
        <li>
            <strong>${email.subject}</strong> from <em>${
                email.sender.name || email.sender.name
            }</em> on ${formatSentDate(email.sentDate)} ${formatSentTime(email.sentDate, email.sentTime)}
            ${
                addButtons
                    ? `<button type="button" id="responseKeywordButton${email.id}"
                        class="border border-black text-black rounded-full px-2 py-1 hover:bg-gray-200 focus:outline-none">
                        ${i18n.global.t("conversation.viewEmail")}
                    </button>`
                    : ""
            }
        </li>
    `
        )
        .join("");

    // Display the emails to the user
    displayAIMsg(
        `
        <p><strong>${messageIntro}</strong></p>
        <ul>
            ${emailListHtml || `<li>${i18n.global.t("conversation.noEmailsToShow")}</li>`}
        </ul>
    `,
        [
            {
                key: "mightRequireAnswer",
                value: i18n.global.t("conversation.showMightRequireAnswerEmails"),
            },
            {
                key: "missedImportantEmailsNotRead",
                value: i18n.global.t("conversation.showMissedImportantEmails"),
            },
        ]
    );

    // Attach event listeners for "requiring answer" emails
    if (addButtons) {
        setTimeout(() => {
            emailsToDisplay.forEach((email) => {
                const keywordButton = document.getElementById(`responseKeywordButton${email.id}`);
                if (keywordButton && typeof email.id === "number") {
                    keywordButton.addEventListener("click", () => {
                        openSeeMailModal(email.id as number);
                    });
                }
            });
        }, 0);
    }
}

async function fetchEmailData(id: number): Promise<Email | undefined> {
    const result = await postData("user/get_simple_email_data/", { ids: [id] });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("conversation.errorMessages.failedToFetchEmailData"),
            result.error as string
        );
        return;
    }
    return result.data.emailsData[0];
}
</script>
