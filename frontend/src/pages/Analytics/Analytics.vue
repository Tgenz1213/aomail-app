<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
    />
    <div class="flex flex-col h-screen">
        <div class="flex h-full">
            <div :class="['ring-1 shadow-sm ring-black ring-opacity-5', isNavMinimized ? 'w-20' : 'w-60']">
                <Navbar @update:isMinimized="(value) => (isNavMinimized = value)" />
            </div>
            <div class="flex-1 overflow-hidden">
                <div class="h-full flex flex-col">
                    <div class="bg-gray-50 ring-1 ring-black ring-opacity-5">
                        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                            <div class="flex items-center">
                                <div class="w-full flex items-center justify-center py-6 2xl:py-7">
                                    <div class="sm:hidden"></div>
                                    <div class="hidden sm:block w-full">
                                        <nav class="flex justify-center space-x-4 w-full" aria-label="Tabs">
                                            <div
                                                v-for="tab in tabs"
                                                :key="tab.name"
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    {
                                                        'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12':
                                                            activeTab === tab.name,
                                                        'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8':
                                                            activeTab !== tab.name,
                                                    },
                                                ]"
                                                @click="activeTab = tab.name"
                                            >
                                                <component 
                                                    :is="tab.icon" 
                                                    class="w-4 h-4" 
                                                    aria-hidden="true"
                                                />
                                                <a
                                                    :class="{
                                                        'text-gray-800': activeTab === tab.name,
                                                        'text-gray-600': activeTab !== tab.name,
                                                    }"
                                                    class="text-sm font-medium"
                                                >
                                                    {{ tab.label }}
                                                </a>
                                            </div>
                                        </nav>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="flex-1 overflow-auto p-8 text-center">
                        <DashboardTab v-if="activeTab === 'dashboard'" />
                        <AomailAdvancedTab v-if="activeTab === 'aomail-data'" />
                        <EmailProvidersAdvancedTab v-if="activeTab === 'provider-data'" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, provide } from "vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import Navbar from "@/global/components/Navbar.vue";
import DashboardTab from "./components/DashboardTab.vue";
import AomailAdvancedTab from "./components/AomailAdvancedTab.vue";
import EmailProvidersAdvancedTab from "./components/EmailProvidersAdvancedTab.vue";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { i18n } from "@/global/preferences";
import { CircleStackIcon, ChartBarIcon, ChartPieIcon } from "@heroicons/vue/24/outline";

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

const isNavMinimized = ref(localStorage.getItem("navbarMinimized") === "true");

const tabs = [
    {
        name: "dashboard",
        icon: CircleStackIcon,
        label: i18n.global.t("analyticsPage.analytics.dashboard"),
        component: DashboardTab,
    },
    {
        name: "aomail-data",
        icon: ChartBarIcon,
        label: i18n.global.t("analyticsPage.analytics.aomailData"),
        component: AomailAdvancedTab,
    },
    {
        name: "provider-data",
        icon: ChartPieIcon,
        label: i18n.global.t("analyticsPage.analytics.emailProviderData"),
        component: EmailProvidersAdvancedTab,
    },
];

const activeTab = ref("dashboard");

const currentTabComponent = computed(() => {
    const tab = tabs.find((t) => t.name === activeTab.value);
    return tab ? tab.component : null;
});

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
