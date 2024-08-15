<template></template>

<script setup lang="ts">
import { inject } from "vue";
const displayMessage = inject<(message: string, aiIcon: string) => Promise<void>>("displayMessage");
const aiIcon = inject<string>("aiIcon") || "";
</script>
