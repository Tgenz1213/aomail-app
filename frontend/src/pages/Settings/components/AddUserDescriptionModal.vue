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
                            {{ $t("settingsPage.accountPage.linkANewEmailAddress") }}
                        </p>
                    </div>
                </div>
                <div class="flex flex-col gap-4 px-8 py-6">
                    <div>
                        <div class="flex space-x-1 items-center">
                            <envelope-icon class="w-4 h-4" />
                            <label class="block text-sm font-medium leading-6 text-gray-900">
                                {{ $t("settingsPage.accountPage.optionalDescription") }}
                            </label>
                        </div>
                        <div class="relative items-stretch mt-2 pb-6">
                            <input
                                v-model="userDescription"
                                type="text"
                                :placeholder="$t('signUpPart1Page.summaryUserPlaceholder')"
                                class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                            />
                        </div>
                    </div>
                    <div class="mt-2 sm:mt-2 sm:flex sm:flex-row">
                        <button
                            type="button"
                            class="ml-auto rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                            @click="linkNewEmail"
                        >
                            {{ $t("settingsPage.accountPage.link") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { getData } from "@/global/fetchData";
import { inject, Ref, ref, onMounted } from "vue";

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const typeApi = inject<Ref<string>>("typeApi", ref(""));
const userDescription = ref("");
const props = defineProps<{
    isOpen: boolean;
}>();

const emit = defineEmits<{
    (e: "closeModal"): void;
}>();

const closeModal = () => {
    emit("closeModal");
};

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Enter") {
        if (props.isOpen) {
            linkNewEmail();
        }
    }
}

async function linkNewEmail() {
    saveVariables();

    const currentTypeApi = sessionStorage.getItem("typeApi");

    if (currentTypeApi === "google") {
        const result = await getData("google/auth_url_link_email/");

        if (!result.success) {
            displayPopup?.("error", "Failed to generate authorization link", result.error as string);
            closeModal();
        } else {
            if ("caches" in window) {
                caches.keys().then((keyList) => Promise.all(keyList.map((key) => caches.delete(key))));
            }
            window.location.replace(result.data.authorizationUrl);
        }
    } else if (currentTypeApi === "microsoft") {
        const result = await getData("microsoft/auth_url_link_email/");

        if (!result.success) {
            displayPopup?.("error", "Failed to generate authorization link", result.error as string);
            closeModal();
        } else {
            window.location.replace(result.data.authorizationUrl);
        }
    }
}

function saveVariables() {
    sessionStorage.setItem("typeApi", typeApi?.value || "");
    sessionStorage.setItem("userDescription", userDescription.value);
}
</script>
