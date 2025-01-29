<template>
    <div v-if="isOpen" class="absolute left-0 right-0 z-50">
        <div class="px-6">
            <div class="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
                <div class="max-h-[400px] overflow-y-auto p-2">
                    <div class="flex items-center justify-between">
                        <h2 class="text-lg font-semibold mb-4">Advanced Optional Filters - Aomail Search</h2>
                        <button
                            @click="resetFilters"
                            class="bg-gray-100 px-3 py-2 text-gray-600 text-sm rounded-md hover:bg-gray-200"
                        >
                            Clear All Filters
                        </button>
                    </div>

                    <!-- Email Provider Section -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">
                            Choose the Email Providers you want to include in your search
                        </h3>
                        <div class="flex items-center space-x-2">
                            <input
                                type="checkbox"
                                id="gmail"
                                :value="GOOGLE"
                                v-model="emailProviders"
                                class="rounded text-gray-600 focus:ring-gray-500"
                            />
                            <label for="gmail" class="flex items-center">Gmail</label>
                        </div>
                        <div class="flex items-center space-x-2">
                            <input
                                type="checkbox"
                                id="outlook"
                                :value="MICROSOFT"
                                v-model="emailProviders"
                                class="rounded text-gray-600 focus:ring-gray-500"
                            />
                            <label for="outlook" class="flex items-center">Outlook</label>
                        </div>
                    </div>

                    <!-- Subject -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">Subject</h3>
                        <input
                            type="text"
                            v-model="aomailSearchFilters.subject"
                            placeholder="Subject contains..."
                            class="w-full rounded-md border border-gray-300 p-2"
                        />
                    </div>

                    <!-- Sender Email -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">Sender Email</h3>
                        <input
                            type="text"
                            v-model="aomailSearchFilters.senderEmail"
                            placeholder="Sender email address contains..."
                            class="w-full rounded-md border border-gray-300 p-2"
                        />
                    </div>

                    <!-- Sender Name -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">Sender Name</h3>
                        <input
                            type="text"
                            v-model="aomailSearchFilters.senderName"
                            placeholder="Sender name contains..."
                            class="w-full rounded-md border border-gray-300 p-2"
                        />
                    </div>

                    <!-- Category -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">Category</h3>

                        <select v-model="aomailSearchFilters.category">
                            <option disabled value="">Select the category to search in</option>
                            <option
                                v-for="category in categories"
                                :key="category.name"
                                class="flex items-center justify-between overflow-hidden font-semibold rounded-md bg-gray-50 px-6 py-4 shadow hover:shadow-md text-gray-700 relative"
                            >
                                {{ category.name }}
                            </option>
                        </select>
                    </div>

                    <!-- Received Date -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">
                            Search from Received Date (choose a date to filter emails from that day until now)
                        </h3>
                        <input
                            type="date"
                            v-model="aomailSearchFilters.sentDate"
                            class="w-full rounded-md border border-gray-300 p-2"
                        />
                    </div>

                    <!-- Read Date -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">
                            Search from Read Date (choose a date to filter emails from that day until now)
                        </h3>
                        <input
                            type="date"
                            v-model="aomailSearchFilters.readDate"
                            class="w-full rounded-md border border-gray-300 p-2"
                        />
                    </div>

                    <!-- Read Status -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">Status</h3>
                        <div class="flex items-center space-x-2">
                            <input
                                type="checkbox"
                                id="read"
                                v-model="aomailSearchFilters.read"
                                class="rounded text-gray-600 focus:ring-gray-500"
                            />
                            <label for="read" class="flex items-center">Read</label>
                        </div>
                        <div class="flex items-center space-x-2">
                            <input
                                type="checkbox"
                                id="archive"
                                v-model="aomailSearchFilters.archive"
                                class="rounded text-gray-600 focus:ring-gray-500"
                            />
                            <label for="archive" class="flex items-center">Archive</label>
                        </div>
                        <div class="flex items-center space-x-2">
                            <input
                                type="checkbox"
                                id="replyLater"
                                v-model="aomailSearchFilters.replyLater"
                                class="rounded text-gray-600 focus:ring-gray-500"
                            />
                            <label for="replyLater" class="flex items-center">Reply Later</label>
                        </div>
                    </div>

                    <!-- Priority Section -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">
                            {{ $t("homePage.modals.filterModal.priority") }}
                        </h3>
                        <div class="flex justify-between items-center">
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="important"
                                    v-model="priorities"
                                    :value="IMPORTANT"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="important" class="flex items-center">
                                    <span
                                        class="bg-orange-100 text-orange-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full"
                                    >
                                        <ExclamationCircleIcon class="h-4 w-4 items-center inline mr-1" />
                                        Important
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="informative"
                                    v-model="priorities"
                                    :value="INFORMATIVE"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="informative" class="flex items-center">
                                    <span
                                        class="bg-blue-100 text-blue-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full"
                                    >
                                        <InformationCircleIcon class="h-4 w-4 inline mr-1" />
                                        Informative
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="useless"
                                    v-model="priorities"
                                    :value="USELESS"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="useless" class="flex items-center">
                                    <span
                                        class="bg-gray-100 text-gray-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full"
                                    >
                                        <TrashIcon class="h-4 w-4 inline mr-1" />
                                        Useless
                                    </span>
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Additional Flags Section -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">Flags</h3>
                        <div class="grid grid-cols-2 gap-2">
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="notification"
                                    v-model="aomailSearchFilters.notification"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="notification" class="flex items-center">
                                    <span
                                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10"
                                    >
                                        Notification
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="newsletter"
                                    v-model="aomailSearchFilters.newsletter"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="newsletter" class="flex items-center">
                                    <span
                                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10"
                                    >
                                        Newsletter
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="meeting"
                                    v-model="aomailSearchFilters.meeting"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="meeting" class="flex items-center">
                                    <span
                                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10"
                                    >
                                        Meeting
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="spam"
                                    v-model="aomailSearchFilters.spam"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="spam" class="flex items-center">
                                    <span
                                        class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10"
                                    >
                                        Spam
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="scam"
                                    v-model="aomailSearchFilters.scam"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="scam" class="flex items-center">
                                    <span
                                        class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10"
                                    >
                                        Scams
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="hasAttachments"
                                    v-model="aomailSearchFilters.hasAttachments"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="scam" class="flex items-center">
                                    <span
                                        class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10"
                                    >
                                        Has Attachments
                                    </span>
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Answer -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">Answer</h3>
                        <div class="grid grid-cols-2 gap-2">
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="answerRequired"
                                    v-model="answers"
                                    :value="ANSWER_REQUIRED"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="answerRequired" class="flex items-center">
                                    <span
                                        class="bg-green-100 text-green-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full"
                                    >
                                        Answer Required
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="mightRequireAnswer"
                                    v-model="answers"
                                    :value="MIGHT_REQUIRE_ANSWER"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="mightRequireAnswer" class="flex items-center">
                                    <span
                                        class="bg-yellow-100 text-yellow-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full"
                                    >
                                        Might Require Answer
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="noAnswerRequired"
                                    v-model="answers"
                                    :value="NO_ANSWER_REQUIRED"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="noAnswerRequired" class="flex items-center">
                                    <span
                                        class="bg-red-100 text-red-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full"
                                    >
                                        No Answer Required
                                    </span>
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Relevance -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">Relevance</h3>
                        <div class="grid grid-cols-2 gap-2">
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="highlyRelevant"
                                    v-model="relevances"
                                    :value="HIGHLY_RELEVANT"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="highlyRelevant" class="flex items-center">
                                    <span
                                        class="bg-green-100 text-green-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full"
                                    >
                                        Highly Relevant
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="possiblyRelevant"
                                    v-model="relevances"
                                    :value="POSSIBLY_RELEVANT"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="possiblyRelevant" class="flex items-center">
                                    <span
                                        class="bg-yellow-100 text-yellow-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full"
                                    >
                                        Possibly Relevant
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="notRelevant"
                                    v-model="relevances"
                                    :value="NOT_RELEVANT"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="notRelevant" class="flex items-center">
                                    <span
                                        class="bg-red-100 text-red-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full"
                                    >
                                        Not Relevant
                                    </span>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import {
    ANSWER_REQUIRED,
    GOOGLE,
    HIGHLY_RELEVANT,
    IMPORTANT,
    INFORMATIVE,
    MICROSOFT,
    MIGHT_REQUIRE_ANSWER,
    NO_ANSWER_REQUIRED,
    NOT_RELEVANT,
    POSSIBLY_RELEVANT,
    USELESS,
} from "@/global/const";
import { getData } from "@/global/fetchData";
import { AomailSearchFilter, Category } from "@/global/types";
import { ExclamationCircleIcon, InformationCircleIcon, TrashIcon } from "@heroicons/vue/20/solid";
import { ref, inject, Ref, onMounted, watch } from "vue";

