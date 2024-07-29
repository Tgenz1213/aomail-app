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

<script setup>
import { ref, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()
const countdown = ref(5)
let timer

const updateCountdown = () => {
    countdown.value--

    if (countdown.value <= 0) {
        redirectNow()
    }
}

const redirectNow = () => {
    clearInterval(timer)
    router.push({ name: "login" })
}

onMounted(() => {
    timer = setInterval(updateCountdown, 1000)
})

onUnmounted(() => {
    clearInterval(timer)
})
</script>

<!-- TODO: FOLLOW these guidelines anyway
the import of constants and function are correct. You must do the following operations:

if possible put everything under script setup if its more optimal and easier to manage
remove all comments (unless those who mentionned Théo & Jean) you DELETE the rest no execption
optimize the code
use strictly camelCase
we are using TypeScript so migrate everything where its needed using interfaces or types -->
