<template>
    <div>
        <h1>{{ $t("errorWebPagesTemplates.error401Page.youAreNotConnected") }}</h1>
        <p>
            {{ $t("errorWebPagesTemplates.error401Page.redirectionToLogin") }}
            {{ countdown }} seconds
        </p>
    </div>
</template>

<script setup>
import { useRedirectCountdown } from "@/global/security"
const { countdown, startCountdown } = useRedirectCountdown("login", 5)

startCountdown()
</script>
