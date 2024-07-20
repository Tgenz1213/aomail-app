<template>
    <div
        v-if="isModalOpen"
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
    >
        <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full">
            <ShowNotification
                :showNotification="showNotification"
                :notificationTitle="notificationTitle"
                :notificationMessage="notificationMessage"
                :backgroundColor="backgroundColor"
                @dismiss-popup="dismissPopup"
            />
            <h2 class="text-xl font-semibold mb-4">Reset Password</h2>
            <p class="mb-4">
                Please enter your email address below to receive a link to reset your password.
            </p>
            <input
                type="email"
                v-model="email"
                placeholder="Enter your email"
                class="w-full p-2 border border-gray-300 rounded mb-4"
                required
            />
            <button
                @click="generateResetLink"
                class="w-full py-2 bg-black text-white rounded hover:bg-gray-800 transition"
            >
                Submit
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import ShowNotification from "../components/NotificationTimer.vue"
import { API_BASE_URL } from "@/main"

const isModalOpen = ref(true)
const email = ref("")
const router = useRouter()

// Variables to display a notification
const showNotification = ref(false)
const notificationTitle = ref("")
const notificationMessage = ref("")
const backgroundColor = ref("")
let timerId = ref(null)

function dismissPopup() {
    showNotification.value = false
    clearTimeout(timerId.value)
}

function displayPopup() {
    showNotification.value = true
    timerId.value = setTimeout(() => {
        dismissPopup()
    }, 4000)
}

async function generateResetLink() {
    try {
        const response = await fetch(`${API_BASE_URL}generate_reset_token/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: email.value }),
        })

        if (response.status === 200) {
            backgroundColor.value = "bg-green-200/[.89] border border-green-400"
            notificationTitle.value = "Check your mailbox!"
            notificationMessage.value = "Redirecting..."
            displayPopup()

            setTimeout(() => {
                router.push({ name: "login" })
            }, 3000)
        } else {
            const data = await response.json()
            backgroundColor.value = "bg-red-200/[.89] border border-red-400"
            notificationTitle.value = "Error sending password reset email"
            notificationMessage.value = data.error
            displayPopup()
        }
    } catch (error) {
        backgroundColor.value = "bg-red-200/[.89] border border-red-400"
        notificationTitle.value = "Error sending password reset email"
        notificationMessage.value = error.message
        displayPopup()
    }
}
</script>

<script>
export default {
    name: "ModalComponent",
}
</script>
