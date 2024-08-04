<template>
    <div v-if="props.isOpen">
        <transition name="modal-fade">
            <div
                @click.self="closeModal"
                class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            >
                <div class="bg-white rounded-lg relative w-[450px]">
                    <slot></slot>
                    <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
                        <button
                            @click="closeModal"
                            @keydown="handleKeyDown"
                            type="button"
                            class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                        >
                            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                        </button>
                    </div>
                    <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
                        <div class="ml-8 flex items-center space-x-1">
                            <p
                                class="block leading-6 text-gray-900"
                                style="font-family: 'Poppins', sans-serif; font-weight: 500"
                            >
                                {{ $t("constants.categoryModalConstants.modifyTheCategory") }}
                            </p>
                        </div>
                    </div>
                    <div class="flex flex-col gap-4 px-8 py-6">
                        <p class="text-red-500" v-if="errorMessage">{{ errorMessage }}</p>
                        <div>
                            <label for="categoryName" class="block text-sm font-medium leading-6 text-gray-900">
                                {{ $t("constants.categoryModalConstants.categoryName") }}
                            </label>
                            <div class="mt-2">
                                <input
                                    id="categoryName"
                                    v-model="categoryName"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"
                                    :placeholder="$t('constants.categoryModalConstants.administrative')"
                                />
                            </div>
                        </div>
                        <div>
                            <label for="categoryDescription" class="block text-sm font-medium leading-6 text-gray-900">
                                {{ $t("constants.categoryModalConstants.categoryDescription") }}
                            </label>
                            <div class="mt-2">
                                <textarea
                                    id="categoryDescription"
                                    v-model="categoryDescription"
                                    rows="3"
                                    style="min-height: 60px"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"
                                ></textarea>
                            </div>
                            <p class="mt-3 text-sm leading-6 text-gray-600">
                                {{ $t("constants.categoryModalConstants.categoryDescriptionExplanation") }}
                            </p>
                        </div>
                        <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
                            <button
                                type="button"
                                class="ml-auto rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                                @click="updateCategory"
                            >
                                {{ $t("constants.userActions.update") }}
                            </button>
                            <button
                                type="button"
                                class="inline-flex w-full justify-center items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto"
                                @click="deleteCategory"
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
                                {{ $t("constants.userActions.delete") }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted } from "vue"
import { useI18n } from "vue-i18n"
import XMarkIcon from "@heroicons/vue/20/solid"
import { API_BASE_URL } from "@/global/const"
import { fetchWithToken } from "@/global/security"
import { Category } from "@/global/types"

interface Props {
    isOpen: boolean
    category: Category
}

const props = defineProps<Props>()

const emit = defineEmits<{
    (event: "closeModal"): void
    (event: "updateCategory", payload: Category): void
    (event: "deleteCategory", payload: string): void
}>()

const { t } = useI18n()

const categoryName = ref(props.category.name || "")
const categoryDescription = ref(props.category.description || "")
const errorMessage = ref("")

watch(
    () => props.category,
    (newVal) => {
        categoryName.value = newVal.name || ""
        categoryDescription.value = newVal.description || ""
    },
    { immediate: true }
)

const closeModal = () => {
    errorMessage.value = ""
    emit("closeModal")
}

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown)
})

async function updateCategory() {
    errorMessage.value = ""

    const updatedCategory: Category = {
        name: categoryName.value,
        description: categoryDescription.value,
    }

    if (categoryDescription.value.length > 300) {
        errorMessage.value = t("homePage.modals.newCategoryModal.maxDescriptionCharacters")
    } else if (categoryName.value.length > 50) {
        errorMessage.value = t("homePage.modals.newCategoryModal.maxNameCharacters")
    } else if (!categoryName.value.trim() || !categoryDescription.value.trim()) {
        errorMessage.value = t("homePage.modals.pleaseFillAllFields")
    } else {
        try {
            const response = await fetchWithToken(`${API_BASE_URL}user/categories/`)

            if (!response) {
                errorMessage.value = "Failed to create category"
                return
            }

            if (!response.ok) {
                errorMessage.value = "Network error"
                return
            }

            const fetchedCategories: Category[] = await response.json()
            const currentName = props.category.name

            if (fetchedCategories.some((cat) => cat.name === categoryName.value && cat.name !== currentName)) {
                errorMessage.value = `${t("homePage.modals.newCategoryModal.theCategoryExists")}${
                    categoryName.value
                }${t("homePage.modals.newCategoryModal.alreadyExists")}`
                categoryName.value = props.category.name || ""
                return
            }

            emit("updateCategory", updatedCategory)
        } catch (error) {
            emit("updateCategory", {
                name: "",
                description: t("homePage.modals.newCategoryModal.errorCheckingExistingCategories"),
            } as Category)
            categoryName.value = props.category.name || ""
        }
    }
}

function deleteCategory() {
    emit("deleteCategory", categoryName.value)
}

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Escape") {
        closeModal()
    } else if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault()
        updateCategory()
    } else if (event.key === "Delete") {
        if (document.activeElement?.id !== "categoryName" && document.activeElement?.id !== "categoryDescription") {
            deleteCategory()
        }
    } else if (event.key === "Tab" && props.isOpen) {
        event.preventDefault()
        if (categoryName.value === "" && document.activeElement?.id !== "categoryName") {
            ;(document.getElementById("categoryName") as HTMLElement)?.focus()
        } else if (categoryDescription.value === "" && document.activeElement?.id !== "categoryDescription") {
            ;(document.getElementById("categoryDescription") as HTMLElement)?.focus()
        } else if (document.activeElement?.id === "categoryName") {
            ;(document.getElementById("categoryDescription") as HTMLElement)?.focus()
        } else {
            ;(document.getElementById("categoryName") as HTMLElement)?.focus()
        }
    }
}
</script>
