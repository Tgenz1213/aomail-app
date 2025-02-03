<template>
    <div class="h-full overflow-y-auto -mr-6">
        <div class="flex gap-6 h-full pr-4">
            <!-- Professional Templates -->
            <div class="w-2/5 bg-white rounded-lg p-4 overflow-y-auto max-h-full">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-lg font-semibold">{{ $t('aiAssistantPage.professionalTemplates.title') }}</h2>
                    <div class="relative">
                        <input type="text" v-model="searchQuery"
                            :placeholder="$t('aiAssistantPage.professionalTemplates.searchPlaceholder')"
                            class="w-48 px-3 py-1 border rounded-md text-sm" />
                        <MagnifyingGlassIcon class="absolute right-2 top-1.5 w-4 h-4 text-gray-400" />
                    </div>
                </div>
                <p class="text-sm text-gray-600 mb-4">
                    {{ $t('aiAssistantPage.professionalTemplates.subtitle') }}
                </p>
                <div class="space-y-4">
                    <div v-if="filteredProfiles.length === 0"
                        class="border rounded-lg p-3 hover:bg-gray-50 cursor-pointer transition-colors">
                        <h3 class="font-medium text-gray-900">{{
                            $t('aiAssistantPage.professionalTemplates.noResult') }}</h3>
                    </div>
                    <div v-else v-for="profile in filteredProfiles" :key="profile.title"
                        class="border rounded-lg p-3 hover:bg-gray-50 cursor-pointer transition-colors"
                        @click="applyProfile(profile)">
                        <h3 class="font-medium text-gray-900">{{ profile.title }}</h3>
                        <p class="text-sm text-gray-600 mt-1">{{ profile.description }}</p>
                    </div>
                </div>
            </div>

            <!-- Guidelines Form -->
            <div class="flex-1 bg-white rounded-lg p-4">
                <h2 class="text-lg font-semibold mb-4">{{ $t('aiAssistantPage.detailedGuidelines.title') }}</h2>
                <div class="bg-blue-50 border border-blue-200 rounded-md p-4 mb-4">
                    <p class="text-sm text-blue-800">
                        {{ $t('aiAssistantPage.detailedGuidelines.subtitle') }}
                    </p>
                </div>
                <form @submit.prevent="saveGuidelines" class="space-y-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">{{
                            $t('aiAssistantPage.detailedGuidelines.important.label') }}</label>
                        <p class="text-xs text-gray-500 mb-2">
                            {{ $t('aiAssistantPage.detailedGuidelines.important.description') }}
                        </p>
                        <textarea v-model="guidelines.important" rows="4"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm"
                            :placeholder="getPlaceholder('important')"></textarea>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            {{ $t('aiAssistantPage.detailedGuidelines.informative.label') }}
                        </label>
                        <p class="text-xs text-gray-500 mb-2">
                            {{ $t('aiAssistantPage.detailedGuidelines.informative.description') }}
                        </p>
                        <textarea v-model="guidelines.informative" rows="4"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm"
                            :placeholder="getPlaceholder('informative')"></textarea>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            {{ $t('aiAssistantPage.detailedGuidelines.lowPriority.label') }}
                        </label>
                        <p class="text-xs text-gray-500 mb-2">
                            {{ $t('aiAssistantPage.detailedGuidelines.lowPriority.description') }}
                        </p>
                        <textarea v-model="guidelines.useless" rows="4"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm"
                            :placeholder="getPlaceholder('useless')"></textarea>
                    </div>
                    <div class="flex justify-end">
                        <button type="submit"
                            class="inline-flex justify-center rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600">
                            {{ $t('aiAssistantPage.detailedGuidelines.saveButton') }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { MagnifyingGlassIcon } from "@heroicons/vue/24/outline";
import { getPredefinedProfiles } from "../utils/jobs";
import { getData, postData } from "@/global/fetchData";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";

const searchQuery = ref("");
const predefinedProfiles = ref(getPredefinedProfiles());
const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

const currentGuidelines = ref({
    importantGuidelines: "",
    informativeGuidelines: "",
    uselessGuidelines: "",
});

const guidelines = ref({
    important: "",
    informative: "",
    useless: "",
});

const filteredProfiles = computed(() => {
    if (!searchQuery.value) return predefinedProfiles.value;
    const query = searchQuery.value.toLowerCase();
    return predefinedProfiles.value.filter(
        (profile) =>
            profile.title.toLowerCase().includes(query) ||
            profile.description.toLowerCase().includes(query) ||
            profile.keywords.some((keyword) => keyword.toLowerCase().includes(query))
    );
});

function getPlaceholder(type: "important" | "informative" | "useless"): string {
    const defaultPlaceholders = {
        important:
            "Example: Urgent client requests, critical project deadlines, direct messages from your supervisor about immediate tasks...",
        informative: "Example: Team updates, project progress reports, industry news relevant to your work...",
        useless: "Example: Marketing newsletters, social media notifications, promotional offers...",
    };

    return currentGuidelines.value[`${type}Guidelines`] || defaultPlaceholders[type];
}

function displayPopup(type: "success" | "error", title: string, message: string) {
    if (type === "error") {
        displayErrorPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    } else {
        displaySuccessPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    }
    timerId.value = setTimeout(dismissPopup, 4000);
}

function dismissPopup() {
    showNotification.value = false;
    if (timerId.value !== null) {
        clearTimeout(timerId.value);
    }
}

async function loadCurrentGuidelines() {
    const result = await getData("user/preferences/guidelines/");
    if (result.success) {
        currentGuidelines.value = result.data;
        guidelines.value = {
            important: result.data.importantGuidelines,
            informative: result.data.informativeGuidelines,
            useless: result.data.uselessGuidelines,
        };
    } else {
        displayPopup("error", "Failed to load current guidelines", result.error as string);
    }
}

function applyProfile(profile: { important: string; informative: string; useless: string }) {
    guidelines.value = {
        important: profile.important,
        informative: profile.informative,
        useless: profile.useless,
    };
}

async function saveGuidelines() {
    const result = await postData("user/preferences/prioritization/", {
        importantGuidelines: guidelines.value.important || currentGuidelines.value.importantGuidelines,
        informativeGuidelines: guidelines.value.informative || currentGuidelines.value.informativeGuidelines,
        uselessGuidelines: guidelines.value.useless || currentGuidelines.value.uselessGuidelines,
    });

    if (result.success) {
        displayPopup("success", "Success", "Guidelines updated successfully");
        await loadCurrentGuidelines();
    } else {
        displayPopup("error", "Failed to update guidelines", result.error as string);
    }
}

loadCurrentGuidelines();
</script> 