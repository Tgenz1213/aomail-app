<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />
    <div class="h-screen bg-white flex min-h-full flex-col justify-center items-center px-6 py-12 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <img class="mx-auto h-12 w-auto" :src="logo" alt="Aomail logo" />
            <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                {{ $t("userLoginPage.connectAccount") }}
            </h2>
        </div>
        <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form class="space-y-6">
                <div>
                    <label for="username" class="block text-sm font-medium leading-6 text-gray-900">
                        {{ $t("constants.username") }}
                    </label>
                    <div class="mt-2">
                        <input
                            id="username"
                            v-model="username"
                            autocomplete="email"
                            required
                            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"
                        />
                    </div>
                </div>
                <div>
                    <div class="flex items-center justify-between">
                        <label for="password" class="block text-sm font-medium leading-6 text-gray-900">
                            {{ $t("constants.password") }}
                        </label>
                        <div class="text-sm">
                            <a :href="`/password-reset-link`" class="font-semibold text-gray-900 hover:text-gray-600">
                                {{ $t("userLoginPage.forgottenPassword") }}
                            </a>
                        </div>
                    </div>
                    <div class="relative items-stretch mt-2 flex">
                        <input
                            id="password"
                            :type="showPassword ? 'text' : 'password'"
                            class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                            v-model="password"
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
                <div>
                    <button
                        type="button"
                        @click="login"
                        class="flex w-full justify-center rounded-md bg-gray-900 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-900"
                    >
                        {{ $t("constants.userActions.login") }}
                    </button>
                </div>
            </form>
            <p class="mt-10 text-center text-sm text-gray-500">
                {{ $t("userLoginPage.doNotHaveAccount") }}
                <a href="/signup" class="font-semibold leading-6 text-gray-900 hover:text-gray-600">
                    {{ $t("userLoginPage.beginFreeTrial") }}
                </a>
            </p>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import NotificationTimer from "@/components/NotificationTimer.vue";
import { useRouter } from "vue-router";
import { API_BASE_URL } from "@/global/const";
import logo from "@/assets/logo-aomail.png";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";

const router = useRouter();

const username = ref<string>("");
const password = ref<string>("");
const showPassword = ref<boolean>(false);
const showNotification = ref<boolean>(false);
const notificationTitle = ref<string>("");
const notificationMessage = ref<string>("");
const backgroundColor = ref<string>("");
const timerId = ref<number | null>(null);

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Tab") {
        event.preventDefault();
        const target = document.activeElement as HTMLElement;
        if (target.id === "username") {
            (document.getElementById("password") as HTMLElement).focus();
        } else {
            (document.getElementById("username") as HTMLElement).focus();
        }
    } else if (event.key === "Enter") {
        event.preventDefault();
        login();
    }
}

function togglePasswordVisibility() {
    showPassword.value = !showPassword.value;
}

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

async function login() {
    if (username.value.length > 150) {
        displayPopup("error", "userLoginPage.loginError", "userLoginPage.maxUsernameLength");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}api/login/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value,
            }),
        });

        if (response.ok) {
            const { access_token } = await response.json();
            localStorage.setItem("access_token", access_token);
            router.push({ name: "home" });
        } else {
            displayPopup("error", "userLoginPage.loginError", "userLoginPage.invalidCredentials");
        }
    } catch {
        displayPopup("error", "userLoginPage.loginError", "userLoginPage.invalidCredentials");
    }
}
</script>
