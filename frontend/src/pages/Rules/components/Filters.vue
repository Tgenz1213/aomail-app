<template>
    <div class="relative">
        <div v-if="isOpen" class="absolute left-0 right-0 z-50">
            <div class="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
                <div class="space-y-4">
                    <h2 class="text-lg font-semibold mb-4">{{ $t("rulesPage.advancedFilters") }}</h2>

                    <!-- Block Filter -->
                    <div class="mb-4">
                        <label for="block" class="block text-sm font-medium text-gray-700">
                            {{ $t("rulesPage.blockSender") }}
                        </label>
                        <input
                            id="block"
                            v-model="block"
                            type="checkbox"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                        />
                    </div>

                    <!-- Category Name Filter -->
                    <div class="mb-4">
                        <label for="categoryName" class="block text-sm font-medium text-gray-700">
                            {{ $t("rulesPage.categoryName") }}
                        </label>
                        <input
                            id="categoryName"
                            v-model="categoryName"
                            type="text"
                            placeholder="Category associated with the rule"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                        />
                    </div>

                    <!-- Priority Filter -->
                    <div class="mb-4">
                        <label for="priority" class="block text-sm font-medium text-gray-700">
                            {{ $t("rulesPage.priority") }}
                        </label>
                        <select
                            id="priority"
                            v-model="priority"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                        >
                            <option value="" disabled>{{ $t("rulesPage.selectPriority") }}</option>
                            <option
                                v-for="priorityOption in priorities"
                                :key="priorityOption.key"
                                :value="priorityOption.key"
                            >
                                {{ priorityOption.label }}
                            </option>
                        </select>
                    </div>

                    <!-- Sender Name Filter -->
                    <div class="mb-4">
                        <label for="senderName" class="block text-sm font-medium text-gray-700">
                            {{ $t("rulesPage.senderName") }}
                        </label>
                        <input
                            id="senderName"
                            v-model="senderName"
                            type="text"
                            placeholder="Sender name associated with the rule"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                        />
                    </div>

                    <!-- Sender Email Filter -->
                    <div class="mb-4">
                        <label for="senderEmail" class="block text-sm font-medium text-gray-700">
                            {{ $t("rulesPage.senderEmail") }}
                        </label>
                        <input
                            id="senderEmail"
                            v-model="senderEmail"
                            type="text"
                            placeholder="Sender email associated with the rule"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, inject, Ref } from "vue";
import { IMPORTANT, INFORMATIVE, USELESS } from "@/global/const";
import { i18n } from "@/global/preferences";

const priorities = ref([
    { key: IMPORTANT.toLocaleLowerCase(), label: i18n.global.t("constants.ruleModalConstants.important") },
    { key: INFORMATIVE.toLocaleLowerCase(), label: i18n.global.t("constants.ruleModalConstants.informative") },
    { key: USELESS.toLocaleLowerCase(), label: i18n.global.t("constants.ruleModalConstants.useless") },
]);

const block = inject<Ref<boolean | null>>("block") || ref(null);
const categoryName = inject<Ref<string>>("categoryName") || ref("");
const priority = inject<Ref<string>>("priority") || ref("");
const senderName = inject<Ref<string>>("senderName") || ref("");
const senderEmail = inject<Ref<string>>("senderEmail") || ref("");

defineProps<{
    isOpen: boolean;
}>();
</script>
