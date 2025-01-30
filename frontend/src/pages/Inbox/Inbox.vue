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
            <div
                :class="['ring-1 shadow-sm ring-black ring-opacity-5', isNavMinimized ? 'w-20' : 'w-60']"
            >
                <Navbar @update:isMinimized="(value) => (isNavMinimized = value)" />
            </div>
            <!-- TO IMPLEMENT LATER :style="{ width: emailsContainerWidth + '%' }"-->
            <div
                class="bg-white ring-1 shadow-sm ring-black ring-opacity-5 h-full"
            >
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
                                {{ $t("constants.freeTrialExpired") }}
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
                            <svg
                                class="animate-spin h-12 w-12 text-black"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                            >
                                <circle
                                    class="opacity-25"
                                    cx="12"
                                    cy="12"
                                    r="10"
                                    stroke="currentColor"
                                    stroke-width="4"
                                ></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                            </svg>
                            <p class="mt-4 text-lg font-semibold">{{ $t("constants.loadingEmails") }}</p>
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
            <!-- TO IMPLEMENT LATER
            <div class="drag-wrapper" @mousedown="initDrag">
                <div class="separator"></div>
                <div class="drag-overlay"></div>
            </div>

            <div
                class="flex overflow-y-auto custom-scrollbar ring-1 shadow-sm ring-black ring-opacity-5"
                :style="{ width: assistantChatWidth + '%' }"
            >
                <AssistantChat />
            </div>-->
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, provide, onMounted, onUnmounted, watch, onBeforeUnmount } from "vue";
import { getData, postData, putData } from "@/global/fetchData";
import { Email, Category, FetchDataResult, Filter } from "@/global/types";
import { DEFAULT_CATEGORY } from "@/global/const";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import Navbar from "@/global/components/Navbar.vue";
import NewCategoryModal from "./components/NewCategoryModal.vue";
import UpdateCategoryModal from "./components/UpdateCategoryModal.vue";
import NewFilterModal from "./components/NewFilterModal.vue";
import UpdateFilterModal from "./components/UpdateFilterModal.vue";
import ImportantEmail from "@/global/components/ImportantEmails.vue";
import InformativeEmail from "@/global/components/InformativeEmails.vue";
import UselessEmail from "@/global/components/UselessEmails.vue";
import ReadEmail from "./components/ReadEmails.vue";
import AssistantChat from "./components/AssistantChat.vue";
import Categories from "./components/Categories.vue";
import SearchBar from "./components/SearchBar.vue";
import { XMarkIcon } from "@heroicons/vue/20/solid";
import { i18n } from "@/global/preferences";

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);
const toSearch = ref(false);
const showFeedbackForm = ref(false);
const isFreeTrialExpired = ref(false);
const isNavMinimized = ref(localStorage.getItem("navbarMinimized") === "true");

const emails = ref<Record<string, Record<string, Email[]>>>({});
const selectedCategory = ref<string>("");
const activeFilters = ref<{ [category: string]: Filter | undefined }>({});
const selectedFilter = ref<Filter | undefined>(activeFilters.value[selectedCategory.value]);
const categoryToUpdate = ref<Category | null>(null);
const filterToUpdate = ref<Filter | null>(null);
const isModalNewCategoryOpen = ref(false);
const isModalUpdateCategoryOpen = ref(false);
const isModalNewFilterOpen = ref(false);
const isModalUpdateFilterOpen = ref(false);
const categories = ref<Category[]>([]);
const filters = ref<{ [categoryName: string]: Filter[] }>({});
const categoryTotals = ref<{ [key: string]: number }>({});
const emailsPerPage = 10;
const currentPage = ref(1);
const isLoading = ref(false);
const firstLoad = ref(true);
const allEmailIds = ref<string[]>([]);
const searchQuery = ref("");
const uselessCount = ref(0);
const importantCount = ref(0);
const informativeCount = ref(0);
const readCount = ref(0);
const previousScrollTop = ref(0);
const previousTime = ref(0);
const importantIds = ref<number[]>([]);
const informativeIds = ref<number[]>([]);
const uselessIds = ref<number[]>([]);
const readIds = ref<number[]>([]);
const isMarking = ref({
    important: false,
    informative: false,
    useless: false,
    archiveRead: false,
});

