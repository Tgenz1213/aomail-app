<template>
    <div v-if="isModalOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
            <NotificationTimer
                :showNotification="showNotification"
                :notificationTitle="notificationTitle"
                :notificationMessage="notificationMessage"
                :backgroundColor="backgroundColor"
                @dismissPopup="dismissPopup"
            />
            <h1 class="text-2xl mb-6">Reset Password</h1>
            <p class="text-lg mb-6">Please enter your new password below.</p>
            <form @submit.prevent="resetPassword">
                <div class="mb-6">
                    <label for="password" class="block font-bold mb-2">Password:</label>
                    <div class="relative items-stretch mt-2 flex">
                        <input
                            ref="passwordInput"
                            :type="showPassword ? 'text' : 'password'"
                            id="password"
                            v-model="password"
                            required
                            class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                        />
                        <div class="flex items-center">
                            <button
                                @click.prevent="togglePasswordVisibility"
                                class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300"
                            >
                                <svg
                                    v-if="!showPassword"
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1.5"
                                    stroke="currentColor"
                                    class="w-6 h-6"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
                                    />
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                                    />
                                </svg>
                                <svg
                                    v-else
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1.5"
                                    stroke="currentColor"
                                    class="w-6 h-6"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
                                    />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="mb-6">
                    <label for="confirmPassword" class="block font-bold mb-2">Confirm Password:</label>
                    <div class="relative items-stretch mt-2 flex">
                        <input
                            ref="confirmPasswordInput"
                            :type="showConfirmPassword ? 'text' : 'password'"
                            id="confirmPassword"
                            v-model="confirmPassword"
                            required
                            class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                        />
                        <div class="flex items-center">
                            <button
                                @click.prevent="toggleConfirmPasswordVisibility"
                                class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300"
                            >
                                <svg
                                    v-if="!showConfirmPassword"
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1.5"
                                    stroke="currentColor"
                                    class="w-6 h-6"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
                                    />
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                                    />
                                </svg>
                                <svg
                                    v-else
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1.5"
                                    stroke="currentColor"
                                    class="w-6 h-6"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
                                    />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
                <button type="submit" class="w-full py-2 bg-black text-white rounded hover:bg-gray-800 transition">
                    Submit
                </button>
            </form>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from "vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { API_BASE_URL } from "@/global/const";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import router from "@/router/router";

const isModalOpen = ref(true);
const password = ref<string>("");
const confirmPassword = ref<string>("");
const uidb64 = ref<string>("");
const token = ref<string>("");
const passwordInput = ref<HTMLInputElement | null>(null);
const confirmPasswordInput = ref<HTMLInputElement | null>(null);
const showPassword = ref<boolean>(false);
const showConfirmPassword = ref<boolean>(false);

const showNotification = ref<boolean>(false);
const notificationTitle = ref<string>("");
const notificationMessage = ref<string>("");
const backgroundColor = ref<string>("");
const timerId = ref<number | null>(null);

function togglePasswordVisibility() {
    showPassword.value = !showPassword.value;
}

function toggleConfirmPasswordVisibility() {
    showConfirmPassword.value = !showConfirmPassword.value;
}

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Enter") {
        event.preventDefault();
        resetPassword();
    }

    if (event.key === "Tab") {
        event.preventDefault();
        if (!password.value) {
            passwordInput.value?.focus();
        } else if (!confirmPassword.value) {
            confirmPasswordInput.value?.focus();
        } else {
            if (document.activeElement === passwordInput.value) {
                confirmPasswordInput.value?.focus();
            } else {
                passwordInput.value?.focus();
            }
        }
    }
};

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
    const urlParams = new URLSearchParams(window.location.search);
    uidb64.value = urlParams.get("uidb64") || "";
    token.value = urlParams.get("token") || "";

    if (!uidb64.value || !token.value) {
        router.push({ name: "login" });
    }
});

onUnmounted(() => {
    document.removeEventListener("keydown", handleKeyDown);
});

function dismissPopup() {
    showNotification.value = false;
    if (timerId.value) {
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

async function resetPassword() {
    if (password.value.length < 8 || password.value.length > 32) {
        displayPopup("error", "Error", "Password length must be between 8 and 32 characters");
        return;
    }

    if (password.value !== confirmPassword.value) {
        displayPopup("error", "Error", "Passwords do not match");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}reset_password/${uidb64.value}/${token.value}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ password: password.value }),
        });

        if (response.ok) {
            displayPopup("success", "Success", "Password reset successful! Redirecting...");
            setTimeout(() => {
                router.push({ name: "login" });
            }, 3000);
        } else {
            const data = await response.json();
            displayPopup("error", "Error", data.error || "An error occurred. Please try again.");
        }
    } catch (error) {
        displayPopup("error", "Error", (error as Error).message || "An error occurred. Please try again.");
    }
}
</script>
