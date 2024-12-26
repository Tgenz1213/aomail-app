<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
    />
    <NewCategoryModal
        :isOpen="isModalNewCategoryOpen"
        @close="closeNewCategoryModal"
        @selectCategory="selectCategory"
    />
    <UpdateCategoryModal
        :isOpen="isModalUpdateCategoryOpen"
        :category="categoryToUpdate"
        @close="closeUpdateCategoryModal"
        @selectCategory="selectCategory"
    />
    <NewFilterModal :isOpen="isModalNewFilterOpen" @close="closeNewFilterModal" />
    <UpdateFilterModal :isOpen="isModalUpdateFilterOpen" :filter="filterToUpdate" @close="closeUpdateFilterModal" />
    <div class="flex flex-col justify-center items-center h-screen">
        <div class="flex h-full w-full">
            <div class="w-[90px] 2xl:w-[100px] bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <NavBarSmall />
            </div>
            <div class="flex-1 bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <div class="flex flex-col h-full relative">
                    <div
                        v-if="showFeedbackForm"
                        class="bg-gray-50 border-b border-black shadow-sm border-opacity-10 overflow-hidden whitespace-nowrap"
                    >
                        <button>
                            <XMarkIcon class="h-6 w-6" @click="hideFeedbackForm" />
                        </button>
                        <p class="animate-marquee">
                            <button
                                class="rounded-md bg-gray-800 p-2 m-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:ring-gray-800"
                                data-tally-open="n0bPqB"
                                data-tally-layout="modal"
                                data-tally-width="700"
                                data-tally-align-left="1"
                                data-tally-emoji-text="👋"
                                data-tally-emoji-animation="wave"
                            >
                                You have been using Aomail for a few weeks, could you give us some feedback? 👋
                            </button>
                        </p>
                    </div>
                    <div
                        v-if="isFreeTrialExpired"
                        class="bg-gray-50 border-b border-black shadow-sm border-opacity-10 overflow-hidden whitespace-nowrap"
                    >
                        <p class="animate-marquee">
                            <button
                                @click="goToSubscriptionSection"
                                class="rounded-md bg-gray-800 p-2 m-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:ring-gray-800"
                            >
                                {{ $t("constants.isFreeTrialExpired") }}
                                {{ $t("constants.freeTrialExpiredDesc") }}
                            </button>
                        </p>
                    </div>
                    <Categories
                        :selected-category="selectedCategory"
                        :category-totals="categoryTotals"
                        @select-category="selectCategory"
                        @open-new-category-modal="openNewCategoryModal"
                        @open-update-category-modal="openUpdateCategoryModal"
                    />
                    <div v-if="!hasEmails" class="flex-1">
                        <div v-if="isLoading || firstLoad" class="flex flex-col justify-center items-center h-full">
                            <svg class="animate-spin h-12 w-12 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                            </svg>
                            <p class="mt-4 text-lg font-semibold">{{ $t("loadingEmails") }}</p>
                        </div>
                        <div v-else class="flex flex-col w-full h-full rounded-xl">
                            <div v-if="toSearch || selectedFilter"><SearchBar /></div>
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
                                <span v-if="!toSearch" class="mt-2 block text-md font-semibold text-gray-900">
                                    {{ $t("homePage.noNewEmail") }}
                                </span>
                                <span v-else class="mt-2 block text-md font-semibold text-gray-900">
                                    {{ $t("homePage.noEmailFound") }}
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
            <!-- NOT FOR v1 
            <AssistantChat v-if="!isHidden" @toggle-visibility="toggleVisibility" />-->
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, provide, onMounted, onUnmounted, watch } from "vue";
import { getData, postData } from "@/global/fetchData";
import { Email, Category, FetchDataResult } from "@/global/types";
import { Filter } from "./utils/types";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import NewCategoryModal from "./components/NewCategoryModal.vue";
import UpdateCategoryModal from "./components/UpdateCategoryModal.vue";
import NewFilterModal from "./components/NewFilterModal.vue";
import UpdateFilterModal from "./components/UpdateFilterModal.vue";
import ImportantEmail from "@/global/components/ImportantEmails.vue";
import InformativeEmail from "@/global/components/InformativeEmails.vue";
import UselessEmail from "@/global/components/UselessEmails.vue";
import ReadEmail from "./components/ReadEmails.vue";
//import AssistantChat from "./components/AssistantChat.vue"; DESACTIVATED FOR NOW DO NOT DELETE
import Categories from "./components/Categories.vue";
import SearchBar from "./components/SearchBar.vue";
import { XMarkIcon } from "@heroicons/vue/20/solid";

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);
const toSearch = ref(false);
const showFeedbackForm = ref(false);
const isFreeTrialExpired = ref(false);

