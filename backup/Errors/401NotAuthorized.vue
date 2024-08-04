<template>
    <div class="fixed inset-0 flex items-center justify-center bg-gray-100">
        <div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full text-center">
            <h1 class="text-2xl font-semibold mb-4">
                {{ $t("errorWebPagesTemplates.error401Page.youAreNotConnected") }}
            </h1>
            <p class="mb-4">
                {{ $t("errorWebPagesTemplates.error401Page.redirectionToLogin") }}
                <span class="font-bold">{{ countdown }}</span>
                seconds
            </p>
            <button @click="redirectNow" class="w-full py-2 bg-black text-white rounded hover:bg-gray-800 transition">
                Redirect Now
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()
const countdown = ref<number>(5)
let timer: ReturnType<typeof setInterval>

const updateCountdown = (): void => {
    countdown.value--

    if (countdown.value <= 0) {
        redirectNow()
    }
}

const redirectNow = (): void => {
    if (timer !== undefined) {
        clearInterval(timer)
    }
    router.push({ name: "login" })
}

onMounted(() => {
    timer = setInterval(updateCountdown, 1000)
})

onUnmounted(() => {
    if (timer !== undefined) {
        clearInterval(timer)
    }
})
</script>
