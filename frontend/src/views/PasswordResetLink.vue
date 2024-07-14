<template>
    <ShowNotification :showNotification="showNotification" :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage" :backgroundColor="backgroundColor" @dismiss-popup="dismissPopup" />
    <div class="password-reset-form">
        <h1>Reset Password</h1>
        <p>Please enter your email address below. We will send you a link to reset your password.
            your password.</p>
        <form @submit.prevent="generateResetLink" class="form">
            <div class="form-group">
                <label for="email">E-mail address :</label>
                <input type="email" id="email" v-model="email" required class="form-control">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</template>


<!--  TODO change the name of that file as it is absolutely not relevant - It must be stricly: PasswordResetLink.vue -->

<script setup>
import { ref } from 'vue';
import { API_BASE_URL } from '@/main';
import { useRouter } from 'vue-router';
import ShowNotification from '../components/ShowNotification.vue';

let email = ref('');
const router = useRouter();
// Variables to display a notification
let showNotification = ref(false);
let notificationTitle = ref('');
let notificationMessage = ref('');
let backgroundColor = ref('');
let timerId = ref(null);


function dismissPopup() {
    showNotification.value = false;
    // Cancel the timer
    clearTimeout(timerId.value);
}
function displayPopup() {
    showNotification.value = true;

    timerId.value = setTimeout(() => {
        dismissPopup();
    }, 4000);
}

async function generateResetLink() {
    try {
        console.log(email.value)
        const response = await fetch(`${API_BASE_URL}generate_reset_token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email.value
            }),
        });

        console.log(response)

        if (response.message === 'Email sent successfully!') {
            // Show the pop-up
            backgroundColor = 'bg-green-200/[.89] border border-green-400';
            notificationTitle = 'Check your mailbox!';
            notificationMessage = 'Redirecting...';
            displayPopup();

            setTimeout(() => {
                router.push({ name: 'home' })
            }, 3000);
        } else {
            // Show the pop-up
            backgroundColor = 'bg-red-200/[.89] border border-red-400';
            notificationTitle = 'Error sending password reset email';
            notificationMessage = response.error;
            displayPopup();
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor = 'bg-red-200/[.89] border border-red-400';
        notificationTitle = 'Error sending password reset email';
        notificationMessage = error.message;
        displayPopup();
    }
}
</script>

<script>
export default {
    name: 'PasswordResetLink',
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