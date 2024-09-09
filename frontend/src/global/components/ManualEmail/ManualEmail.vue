<template>
    <div class="flex flex-col h-full w-full">
        <div class="flex items-center h-[65px] justify-center lg:py-5 2xl:h-[80px] min-h-8">
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
                    {{ $t("constants.userActions.enterManually") }}
                </h1>
            </div>
        </div>
        <div class="flex-1 flex flex-col w-full px-10 pt-4 2xl:px-14 2xl:pt-6 overflow-hidden">
            <div class="flex flex-col space-y-5 h-full w-full">
                <div class="">
                    <RecipientsSection />
                </div>
                <div class="">
                    <SubjectAttachmentsSection />
                </div>
                <div class="flex flex-col h-full space-y-5 pb-4 2xl:pb-6 overflow-hidden">
                    <div class="flex-1 overflow-hidden h-screen border-b-2 rounded-lg">
                        <div id="editor-container" class="flex-1 h-full w-full flex flex-col border-solid">
                            <div id="editor" class="flex-1"></div>
                        </div>
                    </div>
                    <div class="flex gap-x-2 mb-5 2xl:gap-3 2xl:mb-6 items-stretch">
                        <SelectedEmailChoiceButton />
                        <SendEmailButtons />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import SendEmailButtons from "./SendEmailButtons.vue";
import SubjectAttachmentsSection from "./SubjectAttachmentsSection.vue";
import RecipientsSection from "./RecipientsSection.vue";
import SelectedEmailChoiceButton from "./SelectedEmailChoiceButton.vue";
</script>
