<template>
    <transition name="modal-fade">
        <div
            v-if="isOpen"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            @click.self="closeModal"
        >
            <div class="bg-white rounded-lg w-[450px] relative">
                <!-- Modal Header -->
                <div class="absolute right-0 top-0 p-4">
                    <button @click="closeModal" class="text-gray-400 hover:text-gray-500 focus:outline-none">
                        <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                    </button>
                </div>
                <div class="flex items-center h-16 bg-gray-50 rounded-t-lg ring-1 ring-black ring-opacity-5">
                    <h2 class="ml-8 font-semibold text-gray-900">
                        {{ $t("settingsPage.accountPage.troubleshooting") }}
                    </h2>
                </div>

                <!-- Loading Spinner -->
                <div v-if="isLoading" class="flex flex-col items-center p-4 space-y-2">
                    <svg
                        aria-hidden="true"
                        class="inline w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-gray-600 dark:fill-gray-300"
                        viewBox="0 0 100 101"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                            fill="currentColor"
                        />
                        <path
                            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                            fill="currentFill"
                        />
                    </svg>
                    <p class="text-sm text-gray-700">{{ loadingMessage }}</p>
                </div>

                <!-- Display Messages -->
                <div v-else class="p-4">
                    <p v-if="errorMessage" class="text-sm text-red-500">{{ errorMessage }}</p>
                    <p v-if="successMessage" class="text-sm text-green-500">{{ successMessage }}</p>
                    <p v-if="warningMessage" class="text-sm text-orange-500">{{ warningMessage }}</p>
                </div>

                <!-- Linked Emails List -->
                <div v-if="!isLoading" class="max-h-60 w-full overflow-y-auto p-4">
                    <ul role="list" class="space-y-2 w-full">
                        <li
                            v-for="email in emailsLinked"
                            :key="email?.email"
                            class="border border-gray-300 rounded-md bg-gray-100 flex items-center p-2 shadow hover:shadow-md"
                        >
                            <input type="radio" v-model="selectedEmail" :value="email" class="mr-2" />
                            <UserEmailLinked
                                :email="email"
                                :isRegrant="true"
                                class="flex-grow flex items-center justify-between"
                            />
                        </li>
                    </ul>
                </div>

                <div v-if="errorMessage" class="p-4">
                    <button @click="toggleAdvancedInfo" class="text-blue-600 hover:underline">
                        {{ $t("settingsPage.accountPage.troubleshootingModal.advancedExplanations") }}
                    </button>
                    <transition name="fade">
                        <div v-if="showAdvancedInfo" class="mt-2 p-2 border rounded-md bg-gray-100">
                            <p class="text-sm">
                                <span v-if="selectedEmail?.typeApi === GOOGLE">
                                    {{ $t("settingsPage.accountPage.troubleshootingModal.googleRefreshTokenInfo") }}
                                    <a
                                        target="_blank"
                                        href="https://developers.google.com/identity/protocols/oauth2#expiration"
                                        class="text-blue-500 hover:underline"
                                    >
                                        {{ $t("settingsPage.accountPage.troubleshootingModal.googleRefreshTokenLink") }}
                                    </a>
                                </span>
                                <span v-if="selectedEmail?.typeApi === MICROSOFT">
                                    {{ $t("settingsPage.accountPage.troubleshootingModal.microsoftRefreshTokenInfo") }}
                                    <a
                                        target="_blank"
                                        href="https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens"
                                        class="text-blue-500 hover:underline"
                                    >
                                        {{ $t("settingsPage.accountPage.troubleshootingModal.microsoftRefreshTokenLink") }}
                                    </a>
                                </span>
                            </p>
                        </div>
                    </transition>
                </div>

                <!-- Ungrant Consent Section -->
                <div class="p-4">
                    <button @click="toggleConsentInfo" class="text-blue-600 hover:underline">
                        {{ $t("settingsPage.accountPage.troubleshootingModal.didYouKnow") }}
                    </button>
                    <transition name="fade">
                        <div v-if="showConsentInfo" class="mt-2 p-2 border rounded-md bg-gray-100">
                            <p class="text-sm">
                                {{ $t("settingsPage.accountPage.troubleshootingModal.revokeConsentInfo") }}
                            </p>
                            <p class="text-sm">
                                {{ $t("settingsPage.accountPage.troubleshootingModal.forGoogle") }}
                                <a
                                    target="_blank"
                                    href="https://myaccount.google.com/u/1/connections"
                                    class="text-blue-500 hover:underline"
                                >
                                    {{ $t("settingsPage.accountPage.troubleshootingModal.manageGooglePermissions") }}
                                </a>
                            </p>
                            <p class="text-sm">
                                {{ $t("settingsPage.accountPage.troubleshootingModal.forOutlook") }}
                                <a
                                    target="_blank"
                                    href="https://myapps.microsoft.com/"
                                    class="text-blue-500 hover:underline"
                                >
                                    {{ $t("settingsPage.accountPage.troubleshootingModal.manageOutlookPermissions") }}
                                </a>
                                {{ $t("settingsPage.accountPage.troubleshootingModal.outlookWorkAccountNote") }}
                            </p>
                        </div>
                    </transition>
                </div>

                <!-- Action Buttons -->
                <div v-if="!isLoading" class="p-6 flex flex-col items-center space-y-4">
                    <button
                        v-if="errorMessage"
                        :disabled="!selectedEmail"
                        @click="regrantConsent"
                        class="rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:ring-gray-800"
                    >
                        {{ $t("settingsPage.accountPage.troubleshootingModal.regrantConsent") }}
                    </button>
                    <button
                        v-else-if="warningMessage"
                        :disabled="!selectedEmail"
                        @click="synchronize"
                        class="rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:ring-gray-800"
                    >
                        {{ $t("settingsPage.accountPage.troubleshootingModal.synchronize") }}
                    </button>
                    <button
                        v-else
                        :disabled="!selectedEmail"
                        @click="checkConnectivity"
                        class="rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:ring-gray-800"
                        :title="$t('settingsPage.accountPage.troubleshootingModal.connectivityCheckTitle', { provider: providerName })"
                    >
                        {{ $t("settingsPage.accountPage.troubleshootingModal.checkConnectivity") }}
                    </button>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { ref, inject, Ref, computed, onMounted, onUnmounted } from "vue";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import { postData } from "@/global/fetchData";
