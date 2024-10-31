<template>
    <div v-if="isModalOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full">
            <NotificationTimer
                :showNotification="showNotification"
                :notificationTitle="notificationTitle"
                :notificationMessage="notificationMessage"
                :backgroundColor="backgroundColor"
                @dismissPopup="dismissPopup"
            />
            <h2 class="text-xl font-semibold mb-4">Reset Password</h2>
            <p class="mb-4">Please enter your email address below to receive a link to reset your password.</p>
            <input
                type="email"
                v-model="email"
                placeholder="Enter your email"
                class="w-full p-2 border border-gray-300 rounded mb-4"
                required
                ref="emailInput"
            />
            <button
                @click="generateResetLink"
                class="w-full py-2 bg-black text-white rounded hover:bg-gray-800 transition"
            >
                Submit
            </button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { onMounted, onUnmounted, ref } from "vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { API_BASE_URL } from "@/global/const";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import router from "@/router/router";

const isModalOpen = ref(true);
const email = ref("");
const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);
const emailInput = ref<HTMLInputElement | null>(null);

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Enter") {
        event.preventDefault();
        generateResetLink();
    }
    if (event.key === "Tab") {
        event.preventDefault();
        emailInput.value?.focus();
    }
};

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

onUnmounted(() => {
    document.removeEventListener("keydown", handleKeyDown);
});

function dismissPopup() {
    showNotification.value = false;
    if (timerId.value !== null) {
        clearTimeout(timerId.value);
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

async function generateResetLink() {
    if (!email.value) {
        displayPopup("error", "Invalid input", "Please provide an email.");
        return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email.value)) {
        displayPopup("error", "Invalid input", "Email format is not correct.");
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}generate_reset_token/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: email.value }),
        });

        if (response.ok) {
            displayPopup("success", "Check your mailbox!", "Redirecting...");
            timerId.value = setTimeout(() => {
                router.push({ name: "login" });
            }, 3000);
        } else {
            const data = await response.json();
            displayPopup("error", "Error sending password reset email", data.error);
        }
    } catch (error) {
        displayPopup("error", "Error sending password reset email", (error as Error).message);
    }
}
</script>
