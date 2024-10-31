<template>
    <NewCategoryModal
        :isOpen="isModalNewCategoryOpen"
        :errorMessage="errorMessageNewCategoryModal"
        :categoryName="categoryName"
        :categoryDescription="categoryDescription"
        @closeModal="closeNewCategoryModal"
        @addCategory="addCategory"
    />
    <UpdateCategoryModal
        :isOpen="isModalUpdateCategoryOpen"
        :errorMessage="errorMessageUpdateCategoryModal"
        :category="categoryToUpdate"
        :categoryName="updateCategoryName"
        :categoryDescription="updateCategoryDescription"
        @closeModal="closeUpdateCategoryModal"
        @updateCategory="updateCategory"
        @deleteCategoryOnUpdate="deleteCategoryOnUpdate"
    />
    <div class="flex flex-col">
        <div class="relative">
            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center">
                <span class="bg-white px-2 text-sm text-gray-500">
                    {{ $t("constants.category") }}
                </span>
            </div>
        </div>
        <div class="pt-2">
            <div class="relative items-stretch mt-2">
                <div class="flex flex-col gap-y-4">
                    <p>{{ $t("signUpPart1Page.createCategory") }}</p>
                    <div v-if="categories.length === 0">
                        <button
                            @click="openNewCategoryModal"
                            type="button"
                            class="relative block w-full rounded-lg border-2 border-dashed border-gray-300 p-12 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                        >
                            <svg
                                class="mx-auto h-12 w-12 text-gray-400"
                                stroke="currentColor"
                                fill="none"
                                viewBox="0 0 48 48"
                                aria-hidden="true"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M8 14v20c0 4.418 7.163 8 16 8 1.381 0 2.721-.087 4-.252M8 14c0 4.418 7.163 8 16 8s16-3.582 16-8M8 14c0-4.418 7.163-8 16-8s16 3.582 16 8m0 0v14m0-4c0 4.418-7.163 8-16 8S8 28.418 8 24m32 10v6m0 0v6m0-6h6m-6 0h-6"
                                />
                            </svg>
                            <span class="mt-2 block text-sm font-semibold text-gray-900">
                                {{ $t("constants.categoryModalConstants.addCategory") }}
                            </span>
                        </button>
                    </div>
                    <div v-else class="max-h-64 overflow-y-auto flex flex-col gap-y-4">
                        <ul role="list" class="space-y-3">
                            <li
                                v-for="category in categories"
                                :key="category.name"
                                class="flex items-center justify-between overflow-hidden font-semibold rounded-md bg-gray-50 px-6 py-4 shadow hover:shadow-md text-gray-700 relative"
                            >
                                <span>{{ category.name }}</span>
                                <div class="flex gap-1">
                                    <button
                                        type="button"
                                        class="inline-flex justify-center items-center gap-x-1 rounded-md px-3 py-2 text-sm font-semibold text-gray-800 hover:text-black"
                                        @click.stop="openUpdateCategoryModal(category)"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke-width="1.5"
                                            stroke="currentColor"
                                            class="w-6 h-6"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
                                            />
                                        </svg>
                                    </button>
                                    <button
                                        type="button"
                                        class="inline-flex justify-center items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700"
                                        @click="deleteCategory(category)"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke-width="1.5"
                                            stroke="currentColor"
                                            class="w-6 h-6"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                                            />
                                        </svg>
                                    </button>
                                </div>
                            </li>
                        </ul>
                        <button
                            @click="openNewCategoryModal"
                            type="button"
                            class="flex w-full justify-center rounded-md px-3 py-1.5 text-sm font-semibold border-2 border-dashed border-gray-300 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                        >
                            {{ $t("signUpPart1Page.addAnotherCategory") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div>
        <div class="pt-4">
            <button
                @click.prevent="goStepLinkEmail"
                class="flex w-full justify-center rounded-md bg-gray-800 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-gray-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800"
            >
                {{ $t("signUpPart1Page.continue") }}
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { i18n } from "@/global/preferences";
import { Category } from "@/global/types";
import { inject, onMounted, provide, Ref, ref } from "vue";
import NewCategoryModal from "./NewCategoryModal.vue";
import UpdateCategoryModal from "./UpdateCategoryModal.vue";

const categoryToUpdate = ref<Category | null>(null);
const categoryOpened = ref<Category | null>(null);
const categoryName = ref<string>("");
const categoryDescription = ref<string>("");
const errorMessageNewCategoryModal = ref<string>("");
const errorMessageUpdateCategoryModal = ref<string>("");
const updateCategoryName = ref<string>("");
const updateCategoryDescription = ref<string>("");
const categories = inject<Ref<Category[]>>("categories") || ref([]);
const isModalNewCategoryOpen = inject<Ref<boolean>>("isModalNewCategoryOpen") || ref(false);
const isModalUpdateCategoryOpen = inject<Ref<boolean>>("isModalUpdateCategoryOpen") || ref(false);

const goStepLinkEmail = inject<() => void>("goStepLinkEmail");

provide("categoryName", categoryName);
provide("categoryDescription", categoryDescription);
provide("updateCategoryName", updateCategoryName);
provide("updateCategoryDescription", updateCategoryDescription);

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

const openNewCategoryModal = () => {
    isModalNewCategoryOpen.value = true;
};

const closeNewCategoryModal = () => {
    isModalNewCategoryOpen.value = false;
    errorMessageNewCategoryModal.value = "";
};

const addCategory = () => {
    if (!categoryName.value.trim() || !categoryDescription.value.trim()) {
        errorMessageNewCategoryModal.value = i18n.global.t("homePage.modals.pleaseFillAllFields");
    } else if (categories.value.some((cat) => cat.name === categoryName.value)) {
        errorMessageNewCategoryModal.value = i18n.global.t("signUpPart1Page.categoryAlreadyExists");
    } else if (categoryDescription.value.length > 300) {
        errorMessageNewCategoryModal.value = i18n.global.t("homePage.modals.newCategoryModal.maxDescriptionCharacters");
    } else if (categoryName.value.length > 50) {
        errorMessageNewCategoryModal.value = i18n.global.t("homePage.modals.newCategoryModal.maxNameCharacters");
    } else {
        categories.value.push({
            name: categoryName.value,
            description: categoryDescription.value,
        });
        categoryName.value = "";
        categoryDescription.value = "";
        errorMessageNewCategoryModal.value = "";
        isModalNewCategoryOpen.value = false;
    }
};

const openUpdateCategoryModal = (category: Category) => {
    updateCategoryName.value = category.name;
    updateCategoryName.value = category.name;
    updateCategoryDescription.value = category.description;
    categoryOpened.value = category;
    isModalUpdateCategoryOpen.value = true;
};

const closeUpdateCategoryModal = () => {
    isModalUpdateCategoryOpen.value = false;
    errorMessageUpdateCategoryModal.value = "";
};

const updateCategory = () => {
    if (!updateCategoryName.value.trim() || !updateCategoryDescription.value.trim()) {
        errorMessageUpdateCategoryModal.value = i18n.global.t("homepage.modals.pleaseFillAllFields");
    } else if (
        categories.value.some((cat) => cat.name === updateCategoryName.value && cat.name != updateCategoryName.value)
    ) {
        errorMessageUpdateCategoryModal.value = i18n.global.t("signUpPart1Page.categoryAlreadyExists");
    } else if (updateCategoryDescription.value.length > 300) {
        errorMessageUpdateCategoryModal.value = i18n.global.t("homepage.modals.maxDescriptionCharacters");
    } else if (updateCategoryName.value.length > 50) {
        errorMessageUpdateCategoryModal.value = i18n.global.t("homepage.modals.maxNameCharacters");
    } else if (categoryOpened.value) {
        categoryOpened.value.name = updateCategoryName.value;
        categoryOpened.value.description = updateCategoryDescription.value;
        closeUpdateCategoryModal();
    }
};

const deleteCategory = (category: Category) => {
    const indexToRemove = categories.value.indexOf(category);
    if (indexToRemove !== -1) {
        categories.value.splice(indexToRemove, 1);
    }
};

const deleteCategoryOnUpdate = () => {
    if (categoryOpened.value) {
        const indexToRemove = categories.value.indexOf(categoryOpened.value);
        if (indexToRemove !== -1) {
            categories.value.splice(indexToRemove, 1);
        }
    }
    closeUpdateCategoryModal();
};

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Tab") {
        event.preventDefault();

        if (isModalNewCategoryOpen.value) {
            if (categoryName.value == "" && document.activeElement?.id != "categoryName") {
                document.getElementById("categoryName")?.focus();
            } else if (categoryDescription.value == "" && document.activeElement?.id != "categoryDescription") {
                document.getElementById("categoryDescription")?.focus();
            } else if (document.activeElement?.id === "categoryName") {
                document.getElementById("categoryDescription")?.focus();
            } else {
                document.getElementById("categoryName")?.focus();
            }
        } else if (isModalUpdateCategoryOpen.value) {
            if (updateCategoryName.value == "" && document.activeElement?.id != "updateCategoryName") {
                document.getElementById("updateCategoryName")?.focus();
            } else if (
                updateCategoryDescription.value == "" &&
                document.activeElement?.id != "updateCategoryDescription"
            ) {
                document.getElementById("updateCategoryDescription")?.focus();
            } else if (document.activeElement?.id === "updateCategoryName") {
                document.getElementById("updateCategoryDescription")?.focus();
            } else {
                document.getElementById("updateCategoryName")?.focus();
            }
        }
    } else if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        if (isModalNewCategoryOpen.value) {
            addCategory();
        } else if (isModalUpdateCategoryOpen.value) {
            updateCategory();
        }
    } else if (event.key === "Escape") {
        if (isModalUpdateCategoryOpen.value) {
            closeUpdateCategoryModal();
        } else if (isModalNewCategoryOpen.value) {
            closeNewCategoryModal();
        }
    }
}
</script>