const emails = ref<{ [key: string]: { [key: string]: Email[] } }>({});
const selectedCategory = ref<string>("");
const activeFilters = ref<{ [category: string]: Filter | undefined }>({});
const selectedFilter = ref<Filter | undefined>(activeFilters.value[selectedCategory.value]);
const categoryToUpdate = ref<Category | null>(null);
const filterToUpdate = ref<Filter | null>(null);
const isModalNewCategoryOpen = ref(false);
const isModalUpdateCategoryOpen = ref(false);
const isModalNewFilterOpen = ref(false);
const isModalUpdateFilterOpen = ref(false);
//const isHidden = ref(false); DESACTIVATED FOR NOW DO NOT DELETE
const categories = ref<Category[]>([]);
const filters = ref<{ [categoryName: string]: Filter[] }>({});
const categoryTotals = ref<{ [key: string]: number }>({});
const emailsPerPage = 10;
const currentPage = ref(1);
const isLoading = ref(false);
const firstLoad = ref(true);
const allEmailIds = ref<string[]>([]);
const searchQuery = ref("");

watch(
    () => [activeFilters.value, selectedCategory.value],
    () => {
        selectedFilter.value = activeFilters.value[selectedCategory.value];
    },
    { immediate: true }
);

const hideFeedbackForm = () => {
    showFeedbackForm.value = false;
    localStorage.setItem("hideFeedbackForm", "true");
};

const goToSubscriptionSection = () => {
    window.location.replace("/settings?goto=subscription");
};

const fetchEmailsData = async (categoryName: string) => {
    currentPage.value = 1;
    emails.value = {};
    allEmailIds.value = [];
    let response: FetchDataResult;

    if (selectedFilter.value) {
        const priorities = [];
        if (selectedFilter.value?.important) {
            priorities.push("important");
        }
        if (selectedFilter.value?.informative) {
            priorities.push("informative");
        }
        if (selectedFilter.value?.useless) {
            priorities.push("useless");
        }

        if (toSearch.value) {
            response = await postData("user/emails_ids/", {
                advanced: true,
                search: searchQuery.value,
                category: categoryName,
                priority: priorities,
                spam: selectedFilter.value?.spam,
                scam: selectedFilter.value?.scam,
                meeting: selectedFilter.value?.meeting,
                notification: selectedFilter.value?.notification,
                newsletter: selectedFilter.value?.newsletter,
                read: selectedFilter.value?.read,
            });
        } else {
            response = await postData("user/emails_ids/", {
                advanced: true,
                category: categoryName,
                priority: priorities,
                spam: selectedFilter.value?.spam,
                scam: selectedFilter.value?.scam,
                meeting: selectedFilter.value?.meeting,
                notification: selectedFilter.value?.notification,
                newsletter: selectedFilter.value?.newsletter,
                read: selectedFilter.value?.read,
            });
        }
    } else {
        if (toSearch.value) {
            response = await postData("user/emails_ids/", {
                search: searchQuery.value,
                category: categoryName,
            });
        } else {
            response = await postData("user/emails_ids/", { category: categoryName });
        }
    }

    allEmailIds.value = response.data.ids;

    await loadMoreEmails();
};

