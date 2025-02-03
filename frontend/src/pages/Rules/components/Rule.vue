<template>
    <div class="absolute right-4 top-4">
        <PencilSquareIcon @click="editRule()" class="w-6 h-6 text-gray-300 hover:text-gray-800 cursor-pointer" />
    </div>
    <div class="flex w-full items-center justify-between space-x-6 p-6">
        <div class="flex-1 truncate">
            <!-- Triggers Section -->
            <div class="space-y-3">
                <!-- Logical Operator -->
                <div class="flex items-center gap-2">
                    <AdjustmentsHorizontalIcon class="w-4 h-4" />
                    <span class="text-sm font-medium">{{ rule.logicalOperator }}</span>
                </div>
                <!-- Email Triggers -->
                <div v-if="hasEmailTriggers" class="space-y-2">
                    <p class="text-sm font-medium text-gray-700">Email Triggers:</p>

                    <!-- Domains -->
                    <div v-if="rule.domains?.length" class="flex flex-wrap gap-1">
                        <span
                            v-for="domain in rule.domains"
                            :key="domain"
                            class="inline-flex items-center rounded-full bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700"
                        >
                            {{ domain }}
                        </span>
                    </div>

                    <!-- Sender Emails -->
                    <div v-if="rule.senderEmails?.length" class="flex flex-wrap gap-1">
                        <span
                            v-for="email in rule.senderEmails"
                            :key="email"
                            class="inline-flex items-center rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700"
                        >
                            {{ email }}
                        </span>
                    </div>

                    <!-- Has Attachments -->
                    <div v-if="rule.hasAttachements" class="flex items-center gap-1">
                        <PaperClipIcon class="w-4 h-4" />
                        <span class="text-xs">Has attachments</span>
                    </div>

                    <!-- Categories triggers -->
                    <div v-if="rule.categories?.length" class="flex flex-wrap gap-1">
                        <span
                            v-for="category in rule.categories"
                            :key="category"
                            class="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-700"
                        >
                            {{ category }}
                        </span>
                    </div>

                    <!-- Priorities triggers -->
                    <div v-if="rule.priorities?.length" class="flex flex-wrap gap-1">
                        <span
                            v-for="priority in rule.priorities"
                            :key="priority"
                            :class="[
                                'inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium',
                                getPriorityClass(priority),
                            ]"
                        >
                            {{ priority }}
                        </span>
                    </div>

                    <!-- Answers triggers -->
                    <div v-if="rule.answers?.length" class="flex flex-wrap gap-1">
                        <span
                            v-for="answer in rule.answers"
                            :key="answer"
                            class="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-700"
                        >
                            {{ answer }}
                        </span>
                    </div>

                    <!-- Relevances triggers -->
                    <div v-if="rule.relevances?.length" class="flex flex-wrap gap-1">
                        <span
                            v-for="relevance in rule.relevances"
                            :key="relevance"
                            class="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-700"
                        >
                            {{ relevance }}
                        </span>
                    </div>

                    <!-- Flags triggers -->
                    <div v-if="rule.flags?.length" class="flex flex-wrap gap-1">
                        <span
                            v-for="flag in rule.flags"
                            :key="flag"
                            class="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-700"
                        >
                            {{ flag }}
                        </span>
                    </div>

                    <!-- Email deal with triggers -->
                    <div v-if="rule.emailDealWith" class="text-sm text-gray-600">"{{ rule.emailDealWith }}"</div>
                </div>
            </div>

            <!-- Actions Section -->
            <div v-if="hasActions" class="mt-4 space-y-3">
                <p class="text-sm font-medium text-gray-700">Actions:</p>

                <!-- Delete Action -->
                <div v-if="rule.actionDelete" class="flex items-center gap-1">
                    <TrashIcon class="w-4 h-4 text-red-500" />
                    <span class="text-xs text-red-600">Delete email</span>
                </div>

                <!-- Category Action -->
                <div v-if="rule.actionSetCategory" class="flex items-center gap-1">
                    <FolderIcon class="w-4 h-4" />
                    <span class="text-xs">Move to {{ rule.actionSetCategory }}</span>
                </div>

                <!-- Priority Action -->
                <div v-if="rule.actionSetPriority" class="flex items-center gap-1">
                    <ExclamationCircleIcon class="w-4 h-4" />
                    <span class="text-xs">Set priority to {{ rule.actionSetPriority }}</span>
                </div>

                <!-- Relevance Action -->
                <div v-if="rule.actionSetRelevance" class="flex items-center gap-1">
                    <SignalIcon class="w-4 h-4" />
                    <span class="text-xs">Set relevance to {{ rule.actionSetRelevance }}</span>
                </div>

                <!-- Answer Action -->
                <div v-if="rule.actionSetAnswer" class="flex items-center gap-1">
                    <ChatBubbleLeftIcon class="w-4 h-4" />
                    <span class="text-xs">Set answer status to {{ rule.actionSetAnswer }}</span>
                </div>

                <!-- Mark As Actions -->
                <div v-if="rule.actionMarkAs?.length" class="flex flex-wrap gap-1">
                    <span
                        v-for="mark in rule.actionMarkAs"
                        :key="mark"
                        class="inline-flex items-center rounded-full bg-yellow-50 px-2 py-0.5 text-xs font-medium text-yellow-700"
                    >
                        Mark as {{ mark }}
                    </span>
                </div>

                <!-- Transfer Recipients -->
                <div v-if="rule.actionTransferRecipients?.length" class="flex flex-col gap-1">
                    <span class="text-xs">Transfer to:</span>
                    <div class="flex flex-wrap gap-1">
                        <span
                            v-for="recipient in rule.actionTransferRecipients"
                            :key="recipient"
                            class="inline-flex items-center rounded-full bg-indigo-50 px-2 py-0.5 text-xs font-medium text-indigo-700"
                        >
                            {{ recipient }}
                        </span>
                    </div>
                </div>

                <!-- Reply Actions -->
                <div v-if="rule.actionReplyPrompt" class="flex flex-col gap-1">
                    <span class="text-xs">Auto-reply:</span>
                    <span class="text-xs text-gray-600">"{{ rule.actionReplyPrompt }}"</span>

                    <div v-if="rule.actionReplyRecipients?.length" class="flex flex-wrap gap-1 mt-1">
                        <span
                            v-for="recipient in rule.actionReplyRecipients"
                            :key="recipient"
                            class="inline-flex items-center rounded-full bg-pink-50 px-2 py-0.5 text-xs font-medium text-pink-700"
                        >
                            {{ recipient }}
                        </span>
                    </div>
                </div>

                <!-- Tags/Flags -->
                <div v-if="rule.actionSetFlags?.length" class="flex flex-wrap gap-1">
                    <span
                        v-for="tag in rule.actionSetFlags"
                        :key="tag"
                        class="inline-flex items-center rounded-full bg-purple-50 px-2 py-0.5 text-xs font-medium text-purple-700"
                    >
                        {{ tag }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import {
    PencilSquareIcon,
    AdjustmentsHorizontalIcon,
    PaperClipIcon,
    TrashIcon,
    FolderIcon,
    ExclamationCircleIcon,
    SignalIcon,
    ChatBubbleLeftIcon,
} from "@heroicons/vue/24/outline";
import { RuleData } from "../utils/types";

const props = defineProps<{
    rule: RuleData;
}>();

const emit = defineEmits<{
    (e: "edit", rule: RuleData): void;
}>();

// Computed helpers
const hasEmailTriggers = computed(() => {
    return (
        props.rule.domains?.length ||
        props.rule.senderEmails?.length ||
        props.rule.hasAttachements ||
        props.rule.categories?.length ||
        props.rule.priorities?.length ||
        props.rule.answers?.length ||
        props.rule.relevances?.length ||
        props.rule.flags?.length ||
        props.rule.emailDealWith
    );
});

const hasActions = computed(() => {
    return (
        props.rule.actionDelete ||
        props.rule.actionSetCategory ||
        props.rule.actionSetFlags?.length ||
        props.rule.actionMarkAs?.length ||
        props.rule.actionTransferRecipients?.length ||
        props.rule.actionReplyPrompt ||
        props.rule.actionReplyRecipients?.length ||
        props.rule.actionSetPriority ||
        props.rule.actionSetRelevance ||
        props.rule.actionSetAnswer
    );
});

// Helper functions
const getPriorityClass = (priority: string) => {
    switch (priority.toLowerCase()) {
        case "important":
            return "bg-red-50 text-red-700";
        case "informative":
            return "bg-blue-50 text-blue-700";
        default:
            return "bg-gray-50 text-gray-700";
    }
};

function editRule() {
    emit("edit", props.rule);
}
</script>
