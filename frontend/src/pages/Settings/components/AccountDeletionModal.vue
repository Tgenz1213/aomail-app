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
                            {{ $t("settingsPage.accountPage.deleteAccount") }}
                        </p>
                    </div>
                </div>
                <div class="flex flex-col gap-4 px-8 py-6">
                    <div>
                        <label class="block text-sm font-medium leading-6 text-gray-900">
                            {{ $t("settingsPage.accountPage.confirmDeleteAccount") }}
                        </label>
                    </div>
                    <div class="mt-2 sm:mt-2 sm:flex sm:flex-row justify-between">
                        <button
                            type="button"
                            class="ml-auto rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                            @click="closeModal"
                        >
                            {{ $t("constants.userActions.cancel") }}
                        </button>
                        <div class="flex-grow"></div>
                        <button
                            type="button"
                            class="inline-flex w-full justify-center items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto"
                            @click="deleteAccount"
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
                            {{ $t("settingsPage.accountPage.deleteAccount") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script lang="ts" setup>
import { i18n } from "@/global/preferences";
import router from "@/router/router";
import { inject } from "vue";
import { deleteData } from "@/global/fetchData";

defineProps<{
    isOpen: boolean;
}>();

const emit = defineEmits<{
    (e: "closeModal"): void;
}>();

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const closeModal = () => {
    emit("closeModal");
};

async function deleteAccount() {
    const result = await deleteData("delete_account/");
    closeModal();

    if (!result.success) {
        displayPopup?.("error", i18n.global.t("settingsPage.accountPage.errorDeletingAccount"), result.error as string);
    }

    localStorage.clear();
    closeModal();
    displayPopup?.(
        "success",
        i18n.global.t("constants.redirectionInProgress"),
        i18n.global.t("settingsPage.accountPage.accountDeletedSuccess")
    );

    setTimeout(() => {
        router.push({ name: "login" });
    }, 4000);
}
</script>