const loadMoreEmails = async () => {
    if (isLoading.value) return;
    isLoading.value = true;

    const startIndex = (currentPage.value - 1) * emailsPerPage;
    const endIndex = startIndex + emailsPerPage;
    const idsToFetch = allEmailIds.value.slice(startIndex, endIndex);

    if (idsToFetch.length > 0) {
        const emails_details = await postData("user/get_emails_data/", { ids: idsToFetch });
        const newEmails = emails_details.data.data;

        for (const category in newEmails) {
            if (!emails.value[category]) {
                emails.value[category] = {};
            }
            for (const type in newEmails[category]) {
                if (!emails.value[category][type]) {
                    emails.value[category][type] = [];
                }
                emails.value[category][type].push(...newEmails[category][type]);
            }
        }

        currentPage.value++;
    }

    isLoading.value = false;
};

const handleScroll = () => {
    const container = document.querySelector(".custom-scrollbar");
    if (container) {
        const { scrollTop, scrollHeight, clientHeight } = container;
        const threshold = 250;
        if (scrollTop + clientHeight >= scrollHeight - threshold && !isLoading.value) {
            loadMoreEmails();
        }
    }
};

const scroll = () => {
    const container = document.querySelector(".custom-scrollbar");
    if (container) {
        container.addEventListener("scroll", handleScroll);
    }
};

async function fetchCategoriesAndTotals() {
    const categoriesResponse = await getData("user/categories");
    categories.value = categoriesResponse.data;

    const totalsPromises = categories.value.map((category) =>
        postData("user/emails_ids/", {
            subject: "",
            category: category.name,
            read: false,
            replyLater: false,
            advanced: true,
        })
    );
    const totalsResponses = await Promise.all(totalsPromises);

    categories.value.forEach((category, index) => {
        categoryTotals.value[category.name] = totalsResponses[index].data.count;
    });
}

const fetchFiltersData = async (categoryName: string) => {
    const response = await postData("user/filters/", { category: categoryName });
    filters.value[categoryName] = response.data;
};

const openNewFilterModal = () => {
    isModalNewFilterOpen.value = true;
};

const openUpdateFilterModal = (filter: Filter) => {
    filterToUpdate.value = filter;
    isModalUpdateFilterOpen.value = true;
};

provide("displayPopup", displayPopup);
provide("fetchEmailsData", fetchEmailsData);
provide("fetchCategoriesAndTotals", fetchCategoriesAndTotals);
provide("openNewFilterModal", openNewFilterModal);
provide("openUpdateFilterModal", openUpdateFilterModal);
provide("fetchFiltersData", fetchFiltersData);
provide("scroll", scroll);
provide("handleScroll", handleScroll);
provide("emails", emails);
provide("categories", categories);
provide("filters", filters);
provide("selectedCategory", selectedCategory);
provide("selectedFilter", selectedFilter);
provide("activeFilters", activeFilters);
provide("toSearch", toSearch);
provide("searchQuery", searchQuery);

const addCategoryToEmails = (emailList: Email[], category: string): Email[] => {
    return emailList.map((email) => ({
        ...email,
        category: category,
    }));
};

const importantEmails = computed(() => {
    if (!emails.value || !selectedCategory.value) return [];
    const categoryEmails = emails.value[selectedCategory.value]?.important || [];
    const unreadEmails = categoryEmails.filter((email) => !email.read && !email.answerLater && !email.archive);
    return addCategoryToEmails(unreadEmails, selectedCategory.value);
});

const informativeEmails = computed(() => {
    if (!emails.value || !selectedCategory.value) return [];
    const categoryEmails = emails.value[selectedCategory.value]?.informative || [];
    const unreadEmails = categoryEmails.filter((email) => !email.read && !email.answerLater && !email.archive);
    return addCategoryToEmails(unreadEmails, selectedCategory.value);
});

