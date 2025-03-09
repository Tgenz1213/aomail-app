<template>
    <transition name="modal-fade">
        <div
            @click.self="closeModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center p-4"
            v-if="isOpen"
        >
            <div class="bg-white dark:bg-gray-800 rounded-lg relative w-full h-full m-32 p-6 shadow-xl">
                <form @submit.prevent>
                    <div class="space-y-6 overflow-y-auto max-h-full">
                        <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
                            <h2 class="text-2xl font-semibold text-gray-900 dark:text-white">Link Email Account</h2>
                            <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                                Configure your email account using IMAP for reading emails and SMTP for sending them.
                            </p>
                        </div>

                        <div class="space-y-4">
                            <p v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</p>
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                Email Provider
                            </label>
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
                                        :src="getProviderSvg(provider.typeApi)"
                                        :alt="provider.name"
                                        class="w-8 h-8 object-contain"
                                    />
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

                            <div class="space-y-4 mt-6">
                                <div class="space-y-2">
                                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                        Email Address
                                    </label>
                                    <input
                                        type="text"
                                        v-model="emailAddress"
                                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
                                        placeholder="your.email@example.com"
                                    />
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
                            </div>
                        </div>

                        <div class="space-y-4">
                            <h3 class="text-lg font-medium text-gray-900 dark:text-white">IMAP Configuration</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div v-if="selectedProvider.name === 'Other'">
                                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                        Host
                                    </label>
                                    <input
                                        type="text"
                                        v-model="imapHost"
                                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                                        placeholder="imap.example.com"
                                    />
                                </div>
                                <div v-if="selectedProvider.name === 'Other'">
                                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                        Port
                                    </label>
                                    <input
                                        type="number"
                                        v-model="imapPort"
                                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                                    />
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                        App Password
                                    </label>
                                    <div class="flex flex-col">
                                        <div class="relative items-stretch mt-2 flex">
                                            <input
                                                placeholder="Enter your IMAP app password"
                                                id="imapAppPassword"
                                                v-if="!showImapPassword"
                                                type="password"
                                                class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                v-model="imapAppPassword"
                                            />
                                            <input
                                                v-else
                                                id="imapAppPassword"
                                                type="text"
                                                class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                v-model="imapAppPassword"
                                            />
                                            <button
                                                @click="toggleImapPasswordVisibility"
                                                class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300"
                                            >
                                                <svg class="w-6 h-6" stroke="currentColor">
                                                    <use
                                                        :href="
                                                            eyeIcon +
                                                            '#' +
                                                            (showImapPassword ? 'eye-hidden' : 'eye-visible')
                                                        "
                                                    />
                                                </svg>
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <label
                                    class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                                    v-if="selectedProvider.name === 'Other'"
                                >
                                    IMAP Encryption
                                </label>
                                <div class="flex items-center space-x-4" v-if="selectedProvider.name === 'Other'">
                                    <label class="inline-flex items-center">
                                        <input
                                            type="radio"
                                            v-model="imapEncryption"
                                            name="imapEncryption"
                                            value="none"
                                            class="form-radio text-blue-600"
                                        />
                                        <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">No encryption</span>
                                    </label>
                                    <label class="inline-flex items-center">
                                        <input
                                            type="radio"
                                            v-model="imapEncryption"
                                            name="imapEncryption"
                                            value="tls"
                                            class="form-radio text-blue-600"
                                        />
                                        <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">TLS</span>
                                    </label>
                                </div>
                            </div>
                        </div>

                        <div class="space-y-4">
                            <h3 class="text-lg font-medium text-gray-900 dark:text-white">SMTP Configuration</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div v-if="selectedProvider.name === 'Other'">
                                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                        Host
                                    </label>
                                    <input
                                        type="text"
                                        v-model="smtpHost"
                                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                                        placeholder="smtp.example.com"
                                    />
                                </div>
                                <div v-if="selectedProvider.name === 'Other'">
                                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                        Port
                                    </label>
                                    <input
                                        type="number"
                                        v-model="smtpPort"
                                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
                                    />
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                        App Password
                                    </label>
                                    <div class="flex flex-col">
                                        <div class="relative items-stretch mt-2 flex">
                                            <input
                                                placeholder="Enter your SMTP app password"
                                                id="smtpAppPassword"
                                                v-if="!showSmtpPassword"
                                                type="password"
                                                class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                v-model="smtpAppPassword"
                                            />
                                            <input
                                                v-else
                                                id="smtpAppPassword"
                                                type="text"
                                                class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                v-model="smtpAppPassword"
                                            />
                                            <button
                                                type="button"
                                                @click.prevent="toggleSmtpPasswordVisibility"
                                                class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300"
                                            >
                                                <svg class="w-6 h-6" stroke="currentColor">
                                                    <use
                                                        :href="
                                                            eyeIcon +
                                                            '#' +
                                                            (showSmtpPassword ? 'eye-hidden' : 'eye-visible')
                                                        "
                                                    />
                                                </svg>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-span-2" v-if="selectedProvider.name === 'Other'">
                                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                        SMTP Encryption
                                    </label>
                                    <div class="flex items-center space-x-4">
                                        <label class="inline-flex items-center">
                                            <input
                                                type="radio"
                                                v-model="smtpEncryption"
                                                name="smtpEncryption"
                                                value="none"
                                                class="form-radio text-blue-600"
                                            />
                                            <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">
                                                No encryption
                                            </span>
                                        </label>
                                        <label class="inline-flex items-center">
                                            <input
                                                type="radio"
                                                v-model="smtpEncryption"
                                                name="smtpEncryption"
                                                value="ssl"
                                                class="form-radio text-blue-600"
                                            />
                                            <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">SSL</span>
                                        </label>
                                        <label class="inline-flex items-center">
                                            <input
                                                type="radio"
                                                v-model="smtpEncryption"
                                                name="smtpEncryption"
                                                value="tls"
                                                class="form-radio text-blue-600"
                                            />
                                            <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">TLS</span>
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                            <button
                                type="button"
                                @click.stop.prevent="closeModal"
                                class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-600"
                            >
                                Cancel
                            </button>
                            <button
                                type="button"
                                v-if="!isSignup"
                                @click="linkAccount"
                                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:hover:bg-blue-500"
                            >
                                Link Account
                            </button>
                            <button
                                type="button"
                                v-else
                                @click.stop.prevent="saveServerConfigs"
                                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:hover:bg-blue-500"
                            >
                                Save
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { inject, onMounted, onUnmounted, ref } from "vue";
import { postData } from "@/global/fetchData";
import eyeIcon from "@/assets/eye-icon.svg";
import { knownProviders } from "@/global/emailProviders";

