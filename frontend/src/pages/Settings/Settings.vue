<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />
    <div class="flex flex-col justify-center items-center h-screen">
        <div class="flex h-full w-full">
            <div class="w-[90px] 2xl:w-[100px] bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <NavBarSmall />
            </div>
            <div class="flex-1 bg-white ring-1 ring-black ring-opacity-5">
                <div class="flex flex-col h-full">
                    <main class="bg-gray-50 ring-1 ring-black ring-opacity-5">
                        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                            <div class="flex items-center">
                                <div class="w-full flex items-center justify-center py-6 2xl:py-7">
                                    <div class="sm:hidden"></div>
                                    <div class="hidden sm:block w-full">
                                        <nav class="flex justify-center space-x-4 w-full" aria-label="Tabs">
                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    {
                                                        'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12':
                                                            activeSection === 'account',
                                                        'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8':
                                                            activeSection !== 'account',
                                                    },
                                                ]"
                                                @click="setActiveSection('account')"
                                            >
                                                <user-icon class="w-4 h-4" />
                                                <a
                                                    :class="{
                                                        'text-gray-800': activeSection === 'account',
                                                        'text-gray-600': activeSection !== 'account',
                                                    }"
                                                    class="text-sm font-medium"
                                                >
                                                    {{ $t("settingsPage.accountPage.myAccountTitle") }}
                                                </a>
                                            </div>
                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    {
                                                        'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12':
                                                            activeSection === 'preferences',
                                                        'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8':
                                                            activeSection !== 'preferences',
                                                    },
                                                ]"
                                                @click="setActiveSection('preferences')"
                                            >
                                                <adjustments-vertical-icon class="w-4 h-4" />
                                                <a
                                                    :class="{
                                                        'text-gray-800': activeSection === 'preferences',
                                                        'text-gray-600': activeSection !== 'preferences',
                                                    }"
                                                >
                                                    {{ $t("settingsPage.preferencesPage.preferencesTitle") }}
                                                </a>
                                            </div>
                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    {
                                                        'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12':
                                                            activeSection === 'subscription',
                                                        'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8':
                                                            activeSection !== 'subscription',
                                                    },
                                                ]"
                                                @click="setActiveSection('subscription')"
                                            >
                                                <credit-card-icon class="w-4 h-4" />
                                                <a
                                                    :class="{
                                                        'text-gray-800': activeSection === 'subscription',
                                                        'text-gray-600': activeSection !== 'subscription',
                                                    }"
                                                    class="text-sm font-medium"
                                                >
                                                    {{ $t("settingsPage.subscriptionPage.subscriptionTitle") }}
                                                </a>
                                            </div>

                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    {
                                                        'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12':
                                                            activeSection === 'data',
                                                        'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8':
                                                            activeSection !== 'data',
                                                    },
                                                ]"
                                                @click="setActiveSection('data')"
                                            >
                                                <circle-stack-icon class="w-4 h-4" />
                                                <a
                                                    :class="{
                                                        'text-gray-800': activeSection === 'data',
                                                        'text-gray-600': activeSection !== 'data',
                                                    }"
                                                    class="text-sm font-medium"
                                                >
                                                    {{ $t("settingsPage.dataPage.myData") }}
                                                </a>
                                            </div>
                                        </nav>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </main>

                    <div v-if="activeSection === 'account'">
                        <MyAccountMenu />
                    </div>

                    <div v-if="activeSection === 'subscription'" class="flex-1 section mx-8 my-8 2xl:mx-12 2xl:my-12">
                        <SubscriptionMenu />
                    </div>

                    <div v-if="activeSection === 'data'" class="flex flex-col h-full section">
                        <MyDataMenu />
                    </div>

                    <div v-if="activeSection === 'preferences'" class="flex-1 section">
                        <PreferencesMenu />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
/* eslint-disable */
import { ref, onMounted, provide } from "vue";
import { API_BASE_URL } from "@/global/const";
import { fetchWithToken } from "@/global/security";
import "@fortawesome/fontawesome-free/css/all.css";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { AdjustmentsVerticalIcon, UserIcon, CreditCardIcon, CircleStackIcon } from "@heroicons/vue/24/outline";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import PreferencesMenu from "@/pages/Settings/components/PreferencesMenu.vue";
import MyDataMenu from "@/pages/Settings/components/MyDataMenu.vue";
import SubscriptionMenu from "@/pages/Settings/components/SubscriptionMenu.vue";
import MyAccountMenu from "@/pages/Settings/components/MyAccountMenu.vue";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import { i18n } from "@/global/preferences";

const activeSection = ref("account");
const emailSelected = ref("");

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

provide("displayPopup", displayPopup);

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

function closeUserDescriptionModal() {
    isModalUserDescriptionOpen.value = false;
}

async function updateUserDescription() {
    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            email: emailSelected.value,
            user_description: userDescription.value.trim() ? userDescription.value.trim() : "",
        }),
    };

    const response = await fetchWithToken(`${API_BASE_URL}user/social_api/update_user_description/`, requestOptions);

    if (!response) {
        displayPopup("error", "No response from server", "Verify your internet connection");
        return;
    }

    if (!response.ok) {
        displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`);
        return;
    }

    const data = await response.json();

    if (data.message === "User description updated") {
        displayPopup(
            "success",
            t("constants.popUpConstants.successMessages.success"),
            t("settingsPage.accountPage.emailDescriptionUpdated")
        );
    } else {
        displayPopup("error", i18n.global.t("settingsPage.accountPage.errorUpdatingDescription"), data.error);
    }
    closeUserDescriptionModal();
}

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Tab" && !isModalOpen.value) {
        event.preventDefault();
        switchActiveSection();
    } else if (event.key === "Escape") {
        if (isModalOpen.value) {
            closeModal();
        } else if (isModalUserDescriptionOpen.value) {
            closeUserDescriptionModal();
        } else if (isUnlinkModalOpen.value) {
            closeUnlinkModal();
        }
    } else if (event.key === "Enter") {
        if (isModalUserDescriptionOpen.value) {
            updateUserDescription();
        }
    }
}

function switchActiveSection() {
    const nextSection: { [key: string]: string } = {
        account: "preferences",
        preferences: "subscription",
        subscription: "data",
        data: "account",
    };

    setActiveSection(nextSection[activeSection.value]);
}

function setActiveSection(section: string) {
    activeSection.value = section;
}

function closeModal() {
    isModalOpen.value = false;
    const checkbox = document.querySelector('input[name="choice"]') as HTMLInputElement;
    if (checkbox) {
        checkbox.checked = false;
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
