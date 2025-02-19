<template>
    <div v-if="hasEmails">
        <div 
            class="sticky bg-white z-[50]"
            :class="[
                replyLater 
                    ? 'top-[0px]' 
                    : 'top-[48.5px] 2xl:top-[56.5px]'
            ]"
        >
            <div class="py-6 mr-6 ml-6">
                <div class="bg-gray-100 border border-gray-200 bg-opacity-90 rounded-md">
                    <div class="flex px-3 py-2">
                        <div class="flex items-center gap-2">
                            <trash-icon class="w-6 h-6 text-gray-500" />
                            <p class="text-sm font-semibold tracking-wide text-gray-600">
                                {{ $t("constants.ruleModalConstants.useless") }}
                            </p>
                        </div>
                        <div class="ml-auto flex items-center space-x-2">
                            <button
                                @click="markAllAsRead"
                                class="text-xs text-gray-700 bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded-md flex items-center gap-1"
                                :disabled="isMarking?.useless"
                            >
                                <CheckIcon class="h-4 w-4 text-gray-700" v-if="!isMarking?.useless"/>
                                {{ isMarking?.useless ? $t("loading") : $t("markAllAsRead") }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex gap-x-2">
            <div class="flex gap-x-2 px-12 pb-4 w-full group" @click="toggleEmailVisibility">
                <p class="cursor-pointer">
                    {{ $t("homePage.youReceived") }}
                    <span class="font-semibold text-gray-900 dark:text-white hover:text-gray-700 w-full">
                        {{ uselessCount }}
                    </span>
                    <span v-if="uselessCount === 1">
                        {{ $t("homePage.uselessEmail") }}
                    </span>
                    <span v-else>
                        {{ $t("homePage.uselessEmails") }}
                    </span>
                </p>
                <div :class="`hidden group-hover:block bg-gray-100 border border-gray-200 bg-opacity-90 rounded-md px-2 text-sm text-gray-700`">
                    <div class="flex gap-x-1 items-center">
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
                        <p>{{ $t("constants.userActions.clickToSeeUselessEmails") }}</p>
                    </div>
                </div>
            </div>
            <div class="hidden group-hover/main:block px-2 py-0.5 bg-gray-400 text-white text-sm shadow rounded-xl">
                <div class="flex gap-x-1 items-center">
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
                    <p @click="toggleEmailVisibility" class="cursor-pointer">{{ $t("homePage.clickToSeeTheEmail") }}</p>
                </div>
            </div>
        </div>
        <div class="bg-white py-1 sticky z-[25]"
            :class="[
                replyLater 
                    ? 'top-[80px] 2xl:top-[90px]' 
                    : 'top-[137px] 2xl:top-[146px]'
            ]"
        ></div>
        <div v-if="showEmailDescriptions">
            <div v-for="(emailsByDate, date) in groupedEmails" :key="date" class="px-4">
                <div 
                    class="sticky z-[30] bg-transparent"
                    :class="[
                        replyLater 
                            ? 'top-[80px] 2xl:top-[90px]' 
                            : 'top-[137px] 2xl:top-[146px]'
                    ]"
                >
                    <div class="mx-4 relative z-[40]">
                        <div class="relative">
                            <div class="absolute inset-0 z-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t border-gray-200"></div>
                            </div>
                            <div class="relative flex justify-center z-[40]">
                                <span class="bg-white px-2 text-xs text-gray-500 relative z-[40]">{{ formatSentDate(date) }}</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex px-4 -my-[7.5px]">
                    <div class="w-full">
                        <ul role="list" class="divide-y divide-gray-200">
                            <li v-for="email in emailsByDate" :key="email.id" class="pl-5 relative hover:bg-gray-50 transition-colors duration-150">
                                <div class="py-6">
                                    <EmailItem :email="email" :block="true" :replyLater="replyLater" />
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, ref, Ref, watch, onMounted, inject } from "vue";
import { TrashIcon, CheckIcon } from "@heroicons/vue/24/outline";
import { Email } from "@/global/types";
import EmailItem from "@/global/components/EmailItem.vue";
import { formatSentDate } from "../formatters";

const uselessCount = inject("uselessCount") as Ref<number>;

const props = defineProps<{
    emails: Email[];
    replyLater?: boolean;
}>();

let showEmailDescriptions = ref(false);
const localEmails = ref<Email[]>([]);

watch(
    () => props.emails,
    (newEmails) => {
        localEmails.value = [...newEmails];
    },
    { immediate: true, deep: true }
);

const groupedEmails = computed(() => {
    const grouped: Record<string, Email[]> = {};

    localEmails.value
        .filter((email) => !email.read)
        .sort((a, b) => {
            const dateA = a.sentDate ? new Date(`${a.sentDate} ${a.sentTime}`).getTime() : 0;
            const dateB = b.sentDate ? new Date(`${b.sentDate} ${b.sentTime}`).getTime() : 0;
            return dateB - dateA;
        })
        .forEach((email) => {
            const sentDate = email.sentDate || "Unknown Date";
            if (!grouped[sentDate]) {
                grouped[sentDate] = [];
            }
            grouped[sentDate].push(email);
        });

    return grouped;
});

const hasEmails = computed(() => {
    return Object.keys(groupedEmails.value).length > 0;
});

function toggleEmailVisibility() {
    showEmailDescriptions.value = !showEmailDescriptions.value;
    localStorage.setItem("showUseless", JSON.stringify(showEmailDescriptions.value));
}

const markCategoryAsRead = inject<(category: 'important' | 'informative' | 'useless') => void>("markCategoryAsRead");
const isMarking = inject<{
    important: boolean;
    informative: boolean;
    useless: boolean;
}>("isMarking");

const markAllAsRead = () => {
    markCategoryAsRead && markCategoryAsRead('useless');
};

onMounted(() => {
    const storedShowUseless = localStorage.getItem("showUseless");
    if (storedShowUseless) {
        showEmailDescriptions.value = JSON.parse(storedShowUseless);
    }
});
</script>
