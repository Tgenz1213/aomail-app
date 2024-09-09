<template>
    <transition name="modal-fade">
        <div
            @click.self="closeModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            v-if="isOpen"
        >
            <div class="bg-white rounded-lg relative w-[450px]">
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
                        <p class="block font-semibold leading-6 text-gray-900">
                            {{ $t("constants.categoryModalConstants.addCategory") }}
                        </p>
                    </div>
                </div>
                <div class="flex flex-col gap-4 px-8 py-6">
                    <p class="text-red-500" v-if="errorMessage">{{ errorMessage }}</p>
                    <div>
                        <label for="email" class="block text-sm font-medium leading-6 text-gray-900">
                            {{ $t("constants.categoryModalConstants.categoryName") }}
                        </label>
                        <div class="mt-2">
                            <input
                                v-model="categoryName"
                                id="categoryName"
                                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"
                                :placeholder="$t('constants.categoryModalConstants.administrative')"
                            />
                        </div>
                    </div>
                    <div>
                        <label for="about" class="block text-sm font-medium leading-6 text-gray-900">
                            {{ $t("constants.categoryModalConstants.categoryDescription") }}
                        </label>
                        <div class="mt-2">
                            <textarea
                                v-model="categoryDescription"
                                id="categoryDescription"
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
                            class="inline-flex w-full justify-center rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:ml-3 sm:w-auto"
                            @click="addCategory"
                        >
                            {{ $t("constants.userActions.create") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { XMarkIcon } from "@heroicons/vue/24/outline";
import { inject, Ref, ref } from "vue";

const categoryName = inject<Ref<string>>("categoryName") || ref("");
const categoryDescription = inject<Ref<string>>("categoryDescription") || ref("");

defineProps<{
    isOpen: boolean;
    errorMessage: string;
}>();

const emits = defineEmits(["closeModal", "addCategory"]);

const closeModal = () => {
    emits("closeModal");
};

const addCategory = () => {
    emits("addCategory");
};
</script>
