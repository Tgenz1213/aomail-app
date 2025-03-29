<template>
    <div v-if="hasEmails" class="pb-6">
        <div class="sticky top-[48.5px] 2xl:top-[56.5px] z-[50] bg-white">
            <div class="py-6 mr-6 ml-6">
                <div class="group">
                    <div
                        class="bg-stone-100 border border-stone-200 bg-opacity-90 rounded-md cursor-pointer hover:bg-stone-200 transition-colors duration-150"
                        @click="toggleEmailVisibility"
                    >
                        <div class="flex px-3 py-2">
                            <div class="flex items-center gap-2">
                                <CheckIcon class="w-6 h-6 text-stone-500" />
                                <p class="text-sm font-semibold tracking-wide text-stone-600">
                                    {{ $t("constants.ruleModalConstants.read") }}
                                </p>
                            </div>
                            <div
                                class="ml-2 flex gap-x-1 items-center opacity-0 group-hover:opacity-100 transition-opacity duration-150"
                            >
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
                                <p>{{ $t("constants.userActions.clickToSeeReadEmails") }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex gap-x-2" v-if="!showEmailDescriptions">
            <div class="flex gap-x-2 px-12 pb-4 w-full group">
                <p>
                    {{ $t("homePage.youRead") }}
                    <span class="font-semibold text-gray-900 dark:text-white hover:text-gray-700 w-full">
                        {{ readCount }}
                    </span>
                    <span v-if="readCount === 1">
                        {{ $t("homePage.readEmail") }}
                    </span>
                    <span v-else>
                        {{ $t("homePage.readEmails") }}
                    </span>
                </p>
                <button
                    @click="markAllAsArchive"
                    class="text-xs text-stone-700 bg-stone-200 hover:bg-stone-300 px-3 py-1 rounded-md flex items-center gap-1"
                    :disabled="isMarking.read"
                >
                    <ArchiveBoxIcon class="h-4 w-4 text-stone-700" v-if="!isMarking?.read"/>
                    {{ isMarking?.read ? $t("loading") : $t("markAllAsArchive") }}
                </button>
            </div>
        </div>
        <div class="bg-white py-1 sticky z-[25]"
            :class="[
                replyLater 
                    ? 'top-[85px] 2xl:top-[90px]' 
                    : 'top-[137px] 2xl:top-[146px]'
            ]"
        ></div>
        <div v-if="showEmailDescriptions">
            <div v-for="(emailsByDate, date) in groupedEmails" :key="date" class="px-4">
                <div 
                    class="sticky z-[30] bg-transparent"
                    :class="[
                        replyLater 
                            ? 'top-[85px] 2xl:top-[90px]' 
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
                                    <EmailItem :email="email" color="stone" :replyLater="replyLater" />
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
import { CheckIcon, ArchiveBoxIcon } from "@heroicons/vue/24/outline";
import { Email } from "@/global/types";
import EmailItem from "@/global/components/EmailItem.vue";
import { formatSentDate } from "@/global/formatters";

const props = defineProps<{
    emails: Email[];
    replyLater?: boolean;
}>();

const readCount = inject("readCount") as Ref<number>;
const isMarking = inject("isMarking") as {
    [key: string]: boolean;
};
const archiveReadEmails = inject<() => Promise<void>>("archiveReadEmails");

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

    localEmails.value.forEach((email) => {
        if (email.read) {
            const sentDate = email.sentDate || "Unknown Date";
            if (!grouped[sentDate]) {
                grouped[sentDate] = [];
            }
            grouped[sentDate].push(email);
        }
    });

    Object.values(grouped).forEach((emails) => {
        emails.sort((a, b) => {
            const dateTimeA = new Date(`${a.sentDate} ${a.sentTime}`).getTime();
            const dateTimeB = new Date(`${b.sentDate} ${b.sentTime}`).getTime();
            return dateTimeB - dateTimeA;
        });
    });

    const sortedDates = Object.keys(grouped).sort((a, b) => {
        if (a === "Unknown Date") return 1;
        if (b === "Unknown Date") return -1;
        return new Date(b).getTime() - new Date(a).getTime();
    });

    const orderedGrouped: Record<string, Email[]> = {};
    sortedDates.forEach((date) => {
        orderedGrouped[date] = grouped[date];
    });

    return orderedGrouped;
});

const hasEmails = computed(() => {
    return Object.keys(groupedEmails.value).length > 0;
});

// const nbrEmailsRead = computed(() => {
//     return Object.values(groupedEmails.value).reduce((acc, emails) => acc + emails.length, 0);
// });

function toggleEmailVisibility() {
    showEmailDescriptions.value = !showEmailDescriptions.value;
    localStorage.setItem("showRead", JSON.stringify(showEmailDescriptions.value));
}

const markAllAsArchive = () => {
    archiveReadEmails && archiveReadEmails();
};

onMounted(() => {
    const storedShowRead = localStorage.getItem("showRead");
    if (storedShowRead) {
        showEmailDescriptions.value = JSON.parse(storedShowRead);
    }
});
</script>
