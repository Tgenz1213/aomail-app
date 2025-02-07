<template>
    <div class="flex justify-center">
        <div class="w-full max-w-5xl">
            <div class="flex items-start mb-4" :class="{ 'flex-row-reverse': isUser }">
                <!-- User message -->
                <template v-if="isUser">
                    <div class="max-w-2xl">
                        <div class="flex items-start gap-x-3 justify-end">
                            <div class="bg-blue-100 border border-blue-200 p-4 rounded-lg">
                                <p class="text-gray-800" v-html="message"></p>
                            </div>
                            <span class="inline-flex h-12 w-12 items-center justify-center rounded-full flex-shrink-0">
                                <img :src="userImage" alt="User" class="h-12 w-12 rounded-full object-cover" />
                            </span>
                        </div>
                    </div>
                </template>

                <!-- AI message -->
                <template v-else>
                    <div class="mr-3 flex-shrink-0">
                        <span
                            class="inline-flex h-12 w-12 items-center justify-center rounded-full bg-gray-900 text-white"
                        >
                            <img
                                :src="`${API_BASE_URL}agent_icon/${agentIcon}`"
                                alt="Agent Icon"
                                class="h-12 w-12 rounded-full object-cover"
                            />
                        </span>
                    </div>
                    <div class="flex flex-col bg-white rounded-lg p-4 max-w-2xl border border-gray-200">
                        <p v-html="message" class="text-gray-800"></p>
                    </div>
                </template>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import userImage from "@/assets/user.png";
import { API_BASE_URL } from "@/global/const";

// Add these new props
defineProps({
    message: String,
    isUser: Boolean,
    agentIcon: {
        type: String,
        required: true,
    },
});
</script>
