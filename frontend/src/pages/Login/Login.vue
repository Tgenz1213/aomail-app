<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
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
                    <label for="login" class="block text-sm font-medium leading-6 text-gray-900">
                        {{ $t("constants.loginUppercase") }}
                    </label>
                    <div class="mt-2">
                        <input
                            id="login"
                            v-model="username"
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
                                <svg class="w-6 h-6" stroke="currentColor">
                                    <use :href="eyeIcon + '#' + (showPassword ? 'eye-hidden' : 'eye-visible')" />
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
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import logo from "@/assets/logo-aomail.png";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import router from "@/router/router";
import { API_BASE_URL, PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH } from "@/global/const";
import { i18n } from "@/global/preferences";
import eyeIcon from "@/assets/eye-icon.svg";

const username = ref<string>("");
const password = ref<string>("");
const showPassword = ref<boolean>(false);
const showNotification = ref<boolean>(false);
const notificationTitle = ref<string>("");
const notificationMessage = ref<string>("");
const backgroundColor = ref<string>("");
const timerId = ref<number | null>(null);

onMounted(async () => {
    const accessToken = localStorage.getItem("accessToken");

    if (accessToken) {
        const requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${accessToken}`,
            },
        };

        const response = await fetch(`${API_BASE_URL}is_authenticated/`, requestOptions);

        if (response.status === 401) {
            const refreshResponse = await fetch(`${API_BASE_URL}token/refresh/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ accessToken: accessToken }),
            });

            if (refreshResponse.ok) {
                router.push({ name: "inbox" });
            }
        }

        const data = await response?.json();
        if (data?.isAuthenticated) {
            router.push({ name: "inbox" });
        }
    }

    document.addEventListener("keydown", handleKeyDown);
});

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Tab") {
        event.preventDefault();
        const target = document.activeElement as HTMLElement;
        if (target.id === "login") {
            (document.getElementById("password") as HTMLElement).focus();
        } else {
            (document.getElementById("login") as HTMLElement).focus();
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
        displayPopup(
            "error",
            i18n.global.t("userLoginPage.loginError"),
            i18n.global.t("constants.popUpConstants.errorMessages.maxLoginLength150Characters")
        );
        return;
    }

    if (password.value.length < PASSWORD_MIN_LENGTH || password.value.length > PASSWORD_MAX_LENGTH) {
        displayPopup(
            "error",
            i18n.global.t("userLoginPage.loginError"),
            i18n.global.t("constants.popUpConstants.errorMessages.passwordLengthError")
        );
        return;
    }

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username.value,
            password: password.value,
        }),
    };

    try {
        const response = await fetch(`${API_BASE_URL}login/`, requestOptions);

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem("accessToken", data.accessToken);
            router.push({ name: "inbox" });
        } else {
            displayPopup(
                "error",
                i18n.global.t("userLoginPage.loginError"),
                i18n.global.t("userLoginPage.invalidCredentials")
            );
        }
    } catch (error) {
        displayPopup(
            "error",
            i18n.global.t("userLoginPage.loginError"),
            i18n.global.t("userLoginPage.invalidCredentials")
        );
    }
}
</script>
