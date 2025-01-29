<template>
    <div v-if="isOpen" class="absolute left-0 right-0 z-50">
        <div class="px-6">
            <div class="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
                <div class="max-h-[400px] overflow-y-auto p-2">
                    <div class="flex items-center justify-between">
                        <h2 class="text-lg font-semibold mb-4">Advanced Optional Filters - API Search</h2>
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
                            v-model="apiSearchFilters.subject"
                            placeholder="Subject contains..."
                            class="w-full rounded-md border border-gray-300 p-2"
                        />
                    </div>

                    <!-- Sender Email -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">Sender Email</h3>
                        <input
                            type="text"
                            v-model="fromAddress"
                            placeholder="Sender Email Address contains..."
                            class="w-full rounded-md border border-gray-300 p-2"
                        />
                    </div>

                    <!-- To Address -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">Recipient Email</h3>
                        <input
                            type="text"
                            v-model="toAddress"
                            placeholder="Recipient Email Address contains..."
                            class="w-full rounded-md border border-gray-300 p-2"
                        />
                    </div>

                    <!-- Body -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">Email body</h3>
                        <input
                            type="text"
                            v-model="apiSearchFilters.body"
                            placeholder="Email body contains..."
                            class="w-full rounded-md border border-gray-300 p-2"
                        />
                    </div>

                    <!-- Received Date -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">
                            Search from Received Date (choose a date to filter emails from that day until now)
                        </h3>
                        <input
                            type="date"
                            v-model="apiSearchFilters.dateFrom"
                            class="w-full rounded-md border border-gray-300 p-2"
                        />
                    </div>

                    <div class="space-y-4">
                        <!-- Attachment Types Multi-select -->
                        <div class="relative">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Attachment Types</label>
                            <div
                                @click="toggleAttachmentDropdown"
                                class="border rounded-md p-2 flex justify-between items-center cursor-pointer bg-white"
                            >
                                <div class="flex flex-wrap gap-1">
                                    <template v-if="selectedAttachments.length">
                                        <span
                                            v-for="key in selectedAttachments"
                                            :key="key"
                                            class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded-full"
                                        >
                                            {{ attachmentTypes.find((type) => type.key === key)?.value }}
                                        </span>
                                    </template>
                                    <span v-else class="text-gray-500">Select attachment types...</span>
                                </div>
                                <svg
                                    class="w-4 h-4 text-gray-400"
                                    :class="{ 'transform rotate-180': isAttachmentOpen }"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path d="M19 9l-7 7-7-7" stroke-width="2" stroke-linecap="round" />
                                </svg>
                            </div>

                            <!-- Attachment Dropdown Content -->
                            <div
                                v-show="isAttachmentOpen"
                                class="absolute z-10 w-full mt-1 bg-white border rounded-md shadow-lg max-h-60 overflow-y-auto"
                            >
                                <div class="p-2 space-y-1">
                                    <label
                                        v-for="type in attachmentTypes"
                                        :key="type.key"
                                        class="flex items-center p-2 hover:bg-gray-50 rounded cursor-pointer"
                                    >
                                        <input
                                            type="checkbox"
                                            :value="type.key"
                                            v-model="selectedAttachments"
                                            class="rounded border-gray-300 text-gray-600 focus:ring-gray-500"
                                        />
                                        <span class="ml-2">{{ type.value }}</span>
                                    </label>
                                </div>
                            </div>
                        </div>

                        <!-- Search In Folders Multi-select -->
                        <div class="relative">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Search In</label>
                            <div
                                @click="toggleSearchDropdown"
                                class="border rounded-md p-2 flex justify-between items-center cursor-pointer bg-white"
                            >
                                <div class="flex flex-wrap gap-1">
                                    <template v-if="selectedSearchIn.length">
                                        <span
                                            v-for="key in selectedSearchIn"
                                            :key="key"
                                            class="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded-full"
                                        >
                                            {{ searchIn.find((option) => option.key === key)?.value }}
                                        </span>
                                    </template>
                                    <span v-else class="text-gray-500">Select search options...</span>
                                </div>
                                <svg
                                    class="w-4 h-4 text-gray-400"
                                    :class="{ 'transform rotate-180': isSearchOpen }"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path d="M19 9l-7 7-7-7" stroke-width="2" stroke-linecap="round" />
                                </svg>
                            </div>

                            <!-- Search Dropdown Content -->
                            <div
                                v-show="isSearchOpen"
                                class="absolute z-10 w-full mt-1 bg-white border rounded-md shadow-lg"
                            >
                                <div class="p-2 space-y-1">
                                    <label
                                        v-for="option in searchIn"
                                        :key="option.key"
                                        class="flex items-center p-2 hover:bg-gray-50 rounded cursor-pointer"
                                    >
                                        <input
                                            type="checkbox"
                                            :value="option.key"
                                            v-model="selectedSearchIn"
                                            class="rounded border-gray-300 text-gray-600 focus:ring-gray-500"
                                        />
                                        <span class="ml-2">{{ option.value }}</span>
                                    </label>
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
import { ref, inject, Ref, watch, onMounted, onUnmounted } from "vue";
import { ApiSearchFilter, KeyValuePair } from "@/global/types";
import { GOOGLE, MICROSOFT } from "@/global/const";

