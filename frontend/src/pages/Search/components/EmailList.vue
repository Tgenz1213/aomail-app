<template>
    <div class="flex-1 flex flex-col py-2" id="emailList">
        <div class="h-full overflow-y-auto hide-scrollbar">
            <template v-if="isLoading">
                <div class="flex flex-col items-center justify-center h-full">
                    <svg
                        class="animate-spin h-12 w-12 text-black"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                    >
                        <circle
                            class="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            stroke-width="4"
                        ></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                    </svg>
                    <p class="mt-4 text-lg font-semibold">{{ $t("constants.loadingEmails") }}</p>
                </div>
            </template>
            <template v-if="sortedEmailList.length > 0">
                <ul class="">
                    <template v-for="(email, index) in sortedEmailList" :key="email.id">
                        <EmailItem :email="email" />
                        <li v-if="index < sortedEmailList.length - 1" class="flex relative">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t border-gray-200"></div>
                            </div>
                        </li>
                    </template>
                </ul>
            </template>
            <template v-else-if="showEmailApiList">
                <ul class="">
                    <template v-for="(dictEmails, provider) in emailApiList" :key="provider">
                        <div v-for="(emailList, userEmail) in dictEmails" :key="userEmail">
                            <div class="relative w-full py-2">
                                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                    <div class="w-full border-t border-gray-300"></div>
                                </div>
                                <div class="relative flex justify-center">
                                    <span class="bg-gray-100/70 px-4 py-1 text-sm text-gray-600 rounded-full backdrop-blur-sm flex items-center gap-2">
                                        <template v-if="provider === 'google'">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
                                                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                                                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                                                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                                                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                                            </svg>
                                        </template>
                                        <template v-else-if="provider === 'microsoft'">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 23 23">
                                                <path fill="#f25022" d="M1 1h9v9H1z"/>
                                                <path fill="#00a4ef" d="M1 11h9v9H1z"/>
                                                <path fill="#7fba00" d="M11 1h9v9h-9z"/>
                                                <path fill="#ffb900" d="M11 11h9v9h-9z"/>
                                            </svg>
                                        </template>
                                        {{ userEmail }}
                                    </span>
                                </div>
                            </div>
                            <div class="pt-2">
                                <div v-for="email in emailList" :key="email.providerId">
                                    <EmailItem :email="email" />
                                    <li class="flex relative">
                                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                            <div class="w-full border-t border-gray-200"></div>
                                        </div>
                                    </li>
                                </div>
                            </div>
                        </div>
                    </template>
                </ul>
            </template>
            <template v-else>
                <div
                    class="flex flex-col items-center justify-center h-full rounded-lg border-2 border-dashed border-gray-300"
                >
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
                            d="M15.182 16.318A4.486 4.486 0 0012.016 15a4.486 4.486 0 00-3.198 1.318M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z"
                        />
                    </svg>
                    <span class="mt-2 block text-sm font-semibold text-gray-900">
                        {{ $t("searchPage.noResults") }}
                    </span>
                </div>
            </template>
        </div>
    </div>
</template>

<script setup lang="ts">
import { IMPORTANT, INFORMATIVE, USELESS } from "@/global/const";
import { Email } from "@/global/types";
import { computed, inject, Ref, ref, watch } from "vue";
import EmailItem from "./EmailItem.vue";
import { EmailApiListType } from "../utils/types";

const emailList = inject<Ref<Email[]>>("emailList") || ref([]);
const emailApiList = inject<Ref<EmailApiListType>>("emailApiList") || ref<EmailApiListType>({});
let showEmailApiList = false;
const isLoading = inject<Ref<boolean>>("isLoading") || ref(false);

watch(emailApiList, (emailApiList) => {
    showEmailApiList = emailApiList.google !== undefined || emailApiList.microsoft !== undefined;
});

const sortedEmailList = computed(() => {
    const priorityOrder: Record<string, number> = {
        [IMPORTANT]: 0,
        [INFORMATIVE]: 1,
        [USELESS]: 2,
    };

    return [...emailList.value].sort((a, b) => {
        return priorityOrder[a.priority as string] - priorityOrder[b.priority as string];
    });
});
</script>

<style scoped>
.hide-scrollbar {
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;     /* Firefox */
}

.hide-scrollbar::-webkit-scrollbar {
    display: none;             /* Chrome, Safari and Opera */
}
</style>