const emailProviders = ref<string[]>([]);
const priorities = ref<(typeof IMPORTANT | typeof INFORMATIVE | typeof USELESS)[]>([]);
const relevances = ref<(typeof HIGHLY_RELEVANT | typeof POSSIBLY_RELEVANT | typeof NOT_RELEVANT)[]>([]);
const answers = ref<(typeof ANSWER_REQUIRED | typeof MIGHT_REQUIRE_ANSWER | typeof NO_ANSWER_REQUIRED)[]>([]);
const categories = ref<Category[]>([]);

watch(emailProviders, (emailProviders) => {
    aomailSearchFilters.value.emailProvider = emailProviders;
});

watch(priorities, (priorities) => {
    aomailSearchFilters.value.priority = priorities;
});

watch(relevances, (relevances) => {
    aomailSearchFilters.value.relevance = relevances;
});

watch(answers, (answers) => {
    aomailSearchFilters.value.answer = answers;
});

onMounted(async () => {
    const result = await getData("user/categories/");
    if (result.success) {
        categories.value = result.data;
    }
});

const aomailSearchFilters = inject<Ref<AomailSearchFilter>>("aomailSearchFilters") || ref<AomailSearchFilter>({});

defineProps({
    isOpen: Boolean,
});

const resetFilters = () => {
    aomailSearchFilters.value = {
        advanced: undefined,
        emailProvider: undefined,
        subject: undefined,
        senderEmail: undefined,
        senderName: undefined,
        CCEmails: undefined,
        CCNames: undefined,
        category: undefined,
        emailAddresses: undefined,
        archive: undefined,
        replyLater: undefined,
        read: undefined,
        sentDate: undefined,
        readDate: undefined,
        answer: undefined,
        relevance: undefined,
        priority: undefined,
        hasAttachments: undefined,
        spam: undefined,
        scam: undefined,
        newsletter: undefined,
        notification: undefined,
        meeting: undefined,
    };

    emailProviders.value = [];
    priorities.value = [];
    relevances.value = [];
    answers.value = [];
};
</script>