const apiSearchFilters = inject<Ref<ApiSearchFilter>>("apiSearchFilters") || ref<ApiSearchFilter>({});
const emailProviders = ref<string[]>([]);
const fromAddress = ref("");
const toAddress = ref("");
const attachmentTypes: KeyValuePair[] = [
    { key: ".docx", value: "Word Document" },
    { key: ".xlsx", value: "Excel Spreadsheet" },
    { key: ".pptx", value: "PowerPoint Presentation" },
    { key: ".pdf", value: "PDF Document" },
    { key: ".jpg", value: "JPEG Image" },
    { key: ".png", value: "PNG Image" },
    { key: ".gif", value: "GIF Image" },
    { key: ".txt", value: "Text Document" },
    { key: ".zip", value: "ZIP Archive" },
    { key: ".mp3", value: "MP3 Audio" },
    { key: ".mp4", value: "MP4 Video" },
    { key: ".html", value: "HTML Document" },
];
const searchIn: KeyValuePair[] = [
    { key: "spams", value: "Spams" },
    { key: "deleted_emails", value: "Deleted emails" },
    { key: "drafts", value: "Drafts" },
    { key: "sent_emails", value: "Sent emails" },
];

const selectedAttachments = ref<string[]>([]);
const selectedSearchIn = ref<string[]>([]);
const isAttachmentOpen = ref(false);
const isSearchOpen = ref(false);

const toggleAttachmentDropdown = () => {
    isAttachmentOpen.value = !isAttachmentOpen.value;
    if (isAttachmentOpen.value) isSearchOpen.value = false;
};

const toggleSearchDropdown = () => {
    isSearchOpen.value = !isSearchOpen.value;
    if (isSearchOpen.value) isAttachmentOpen.value = false;
};

const handleClickOutside = (event: MouseEvent) => {
    const target = event.target as HTMLElement;
    if (!target.closest(".relative")) {
        isAttachmentOpen.value = false;
        isSearchOpen.value = false;
    }
};

onMounted(() => {
    document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
    document.removeEventListener("click", handleClickOutside);
});

watch(fromAddress, (fromAddress) => {
    apiSearchFilters.value.fromAddresses = [fromAddress];
});

watch(toAddress, (toAddress) => {
    apiSearchFilters.value.toAddresses = [toAddress];
});

watch(emailProviders, (emailProviders) => {
    apiSearchFilters.value.emailProvider = emailProviders;
});

watch(selectedAttachments, (selectedAttachments) => {
    apiSearchFilters.value.fileExtensions = selectedAttachments;
});

watch(selectedSearchIn, (selectedSearchIn) => {
    if (selectedSearchIn.length > 0) {
        apiSearchFilters.value.searchIn = {};

        selectedSearchIn.map((item) => {
            if (!apiSearchFilters.value.searchIn) {
                apiSearchFilters.value.searchIn = {};
            }
            apiSearchFilters.value.searchIn[item] = true;
        });
    }
});

defineProps({
    isOpen: Boolean,
});

const resetFilters = () => {
    apiSearchFilters.value = {
        advanced: undefined,
        emailProvider: undefined,
        fileExtensions: undefined,
        filenames: undefined,
        searchIn: undefined,
        fromAddresses: undefined,
        toAddresses: undefined,
        subject: undefined,
        body: undefined,
        dateFrom: undefined,
    };

    emailProviders.value = [];
    fromAddress.value = "";
    toAddress.value = "";
    selectedSearchIn.value = [];
    selectedAttachments.value = [];
};
</script>
