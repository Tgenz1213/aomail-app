<template>
    <transition name="modal-fade">
        <div
            @click.self="closeModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            v-if="isModalOpen"
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
                            {{ $ i18n.global.t("settingsPage.accountPage.updateMyDescription") }}
                        </p>
                    </div>
                </div>
                <div class="flex flex-col gap-4 px-8 py-6">
                    <div>
                        <div class="flex space-x-1 items-center">
                            <envelope-icon class="w-4 h-4" />
                            <label class="block text-sm font-medium leading-6 text-gray-900">{{ emailSelected }}</label>
                        </div>
                        <div class="relative items-stretch mt-2 pb-6">
                            <input
                                v-model="userDescription"
                                type="text"
                                placeholder="Résumez-vous pour aider l'assistant"
                                class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                            />
                        </div>
                    </div>
                    <div class="mt-2 sm:mt-2 sm:flex sm:flex-row">
                        <button
                            type="button"
                            class="ml-auto rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                            @click="updateUserDescription"
                        >
                            {{ $ i18n.global.t("constants.userActions.update") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script lang="ts" setup>
import { ref, defineProps, defineEmits } from "vue";
import { i18n } from "@/global/Settings/preferences";
import { postData } from "@/global/fetchData";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";

const props = defineProps({
    emailSelected: {
        type: String,
        required: true,
    },
    isModalOpen: {
        type: Boolean,
        required: true,
    },
});

const emits = defineEmits(["close-modal"]);

const userDescription = ref("");
const showNotification = ref<boolean>(false);
const notificationTitle = ref<string>("");
const notificationMessage = ref<string>("");
const backgroundColor = ref<string>("");
const timerId = ref<number | null>(null);

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

function closeModal() {
    emits("close-modal");
}

async function updateUserDescription() {
    const result = await postData("user/social_api/update_user_description/", {
        email: props.emailSelected,
        user_description: userDescription.value.trim() ? userDescription.value.trim() : "",
    });

    if (result.success) {
        displayPopup(
            "success",
            i18n.global.t("constants.popUpConstants.successMessages.success"),
            i18n.global.t("settingsPage.accountPage.emailDescriptionUpdated")
        );
    } else {
        displayPopup(
            "error",
            i18n.global.t("settingsPage.accountPage.errorUpdatingDescription"),
            result.error as string
        );
    }
    closeModal();
}
</script>


<!-- todo:
rename variables to be local => closeUnlinkModal => closeModal & isUnlinkModalOpen => isModalOpen 
copy functions to ensure functionnality
fix issues with TS
add a script setup -->
