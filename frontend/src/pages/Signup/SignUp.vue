<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
    />
    <div class="h-screen flex flex-col px-6 2xl:py-12 lg:px-8 overflow-y-auto">
        <div class="flex-grow flex flex-col justify-center py-4">
            <div class="w-full flex flex-col items-center">
                <div class="flex flex-col 2xl:mt-0 gap-y-1">
                    <img class="mx-auto h-10 w-auto" :src="logo" alt="Aomail logo" />
                    <h2 class="text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                        {{ $t("signUpPart1Page.signUp") }}
                    </h2>
                </div>
                <div class="2xl:mt-6 sm:mt-4 sm:mx-auto sm:w-full sm:max-w-[545px]">
                    <div class="flex flex-col rounded-lg">
                        <div>
                            <div class="flex items-center justify-center h-[65px]">
                                <StepsTracker :signUpPage="''" />
                            </div>
                            <div class="bg-white px-6 py-4">
                                <CredentialsForm v-if="step === 0" />
                            </div>
                        </div>
                    </div>
                    <p class="mt-2 text-center text-sm text-gray-600">
                        {{ $t("signUpPart1Page.youHaveAnAccount") }}
                        <a href="/" class="font-semibold leading-6 text-gray-900 hover:text-black">
                            {{ $t("constants.userActions.login") }}
                        </a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, provide } from "vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { i18n } from "@/global/preferences";
import logo from "@/assets/logo-aomail.png";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { Category } from "@/global/types";
import router from "@/router/router";
import CredentialsForm from "./components/CredentialsForm.vue";
import StepsTracker from "./components/StepsTracker.vue";
import { API_BASE_URL, PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH } from "@/global/const";

const showNotification = ref<boolean>(false);
const step = ref<number>(0);
const login = ref<string>("");
const userDescription = ref<string>("");
const password = ref<string>("");
const confirmPassword = ref<string>("");
const credentialError = ref<string>("");
const notificationTitle = ref<string>("");
const notificationMessage = ref<string>("");
const backgroundColor = ref<string>("");
const timerId = ref<number | null>(null);
const categories = ref<Category[]>([]);
const isModalNewCategoryOpen = ref<boolean>(false);
const isModalUpdateCategoryOpen = ref<boolean>(false);

provide("step", step);
provide("isModalNewCategoryOpen", isModalNewCategoryOpen);
provide("isModalUpdateCategoryOpen", isModalUpdateCategoryOpen);
provide("userDescription", userDescription);
provide("login", login);
provide("password", password);
provide("confirmPassword", confirmPassword);
provide("credentialError", credentialError);
provide("categories", categories);
provide("displayPopup", displayPopup);
provide("clearError", clearError);
provide("goStepCategoriesForm", goStepCategoriesForm);
provide("goStepLinkEmail", goStepLinkEmail);

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
    sessionStorage.clear();

    const browserLanguage = navigator.language.toLowerCase();
    const languageKey = browserLanguage.startsWith("fr") ? "french" : "american";

    if (!localStorage.getItem("language")) {
        localStorage.setItem("language", languageKey);
        i18n.global.locale = languageKey;
    }

    if (!localStorage.getItem("timezone")) {
        try {
            const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            localStorage.setItem("timezone", timezone);
        } catch {
            localStorage.setItem("timezone", "UTC");
        }
    }
});

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Tab") {
        event.preventDefault();
        if (step.value == 0) {
            if (document.activeElement?.id === "email") {
                document.getElementById("password")?.focus();
            } else if (document.activeElement?.id === "password") {
                document.getElementById("confirmPassword")?.focus();
            } else if (document.activeElement?.id === "confirmPassword") {
                document.getElementById("userDescription")?.focus();
            } else {
                document.getElementById("email")?.focus();
            }
        }
    } else if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        if (step.value === 0) {
            goStepLinkEmail();
        } else if (step.value === 1) {
            goStepCategoriesForm();
        }
    }
}

function goStepCategoriesForm() {
    step.value++;
}

function clearError() {
    credentialError.value = "";
}

async function goStepLinkEmail() {
    clearError();

    if (!login.value.trim()) {
        credentialError.value = i18n.global.t("constants.popUpConstants.errorMessages.pleaseEnterAnIdentifier");
        return;
    }

    if (!password.value.trim()) {
        credentialError.value = i18n.global.t("constants.popUpConstants.errorMessages.pleaseEnterPassword");
        return;
    }

    if (login.value.length > 150) {
        credentialError.value = i18n.global.t("constants.popUpConstants.errorMessages.maxLoginLength150Characters");
        return;
    }

    try {
        const requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                email: login.value,
            },
        };

        const result = await fetch(`${API_BASE_URL}check_username/`, requestOptions);
        const data = await result.json();

        if (data.available === false) {
            credentialError.value = i18n.global.t("constants.popUpConstants.errorMessages.usernameAlreadyExists");
            return;
        }
    } catch (error) {
        if (error instanceof Error) {
            displayPopup?.(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.errorMessageVerificationIdentifier"),
                error.message
            );
        } else {
            displayPopup?.(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.errorMessageVerificationIdentifier"),
                "An unknown error occurred"
            );
        }
        return;
    }

    if (!password.value.trim()) {
        credentialError.value = i18n.global.t("constants.popUpConstants.errorMessages.pleaseEnterPassword");
        return;
    } else if (!confirmPassword.value.trim()) {
        credentialError.value = i18n.global.t("constants.popUpConstants.errorMessages.pleaseConfirmPassword");
        return;
    } else if (password.value.length < PASSWORD_MIN_LENGTH || password.value.length > PASSWORD_MAX_LENGTH) {
        credentialError.value = i18n.global.t("constants.popUpConstants.errorMessages.passwordLengthError");
        return;
    } else if (password.value !== confirmPassword.value) {
        credentialError.value = i18n.global.t("constants.popUpConstants.errorMessages.passwordsDoNotMatch");
        return;
    }

    sessionStorage.setItem("username", login.value);
    sessionStorage.setItem("userDescription", userDescription.value);
    sessionStorage.setItem("password", password.value);

    router.push({ name: "signupLink" });
}

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
