<template>
    <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" @dismiss-popup="dismissPopup" />
    <div class="password-reset-form">
        <h1>Reset Password</h1>
        <p>Please enter your new password below.</p>
        <form @submit.prevent="resetPassword" class="form">
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required class="form-control">
            </div>
            <div class="form-group">
                <label for="confirmPassword">Confirm Password:</label>
                <input type="password" id="confirmPassword" v-model="confirmPassword" required class="form-control">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { API_BASE_URL } from '@/main';
import { useRouter } from 'vue-router';
import ShowNotification from '../components/ShowNotification.vue';

let password = ref('');
let confirmPassword = ref('');
let uidb64 = ref('');
let token = ref('');
const router = useRouter();

// Variables to display a notification
let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
let timerId = ref(null);

onMounted(() => {
    const urlParams = new URLSearchParams(window.location.search);
    uidb64.value = urlParams.get('uidb64');
    token.value = urlParams.get('token');
});

function dismissPopup() {
    showNotification.value = false;
    clearTimeout(timerId.value);
}

function displayPopup() {
    showNotification.value = true;
    timerId.value = setTimeout(() => {
        dismissPopup();
    }, 4000);
}
async function resetPassword() {
    if (password.value.length < 8 || password.value.length > 32) {
        backgroundColor.value = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = 'Error';
        notificationMessage.value = "Password length must be between 8 and 32 characters";
        displayPopup();
        return;
    }

    if (password.value !== confirmPassword.value) {
        backgroundColor.value = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = 'Error';
        notificationMessage.value = "Passwords do not match";
        displayPopup();
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}reset_password/${uidb64.value}/${token.value}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                password: password.value
            }),
        });

        if (response.status === 200) {
            backgroundColor.value = 'bg-green-200/[.89] border border-green-400';
            notificationTitle.value = 'Success';
            notificationMessage.value = 'Password reset successful! Redirecting...';
            displayPopup();

            setTimeout(() => {
                router.push({ name: 'login' })
            }, 3000);
        } else {
            const data = await response.json();
            backgroundColor.value = 'bg-red-200/[.89] border border-red-400';
            notificationTitle.value = 'Error';
            notificationMessage.value = data.error || 'An error occurred. Please try again.';
            displayPopup();
        }
    } catch (error) {
        backgroundColor.value = 'bg-red-200/[.89] border border-red-400';
        notificationTitle.value = 'Error';
        notificationMessage.value = error.message || 'An error occurred. Please try again.';
        displayPopup();
    }
}
</script>

<script>
export default {
    name: 'ResetPasswordForm',
}
</script>

<style scoped>
.password-reset-form {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
}

.password-reset-form h1 {
    font-size: 24px;
    margin-bottom: 20px;
}

.password-reset-form p {
    font-size: 16px;
    margin-bottom: 20px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    font-weight: bold;
}

.form-control {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
}

.btn {
    display: inline-block;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #007bff;
    color: #fff;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: #0056b3;
}
</style>