<template>
    <div class="relative" :style="{ width: assistantChatWidth + '%' }">
        <div
            :class="[
                'bg-white border-r border-gray-200 flex flex-col transition-all duration-500 ease-in-out',
                isExpanded ? 'w-full' : 'w-0',
            ]"
        >
            <button
                @click="toggleSidebar"
                class="absolute left-0 top-1/2 transform -translate-y-1/2 rounded-r-sm flex items-center justify-center w-8 h-8 border-t border-r border-b border-gray-300 focus:outline-none hover:bg-gray-100"
            >
                <ChevronDoubleLeftIcon v-if="!isExpanded" class="h-5 w-5 text-gray-700" />
                <ChevronDoubleRightIcon v-else class="h-5 w-5 text-gray-700" />
            </button>
            <div :class="[isExpanded ? 'p-6 bg-white' : 'hidden']">
                <Conversation />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { provide, ref, inject, Ref } from "vue";
import Conversation from "../components/Conversation.vue";
import { ChevronDoubleLeftIcon, ChevronDoubleRightIcon } from "@heroicons/vue/24/outline";
import { Message } from "@/global/types";

const isExpanded = ref(localStorage.getItem("inboxAiAssistantMinimized") === "true");
const hasBeenExpanded = ref(false);

const toggleSidebar = () => {
    if (!hasBeenExpanded.value) {
        hasBeenExpanded.value = true;
    }
    isExpanded.value = !isExpanded.value;
    localStorage.setItem("inboxAiAssistantMinimized", isExpanded.value.toString());
};

const userInputResolver = ref<((value: string) => void) | null>(null);
const waitForButtonClick = ref(false);
const messages = ref<Message[]>([]);

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
provide("displayUserMsg", displayUserMsg);
provide("waitForUserInput", waitForUserInput);

// Receive the assistantChatWidth from parent
const assistantChatWidth = inject("assistantChatWidth") as Ref<number>;
</script>

<style scoped>
.relative {
    transition: width 0.3s ease-in-out;
}
</style>
