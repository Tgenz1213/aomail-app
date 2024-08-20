<template>
    <div class="absolute right-4 top-4">
        <PencilSquareIcon @click="editRule()" class="w-6 h-6 text-gray-300 hover:text-gray-800 cursor-pointer" />
    </div>
    <div class="flex w-full items-center justify-between space-x-6 p-6">
        <div class="flex-1 truncate">
            <div class="flex items-center space-x-3">
                <h3 class="truncate text-sm font-medium text-gray-900">
                    {{ rule.username }}
                </h3>
            </div>
            <p class="mt-1 mb-4 truncate text-sm text-gray-500">{{ rule.email }}</p>
            <div v-if="rule.category" class="flex gap-1">
                <div class="flex space-x-1 items-center">
                    <ArchiveBoxIcon class="w-4 h-4" />
                    <p class="font-semibold text-sm">{{ $t("constants.category") }}</p>
                </div>
                <span
                    class="inline-flex flex-shrink-0 items-center rounded-full bg-gray-50 px-1.5 py-0.5 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/20"
                >
                    {{ rule.category }}
                </span>
            </div>
            <div v-if="rule.priority !== ''" class="flex gap-1 mt-2">
                <div class="flex space-x-1 items-center">
                    <ExclamationCircleIcon class="w-4 h-4" />
                    <p class="font-semibold text-sm">
                        {{ $t("rulesPage.priorityField") }}
                    </p>
                </div>
                <span
                    v-if="rule.priority === IMPORTANT"
                    class="inline-flex flex-shrink-0 items-center rounded-full bg-red-50 px-1.5 py-0.5 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/20"
                >
                    {{ $t("rulesPage.priorityRule.important") }}
                </span>
                <span
                    v-if="rule.priority === INFORMATIVE"
                    class="inline-flex flex-shrink-0 items-center rounded-full bg-blue-50 px-1.5 py-0.5 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-600/20"
                >
                    {{ $t("rulesPage.priorityRule.informative") }}
                </span>
                <span
                    v-if="rule.priority === USELESS"
                    class="inline-flex flex-shrink-0 items-center rounded-full bg-gray-50 px-1.5 py-0.5 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/20"
                >
                    {{ $t("rulesPage.priorityRule.useless") }}
                </span>
            </div>
            <div v-if="rule.mailStop" class="flex gap-1 mt-2">
                <div class="flex space-x-1 items-center">
                    <ShieldCheckIcon class="w-4 h-4" />
                    <p class="font-semibold text-sm">
                        {{ $t("rulesPage.blockedEmail") }}
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// todo: setup properties and imports
import { ArchiveBoxIcon, ExclamationCircleIcon, ShieldCheckIcon, PencilSquareIcon } from "@heroicons/vue/24/outline";
import { IMPORTANT, INFORMATIVE, USELESS } from "@/global/const";
import { RuleData } from "../utils/types";

const props = defineProps<{
    rule: RuleData;
}>();

const emit = defineEmits<{
    (e: "edit", rule: RuleData): void;
}>();

function editRule() {
    emit("edit", props.rule);
}
</script>
