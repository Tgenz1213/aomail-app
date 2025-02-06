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
                            <!-- Trigger List -->
                            <div class="space-y-4">
                                <div v-for="(trigger, index) in triggers" :key="index" class="space-y-4">
                                    <!-- Trigger Type Selection -->
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">
                                            {{ index === 0 ? 'Choose trigger' : `Choose ${index + 1}${getOrdinalSuffix(index + 1)} trigger` }}
                                        </label>
                                        <select
                                            v-model="trigger.type"
                                            class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                        >
                                            <option value="">Select a trigger type</option>
                                            <option
                                                v-for="option in availableTriggerTypes"
                                                :key="option.value"
                                                :value="option.value"
                                                :disabled="isTypeUsed(option.value, index, triggers)"
                                            >
                                                {{ option.label }}
                                            </option>
                                        </select>
                                    </div>

                                    <!-- Trigger Value Input -->
                                    <div v-if="trigger.type" class="pl-4 border-l-2 border-gray-200">
                                        <!-- Email Domains -->
                                        <div v-if="trigger.type === 'domains'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">Email Domains</label>
                                            <TagInput
                                                v-model="trigger.value"
                                                placeholder="Add domain (e.g. gmail.com)"
                                                :validate="validateDomain"
                                            />
                                        </div>

                                        <!-- Sender Emails -->
                                        <div v-if="trigger.type === 'senderEmails'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">Sender Emails</label>
                                            <TagInput
                                                v-model="trigger.value"
                                                placeholder="Add email address"
                                                :validate="validateEmail"
                                            />
                                        </div>

                                        <!-- Has Attachments -->
                                        <div v-if="trigger.type === 'hasAttachments'" class="space-y-2">
                                            <div class="flex items-center">
                                                <input
                                                    v-model="trigger.value"
                                                    type="checkbox"
                                                    class="h-4 w-4 rounded border-gray-300 text-gray-600 focus:ring-gray-500"
                                                />
                                                <label class="ml-2 text-sm text-gray-700">Has attachments</label>
                                            </div>
                                        </div>

                                        <!-- Categories -->
                                        <div v-if="trigger.type === 'categories'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">Categories</label>
                                            <multiselect
                                                v-model="trigger.value"
                                                :options="categoryOptions.map((c: Category) => c.name)"
                                                :multiple="true"
                                                placeholder="Select categories"
                                                class="multiselect-gray"
                                            />
                                        </div>

                                        <!-- Other trigger types... -->
                                        <template v-for="option in ['priorities', 'answers', 'relevances', 'flags']" :key="option">
                                            <div v-if="trigger.type === option" class="space-y-2">
                                                <label class="block text-sm text-gray-700">{{ formatLabel(option) }}</label>
                                                <multiselect
                                                    v-model="trigger.value"
                                                    :options="getOptionsForType(option)"
                                                    :multiple="true"
                                                    track-by="key"
                                                    label="value"
                                                    placeholder="Select options"
                                                    class="multiselect-gray"
                                                />
                                            </div>
                                        </template>
                                    </div>

                                    <!-- Logical Operator Display -->
                                    <div v-if="index < triggers.length - 1" class="flex items-center justify-center py-2">
                                        <span class="px-3 py-1 bg-gray-100 rounded-full text-sm font-medium text-gray-700">
                                            {{ formData.logicalOperator }}
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <!-- Add Trigger Button -->
                            <button
                                @click="addTrigger"
                                class="w-full py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                                :disabled="!canAddMoreTriggers"
                            >
                                Add Another Trigger
                            </button>
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
                            <!-- Action List -->
                            <div class="space-y-4">
                                <div v-for="(action, index) in actions" :key="index" class="space-y-4">
                                    <!-- Action Type Selection -->
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-1">
                                            {{ index === 0 ? 'Choose action' : `Choose ${index + 1}${getOrdinalSuffix(index + 1)} action` }}
                                        </label>
                                        <select
                                            v-model="action.type"
                                            class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                        >
                                            <option value="">Select an action type</option>
                                            <option
                                                v-for="option in availableActionTypes"
                                                :key="option.value"
                                                :value="option.value"
                                                :disabled="isTypeUsed(option.value, index, actions)"
                                            >
                                                {{ option.label }}
                                            </option>
                                        </select>
                                    </div>

                                    <!-- Action Value Input -->
                                    <div v-if="action.type" class="pl-4 border-l-2 border-gray-200">
                                        <!-- Set Flags -->
                                        <div v-if="action.type === 'setFlags'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">Set Flags</label>
                                            <multiselect
                                                v-model="action.value"
                                                :options="flagOptions"
                                                :multiple="true"
                                                track-by="key"
                                                label="value"
                                                placeholder="Add flag"
                                                class="multiselect-gray"
                                            />
                                        </div>

                                        <!-- Mark As -->
                                        <div v-if="action.type === 'markAs'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">Mark As</label>
                                            <multiselect
                                                v-model="action.value"
                                                :options="markAsOptions"
                                                :multiple="true"
                                                track-by="key"
                                                label="value"
                                                placeholder="Select marking options"
                                                class="multiselect-gray"
                                            />
                                        </div>

                                        <!-- Delete Email -->
                                        <div v-if="action.type === 'delete'" class="space-y-2">
                                            <div class="flex items-center">
                                                <input
                                                    v-model="action.value"
                                                    type="checkbox"
                                                    class="h-4 w-4 rounded border-gray-300 text-gray-600 focus:ring-gray-500"
                                                />
                                                <label class="ml-2 text-sm text-gray-700">Delete email</label>
                                            </div>
                                        </div>

                                        <!-- Set Category -->
                                        <div v-if="action.type === 'setCategory'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">Set Category</label>
                                            <select
                                                v-model="action.value"
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

                                        <!-- Set Priority -->
                                        <div v-if="action.type === 'setPriority'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">Set Priority</label>
                                            <select
                                                v-model="action.value"
                                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                            >
                                                <option value="">Select priority</option>
                                                <option
                                                    v-for="priority in priorityOptions"
                                                    :key="priority.key"
                                                    :value="priority.value"
                                                >
                                                    {{ priority.value }}
                                                </option>
                                            </select>
                                        </div>

                                        <!-- Set Relevance -->
                                        <div v-if="action.type === 'setRelevance'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">Set Relevance</label>
                                            <select
                                                v-model="action.value"
                                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                            >
                                                <option value="">Select relevance</option>
                                                <option
                                                    v-for="relevance in relevanceOptions"
                                                    :key="relevance.key"
                                                    :value="relevance.value"
                                                >
                                                    {{ relevance.value }}
                                                </option>
                                            </select>
                                        </div>

                                        <!-- Set Answer -->
                                        <div v-if="action.type === 'setAnswer'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">Set Answer</label>
                                            <select
                                                v-model="action.value"
                                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                            >
                                                <option value="">Select answer</option>
                                                <option
                                                    v-for="answer in answerOptions"
                                                    :key="answer.key"
                                                    :value="answer.value"
                                                >
                                                    {{ answer.value }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Add Action Button -->
                            <button
                                @click="addAction"
                                class="w-full py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                                :disabled="!canAddMoreActions"
                            >
                                Add Another Action
                            </button>
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
import { computed, inject, onMounted, ref, watch } from "vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import { getData, postData } from "@/global/fetchData";
import { Category, EmailSender, KeyValuePair } from "@/global/types";
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

const selectedPriorities = ref<KeyValuePair[]>([]);
const selectedAnswers = ref<KeyValuePair[]>([]);
const selectedRelevances = ref<KeyValuePair[]>([]);
const selectedFlags = ref<KeyValuePair[]>([]);
const selectedActionFlags = ref<KeyValuePair[]>([]);
const selectedActionMarkAs = ref<KeyValuePair[]>([]);

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

const errorMessage = ref("");

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
    () => props.isOpen,
    (newValue) => {
        isOpen.value = newValue;
    }
);

