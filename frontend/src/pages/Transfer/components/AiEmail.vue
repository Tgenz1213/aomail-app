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
    <div
      class="overflow-y-auto flex-1"
      style="margin-right: 2px"
      ref="scrollableDiv"
    >
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
import { i18n } from "@/global/preferences";
import { AiRecipient, Recipient } from "@/global/types";
import { inject, Ref, ref } from "vue";
import SendAiInstructionButton from "@/global/components/SendAiInstructionButton.vue";
import { postData } from "@/global/fetchData";

const isWriting = inject<Ref<boolean>>("isWriting") || ref(false);
const AIContainer =
  inject<Ref<HTMLElement | null>>("AIContainer") ||
  ref<HTMLElement | null>(document.getElementById("AIContainer"));
const textareaValue = ref("");
const selectedPeople = inject<Ref<Recipient[]>>("selectedPeople") || ref([]);
const selectedCC = inject<Ref<Recipient[]>>("selectedCC") || ref([]);
const selectedBCC = inject<Ref<Recipient[]>>("selectedBCC") || ref([]);
const textareaValueSave = inject<Ref<string>>("textareaValueSave") || ref("");
const imageURL = inject<Ref<string>>("imageURL") || ref("");

const displayMessage =
  inject<(message: string, aiIcon: string) => void>("displayMessage");
const scrollToBottom = inject<() => void>("scrollToBottom");
const loading = inject<() => void>("loading");
const hideLoading = inject<() => void>("hideLoading");

function handleEnterKey(event: KeyboardEvent) {
  const target = event.target as HTMLElement | null;

  if (
    target &&
    target.id === "dynamicTextarea" &&
    event.key === "Enter" &&
    !event.shiftKey
  ) {
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

async function handleAIClick() {
  if (!AIContainer.value) return;
  if (isWriting.value) {
    return;
  }
  setWriting();
  displayUserMessage?.();
  findUserAi();
}

const setWriting = () => {
  isWriting.value = true;
};

async function findUserAi() {
  if (textareaValueSave.value === "") {
    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`;
    displayMessage?.(
      i18n.global.t("constants.sendEmailConstants.noRecipientsEntered"),
      aiIcon
    );
  } else {
    loading?.();
    scrollToBottom?.();

    const result = await postData("find_user_ai/", {
      query: textareaValueSave.value,
    });
    if (!result.success) {
      const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
      displayMessage?.(
        i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain"),
        aiIcon
      );
      return;
    }
    hideLoading?.();

    const mainRecipients = result.data.mainRecipients;
    const ccRecipients = result.data.ccRecipients;
    const bccRecipients = result.data.bccRecipients;

    processRecipients(mainRecipients, ccRecipients, bccRecipients);
  }
}

function processRecipients(
  mainRecipients: AiRecipient[],
  ccRecipients: AiRecipient[],
  bccRecipients: AiRecipient[]
) {
  let noUsersAdded = true;

  noUsersAdded =
    processSingleEmailRecipients(mainRecipients, selectedPeople.value) &&
    noUsersAdded;
  noUsersAdded =
    processSingleEmailRecipients(ccRecipients, selectedCC.value) &&
    noUsersAdded;
  noUsersAdded =
    processSingleEmailRecipients(bccRecipients, selectedBCC.value) &&
    noUsersAdded;

  if (!AIContainer.value) return;

  if (
    mainRecipients.length > 0 ||
    ccRecipients.length > 0 ||
    bccRecipients.length > 0
  ) {
    displayMultipleEmailsMessage();
    scrollToBottom?.();
  }

  if (noUsersAdded) {
    displayNoRecipientsFoundMessage();
  }
}

function processSingleEmailRecipients(
  recipients: AiRecipient[],
  selectedGroup: Recipient[]
) {
  let noUsersAdded = true;
  for (let i = 0; i < recipients.length; i++) {
    const user = recipients[i];
    const emails = user.email;
    if (emails.length === 1) {
      selectedGroup.push({ username: user.username, email: emails[0] });
      recipients.splice(i, 1);
      noUsersAdded = false;
      i--;
    }
  }
  return noUsersAdded;
}

function displayMultipleEmailsMessage() {
  if (!AIContainer.value) return;
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
}

function displayNoRecipientsFoundMessage() {
  const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
  displayMessage?.(
    i18n.global.t(
      "constants.sendEmailConstants.noRecipientsFoundPleaseTryAgainOrEnterManually"
    ),
    aiIcon
  );
}

function adjustHeight(event: Event) {
  const textarea = event.target as HTMLTextAreaElement | null;

  if (textarea) {
    textarea.style.height = "auto";
    textarea.style.overflowY = "auto";
  }
}
</script>
