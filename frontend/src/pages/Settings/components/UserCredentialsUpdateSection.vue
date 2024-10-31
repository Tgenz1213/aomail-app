<template>
    <div class="flex-col w-full pt-6">
        <div class="relative w-full">
            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center">
                <span class="bg-white px-2 text-sm text-gray-500">
                    {{ $t("settingsPage.accountPage.changeMyUsernameOrMyPassword") }}
                </span>
            </div>
        </div>
        <div class="pt-6 pb-10">
            <div class="flex space-x-1 items-center">
                <EnvelopeIcon class="w-4 h-4" />
                <label class="block text-sm font-medium leading-6 text-gray-900">
                    {{ $t("constants.username") }}
                </label>
            </div>
            <div class="relative items-stretch mt-2">
                <input
                    id="usernameInput"
                    v-model="usernameInput"
                    type="text"
                    class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                />
            </div>
            <div class="pt-4">
                <div class="grid grid-cols-2 gap-6">
                    <div class="flex flex-col">
                        <div class="flex space-x-1 items-center">
                            <KeyIcon class="w-4 h-4" />
                            <label class="block text-sm font-medium leading-6 text-gray-900">
                                {{ $t("settingsPage.accountPage.newPassword") }}
                            </label>
                        </div>
                        <div class="relative items-stretch mt-2 flex">
                            <input
                                id="newPassword"
                                v-if="!showPassword"
                                type="password"
                                class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                v-model="newPassword"
                            />
                            <input
                                v-else
                                id="newPassword"
                                type="text"
                                class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                v-model="newPassword"
                            />
                            <div class="flex items-center">
                                <button
                                    @click="togglePasswordVisibility"
                                    class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300"
                                >
                                    <svg
                                        v-if="!showPassword"
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
                                            d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
                                        />
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                                        />
                                    </svg>
                                    <svg
                                        v-else
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
                                            d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
                                        />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="flex flex-col">
                        <div class="flex space-x-1 items-center">
                            <KeyIcon class="w-4 h-4" />
                            <label class="block text-sm font-medium leading-6 text-gray-900">
                                {{ $t("settingsPage.accountPage.confirmYourNewPassword") }}
                            </label>
                        </div>
                        <div class="relative items-stretch mt-2 flex">
                            <input
                                id="confirmPassword"
                                v-if="!showConfirmPassword"
                                type="password"
                                class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                v-model="confirmPassword"
                            />
                            <input
                                v-else
                                id="confirmPassword"
                                type="text"
                                class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                v-model="confirmPassword"
                            />
                            <button
                                @click="toggleConfirmPasswordVisibility"
                                class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300"
                            >
                                <svg
                                    v-if="!showConfirmPassword"
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
                                        d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
                                    />
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                                    />
                                </svg>
                                <svg
                                    v-else
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
                                        d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
                                    />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex justify-end pt-4">
                <button
                    @click="handleSubmit"
                    class="rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
                >
                    {{ $t("constants.userActions.modify") }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { getData, postData } from "@/global/fetchData";
import { inject, onMounted, onUnmounted, Ref, ref } from "vue";
import { i18n } from "@/global/preferences";
import { KeyIcon, EnvelopeIcon } from "@heroicons/vue/24/outline";

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const usernameInput = inject<Ref<string>>("usernameInput", ref(""));
const username = inject<Ref<string>>("username", ref(""));

const newPassword = ref("");
const confirmPassword = ref("");
const showPassword = ref(false);
const showConfirmPassword = ref(false);

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Tab") {
        event.preventDefault();

        const usernameInput = document.getElementById("usernameInput") as HTMLInputElement | null;
        const confirmPassword = document.getElementById("confirmPassword") as HTMLInputElement | null;
        const newPassword = document.getElementById("newPassword") as HTMLInputElement | null;

        if (document.activeElement === usernameInput) {
            newPassword?.focus();
        } else if (document.activeElement === newPassword) {
            confirmPassword?.focus();
        } else if (document.activeElement === confirmPassword) {
            usernameInput?.focus();
        }
    }
}

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

