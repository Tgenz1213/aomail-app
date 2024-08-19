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
import { getData, postData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import { Recipient } from "@/global/types";
import Quill from "quill";
import { inject, onMounted, provide, Ref, ref, watch } from "vue";
import SendAiInstructionButton from "./SendAiInstructionButton.vue";

interface EmailMapping {
    [username: string]: string;
}

const imageURL = ref<string>(require("@/assets/user.png"));
const counterDisplay = inject<Ref<number>>("counterDisplay") || ref(0);
const isAIWriting = inject<Ref<boolean>>("isAIWriting") || ref(false);
const AIContainer =
    inject<Ref<HTMLElement | null>>("AIContainer") || ref<HTMLElement | null>(document.getElementById("AIContainer"));
const subjectInput = inject<Ref<string>>("subjectInput") || ref("");
const textareaValue = ref("");
const textareaValueSave = inject<Ref<string>>("textareaValueSave") || ref("");
const selectedPeople = inject<Ref<Recipient[]>>("selectedPeople") || ref([]);
const selectedCC = inject<Ref<Recipient[]>>("selectedCC") || ref([]);
const selectedCCI = inject<Ref<Recipient[]>>("selectedCCI") || ref([]);
const quill = inject<Ref<Quill | null>>("quill");
const stepContainer = inject<Ref<number>>("stepContainer") || ref(0);
const history = inject<Ref<{}>>("history") || ref({});
const selectedFormality = inject<Ref<string>>("selectedFormality") || ref("");
const selectedLength = inject<Ref<string>>("selectedLength") || ref("");
const AiEmailBody = inject<Ref<string>>("AiEmailBody") || ref("");

const displayMessage = inject<(message: string, aiIcon: string) => void>("displayMessage");
const scrollToBottom = inject<() => void>("scrollToBottom");
const loading = inject<() => void>("loading");
const hideLoading = inject<() => void>("hideLoading");

provide("handleAIClick", handleAIClick);
provide("askContent", askContent);
provide("selectedFormality", selectedFormality);
provide("selectedLength", selectedLength);

function handleEnterKey(event: any) {
    if (event.target.id === "dynamicTextarea" && event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        handleAIClick();
    }
}

const setAiWriting = () => {
    isAIWriting.value = true;
};

async function handleAIClick() {
    if (isAIWriting.value) {
        return;
    }
    setAiWriting();
    let messageHTML = "";
    let userInput = textareaValue.value;
    messageHTML = `
      <div class="flex pb-12">
        <div class="mr-4 flex">
          <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
            <img src="${imageURL.value}" alt="Profile Image" class="h-14 w-14 rounded-full">
          </span>
        </div>
        <div>
          <p class="font-serif">${userInput}</p>
        </div>
      </div>
    `;
    if (!AIContainer.value) return;

    AIContainer.value.innerHTML += messageHTML;
    textareaValueSave.value = textareaValue.value;
    textareaValue.value = "";
    scrollToBottom?.();
    setTimeout(async () => {
        if (stepContainer.value === 0) {
            if (textareaValueSave.value == "") {
                const message = i18n.global.t("constants.sendEmailConstants.noRecipientsEntered");
                const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`;
                displayMessage?.(message, aiIcon);
            } else {
                loading?.();
                scrollToBottom?.();
                const result = await postData("api/find_user_ai/", { query: textareaValueSave.value });
                if (!result.success) {
                    const message = i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain");
                    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
                    displayMessage?.(message, aiIcon);
                    return;
                }
                hideLoading?.();
                let noUsersAdded = true;
                let waitforUserChoice = false;
                const mainRecipients = result.data.mainRecipients;
                const ccRecipients = result.data.ccRecipients;
                const bccRecipients = result.data.bccRecipients;
                for (let i = 0; i < mainRecipients.length; i++) {
                    const user = mainRecipients[i];
                    const emails = user.email;
                    if (emails.length == 1) {
                        const person = { username: user.username, email: emails[0] };
                        selectedPeople.value.push(person);
                        mainRecipients.splice(i, 1);
                        noUsersAdded = false;
                        i--;
                    }
                }
                for (let i = 0; i < ccRecipients.length; i++) {
                    const user = ccRecipients[i];
                    const emails = user.email;
                    if (emails.length == 1) {
                        const person = { username: user.username, email: emails[0] };
                        selectedCC.value.push(person);
                        delete ccRecipients[i];
                        ccRecipients.splice(i, 1);
                        noUsersAdded = false;
                        i--;
                    }
                }
                for (let i = 0; i < bccRecipients.length; i++) {
                    const user = bccRecipients[i];
                    const emails = user.email;
                    if (emails.length == 1) {
                        const person = { username: user.username, email: emails[0] };
                        selectedCCI.value.push(person);
                        bccRecipients.splice(i, 1);
                        noUsersAdded = false;
                        i--;
                    }
                }
                if (!AIContainer.value) return;
                if (mainRecipients.length > 0 || ccRecipients.length > 0 || bccRecipients.length > 0) {
                    const messageHTML = `
                                <div class="flex pb-2">
                                    <div class="mr-4 flex">
                                        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
                                            </svg>
                                        </span>
                                    </div>
                                    <div>
                                        <p>${i18n.global.t(
                                            "constants.sendEmailConstants.multipleEmailsFoundForSomeRecipients"
                                        )}</p>
                                    </div>
                                </div>
                            `;
                    AIContainer.value.innerHTML += messageHTML;
                    if (mainRecipients.length > 0) {
                        waitforUserChoice = true;
                        const emailList: EmailMapping[] = [];
                        for (const user of mainRecipients) {
                            for (const email of user.email) {
                                if (email !== "") {
                                    const emailMapping: EmailMapping = {};
                                    emailMapping[user.username] = email;
                                    emailList.push(emailMapping);
                                    noUsersAdded = false;
                                }
                            }
                        }
                        askChoiceRecipier(emailList, "main");
                    }
                    if (ccRecipients.length > 0) {
                        waitforUserChoice = true;
                        const emailList: EmailMapping[] = [];
                        for (const user of ccRecipients) {
                            for (const email of user.email) {
                                if (email !== "") {
                                    const emailMapping: EmailMapping = {};
                                    emailMapping[user.username] = email;
                                    emailList.push(emailMapping);
                                    noUsersAdded = false;
                                }
                            }
                        }
                        askChoiceRecipier(emailList, "cc");
                    }
                    if (bccRecipients.length > 0) {
                        waitforUserChoice = true;
                        const emailList: EmailMapping[] = [];
                        for (const user of bccRecipients) {
                            for (const email of user.email) {
                                if (email !== "") {
                                    const emailMapping: EmailMapping = {};
                                    emailMapping[user.username] = email;
                                    emailList.push(emailMapping);
                                    noUsersAdded = false;
                                }
                            }
                        }
                        askChoiceRecipier(emailList, "bcc");
                    }
                    nextStepRecipier();
                    scrollToBottom?.();
                }
                if (noUsersAdded) {
                    const message = i18n.global.t(
                        "constants.sendEmailConstants.noRecipientsFoundPleaseTryAgainOrEnterManually"
                    );
                    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
                    displayMessage?.(message, aiIcon);
                } else if (!waitforUserChoice) {
                    stepContainer.value = 1;
                    askContent();
                }
            }
        } else if (stepContainer.value == 1) {
            if (!AIContainer.value || !quill?.value) return;
            if (textareaValueSave.value == "") {
                const message = i18n.global.t("constants.sendEmailConstants.noDraftsEnteredPleaseTryAgain");
                const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`;
                displayMessage?.(message, aiIcon);
            } else {
                loading?.();
                scrollToBottom?.();
                const result = await postData("api/new_email_ai/", {
                    inputData: textareaValueSave.value,
                    length: selectedLength.value,
                    formality: selectedFormality.value,
                });
                hideLoading?.();
                if (!result.success) {
                    const message = i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain");
                    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
                    displayMessage?.(message, aiIcon);
                    return;
                }
                subjectInput.value = result.data.subject;
                AiEmailBody.value = result.data.mail;
                stepContainer.value = 2;
                const formattedMail = result.data.mail.replace(/\n/g, "<br>");
                const messageHTML = `
                      <div class="flex pb-12">
                          <div class="mr-4 flex">
                              <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                                </svg>
                              </span>
                          </div>
                          <div>
                              <p><strong>${i18n.global.t("newPage.subject")}</strong> ${result.data.subject}</p>
                              <p><strong>${i18n.global.t("newPage.emailContent")}</strong> ${formattedMail}</p>
                          </div>
                      </div>
                  `;
                AIContainer.value.innerHTML += messageHTML;
                subjectInput.value = result.data.subject;
                const quillEditorContainer = quill.value.root;
                quillEditorContainer.innerHTML = result.data.mail.replace(/<\/p>/g, "</p><p></p>");
                const message = i18n.global.t("constants.sendEmailConstants.emailFeedbackRequest");
                const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
                displayMessage?.(message, aiIcon);
            }
        } else if (stepContainer.value == 2) {
            if (textareaValueSave.value == "") {
                const message = i18n.global.t("constants.sendEmailConstants.noSuggestionsEnteredPleaseTryAgain");
                const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`;
                displayMessage?.(message, aiIcon);
            } else {
                if (!AIContainer.value || !quill?.value) return;

                loading?.();
                scrollToBottom?.();
                const result = await postData("api/improve_draft/", {
                    userInput: textareaValueSave.value,
                    length: selectedLength.value,
                    formality: selectedFormality.value,
                    subject: subjectInput.value,
                    body: AiEmailBody.value,
                    history: history.value,
                });
                hideLoading?.();

                if (!result.success) {
                    const message = i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain");
                    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
                    displayMessage?.(message, aiIcon);
                    return;
                }
                subjectInput.value = result.data.subject;
                AiEmailBody.value = result.data.emailBody;
                history.value = result.data.history;
                const formattedMail = result.data.emailBody.replace(/\n/g, "<br>");
                const messageHTML = `
                      <div class="flex pb-12">
                          <div class="mr-4 flex">
                              <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                                </svg>
                              </span>
                          </div>
                          <div>
                              <p><strong>${i18n.global.t("newPage.subject")}</strong> ${result.data.subject}</p>
                              <p><strong>${i18n.global.t("newPage.emailContent")}</strong> ${formattedMail}</p>
                          </div>
                      </div>
                  `;
                AIContainer.value.innerHTML += messageHTML;
                const quillEditorContainer = quill.value.root;
                quillEditorContainer.innerHTML = result.data.emailBody;
                quillEditorContainer.style.cssText = "p { margin-bottom: 20px; }";

                const message = i18n.global.t("constants.sendEmailConstants.betterEmailFeedbackRequest");
                const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
                displayMessage?.(message, aiIcon);
            }
        }
    }, 0);
}

function adjustHeight(event: any) {
    const textarea = event.target;
    textarea.style.height = "auto";
    textarea.style.overflowY = "auto";
}

const emailSelected = inject<Ref<string>>("emailSelected") || ref("");
watch(emailSelected, () => {
    getProfileImage();
});

onMounted(() => {
    getProfileImage();
});

async function getProfileImage() {
    const result = await getData(`user/social_api/get_profile_image/`, { email: emailSelected.value });
    if (!result.success) return;
    imageURL.value = result.data.profileImageUrl;
}

function askChoiceRecipier(list: any[], type: string) {
    let buttonsHTML = "";
    const firstUsername = Object.keys(list[0])[0];
    const userLabel =
        type === "main"
            ? i18n.global.t("newPage.mainRecipient")
            : type === "cc"
            ? i18n.global.t("newPage.ccRecipient")
            : i18n.global.t("newPage.bccRecipient");
    const usernameHTML = `<div>${i18n.global.t(
        "newPage.forUser"
    )}<strong>${firstUsername}</strong> [${userLabel}]</div>`;

    list.forEach((item, index) => {
        const username = Object.keys(item)[0];
        const email = item[username];
        const buttonLabel = type === "main" ? "main" : type === "cc" ? "cc" : "bcc";
        const buttonId = `button-${buttonLabel}-${index}`;

        // if index is a even number
        if (index % 2 === 0) {
            buttonsHTML += '<div class="mr-4">';
        }

        buttonsHTML += `
            <div class="mr-4">
                <button type="button" id="${buttonId}" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                    ${email}
                </button>
            </div>
        `;

        // if index is an odd number or its the last element
        if (index % 2 == 1 || index === list.length - 1) {
            buttonsHTML += "</div>";
        }
    });

    const messageHTML = `
        <div class="flex pb-1 pl-[72px]">
            <div class="flex flex-col">
                ${usernameHTML}
                <br>
                ${buttonsHTML}
            </div>
        </div>
        <br>
    `;

    if (!AIContainer.value) return;

    AIContainer.value.innerHTML += messageHTML;

    list.forEach((item, index) => {
        const buttonLabel = type === "main" ? "main" : type === "cc" ? "cc" : "bcc";
        const buttonId = `button-${buttonLabel}-${index}`;

        setTimeout(() => {
            const button = document.getElementById(buttonId);

            if (!button) return;

            button.addEventListener("click", () => {
                const username = Object.keys(item)[0];
                const email = item[username];

                if (type === "main") {
                    const person = { username: username, email: email };
                    const isPersonAlreadySelected = selectedPeople.value.some((p) => p.email === person.email);
                    if (!isPersonAlreadySelected) {
                        selectedPeople.value.push(person);
                    }
                } else if (type === "cc") {
                    const person = { username: username, email: email };
                    const isPersonAlreadySelected = selectedCC.value.some((p) => p.email === person.email);
                    if (!isPersonAlreadySelected) {
                        selectedCC.value.push(person);
                    }
                } else {
                    const person = { username: username, email: email };
                    const isPersonAlreadySelected = selectedCCI.value.some((p) => p.email === person.email);
                    if (!isPersonAlreadySelected) {
                        selectedCCI.value.push(person);
                    }
                }
            });
        }, 0);
    });
}

function askContent() {
    if (!AIContainer.value) return;
    const message = i18n.global.t("constants.sendEmailConstants.draftEmailRequest");
    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
    displayMessage?.(message, aiIcon);
}

function nextStepRecipier() {
    if (!AIContainer.value) return;
    const messageHTML = `
      <div class="flex pb-12 pl-[72px]">
        <div class="flex flex-col">
          <div class="flex mt-4">
            <div class="mr-4">
              <button type="button" id="nextButton" class="flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-gray-900 text-white hover:bg-black border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
                ${i18n.global.t("newPage.moveToNextStep")}
              </button>
          </div>
        </div>
      </div>
    `;

    AIContainer.value.innerHTML += messageHTML;

    setTimeout(() => {
        const nextButton = document.getElementById("nextButton");
        if (nextButton) {
            nextButton.addEventListener("click", () => {
                stepContainer.value = 1;
                askContent();
            });
        }
    }, 0);
}
</script>
