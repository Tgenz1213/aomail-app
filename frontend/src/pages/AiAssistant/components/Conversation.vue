<template>
    <SeeMailModal
        v-if="isSeeMailOpen"
        :isOpen="isSeeMailOpen"
        :email="selectedEmail"
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
    <div class="flex-1 p-4 bg-white flex flex-col relative">
        <div class="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200">
            <div v-for="(message, index) in messages" :key="index" class="mb-4">
                <ChatBubble :message="message.textHtml" :isUser="message.isUser" />
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
import { Email, KeyValuePair, Message } from "@/global/types";
import { postData, getData, putData, deleteData } from "@/global/fetchData";
import { formatSentDate, formatSentTime } from "@/global/formatters";
import { i18n } from "@/global/preferences";
import router from "@/router/router";
import SeeMailModal from "@/global/components/SeeMailModal.vue";

interface Reminder {
    id: number;
    receivedDate: string;
    receivedTime: string;
    subject: string;
    sender: string;
    importance: string;
}

const currentStep = ref("requiringAnswer");

const messages = inject("messages") as Ref<Message[]>;
const waitForButtonClick = inject("waitForButtonClick") as Ref<boolean>;
const isSeeMailOpen = ref(false);
const selectedEmail = ref<Email | undefined>(undefined);
const emailList = ref<Email[]>([]);

const emailsRequiringAnswer = ref<Reminder[]>([]);
const emailsMightRequireAnswer = ref<Reminder[]>([]);
const importantEmails = ref<Reminder[]>([]);

async function openSeeMailModal(id: number) {
    const emailFetched = await fetchEmailData(id);

    if (!emailFetched) {
        return;
    }
    selectedEmail.value = emailFetched;
    const result = await postData("user/get_email_content/", { id: id });
    if (!result.success) {
        displayPopup?.("error", "Failed to fetch email content", result.error as string);
        return;
    }

    selectedEmail.value.htmlContent = result.data.content;
    isSeeMailOpen.value = true;
}

const closeSeeMailModal = () => {
    isSeeMailOpen.value = false;
};

function openRule() {
    if (selectedEmail?.value?.rule?.hasRule) {
        openRuleEditor();
    } else {
        openNewRule();
    }
}

function openRuleEditor() {
    router.push({ name: "rules", query: { idRule: selectedEmail?.value?.rule.ruleId, editRule: "true" } });
}

function openNewRule() {
    router.push({
        name: "rules",
        query: {
            ruleName: selectedEmail?.value?.sender.name,
            ruleEmail: selectedEmail?.value?.sender.email,
            editRule: "false",
        },
    });
}

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
        displayPopup?.("error", i18n.global.t("constants.popUpConstants.deleteEmailFailure"), "Email id not found");
        return;
    }

    const result = await deleteData(`user/emails/${selectedEmail?.value.id}/delete/`);
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("constants.popUpConstants.deleteEmailFailure"), result.error as string);
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
const displayUserMsg = inject<(message: string) => void>("displayUserMsg")!;
const waitForUserInput = inject<() => Promise<string>>("waitForUserInput")!;

const displayAIMsg = (message: string, options: KeyValuePair[] | undefined = undefined) => {
    messages.value.push({
        textHtml: message,
        isUser: false,
        buttonOptions: options,
    });
};

const handleButtonClick = async (option: KeyValuePair, index: number) => {
    waitForButtonClick.value = false;
    displayUserMsg(option.value);

    // Logic to handle sequential review steps
    switch (option.key) {
        case "mightRequireAnswer":
            currentStep.value = "mightRequireAnswer";
            displayNextEmails("emailsMightRequireAnswer");
            break;
        case "importantEmailsNotRead":
            currentStep.value = "importantEmailsNotRead";
            displayNextEmails("importantEmails");
            break;
        case "finishReview":
            displayAIMsg("Great! You've reviewed all emails. Enjoy your clean inbox");
            break;
        default:
            console.error("Unknown option key:", option.key);
    }

    // Remove button options after clicking
    messages.value[index].buttonOptions = undefined;
};

function displayNextEmails(category: string) {
    const categoryMap: Record<string, Ref<Reminder[]>> = {
        emailsMightRequireAnswer: emailsMightRequireAnswer,
        importantEmails: importantEmails,
    };

    const emailsToDisplay = categoryMap[category]?.value || [];
    const messageIntro =
        emailsToDisplay.length > 0 ? "Here are the next emails for review:" : "No emails to review in this category.";

    const emailListHtml = emailsToDisplay
        .map(
            (email) => `
            <li>
                <strong>${email.subject}</strong> from <em>${email.sender}</em> on ${formatSentDate(
                email.receivedDate
            )} ${formatSentTime(email.receivedDate, email.receivedTime)}
            </li>
        `
        )
        .join("");

    displayAIMsg(
        `
        <p><strong>${messageIntro}</strong></p>
        <ul>
            ${emailListHtml || "<li>No emails to show.</li>"}
        </ul>
    `,
        [
            {
                key: "importantEmailsNotRead",
                value: "Show missed important emails",
            },
            {
                key: "finishReview",
                value: "Finish reviewing emails",
            },
        ]
    );
}

