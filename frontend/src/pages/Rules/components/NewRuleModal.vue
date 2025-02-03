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
                        <h2 class="text-lg font-semibold text-gray-900">Create New Rule</h2>
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
                                        :options="categoryOptions.map((c) => c.name)"
                                        :multiple="true"
                                        placeholder="Select categories"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Priorities</label>
                                    <multiselect
                                        v-model="formData.priorities"
                                        :options="priorityOptions"
                                        :multiple="true"
                                        placeholder="Select priorities"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Answer Requirements</label>
                                    <multiselect
                                        v-model="formData.answers"
                                        :options="answerOptions"
                                        :multiple="true"
                                        placeholder="Select answer requirements"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Relevance</label>
                                    <multiselect
                                        v-model="formData.relevances"
                                        :options="relevanceOptions"
                                        :multiple="true"
                                        placeholder="Select relevance levels"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Flags</label>
                                    <multiselect
                                        v-model="formData.flags"
                                        :options="flagOptions"
                                        :multiple="true"
                                        placeholder="Select flags"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Email Content Deals With</label>
                                    <textarea
                                        v-model="formData.emailDealWith"
                                        rows="2"
                                        class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                        placeholder="Describe what the email content should deal with..."
                                    />
                                </div>
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

                                <div>
                                    <label class="block text-sm text-gray-700">Transfer to Recipients</label>
                                    <TagInput
                                        v-model="formData.actionTransferRecipients"
                                        placeholder="Add email address"
                                        :validate="validateEmail"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Set Flags</label>
                                    <multiselect
                                        v-model="formData.actionSetFlags"
                                        :options="flagOptions"
                                        :multiple="true"
                                        placeholder="Add flag"
                                        class="multiselect-gray"
                                    />
                                </div>

                                <div>
                                    <label class="block text-sm text-gray-700">Mark As</label>
                                    <multiselect
                                        v-model="formData.actionMarkAs"
                                        :options="markAsOptions"
                                        :multiple="true"
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
                                        <option v-for="priority in priorityOptions" :key="priority" :value="priority">
                                            {{ priority }}
                                        </option>
                                    </select>
                                </div>
                            </div>

                            <!-- AI Actions -->
                            <div class="space-y-4">
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
                                        v-model="formData.actionReplyRecipients"
                                        placeholder="Add email address"
                                        :validate="validateEmail"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Submit Button -->
                    <div class="flex justify-end pt-4">
                        <button
                            type="button"
                            class="px-4 py-2 bg-gray-800 text-white rounded-md hover:bg-black focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                            @click="handleSubmit"
                        >
                            Create Rule
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { inject, onMounted, ref, watch } from "vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import { getData, postData } from "@/global/fetchData";
import { Category, EmailSender } from "@/global/types";
import { RuleData } from "../utils/types";
import Multiselect from "vue-multiselect";
import TagInput from "./TagInput.vue";
import { i18n } from "@/global/preferences";

interface Props {
    isOpen: boolean;
    categories: Category[];
    emailSenders: EmailSender[];
}

const props = withDefaults(defineProps<Props>(), {
    isOpen: false,
    categories: () => [],
});

const emit = defineEmits<{
    (e: "update:isOpen", value: boolean): void;
    (e: "fetch-rules"): void;
}>();

const isOpen = ref(props.isOpen);

// Section visibility state
const sections = ref({
    triggers: false,
    actions: false,
});

// Form state
const formData = ref<RuleData>({
    logicalOperator: "AND",
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
    actionSetCategory: undefined,
    actionSetPriority: "",
    actionSetRelevance: "",
    actionSetAnswer: "",
    actionReplyPrompt: "",
    actionReplyRecipients: [],
});

const errorMessage = ref("");

// Options
const priorityOptions = ["Important", "Informative", "Useless"];
const answerOptions = ["Answer Required", "Might Require Answer", "No Answer Required"];
const relevanceOptions = ["Highly Relevant", "Possibly Relevant", "Not Relevant"];
const flagOptions = ["Spam", "Scam", "Newsletter", "Notification", "Meeting"];
const markAsOptions = ["Read", "Answer Later", "Archive"];
let categoryOptions: Category[] = [];

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

watch(
    () => props.isOpen,
    (newValue) => {
        isOpen.value = newValue;
    }
);

const closeModal = () => {
    isOpen.value = false;
    errorMessage.value = "";
    emit("update:isOpen", false);
};

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Escape") {
        closeModal();
    }
};

const handleSubmit = async () => {
    const result = await postData("user/rules/", formData.value);

    if (!result.success) {
        errorMessage.value = result.error as string;
        return;
    }
    displayPopup?.("success", "Success", "Rule created successfully");

    emit("fetch-rules");
    closeModal();
};

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
    document.addEventListener("keydown", handleKeyDown);
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
