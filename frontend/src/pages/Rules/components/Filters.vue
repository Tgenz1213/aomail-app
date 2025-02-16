<template>
    <div class="relative">
        <div v-if="isOpen" class="absolute left-0 right-0 z-50">
            <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200 max-h-[80vh] overflow-hidden">
                <button
                    type="button"
                    @click="resetFilters"
                    class="m-2 absolute top-0 right-0 bg-gray-700 px-8 2xl:px-10 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center justify-between 2xl:text-lg rounded-md"
                >
                    {{ $t("rulesPage.filters.resetFilters") }}
                </button>

                <!-- Logical Operator -->
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                        {{ $t("rulesPage.filters.logicalOperator") }}
                    </label>
                    <select
                        v-model="logicalOperator"
                        class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                    >
                        <option value="AND">{{ $t("rulesPage.filters.logicalOperatorAnd") }}</option>
                        <option value="OR">{{ $t("rulesPage.filters.logicalOperatorOr") }}</option>
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
                            <span class="text-sm font-medium text-gray-900">
                                {{ $t("rulesPage.filters.triggers.title") }}
                            </span>
                            <ChevronDownIcon
                                class="h-5 w-5 text-gray-500"
                                :class="{ 'transform rotate-180': sections.triggers }"
                            />
                        </button>

                        <div v-if="sections.triggers" class="p-4 border-t space-y-4">
                            <!-- Email Triggers -->
                            <div class="space-y-4">
                                <h4 class="text-sm font-medium text-gray-700">
                                    {{ $t("rulesPage.filters.triggers.emailTriggers") }}
                                </h4>

                                <div>
                                    <label class="block text-sm text-gray-700">
                                        {{ $t("rulesPage.filters.triggers.emailDomains") }}
                                    </label>
                                    <div class="space-y-2">
                                        <div class="text-xs text-gray-500">
                                            {{ $t("rulesPage.filters.triggers.emailDomainsHelp") }}
                                        </div>
                                        <TagInput
                                            v-model="domains"
                                            :placeholder="$t('rulesPage.modals.common.addDomain')"
                                            :validate="validateDomain"
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">
                                        {{ $t("rulesPage.filters.triggers.senderEmails") }}
                                    </label>
                                    <TagInput
                                        v-model="senderEmails"
                                        :placeholder="$t('rulesPage.modals.common.addEmailAddress')"
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
                                        {{ $t("rulesPage.filters.triggers.hasAttachments") }}
                                    </label>
                                </div>
                            </div>

                            <!-- AI Processing Triggers -->
                            <div class="space-y-4">
                                <h4 class="text-sm font-medium text-gray-700">
                                    {{ $t("rulesPage.filters.triggers.aiProcessingTriggers") }}
                                </h4>

                                <div>
                                    <label class="block text-sm text-gray-700">
                                        {{ $t("rulesPage.filters.triggers.categories") }}
                                    </label>
                                    <multiselect
                                        v-model="selectedCategoriesNames"
                                        :options="categoryOptions.map((c: Category) => c.name)"
                                        :multiple="true"
                                        :placeholder="$t('rulesPage.modals.common.selectCategory')"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">
                                        {{ $t("rulesPage.filters.triggers.priorities") }}
                                    </label>
                                    <multiselect
                                        v-model="selectedPriorities"
                                        :options="priorityOptions"
                                        :multiple="true"
                                        track-by="key"
                                        label="value"
                                        :placeholder="$t('rulesPage.modals.common.selectPriority')"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">
                                        {{ $t("rulesPage.filters.triggers.answerRequirements") }}
                                    </label>
                                    <multiselect
                                        v-model="selectedAnswers"
                                        :options="answerOptions"
                                        :multiple="true"
                                        track-by="key"
                                        label="value"
                                        :placeholder="$t('rulesPage.modals.common.selectOptions')"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">
                                        {{ $t("rulesPage.filters.triggers.relevance") }}
                                    </label>
                                    <multiselect
                                        v-model="selectedRelevance"
                                        :options="relevanceOptions"
                                        :multiple="true"
                                        track-by="key"
                                        label="value"
                                        :placeholder="$t('rulesPage.modals.common.selectRelevance')"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">
                                        {{ $t("rulesPage.filters.triggers.flags") }}
                                    </label>
                                    <multiselect
                                        v-model="selectedFlags"
                                        :options="flagOptions"
                                        :multiple="true"
                                        track-by="key"
                                        label="value"
                                        :placeholder="$t('rulesPage.modals.common.selectOptions')"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">
                                        {{ $t("rulesPage.filters.triggers.emailContentDealsWith") }}
                                    </label>
                                    <textarea
                                        v-model="emailDealWith"
                                        rows="2"
                                        class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                        :placeholder="$t('rulesPage.filters.triggers.emailContentPlaceholder')"
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
import { KeyValuePair } from "@/global/types";
import {
    ANSWER_REQUIRED,
    HIGHLY_RELEVANT,
    IMPORTANT,
    INFORMATIVE,
    USELESS,
    MIGHT_REQUIRE_ANSWER,
    NO_ANSWER_REQUIRED,
    POSSIBLY_RELEVANT,
    NOT_RELEVANT,
    SPAM,
    SCAM,
    NEWSLETTER,
    NOTIFICATION,
    MEETING,
} from "@/global/const";

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
const priorityOptions: KeyValuePair[] = [
    { key: IMPORTANT, value: i18n.global.t("rulesPage.priorityRule.important") },
    { key: INFORMATIVE, value: i18n.global.t("rulesPage.priorityRule.informative") },
    { key: USELESS, value: i18n.global.t("rulesPage.priorityRule.useless") },
];
const answerOptions: KeyValuePair[] = [
    { key: ANSWER_REQUIRED, value: i18n.global.t("rulesPage.modals.common.triggers.types.answers.options.required") },
    { key: MIGHT_REQUIRE_ANSWER, value: i18n.global.t("rulesPage.modals.common.triggers.types.answers.options.might") },
    { key: NO_ANSWER_REQUIRED, value: i18n.global.t("rulesPage.modals.common.triggers.types.answers.options.none") },
];
const relevanceOptions: KeyValuePair[] = [
    { key: HIGHLY_RELEVANT, value: i18n.global.t("rulesPage.modals.common.triggers.types.relevances.options.high") },
    {
        key: POSSIBLY_RELEVANT,
        value: i18n.global.t("rulesPage.modals.common.triggers.types.relevances.options.possible"),
    },
    { key: NOT_RELEVANT, value: i18n.global.t("rulesPage.modals.common.triggers.types.relevances.options.none") },
];
const flagOptions: KeyValuePair[] = [
    { key: SPAM, value: i18n.global.t("rulesPage.modals.common.triggers.types.flags.options.spam") },
    { key: SCAM, value: i18n.global.t("rulesPage.modals.common.triggers.types.flags.options.scam") },
    { key: NEWSLETTER, value: i18n.global.t("rulesPage.modals.common.triggers.types.flags.options.newsletter") },
    { key: NOTIFICATION, value: i18n.global.t("rulesPage.modals.common.triggers.types.flags.options.notification") },
    { key: MEETING, value: i18n.global.t("rulesPage.modals.common.triggers.types.flags.options.meeting") },
];