const closeModal = () => {
    errorMessage.value = "";
    emit("update:isOpen", false);
};

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Escape") {
        closeModal();
    }
};

// New interfaces
interface Trigger {
    type: string;
    value: any;
}

// Add to your existing data
const triggers = ref<Trigger[]>([{ type: '', value: null }]);
const actions = ref<Trigger[]>([{ type: '', value: null }]);

const triggerTypes = [
    { value: 'domains', label: 'Email Domains' },
    { value: 'senderEmails', label: 'Sender Emails' },
    { value: 'hasAttachments', label: 'Has Attachments' },
    { value: 'categories', label: 'Categories' },
    { value: 'priorities', label: 'Priorities' },
    { value: 'answers', label: 'Answer Requirements' },
    { value: 'relevances', label: 'Relevance' },
    { value: 'flags', label: 'Flags' },
];

const availableTriggerTypes = computed(() => triggerTypes);

const isTypeUsed = (type: string, currentIndex: number, items: Trigger[]) => {
    return items.some((item, index) => index !== currentIndex && item.type === type);
};

const canAddMoreTriggers = computed(() => {
    return triggers.value.length < triggerTypes.length && 
           triggers.value[triggers.value.length - 1].type !== '';
});

const addTrigger = () => {
    triggers.value.push({ type: '', value: null });
};

