<template>
    <transition name="modal-fade">
        <Modal
            v-if="props.isOpen"
            @click.self="closeModal"
            class="fixed z-[250] top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
        >
            <div class="bg-white rounded-lg relative w-[550px] max-h-[90vh] overflow-y-auto">
                <!-- Modal header -->
                <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
                    <button
                        @click="closeModal"
                        type="button"
                        class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                    >
                        <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                    </button>
                </div>
                <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
                    <div class="ml-8 flex items-center space-x-1">
                        <p class="block leading-6 text-gray-900 font-medium">
                            {{ $t("homePage.modals.filterModal.updateFilter") }}
                        </p>
                    </div>
                </div>

                <!-- Modal body -->
                <div class="flex flex-col gap-4 px-8 py-6">
                    <p class="text-red-500" v-if="errorMessage">{{ errorMessage }}</p>

                    <!-- Filter Name -->
                    <div>
                        <label for="filterName" class="block text-sm font-medium leading-6 text-gray-900">
                            {{ $t("homePage.modals.filterModal.filterName") }}
                        </label>
                        <div class="mt-2">
                            <input
                                id="updateFilterName"
                                v-model="filterData.name"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"
                                :placeholder="$t('homePage.modals.filterModal.filterNamePlaceholder')"
                            />
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
                                    :id="IMPORTANT"
                                    v-model="filterData.important"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label :for="IMPORTANT" class="flex items-center">
                                    <span
                                        class="bg-indigo-100 text-indigo-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full"
                                    >
                                        <ExclamationCircleIcon class="h-4 w-4 items-center inline mr-1" />
                                        {{ $t("homePage.modals.filterModal.important") }}
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    :id="INFORMATIVE"
                                    v-model="filterData.informative"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label :for="INFORMATIVE" class="flex items-center">
                                    <span
                                        class="bg-blue-100 text-blue-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full"
                                    >
                                        <InformationCircleIcon class="h-4 w-4 inline mr-1" />
                                        {{ $t("homePage.modals.filterModal.informative") }}
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    :id="USELESS"
                                    v-model="filterData.useless"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label :for="USELESS" class="flex items-center">
                                    <span
                                        class="bg-gray-100 text-gray-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full"
                                    >
                                        <TrashIcon class="h-4 w-4 inline mr-1" />
                                        {{ $t("homePage.modals.filterModal.useless") }}
                                    </span>
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Read Status -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">
                            {{ $t("homePage.modals.filterModal.readStatus") }}
                        </h3>
                        <div class="flex items-center space-x-2">
                            <input
                                type="checkbox"
                                id="read"
                                v-model="filterData.read"
                                class="rounded text-gray-600 focus:ring-gray-500"
                            />
                            <label
                                for="read"
                                class="flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1.5"
                                    stroke="currentColor"
                                    class="h-4 w-4 mr-1"
                                >
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                                </svg>
                                {{ $t("homePage.modals.filterModal.read") }}
                            </label>
                        </div>
                    </div>

                    <!-- Flags -->
                    <div>
                        <h3 class="text-sm font-medium leading-6 text-gray-900 mb-2">
                            {{ $t("homePage.modals.filterModal.flags") }}
                        </h3>
                        <div class="grid grid-cols-2 gap-2">
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="notification"
                                    v-model="filterData.notification"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="notification" class="flex items-center">
                                    <span
                                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10"
                                    >
                                        {{ $t("homePage.modals.filterModal.notification") }}
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="newsletter"
                                    v-model="filterData.newsletter"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="newsletter" class="flex items-center">
                                    <span
                                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10"
                                    >
                                        {{ $t("homePage.modals.filterModal.newsletter") }}
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="meeting"
                                    v-model="filterData.meeting"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="meeting" class="flex items-center">
                                    <span
                                        class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10"
                                    >
                                        {{ $t("homePage.modals.filterModal.meeting") }}
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="spam"
                                    v-model="filterData.spam"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="spam" class="flex items-center">
                                    <span
                                        class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10"
                                    >
                                        {{ $t("homePage.modals.filterModal.spam") }}
                                    </span>
                                </label>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="scams"
                                    v-model="filterData.scam"
                                    class="rounded text-gray-600 focus:ring-gray-500"
                                />
                                <label for="scams" class="flex items-center">
                                    <span
                                        class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10"
                                    >
                                        {{ $t("homePage.modals.filterModal.scams") }}
                                    </span>
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Action buttons -->
                    <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
                        <button
                            type="button"
                            class="inline-flex w-full rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:w-auto"
                            @click="updateFilter"
                        >
                            {{ $t("constants.userActions.update") }}
                        </button>
                        <button
                            type="button"
                            class="mr-2 inline-flex w-full justify-center items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto"
                            @click="deleteFilter"
                        >
                            <TrashIcon class="h-5 w-5" />
                            {{ $t("constants.userActions.delete") }}
                        </button>
                    </div>
                </div>
            </div>
        </Modal>
    </transition>
</template>

<script setup lang="ts">
import { Ref, ref, watch, inject, onMounted, onUnmounted } from "vue";
import { i18n } from "@/global/preferences";
import { XMarkIcon, ExclamationCircleIcon, InformationCircleIcon, TrashIcon } from "@heroicons/vue/20/solid";
import { putData, deleteData } from "@/global/fetchData";
import { Filter, Email } from "@/global/types";
import { USELESS, INFORMATIVE, IMPORTANT } from "@/global/const";

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Enter") {
        event.preventDefault();
        updateFilter();
    } else if (event.key === "Escape") {
        event.preventDefault();
        closeModal();
    } else if (event.key === "Tab") {
        event.preventDefault();
        const filterNameElement = document.getElementById("updateFilterName") as HTMLInputElement;
        filterNameElement?.focus();
    }
};

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

