<template>
    <transition name="modal-fade">
        <div
            @click.self="closeModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center p-4"
            v-if="isOpen"
        >
            <div class="bg-white dark:bg-gray-800 rounded-lg relative w-full max-w-2xl p-6 shadow-xl">
                <div class="space-y-6">
                    <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
                        <h2 class="text-2xl font-semibold text-gray-900 dark:text-white">Link Email Account</h2>
                        <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                            Configure your email account using IMAP for reading emails and SMTP for sending them.
                        </p>
                    </div>

                    <div class="space-y-2">
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                            Account Description
                            <span class="text-gray-500 dark:text-gray-400">(Optional)</span>
                        </label>
                        <input
                            v-model="userDescription"
                            :placeholder="$t('signUpPart1Page.summaryUserPlaceholder')"
                            class="w-full p-2.5 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                        />
                    </div>

                    <div class="space-y-4">
                        <p v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</p>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Email Provider</label>
                        <div class="flex items-center space-x-4 mb-4">
                            <div
                                v-for="provider in knownProviders"
                                :key="provider.name"
                                @click="selectProvider(provider)"
                                :class="[
                                    'cursor-pointer p-3 rounded-lg border-2 transition-all duration-200 flex flex-col items-center',
                                    selectedProvider.name === provider.name
                                        ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                                        : 'border-gray-200 dark:border-gray-700 hover:border-blue-200',
                                ]"
                            >
                                <img
                                    v-if="provider.name !== 'Other'"
                                    :src="getProviderLogo(provider.name)"
                                    :alt="provider.name"
                                    class="w-8 h-8 object-contain"
                                />
                                <span v-else class="w-8 h-8 flex items-center justify-center text-xl">⚙️</span>
                                <p class="text-sm mt-2 text-center text-gray-700 dark:text-gray-300">
                                    {{ provider.name }}
                                </p>
                            </div>
                        </div>

                        <a
                            v-if="selectedProvider.link"
                            :href="selectedProvider.link"
                            target="_blank"
                            class="inline-flex items-center text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
                        >
                            <span>View provider setup guide</span>
                            <svg class="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                                />
                            </svg>
                        </a>
                    </div>

                    <div class="space-y-4">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-white">IMAP Configuration</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div v-if="selectedProvider.name === 'Other'">
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Host</label>
                                <input
                                    type="text"
                                    v-model="imapHostName"
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                                    placeholder="imap.example.com"
                                />
                            </div>
                            <div v-if="selectedProvider.name === 'Other'">
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Port</label>
                                <input
                                    type="number"
                                    v-model="imapPort"
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                                />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                    Username
                                </label>
                                <input
                                    type="text"
                                    v-model="imapUsername"
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
                                    placeholder="your.email@example.com"
                                />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                    App Password
                                </label>
                                <input
                                    type="password"
                                    v-model="imapAppPassword"
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
                                    placeholder="Your app-specific password"
                                />
                            </div>
                            <div class="col-span-2">
                                <label class="flex items-center" v-if="selectedProvider.name === 'Other'">
                                    <input
                                        type="checkbox"
                                        v-model="imapSsl"
                                        class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                                    />
                                    <span class="ml-2 text-sm text-gray-600 dark:text-gray-400">Use SSL/TLS</span>
                                </label>
                            </div>
                        </div>
                    </div>

                    <div class="space-y-4">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-white">SMTP Configuration</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div v-if="selectedProvider.name === 'Other'">
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Host</label>
                                <input
                                    type="text"
                                    v-model="smtpHostName"
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                                    placeholder="smtp.example.com"
                                />
                            </div>
                            <div v-if="selectedProvider.name === 'Other'">
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Port</label>
                                <input
                                    type="number"
                                    v-model="smtpPort"
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                                />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                    Username
                                </label>
                                <input
                                    type="text"
                                    v-model="smtpUsername"
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
                                    placeholder="your.email@example.com"
                                />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                    App Password
                                </label>
                                <input
                                    type="password"
                                    v-model="smtpAppPassword"
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
                                    placeholder="Your app-specific password"
                                />
                            </div>
                            <div class="col-span-2">
                                <label class="flex items-center" v-if="selectedProvider.name === 'Other'">
                                    <input
                                        type="checkbox"
                                        v-model="smtpSsl"
                                        class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                                    />
                                    <span class="ml-2 text-sm text-gray-600 dark:text-gray-400">Use SSL/TLS</span>
                                </label>
                            </div>
                        </div>
                    </div>

                    <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                        <button
                            @click="closeModal"
                            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-600"
                        >
                            Cancel
                        </button>
                        <button
                            @click="linkAccount"
                            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:hover:bg-blue-500"
                        >
                            Link Account
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { inject, ref } from "vue";
import { postData } from "@/global/fetchData";
import fastmailLogo from "@/assets/logos/fastmail.svg";
import microsoftLogo from "@/assets/logos/microsoft.svg";
import orangeLogo from "@/assets/logos/orange.svg";
import googleLogo from "@/assets/logos/google.svg";
import yahooLogo from "@/assets/logos/yahoo.svg";
import appleLogo from "@/assets/logos/apple.svg";
import gmxLogo from "@/assets/logos/gmx.svg";
import { knownProviders } from "@/global/emailProviders";

