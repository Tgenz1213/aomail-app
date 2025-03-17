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
            <div
                :style="{ width: manualEmailWidth + '%' }"
                class="flex flex-col bg-white lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full overflow-y-auto"
            >
                <div class="sticky top-0 bg-white z-[10] pb-4">
                    <div class="flex items-center h-[65px] justify-center lg:py-5 2xl:h-[80px] min-h-6">
                        <div class="flex gap-x-3 items-center">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke-width="1"
                                stroke="currentColor"
                                class="w-6 h-6 2xl:w-7 2xl:h-7"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672ZM12 2.25V4.5m5.834.166-1.591 1.591M20.25 10.5H18M7.757 14.743l-1.59 1.59M6 10.5H3.75m4.007-4.243-1.59-1.59"
                                />
                            </svg>
                            <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500">
                                {{ $t("constants.manualSearch") }}
                            </h1>
                        </div>
                    </div>
                    <SearchMenu class="w-full mb-4" />
                </div>
                <EmailList class="flex-1 flex flex-col w-full px-6 pt-2 mb-4" />
            </div>
            <div class="drag-wrapper">
                <div class="separator"></div>
                <div class="drag-overlay" @mousedown="initDrag"></div>
            </div>
            <div
                :style="{ width: aiEmailWidth + '%' }"
                class="flex flex-col bg-gray-50 lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full"
            >
                <AiSearchMenu />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, provide, watch, Ref } from "vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { AttachmentType, Recipient, Email, EmailLinked } from "@/global/types";
import { i18n } from "@/global/preferences";
import { getData } from "@/global/fetchData";
import Navbar from "@/global/components/Navbar.vue";
import SearchMenu from "./components/SearchMenu.vue";
import AiSearchMenu from "./components/AiSearchMenu.vue";
import EmailList from "./components/EmailList.vue";
import userImage from "@/assets/user.png";
import { EmailApiListType } from "./utils/types";
import { AOMAIL_SEARCH_KEY, API_SEARCH_KEY } from "@/global/const";
import { KeyValuePair } from "@/global/types";

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

let isEmailhere = ref(false);
const startDate = ref("");
const selectedInterval = ref("");
const selectedSearchIn = ref(null);
const selectedPerson = ref<Recipient[]>([]);
const fromSelectedPerson = ref<Recipient[]>([]);
const selectedRecipients = ref<Recipient[]>([]);
const attachmentsSelected = ref<AttachmentType[]>([]);
const people = ref<Recipient[]>([]);
const selectedPeople = ref<Recipient[]>([]);
const emailsLinked = ref<EmailLinked[]>([]);
const contacts: Recipient[] = [];
const queryGetRecipients = ref("");
const emailIds = ref<number[]>([]);
const emailList = ref<Email[]>([]);
const isNavMinimized = ref(localStorage.getItem("navbarMinimized") === "true");
const manualEmailWidth = ref(65);
const aiEmailWidth = ref(35);
const isDragging = ref(false);
const startX = ref(0);
const startManualWidth = ref(0);
const startAiWidth = ref(0);
const initialContainerWidth = ref(0);
const imageURL = ref<string>(userImage);
const emailSelected = ref(localStorage.getItem("email") || "");
const emailApiList = ref<EmailApiListType>({});
const isLoading = ref(false);
const searchModes: KeyValuePair[] = [
    { key: AOMAIL_SEARCH_KEY, value: i18n.global.t("searchPage.searchModes.aomail") },
    { key: API_SEARCH_KEY, value: i18n.global.t("searchPage.searchModes.allEmails") },
];
const selectedSearchMode = ref<KeyValuePair>({
    key: AOMAIL_SEARCH_KEY,
    value: i18n.global.t("searchPage.searchModes.aomail"),
});

watch(selectedSearchMode, (newMode) => {
    console.log("Search mode changed to:", newMode.key);
    selectedSearchMode.value = newMode;
});

onMounted(() => {
    const storedManualWidth = localStorage.getItem("searchManualWidth");
    const storedAiWidth = localStorage.getItem("searchAiWidth");
    if (storedManualWidth && storedAiWidth) {
        manualEmailWidth.value = parseInt(storedManualWidth, 10);
        aiEmailWidth.value = parseInt(storedAiWidth, 10);
    }

    checkLoginStatus();
    fetchEmailLinked();
    fetchRecipients();
});

async function getProfileImage() {
    const result = await getData(`user/social_api/get_profile_image/`, { email: emailSelected.value });
    if (!result.success) return;
    imageURL.value = result.data.profileImageUrl;
}

