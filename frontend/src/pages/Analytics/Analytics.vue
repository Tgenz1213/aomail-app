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
                <div class="h-full flex flex-col bg-gray-50">
                    <div class="bg-white border-b border-gray-200">
                        <div class="px-8 py-4">
                            <nav class="-mb-px flex space-x-8">
                                <a
                                    v-for="tab in tabs"
                                    :key="tab.name"
                                    :class="[
                                        activeTab === tab.name
                                            ? 'border-blue-500 text-blue-600'
                                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                                        'whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm cursor-pointer',
                                    ]"
                                    @click="activeTab = tab.name"
                                >
                                    <component :is="tab.icon" class="h-5 w-5 inline-block mr-1" aria-hidden="true" />
                                    {{ tab.label }}
                                </a>
                            </nav>
                        </div>
                    </div>
                    <div class="flex-1 overflow-auto p-8 text-center">
                        <Transition
                            enter-active-class="transition-opacity duration-200"
                            leave-active-class="transition-opacity duration-200"
                            enter-from-class="opacity-0"
                            leave-to-class="opacity-0"
                        >
                            <component :is="currentTabComponent" />
                        </Transition>
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
