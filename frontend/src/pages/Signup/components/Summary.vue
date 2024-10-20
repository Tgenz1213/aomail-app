<template>
    <div class="flex flex-col">
        <div class="relative">
            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center">
                <span class="bg-white px-2 text-sm text-gray-500">
                    {{ $t("signuUpLinkPage.toolsPresentation") }}
                </span>
            </div>
        </div>
        <div class="py-6">
            <div class="relative items-stretch mt-2">
                <iframe
                    class="w-full aspect-[12/5] mx-auto rounded-xl overflow-hidden"
                    src="https://www.youtube.com/embed/3kms81MLYsM"
                    title="Demo v1"
                    allowfullscreen
                ></iframe>
            </div>
        </div>
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
                        ESOF Cyber score: 9.7/10
                        <a href="https://tacsecurity.com/" class="text-blue-600 hover:underline" target="_blank">
                            TAC Security assessor
                        </a>
                    </span>
                </div>
                <!-- Keypoint 2: Emails Content Encryption -->
                <div class="flex items-center space-x-3 mt-4">
                    <LockClosedIcon class="h-6 w-6 text-gray-600" aria-hidden="true" />
                    <span>Emails content are encrypted at rest on our database</span>
                </div>
                <!-- Keypoint 3: Emails Fallback to Gmail/Outlook -->
                <div class="flex items-center space-x-3 mt-4">
                    <CloudIcon class="h-6 w-6 text-indigo-600" aria-hidden="true" />
                    <span>Emails still available in Gmail or Outlook as a fallback</span>
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
import { inject } from "vue";
import { ShieldCheckIcon, LockClosedIcon, CloudIcon } from "@heroicons/vue/24/outline";

const submitSignupData = inject<() => void>("submitSignupData");
</script>