onUnmounted(() => {
    document.removeEventListener("keydown", handleKeyDown);
});

const props = defineProps<{
    isOpen: boolean;
    filter: Filter | null;
}>();

const emit = defineEmits<{
    (e: "close"): void;
    (e: "update", filter: Filter): void;
    (e: "delete", filterId: string): void;
}>();

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const fetchEmailsData = inject("fetchEmailsData") as (categoryName: string) => Promise<void>;
const filters = inject("filters") as Ref<{ [categoryName: string]: Filter[] }>;
const selectedCategory = inject("selectedCategory") as Ref<string>;
const selectedFilter = inject("selectedFilter") as Ref<Filter | undefined>;
const activeFilters = inject("activeFilters") as Ref<{
    [category: string]: Filter | undefined;
}>;
const handleScroll = inject("handleScroll") as (() => void) | undefined;
const currentPage = inject("currentPage") as Ref<number>;
const emails = inject("emails") as Ref<Record<string, Record<string, Email[]>>>;
const allEmailIds = inject("allEmailIds") as Ref<string[]>;
const isLoading = inject("isLoading") as Ref<boolean>;

const errorMessage = ref("");
const filterData = ref<Filter>({
    name: "",
    important: false,
    informative: false,
    category: "",
    useless: false,
    read: false,
    notification: false,
    newsletter: false,
    spam: false,
    scam: false,
    meeting: false,
});

watch(
    () => props.filter,
    (newFilter) => {
        if (newFilter) {
            filterData.value = { ...newFilter };
        }
    },
    { immediate: true }
);

const closeModal = () => {
    emit("close");
    resetForm();
};

const updateFilter = async () => {
    if (!props.isOpen) {
        return;
    }

    if (!filterData.value.name.trim()) {
        errorMessage.value = i18n.global.t("homePage.modals.pleaseFillAllFields");
        return;
    }

    const categoryFilters = filters.value[selectedCategory.value] || [];
    const response = await putData(`update_filter/`, { ...filterData.value, filterName: props.filter?.name });

    if (response.success) {
        selectedFilter.value = { ...response.data };
        activeFilters.value[selectedCategory.value] = { ...response.data };

        localStorage.setItem("activeFilters", JSON.stringify(activeFilters.value));

        currentPage.value = 1;
        emails.value = {};
        allEmailIds.value = [];
        isLoading.value = false;

        const filterIndex = categoryFilters.findIndex((filter) => filter.name === props.filter?.name);
        if (filterIndex !== -1) {
            categoryFilters[filterIndex] = { ...response.data };
        } else {
            categoryFilters.push({ ...response.data });
        }

        await fetchEmailsData(selectedCategory.value);
        const container = document.querySelector(".custom-scrollbar");
        if (container) {
            container.scrollTop = 0;
            if (handleScroll) {
                container.removeEventListener("scroll", handleScroll);
                container.addEventListener("scroll", handleScroll);
            }
        }
        scroll?.();

        closeModal();
        displayPopup?.(
            "success",
            i18n.global.t("constants.popUpConstants.successMessages.success"),
            i18n.global.t("constants.popUpConstants.successMessages.updateFilterSuccess")
        );
    } else {
        errorMessage.value = response.error as string;
    }
};

const deleteFilter = async () => {
    if (!props.isOpen) {
        return;
    }

    const categoryFilters = filters.value[selectedCategory.value];
    if (!categoryFilters) {
        return;
    }

    const response = await deleteData(`delete_filter/`, {
        filterName: props.filter?.name,
        category: filterData.value.category,
    });

    if (response.success) {
        const allEmailsFilter: Filter = {
            id: 0,
            name: "All emails",
            important: true,
            informative: true,
            useless: true,
            read: true,
            notification: true,
            newsletter: true,
            spam: true,
            scam: true,
            meeting: true,
            category: filterData.value.category,
        };

        const filterIndex = categoryFilters.findIndex((filter) => filter.name === props.filter?.name);
        if (filterIndex !== -1) {
            categoryFilters.splice(filterIndex, 1);
        }

        const existingAllEmailsIndex = categoryFilters.findIndex((f) => f.id === 0);
        if (existingAllEmailsIndex !== -1) {
            categoryFilters.splice(existingAllEmailsIndex, 1);
        }
        categoryFilters.unshift(allEmailsFilter);

        selectedFilter.value = allEmailsFilter;
        activeFilters.value[selectedCategory.value] = allEmailsFilter;

        localStorage.setItem("activeFilters", JSON.stringify(activeFilters.value));

        currentPage.value = 1;
        emails.value = {};
        allEmailIds.value = [];
        isLoading.value = false;

        filters.value = { ...filters.value };

        await fetchEmailsData(selectedCategory.value);
        const container = document.querySelector(".custom-scrollbar");
        if (container) {
            container.scrollTop = 0;
            if (handleScroll) {
                container.addEventListener("scroll", handleScroll);
            }
        }
        scroll?.();

        closeModal();
        displayPopup?.(
            "success",
            i18n.global.t("constants.popUpConstants.successMessages.success"),
            i18n.global.t("constants.popUpConstants.successMessages.deleteFilterSuccess")
        );
    } else {
        errorMessage.value = response.error as string;
    }
};

const resetForm = () => {
    errorMessage.value = "";
};
</script>