import { EmailLinked } from "@/global/types";
import UserEmailLinked from "./UserEmailLinked.vue";
import { i18n } from "@/global/preferences";
import { GOOGLE, MICROSOFT } from "@/global/const";

interface connectivityResponse {
    isTokenValid: boolean;
    nbMissedEmails?: number;
}

const props = defineProps<{
    isOpen: boolean;
}>();

const emit = defineEmits<{
    (e: "closeModal"): void;
}>();

const emailsLinked = inject<Ref<EmailLinked[]>>("emailsLinked", ref([]));
const showConsentInfo = ref(false);
const selectedEmail = ref<EmailLinked | null>(null);
const errorMessage = ref<string | null>(null);
const successMessage = ref<string | null>(null);
const warningMessage = ref<string | null>(null);
const isLoading = ref(false);
const loadingMessage = ref("");
const showAdvancedInfo = ref(false);
const nbMissedEmails = ref(0);

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Escape" && props.isOpen) {
        event.preventDefault();
        closeModal();
    }
};

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

onUnmounted(() => {
    document.removeEventListener("keydown", handleKeyDown);
});

const closeModal = () => {
    emit("closeModal");
    resetMessages();
};

const providerName = computed(() => {
    return selectedEmail.value ? getProviderName(selectedEmail.value.typeApi) : "";
});

const toggleConsentInfo = () => {
    showConsentInfo.value = !showConsentInfo.value;
};

