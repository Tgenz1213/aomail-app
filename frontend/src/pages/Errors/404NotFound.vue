<template>
    <div class="fixed inset-0 flex items-center justify-center bg-gray-100">
        <div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full text-center">
            <h2 class="text-2xl font-semibold mb-4">
                {{ $t("errorWebPagesTemplates.error404Page.pageNotFound") }}
            </h2>
            <p class="mb-8 text-gray-600">
                {{ $t("errorWebPagesTemplates.error404Page.pageDoesNotExist") }}
            </p>
            <div class="flex justify-center space-x-4">
                <button
                    @click="goBack"
                    class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 transition"
                >
                    Go back
                </button>
                <button @click="goHome" class="px-4 py-2 bg-black text-white rounded hover:bg-gray-800 transition">
                    Go to Inbox
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import router from "@/router/router";

const goBack = () => {
    router.go(-1);
};

const goHome = () => {
    router.push({ name: "login" });
};
</script>
