<template>
    <div class="absolute right-4 top-4">
        <PencilSquareIcon @click="editRule()" class="w-6 h-6 text-gray-300 hover:text-gray-800 cursor-pointer" />
    </div>
    <div class="flex w-full items-center justify-between space-x-6 p-6">
        <div class="flex-1 truncate">
            <!-- Triggers Section -->
            <div class="space-y-3">
                <p class="text-sm font-medium text-gray-700">{{ $t("rulesPage.modals.common.triggers.title") }}:</p>
                <div class="flex flex-wrap items-center gap-2">
                    <template v-if="hasEmailTriggers">
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

                        <!-- Logical Operator after domains -->
                        <span
                            v-if="rule.domains?.length && hasNextTrigger('domains')"
                            class="px-2 text-sm font-medium text-gray-500"
                        >
                            {{ rule.logicalOperator }}
                        </span>

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

                        <!-- Logical Operator after sender emails -->
                        <span
                            v-if="rule.senderEmails?.length && hasNextTrigger('senderEmails')"
                            class="px-2 text-sm font-medium text-gray-500"
                        >
                            {{ rule.logicalOperator }}
                        </span>

                        <!-- Has Attachments -->
                        <div v-if="rule.hasAttachements" class="flex items-center gap-1">
                            <PaperClipIcon class="w-4 h-4" />
                            <span class="text-xs">
                                {{ $t("rulesPage.modals.common.triggers.types.hasAttachments.label") }}
                            </span>
                        </div>

                        <!-- Logical Operator after attachments -->
                        <span
                            v-if="rule.hasAttachements && hasNextTrigger('hasAttachements')"
                            class="px-2 text-sm font-medium text-gray-500"
                        >
                            {{ rule.logicalOperator }}
                        </span>

                        <!-- Categories -->
                        <div v-if="rule.categories?.length" class="flex flex-wrap gap-1">
                            <span
                                v-for="category in rule.categories"
                                :key="category"
                                class="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-700"
                            >
                                {{ category }}
                            </span>
                        </div>

                        <!-- Logical Operator after categories -->
                        <span
                            v-if="rule.categories?.length && hasNextTrigger('categories')"
                            class="px-2 text-sm font-medium text-gray-500"
                        >
                            {{ rule.logicalOperator }}
                        </span>

                        <!-- Priorities -->
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

                        <!-- Logical Operator after priorities -->
                        <span
                            v-if="rule.priorities?.length && hasNextTrigger('priorities')"
                            class="px-2 text-sm font-medium text-gray-500"
                        >
                            {{ rule.logicalOperator }}
                        </span>

                        <!-- Answers -->
                        <div v-if="rule.answers?.length" class="flex flex-wrap gap-1">
                            <span
                                v-for="answer in rule.answers"
                                :key="answer"
                                class="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-700"
                            >
                                {{ answer }}
                            </span>
                        </div>

                        <!-- Logical Operator after answers -->
                        <span
                            v-if="rule.answers?.length && hasNextTrigger('answers')"
                            class="px-2 text-sm font-medium text-gray-500"
                        >
                            {{ rule.logicalOperator }}
                        </span>

                        <!-- Relevances -->
                        <div v-if="rule.relevances?.length" class="flex flex-wrap gap-1">
                            <span
                                v-for="relevance in rule.relevances"
                                :key="relevance"
                                class="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-700"
                            >
                                {{ relevance }}
                            </span>
                        </div>

                        <!-- Logical Operator after relevances -->
                        <span
                            v-if="rule.relevances?.length && hasNextTrigger('relevances')"
                            class="px-2 text-sm font-medium text-gray-500"
                        >
                            {{ rule.logicalOperator }}
                        </span>

                        <!-- Flags -->
                        <div v-if="rule.flags?.length" class="flex flex-wrap gap-1">
                            <span
                                v-for="flag in rule.flags"
                                :key="flag"
                                class="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-700"
                            >
                                {{ $t(`homePage.flag.${flag.toLowerCase()}`) }}
                            </span>
                        </div>

                        <!-- Logical Operator after flags -->
                        <span
                            v-if="rule.flags?.length && hasNextTrigger('flags')"
                            class="px-2 text-sm font-medium text-gray-500"
                        >
                            {{ rule.logicalOperator }}
                        </span>

                        <!-- Email deal with -->
                        <div v-if="rule.emailDealWith" class="text-sm text-gray-600">"{{ rule.emailDealWith }}"</div>
                    </template>
                </div>
            </div>

            <!-- Actions Section -->
            <div v-if="hasActions" class="mt-4 space-y-3">
                <p class="text-sm font-medium text-gray-700">{{ $t("rulesPage.modals.common.actions.title") }}:</p>
                <div class="flex flex-wrap items-center gap-2">
                    <!-- Delete Action -->
                    <div v-if="rule.actionDelete" class="flex items-center gap-1">
                        <TrashIcon class="w-4 h-4 text-red-500" />
                        <span class="text-xs text-red-600">
                            {{ $t("rulesPage.modals.common.actions.types.delete.label") }}
                        </span>
                    </div>

                    <!-- Category Action -->
                    <div v-if="rule.actionSetCategory" class="flex items-center gap-1">
                        <FolderIcon class="w-4 h-4" />
                        <span class="text-xs">
                            {{ $t("rulesPage.modals.common.actions.types.setCategory.label") }}:
                            {{ rule.actionSetCategory }}
                        </span>
                    </div>

                    <!-- Priority Action -->
                    <div v-if="rule.actionSetPriority" class="flex items-center gap-1">
                        <ExclamationCircleIcon class="w-4 h-4" />
                        <span class="text-xs">
                            {{ $t("rulesPage.modals.common.actions.types.setPriority.label") }}:
                            {{ rule.actionSetPriority }}
                        </span>
                    </div>

                    <!-- Relevance Action -->
                    <div v-if="rule.actionSetRelevance" class="flex items-center gap-1">
                        <SignalIcon class="w-4 h-4" />
                        <span class="text-xs">
                            {{ $t("rulesPage.modals.common.actions.types.setRelevance.label") }}:
                            {{ rule.actionSetRelevance }}
                        </span>
                    </div>

                    <!-- Answer Action -->
                    <div v-if="rule.actionSetAnswer" class="flex items-center gap-1">
                        <ChatBubbleLeftIcon class="w-4 h-4" />
                        <span class="text-xs">
                            {{ $t("rulesPage.modals.common.actions.types.setAnswer.label") }}:
                            {{ rule.actionSetAnswer }}
                        </span>
                    </div>

                    <!-- Mark As Actions -->
                    <div v-if="rule.actionMarkAs?.length" class="flex flex-wrap gap-1">
                        <span
                            v-for="mark in rule.actionMarkAs"
                            :key="mark"
                            class="inline-flex items-center rounded-full bg-yellow-50 px-2 py-0.5 text-xs font-medium text-yellow-700"
                        >
                            {{ $t(`rulesPage.modals.common.actions.types.markAs.options.${mark}`) }}
                        </span>
                    </div>

                    <!-- Transfer Recipients -->
                    <div v-if="rule.actionTransferRecipients?.length" class="flex flex-col gap-1">
                        <span class="text-xs">{{ $t("constants.userActions.transfer") }}:</span>
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
                        <span class="text-xs">{{ $t("constants.userActions.reply") }}:</span>
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
                            {{ $t(`homePage.flag.${tag.toLowerCase()}`) }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import {
    PencilSquareIcon,
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

function hasNextTrigger(currentTrigger: keyof RuleData) {
    const triggerOrder: (keyof RuleData)[] = [
        "domains",
        "senderEmails",
        "hasAttachements",
        "categories",
        "priorities",
        "answers",
        "relevances",
        "flags",
        "emailDealWith",
    ];

    const currentIndex = triggerOrder.indexOf(currentTrigger);
    if (currentIndex === -1) return false;

    return triggerOrder.slice(currentIndex + 1).some((trigger) => {
        const value = props.rule[trigger];
        if (trigger === "hasAttachements") return Boolean(value);
        return Array.isArray(value) ? value.length > 0 : Boolean(value);
    });
}
</script>
