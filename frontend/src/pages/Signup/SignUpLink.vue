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
                                    <EmailLinkForm v-if="step === 1" />
                                    <CategoriesForm v-if="step === 2" />
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, provide } from "vue";
import { postData } from "@/global/fetchData";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { i18n } from "@/global/preferences";
import logo from "@/assets/logo-aomail.png";
import StepsTracker from "./components/StepsTracker.vue";
import EmailLinkForm from "./components/EmailLinkForm.vue";
import CategoriesForm from "./components/CategoriesForm.vue";
import router from "@/router/router";
import { API_BASE_URL } from "@/global/const";
import { Category } from "@/global/types";
import { createDefaultFilters } from "@/global/filters";

const showNotification = ref<boolean>(false);
const notificationTitle = ref<string>("");
const notificationMessage = ref<string>("");
const backgroundColor = ref<string>("");
const timerId = ref<number | null>(null);
const step = ref(1);

provide("step", step);
provide("submitSignupData", submitSignupData);
provide("createCategories", createCategories);
provide("processDemoEmails", processDemoEmails);

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Enter") {
        event.preventDefault();
        if (step.value === 1) {
            submitSignupData(event);
        } else if (step.value === 2) {
            router.push({ name: "inbox" });
        }
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
            i18n.global.t("signUpLinkPage.acceptTerms"),
            i18n.global.t("signUpLinkPage.termsNotAccepted")
        );
        return;
    } else {
        label.classList.remove("text-red-500");
        label.classList.add("text-gray-500");
        link.classList.remove("text-red-500");
        link.classList.add("text-black");
    }
    displayPopup(
        "success",
        i18n.global.t("signUpLinkPage.accountCreationInProgress"),
        i18n.global.t("signUpLinkPage.waitingDatabaseResponse")
    );

    const urlParams = new URLSearchParams(window.location.search);
    const authorizationCode = urlParams.get("code");
    if (authorizationCode) {
        sessionStorage.setItem("code", authorizationCode);
    } else {
        displayPopup(
            "error",
            i18n.global.t("signUpLinkPage.authorizationError"),
            i18n.global.t("signUpLinkPage.authorizationCodeNotFound")
        );
    }

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            login: sessionStorage.getItem("email"),
            password: sessionStorage.getItem("password"),
            timezone: localStorage.getItem("timezone"),
            language: localStorage.getItem("language"),
            code: sessionStorage.getItem("code"),
            typeApi: sessionStorage.getItem("typeApi"),
        }),
    };

    try {
        const response = await fetch(`${API_BASE_URL}signup/`, requestOptions);

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem("accessToken", data.accessToken);
            localStorage.setItem("signupToken", data.signupToken);
            localStorage.setItem("emailSocial", data.emailSocial);
            step.value++;
        } else {
            const data = await response.json();
            displayPopup("error", i18n.global.t("signUpLinkPage.accountCreationError"), data.error);
        }
    } catch (error) {
        displayPopup("error", i18n.global.t("signUpLinkPage.accountCreationError"), (error as Error).message);
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

async function createCategories(categories: Category[]) {
    try {
        const response = await postData("create_categories/", {
            categories,
        });
        if (!response.success) {
            displayPopup("error", i18n.global.t("signUpLinkPage.categoryCreationError"), "");
        }

        for (const category of categories) {
            await createDefaultFilters(category.name);
        }
    } catch (error) {
        displayPopup("error", i18n.global.t("signUpLinkPage.categoryCreationError"), (error as Error).message);
    }
}

async function processDemoEmails() {
    try {
        const overlay = document.createElement("div");
        overlay.className = "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50";

        const loadingBar = document.createElement("div");
        loadingBar.className = "bg-white p-6 rounded-lg shadow-lg flex flex-col items-center space-y-4";

        const iconContainer = document.createElement("div");
        iconContainer.className = "inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900";

        const emailIcon = `
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-white">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
            </svg>`;

        const rocketIcon = `
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-white">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.59 14.37a6 6 0 01-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 006.16-12.12A14.98 14.98 0 009.631 8.41m5.96 5.96a14.926 14.926 0 01-5.841 2.58m-.119-8.54a6 6 0 00-7.381 5.84h4.8m2.581-5.84a14.927 14.927 0 00-2.58 5.84m2.699 2.7c-.103.021-.207.041-.311.06a15.09 15.09 0 01-2.448-2.448 14.9 14.9 0 01.06-.312m-2.24 2.39a4.493 4.493 0 00-1.757 4.306 4.493 4.493 0 004.306-1.758M16.5 9a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z" />
            </svg>`;

        iconContainer.innerHTML = emailIcon;

        const text = document.createElement("div");
        text.className = "text-lg font-semibold text-gray-900 text-center";
        text.textContent = i18n.global.t("signUpLinkPage.processingLastEmails");

        const progressContainer = document.createElement("div");
        progressContainer.className = "w-64 h-2 bg-gray-200 rounded-full overflow-hidden";

        const progressBar = document.createElement("div");
        progressBar.className = "h-full bg-gray-900 transition-all duration-300";
        progressBar.style.width = "0%";

        progressContainer.appendChild(progressBar);
        loadingBar.appendChild(iconContainer);
        loadingBar.appendChild(text);
        loadingBar.appendChild(progressContainer);
        overlay.appendChild(loadingBar);
        document.body.appendChild(overlay);

        let isEmailIcon = true;
        const iconInterval = setInterval(() => {
            iconContainer.innerHTML = isEmailIcon ? rocketIcon : emailIcon;
            isEmailIcon = !isEmailIcon;
        }, 1000);

        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 0.714;
            progressBar.style.width = `${Math.min(progress, 100)}%`;
        }, 100);

        const response = await postData("process_demo_data/", {
            emailSocial: localStorage.getItem("emailSocial"),
            typeApi: sessionStorage.getItem("typeApi"),
            signupToken: localStorage.getItem("signupToken"),
        });

        await new Promise((resolve) => setTimeout(resolve, 14000));

        clearInterval(iconInterval);
        clearInterval(progressInterval);
        document.body.removeChild(overlay);

        if (response.success) {
            sessionStorage.clear();
            router.push({ name: "inbox" });
        } else {
            displayPopup("error", i18n.global.t("signUpLinkPage.demoProcessingError"), "");
        }
    } catch (error) {
        displayPopup("error", i18n.global.t("signUpLinkPage.demoProcessingError"), (error as Error).message);
    }
}
</script>
