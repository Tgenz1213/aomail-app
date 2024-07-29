<template>
    <div
        v-if="isModalOpen"
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
    >
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
                    <label for="confirmPassword" class="block font-bold mb-2">
                        Confirm Password:
                    </label>
                    <input
                        type="password"
                        id="confirmPassword"
                        v-model="confirmPassword"
                        required
                        class="w-full p-2 border border-gray-300 rounded"
                    />
                </div>
                <button
                    type="submit"
                    class="w-full py-2 bg-black text-white rounded hover:bg-gray-800 transition"
                >
                    Submit
                </button>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

import { useRouter } from "vue-router"
import ShowNotification from "@/components/NotificationTimer.vue"
import { API_BASE_URL } from "@/global/const";

const isModalOpen = ref(true)
const password = ref("")
const confirmPassword = ref("")
const uidb64 = ref("")
const token = ref("")
const router = useRouter()

// Variables to display a notification
const showNotification = ref(false)
const notificationTitle = ref("")
const notificationMessage = ref("")
const backgroundColor = ref("")
const timerId = ref(null)

onMounted(() => {
    const urlParams = new URLSearchParams(window.location.search)
    uidb64.value = urlParams.get("uidb64")
    token.value = urlParams.get("token")
})

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

async function resetPassword() {
    if (password.value.length < 8 || password.value.length > 32) {
        backgroundColor.value = "bg-red-200/[.89] border border-red-400"
        notificationTitle.value = "Error"
        notificationMessage.value = "Password length must be between 8 and 32 characters"
        displayPopup()
        return
    }

    if (password.value !== confirmPassword.value) {
        backgroundColor.value = "bg-red-200/[.89] border border-red-400"
        notificationTitle.value = "Error"
        notificationMessage.value = "Passwords do not match"
        displayPopup()
        return
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}reset_password/${uidb64.value}/${token.value}/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ password: password.value }),
            }
        )

        if (response.status === 200) {
            backgroundColor.value = "bg-green-200/[.89] border border-green-400"
            notificationTitle.value = "Success"
            notificationMessage.value = "Password reset successful! Redirecting..."
            displayPopup()

            setTimeout(() => {
                router.push({ name: "login" })
            }, 3000)
        } else {
            const data = await response.json()
            backgroundColor.value = "bg-red-200/[.89] border border-red-400"
            notificationTitle.value = "Error"
            notificationMessage.value = data.error || "An error occurred. Please try again."
            displayPopup()
        }
    } catch (error) {
        backgroundColor.value = "bg-red-200/[.89] border border-red-400"
        notificationTitle.value = "Error"
        notificationMessage.value = error.message || "An error occurred. Please try again."
        displayPopup()
    }
}
</script>

<script>
export default {
    name: "ResetPasswordForm",
}
</script>



<!-- TODO: FOLLOW these guidelines anyway
the import of constants and function are correct. You must do the following operations:

create functions: displaySuccessPopUp & displayErrorPpUp instead of hardcodin everywhere
if possible put everything under script setup if its more optimal and easier to manage
remove all comments (unless those who mentionned Théo & Jean) you DELETE the rest no execption
optimize the code
use strictly camelCase
we are using TypeScript so migrate everything where its needed using interfaces or types -->