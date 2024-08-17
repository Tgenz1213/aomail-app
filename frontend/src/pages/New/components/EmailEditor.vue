<template>
    <div class="flex flex-col">
        <div class="flex gap-x-2 items-center">
            <h2 class="text-gray-800 font-semibold text-xl 2xl:text-2xl">
                {{ $t("constants.sendEmailConstants.emailBody") }}
            </h2>
            <button
                @click="toggleEditing"
                class="h-8 w-8 inline-flex items-center justify-center rounded-md border border-gray-300 bg-gray-50 text-gray-500 shadow-sm ring-1 ring-gray-300 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5 2xl:h-6 2xl:w-6"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                >
                    <path d="M6 9v10a1 1 0 001 1h10a1 1 0 001-1V9m-4 0V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v5" />
                </svg>
            </button>
        </div>
        <textarea
            v-model="emailBody"
            rows="6"
            class="mt-2 block w-full rounded-md border-0 py-2.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 2xl:py-3 2xl:text-base"
        ></textarea>
    </div>
</template>

<script setup>
import { ref } from "vue";

const emailBody = ref("");
const toggleEditing = () => {
    // Implement toggle editing logic
};
</script>
