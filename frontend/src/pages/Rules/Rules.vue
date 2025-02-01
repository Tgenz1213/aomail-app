<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
    />
    <div class="flex flex-col justify-center items-center h-screen">
        <div class="flex h-full w-full">
            <div :class="['ring-1 shadow-sm ring-black ring-opacity-5', isNavMinimized ? 'w-20' : 'w-60']">
                <Navbar @update:isMinimized="(value) => isNavMinimized = value" />
            </div>
            <div class="flex-1 bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <div class="flex flex-col h-full relative">
                    <main class="bg-gray-50 ring-1 ring-black ring-opacity-5 z-50">
                        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                            <div class="flex items-center">
                                <div class="w-full flex items-center justify-center py-6 2xl:py-7">
                                    <div class="sm:hidden"></div>
                                    <div class="hidden sm:block w-full">
                                        <nav class="flex justify-center space-x-4 w-full" aria-label="Tabs">
                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-12'
                                                ]"
                                                @click="() => router.push('/ai-assistant')"
                                            >
                                                <SparklesIcon class="w-4 h-4" />
                                                <a class="text-sm font-medium text-gray-600">
                                                    {{ $t("aiAssistantPage.navtitle") }}
                                                </a>
                                            </div>
                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8'
                                                ]"
                                                @click="() => router.push('/custom-categorization')"
                                            >
                                                <ChatBubbleLeftRightIcon class="w-4 h-4" />
                                                <a class="text-sm font-medium text-gray-600">
                                                    {{ $t("aiAssistantPage.emailCategories.button") }}
                                                </a>
                                            </div>
                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-8'
                                                ]"
                                                @click="() => router.push('/rules')"
                                            >
                                                <AdjustmentsHorizontalIcon class="w-4 h-4" />
                                                <a class="text-sm font-medium text-gray-800">
                                                    {{ $t("aiAssistantPage.rules.button") }}
                                                </a>
                                            </div>
                                        </nav>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </main>
                    <SearchBar @fetchRules="fetchRules" />
                    <div
                        v-if="rules.length > 0"
                        class="flex-grow overflow-y-auto custom-scrollbar"
                        style="margin-right: 2px; margin-bottom: 120px"
                    >
                        <div class="p-6">
                            <ul
                                v-if="rules.length > 0"
                                category="list"
                                class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
                            >
                                <li
                                    v-for="rule in rules"
                                    :key="rule.email"
                                    class="col-span-1 rounded-lg bg-white border-2 border-gray-100 hover:border-3 hover:border-gray-800 hover:shadow-sm relative"
                                >
                                    <Rule :rule="rule" @edit="handleEditRule" />
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div v-if="rules.length === 0" class="flex p-4 w-full h-full">
                        <div
                            class="cursor-pointer flex items-center justify-center w-full h-full rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 text-center"
                            @click="showModal = true"
                        >
                            <div class="flex-col">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1"
                                    stroke="currentColor"
                                    class="w-12 h-12 mx-auto text-gray-400"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
                                    />
                                </svg>
                                <span class="mt-2 block text-sm font-semibold text-gray-900">
                                    {{ $t("constants.userActions.createARule") }}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div
                        v-if="rules.length > 0"
                        class="cursor-pointer flex items-center justify-center w-auto right-6 left-6 absolute bottom-5 h-[85px] rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 text-center"
                        @click="showModal = true"
                    >
                        <div class="flex-col">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke-width="1"
                                stroke="currentColor"
                                class="w-10 h-10 mx-auto text-gray-400"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
                                />
                            </svg>
                            <span class="mt-2 block text-sm font-semibold text-gray-900">
                                {{ $t("rulesPage.createRule") }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <NewRuleModal
        :isOpen="showModal"
        @update:isOpen="updateModalStatus"
        :emailSenders="emailSenders"
        :categories="categories"
        :sender="senderSelected"
        @fetch-rules="fetchRules"
    />
    <UpdateRuleModal
        :isOpen="showUpdateModal"
        :rule="ruleSelected"
        :categories="categories"
        :emailSenders="emailSenders"
        @update:isOpen="updateModalUpdateStatus"
        @fetch-rules="fetchRules"
    />
</template>

<script lang="ts" setup>
import { getData, postData } from "@/global/fetchData";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { ref, onMounted, provide, watch, onUnmounted } from "vue";
import Navbar from "@/global/components/Navbar.vue";
import NewRuleModal from "./components/NewRuleModal.vue";
import UpdateRuleModal from "./components/UpdateRuleModal.vue";
import Rule from "./components/Rule.vue";
import SearchBar from "./components/SearchBar.vue";
import { EmailSender } from "@/global/types";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { FilterPayload, RuleData } from "./utils/types";
import { i18n } from "@/global/preferences";
import { ChatBubbleLeftRightIcon, AdjustmentsHorizontalIcon, SparklesIcon } from "@heroicons/vue/24/outline";
import { useRouter } from 'vue-router';

const router = useRouter();

const showModal = ref(false);
const showUpdateModal = ref(false);
const rules = ref<RuleData[]>([]);
const ruleIds = ref<number[]>([]);
const categories = ref<any[]>([]);
const emailSenders = ref<any[]>([]);
const senderSelected = ref<EmailSender | null>(null);
const ruleSelected = ref<any>(null);
const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);
const isLoading = ref(false);
const currentPage = ref(1);
const rulesPerPage = 100;
const totalRules = ref<number | null>(null);

