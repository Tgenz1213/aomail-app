<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
    />
    <div class="flex flex-col justify-center items-center h-screen">
        <div class="flex h-full w-full">
            <div :class="['ring-1 shadow-sm ring-black ring-opacity-5', isNavMinimized ? 'w-20' : 'w-60']">
                <Navbar @update:isMinimized="(value) => (isNavMinimized = value)" />
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
                                                    'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8',
                                                ]"
                                                @click="() => router.push('/rules')"
                                            >
                                                <SparklesIcon class="w-4 h-4" />
                                                <a class="text-sm font-medium text-gray-800">
                                                    {{ $t("aiAssistantPage.rules.button") }}
                                                </a>
                                            </div>
                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-8',
                                                ]"
                                                @click="() => router.push('/ai-assistant')"
                                            >
                                                <BoltIcon class="w-4 h-4" />
                                                <a class="text-sm font-medium text-gray-600">
                                                    {{ $t("aiAssistantPage.navtitle") }}
                                                </a>
                                            </div>
                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8',
                                                ]"
                                                @click="() => router.push('/custom-categorization')"
                                            >
                                                <ChatBubbleLeftRightIcon class="w-4 h-4" />
                                                <a class="text-sm font-medium text-gray-600">
                                                    {{ $t("aiAssistantPage.emailCategories.button") }}
                                                </a>
                                            </div>
                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8',
                                                ]"
                                                @click="() => router.push('/prompt-customization')"
                                            >
                                                <AdjustmentsHorizontalIcon class="w-4 h-4" />
                                                <a class="text-sm font-medium text-gray-600">
                                                    {{ $t("aiAssistantPage.promptCustomization.button") }}
                                                </a>
                                            </div>
                                        </nav>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </main>
                    <div class="flex-1 overflow-auto p-6">
                        <PrioritizationGuidelines />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, provide } from "vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import Navbar from "@/global/components/Navbar.vue";
import { ChatBubbleLeftRightIcon, AdjustmentsHorizontalIcon, SparklesIcon, BoltIcon } from "@heroicons/vue/24/outline";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { getData } from "@/global/fetchData";
import PrioritizationGuidelines from "./components/PrioritizationGuidelines.vue";
import { useRouter } from "vue-router";
import { i18n } from "@/global/preferences";

const router = useRouter();
const showNotification = ref(false);
const isNavMinimized = ref(localStorage.getItem("navbarMinimized") === "true");
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

const currentGuidelines = ref({
    importantGuidelines: "",
    informativeGuidelines: "",
    uselessGuidelines: "",
});

const guidelines = ref({
    important: "",
    informative: "",
    useless: "",
});

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

async function loadCurrentGuidelines() {
    const result = await getData("user/preferences/guidelines/");
    if (result.success) {
        currentGuidelines.value = result.data;
        guidelines.value = {
            important: result.data.importantGuidelines,
            informative: result.data.informativeGuidelines,
            useless: result.data.uselessGuidelines,
        };
    } else {
        displayPopup(
            "error",
            i18n.global.t("aiAssistantPage.errorMessages.failedToLoadGuidelines"),
            result.error as string
        );
    }
}

provide("displayPopup", displayPopup);

onMounted(() => {
    loadCurrentGuidelines();
});
</script>