// Form state
const logicalOperator = ref(props.initialFilters?.logicalOperator || "AND");
const domains = ref<string[]>(props.initialFilters?.domains || []);
const senderEmails = ref<string[]>(props.initialFilters?.senderEmails || []);
const hasAttachments = ref(props.initialFilters?.hasAttachments || false);
const selectedPriorities = ref<KeyValuePair[]>(
    (props.initialFilters?.priorities
        ?.map((key) => priorityOptions.find((opt) => opt.key === key))
        .filter(Boolean) as KeyValuePair[]) || []
);
const selectedAnswers = ref<KeyValuePair[]>(
    (props.initialFilters?.answers
        ?.map((key) => answerOptions.find((opt) => opt.key === key))
        .filter(Boolean) as KeyValuePair[]) || []
);
const selectedRelevance = ref<KeyValuePair[]>(
    (props.initialFilters?.relevance
        ?.map((key) => relevanceOptions.find((opt) => opt.key === key))
        .filter(Boolean) as KeyValuePair[]) || []
);
const selectedFlags = ref<KeyValuePair[]>(
    (props.initialFilters?.flags
        ?.map((key) => flagOptions.find((opt) => opt.key === key))
        .filter(Boolean) as KeyValuePair[]) || []
);
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
            priorities: selectedPriorities.value.map((item) => item.key),
            answers: selectedAnswers.value.map((item) => item.key),
            relevance: selectedRelevance.value.map((item) => item.key),
            flags: selectedFlags.value.map((item) => item.key),
            emailDealWith: emailDealWith.value,
        });
    },
    { deep: true }
);

const resetFilters = () => {
    selectedCategoriesNames.value = [];
    selectedPriorities.value = [];
    selectedAnswers.value = [];
    selectedRelevance.value = [];
    selectedFlags.value = [];
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
