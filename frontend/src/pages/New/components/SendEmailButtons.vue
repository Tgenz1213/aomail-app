<template>
    <div class="inline-flex rounded-lg shadow-lg items-stretch">
        <button
            @click="sendEmail"
            class="bg-gray-700 rounded-l-lg px-6 py-2 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center 2xl:px-7 2xl:py-3 2xl:text-lg"
        >
            {{ $t("constants.userActions.send") }}
            <PaperAirplaneIcon class="w-4 2xl:w-5" aria-hidden="true" />
        </button>
        <Menu as="div" class="relative -ml-px block items-stretch">
            <MenuButton
                @click.self="isMenuOpen = false"
                @click="toggleMenu"
                class="relative inline-flex items-center rounded-r-lg px-2 py-2 text-white border-l border-gray-300 bg-gray-700 hover:bg-gray-900 focus:z-10 2xl:px-3 2xl:py-3"
            >
                <span class="sr-only">{{ $t("newPage.openOptions") }}</span>
                <ChevronDownIcon class="h-8 w-5 2xl:h-9 2xl:w-6" aria-hidden="true" />
            </MenuButton>
            <transition
                enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 -translate-y-2"
                enter-to-class="transform opacity-100 translate-y-0"
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 translate-y-0"
                leave-to-class="transform opacity-0 -translate-y-2"
            >
                <MenuItems
                    v-if="isMenuOpen"
                    class="absolute right-0 z-10 -mr-1 bottom-full mb-2 w-56 origin-bottom-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                >
                    <div class="py-1">
                        <button
                            :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']"
                            @click="scheduleSend"
                        >
                            Schedule send
                        </button>
                    </div>
                </MenuItems>
            </transition>
        </Menu>
    </div>
</template>

<script setup lang="ts">
import { MICROSOFT } from "@/global/const";
import { postData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import { EmailLinked, Recipient, UploadedFile } from "@/global/types";
import Quill from "quill";
import { ChevronDownIcon } from "@heroicons/vue/24/outline";
import { inject, onMounted, onUnmounted, Ref, ref } from "vue";

const isMenuOpen = ref(false);
const active = ref(false);
const quill = inject<Ref<Quill | null>>("quill");
const subjectInput = inject<Ref<string>>("subjectInput") || ref("");
const selectedPeople = inject<Ref<Recipient[]>>("selectedPeople") || ref([]);
const fileObjects = inject<Ref<File[]>>("fileObjects") || ref([]);
const selectedCC = inject<Ref<Recipient[]>>("selectedCC") || ref([]);
const selectedCCI = inject<Ref<Recipient[]>>("selectedCCI") || ref([]);
const stepContainer = inject<Ref<number>>("stepContainer") || ref(0);
const emailSelected = inject<Ref<string>>("emailSelected") || ref("");
const AIContainer =
    inject<Ref<HTMLElement | null>>("AIContainer") || ref<HTMLElement | null>(document.getElementById("AIContainer"));
const uploadedFiles = inject<Ref<UploadedFile[]>>("uploadedFiles") || ref([]);
const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const displayMessage = inject<(message: string, aiIcon: string) => void>("displayMessage");
const emailsLinked = inject<Ref<EmailLinked[]>>("emailsLinked", ref([]));

const handleClickOutside = (event: MouseEvent) => {
    const target = event.target as Element;
    if (!target.closest(".relative")) {
        isMenuOpen.value = false;
    }
};

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
    document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
    document.removeEventListener("click", handleClickOutside);
});

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value;
};

function handleKeyDown(event: KeyboardEvent) {
    if (event.ctrlKey && event.key === "Enter") {
        sendEmail();
    }
}

async function sendEmail() {
    if (!AIContainer.value || !quill?.value) return;

    const emailSubject = subjectInput.value;
    const emailBody = quill.value.root.innerHTML;

    if (!emailSubject.trim()) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoSubject")
        );
        return;
    }
    if (emailBody === "<p><br></p>") {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoObject")
        );
        return;
    }
    if (selectedPeople.value.length === 0) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoRecipient")
        );
        return;
    }

    const formData = new FormData();

    formData.append("subject", emailSubject);
    formData.append("message", emailBody);
    fileObjects.value.forEach((file) => formData.append("attachments", file));

    selectedPeople.value.forEach((person) => formData.append("to", person.email));
    if (selectedCC.value.length > 0) {
        selectedCC.value.forEach((person) => formData.append("cc", person.email));
    }
    if (selectedCCI.value.length > 0) {
        selectedCCI.value.forEach((person) => formData.append("cci", person.email));
    }
    formData.append("email", emailSelected.value);

    const result = await postData(`user/social_api/send_email/`, {
        body: formData,
    });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            result.error as string
        );
        return;
    }

    displayPopup?.(
        "success",
        i18n.global.t("constants.popUpConstants.successMessages.success"),
        i18n.global.t("constants.popUpConstants.successMessages.emailSuccessfullySent")
    );

    subjectInput.value = "";
    quill.value.root.innerHTML = "";
    selectedPeople.value = [];
    selectedCC.value = [];
    selectedCCI.value = [];
    stepContainer.value = 0;
    AIContainer.value.innerHTML = "";
    localStorage.removeItem("uploadedFiles");
    uploadedFiles.value = [];
    fileObjects.value = [];

    const message = i18n.global.t("constants.sendEmailConstants.emailRecipientRequest");
    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
    displayMessage?.(message, ai_icon);
}

async function scheduleSend() {
    if (!AIContainer.value || !quill?.value) return;
    const emailSubject = subjectInput.value;
    const emailBody = quill.value.root.innerHTML;

    for (const tupleEmail of emailsLinked.value) {
        if (emailSelected.value === tupleEmail.email && tupleEmail.typeApi !== MICROSOFT) {
            displayPopup?.(
                "error",
                "Email service provider not supported",
                "Scheduled send is only available for Outlook accounts"
            );
            return;
        }
    }

    if (!emailSubject.trim()) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoSubject")
        );
        return;
    } else if (emailBody == "<p><br></p>") {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoObject")
        );
        return;
    } else if (selectedPeople.value.length == 0) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoRecipient")
        );
        return;
    }

    const formData = new FormData();

    formData.append("subject", emailSubject);
    formData.append("message", emailBody);
    fileObjects.value.forEach((file) => formData.append("attachments", file));

    selectedPeople.value.forEach((person) => formData.append("to", person.email));
    if (selectedCC.value.length > 0) {
        selectedCC.value.forEach((person) => formData.append("cc", person.email));
    }
    if (selectedCCI.value.length > 0) {
        selectedCCI.value.forEach((person) => formData.append("cci", person.email));
    }
    formData.append("email", emailSelected.value);
    // TODO: add a modal - for now its HARD coded values! DO NOT PUSH THAT IN PRODUCTION
    formData.append("datetime", "2024-07-02T10:00:00Z");

    const result = await postData(`user/social_api/send_schedule_email/`, {
        body: formData,
    });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
            result.error as string
        );
    }

    displayPopup?.("success", "Email scheduled successfully!", "Your email will be send on time");

    subjectInput.value = "";
    quill.value.root.innerHTML = "";
    selectedPeople.value = [];
    selectedCC.value = [];
    selectedCCI.value = [];
    stepContainer.value = 0;
    AIContainer.value.innerHTML = "";
    localStorage.removeItem("uploadedFiles");
    uploadedFiles.value = [];
    fileObjects.value = [];

    const message = i18n.global.t("constants.sendEmailConstants.emailRecipientRequest");
    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
    displayMessage?.(message, ai_icon);
}
</script>
