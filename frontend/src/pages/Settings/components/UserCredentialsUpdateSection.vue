<template>
    <div class="flex-col w-full pt-6">
        <div class="relative w-full">
            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center">
                <span class="bg-gray-100/70 px-4 py-1 text-md text-gray-600 rounded-full backdrop-blur-sm">
                    {{ $t("settingsPage.accountPage.changeMyUsernameOrMyPassword") }}
                </span>
            </div>
        </div>
        <div class="pt-8 pb-10">
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
                                    <svg class="w-6 h-6" stroke="currentColor">
                                        <use :href="eyeIcon + '#' + (showPassword ? 'eye-hidden' : 'eye-visible')" />
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
                                <svg class="w-6 h-6" stroke="currentColor">
                                    <use :href="eyeIcon + '#' + (showConfirmPassword ? 'eye-hidden' : 'eye-visible')" />
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
import { PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH } from "@/global/const";
import eyeIcon from "@/assets/eye-icon.svg";

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const usernameInput = inject<Ref<string>>("usernameInput", ref(""));
const username = inject<Ref<string>>("username", ref(""));

const newPassword = ref("");
const confirmPassword = ref("");
const showPassword = ref(false);
const showConfirmPassword = ref(false);

function handleKeyDown(event: KeyboardEvent) {
    const usernameInput = document.getElementById("usernameInput") as HTMLInputElement | null;
    const confirmPassword = document.getElementById("confirmPassword") as HTMLInputElement | null;
    const newPassword = document.getElementById("newPassword") as HTMLInputElement | null;

    if (
        event.key === "Tab" &&
        (document.activeElement === usernameInput ||
            document.activeElement === newPassword ||
            document.activeElement === confirmPassword)
    ) {
        event.preventDefault();

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
        if (newPassword.value.length < PASSWORD_MIN_LENGTH || newPassword.value.length > PASSWORD_MAX_LENGTH) {
            displayPopup?.(
                "error",
                i18n.global.t("settingsPage.preferencesPage.popUpConstants.errorMessages.passwordLengthError"),
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
