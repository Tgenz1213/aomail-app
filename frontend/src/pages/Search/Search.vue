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
            <div class="w-[90px] bg-white ring-1 shadow-sm ring-black ring-opacity-5 2xl:w-[100px]">
                <NavBarSmall />
            </div>
            <div
                id="firstMainColumn"
                class="flex flex-col bg-gray-50 lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[700px]"
            >
                <AiSearchMenu />
            </div>
            <div
                id="secondMainColumn"
                class="flex flex-col bg-white lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[700px] overflow-y-auto"
            >
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
                <div class="flex-1 flex flex-col w-full px-6 pt-2 mb-4">
                    <SearchMenu />
                    <EmailList />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, provide } from "vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { AttachmentType, Contact, Email, Recipient } from "@/global/types";
import { i18n } from "@/global/preferences";
import { getData } from "@/global/fetchData";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import SearchMenu from "./components/SearchMenu.vue";
import AiSearchMenu from "./components/AiSearchMenu.vue";
import EmailList from "./components/EmailList.vue";

const people = ref<Recipient[]>([]);
const selectedPeople = ref<Recipient[]>([]);

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

let emailsLinked = ref("");

const contacts: Contact[] = [];
const queryGetContacts = ref("");
const emailIds = ref<number[]>([]);
const emailList = ref<Email[]>([]);

onMounted(async () => {
    checkLoginStatus();
    fetchEmailLinked();
    fetchContacts();
});

const filteredPeople = computed(() => {
    if (!contacts || queryGetContacts.value === "") {
        return contacts || [];
    }
    return contacts.filter((person) => {
        const username = person?.username || "";
        return username.toLowerCase().includes(queryGetContacts.value.toLowerCase());
    });
});

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
provide("emailIds", emailIds);
provide("emailList", emailList);

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

async function fetchContacts() {
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
</script>
