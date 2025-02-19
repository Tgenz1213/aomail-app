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
                <div class="bg-orange-100 z-[60] border border-orange-200 bg-opacity-90 rounded-md">
                    <div class="flex px-3 py-2">
                        <div class="flex items-center gap-2">
                            <exclamation-triangle-icon class="w-6 h-6 text-orange-500" />
                            <p class="text-sm font-semibold tracking-wide text-orange-600">
                                {{ $t("constants.ruleModalConstants.important") }}
                            </p>
                        </div>
                        <div class="ml-auto flex items-center space-x-2">
                            <button
                                @click="markAllAsRead"
                                class="text-xs text-orange-700 bg-orange-200 hover:bg-orange-300 px-3 py-1 rounded-md flex items-center gap-1"
                                :disabled="isMarking?.important"
                            >
                                <CheckIcon class="h-4 w-4 text-orange-700" v-if="!isMarking?.important"/>
                                {{ isMarking?.important ? $t("loading") : $t("markAllAsRead") }}
                            </button>
                        </div>
                    </div>
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
                                <EmailItem :email="email" color="orange" :replyLater="replyLater" />
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, inject, computed, watch } from "vue";
import { ExclamationTriangleIcon, CheckIcon } from "@heroicons/vue/24/outline";
import { Email } from "@/global/types";
import EmailItem from "@/global/components/EmailItem.vue";
import { formatSentDate } from "../formatters";

const markCategoryAsRead = inject<(category: 'important' | 'informative' | 'useless') => void>("markCategoryAsRead");
const isMarking = inject<{
    important: boolean;
    informative: boolean;
    useless: boolean;
}>("isMarking");
//const readCount = inject("readCount") as Ref<number>;

const props = defineProps<{
    emails: Email[];
    replyLater?: boolean;
}>();

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

const markAllAsRead = () => {
    markCategoryAsRead && markCategoryAsRead('important');
    /* Problem => not sufficient because it doesn't allow the user to read the emails mark as read if the counter is updated
    const importantEmails = localEmails.value.filter(email => email.priority === 'important' && !email.read);
    const ids = importantEmails.map(email => email.id);
    readCount.value += ids.length;
    localEmails.value = localEmails.value.map(email => {
        if (ids.includes(email.id)) {
            return { ...email, read: true };
        }
        return email;
    });*/
};
</script>
