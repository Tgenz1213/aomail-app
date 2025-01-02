<template>
    <div class="flex h-screen">
        <Conversation />
    </div>
</template>

<script setup lang="ts">
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { Category, EmailLinked } from "@/global/types";
import { provide, ref } from "vue";
import Conversation from "./components/Conversation.vue";

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

const userInput = ref("");
const categories = ref<Category[]>([]);
const emailsLinked = ref<EmailLinked[]>([]);
provide("categories", categories);
provide("emailsLinked", emailsLinked);
provide("userInput", userInput);
provide("displayPopup", displayPopup);

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