const filteredPeople = computed(() => {
    if (!contacts || queryGetRecipients.value === "") {
        return contacts || [];
    }
    return contacts.filter((person) => {
        const username = person?.username || "";
        return username.toLowerCase().includes(queryGetRecipients.value.toLowerCase());
    });
});

provide("imageURL", imageURL);
provide("emailSelected", emailSelected);
provide("displayPopup", displayPopup);
provide("filteredPeople", filteredPeople);
provide("people", people);
provide("selectedPeople", selectedPeople);
provide("attachmentsSelected", attachmentsSelected);
provide("startDate", startDate);
provide("selectedInterval", selectedInterval);
provide("selectedRecipients", selectedRecipients);
provide("fromSelectedPerson", fromSelectedPerson);
provide("selectedPerson", selectedPerson);
provide("selectedSearchIn", selectedSearchIn);
provide("selectedSearchMode", selectedSearchMode);
provide("emailIds", emailIds);
provide("emailList", emailList);
provide("emailApiList", emailApiList);
provide("isLoading", isLoading);
provide("loading", () => {
    isLoading.value = true;
});
provide("hideLoading", () => {
    isLoading.value = false;
});
provide("searchModes", searchModes);
provide("selectedSearchMode", selectedSearchMode);

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

const checkLoginStatus = () => {
    const emailList = document.getElementById("emailList");
    if (!emailList) {
        return;
    }
    const hasEmails = emailList.getElementsByClassName("email-item").length > 0;
    isEmailhere.value = hasEmails;
};

async function fetchRecipients() {
    const result = await getData(`user/contacts/`);

    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.contactFetchError"),
            result.error as string
        );
        return;
    }

    contacts.push(...result.data);
}

async function fetchEmailLinked() {
    const result = await getData(`user/emails_linked/`);

    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailLinkedFetchError"),
            result.error as string
        );
        return;
    }

    emailsLinked.value = result.data;
}

const initDrag = (event: MouseEvent) => {
    isDragging.value = true;
    startX.value = event.clientX;
    startManualWidth.value = manualEmailWidth.value;
    startAiWidth.value = aiEmailWidth.value;

    const container = (event.target as HTMLElement).closest(".flex");
    initialContainerWidth.value = container ? container.clientWidth : 0;

    window.addEventListener("mousemove", onDrag);
    window.addEventListener("mouseup", stopDrag);
};

const onDrag = (event: MouseEvent) => {
    if (!isDragging.value) return;

    const deltaX = event.clientX - startX.value;
    if (initialContainerWidth.value === 0) return;

    const deltaPercent = (deltaX / initialContainerWidth.value) * 100;
    let newManualWidth = startManualWidth.value + deltaPercent;
    let newAiWidth = startAiWidth.value - deltaPercent;

    const MIN_WIDTH = 20;
    const MAX_WIDTH = 80;

    if (newManualWidth < MIN_WIDTH) {
        newManualWidth = MIN_WIDTH;
        newAiWidth = 100 - MIN_WIDTH;
    } else if (newAiWidth < MIN_WIDTH) {
        newAiWidth = MIN_WIDTH;
        newManualWidth = 100 - MIN_WIDTH;
    }

    manualEmailWidth.value = newManualWidth;
    aiEmailWidth.value = newAiWidth;
};

const stopDrag = () => {
    if (isDragging.value) {
        isDragging.value = false;
        saveWidths();
        window.removeEventListener("mousemove", onDrag);
        window.removeEventListener("mouseup", stopDrag);
    }
};

const saveWidths = () => {
    localStorage.setItem("searchManualWidth", manualEmailWidth.value.toString());
    localStorage.setItem("searchAiWidth", aiEmailWidth.value.toString());
};
</script>

<style scoped>
div:nth-child(2),
div:nth-child(4) {
    transition: none !important;
}

.drag-wrapper {
    position: relative;
    width: 1px;
    height: 100%;
    cursor: col-resize;
}

.separator {
    position: absolute;
    left: 50%;
    top: 0;
    transform: translateX(-50%);
    width: 0.5px;
    height: 100%;
    background-color: #e0e0e0;
    z-index: 1;
}

.drag-overlay {
    position: absolute;
    left: -3.5px;
    top: 0;
    width: 8px;
    height: 100%;
    background: transparent;
    z-index: 2;
}

.drag-wrapper:hover .separator {
    background-color: #aaa;
}
</style>