const uselessEmails = computed(() => {
    if (!emails.value || !selectedCategory.value) return [];
    const categoryEmails = emails.value[selectedCategory.value]?.useless || [];
    const unreadEmails = categoryEmails.filter((email) => !email.read && !email.answerLater && !email.archive);
    return addCategoryToEmails(unreadEmails, selectedCategory.value);
});

const readEmails = computed(() => {
    if (!emails.value || !selectedCategory.value) return [];
    const allEmails = [
        ...(emails.value[selectedCategory.value]?.important || []),
        ...(emails.value[selectedCategory.value]?.informative || []),
        ...(emails.value[selectedCategory.value]?.useless || []),
    ];
    const filteredEmails = allEmails.filter((email) => !email.answerLater && !email.archive);
    return addCategoryToEmails(filteredEmails, selectedCategory.value);
});

const hasEmails = computed(() => {
    if (!emails.value || !selectedCategory.value) return false;

    const categoryEmails = emails.value[selectedCategory.value];
    if (!categoryEmails) return false;

    const importantEmails = categoryEmails.important?.filter((email) => !email.answerLater && !email.archive) || [];
    const informativeEmails = categoryEmails.informative?.filter((email) => !email.answerLater && !email.archive) || [];
    const uselessEmails = categoryEmails.useless?.filter((email) => !email.answerLater && !email.archive) || [];

    return importantEmails.length > 0 || informativeEmails.length > 0 || uselessEmails.length > 0;
});

const selectCategory = async (category: Category) => {
    firstLoad.value = true;
    selectedCategory.value = category.name;
    currentPage.value = 1;
    emails.value = {};
    allEmailIds.value = [];
    toSearch.value = false;
    searchQuery.value = "";

    await fetchEmailsData(selectedCategory.value);
    await fetchFiltersData(selectedCategory.value);
    localStorage.setItem("selectedCategory", category.name);

    firstLoad.value = false;

    scroll();
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

const closeUpdateFilterModal = () => {
    isModalUpdateFilterOpen.value = false;
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

const loadActiveFilters = async () => {
    const storedFilters = localStorage.getItem("activeFilters");
    if (storedFilters) {
        const parsedFilters = JSON.parse(storedFilters);
        for (const category in parsedFilters) {
            await fetchFiltersData(category);
            const filterArray = filters.value[category];
            if (filterArray && parsedFilters[category]) {
                const filter = filterArray.find((f) => f.name === parsedFilters[category].name);
                if (filter) {
                    activeFilters.value[category] = filter;
                }
            }
        }
    }
};

const processFeedBackForm = async () => {
    const result = await getData("user/preferences/plan/");
    if (result.success) {
        const differenceInDays = Math.round(
            (new Date().getTime() - new Date(result.data.createdAt).getTime()) / (1000 * 3600 * 24)
        );

        if (differenceInDays >= 14 && !localStorage.getItem("hideFeedbackForm")) {
            showFeedbackForm.value = true;
        }

        if (result.data.isTrial) {
            if (new Date().getTime() > new Date(result.data.expiresThe).getTime()) {
                isFreeTrialExpired.value = true;
            }
        }
    }
};

onMounted(async () => {
    processFeedBackForm();
    loadActiveFilters();
    await fetchCategoriesAndTotals();

    const storedTopic = localStorage.getItem("selectedCategory");
    if (storedTopic) {
        selectedCategory.value = storedTopic;
    } else {
        selectedCategory.value = "Others";
    }

    await loadActiveFilters();

    await fetchEmailsData(selectedCategory.value);
    await fetchFiltersData(selectedCategory.value);

    firstLoad.value = false;

    scroll();
});

onUnmounted(() => {
    const container = document.querySelector(".custom-scrollbar");
    if (container) {
        container.removeEventListener("scroll", handleScroll);
    }
});
</script>