const emailsContainerWidth = ref<number>(parseFloat(localStorage.getItem("inboxEmailsWidth") || '70')); // Default to 70%
const assistantChatWidth = ref<number>(parseFloat(localStorage.getItem("inboxAssistantChatWidth") || '30')); // Default to 30%

let totalPages = computed(() => {
    return Math.ceil(allEmailIds.value.length / emailsPerPage);
});

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

const fetchEmailCounts = async (categoryName: string) => {
    let response: FetchDataResult;

    if (selectedFilter.value?.id === 0) {
        // case when using All emails filter
        response = await postData("user/emails_counts/", {
            category: categoryName,
        });
    } else if (selectedFilter.value) {
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
            response = await postData("user/emails_counts/", {
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
            response = await postData("user/emails_counts/", {
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
            response = await postData("user/emails_counts/", {
                search: searchQuery.value,
                category: categoryName,
            });
        } else {
            response = await postData("user/emails_counts/", {
                category: categoryName,
            });
        }
    }
    const data = response.data;
    uselessCount.value = data.useless_count;
    importantCount.value = data.important_count;
    informativeCount.value = data.informative_count;
    readCount.value = data.read_count;
    uselessIds.value = data.useless_ids;
    importantIds.value = data.important_ids;
    informativeIds.value = data.informative_ids;
    readIds.value = data.read_ids;
};

const fetchEmailsData = async (categoryName: string) => {
    currentPage.value = 1;
    emails.value = {};
    allEmailIds.value = [];
    let response: FetchDataResult;

    if (selectedFilter.value?.id === 0) {
        // case when using All emails filter
        response = await postData("user/emails_ids/", { category: categoryName });
    } else if (selectedFilter.value) {
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
    console.log("allEmailIds", response.data.ids);

    await loadMoreEmails();
};

async function loadPage(pageNumber: number) {
    const startIndex = (pageNumber - 1) * emailsPerPage;
    const endIndex = startIndex + emailsPerPage;
    const idsToFetch = allEmailIds.value.slice(startIndex, endIndex);

    if (!idsToFetch.length) return;

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
}

const loadMoreEmails = async (pagesToLoad = 1) => {
    if (isLoading.value) return;
    isLoading.value = true;

    for (let i = 0; i < pagesToLoad; i++) {
        if (currentPage.value <= totalPages.value) {
            await loadPage(currentPage.value);
            currentPage.value++;
        } else {
            break;
        }
    }

    if (currentPage.value <= totalPages.value) {
        loadPage(currentPage.value).catch((err) => {
            console.error("Prefetch error:", err);
        });
        currentPage.value++;
    }

    isLoading.value = false;
};

function debounce(func: (...args: any[]) => void, wait: number) {
    let timeout: ReturnType<typeof setTimeout> | null = null;
    return (...args: any[]) => {
        if (timeout) clearTimeout(timeout);
        timeout = setTimeout(() => {
            func(...args);
            timeout = null;
        }, wait);
    };
}

const handleScroll = debounce(() => {
    const container = document.querySelector(".custom-scrollbar");
    if (!container) return;

    const { scrollTop, scrollHeight, clientHeight } = container;
    const now = performance.now();
    const distance = Math.abs(scrollTop - previousScrollTop.value);
    const elapsedTime = now - previousTime.value;
    const speed = distance / elapsedTime || 0;

    previousScrollTop.value = scrollTop;
    previousTime.value = now;

    const threshold = 800;
    if (scrollTop + clientHeight >= scrollHeight - threshold && !isLoading.value) {
        if (speed > 1.5) {
            loadMoreEmails(2);
        } else {
            loadMoreEmails(1);
        }
    }
}, 100);

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
    if (response.data.length > 0) {
        response.data = [{ name: "All emails", id: 0 }, ...response.data];
    }
    filters.value[categoryName] = response.data;
};

const openNewFilterModal = () => {
    isModalNewFilterOpen.value = true;
};

const openUpdateFilterModal = (filter: Filter) => {
    filterToUpdate.value = filter;
    isModalUpdateFilterOpen.value = true;
};

const markCategoryAsRead = async (category: "important" | "informative" | "useless") => {
    isMarking.value[category] = true;

    try {
        let ids: number[] = [];
        switch (category) {
            case "important":
                ids = importantIds.value;
                break;
            case "informative":
                ids = informativeIds.value;
                break;
            case "useless":
                ids = uselessIds.value;
                break;
            default:
                ids = [];
        }

        if (ids.length === 0) {
            displayPopup?.("error", i18n.global.t("constants.popUpConstants.errorMessages.noEmailsToMark"), "");
            return;
        }

        const result = await putData("user/emails/update/", { ids, action: "read" });

        if (result.success) {
            await fetchEmailsData(selectedCategory.value);
            await fetchFiltersData(selectedCategory.value);
            await fetchEmailCounts(selectedCategory.value);

            displayPopup?.(
                "success",
                i18n.global.t("constants.popUpConstants.successMessages.emailsMarkedAsRead"),
                i18n.global.t("constants.popUpConstants.successMessages.emailsMarkedAsReadDescription")
            );
        } else {
            displayPopup?.(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.failedToMarkAsRead"),
                result.error as string
            );
        }
    } catch (error) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.unexpectedError"),
            (error as Error).message
        );
    } finally {
        isMarking.value[category] = false;
    }
};

const archiveReadEmails = async () => {
    const category = selectedCategory.value;
    if (!category) {
        displayPopup?.("error", i18n.global.t("constants.popUpConstants.errorMessages.noCategorySelected"), "");
        return;
    }

    isMarking.value["archiveRead"] = true;

    try {
        const readEmailsInCategory = readEmails.value;
        const ids = readEmailsInCategory.map((email) => email.id);

        if (ids.length === 0) {
            displayPopup?.("error", i18n.global.t("constants.popUpConstants.errorMessages.noEmailsToArchive"), "");
            return;
        }

        const result = await putData("user/emails/update/", { ids, action: "archive" });

        if (result.success) {
            await fetchEmailsData(category);
            await fetchFiltersData(category);
            await fetchEmailCounts(category);

            readEmailsInCategory.forEach((email) => {
                email.archive = true;
            });

            displayPopup?.(
                "success",
                i18n.global.t("constants.popUpConstants.successMessages.emailsArchived"),
                i18n.global.t("constants.popUpConstants.successMessages.emailsArchivedDescription")
            );
        } else {
            displayPopup?.(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.failedToArchive"),
                result.error as string
            );
        }
    } catch (error) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.unexpectedError"),
            (error as Error).message
        );
    } finally {
        isMarking.value["archiveRead"] = false;
    }
};

