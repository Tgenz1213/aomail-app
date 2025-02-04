<template>
    <div class="relative">
        <div v-if="isOpen" class="absolute left-0 right-0 z-50">
            <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200 max-h-[80vh] overflow-hidden">
                <button
                    type="button"
                    @click="resetFilters"
                    class="m-2 absolute top-0 right-0 bg-gray-700 px-8 2xl:px-10 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center justify-between 2xl:text-lg rounded-md"
                >
                    Reset Filters
                </button>

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

                <!-- Scrollable content -->
                <div class="overflow-y-hidden max-h-[60vh]">
                    <!-- Triggers Section -->
                    <div class="border rounded-md">
                        <button
                            @click="sections.triggers = !sections.triggers"
                            class="w-full flex justify-between items-center p-3 text-left"
                        >
                            <span class="text-sm font-medium text-gray-900">Triggers</span>
                            <ChevronDownIcon
                                class="h-5 w-5 text-gray-500"
                                :class="{ 'transform rotate-180': sections.triggers }"
                            />
                        </button>

                        <div v-if="sections.triggers" class="p-4 border-t space-y-4">
                            <!-- Email Triggers -->
                            <div class="space-y-4">
                                <h4 class="text-sm font-medium text-gray-700">Email Triggers</h4>

                                <div>
                                    <label class="block text-sm text-gray-700">Email Domains</label>
                                    <div class="space-y-2">
                                        <div class="text-xs text-gray-500">
                                            Enter domains to match (e.g., "gmail.com", "esaip.org").
                                        </div>
                                        <TagInput
                                            v-model="domains"
                                            placeholder="Add domain (e.g. gmail.com, esaip.org)"
                                            :validate="validateDomain"
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Sender Emails</label>
                                    <TagInput
                                        v-model="senderEmails"
                                        placeholder="Add email address"
                                        :validate="validateEmail"
                                    />
                                </div>

                                <div class="flex items-center">
                                    <input
                                        id="hasAttachments"
                                        v-model="hasAttachments"
                                        type="checkbox"
                                        class="h-4 w-4 rounded border-gray-300 text-gray-600 focus:ring-gray-500"
                                    />
                                    <label for="hasAttachments" class="ml-2 text-sm text-gray-700">
                                        Has attachments
                                    </label>
                                </div>
                            </div>

                            <!-- AI Processing Triggers -->
                            <div class="space-y-4">
                                <h4 class="text-sm font-medium text-gray-700">AI Processing Triggers</h4>

                                <div>
                                    <label class="block text-sm text-gray-700">Categories</label>
                                    <multiselect
                                        v-model="selectedCategoriesNames"
                                        :options="categoryOptions.map((c: Category) => c.name)"
                                        :multiple="true"
                                        placeholder="Select categories"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Priorities</label>
                                    <multiselect
                                        v-model="selectedPriorities"
                                        :options="priorityOptions"
                                        :multiple="true"
                                        placeholder="Select priorities"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Answer Requirements</label>
                                    <multiselect
                                        v-model="selectedAnswers"
                                        :options="answerOptions"
                                        :multiple="true"
                                        placeholder="Select answer requirements"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Relevance</label>
                                    <multiselect
                                        v-model="selectedRelevance"
                                        :options="relevanceOptions"
                                        :multiple="true"
                                        placeholder="Select relevance levels"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Flags</label>
                                    <multiselect
                                        v-model="selectedFlags"
                                        :options="flagOptions"
                                        :multiple="true"
                                        placeholder="Select flags"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Email Content Deals With</label>
                                    <textarea
                                        v-model="emailDealWith"
                                        rows="2"
                                        class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                        placeholder="Describe what the email content should deal with..."
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, ref, watch } from "vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
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
        emailDealWith?: string;
    };
}>();

const emit = defineEmits<{
    (e: "update:filters", filters: object): void;
    (e: "fetchRules"): void;
}>();

// Section visibility state
const sections = ref({
    triggers: true,
});

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
const emailDealWith = ref(props.initialFilters?.emailDealWith || "");

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
        emailDealWith,
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
            emailDealWith: emailDealWith.value,
        });
    },
    { deep: true }
);

const resetFilters = () => {
    emit("update:filters", {});
    emit("fetchRules");
};

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
    // Remove @ prefix if present
    const cleanDomain = domain.startsWith("@") ? domain.slice(1) : domain;

    // Domain can contain letters, numbers, dots, and hyphens
    // Must have at least one dot
    // Each part must start and end with alphanumeric
    const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9](\.[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])+$/;

    return domainRegex.test(cleanDomain);
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
