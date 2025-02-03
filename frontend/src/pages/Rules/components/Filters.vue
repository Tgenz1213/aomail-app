<template>
    <div class="relative">
        <div v-if="isOpen" class="absolute left-0 right-0 z-50">
            <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
                <div class="space-y-6">
                    <h2 class="text-lg font-semibold mb-4">{{ $t("rulesPage.advancedFilters") }}</h2>

                    <!-- Logical Operator -->
                    <div class="mb-4">
                        <label class="block text-sm font-medium text-gray-700 mb-1">Logical Operator</label>
                        <select
                            v-model="logicalOperator"
                            class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                        >
                            <option value="AND">AND - All conditions must match</option>
                            <option value="OR">OR - Any condition can match</option>
                        </select>
                    </div>

                    <!-- Email Triggers Section -->
                    <div class="border-t pt-4">
                        <h3 class="text-md font-medium text-gray-900 mb-4">Email Triggers</h3>

                        <!-- Domains -->
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Domains</label>
                            <TagInput
                                v-model="domains"
                                placeholder="Add domain (e.g. gmail.com)"
                                :validate="validateDomain"
                            />
                        </div>

                        <!-- Sender Emails -->
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Sender Emails</label>
                            <TagInput
                                v-model="senderEmails"
                                placeholder="Add email address"
                                :validate="validateEmail"
                            />
                        </div>

                        <!-- Has Attachments -->
                        <div class="flex items-center mb-4">
                            <input
                                id="hasAttachments"
                                v-model="hasAttachments"
                                type="checkbox"
                                class="h-4 w-4 rounded border-gray-300 text-gray-600 focus:ring-gray-500"
                            />
                            <label for="hasAttachments" class="ml-2 block text-sm text-gray-700">Has attachments</label>
                        </div>
                    </div>

                    <!-- AI Processing Triggers Section -->
                    <div class="border-t pt-4">
                        <h3 class="text-md font-medium text-gray-900 mb-4">AI Processing Triggers</h3>

                        <!-- Categories -->
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Categories</label>
                            <multiselect
                                v-model="selectedCategoriesNames"
                                :options="categoryOptions"
                                :multiple="true"
                                placeholder="Select categories"
                                track-by="id"
                                label="name"
                                class="multiselect-gray"
                            />
                        </div>

                        <!-- Priorities -->
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Priorities</label>
                            <multiselect
                                v-model="selectedPriorities"
                                :options="priorityOptions"
                                :multiple="true"
                                placeholder="Select priorities"
                                class="multiselect-gray"
                            />
                        </div>

                        <!-- Answer Requirements -->
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Answer Requirements</label>
                            <multiselect
                                v-model="selectedAnswers"
                                :options="answerOptions"
                                :multiple="true"
                                placeholder="Select answer requirements"
                                class="multiselect-gray"
                            />
                        </div>

                        <!-- Relevance -->
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Relevance</label>
                            <multiselect
                                v-model="selectedRelevance"
                                :options="relevanceOptions"
                                :multiple="true"
                                placeholder="Select relevance levels"
                                class="multiselect-gray"
                            />
                        </div>

                        <!-- Flags -->
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Flags</label>
                            <multiselect
                                v-model="selectedFlags"
                                :options="flagOptions"
                                :multiple="true"
                                placeholder="Select flags"
                                class="multiselect-gray"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, ref, watch } from "vue";
import Multiselect from "vue-multiselect";
import TagInput from "./TagInput.vue";
import { i18n } from "@/global/preferences";
import { getData } from "@/global/fetchData";

interface Category {
    id: number;
    name: string;
}

const props = defineProps<{
    isOpen: boolean;
    initialFilters?: {
        logicalOperator?: string;
        domains?: string[];
        senderEmails?: string[];
        hasAttachments?: boolean;
        categories?: string[];
        priorities?: string[];
        answers?: string[];
        relevance?: string[];
        flags?: string[];
    };
}>();

const emit = defineEmits<{
    (e: "update:filters", filters: object): void;
}>();
const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

// Options for dropdowns
let categoryOptions: Category[] = [];
const priorityOptions = ["Important", "Informative", "Useless"];
const answerOptions = ["Answer Required", "Might Require Answer", "No Answer Required"];
const relevanceOptions = ["Highly Relevant", "Possibly Relevant", "Not Relevant"];
const flagOptions = ["Spam", "Scam", "Newsletter", "Notification", "Meeting"];

// Form state
const logicalOperator = ref(props.initialFilters?.logicalOperator || "AND");
const domains = ref<string[]>(props.initialFilters?.domains || []);
const senderEmails = ref<string[]>(props.initialFilters?.senderEmails || []);
const hasAttachments = ref(props.initialFilters?.hasAttachments || false);
const selectedPriorities = ref<string[]>(props.initialFilters?.priorities || []);
const selectedAnswers = ref<string[]>(props.initialFilters?.answers || []);
const selectedRelevance = ref<string[]>(props.initialFilters?.relevance || []);
const selectedFlags = ref<string[]>(props.initialFilters?.flags || []);
const selectedCategoriesNames = ref<string[]>([]);

// Watch for changes and emit updates
watch(
    [
        logicalOperator,
        domains,
        senderEmails,
        hasAttachments,
        selectedCategoriesNames,
        selectedPriorities,
        selectedAnswers,
        selectedRelevance,
        selectedFlags,
    ],
    () => {
        emit("update:filters", {
            logicalOperator: logicalOperator.value,
            domains: domains.value,
            senderEmails: senderEmails.value,
            hasAttachments: hasAttachments.value,
            categories: selectedCategoriesNames.value,
            priorities: selectedPriorities.value,
            answers: selectedAnswers.value,
            relevance: selectedRelevance.value,
            flags: selectedFlags.value,
        });
    },
    { deep: true }
);

// Fetch categories when component mounts
async function fetchCategories() {
    const result = await getData("user/categories/");
    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.failedToFetchCategories"),
            result.error as string
        );
        return;
    }
    categoryOptions = result.data;
}

onMounted(async () => {
    await fetchCategories();
});

// Validation functions
const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

const validateDomain = (domain: string) => {
    const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/;
    return domainRegex.test(domain);
};
</script>

<style>
.multiselect-gray {
    --ms-tag-bg: #f3f4f6;
    --ms-tag-color: #374151;
    --ms-ring-color: rgb(107 114 128 / 0.5);
    --ms-option-bg-selected: #f3f4f6;
}
</style>