provide("markCategoryAsRead", markCategoryAsRead);
provide("archiveReadEmails", archiveReadEmails);
provide("displayPopup", displayPopup);
provide("fetchEmailsData", fetchEmailsData);
provide("fetchCategoriesAndTotals", fetchCategoriesAndTotals);
provide("openNewFilterModal", openNewFilterModal);
provide("openUpdateFilterModal", openUpdateFilterModal);
provide("fetchFiltersData", fetchFiltersData);
provide("scroll", scroll);
provide("handleScroll", handleScroll);
provide("isMarking", isMarking);
provide("emails", emails);
provide("categories", categories);
provide("filters", filters);
provide("selectedCategory", selectedCategory);
provide("selectedFilter", selectedFilter);
provide("activeFilters", activeFilters);
provide("toSearch", toSearch);
provide("searchQuery", searchQuery);
provide("uselessCount", uselessCount);
provide("importantCount", importantCount);
provide("informativeCount", informativeCount);
provide("readCount", readCount);
provide("loadMoreEmails", loadMoreEmails);

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
    const filteredEmails = allEmails.filter((email) => email.read && !email.answerLater && !email.archive);
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
    await fetchEmailCounts(selectedCategory.value);
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

// Drag state
const isDragging = ref(false);
const startX = ref(0);
const startEmailsWidth = ref(0);
const startAssistantWidth = ref(0);
const initialContainerWidth = ref(0);