defineProps<{
    isOpen: boolean;
}>();

const emit = defineEmits<{
    (e: "closeModal"): void;
}>();

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const providerLogos: Record<string, string> = {
    Fastmail: fastmailLogo,
    Microsoft: microsoftLogo,
    Google: googleLogo,
    Yahoo: yahooLogo,
    Apple: appleLogo,
    Orange: orangeLogo,
    GMX: gmxLogo,
};

const getProviderLogo = (providerName: string) => {
    return providerLogos[providerName] || "";
};

const selectedProvider = ref(knownProviders[0]);
const errorMessage = ref("");
const userDescription = ref("");

const imapHostName = ref(selectedProvider.value.imapHost);
const imapPort = ref(selectedProvider.value.imapPort);
const imapUsername = ref("");
const imapAppPassword = ref("");
const imapSsl = ref(selectedProvider.value.imapSsl);

const smtpHostName = ref(selectedProvider.value.smtpHost);
const smtpPort = ref(selectedProvider.value.smtpPort);
const smtpUsername = ref("");
const smtpAppPassword = ref("");
const smtpSsl = ref(selectedProvider.value.smtpSsl);

const selectProvider = (provider: (typeof knownProviders)[0]) => {
    selectedProvider.value = provider;
    imapHostName.value = provider.imapHost;
    imapPort.value = provider.imapPort;
    imapUsername.value = "";
    imapAppPassword.value = "";
    imapSsl.value = provider.imapSsl;
    smtpHostName.value = provider.smtpHost;
    smtpPort.value = provider.smtpPort;
    smtpUsername.value = "";
    smtpAppPassword.value = "";
    smtpSsl.value = provider.smtpSsl;
};

const linkAccount = async () => {
    const result = await postData("social_api/link", {
        isImapSmtp: true,
        userDescription: userDescription.value,
        imapHostName: imapHostName.value,
        imapPort: imapPort.value,
        imapUsername: imapUsername.value,
        imapAppPassword: imapAppPassword.value,
        imapSsl: imapSsl.value,
        smtpHostName: smtpHostName.value,
        smtpPort: smtpPort.value,
        smtpUsername: smtpUsername.value,
        smtpAppPassword: smtpAppPassword.value,
        smtpSsl: smtpSsl.value,
    });

    if (!result.success) {
        errorMessage.value = result.error as string;
    } else {
        displayPopup?.("success", "Email linked", "Your email has been linked successfully");
        closeModal();
    }
};

const closeModal = () => {
    emit("closeModal");
};
</script>
