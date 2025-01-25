<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
    />
    <div class="h-screen flex flex-col">
        <div class="flex h-full">
            <div :class="['ring-1 shadow-sm ring-black ring-opacity-5', isNavMinimized ? 'w-20' : 'w-60']">
                <Navbar @update:isMinimized="(value) => (isNavMinimized = value)" />
            </div>

            <div class="flex flex-1 flex-col">
                <div class="px-6 py-4 bg-gray-100 border-b border-gray-300">
                    <div class="relative">
                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                            <div class="w-full border-t border-gray-300"></div>
                        </div>
                        <div class="relative flex justify-center">
                            <span class="bg-gray-100 px-4 text-sm font-medium text-gray-600">AI Section</span>
                        </div>
                    </div>
                    <div class="mt-4 flex flex-col gap-3 md:flex-row md:items-center md:gap-6">
                        <a
                            href="/custom-categorization"
                            class="rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
                        >
                            Customize My Automatic Email Categorization
                        </a>

                        <a
                            href="/rules"
                            class="flex items-center gap-2 rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
                        >
                            <BeakerIcon class="w-5 h-5" />
                            {{ $t("constants.rulesNavbar") }}
                        </a>

                        <button
                            class="flex items-center gap-2 rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
                        >
                            <CogIcon class="w-5 h-5" />
                            AI Settings
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { provide, ref } from "vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import Navbar from "@/global/components/Navbar.vue";
import { BeakerIcon, CogIcon } from "@heroicons/vue/24/outline";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";

const showNotification = ref(false);
const isNavMinimized = ref(localStorage.getItem("navbarMinimized") === "true");
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

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