const getOptionsForType = (type: string) => {
    switch (type) {
        case 'priorities':
            return priorityOptions;
        case 'answers':
            return answerOptions;
        case 'relevances':
            return relevanceOptions;
        case 'flags':
            return flagOptions;
        default:
            return [];
    }
};

const formatLabel = (str: string) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
};

const getOrdinalSuffix = (num: number) => {
    const j = num % 10;
    const k = num % 100;
    if (j == 1 && k != 11) return "st";
    if (j == 2 && k != 12) return "nd";
    if (j == 3 && k != 13) return "rd";
    return "th";
};

// Add to your existing data
const actionTypes = [
    { value: 'setFlags', label: 'Set Flags' },
    { value: 'markAs', label: 'Mark As' },
    { value: 'delete', label: 'Delete Email' },
    { value: 'setCategory', label: 'Set Category' },
    { value: 'setPriority', label: 'Set Priority' },
    { value: 'setRelevance', label: 'Set Relevance' },
    { value: 'setAnswer', label: 'Set Answer' },
];

const availableActionTypes = computed(() => actionTypes);

const canAddMoreActions = computed(() => {
    return actions.value.length < actionTypes.length && 
           actions.value[actions.value.length - 1].type !== '';
});

const addAction = () => {
    actions.value.push({ type: '', value: null });
};

// Modify handleSubmit to include actions
const handleSubmit = async () => {
    // Transform triggers into formData format
    triggers.value.forEach(trigger => {
        switch (trigger.type) {
            case 'domains':
                formData.value.domains = trigger.value;
                break;
            case 'senderEmails':
                formData.value.senderEmails = trigger.value;
                break;
            // ... handle other cases
        }
    });
    
    // Transform actions into formData format
    actions.value.forEach(action => {
        switch (action.type) {
            case 'setFlags':
                formData.value.actionSetFlags = action.value;
                break;
            case 'markAs':
                formData.value.actionMarkAs = action.value;
                break;
            case 'delete':
                formData.value.actionDelete = action.value;
                break;
            case 'setCategory':
                formData.value.actionSetCategory = action.value;
                break;
            case 'setPriority':
                formData.value.actionSetPriority = action.value;
                break;
            case 'setRelevance':
                formData.value.actionSetRelevance = action.value;
                break;
            case 'setAnswer':
                formData.value.actionSetAnswer = action.value;
                break;
        }
    });
    
    // ... rest of your existing submit logic ...
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

onMounted(async () => {
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
