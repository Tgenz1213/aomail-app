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
                    <img class="mx-auto h-10 w-auto" :src="logo" alt="Aomail" />
                    <h2 class="text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                        {{ $t("signUpPart1Page.signUp") }}
                    </h2>
                </div>
                <div class="2xl:mt-6 sm:mt-4 sm:mx-auto sm:w-full sm:max-w-[545px]">
                    <div class="flex flex-col">
                        <div class="">
                            <div class="flex items-center justify-center h-[65px]">
                                <StepsTracker :signUpPage="'linkEmail'" />
                            </div>
                            <div class="bg-white px-6 py-4 sm:px-12">
                                <form class="space-y-6">
                                    <EmailLinkForm v-if="step === 3" />
                                    <Summary v-if="step === 4" />
                                </form>
                            </div>
                        </div>
                    </div>
                    <p class="mt-6 text-center text-sm text-gray-500">
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
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { i18n } from "@/global/preferences";
import logo from "@/assets/logo-aomail.png";
import StepsTracker from "./components/StepsTracker.vue";
import { postData } from "@/global/fetchData";
import EmailLinkForm from "./components/EmailLinkForm.vue";
import Summary from "./components/Summary.vue";
import router from "@/router/router";
import { API_BASE_URL } from "@/global/const";

const showNotification = ref<boolean>(false);
const notificationTitle = ref<string>("");
const notificationMessage = ref<string>("");
const backgroundColor = ref<string>("");
const timerId = ref<number | null>(null);
const step = ref(3);

provide("step", step);
provide("submitSignupData", submitSignupData);
provide("goStepSignUpSummary", goStepSignUpSummary);

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Enter") {
        event.preventDefault();
        if (step.value === 3) {
            goStepSignUpSummary(event);
        }
    }
}

async function goStepSignUpSummary(event: Event) {
    event.preventDefault();
    const urlParams = new URLSearchParams(window.location.search);
    const authorizationCode = urlParams.get("code");

    if (authorizationCode) {
        sessionStorage.setItem("code", authorizationCode);
        step.value++;
    } else {
        displayPopup(
            "error",
            i18n.global.t("signuUpLinkPage.authorizationError"),
            i18n.global.t("signuUpLinkPage.authorizationCodeNotFound")
        );
    }
}

async function submitSignupData(event: Event) {
    event.preventDefault();
    const checkbox = document.getElementById("comments") as HTMLInputElement;
    const label = document.querySelector('label[for="comments"]') as HTMLLabelElement;
    const link = document.querySelector('label[for="comments"] a') as HTMLAnchorElement;

    if (!checkbox.checked) {
        label.classList.add("text-red-500");
        label.classList.remove("text-gray-500");
        link.classList.add("text-red-500");
        link.classList.remove("text-black");

        displayPopup(
            "error",
            i18n.global.t("signuUpLinkPage.acceptTerms"),
            i18n.global.t("signuUpLinkPage.termsNotAccepted")
        );
        return;
    } else {
        label.classList.remove("text-red-500");
        label.classList.add("text-gray-500");
        link.classList.remove("text-red-500");
        link.classList.add("text-black");
    }

    displayPopup("success", "Account creation in progress...", "Waiting for database response");

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            login: sessionStorage.getItem("login"),
            password: sessionStorage.getItem("password"),
            timezone: localStorage.getItem("timezone"),
            language: localStorage.getItem("language"),
            theme: localStorage.getItem("theme"),
            categories: localStorage.getItem("categories"),
            code: sessionStorage.getItem("code"),
            typeApi: sessionStorage.getItem("typeApi"),
            userDescription: sessionStorage.getItem("userDescription"),
        }),
    };

    try {
        const response = await fetch(`${API_BASE_URL}signup/`, requestOptions);

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem("accessToken", data.accessToken);
            sessionStorage.clear();
            localStorage.removeItem("categories");
            router.push({ name: "home" });
        } else {
            const data = await response.json();
            displayPopup("error", i18n.global.t("signuUpLinkPage.accountCreationError"), data.error);
        }
    } catch (error) {
        displayPopup("error", i18n.global.t("signuUpLinkPage.accountCreationError"), (error as Error).message);
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

function dismissPopup() {
    showNotification.value = false;
    if (timerId.value !== null) {
        clearTimeout(timerId.value);
    }
}
</script>