const toggleAdvancedInfo = () => {
    showAdvancedInfo.value = !showAdvancedInfo.value;
};

const resetMessages = () => {
    errorMessage.value = null;
    successMessage.value = null;
    warningMessage.value = null;
};

 

const synchronize = async () => {
    if (!selectedEmail.value) return;

    isLoading.value = true;
    loadingMessage.value = i18n.global.t("settingsPage.accountPage.troubleshootingModal.synchronize");

    const result = await postData("user/social_api/synchronize/", {
        email: selectedEmail.value.email,
        nbMissedEmails: nbMissedEmails.value,
    });
    isLoading.value = false;
    resetMessages();

    if (!result.success) {
        errorMessage.value = result.error as string;
        return;
    }

    const nbProcessedEmails = result.data.nbProcessedEmails as number;

    if (nbMissedEmails.value !== nbProcessedEmails) {
        const emailKey = nbProcessedEmails <= 1 ? i18n.global.t("constants.email") : i18n.global.t("constants.emails");

        warningMessage.value =
            i18n.global.t("settingsPage.accountPage.notAllMissedEmailsProcessed") +
            " " +
            `${nbProcessedEmails} ${emailKey} ${i18n.global.t("settingsPage.accountPage.processedOutOf")} ${
                nbMissedEmails.value
            } ${i18n.global.t("settingsPage.accountPage.expected")}`;
        nbMissedEmails.value = nbMissedEmails.value - nbProcessedEmails;
    } else {
        const successMessageKey =
            nbProcessedEmails === 1
                ? "settingsPage.accountPage.singleMissedEmailProcessed"
                : "settingsPage.accountPage.allMissedEmailsProcessed";
        successMessage.value = i18n.global.t(successMessageKey) + " " + i18n.global.t("settingsPage.accountPage.troubleshootingModal.closeModal");
    }
};

const getProviderName = (typeApi: string) => {
    switch (typeApi) {
        case GOOGLE:
            return "Gmail";
        case MICROSOFT:
            return "Outlook";
    }
};

const checkConnectivity = async () => {
    resetMessages();
    if (!selectedEmail.value) return;

    isLoading.value = true;
    loadingMessage.value = i18n.global.t("settingsPage.accountPage.troubleshootingModal.checkingConnectivity");

    const result = await postData("user/social_api/check_connectivity/", { email: selectedEmail.value.email });
    isLoading.value = false;

    if (!result.success) {
        errorMessage.value = result.error as string;
        return;
    }

    const data = result.data as connectivityResponse;
    const providerName = getProviderName(selectedEmail.value.typeApi);

    if (data.isTokenValid) {
        if (data.nbMissedEmails === 0) {
            successMessage.value = i18n.global.t("settingsPage.accountPage.troubleshootingModal.connectivityCheckSuccess", {
                provider: providerName
            });
        } else if (data.nbMissedEmails && data.nbMissedEmails > 0) {
            nbMissedEmails.value = data.nbMissedEmails;

            warningMessage.value = i18n.global.t(
                `settingsPage.accountPage.troubleshootingModal.connectivityCheckMissedEmails.${data.nbMissedEmails > 1 ? 'plural' : 'singular'}`,
                {
                    provider: providerName,
                    count: data.nbMissedEmails
                }
            );
        }
    } else {
        errorMessage.value = i18n.global.t("settingsPage.accountPage.troubleshootingModal.connectivityCheckFailed", {
            provider: providerName
        });
    }
};

const regrantConsent = async () => {
    sessionStorage.setItem("regrantConsent", "true");
    authorize();
};

async function authorize() {
    sessionStorage.setItem("typeApi", GOOGLE);

    const result = await postData(`${selectedEmail.value?.typeApi}/auth_url_regrant/`, {
        email: selectedEmail.value?.email,
    });
    if (result.success) {
        window.location.replace(result.data.authorizationUrl);
    } else {
        errorMessage.value = result.error as string;
    }
}
</script>
