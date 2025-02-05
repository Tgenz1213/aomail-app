<template>
    <transition name="modal-fade">
        <div
            @click.self="closeModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            v-if="isOpen"
        >
            <div class="bg-white rounded-lg relative w-[600px] max-h-[90vh] overflow-y-auto">
                <!-- Header -->
                <div class="sticky top-0 z-10 bg-white rounded-t-lg border-b border-gray-200">
                    <div class="flex items-center justify-between p-4">
                        <h2 class="text-lg font-semibold text-gray-900">
                            {{ $t("rulesPage.modals.updateRule.modifyTheRule") }}
                        </h2>
                        <button @click="closeModal" class="text-gray-400 hover:text-gray-500">
                            <XMarkIcon class="h-6 w-6" />
                        </button>
                    </div>
                </div>

                <!-- Content -->
                <div class="p-4 space-y-6">
                    <div v-if="errorMessage" class="text-red-600 text-sm mb-4">
                        {{ errorMessage }}
                    </div>

                    <!-- Logical Operator -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Logical Operator</label>
                        <select
                            v-model="formData.logicalOperator"
                            class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                        >
                            <option value="AND">AND - All conditions must match</option>
                            <option value="OR">OR - Any condition can match</option>
                        </select>
                    </div>

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
                                            v-model="formData.domains"
                                            placeholder="Add domain (e.g. gmail.com, esaip.org)"
                                            :validate="validateDomain"
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Sender Emails</label>
                                    <TagInput
                                        v-model="formData.senderEmails"
                                        placeholder="Add email address"
                                        :validate="validateEmail"
                                    />
                                </div>

                                <div class="flex items-center">
                                    <input
                                        id="hasAttachments"
                                        v-model="formData.hasAttachements"
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
                                        v-model="formData.categories"
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
                                        label="value"
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
                                        label="value"
                                        placeholder="Select answer requirements"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Relevance</label>
                                    <multiselect
                                        v-model="selectedRelevances"
                                        :options="relevanceOptions"
                                        :multiple="true"
                                        label="value"
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
                                        label="value"
                                        placeholder="Select flags"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <!-- <div>
                                    <label class="block text-sm text-gray-700">Email Content Deals With</label>
                                    <textarea
                                        v-model="formData.emailDealWith"
                                        rows="2"
                                        class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                        placeholder="Describe what the email content should deal with..."
                                    />
                                </div> -->
                            </div>
                        </div>
                    </div>

                    <!-- Actions Section -->
                    <div class="border rounded-md">
                        <button
                            @click="sections.actions = !sections.actions"
                            class="w-full flex justify-between items-center p-3 text-left"
                        >
                            <span class="text-sm font-medium text-gray-900">Actions</span>
                            <ChevronDownIcon
                                class="h-5 w-5 text-gray-500"
                                :class="{ 'transform rotate-180': sections.actions }"
                            />
                        </button>

                        <div v-if="sections.actions" class="p-4 border-t space-y-4">
                            <!-- Static Actions -->
                            <div class="space-y-4">
                                <h4 class="text-sm font-medium text-gray-700">Email Actions</h4>

                                <!-- <div>
                                    <label class="block text-sm text-gray-700">Transfer to Recipients</label>
                                    <TagInput
                                        v-model="formData.actionTransferRecipients "
                                        placeholder="Add email address"
                                        :validate="validateEmail"
                                    />
                                </div> -->

                                <div>
                                    <label class="block text-sm text-gray-700">Set Flags</label>
                                    <multiselect
                                        v-model="selectedActionFlags"
                                        :options="flagOptions"
                                        :multiple="true"
                                        label="value"
                                        placeholder="Add flag"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Mark As</label>
                                    <multiselect
                                        v-model="selectedActionMarkAs"
                                        :options="markAsOptions"
                                        :multiple="true"
                                        label="value"
                                        placeholder="Select marking options"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div class="flex items-center">
                                    <input
                                        id="actionDelete"
                                        v-model="formData.actionDelete"
                                        type="checkbox"
                                        class="h-4 w-4 rounded border-gray-300 text-gray-600 focus:ring-gray-500"
                                    />
                                    <label for="actionDelete" class="ml-2 text-sm text-gray-700">Delete email</label>
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Set Category</label>
                                    <select
                                        v-model="formData.actionSetCategory"
                                        class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                    >
                                        <option value="">Select category</option>
                                        <option
                                            v-for="category in props.categories"
                                            :key="category.name"
                                            :value="category.name"
                                        >
                                            {{ category.name }}
                                        </option>
                                    </select>
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Set Priority</label>
                                    <select
                                        v-model="formData.actionSetPriority"
                                        class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                    >
                                        <option value="">Select priority</option>
                                        <option
                                            v-for="priority in priorityOptions"
                                            :key="priority.key"
                                            :value="priority.key"
                                        >
                                            {{ priority.value }}
                                        </option>
                                    </select>
                                </div>
                            </div>

                            <!-- AI Actions -->
                            <!-- <div class="space-y-4">
                                <h4 class="text-sm font-medium text-gray-700">AI Actions</h4>

                                <div>
                                    <label class="block text-sm text-gray-700">Auto-Reply Prompt</label>
                                    <textarea
                                        v-model="formData.actionReplyPrompt"
                                        rows="2"
                                        class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                        placeholder="Describe how to reply to the email..."
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Reply Recipients</label>
                                    <TagInput
                                        v-model="formData.actionReplyRecipients "
                                        placeholder="Add email address"
                                        :validate="validateEmail"
                                    />
                                </div>
                            </div> -->
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
                        <button
                            type="button"
                            class="ml-auto rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                            @click="updateUserRule"
                        >
                            {{ $t("constants.userActions.modify") }}
                        </button>
                        <button
                            type="button"
                            class="inline-flex w-full justify-center items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto"
                            @click="deleteRule"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke-width="1.5"
                                stroke="currentColor"
                                class="w-6 h-6"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                                />
                            </svg>
                            {{ $t("constants.userActions.delete") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, inject } from "vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import { putData, deleteData } from "@/global/fetchData";
import { Category, EmailSender, KeyValuePair } from "@/global/types";
import { RuleData } from "../utils/types";
import Multiselect from "vue-multiselect";
import TagInput from "./TagInput.vue";
import { i18n } from "@/global/preferences";

interface Props {
    isOpen: boolean;
    rule: RuleData | null;
    categories: Category[];
    emailSenders: EmailSender[];
}

const props = withDefaults(defineProps<Props>(), {
    isOpen: false,
    categories: () => [],
    rule: null,
    emailSenders: () => [],
});

const emit = defineEmits<{
    (e: "update:isOpen", value: boolean): void;
    (e: "fetch-rules"): void;
}>();

// Section visibility state
const sections = ref({
    triggers: false,
    actions: false,
});

const errorMessage = ref("");
const totalRules = inject("totalRules", ref(0));

const selectedPriorities = ref<KeyValuePair[]>([]);
const selectedAnswers = ref<KeyValuePair[]>([]);
const selectedRelevances = ref<KeyValuePair[]>([]);
const selectedFlags = ref<KeyValuePair[]>([]);
const selectedActionFlags = ref<KeyValuePair[]>([]);
const selectedActionMarkAs = ref<KeyValuePair[]>([]);

// Form state
const formData = ref<RuleData>({
    logicalOperator: "OR",
    domains: [],
    senderEmails: [],
    hasAttachements: false,
    categories: [],
    priorities: [],
    answers: [],
    relevances: [],
    flags: [],
    emailDealWith: "",
    actionTransferRecipients: [],
    actionSetFlags: [],
    actionMarkAs: [],
    actionDelete: false,
    actionSetCategory: "",
    actionSetPriority: "",
    actionSetRelevance: "",
    actionSetAnswer: "",
    actionReplyPrompt: "",
    actionReplyRecipients: [],
});

// Options
const priorityOptions: KeyValuePair[] = [
    { key: "important", value: "Important" },
    { key: "informative", value: "Informative" },
    { key: "useless", value: "Useless" },
];
const answerOptions: KeyValuePair[] = [
    { key: "Answer Required", value: "Answer Required" },
    { key: "Might Require Answer", value: "Might Require Answer" },
    { key: "No Answer Required", value: "No Answer Required" },
];
const relevanceOptions: KeyValuePair[] = [
    { key: "Highly Relevant", value: "Highly Relevant" },
    { key: "Possibly Relevant", value: "Possibly Relevant" },
    { key: "Not Relevant", value: "Not Relevant" },
];
const flagOptions: KeyValuePair[] = [
    { key: "spam", value: "spam" },
    { key: "scam", value: "scam" },
    { key: "newsletter", value: "newsletter" },
    { key: "notification", value: "notification" },
    { key: "meeting", value: "meeting" },
];
const markAsOptions: KeyValuePair[] = [
    { key: "read", value: "read" },
    { key: "answerLater", value: "answer later" },
    { key: "archive", value: "archive" },
];
const categoryOptions = computed(() => props.categories);

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

watch(
    () => props.rule,
    (newVal) => {
        if (newVal) {
            formData.value = { ...newVal };
        }
    },
    { immediate: true }
);

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

async function deleteRule() {
    if (!formData.value.id) {
        errorMessage.value = i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleDeletionError");
        return;
    }

    const result = await deleteData(`user/rules/`, { ids: [formData.value.id] });

    if (!result.success) {
        errorMessage.value = result.error as string;
        return;
    }

    totalRules.value -= 1;
    displayPopup?.(
        "success",
        i18n.global.t("constants.popUpConstants.successMessages.success"),
        i18n.global.t("rulesPage.popUpConstants.successMessages.ruleDeletedSuccessfully")
    );
    closeModal();
    emit("fetch-rules");
}

async function updateUserRule() {
    if (!formData.value.id) {
        errorMessage.value = i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError");
        return;
    }

    // transform KeyValuePair[] to string[]
    formData.value.priorities = selectedPriorities.value.map((priority) => priority.key);
    formData.value.answers = selectedAnswers.value.map((answer) => answer.key);
    formData.value.relevances = selectedRelevances.value.map((relevance) => relevance.key);
    formData.value.flags = selectedFlags.value.map((flag) => flag.key);
    formData.value.actionMarkAs = selectedActionMarkAs.value.map((markAs) => markAs.key);
    formData.value.actionSetFlags = selectedActionFlags.value.map((flag) => flag.key);

    const result = await putData(`user/rules/`, { ids: [formData.value.id], ...formData.value });

    if (!result.success) {
        errorMessage.value = result.error as string;
        return;
    }

    displayPopup?.(
        "success",
        i18n.global.t("constants.popUpConstants.successMessages.success"),
        i18n.global.t("rulesPage.popUpConstants.successMessages.ruleUpdatedSuccessfully")
    );
    closeModal();
    emit("fetch-rules");
}

function closeModal() {
    errorMessage.value = "";
    emit("update:isOpen", false);
}

onMounted(() => {
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeModal();
        }
    });
});
</script>

<style>
.multiselect-gray {
    --ms-tag-bg: #f3f4f6;
    --ms-tag-color: #374151;
    --ms-ring-color: rgb(107 114 128 / 0.5);
    --ms-option-bg-selected: #f3f4f6;
}
</style>
