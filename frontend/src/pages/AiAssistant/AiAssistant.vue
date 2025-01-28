<template>
    <NotificationTimer :showNotification="showNotification" :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" @dismissPopup="dismissPopup" />
    <div class="h-screen flex flex-col">
        <div class="flex h-full">
            <div :class="['ring-1 shadow-sm ring-black ring-opacity-5', isNavMinimized ? 'w-20' : 'w-60']">
                <Navbar @update:isMinimized="(value) => (isNavMinimized = value)" />
            </div>

            <div class="flex flex-1 flex-col">
                <div class="px-6 py-3 bg-gray-50 border-b border-black shadow-sm border-opacity-10">
                    <div class="max-w-3xl mx-auto text-center mb-4">
                        <h1 class="text-xl font-semibold text-gray-900">Email Organization Preferences</h1>
                        <p class="text-sm text-gray-600">
                            Customize how AI understands and organizes your emails based on your professional needs.
                        </p>
                    </div>

                    <div class="flex justify-center gap-4">
                        <a href="/custom-categorization"
                            class="group relative flex items-center gap-2 rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
                            @mouseenter="showTooltip = 'chat'" @mouseleave="showTooltip = ''">
                            <ChatBubbleLeftRightIcon class="w-5 h-5" />
                            <span>Email Categories</span>
                            <div v-if="showTooltip === 'chat'"
                                class="absolute -top-16 w-72 p-2 bg-gray-800 text-white text-sm rounded shadow-lg">
                                Have a conversation with AI to explain how you want your emails organized. Perfect for
                                unique workflows and specific preferences.
                            </div>
                        </a>

                        <a href="/rules"
                            class="group relative flex items-center gap-2 rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
                            @mouseenter="showTooltip = 'rules'" @mouseleave="showTooltip = ''">
                            <AdjustmentsHorizontalIcon class="w-5 h-5" />
                            <span>{{ $t("constants.rulesNavbar") }}</span>
                            <div v-if="showTooltip === 'rules'"
                                class="absolute -top-16 w-72 p-2 bg-gray-800 text-white text-sm rounded shadow-lg">
                                Set up automated rules to handle specific emails, like always marking certain senders as
                                important or moving newsletters to a separate category.
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 overflow-auto p-6">
                    <div class="flex gap-6">
                        <!-- Professional Templates -->
                        <div class="w-2/5 bg-white rounded-lg shadow p-4">
                            <div class="flex justify-between items-center mb-4">
                                <h2 class="text-lg font-semibold">Professional Templates</h2>
                                <div class="relative">
                                    <input type="text" v-model="searchQuery" placeholder="Search job..."
                                        class="w-48 px-3 py-1 border rounded-md text-sm" />
                                    <MagnifyingGlassIcon class="absolute right-2 top-1.5 w-4 h-4 text-gray-400" />
                                </div>
                            </div>
                            <p class="text-sm text-gray-600 mb-4">
                                Choose a template that matches your profession. These templates contain pre-configured
                                guidelines based on common email patterns.
                            </p>
                            <div class="space-y-4 max-h-[600px] overflow-y-auto">
                                <div v-if="filteredProfiles.length === 0"
                                    class="border rounded-lg p-3 hover:bg-gray-50 cursor-pointer transition-colors">
                                    <h3 class="font-medium text-gray-900">No result</h3>
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
                        <div class="flex-1 bg-white rounded-lg shadow p-4">
                            <h2 class="text-lg font-semibold mb-4">Detailed Guidelines</h2>
                            <div class="bg-blue-50 border border-blue-200 rounded-md p-4 mb-4">
                                <p class="text-sm text-blue-800">
                                    These guidelines help AI understand how to categorize your emails. Be specific and
                                    include examples that reflect your actual email patterns.
                                </p>
                            </div>
                            <form @submit.prevent="saveGuidelines" class="space-y-6">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Important Emails</label>
                                    <p class="text-xs text-gray-500 mb-2">
                                        Describe emails that need immediate attention or are crucial for your work
                                    </p>
                                    <textarea v-model="guidelines.important" rows="4"
                                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm"
                                        :placeholder="getPlaceholder('important')"></textarea>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">
                                        Informative Emails
                                    </label>
                                    <p class="text-xs text-gray-500 mb-2">
                                        Describe emails that are useful but don't require immediate action
                                    </p>
                                    <textarea v-model="guidelines.informative" rows="4"
                                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm"
                                        :placeholder="getPlaceholder('informative')"></textarea>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">
                                        Low Priority Emails
                                    </label>
                                    <p class="text-xs text-gray-500 mb-2">
                                        Describe emails that are not relevant to your work or can be safely ignored
                                    </p>
                                    <textarea v-model="guidelines.useless" rows="4"
                                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 sm:text-sm"
                                        :placeholder="getPlaceholder('useless')"></textarea>
                                </div>
                                <div class="flex justify-end">
                                    <button type="submit"
                                        class="inline-flex justify-center rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600">
                                        Save Guidelines
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import Navbar from "@/global/components/Navbar.vue";
import { ChatBubbleLeftRightIcon, AdjustmentsHorizontalIcon, MagnifyingGlassIcon } from "@heroicons/vue/24/outline";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { getData, postData } from "@/global/fetchData";
import { predefinedProfiles } from "./utils/jobs";

const showTooltip = ref("");
const searchQuery = ref("");
const showNotification = ref(false);
const isNavMinimized = ref(localStorage.getItem("navbarMinimized") === "true");
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

predefinedProfiles;

const filteredProfiles = computed(() => {
    if (!searchQuery.value) return predefinedProfiles;
    const query = searchQuery.value.toLowerCase();
    return predefinedProfiles.filter(
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

onMounted(() => {
    loadCurrentGuidelines();
});
</script>
