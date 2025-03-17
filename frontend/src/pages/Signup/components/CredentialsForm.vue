<template>
    <div class="flex flex-col gap-y-4">
        <div v-if="credentialError" class="mt-2 text-sm text-red-600">
            {{ credentialError }}
        </div>
        <div>
            <div class="flex gap-x-1 items-center">
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
                        d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"
                    />
                </svg>
                <label for="login" class="block text-sm font-medium leading-6 text-gray-900">
                    {{ $t("constants.loginUppercase") }}
                </label>
            </div>
            <div class="mt-2">
                <input
                    v-model="login"
                    id="login"
                    type="text"
                    class="block w-full rounded-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                />
            </div>
        </div>
        <div>
            <div class="flex gap-x-1 items-center">
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
                        d="M15.75 5.25a3 3 0 0 1 3 3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1 1 21.75 8.25Z"
                    />
                </svg>
                <label for="password" class="block text-sm font-medium leading-6 text-gray-900">
                    {{ $t("constants.password") }}
                </label>
            </div>
            <div class="relative items-stretch mt-2 flex">
                <input
                    id="password"
                    v-if="!showPassword"
                    type="password"
                    class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                    v-model="password"
                />
                <input
                    id="password"
                    v-else
                    type="text"
                    class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                    v-model="password"
                />
                <div class="flex items-center">
                    <button
                        @click.prevent="togglePasswordVisibility"
                        class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300"
                    >
                        <svg class="w-6 h-6" stroke="currentColor">
                            <use :href="eyeIcon + '#' + (showPassword ? 'eye-hidden' : 'eye-visible')" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <div>
            <div class="flex gap-x-1 items-center">
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
                        d="M15.75 5.25a3 3 0 0 1 3 3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1 1 21.75 8.25Z"
                    />
                </svg>
                <label for="password" class="block text-sm font-medium leading-6 text-gray-900">
                    {{ $t("signUpPart1Page.passwordConfirm") }}
                </label>
            </div>
            <div class="relative items-stretch mt-2 flex">
                <input
                    id="confirmPassword"
                    v-if="!showConfirmPassword"
                    type="password"
                    v-model="confirmPassword"
                    @input="clearError"
                    autocomplete="current-password"
                    class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                />
                <input
                    id="confirmPassword"
                    v-else
                    type="text"
                    class="flex-1 rounded-l-md border-0 pl-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-800 sm:text-sm sm:leading-6"
                    v-model="confirmPassword"
                />
                <button
                    @click.prevent="toggleConfirmPasswordVisibility"
                    class="p-2 bg-gray-50 rounded-r-md ring-l-none ring-1 ring-inset ring-gray-300"
                >
                    <svg class="w-6 h-6" stroke="currentColor">
                        <use :href="eyeIcon + '#' + (showConfirmPassword ? 'eye-hidden' : 'eye-visible')" />
                    </svg>
                </button>
            </div>
        </div>
        <div>
            <div class="pt-2">
                <button
                    @click.prevent="goStepLinkEmail"
                    class="flex w-full justify-center rounded-md bg-gray-800 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500"
                >
                    {{ $t("signUpPart1Page.continue") }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject, Ref, ref } from "vue";
import eyeIcon from "@/assets/eye-icon.svg";

const login = inject<Ref<string>>("login") || ref("");
const password = inject<Ref<string>>("password") || ref("");
const confirmPassword = inject<Ref<string>>("confirmPassword") || ref("");
const credentialError = inject<Ref<string>>("credentialError") || ref("");
const showPassword = ref<boolean>(false);
const showConfirmPassword = ref<boolean>(false);

const goStepLinkEmail = inject<() => void>("goStepLinkEmail");
const clearError = inject<() => void>("clearError");

function togglePasswordVisibility() {
    showPassword.value = !showPassword.value;
}

function toggleConfirmPasswordVisibility() {
    showConfirmPassword.value = !showConfirmPassword.value;
}
</script>
