<template>
    <div class="flex items-center gap-4 p-4 border-t bg-white">
        <!-- Input field for user response -->
        <input
            type="text"
            v-model="userInput"
            placeholder="Type your response..."
            class="flex-1 p-2 border rounded-md focus:outline-none focus:ring focus:ring-blue-300"
        />
        <!-- Submit button -->
        <button
            @click="submitResponse"
            :disabled="!userInput.trim()"
            class="px-4 py-2 bg-blue-500 text-white text-sm font-medium rounded-md hover:bg-blue-600 disabled:bg-gray-300"
        >
            Send
        </button>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits(["response"]);

const userInput = ref("");

function submitResponse() {
    if (userInput.value.trim()) {
        emit("response", userInput.value.trim());
        userInput.value = "";
    }
}
</script>
