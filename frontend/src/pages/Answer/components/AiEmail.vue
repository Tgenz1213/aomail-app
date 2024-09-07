<template>
    <div class="flex items-center justify-center h-[65px] 2xl:h-[80px]">
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
                    d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z"
                />
            </svg>
            <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500">
                {{ $t("constants.aiAssistant") }}
            </h1>
        </div>
    </div>
    <div class="flex flex-1 flex-col divide-y overflow-y-auto">
        <div class="overflow-y-auto flex-1" style="margin-right: 2px" ref="scrollableDiv">
            <div class="px-10 py-4 2xl:px-13.5 2xl:py-6">
                <div class="flex-grow">
                    <div id="AIContainer"></div>
                </div>
            </div>
        </div>
        <div class="flex flex-col h-[22vh] 2xl:h-[23vh]">
            <textarea
                id="dynamicTextarea"
                @keydown.enter="handleEnterKey"
                @input="adjustHeight"
                v-model="textareaValue"
                class="overflow-y-hidden pt-4 pl-6 flex-1 w-full border-transparent bg-transparent text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 focus:border-transparent focus:bg-transparent focus:ring-0 2xl:pt-5 2xl:pl-7 2xl:text-base"
                :placeholder="$t('constants.instruction')"
            ></textarea>
            <SendAiInstructionButton />
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, provide, Ref, ref } from "vue";
import { getData, postData } from "@/global/fetchData";
import userImage from "@/assets/user.png";
import { i18n } from "@/global/preferences";
import Quill from "quill";

const textareaValue = ref("");
const isWriting = inject<Ref<boolean>>("isWriting") || ref(false);
const AIContainer =
    inject<Ref<HTMLElement | null>>("AIContainer") || ref<HTMLElement | null>(document.getElementById("AIContainer"));
const imageURL = ref<string>(userImage);
const emailSelected = inject<Ref<string>>("emailSelected") || ref("");
const textareaValueSave = inject<Ref<string>>("textareaValueSave") || ref("");
const quill = inject<Ref<Quill | null>>("quill");
const history = inject<Ref<Record<string, any>>>("history") || ref({});
const subjectInput = inject<Ref<string>>("subjectInput") || ref("");
const importance = inject<Ref<string>>("importance") || ref("");

const scrollToBottom = inject<() => void>("scrollToBottom");
const displayMessage = inject<(message: string, aiIcon: string) => void>("displayMessage");
const hideLoading = inject<() => void>("hideLoading");
const loading = inject<() => void>("loading");

provide("handleAIClick", handleAIClick);

onMounted(() => {
    getProfileImage();
});

async function getProfileImage() {
    const result = await getData(`user/social_api/get_profile_image/`, { email: emailSelected.value });
    if (!result.success) return;
    imageURL.value = result.data.profileImageUrl;
}

function handleEnterKey(event: any) {
    if (event.target.id === "dynamicTextarea" && event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        handleAIClick();
    }
}

function displayUserMessage() {
    if (!AIContainer.value) return;

    const messageHTML = `
        <div class="flex pb-12">
            <div class="mr-4 flex">
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                <img src="${imageURL.value}" alt="Profile Image" class="h-14 w-14 rounded-full">
            </span>
            </div>
            <div>
            <p class="font-serif">${textareaValue.value}</p>
            </div>
        </div>
    `;
    AIContainer.value.innerHTML += messageHTML;
    textareaValueSave.value = textareaValue.value;
    textareaValue.value = "";
    scrollToBottom?.();
}

function handleAIClick() {
    if (isWriting.value) {
        return;
    }
    setWriting();
    displayUserMessage();

    if (textareaValueSave.value == "") {
        const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`;
        displayMessage?.(i18n.global.t("constants.sendEmailConstants.noSuggestionsEnteredPleaseTryAgain"), aiIcon);
        return;
    }

    generateNewEmailResponse();
}

const generateNewEmailResponse = async () => {
    if (!AIContainer.value || !quill?.value) return;

    loading?.();
    scrollToBottom?.();

    const result = await postData("api/get_new_email_response/", {
        body: quill?.value.root.innerHTML,
        userInput: textareaValueSave.value,
        subject: subjectInput.value,
        importance: importance.value,
        history: history.value,
    });

    hideLoading?.();

    if (!result.success) {
        const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
        displayMessage?.(i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain"), aiIcon);
        return;
    }

    history.value = result.data.history;
    const quillEditorContainer = quill.value.root;
    quillEditorContainer.innerHTML = result.data.emailBody.replace(
        /(<ul>|<ol>|<\/li>)(?:[\s]+)(<li>|<\/ul>|<\/ol>)/g,
        "$1$2"
    );

    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
    displayMessage?.(i18n.global.t("constants.sendEmailConstants.doesThisResponseSuitYou"), aiIcon);
};

const setWriting = () => {
    isWriting.value = true;
};

function adjustHeight(event: any) {
    const textarea = event.target;
    textarea.style.height = "auto";
    textarea.style.overflowY = "auto";
}
</script>
