<template>
    <div class="flex items-start mb-4" :class="{ 'flex-row-reverse': isUser }">
        <!-- User or AI avatar -->
        <img v-if="isUser" :src="userImage" alt="User" class="w-10 h-10 rounded-full" />
        <img v-else :src="logoAomail" alt="AI" class="w-10 h-10 rounded-full" />

        <!-- Chat bubble -->
        <div
            :class="[
                'px-4 py-3 rounded-xl text-sm max-w-xs',
                isUser ? 'bg-blue-500 text-white ml-2' : 'bg-green-100 text-gray-800 mr-2',
            ]"
            :style="isUser ? 'border-top-right-radius: 0.5rem;' : 'border-top-left-radius: 0.5rem;'"
        >
            {{ message }}
        </div>
    </div>
</template>

<script setup lang="ts">
import userImage from "@/assets/user.png";
import logoAomail from "@/assets/logo-aomail.png";

defineProps({
    message: String,
    isUser: Boolean,
});
</script>
