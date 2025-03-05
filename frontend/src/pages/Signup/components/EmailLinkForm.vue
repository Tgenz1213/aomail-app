<template>
    <div class="flex flex-col">
        <div class="relative">
            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center">
                <span class="bg-white px-2 text-sm text-gray-500">
                    {{ $t("signUpLinkPage.linkYourMailAccount") }}
                </span>
            </div>
        </div>
        <div class="py-4">
            <div class="relative items-stretch mt-2 flex justify-center items-center gap-4">
                <button
                    type="button"
                    :class="[
                        'inline-flex items-center gap-x-2 rounded-md px-3 py-2.5 text-sm font-semibold text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600',
                        isGoogleLinked ? 'bg-emerald-500 cursor-default' : 'bg-gray-700 hover:bg-gray-600',
                    ]"
                    @click="authorizeGoogle"
                >
                    <img src="@/assets/logos/google.svg" alt="Google" class="w-5 h-5" />
                    {{ $t("signUpLinkPage.linkYourGmailAccount") }}
                    <CheckIcon v-if="isGoogleLinked" class="h-5 w-5 text-white" aria-hidden="true" />
                </button>
                <button
                    type="button"
                    :class="[
                        'inline-flex items-center gap-x-2 rounded-md px-3 py-2.5 text-sm font-semibold text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600',
                        isMicrosoftLinked ? 'bg-emerald-500 cursor-default' : 'bg-gray-700 hover:bg-gray-600',
                    ]"
                    @click="authorizeMicrosoft"
                >
                    <img src="@/assets/logos/microsoft.svg" alt="Microsoft" class="w-5 h-5" />
                    {{ $t("signUpLinkPage.linkYourOutlookAccount") }}
                    <CheckIcon v-if="isMicrosoftLinked" class="h-5 w-5 text-white" aria-hidden="true" />
                </button>
            </div>
        </div>
        <div class="pt-4">
            <div class="relative">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="w-full border-t border-gray-300"></div>
                </div>
                <div class="relative flex justify-center">
                    <span class="bg-white px-2 text-sm text-gray-500">
                        {{ $t("signUpLinkPage.informationOnDataConfidentiality") }}
                    </span>
                </div>
            </div>
            <div class="pt-4">
                <div class="relative items-stretch mt-2">
                    <!-- Keypoint 1: ESOF Cyber Score -->
                    <div class="flex items-center space-x-3">
                        <ShieldCheckIcon class="h-6 w-6 text-green-600" aria-hidden="true" />
                        <span>
                            {{ $t("signUpLinkPage.ESOFCyberScore") }} 9.7/10
                            <a
                                href="https://aomail.ai/aomail-tac-security-tier2-assessment.pdf"
                                class="text-blue-600 hover:underline"
                                target="_blank"
                            >
                                {{ $t("signUpLinkPage.cyberScoreAssessor") }}
                            </a>
                        </span>
                    </div>
                    <!-- Keypoint 2: Emails Content Encryption -->
                    <div class="flex items-center space-x-3 mt-4">
                        <LockClosedIcon class="h-6 w-6 text-gray-600" aria-hidden="true" />
                        <span>{{ $t("signUpLinkPage.emailsAreEncryptedAtRest") }}</span>
                    </div>
                    <!-- Keypoint 3: Emails Fallback to Gmail/Outlook -->
                    <div class="flex items-center space-x-3 mt-4">
                        <CloudIcon class="h-6 w-6 text-indigo-600" aria-hidden="true" />
                        <span>{{ $t("signUpLinkPage.emailsFallbackToProviders") }}</span>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <div class="pt-8">
                <button
                    id="submit-button"
                    @click="submitSignupData"
                    class="flex w-full justify-center rounded-md bg-gray-800 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800"
                >
                    {{ $t("signUpLinkPage.finalizeRegistration") }}
                </button>
            </div>
        </div>
        <div class="space-y-5 pt-3">
            <div class="relative flex items-start">
                <div class="flex h-6 items-center">
                    <input
                        id="comments"
                        aria-describedby="comments-description"
                        name="comments"
                        type="checkbox"
                        class="h-4 w-4 rounded border-gray-300 text-black focus:ring-black"
                    />
                </div>
                <div class="ml-3 text-sm leading-6 w-full">
                    <label for="comments" class="text-gray-500 font-normal">
                        {{ $t("signUpLinkPage.iAcceptThe") }}
                        <a
                            href="https://aomail.ai/terms-of-service"
                            class="font-medium text-black hover:underline"
                            target="_blank"
                        >
                            {{ $t("signUpLinkPage.termsOfService") }}
                        </a>
                        {{ $t("signUpLinkPage.andThe") }}
                        <a
                            href="https://aomail.ai/privacy-policy"
                            class="font-medium text-black hover:underline"
                            target="_blank"
                        >
                            {{ $t("signUpLinkPage.privacyPolicy") }}
                        </a>
                        {{ $t("signUpLinkPage.of") }}
                        Aomail
                    </label>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { API_BASE_URL, GOOGLE, MICROSOFT } from "@/global/const";
import { inject, onMounted, ref } from "vue";
import { ShieldCheckIcon, LockClosedIcon, CloudIcon, CheckIcon } from "@heroicons/vue/24/outline";
const submitSignupData = inject<() => void>("submitSignupData");
const isGoogleLinked = ref(false);
const isMicrosoftLinked = ref(false);

onMounted(() => {
    const typeApi = sessionStorage.getItem("typeApi");
    if (typeApi === GOOGLE) {
        isGoogleLinked.value = true;
    } else if (typeApi === MICROSOFT) {
        isMicrosoftLinked.value = true;
    }
});

function authorizeGoogle(event: Event) {
    event.preventDefault();
    sessionStorage.setItem("typeApi", GOOGLE);
    window.location.replace(`${API_BASE_URL}google/auth_url/`);
}

function authorizeMicrosoft(event: Event) {
    event.preventDefault();
    sessionStorage.setItem("typeApi", MICROSOFT);
    window.location.replace(`${API_BASE_URL}microsoft/auth_url/`);
}
</script>
