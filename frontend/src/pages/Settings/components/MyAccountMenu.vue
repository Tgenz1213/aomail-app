<template>
    <AddUserDescriptionModal :isOpen="isAddUserDescriptionModalOpen" @closeModal="closeAddUserDescriptionModal" />
    <AccountDeletionModal :isOpen="isAccountDeletionModalOpen" @closeModal="closeAccountDeletionModal" />
    <TroubleshootingMenuModal :isOpen="isTroubleshootingMenuModalOpen" @closeModal="closeTroubleshootingMenu" />
    <ImapSmtpModal :isOpen="isImapSmtpModalOpen" @closeModal="closeImapSmtpModal" />
    <div class="flex-1 h-full">
        <div class="h-full w-full flex items-center justify-center">
            <div class="flex gap-x-10 h-full w-full py-10 px-8 2xl:py-14 2xl:px-12">
                <div class="flex-1 flex-col h-full flex-grow px-4">
                    <UserCredentialsUpdateSection />
                    <div class="flex-col flex-grow w-full py-12 2xl:py-20">
                        <div class="relative w-full">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t border-gray-300"></div>
                            </div>
                            <div class="relative flex justify-center">
                                <span
                                    class="bg-gray-100/70 px-4 py-1 text-md text-gray-600 rounded-full backdrop-blur-sm"
                                >
                                    {{ $t("constants.userActions.delete") }}
                                </span>
                            </div>
                        </div>
                        <div class="pt-8">
                            <div class="flex space-x-1 items-center justify-between">
                                <div class="flex items-center gap-2">
                                    <input
                                        type="checkbox"
                                        class="form-radio text-red-600 border-red-400 focus:border-red-500 focus:ring-red-200 h-5 w-5"
                                        v-model="isDeleteRadioButtonChecked"
                                    />
                                    <label for="push-everything" class="block text-sm font-medium leading-6">
                                        {{ $t("settingsPage.accountPage.confirmDeleteAccount") }}
                                    </label>
                                </div>
                                <button
                                    @click="openAccountDeletionModal"
                                    type="submit"
                                    class="inline-flex w-full justify-cente items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto"
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
                <div class="flex-1 flex-col h-full flex-grow px-4 py-6">
                    <div class="relative w-full">
                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                            <div class="w-full border-t border-gray-300"></div>
                        </div>
                        <div class="relative flex justify-center">
                            <span class="bg-gray-100/70 px-4 py-1 text-md text-gray-600 rounded-full backdrop-blur-sm">
                                {{ $t("settingsPage.accountPage.linkANewEmailAddress") }}
                            </span>
                        </div>
                    </div>
                    <div class="pt-[60px]">
                        <div class="overflow-y-auto w-full">
                            <div class="max-h-20 sm:max-h-24 md:max-h-32 lg:max-h-40 w-full">
                                <ul role="list" class="space-y-1 w-full">
                                    <li
                                        v-for="email in emailsLinked"
                                        :key="email?.email"
                                        class="border border-black w-full overflow-hidden font-semibold rounded-md bg-gray-10 px-6 py-0 shadow hover:shadow-md text-gray-700 relative"
                                    >
                                        <UserEmailLinked :email="email" />
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <!--<div class="relative w-full py-4">
                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                            <div class="w-full border-t border-gray-300"></div>
                        </div>
                        <div class="relative flex justify-center">
                            <span class="bg-gray-100/70 px-4 py-1 text-md text-gray-600 rounded-full backdrop-blur-sm">
                                {{ $t("settingsPage.accountPage.chooseTheEmailServiceProvider") }}
                            </span>
                        </div>
                    </div>-->
                    <div class="flex gap-x-4 justify-center">
                        <div class="pt-4">
                            <div class="relative items-stretch mt-2 flex justify-center items-center">
                                <button
                                    type="button"
                                    class="relative group inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                    @click="authorize(MICROSOFT)"
                                >
                                    <img src="@/assets/logos/microsoft.svg" alt="Microsoft" class="w-5 h-5" />
                                    <span
                                        class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden w-max px-2 py-1 text-xs text-white bg-black rounded-md group-hover:block"
                                    >
                                        {{ $t("settingsPage.accountPage.securelyLinkOutlookAccount") }}
                                    </span>
                                </button>
                            </div>
                        </div>
                        <div class="py-4">
                            <div class="relative items-stretch mt-2 flex justify-center items-center">
                                <button
                                    type="button"
                                    class="relative group inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                    @click="authorize(GOOGLE)"
                                >
                                    <img src="@/assets/logos/google.svg" alt="Google" class="w-5 h-5" />
                                    <span
                                        class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden w-max px-2 py-1 text-xs text-white bg-black rounded-md group-hover:block"
                                    >
                                        {{ $t("settingsPage.accountPage.securelyLinkGmailAccount") }}
                                    </span>
                                </button>
                            </div>
                        </div>
                        <div class="py-4">
                            <div class="relative items-stretch mt-2 flex justify-center items-center">
                                <button
                                    type="button"
                                    class="relative group inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                    @click="openImapSmtpModal"
                                >
                                    <InboxIcon class="w-5 h-5" />
                                    <span
                                        class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden w-max px-2 py-1 text-xs text-white bg-black rounded-md group-hover:block"
                                    >
                                        Any IMAP & SMTP provider
                                    </span>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="flex-col flex-grow w-full pt-[168px] 2xl:pt-44">
                        <div class="relative w-full">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t border-gray-300"></div>
                            </div>
                            <div class="relative flex justify-center">
                                <span
                                    class="bg-gray-100/70 px-4 py-1 text-md text-gray-600 rounded-full backdrop-blur-sm"
                                >
                                    {{ $t("settingsPage.accountPage.troubleshooting") }}
                                </span>
                            </div>
                        </div>
                        <div class="pt-8 flex flex-col items-center space-y-4">
                            <button
                                @click="openTroubleshootingMenu"
                                class="rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:ring-gray-800"
                            >
                                {{ $t("settingsPage.accountPage.noLongerReceivingEmails") }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { InboxIcon } from "@heroicons/vue/24/outline";
import { ref, onMounted, provide, inject, Ref } from "vue";
import { getData, postData } from "@/global/fetchData";
import { GOOGLE, MICROSOFT } from "@/global/const";
import AddUserDescriptionModal from "./AddUserDescriptionModal.vue";
import AccountDeletionModal from "./AccountDeletionModal.vue";
import UserEmailLinked from "./UserEmailLinked.vue";
import UserCredentialsUpdateSection from "./UserCredentialsUpdateSection.vue";
import TroubleshootingMenuModal from "./TroubleshootingMenuModal.vue";
import ImapSmtpModal from "@/global/components/ImapSmtpModal.vue";
import { i18n } from "@/global/preferences";
import { EmailLinked } from "@/global/types";
import { Plan } from "../utils/types";

const usernameInput = ref("");
const username = ref("");

const typeApi = ref("");
const userPlan = inject<Ref<Plan>>("userPlan");
const isDeleteRadioButtonChecked = inject<Ref<boolean>>("isDeleteRadioButtonChecked", ref(false));
const isAddUserDescriptionModalOpen = inject<Ref<boolean>>("isAddUserDescriptionModalOpen", ref(false));
const isTroubleshootingMenuModalOpen = inject<Ref<boolean>>("isTroubleshootingMenuModalOpen", ref(false));
const isAccountDeletionModalOpen = inject<Ref<boolean>>("isAccountDeletionModalOpen", ref(false));
const emailsLinked = inject<Ref<EmailLinked[]>>("emailsLinked", ref([]));
const isImapSmtpModalOpen = ref(false);

provide("typeApi", typeApi);
provide("usernameInput", usernameInput);
provide("username", username);
provide("fetchEmailLinked", fetchEmailLinked);

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const closeAddUserDescriptionModal = inject<() => void>("closeAddUserDescriptionModal");
const closeAccountDeletionModal = inject<() => void>("closeAccountDeletionModal");
const openAddUserDescriptionModal = inject<() => void>("openAddUserDescriptionModal");
const openAccountDeletionModal = inject<() => void>("openAccountDeletionModal");
const openTroubleshootingMenu = inject<() => void>("openTroubleshootingMenu");
const closeTroubleshootingMenu = inject<() => void>("closeTroubleshootingMenu");

onMounted(() => {
    checkAuthorizationCode();
    fetchEmailLinked();
    fetchUsername();
});

function authorize(provider: string) {
    if (userPlan?.value) {
        if (userPlan.value.isTrial) {
            displayPopup?.(
                "error",
                i18n.global.t("settingsPage.accountPage.failedToGenerateAuthURL"),
                i18n.global.t("settingsPage.accountPage.singleEmailTrialLinkLimit")
            );
            return;
        }

        if (!userPlan.value.isActive) {
            displayPopup?.(
                "error",
                i18n.global.t("settingsPage.accountPage.failedToGenerateAuthURL"),
                i18n.global.t("settingsPage.accountPage.inactiveSubscriptionLinkError")
            );
            return;
        }
    }

    typeApi.value = provider;

    if (provider === MICROSOFT || provider === GOOGLE) {
        openAddUserDescriptionModal?.();
    }

    return;
}

function checkAuthorizationCode() {
    const regrantConsent = sessionStorage.getItem("regrantConsent");
    const urlParams = new URLSearchParams(window.location.search);
    const authorizationCode = urlParams.get("code");

    if (authorizationCode) {
        if (regrantConsent === "true") {
            linkEmail(authorizationCode, true);
        } else {
            linkEmail(authorizationCode);
        }
    }
}

async function linkEmail(authorizationCode: string, regrantConsent?: boolean) {
    const result = await postData("user/social_api/link/", {
        code: authorizationCode,
        typeApi: sessionStorage.getItem("typeApi"),
        userDescription: sessionStorage.getItem("userDescription"),
    });

    if (!result.success) {
        displayPopup?.("error", i18n.global.t("settingsPage.accountPage.emailLinkingFailure"), result.error as string);
    } else {
        await fetchEmailLinked();

        if (regrantConsent) {
            displayPopup?.(
                "success",
                i18n.global.t("constants.popUpConstants.successMessages.success"),
                i18n.global.t("settingsPage.accountPage.connectionReestablishedSuccess")
            );
        } else {
            displayPopup?.(
                "success",
                i18n.global.t("constants.popUpConstants.successMessages.success"),
                i18n.global.t("settingsPage.accountPage.emailLinkedSuccess")
            );
        }
    }

    sessionStorage.clear();
    const modifiedUrl = window.location.origin + window.location.pathname;
    window.history.replaceState({}, document.title, modifiedUrl);
}

async function fetchEmailLinked() {
    const result = await getData("user/emails_linked/");
    if (!result) return;

    emailsLinked.value = result.data;
}

async function fetchUsername() {
    const result = await getData(`user/preferences/username/`);

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.accountPage.failedToFetchUsername"),
            result.error as string
        );
        return;
    }

    usernameInput.value = result.data.username;
    username.value = result.data.username;
}

const openImapSmtpModal = () => {
    isImapSmtpModalOpen.value = true;
};

const closeImapSmtpModal = () => {
    isImapSmtpModalOpen.value = false;
};
</script>