const props = defineProps<{
    isOpen: boolean;
    isSignup: boolean;
    saveImapSmtpConfigs?: (
        typeApi: string,
        emailAddress: string,
        userDescription: string,
        imapHost: string,
        imapPort: number,
        imapAppPassword: string,
        imapEncryption: string,
        smtpHost: string,
        smtpPort: number,
        smtpAppPassword: string,
        smtpEncryption: string
    ) => void;
}>();

const emit = defineEmits<{
    (e: "closeModal"): void;
}>();

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const fetchEmailLinked = inject<() => void>("fetchEmailLinked");

function getProviderSvg(provider: string) {
    try {
        return require(`@/assets/logos/${provider}.svg`);
    } catch {
        return require(`@/assets/logos/other.svg`);
    }
}

const selectedProvider = ref(knownProviders[0]);
const errorMessage = ref("");

const typeApi = ref(selectedProvider.value.typeApi);
const emailAddress = ref("");
const userDescription = ref("");

const imapHost = ref(selectedProvider.value.imapHost);
const imapPort = ref(selectedProvider.value.imapPort);
const imapAppPassword = ref("");
const imapEncryption = ref("tls");
const smtpHost = ref(selectedProvider.value.smtpHost);
const smtpPort = ref(selectedProvider.value.smtpPort);
const smtpAppPassword = ref("");
const smtpEncryption = ref("ssl");

const showImapPassword = ref(false);
const showSmtpPassword = ref(false);

const selectProvider = (provider: (typeof knownProviders)[0]) => {
    selectedProvider.value = provider;
    typeApi.value = provider.typeApi;

    imapHost.value = provider.imapHost;
    imapPort.value = provider.imapPort;
    imapAppPassword.value = "";
    imapEncryption.value = provider.imapEncryption;

    smtpHost.value = provider.smtpHost;
    smtpPort.value = provider.smtpPort;
    smtpAppPassword.value = "";
    smtpEncryption.value = provider.smtpEncryption;
};

const linkAccount = async () => {
    const result = await postData("user/social_api/link/", {
        typeApi: typeApi.value,
        emailAddress: emailAddress.value,
        userDescription: userDescription.value,
        imapHost: imapHost.value,
        imapPort: imapPort.value,
        imapAppPassword: imapAppPassword.value,
        imapEncryption: imapEncryption.value,
        smtpHost: smtpHost.value,
        smtpPort: smtpPort.value,
        smtpAppPassword: smtpAppPassword.value,
        smtpEncryption: smtpEncryption.value,
    });

    if (!result.success) {
        errorMessage.value = result.error as string;
    } else {
        displayPopup?.("success", "Email linked", "Your email has been linked successfully");
        fetchEmailLinked?.();
        closeModal();
    }
};

function saveServerConfigs() {
    if (props.saveImapSmtpConfigs) {
        props.saveImapSmtpConfigs(
            typeApi.value,
            emailAddress.value,
            userDescription.value,
            imapHost.value,
            imapPort.value,
            imapAppPassword.value,
            imapEncryption.value,
            smtpHost.value,
            smtpPort.value,
            smtpAppPassword.value,
            smtpEncryption.value
        );
    }
    closeModal();
}

function toggleImapPasswordVisibility() {
    showImapPassword.value = !showImapPassword.value;
}

function toggleSmtpPasswordVisibility() {
    showSmtpPassword.value = !showSmtpPassword.value;
}

const closeModal = () => {
    emit("closeModal");
    errorMessage.value = "";
};

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Escape") {
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
</script>
