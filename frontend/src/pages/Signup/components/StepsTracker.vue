<template>
    <nav>
        <ol role="list" class="flex items-center" v-if="step === 0">
            <StepMarker :isCurrentStep="true" />
            <StepMarker @onClick="goStepLinkEmail" />
            <StepMarker :isLastStep="true" />
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 1">
            <StepMarker @onClick="goBackStepCredentialsForm" :isCompleted="true" />
            <StepMarker @onClick="submitSignupData" :isCurrentStep="true" />
            <StepMarker :isLastStep="true" />
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 2">
            <StepMarker :isCompleted="true" />
            <StepMarker :isCompleted="true" />
            <StepMarker :isLastStep="true" />
        </ol>
    </nav>
</template>

<script setup lang="ts">
import { inject, ref, Ref } from "vue";
import StepMarker from "./StepMarker.vue";

const props = defineProps<{
    signUpPage: string;
}>();

const step = inject<Ref<number>>("step") || ref(props.signUpPage === "linkEmail" ? 1 : 0);

const goBackStepCredentialsForm = () => {
    step.value = 0;
};

const submitSignupData = inject<() => void>("submitSignupData");
const goStepLinkEmail = inject<() => void>("goStepLinkEmail");
</script>
