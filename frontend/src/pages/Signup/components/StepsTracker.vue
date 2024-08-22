<template>
    <nav>
        <ol role="list" class="flex items-center" v-if="step === 0">
            <StepMarker :isCurrentStep="true" @onClick="goStepPreferencesForm" />
            <StepMarker @onClick="goStepPreferencesForm" />
            <StepMarker @onClick="goStepCategoriesForm" />
            <StepMarker />
            <StepMarker :isLastStep="true" />
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 1">
            <StepMarker @onClick="geStepCredentialsForm" :isCompleted="true" />
            <StepMarker :isCurrentStep="true" />
            <StepMarker @onClick="goStepCategoriesForm" />
            <StepMarker />
            <StepMarker :isLastStep="true" />
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 2">
            <StepMarker @onClick="geStepCredentialsForm" :isCompleted="true" />
            <StepMarker @onClick="goStepPreferencesForm" :isCompleted="true" />
            <StepMarker :isCurrentStep="true" />
            <StepMarker @onClick="submitSignupData" />
            <StepMarker :isLastStep="true" />
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 3">
            <StepMarker />
            <StepMarker />
            <StepMarker />
            <StepMarker />
            <StepMarker :isLastStep="true" />
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 4">
            <StepMarker />
            <StepMarker />
            <StepMarker />
            <StepMarker />
            <StepMarker :isLastStep="true" />
        </ol>
    </nav>
</template>

<script setup lang="ts">
import { inject, onMounted, ref, Ref } from "vue";
import StepMarker from "./StepMarker.vue";

const props = defineProps<{
    signUpPage: string;
}>();

const step = inject<Ref<number>>("step") || ref(0);

function geStepCredentialsForm() {
    // step.value = 0;
}

function goStepPreferencesForm() {
    // step.value = 1;
}

function goStepCategoriesForm() {
    // step.value = 2;
}

function submitSignupData() {
    // step.value = 3;
}

onMounted(() => {
    if (props.signUpPage == "signUp") {
        step.value = 0;
    }
});
</script>
