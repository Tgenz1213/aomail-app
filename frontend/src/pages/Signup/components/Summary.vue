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
                <p class="font-semibold">{{ $t("constants.workInProgress") }}</p>
                <!-- To add : A video that explain the tool -->
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
                <p class="font-semibold">{{ $t("constants.workInProgress") }}</p>
                <!-- To add : A video that explain how data is saved and used -->
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
                        <a href="terms-and-conditions" class="font-medium text-black hover:underline" target="_blank">
                            {{ $t("signuUpLinkPage.conditionsAndPrivacyPolicyOf") }}
                        </a>
                        Aomail
                    </label>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject } from "vue";

const submitSignupData = inject<() => void>("submitSignupData");
</script>
