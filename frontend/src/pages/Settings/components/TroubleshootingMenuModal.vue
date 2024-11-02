<!-- TODO for Théo:
1) Add a spinner when loading 
2) Re-work the UI to match Aomail design
3) Hide the tooltip "This checks if Aomail is connected with {{ providerName }} servers" and display it onButtonHover
4) Clean translations for all text I wrote
 (try to optimize while thinking not all languages have the same logic as French and English => better duplicate some data sometimes) 
5) Keep the code clean (you can delete comments) + Format the code with Prettier (Shift + Alt + F)
-->

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
                <div v-if="isLoading" class="flex flex-col items-center p-4">
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
                            class="border border-gray-300 rounded-md bg-gray-100 flex items-center justify-between p-2 shadow hover:shadow-md"
                        >
                            <label class="flex items-center">
                                <input type="radio" v-model="selectedEmail" :value="email" class="mr-2" />
                                <UserEmailLinked :email="email" :isRegrant="true" />
                            </label>
                        </li>
                    </ul>
                </div>

                <div v-if="errorMessage" class="p-4">
                    <button @click="toggleAdvancedInfo" class="text-blue-600 hover:underline">
                        Advanced Explanations
                    </button>
                    <transition name="fade">
                        <div v-if="showAdvancedInfo" class="mt-2 p-2 border rounded-md bg-gray-100">
                            <p class="text-sm">
                                <span v-if="selectedEmail?.typeApi === GOOGLE">
                                    You have changed your Google account password or revoked consent for Aomail. A list
                                    of all possible reasons can be found at:
                                    <a
                                        target="_blank"
                                        href="https://developers.google.com/identity/protocols/oauth2#expiration"
                                        class="text-blue-500 hover:underline"
                                    >
                                        Google Refresh Token Expiration Conditions
                                    </a>
                                </span>
                                <span v-if="selectedEmail?.typeApi === MICROSOFT">
                                    You have not used your Microsoft account for 90 days (neither sent nor received
                                    emails). More information about expiration conditions can be found at:
                                    <a
                                        target="_blank"
                                        href="https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens"
                                        class="text-blue-500 hover:underline"
                                    >
                                        Microsoft Refresh Token Expiration Conditions
                                    </a>
                                </span>
                            </p>
                        </div>
                    </transition>
                </div>

                <!-- Ungrant Consent Section -->
                <div class="p-4">
                    <button @click="toggleConsentInfo" class="text-blue-600 hover:underline">Did you know?</button>
                    <transition name="fade">
                        <div v-if="showConsentInfo" class="mt-2 p-2 border rounded-md bg-gray-100">
                            <p class="text-sm">
                                You can revoke your consent at any time for apps that you've authorized:
                            </p>
                            <p class="text-sm">
                                For Google:
                                <a
                                    target="_blank"
                                    href="https://myaccount.google.com/u/1/connections"
                                    class="text-blue-500 hover:underline"
                                >
                                    Manage Google App Permissions
                                </a>
                            </p>
                            <p class="text-sm">
                                For Outlook:
                                <a
                                    target="_blank"
                                    href="https://myapps.microsoft.com/"
                                    class="text-blue-500 hover:underline"
                                >
                                    Manage Outlook App Permissions
                                </a>
                                or contact your administrator if you are using a school or work account.
                            </p>
                        </div>
                    </transition>
                </div>

                <!-- Action Buttons -->
                <div v-if="!isLoading" class="pt-6 flex flex-col items-center space-y-4">
                    <button
                        v-if="errorMessage"
                        :disabled="!selectedEmail"
                        @click="regrantConsent"
                        class="rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:ring-gray-800"
                    >
                        Regrant consent
                    </button>
                    <button
                        v-else-if="warningMessage"
                        :disabled="!selectedEmail"
                        @click="synchronize"
                        class="rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:ring-gray-800"
                    >
                        Synchronize
                    </button>
                    <button
                        v-else
                        :disabled="!selectedEmail"
                        @click="checkConnectivity"
                        class="rounded-md bg-gray-800 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:ring-gray-800"
                    >
                        Check connectivity
                        <div v-if="selectedEmail">
                            This checks if Aomail is connected with {{ providerName }} servers
                        </div>
                    </button>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, inject, Ref, computed, onMounted, onUnmounted } from "vue";
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

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

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

function capitalizeFirstLetter(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

const synchronize = async () => {
    if (!selectedEmail.value) return;

    isLoading.value = true;
    loadingMessage.value = "Synchronizing your data...";

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
        successMessage.value = i18n.global.t(successMessageKey) + " " + "You can close this modal.";
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
    loadingMessage.value = "Checking connectivity...";

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
            successMessage.value = `Aomail is connected to your ${providerName} account and no emails have been missed. No action is required. You can close this modal.`;
        } else if (data.nbMissedEmails && data.nbMissedEmails > 0) {
            nbMissedEmails.value = data.nbMissedEmails;

            warningMessage.value = `Aomail is connected to your ${providerName} account, but ${
                data.nbMissedEmails
            } email${
                data.nbMissedEmails > 1 ? "s have" : " has"
            } been missed. Please synchronize with ${capitalizeFirstLetter(selectedEmail.value.typeApi)} servers.`;
        }
    } else {
        errorMessage.value = `Aomail is not connected to your ${providerName} account. Please regrant access and then synchronize emails received with Aomail.`;
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
