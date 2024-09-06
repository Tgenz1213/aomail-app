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
            <div class="w-[90px] 2xl:w-[100px] bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <NavBarSmall />
            </div>
            <div class="flex-1 bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <div class="flex flex-col h-full relative">
                    <div class="divide-y divide-gray-200">
                        <div
                            class="flex items-center justify-center h-[70px] 2xl:h-[80px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-50"
                        >
                            <h1 class="font-poppins font-medium">
                                {{ $t("rulesPage.assistantRules") }}
                            </h1>
                        </div>
                        <SearchBar @input="updateSearchQuery"></SearchBar>
                    </div>
                    <div
                        v-if="rules.length > 0"
                        class="flex-grow overflow-y-auto"
                        style="margin-right: 2px; margin-bottom: 120px"
                    >
                        <div class="p-6">
                            <ul
                                v-if="filteredRules.length > 0"
                                category="list"
                                class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
                            >
                                <li
                                    v-for="rule in filteredRules"
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
                                {{ $t("rulesPage.assistantRules") }}
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
import { getData } from "@/global/fetchData";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { ref, onMounted, computed, provide } from "vue";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import NewRuleModal from "./components/NewRuleModal.vue";
import UpdateRuleModal from "./components/UpdateRuleModal.vue";
import Rule from "./components/Rule.vue";
import SearchBar from "./components/SearchBar.vue";
import { EmailSender } from "@/global/types";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";

const showModal = ref(false);
const showUpdateModal = ref(false);
const rules = ref<any[]>([]);
const categories = ref<any[]>([]);
const emailSenders = ref<any[]>([]);
const senderSelected = ref<EmailSender | null>(null);
const ruleSelected = ref<any>(null);
const searchQuery = ref("");
const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

provide("displayPopup", displayPopup);

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

const filteredRules = computed(() => {
    if (!searchQuery.value) return rules.value;
    return rules.value.filter(
        (rule) =>
            rule.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            rule.email.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            (rule.category && rule.category.toLowerCase().includes(searchQuery.value.toLowerCase()))
    );
});

function handleKeyDown(event: KeyboardEvent) {
    if (event.ctrlKey && event.key === "k") {
        (document.getElementById("search-field") as HTMLInputElement).focus();
        event.preventDefault();
    }
}

function updateSearchQuery(event: Event) {
    searchQuery.value = (event.target as HTMLInputElement).value;
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
    const result = await getData("user/rules/");

    if (!result.success) {
        displayPopup?.("error", "Failed to fetch rules", result.error as string);
        return;
    }

    rules.value = result.data.map((rule: any) => ({
        id: rule.id,
        name: rule.senderName,
        email: rule.senderEmail,
        category: rule.categoryName,
        priority: rule.priority,
        mailStop: rule.block,
    }));
}

async function fetchRuleById(idRule: string) {
    const result = await getData(`user/rules/${idRule}/`);

    if (!result.success) {
        displayPopup?.("error", "Failed to fetch rule by id", result.error as string);
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
        displayPopup?.("error", "Failed to fetch categories", result.error as string);
        return;
    }

    categories.value = result.data;
}

async function fetchEmailSenders() {
    const result = await getData("user/contacts/");

    if (!result.success) {
        displayPopup?.("error", "Failed to fetch contacts", result.error as string);
        return;
    }

    emailSenders.value = result.data;
}

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);

    fetchRules();
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
});
</script>
