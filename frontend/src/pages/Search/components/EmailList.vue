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
                        <EmailItem :email="email" :searchMode="selectedSearchMode.key" />
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
                                    <span
                                        class="bg-gray-100/70 px-4 py-1 text-sm text-gray-600 rounded-full backdrop-blur-sm flex items-center gap-2"
                                    >
                                        <img
                                            v-if="provider === GOOGLE"
                                            src="@/assets/logos/google.svg"
                                            alt="Google"
                                            class="w-5 h-5"
                                        />
                                        <img
                                            v-if="provider === MICROSOFT"
                                            src="@/assets/logos/microsoft.svg"
                                            alt="Microsoft"
                                            class="w-5 h-5"
                                        />
                                        {{ userEmail }}
                                    </span>
                                </div>
                            </div>
                            <div class="pt-2">
                                <div v-for="email in emailList" :key="email.providerId">
                                    <EmailItem
                                        :email="email"
                                        :provider_email="userEmail"
                                        :searchMode="selectedSearchMode.key"
                                    />
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
import { GOOGLE, IMPORTANT, INFORMATIVE, MICROSOFT, USELESS } from "@/global/const";
import { Email, KeyValuePair } from "@/global/types";
import { computed, inject, Ref, ref, watch } from "vue";
import EmailItem from "./EmailItem.vue";
import { EmailApiListType } from "../utils/types";

const emailList = inject<Ref<Email[]>>("emailList") || ref([]);
const emailApiList = inject<Ref<EmailApiListType>>("emailApiList") || ref<EmailApiListType>({});
const selectedSearchMode = inject<Ref<KeyValuePair>>("selectedSearchMode")!;
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
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
}

.hide-scrollbar::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
}
</style>
