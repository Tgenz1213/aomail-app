<template>
    <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full text-center">
            <h2 class="text-xl font-semibold mb-4">Logging out...</h2>
            <p class="mb-4">You will be redirected to the homepage in {{ countdown }} seconds.</p>
            <p class="text-sm text-gray-500">Clearing session data...</p>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import router from "@/router/router";

const countdown = ref(5);

onMounted(() => {
    localStorage.clear();

    const timer = setInterval(() => {
        if (countdown.value > 0) {
            countdown.value--;
        } else {
            clearInterval(timer);
            router.push({ name: "login" });
        }
    }, 1000);
});
</script>