const filters = ref<FilterPayload>({ advanced: false });
const block = ref<boolean | null>(null);
const categoryName = ref("");
const priority = ref("");
const senderName = ref("");
const senderEmail = ref("");
const searchInput = ref("");

const debounceTimer = ref<number | undefined>(undefined);
const isNavMinimized = ref(localStorage.getItem('navbarMinimized') === 'true');

onMounted(async () => {
    await fetchRules();
    fetchEmailSenders();
    fetchCategories();

    const urlParams = new URLSearchParams(window.location.search);
    const editRule = urlParams.get("editRule");
    const ruleId = urlParams.get("idRule");
    const nameSender = urlParams.get("ruleName");
    const emailSender = urlParams.get("ruleEmail");

    if (editRule === "true" && ruleId) {
        fetchRuleById(ruleId);

        if (ruleSelected.value) {
            updateModalUpdateStatus(true);
            const newUrl = `${window.location.protocol}//${window.location.host}${window.location.pathname}`;
            window.history.replaceState({}, document.title, newUrl);
        }
    } else if (editRule === "false" && nameSender && emailSender) {
        senderSelected.value = { username: nameSender as string, email: emailSender as string };
        updateModalStatus(true);
        const newUrl = `${window.location.protocol}//${window.location.host}${window.location.pathname}`;
        window.history.replaceState({}, document.title, newUrl);
    }

    document.addEventListener("keydown", handleKeyDown);
    const container = document.querySelector(".custom-scrollbar");
    if (container) {
        container.addEventListener("scroll", handleScroll);
    }
});

onUnmounted(() => {
    const container = document.querySelector(".custom-scrollbar");
    if (container) {
        container.removeEventListener("scroll", handleScroll);
    }
});

watch(searchInput, (newValue) => {
    clearTimeout(debounceTimer.value);

    if (newValue.trim() !== "" && !filters.value.advanced) {
        // Set up a timer to call fetchRules after 900ms of inactivity
        debounceTimer.value = setTimeout(() => {
            fetchRules();
        }, 900);
    }
});

provide("totalRules", totalRules);
provide("block", block);
provide("categoryName", categoryName);
provide("priority", priority);
provide("senderName", senderName);
provide("senderEmail", senderEmail);
provide("searchInput", searchInput);
provide("displayPopup", displayPopup);
provide("fetchRules", fetchRules);

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

