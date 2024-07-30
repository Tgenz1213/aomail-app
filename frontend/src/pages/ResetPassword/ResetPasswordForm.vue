<template>
    <div v-if="isModalOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
            <ShowNotification
                :showNotification="showNotification"
                :notificationTitle="notificationTitle"
                :notificationMessage="notificationMessage"
                :backgroundColor="backgroundColor"
                @dismiss-popup="dismissPopup"
            />
            <h1 class="text-2xl mb-6">Reset Password</h1>
            <p class="text-lg mb-6">Please enter your new password below.</p>
            <form @submit.prevent="resetPassword">
                <div class="mb-6">
                    <label for="password" class="block font-bold mb-2">Password:</label>
                    <input
                        type="password"
                        id="password"
                        v-model="password"
                        required
                        class="w-full p-2 border border-gray-300 rounded"
                    />
                </div>
                <div class="mb-6">
                    <label for="confirmPassword" class="block font-bold mb-2">Confirm Password:</label>
                    <input
                        type="password"
                        id="confirmPassword"
                        v-model="confirmPassword"
                        required
                        class="w-full p-2 border border-gray-300 rounded"
                    />
                </div>
                <button type="submit" class="w-full py-2 bg-black text-white rounded hover:bg-gray-800 transition">
                    Submit
                </button>
            </form>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import ShowNotification from "@/components/NotificationTimer.vue"
import { API_BASE_URL } from "@/global/const"
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp"

const isModalOpen = ref(true)
const password = ref<string>("")
const confirmPassword = ref<string>("")
const uidb64 = ref<string>("")
const token = ref<string>("")
const router = useRouter()

const showNotification = ref<boolean>(false)
const notificationTitle = ref<string>("")
const notificationMessage = ref<string>("")
const backgroundColor = ref<string>("")
const timerId = ref<NodeJS.Timeout | null>(null)

onMounted(() => {
    const urlParams = new URLSearchParams(window.location.search)
    uidb64.value = urlParams.get("uidb64") || ""
    token.value = urlParams.get("token") || ""
})

function dismissPopup() {
    showNotification.value = false
    if (timerId.value) {
        clearTimeout(timerId.value)
    }
}

function displayPopup(type: "success" | "error", title: string, message: string) {
    if (type === "error") {
        displayErrorPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message)
    } else {
        displaySuccessPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message)
    }
    timerId.value = setTimeout(dismissPopup, 4000)
}

async function resetPassword() {
    if (password.value.length < 8 || password.value.length > 32) {
        displayPopup("error", "Error", "Password length must be between 8 and 32 characters")
        return
    }

    if (password.value !== confirmPassword.value) {
        displayPopup("error", "Error", "Passwords do not match")
        return
    }

    try {
        const response = await fetch(`${API_BASE_URL}reset_password/${uidb64.value}/${token.value}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ password: password.value }),
        })

        if (response.ok) {
            displayPopup("success", "Success", "Password reset successful! Redirecting...")
            setTimeout(() => {
                router.push({ name: "login" })
            }, 3000)
        } else {
            const data = await response.json()
            displayPopup("error", "Error", data.error || "An error occurred. Please try again.")
        }
    } catch (error) {
        displayPopup("error", "Error", (error as Error).message || "An error occurred. Please try again.")
    }
}
</script>
