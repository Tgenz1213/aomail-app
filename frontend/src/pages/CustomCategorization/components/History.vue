<template>
    <div class="p-4 bg-gray-100 w-full md:w-80 h-screen overflow-y-auto border-l">
        <h2 class="text-xl font-semibold mb-4">Chat History Overview</h2>

        <!-- User Description Chat History -->
        <div class="mb-6">
            <h3 class="text-lg font-medium text-gray-800 mb-2">User Description</h3>
            <div v-for="(message, index) in userDescriptionMessages" :key="index" class="mb-2">
                <div :class="['p-2 rounded-md', message.isUser ? 'bg-blue-500 text-white' : 'bg-gray-300']">
                    <p>{{ message.text }}</p>
                </div>
            </div>
        </div>

        <!-- User Categories Chat History -->
        <div class="mb-6">
            <h3 class="text-lg font-medium text-gray-800 mb-2">User Categories</h3>
            <div v-for="(message, index) in userCategoriesMessages" :key="index" class="mb-2">
                <div :class="['p-2 rounded-md', message.isUser ? 'bg-blue-500 text-white' : 'bg-gray-300']">
                    <p>{{ message.text }}</p>
                </div>
            </div>
        </div>

        <!-- User Prioritization Chat History -->
        <div class="mb-6">
            <h3 class="text-lg font-medium text-gray-800 mb-2">User Prioritization</h3>
            <div v-for="(message, index) in userPrioritizationMessages" :key="index" class="mb-2">
                <div :class="['p-2 rounded-md', message.isUser ? 'bg-blue-500 text-white' : 'bg-gray-300']">
                    <p>{{ message.text }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const userDescriptionMessages = ref([
    {
        text: "Hello and welcome to the categorization customization feature! By default, you are using predefined guidelines. You can change them, and I am here to help you with that.",
        isUser: false,
    },
    { text: "Do you like your current email categorization?", isUser: false },
    { text: "No", isUser: true },
    { text: "Okay, let's improve that!", isUser: false },
]);

const userCategoriesMessages = ref([
    {
        text: "Let's talk about how you want your emails to be categorized. I can help with that.",
        isUser: false,
    },
    { text: "I want to categorize my emails based on importance and subject.", isUser: true },
    { text: "Got it! Let's set that up for you.", isUser: false },
]);

const userPrioritizationMessages = ref([
    { text: "Now, let's prioritize your emails.", isUser: false },
    { text: "I want urgent emails to come first, then the rest.", isUser: true },
    { text: "Great, we'll set that priority for you.", isUser: false },
]);
</script>
