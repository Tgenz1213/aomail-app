<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />
    <div class="flex-1 section">
        <div class="mx-auto w-full h-full px-8 2xl:px-12 pt-10">
            <div class="flex flex-col h-full pb-6">
                <div class="flex gap-x-10 w-full">
                    <div class="flex-1 flex flex-col">
                        <div class="relative">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t border-gray-300"></div>
                            </div>
                            <div class="relative flex justify-center">
                                <span class="bg-white px-2 text-sm text-gray-500">
                                    {{ $t("constants.language") }}
                                </span>
                            </div>
                        </div>
                        <div class="pt-10 pb-10">
                            <LanguageSelection />
                        </div>
                    </div>

                    <div class="flex-1 flex flex-col">
                        <div class="relative">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t border-gray-300"></div>
                            </div>
                            <div class="relative flex justify-center">
                                <span class="bg-white px-2 text-sm text-gray-500">
                                    {{ $t("constants.theme") }}
                                </span>
                            </div>
                        </div>
                        <div class="pt-10 pb-10">
                            <div class="relative items-stretch dark:bg-gray-800">
                                <ThemeSelection />
                            </div>
                        </div>
                    </div>
                </div>

                <div class="flex gap-x-10 w-full">
                    <div class="flex-1 flex flex-col">
                        <div class="relative">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t border-gray-300"></div>
                            </div>
                            <div class="relative flex justify-center">
                                <span class="bg-white px-2 text-sm text-gray-500">
                                    {{ $t("constants.timezone") }}
                                </span>
                            </div>
                        </div>
                        <div class="pt-10 pb-10">
                            <TimeZoneSelection></TimeZoneSelection>
                        </div>
                    </div>
                </div>

                <div
                    class="flex-1 w-full h-full rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 text-center"
                >
                    <div class="flex flex-col h-full items-center justify-center">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1"
                            stroke="currentColor"
                            class="w-12 h-12 mx-auto text-gray-400"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M11.42 15.17 17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 0 0 4.486-6.336l-3.276 3.277a3.004 3.004 0 0 1-2.25-2.25l3.276-3.276a4.5 4.5 0 0 0-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437 1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008Z"
                            />
                        </svg>
                        <span class="mt-2 block text-sm font-semibold text-gray-900">
                            {{ $t("constants.underDevelopment") }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { getData, postData } from "@/global/fetchData";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { API_BASE_URL } from "@/global/const";
import NotificationTimer from "@/components/NotificationTimer.vue";
import { i18n } from "@/global/Settings/preferences";
import TimeZoneSelection from "@/pages/Settings/components/TimeZoneSelection.vue";

const userEmailDescription = ref("");
const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

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
