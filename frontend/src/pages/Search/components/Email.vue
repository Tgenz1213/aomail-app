<template>
    <li class="group flex justify-between items-center py-2 email-item" @click="toggleHiddenParagraph(index)">
        <div class="flex flex-col justify-center">
            <span class="font-semibold text-sm leading-6">
                {{ email.sender.name }}
                - {{ email.sender.email }}
                <span class="font-normal ml-2 text-gray-600 text-xs">
                    {{ email.sentDate }}
                </span>
            </span>
            <span class="text-sm gray-600">{{ email.subject }} - {{ email.oneLineSummary }}</span>
            <div v-if="showSummary" class="py-1">
                <p class="text-xs">{{ email.shortSummary }}</p>
            </div>
            <div class="mt-1 flex space-x-2">
                <span
                    v-if="email.priority === 'important'"
                    class="inline-flex items-center rounded-md bg-orange-50 px-2 py-1 text-xs font-medium text-orange-700 ring-1 ring-inset ring-orange-600/10"
                >
                    Important
                </span>
                <span
                    v-else-if="email.priority === 'informative'"
                    class="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10"
                >
                    Informative
                </span>
                <span
                    v-else
                    class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10"
                >
                    Useless
                </span>

                <span
                    class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10"
                >
                    {{ email.category }}
                </span>

                <span
                    v-if="email.read"
                    class="inline-flex items-center rounded-md bg-stone-50 px-2 py-1 text-xs font-medium text-stone-600 ring-1 ring-inset ring-stone-500/10"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke-width="1.5"
                        stroke="currentColor"
                        class="h-4 w-4 mr-1"
                    >
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                    </svg>
                    Lu
                </span>
                <span
                    v-bind:class="{
                        'hidden group-hover:block px-1.5 text-white shadow rounded-xl inline-flex': true,
                        'bg-orange-300': email.priority === 'important',
                        'bg-blue-300': email.priority === 'informative',
                        'bg-gray-300': email.priority !== 'important' && email.priority !== 'informative',
                    }"
                >
                    <div class="flex gap-x-1 items-center justify-center h-full">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1.5"
                            stroke="currentColor"
                            class="w-4 h-4"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5"
                            />
                        </svg>
                        <p class="text-xs">
                            {{ $t("constants.userActions.clickToSeeTheSummary") }}
                        </p>
                    </div>
                </span>
            </div>
        </div>
        <span class="isolate inline-flex items-center rounded-2xl">
            <div class="relative group">
                <button
                    @click.stop="openMail(email.id)"
                    class="border border-black text-black rounded-full px-2 py-1 hover:bg-gray-200 focus:outline-none focus:border-gray-500 flex items-center gap-x-2 justify-center"
                >
                    <EyeIcon class="w-5 h-5" />
                    Voir
                </button>
            </div>
        </span>
    </li>
</template>

<script setup lang="ts">
import { postData } from "@/global/fetchData";
import { inject } from "vue";
import { EyeIcon } from "@heroicons/vue/24/outline";

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

function toggleHiddenParagraph(index: any) {
    // fixable if email displayed is scoped alone => create a var cosnt showSummary = ref(false)
    // sortedEmailList.value[index].showSummary = !sortedEmailList.value[index].showSummary;
}

async function openMail(emailId: number) {
    const result = await postData("user/get_email_content/", {
        id: emailId,
    });

    if (!result.success) {
        displayPopup?.("error", "Failed to open the email", result.error as string);
    }

    // todo: find the category and update the variable category
    // const emailIndex = emailList.value.findIndex((email: Email) => email.id === emailId);

    // if (emailIndex !== -1) {
    //     emailList.value[emailIndex] = {
    //         ...emailList.value[emailIndex],
    //         htmlContent: result.data.htmlContent,
    //         category: "",
    //     };

    //     selectedEmail.value = emailList.value[emailIndex];
    //     isModalSeeOpen.value = true;
    // }
}
</script>
