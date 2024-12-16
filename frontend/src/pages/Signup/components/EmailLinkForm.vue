<template>
    <div class="flex flex-col">
        <div class="relative">
            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center">
                <span class="bg-white px-2 text-sm text-gray-500">
                    {{ $t("signuUpLinkPage.linkYourMailAccount") }}
                </span>
            </div>
        </div>
        <div class="py-4">
            <div class="relative items-stretch mt-2 flex justify-center items-center gap-4">
                <button
                    type="button"
                    class="inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                    @click="authorizeGoogle"
                >
                    <svg
                        class="-ml-0.5 h-5 w-5"
                        aria-hidden="true"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="currentColor"
                    >
                        <path
                            d="M23.4392061,12.2245191 C23.4392061,11.2412519 23.3594198,10.5237252 23.1867481,9.77963359 L11.9587786,9.77963359 L11.9587786,14.2176183 L18.5493435,14.2176183 C18.4165191,15.3205191 17.6989924,16.9814656 16.104458,18.0975573 L16.0821069,18.2461374 L19.6321832,20.9963359 L19.8781374,21.0208855 C22.1369771,18.9347176 23.4392061,15.8652824 23.4392061,12.2245191"
                            id="Shape"
                            fill="#4285F4"
                        ></path>
                        <path
                            d="M11.9587786,23.9175573 C15.1876031,23.9175573 17.898229,22.8545038 19.8781374,21.0208855 L16.104458,18.0975573 C15.094626,18.8018015 13.7392672,19.2934351 11.9587786,19.2934351 C8.79636641,19.2934351 6.11230534,17.2073588 5.15551145,14.3239695 L5.01526718,14.3358779 L1.32384733,17.1927023 L1.27557252,17.3269008 C3.24210687,21.2334046 7.28152672,23.9175573 11.9587786,23.9175573"
                            id="Shape"
                            fill="#34A853"
                        ></path>
                        <path
                            d="M5.15551145,14.3239695 C4.90305344,13.5798779 4.75694656,12.7825649 4.75694656,11.9587786 C4.75694656,11.1349008 4.90305344,10.3376794 5.14222901,9.59358779 L5.13554198,9.4351145 L1.3978626,6.53239695 L1.27557252,6.59056489 C0.465068702,8.21166412 0,10.0320916 0,11.9587786 C0,13.8854656 0.465068702,15.7058015 1.27557252,17.3269008 L5.15551145,14.3239695"
                            id="Shape"
                            fill="#FBBC05"
                        ></path>
                        <path
                            d="M11.9587786,4.62403053 C14.2043359,4.62403053 15.719084,5.59401527 16.5828092,6.40461069 L19.9578321,3.10928244 C17.8850382,1.18259542 15.1876031,0 11.9587786,0 C7.28152672,0 3.24210687,2.68406107 1.27557252,6.59056489 L5.14222901,9.59358779 C6.11230534,6.71019847 8.79636641,4.62403053 11.9587786,4.62403053"
                            id="Shape"
                            fill="#EB4335"
                        ></path>
                    </svg>
                    {{ $t("signuUpLinkPage.linkYourGmailAccount") }}
                </button>
                <button
                    type="button"
                    class="inline-flex items-center gap-x-2 rounded-md bg-gray-700 px-3 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                    @click="authorizeMicrosoft"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 21 21">
                        <title>MS-SymbolLockup</title>
                        <rect x="1" y="1" width="9" height="9" fill="#f25022" />
                        <rect x="1" y="11" width="9" height="9" fill="#00a4ef" />
                        <rect x="11" y="1" width="9" height="9" fill="#7fba00" />
                        <rect x="11" y="11" width="9" height="9" fill="#ffb900" />
                    </svg>
                    {{ $t("signuUpLinkPage.linkYourOutlookAccount") }}
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
                        {{ $t("signuUpLinkPage.informationOnDataConfidentiality") }}
                    </span>
                </div>
            </div>
            <div class="pt-4">
                <div class="relative items-stretch mt-2">
                    <!-- Keypoint 1: ESOF Cyber Score -->
                    <div class="flex items-center space-x-3">
                        <ShieldCheckIcon class="h-6 w-6 text-green-600" aria-hidden="true" />
                        <span>
                            {{ $t("signuUpLinkPage.ESOFCyberScore") }} 9.7/10
                            <a href="https://tacsecurity.com/" class="text-blue-600 hover:underline" target="_blank">
                                {{ $t("signuUpLinkPage.cyberScoreAssessor") }}
                            </a>
                        </span>
                    </div>
                    <!-- Keypoint 2: Emails Content Encryption -->
                    <div class="flex items-center space-x-3 mt-4">
                        <LockClosedIcon class="h-6 w-6 text-gray-600" aria-hidden="true" />
                        <span>{{ $t("signuUpLinkPage.emailsAreEncryptedAtRest") }}</span>
                    </div>
                    <!-- Keypoint 3: Emails Fallback to Gmail/Outlook -->
                    <div class="flex items-center space-x-3 mt-4">
                        <CloudIcon class="h-6 w-6 text-indigo-600" aria-hidden="true" />
                        <span>{{ $t("signuUpLinkPage.emailsFallbackToProviders") }}</span>
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
                    {{ $t("signuUpLinkPage.finalizeRegistration") }}
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
                        {{ $t("signuUpLinkPage.iAcceptThe") }}
                        <a
                            href="https://aomail.ai/terms-of-service"
                            class="font-medium text-black hover:underline"
                            target="_blank"
                        >
                            {{ $t("signuUpLinkPage.termsOfService") }}
                        </a>
                        {{ $t("signuUpLinkPage.andThe") }}
                        <a
                            href="https://aomail.ai/privacy-policy"
                            class="font-medium text-black hover:underline"
                            target="_blank"
                        >
                            {{ $t("signuUpLinkPage.privacyPolicy") }}
                        </a>
                        {{ $t("signuUpLinkPage.of") }}
                        Aomail
                    </label>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { API_BASE_URL, GOOGLE, MICROSOFT } from "@/global/const";
import { inject, onMounted } from "vue";
import { ShieldCheckIcon, LockClosedIcon, CloudIcon } from "@heroicons/vue/24/outline";

const submitSignupData = inject<() => void>("submitSignupData");

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