onMounted(async () => {
    await fetchAiReminders();
});

async function fetchAiReminders() {
    // Simulating the fetching of email reminders
    const fakeEmailsRequiringAnswer: Reminder[] = [
        {
            id: 188,
            receivedDate: "2025-01-10",
            receivedTime: "19:03",
            subject: "Follow-up on project status",
            sender: "manager@company.com",
            importance: "Important",
        },
        {
            id: 189,
            receivedDate: "2025-01-12",
            receivedTime: "19:03",
            subject: "Request for documents",
            sender: "client@business.com",
            importance: "Important",
        },
    ];

    const fakeEmailsMightRequireAnswer: Reminder[] = [
        {
            id: 188,
            receivedDate: "2025-01-14",
            receivedTime: "19:03",
            subject: "Question about the meeting agenda",
            sender: "colleague@work.com",
            importance: "Informative",
        },
        {
            id: 189,
            receivedDate: "2025-01-15",
            receivedTime: "19:03",
            subject: "Details about the event",
            sender: "events@org.com",
            importance: "Informative",
        },
        {
            id: 187,
            receivedDate: "2025-01-13",
            receivedTime: "19:03",
            subject: "Team dinner planning",
            sender: "team@company.com",
            importance: "Informative",
        },
    ];

    const fakeImportantUnreadEmails: Reminder[] = [
        {
            id: 187,
            receivedDate: "2025-01-05",
            receivedTime: "19:03",
            subject: "Updated contract terms",
            sender: "legal@company.com",
            importance: "Important",
        },
        {
            id: 189,
            receivedDate: "2025-01-03",
            receivedTime: "19:03",
            subject: "Annual performance review schedule",
            sender: "hr@company.com",
            importance: "Important",
        },
        {
            id: 188,
            receivedDate: "2025-01-01",
            receivedTime: "19:03",
            subject: "New company policies",
            sender: "policy@company.com",
            importance: "Important",
        },
    ];

    // Determine the highest-priority category to display
    let emailsToDisplay: Reminder[] = [];
    let messageIntro: string = "";
    let addButtons: boolean = false;

    if (fakeEmailsRequiringAnswer.length > 0) {
        emailsToDisplay = fakeEmailsRequiringAnswer;
        messageIntro = "Hey, you might have forgotten to answer these emails:";
        addButtons = true; // Add buttons for "requiring an answer" emails
    } else if (fakeEmailsMightRequireAnswer.length > 0) {
        emailsToDisplay = fakeEmailsMightRequireAnswer;
        messageIntro = "Hey, you have these emails that might require an answer:";
    } else if (fakeImportantUnreadEmails.length > 0) {
        emailsToDisplay = fakeImportantUnreadEmails;
        messageIntro = "Hey, you have these important emails that you have not read and received more than 7 days ago:";
    } else {
        messageIntro = "You have no pending emails at the moment!";
    }

    // Generate the email list HTML
    const emailListHtml = emailsToDisplay
        .map(
            (email) => `
        <li>
            <strong>${email.subject}</strong> from <em>${email.sender}</em> on ${formatSentDate(
                email.receivedDate
            )} ${formatSentTime(email.receivedDate, email.receivedTime)}
            ${
                addButtons
                    ? `<button type="button" id="responseKeywordButton${email.id}"
                        class="border border-black text-black rounded-full px-2 py-1 hover:bg-gray-200 focus:outline-none">
                        View Email
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
            ${emailListHtml || "<li>No emails to show.</li>"}
        </ul>
    `,
        [
            { key: "mightRequireAnswer", value: "Show emails that might require an answer" },
            { key: "importantEmailsNotRead", value: "Show missed important emails" },
        ]
    );

    // Attach event listeners for "requiring answer" emails
    if (addButtons) {
        setTimeout(() => {
            emailsToDisplay.forEach((email) => {
                const keywordButton = document.getElementById(`responseKeywordButton${email.id}`);
                if (keywordButton) {
                    keywordButton.addEventListener("click", () => {
                        openSeeMailModal(email.id);
                    });
                }
            });
        }, 0);
    }
}

async function fetchEmailData(id: number): Promise<Email | undefined> {
    const result = await getData(`user/emails/${id}/data/`);

    if (!result.success) {
        displayPopup?.("error", "Failed to fetch email data", result.error as string);
        return;
    }
    return result.data;
}
</script>
