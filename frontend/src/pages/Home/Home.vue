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
                    <Categories
                        :selected-category="selectedCategory"
                        :category-totals="categoryTotals"
                        @select-category="selectCategory"
                        @open-new-category-modal="openNewCategoryModal"
                        @open-update-category-modal="openUpdateCategoryModal"
                    />
                    <div v-if="!hasEmails" class="flex-1">
                        <div class="flex flex-col w-full h-full rounded-xl">
                            <div
                                class="flex flex-col justify-center items-center h-full m-5 rounded-lg border-2 border-dashed border-gray-400 p-12 text-center hover:border-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1"
                                    stroke="currentColor"
                                    class="mx-auto h-14 w-14 text-gray-400"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
                                    />
                                </svg>
                                <span class="mt-2 block text-md font-semibold text-gray-900">
                                    {{ $t("homePage.noNewEmail") }}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div v-else class="flex-1 overflow-y-auto custom-scrollbar">
                        <SearchBar />
                        <ImportantEmail :emails="importantEmails" />
                        <InformativeEmail :emails="informativeEmails" />
                        <UselessEmail :emails="uselessEmails" />
                        <ReadEmail :emails="readEmails" />
                    </div>
                </div>
            </div>
            <AssistantChat v-if="!isHidden" @toggle-visibility="toggleVisibility" />
        </div>
        <NewCategoryModal :isOpen="isModalNewCategoryOpen" @close="closeNewCategoryModal" />
        <UpdateCategoryModal
            :isOpen="isModalUpdateCategoryOpen"
            :category="categoryToUpdate"
            @close="closeUpdateCategoryModal"
        />
        <NewFilterModal :isOpen="isModalNewFilterOpen" @close="closeNewFilterModal" />
    </div>
</template>

<script setup lang="ts">
import { ref, computed, provide, onMounted } from "vue";
import { getData, postData } from "@/global/fetchData";
import { Email, Category } from "@/global/types";
import { Filter } from './utils/types';
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import NewCategoryModal from "./components/NewCategoryModal.vue";
import UpdateCategoryModal from "./components/UpdateCategoryModal.vue";
import NewFilterModal from "./components/NewFilterModal.vue";
import ImportantEmail from "@/global/components/ImportantEmails.vue";
import InformativeEmail from "@/global/components/InformativeEmails.vue";
import UselessEmail from "@/global/components/UselessEmails.vue";
import ReadEmail from "./components/ReadEmails.vue";
import AssistantChat from "./components/AssistantChat.vue";
import Categories from "./components/Categories.vue";
import SearchBar from "./components/SearchBar.vue";

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

const emails = ref<{ [key: string]: { [key: string]: Email[] } }>({});
const selectedCategory = ref<string>("");
const categoryToUpdate = ref<Category | null>(null);
const isModalNewCategoryOpen = ref(false);
const isModalUpdateCategoryOpen = ref(false);
const isModalNewFilterOpen = ref(false);
const isHidden = ref(false);
const categories = ref<Category[]>([]);
const filters = ref<Filter[]>([]);
const categoryTotals = ref<{ [key: string]: number }>({});

const fetchEmailsData = async (categoryName: string) => {
    const response = await postData("user/emails_ids/", { subject: "", category: categoryName });
    const emails_details = await postData("user/get_emails_data/", { ids: response.data.ids });
    emails.value = emails_details.data.data;
    console.log(emails.value);
};

async function fetchCategoriesAndTotals() {
    const categoriesResponse = await getData("user/categories");
    categories.value = categoriesResponse.data;

    const totalsPromises = categories.value.map((category) =>
        postData("user/emails_ids/", { subject: "", category: category.name, read: false, advanced: true })
    );
    const totalsResponses = await Promise.all(totalsPromises);

    console.log("TOTAL", totalsResponses);

    categories.value.forEach((category, index) => {
        categoryTotals.value[category.name] = totalsResponses[index].data.count;
    });
}

const openNewFilterModal = () => {
    isModalNewFilterOpen.value = true;
}

provide("displayPopup", displayPopup);
provide("fetchEmailsData", fetchEmailsData);
provide("fetchCategoriesAndTotals", fetchCategoriesAndTotals);
provide("openNewFilterModal", openNewFilterModal);
provide("categories", categories);
provide("filters", filters);
provide("selectedCategory", selectedCategory);

const addCategoryToEmails = (emailList: Email[], category: string): Email[] => {
    return emailList.map((email) => ({
        ...email,
        category: category,
    }));
};

const importantEmails = computed(() => {
    if (!emails.value || !selectedCategory.value) return [];
    const categoryEmails = emails.value[selectedCategory.value]?.important || [];
    return addCategoryToEmails(categoryEmails, selectedCategory.value);
});

const informativeEmails = computed(() => {
    if (!emails.value || !selectedCategory.value) return [];
    const categoryEmails = emails.value[selectedCategory.value]?.informative || [];
    return addCategoryToEmails(categoryEmails, selectedCategory.value);
});

const uselessEmails = computed(() => {
    if (!emails.value || !selectedCategory.value) return [];
    const categoryEmails = emails.value[selectedCategory.value]?.useless || [];
    return addCategoryToEmails(categoryEmails, selectedCategory.value);
});

const readEmails = computed(() => {
    if (!emails.value || !selectedCategory.value) return [];
    const allEmails = [
        ...(emails.value[selectedCategory.value]?.important || []),
        ...(emails.value[selectedCategory.value]?.informative || []),
        ...(emails.value[selectedCategory.value]?.useless || [])
    ];
    return addCategoryToEmails(allEmails, selectedCategory.value);
});

const hasEmails = computed(() => {
    if (!emails.value || !selectedCategory.value) return false;
    const categoryEmails = emails.value[selectedCategory.value];
    return categoryEmails && (
        (categoryEmails.important && categoryEmails.important.length > 0) ||
        (categoryEmails.informative && categoryEmails.informative.length > 0) ||
        (categoryEmails.useless && categoryEmails.useless.length > 0)
    );
});

const toggleVisibility = () => {
    isHidden.value = !isHidden.value;
};

const selectCategory = (category: Category) => {
    selectedCategory.value = category.name;
    fetchEmailsData(selectedCategory.value);
    localStorage.setItem("selectedCategory", category.name);
};

const openNewCategoryModal = () => {
    isModalNewCategoryOpen.value = true;
};

const closeNewCategoryModal = () => {
    isModalNewCategoryOpen.value = false;
};

const closeNewFilterModal = () => {
    isModalNewFilterOpen.value = false;
};

const openUpdateCategoryModal = (category: Category) => {
    categoryToUpdate.value = category;
    isModalUpdateCategoryOpen.value = true;
};

const closeUpdateCategoryModal = () => {
    isModalUpdateCategoryOpen.value = false;
    categoryToUpdate.value = null;
};

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

onMounted(() => {
    fetchCategoriesAndTotals();
    const storedTopic = localStorage.getItem("selectedCategory");
    if (storedTopic) {
        selectedCategory.value = storedTopic;
    } else {
        selectedCategory.value = "Others";
    }
    console.log("DEBUG 0", emails.value);
    fetchEmailsData(selectedCategory.value);
});
</script>
