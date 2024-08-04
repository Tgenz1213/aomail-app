<template>
    <div v-if="props.isOpen">
        <transition name="modal-fade">
            <div
                @click.self="closeModal"
                class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
                v-if="props.isOpen"
            >
                <div class="bg-white rounded-lg relative w-[450px]">
                    <slot></slot>
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
                            <p
                                class="block leading-6 text-gray-900"
                                style="font-family: 'Poppins', sans-serif; font-weight: 500"
                            >
                                {{ $t("constants.categoryModalConstants.addCategory") }}
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
                                class="inline-flex w-full rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:w-auto"
                                @click="addCategory"
                            >
                                {{ $t("constants.userActions.create") }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineProps, defineEmits } from "vue"
import { useI18n } from "vue-i18n"
import XMarkIcon from "@heroicons/vue/20/solid"
import { API_BASE_URL } from "@/global/const"
import { fetchWithToken } from "@/global/security"
import { Category } from "@/global/types"

interface Props {
    isOpen: boolean
    errorMessage?: string
}

interface Emits {
    (event: "closeModal"): void
    (event: "addCategory", payload: Category | { error: string; description: any }): void
}

const props = defineProps<Props>()
const emits = defineEmits<Emits>()

const { t } = useI18n()

const categoryName = ref("")
const categoryDescription = ref("")
const errorMessage = ref("")

const closeModal = () => {
    errorMessage.value = ""
    emits("closeModal")
}

const addCategory = async () => {
    errorMessage.value = ""

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

            if (fetchedCategories.some((cat: Category) => cat.name === categoryName.value)) {
                errorMessage.value = `${t("homePage.modals.newCategoryModal.theCategoryExists")}${
                    categoryName.value
                }${t("homePage.modals.newCategoryModal.alreadyExists")}`
                return
            }

            emits("addCategory", { name: categoryName.value, description: categoryDescription.value })
            categoryDescription.value = ""
            categoryName.value = ""
        } catch (error) {
            emits("addCategory", {
                error: t("homePage.modals.newCategoryModal.errorCheckingExistingCategories"),
                description: error,
            })
            categoryDescription.value = ""
            categoryName.value = ""
        }
    }
}

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Escape") {
        closeModal()
    } else if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault()
        addCategory()
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

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown)
})
</script>
