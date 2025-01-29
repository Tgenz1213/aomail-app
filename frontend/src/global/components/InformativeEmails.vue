<template>
<div v-if="hasEmails">
  <div class="sticky top-[48.5px] 2xl:top-[56.5px] z-[50] bg-white">
    <div class="py-6 mr-6 ml-6">
      <div class="bg-blue-100 z-[60] border border-blue-200 bg-opacity-90 rounded-md">
        <div class="flex px-3 py-2">
          <div class="flex items-center gap-2">
            <information-circle-icon class="w-6 h-6 text-blue-500" />
            <p class="text-sm font-semibold tracking-wide text-blue-600">
              {{ $t("constants.ruleModalConstants.informative") }}
            </p>
          </div>
          <div class="ml-auto flex items-center space-x-2">
            <button
              @click="markAllAsRead"
              class="text-xs text-blue-700 bg-blue-200 hover:bg-blue-300 px-3 py-1 rounded-md flex items-center gap-1"
              :disabled="isMarking?.informative"
            >
              <CheckIcon v-if="!isMarking?.informative" class="h-4 w-4 text-blue-700" />
              {{ isMarking?.informative ? $t("loading") : $t("markAllAsRead") }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-for="(emailsByDate, date) in groupedEmails" :key="date" class="px-4">
    <div class="sticky top-[137px] 2xl:top-[146px] z-[30] bg-white">
      <div class="mx-4">
        <div class="relative">
          <div class="absolute inset-0 z-0 flex items-center" aria-hidden="true">
            <div class="w-full border-t border-gray-200"></div>
          </div>
          <div class="relative flex justify-center">
            <span class="bg-white px-2 text-xs text-gray-500">{{ formatSentDate(date) }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="flex px-4 py-4">
      <div class="flex">
        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-blue-100">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-6 h-6 text-blue-500"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z"
            />
          </svg>
        </span>
      </div>
      <div class="ml-6 flex-grow">
        <div class="overflow-hidden border-l-4 border-blue-200 hover:rounded-l-xl" style="overflow: visible">
          <ul role="list" class="divide-y divide-gray-200">
            <li v-for="email in emailsByDate" :key="email.id" class="px-6 md:py-5 2xl:py-6">
              <EmailItem :email="email" color="blue" :replyLater="replyLater" />
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>

</template>

<script setup lang="ts">
import { ref, inject, computed, watch } from "vue";
import { Email } from "@/global/types";
import EmailItem from "@/global/components/EmailItem.vue";
import { formatSentDate } from "../formatters";
import { InformationCircleIcon, CheckIcon } from "@heroicons/vue/24/outline";

const markCategoryAsRead = inject<(category: 'important' | 'informative' | 'useless') => void>("markCategoryAsRead");
const isMarking = inject<{
    important: boolean;
    informative: boolean;
    useless: boolean;
}>("isMarking");

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

/**
 * Handler for the "Mark All as Read" button
 */
const markAllAsRead = () => {
    markCategoryAsRead && markCategoryAsRead('informative');
};
</script>