// Initialize drag
const initDrag = (event: MouseEvent) => {
    isDragging.value = true;
    startX.value = event.clientX;
    startEmailsWidth.value = emailsContainerWidth.value;
    startAssistantWidth.value = assistantChatWidth.value;

    const container = (event.target as HTMLElement).closest('.flex');
    initialContainerWidth.value = container ? container.clientWidth : 0;

    window.addEventListener("mousemove", onDrag);
    window.addEventListener("mouseup", stopDrag);
};

// Handle dragging
const onDrag = (event: MouseEvent) => {
    if (!isDragging.value) return;

    const deltaX = event.clientX - startX.value;
    if (initialContainerWidth.value === 0) return;

    const deltaPercent = (deltaX / initialContainerWidth.value) * 100;
    let newEmailsWidth = startEmailsWidth.value + deltaPercent;
    let newAssistantWidth = startAssistantWidth.value - deltaPercent;

    const MIN_WIDTH = 20;
    const MAX_WIDTH = 80;

    if (newEmailsWidth < MIN_WIDTH) {
        newEmailsWidth = MIN_WIDTH;
        newAssistantWidth = 100 - MIN_WIDTH;
    } else if (newAssistantWidth < MIN_WIDTH) {
        newAssistantWidth = MIN_WIDTH;
        newEmailsWidth = 100 - MIN_WIDTH;
    } else if (newEmailsWidth > MAX_WIDTH) {
        newEmailsWidth = MAX_WIDTH;
        newAssistantWidth = 100 - MAX_WIDTH;
    } else if (newAssistantWidth > MAX_WIDTH) {
        newAssistantWidth = MAX_WIDTH;
        newEmailsWidth = 100 - MAX_WIDTH;
    }

    emailsContainerWidth.value = newEmailsWidth;
    assistantChatWidth.value = newAssistantWidth;
};

// Stop dragging
const stopDrag = () => {
    if (isDragging.value) {
        isDragging.value = false;
        saveWidths();
        window.removeEventListener("mousemove", onDrag);
        window.removeEventListener("mouseup", stopDrag);
    }
};

// Save widths to localStorage
const saveWidths = () => {
    localStorage.setItem("inboxEmailsWidth", emailsContainerWidth.value.toString());
    localStorage.setItem("inboxAssistantChatWidth", assistantChatWidth.value.toString());
};

onMounted(async () => {
    processFeedBackForm();
    loadActiveFilters();
    await fetchCategoriesAndTotals();

    const storedTopic = localStorage.getItem("selectedCategory");
    if (storedTopic) {
        selectedCategory.value = storedTopic;
    } else {
        selectedCategory.value = DEFAULT_CATEGORY;
    }

    await loadActiveFilters();

    await fetchEmailsData(selectedCategory.value);
    await fetchFiltersData(selectedCategory.value);
    await fetchEmailCounts(selectedCategory.value);

    firstLoad.value = false;

    scroll();
});

onUnmounted(() => {
    const container = document.querySelector(".custom-scrollbar");
    if (container) {
        container.removeEventListener("scroll", handleScroll);
    }
});

onBeforeUnmount(() => {
    window.removeEventListener("mousemove", onDrag);
    window.removeEventListener("mouseup", stopDrag);
});
</script>

<style scoped>
/* Draggable Divider Wrapper */
.drag-wrapper {
    position: relative;
    width: 5px; /* Increased width for easier dragging */
    height: 100%;
    cursor: col-resize;
    background: transparent;
    z-index: 10; /* Ensure it's above other elements */
}

/* Visible Separator */
.separator {
    position: absolute;
    left: 50%;
    top: 0;
    transform: translateX(-50%);
    width: 1px; /* Thinner separator */
    height: 100%;
    background-color: #e0e0e0;
    z-index: 1;
}

/* Transparent Drag Overlay */
.drag-overlay {
    position: absolute;
    left: -2px; /* Adjusted for increased wrapper width */
    top: 0;
    width: 9px; /* Increased for better usability */
    height: 100%;
    background: transparent;
    z-index: 2;
}

/* Hover Effect */
.drag-wrapper:hover .separator {
    background-color: #aaa;
}
</style>
