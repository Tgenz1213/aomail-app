<template>
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
import { KeyValuePair, Message } from "@/global/types";
import { postData, getData } from "@/global/fetchData";
import { formatSentDate, formatSentTime } from "@/global/formatters";

interface Email {
    id: number;
    receivedDate: string;
    receivedTime: string;
    subject: string;
    emailAddress: string;
    importance: string;
}

const messages = inject("messages") as Ref<Message[]>;
const waitForButtonClick = inject("waitForButtonClick") as Ref<boolean>;
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
    // Remove the button options after clicking
    messages.value[index].buttonOptions = undefined;
};

onMounted(async () => {
    await fetchAiReminders();
});

async function fetchAiReminders() {
    // Simulating the fetching of email reminders
    const fakeEmailsRequiringAnswer: Email[] = [
        {
            id: 1,
            receivedDate: "2025-01-10",
            receivedTime: "19:03",
            subject: "Follow-up on project status",
            emailAddress: "manager@company.com",
            importance: "Important",
        },
        {
            id: 2,
            receivedDate: "2025-01-12",
            receivedTime: "19:03",
            subject: "Request for documents",
            emailAddress: "client@business.com",
            importance: "Important",
        },
    ];

    const fakeEmailsMightRequireAnswer: Email[] = [
        {
            id: 3,
            receivedDate: "2025-01-14",
            receivedTime: "19:03",
            subject: "Question about the meeting agenda",
            emailAddress: "colleague@work.com",
            importance: "Informative",
        },
        {
            id: 4,
            receivedDate: "2025-01-15",
            receivedTime: "19:03",
            subject: "Details about the event",
            emailAddress: "events@org.com",
            importance: "Informative",
        },
        {
            id: 5,
            receivedDate: "2025-01-13",
            receivedTime: "19:03",
            subject: "Team dinner planning",
            emailAddress: "team@company.com",
            importance: "Informative",
        },
    ];

    const fakeImportantUnreadEmails: Email[] = [
        {
            id: 6,
            receivedDate: "2025-01-05",
            receivedTime: "19:03",
            subject: "Updated contract terms",
            emailAddress: "legal@company.com",
            importance: "Important",
        },
        {
            id: 7,
            receivedDate: "2025-01-03",
            receivedTime: "19:03",
            subject: "Annual performance review schedule",
            emailAddress: "hr@company.com",
            importance: "Important",
        },
        {
            id: 8,
            receivedDate: "2025-01-01",
            receivedTime: "19:03",
            subject: "New company policies",
            emailAddress: "policy@company.com",
            importance: "Important",
        },
        {
            id: 9,
            receivedDate: "2024-12-30",
            receivedTime: "19:03",
            subject: "Welcome to the team!",
            emailAddress: "welcome@company.com",
            importance: "Important",
        },
        {
            id: 10,
            receivedDate: "2024-12-28",
            receivedTime: "19:03",
            subject: "Your benefits package",
            emailAddress: "benefits@company.com",
            importance: "Important",
        },
    ];

    // Display the emails to the user
    displayAIMsg(`
        <p><strong>Hey, you might have forgotten to answer these emails:</strong></p>
        <ul>
            ${fakeEmailsRequiringAnswer
                .map(
                    (email) => `
                <li>
                    <strong>${email.subject}</strong> from <em>${email.emailAddress}</em> on ${formatSentDate(
                        email.receivedDate
                    )} ${formatSentTime(email.receivedDate, email.receivedTime)}
                </li>
            `
                )
                .join("")}
        </ul>
    `);

    displayAIMsg(`
        <p><strong>Hey, you have these emails that might require an answer:</strong></p>
        <ul>
            ${fakeEmailsMightRequireAnswer
                .map(
                    (email) => `
                <li>
                    <strong>${email.subject}</strong> from <em>${email.emailAddress}</em> on ${formatSentDate(
                        email.receivedDate
                    )} ${formatSentTime(email.receivedDate, email.receivedTime)}
                </li>
            `
                )
                .join("")}
        </ul>
    `);

    displayAIMsg(`
        <p><strong>Hey, you have these important emails that you have not read and received more than 7 days ago:</strong></p>
        <ul>
            ${fakeImportantUnreadEmails
                .map(
                    (email) => `
                <li>
                    <strong>${email.subject}</strong> from <em>${email.emailAddress}</em> on ${formatSentDate(
                        email.receivedDate
                    )} ${formatSentTime(email.receivedDate, email.receivedTime)}
                </li>
            `
                )
                .join("")}
        </ul>
    `);
}
</script>
