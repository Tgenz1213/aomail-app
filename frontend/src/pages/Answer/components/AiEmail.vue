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
import { inject, provide, Ref, ref } from "vue";

const textareaValue = ref("");
const isWriting = inject<Ref<boolean>>("isWriting") || ref(false);
const AIContainer =
    inject<Ref<HTMLElement | null>>("AIContainer") || ref<HTMLElement | null>(document.getElementById("AIContainer"));

provide("handleAIClick", handleAIClick);

function handleEnterKey(event: any) {
    if (event.target.id === "dynamicTextarea" && event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        handleAIClick();
    }
}

async function handleAIClick() {
    if (!AIContainer.value) return;
    if (isWriting.value) {
        return;
    }
    setWriting();
}

const setWriting = () => {
    isWriting.value = true;
};

function adjustHeight(event: any) {
    const textarea = event.target;
    textarea.style.height = "auto";
    textarea.style.overflowY = "auto";
}
</script>
