<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
    />
    <div class="h-screen">
        <div class="flex h-full w-full">
            <div class="w-[90px] 2xl:w-[100px] bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <NavBarSmall />
            </div>
            <div class="flex-1 bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <div class="flex flex-col h-full relative">
                    <div class="w-full px-6 py-3 border-b border-gray-200 flex flex-col justify-center items-center">
                        <h1 class="text-xl font-semibold text-black-600">Custom Categorization Chatbot</h1>
                        <p class="text-sm text-gray-600">
                            Improve your email categorization to fit your needs and stay organized easily.
                        </p>
                    </div>
                    <div class="flex-1 overflow-y-auto">
                        <Conversation />
                    </div>

                    <ChatInput v-if="!waitForButtonClick" @response="handleUserResponse" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { provide, ref } from "vue";
import Conversation from "./components/Conversation.vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import ChatInput from "./components/ChatInput.vue";
import { Message } from "@/global/types";

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

const userInputResolver = ref<((value: string) => void) | null>(null);
const waitForButtonClick = ref(false);
const messages = ref<Message[]>([
    {
        textHtml: "Hello and welcome to the custom email categorization feature",
        isUser: false,
    },
]);

const displayUserMsg = (message: string) => {
    messages.value.push({ textHtml: message, isUser: true });
};

const handleUserResponse = (response: string) => {
    displayUserMsg(response);
    if (userInputResolver.value) {
        userInputResolver.value(response);
        userInputResolver.value = null;
    }
};

async function waitForUserInput(): Promise<string> {
    return new Promise((resolve) => {
        userInputResolver.value = resolve;
    });
}

provide("waitForButtonClick", waitForButtonClick);
provide("messages", messages);
provide("displayPopup", displayPopup);
provide("displayUserMsg", displayUserMsg);
provide("waitForUserInput", waitForUserInput);

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
</script>