onUnmounted(() => {
    document.removeEventListener("keydown", handleKeyDown);
});

function togglePasswordVisibility(event: Event) {
    event.preventDefault();
    showPassword.value = !showPassword.value;
}

function toggleConfirmPasswordVisibility() {
    showConfirmPassword.value = !showConfirmPassword.value;
}

async function handleSubmit() {
    // Check if there are no updates to make
    if (username.value === usernameInput.value && !newPassword.value && !confirmPassword.value) {
        return;
    }

    // Variables to track whether an update occurs
    const usernameChanged = usernameInput.value !== username.value;
    const passwordChanged = newPassword.value !== "" || confirmPassword.value !== "";

    // Handle username updates
    if (usernameChanged) {
        const result = await getData(`check_username/`);

        if (!result.success) {
            displayPopup?.(
                "error",
                i18n.global.t("settingsPage.accountPage.failedToCheckUsernameValidity"),
                result.error as string
            );
            return;
        }

        if (result.data.available === false) {
            displayPopup?.(
                "error",
                i18n.global.t("settingsPage.accountPage.usernameAlreadyExists"),
                i18n.global.t("settingsPage.accountPage.pleaseChooseDifferentUsername")
            );
            return;
        }

        if (usernameInput.value.length > 150) {
            displayPopup?.(
                "error",
                i18n.global.t(
                    "settingsPage.preferencesPage.popUpConstants.errorMessages.usernameMustNotExceed150Characters"
                ),
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.chooseAShorterUsername")
            );
            return;
        }

        if (/\s/.test(usernameInput.value)) {
            displayPopup?.(
                "error",
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.usernameMustNotContainSpaces"),
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.chooseAUsernameWithoutSpaces")
            );
            return;
        }

        await updateUsername(usernameChanged, passwordChanged);
    }

    // Handle password updates
    if (passwordChanged) {
        if (newPassword.value.length < 8 || newPassword.value.length > 32) {
            displayPopup?.(
                "error",
                i18n.global.t(
                    "settingsPage.preferencesPage.popUpConstants.errorMessages.passwordMustBeBetween8And32Characters"
                ),
                i18n.global.t(
                    "settingsPage.preferencesPage.popUpConstants.errorMessages.chooseAPasswordWithTheAppropriateLength"
                )
            );
            return;
        }

        await updatePassword(usernameChanged, passwordChanged);
    }

    // If both updates were successful
    if (usernameChanged && passwordChanged) {
        displayPopup?.(
            "success",
            i18n.global.t("constants.popUpConstants.successMessages.success"),
            i18n.global.t("settingsPage.accountPage.credentialsUpdatedSuccess")
        );
    }
}

async function updatePassword(usernameChanged: boolean, passwordChanged: boolean) {
    const result = await postData(`user/preferences/update_password/`, { password: newPassword.value });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.accountPage.errorUpdatingPassword"),
            result.error as string
        );
        return;
    }

    if (passwordChanged && !usernameChanged) {
        displayPopup?.(
            "success",
            i18n.global.t("constants.popUpConstants.successMessages.success"),
            i18n.global.t("settingsPage.accountPage.passwordUpdatedSuccess")
        );
    }
}

async function updateUsername(usernameChanged: boolean, passwordChanged: boolean) {
    const result = await postData(`user/preferences/update_username/`, { username: usernameInput.value });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.accountPage.errorUpdatingUsername"),
            result.error as string
        );
        return;
    }

    if (usernameChanged && !passwordChanged) {
        displayPopup?.(
            "success",
            i18n.global.t("constants.popUpConstants.successMessages.success"),
            i18n.global.t("settingsPage.accountPage.usernameUpdatedSuccess")
        );
    }
    username.value = usernameInput.value;
}
</script>