function handleKeyDown(event: KeyboardEvent) {
    if (event.ctrlKey && event.key === "k") {
        (document.getElementById("search-field") as HTMLInputElement).focus();
        event.preventDefault();
    }
}

function updateModalStatus(status: boolean) {
    showModal.value = status;
}

function updateModalUpdateStatus(status: boolean) {
    showUpdateModal.value = status;
}

function handleEditRule(rule: any) {
    ruleSelected.value = rule;
    showUpdateModal.value = true;
}

async function fetchRules() {
    if (
        block.value !== null ||
        categoryName.value.trim() !== "" ||
        priority.value.trim() !== "" ||
        senderName.value.trim() !== "" ||
        senderEmail.value.trim() !== ""
    ) {
        filters.value = {
            advanced: true,
            ...(block.value !== null && { block: block.value }),
            ...(categoryName.value && { categoryName: categoryName.value }),
            ...(priority.value && { priority: priority.value }),
            ...(senderName.value && { senderName: senderName.value }),
            ...(senderEmail.value && { senderEmail: senderEmail.value }),
        };
    } else {
        filters.value = {
            search: searchInput.value.trim(),
        };
    }

    let result = await postData("user/rules_ids/", filters.value);

    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.failedToFetchRules"),
            result.error as string
        );
        return;
    }

    ruleIds.value = result.data.ids;
    totalRules.value = result.data.count;

    result = await postData("user/get_rules_data/", { ids: result.data.ids.slice(0, 100) });

    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.failedToFetchRules"),
            result.error as string
        );
        return;
    }

    rules.value = result.data.rulesData.map((rule: RuleData) => ({
        id: rule.id,
        name: rule.username,
        email: rule.email,
        category: rule.category,
        priority: rule.priority,
        block: rule.block,
    }));
}

const handleScroll = () => {
    const container = document.querySelector(".custom-scrollbar");
    if (container) {
        const { scrollTop, scrollHeight, clientHeight } = container;
        const threshold = 250;
        if (scrollTop + clientHeight >= scrollHeight - threshold && !isLoading.value) {
            loadMoreRules();
        }
    }
};

const loadMoreRules = async () => {
    if (isLoading.value) return;
    isLoading.value = true;

    const startIndex = (currentPage.value - 1) * rulesPerPage;
    const endIndex = startIndex + rulesPerPage;
    const idsToFetch = ruleIds.value.slice(startIndex, endIndex);

    if (idsToFetch.length > 0) {
        const result = await postData("user/get_rules_data/", { ids: idsToFetch });

        if (!result.success) {
            displayPopup(
                "error",
                i18n.global.t("rulesPage.popUpConstants.errorMessages.failedToFetchRules"),
                result.error as string
            );
            return;
        }

        rules.value = [
            ...rules.value,
            result.data.rulesData.map((rule: RuleData) => ({
                id: rule.id,
                name: rule.username,
                email: rule.email,
                category: rule.category,
                priority: rule.priority,
                block: rule.block,
            })),
        ];

        currentPage.value++;
    }

    isLoading.value = false;
};

async function fetchRuleById(idRule: string) {
    const result = await getData(`user/rules/${idRule}/`);

    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.failedToFetchRuleById"),
            result.error as string
        );
        return;
    }

    ruleSelected.value = {
        id: result.data.id,
        name: result.data.senderName,
        email: result.data.senderEmail,
        category: result.data.categoryName,
        priority: result.data.priority,
        mailStop: result.data.block,
    };
}

async function fetchCategories() {
    const result = await getData("user/categories/");
    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.failedToFetchCategories"),
            result.error as string
        );
        return;
    }

    categories.value = result.data;
}

async function fetchEmailSenders() {
    const result = await getData("user/contacts/");

    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.failedToFetchContacts"),
            result.error as string
        );
        return;
    }

    emailSenders.value = result.data;
}
</script>
