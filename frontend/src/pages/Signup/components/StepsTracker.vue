<template>
    <nav>
        <ol role="list" class="flex items-center" v-if="step === 0">
            <StepMarker :isCurrentStep="true" />
            <StepMarker @onClick="goStepPreferencesForm" />
            <StepMarker />
            <StepMarker />
            <StepMarker :isLastStep="true" />
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 1">
            <StepMarker @onClick="goBackStepCredentialsForm" :isCompleted="true" />
            <StepMarker :isCurrentStep="true" />
            <StepMarker @onClick="goStepCategoriesForm" />
            <StepMarker />
            <StepMarker :isLastStep="true" />
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 2">
            <StepMarker @onClick="goBackStepCredentialsForm" :isCompleted="true" />
            <StepMarker @onClick="goBackStepPreferencesForm" :isCompleted="true" />
            <StepMarker :isCurrentStep="true" />
            <StepMarker @onClick="goStepLinkEmail" />
            <StepMarker :isLastStep="true" />
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 3">
            <StepMarker :isCompleted="true" />
            <StepMarker :isCompleted="true" />
            <StepMarker :isCompleted="true" />
            <StepMarker :isCurrentStep="true" />
            <StepMarker @onClick="goStepSignUpSummary" :isLastStep="true" />
        </ol>
        <ol role="list" class="flex items-center" v-if="step === 4">
            <StepMarker :isCompleted="true" />
            <StepMarker :isCompleted="true" />
            <StepMarker :isCompleted="true" />
            <StepMarker @onClick="goBackStepLinkEmail" :isCompleted="true" />
            <StepMarker @onClick="submitSignupData" :isCurrentStep="true" :isLastStep="true" />
        </ol>
    </nav>
</template>

<script setup lang="ts">
import { inject, ref, Ref } from "vue";
import StepMarker from "./StepMarker.vue";

const props = defineProps<{
    signUpPage: string;
}>();

const step = inject<Ref<number>>("step") || ref(props.signUpPage === "linkEmail" ? 3 : 0);

const goBackStepCredentialsForm = () => {
    step.value = 0;
};
const goBackStepPreferencesForm = () => {
    step.value = 1;
};
const goBackStepLinkEmail = () => {
    step.value = 3;
};

const goStepSignUpSummary = inject<() => void>("goStepSignUpSummary");
const submitSignupData = inject<() => void>("submitSignupData");
const goStepCategoriesForm = inject<() => void>("goStepCategoriesForm");
const goStepPreferencesForm = inject<() => void>("goStepPreferencesForm");
const goStepLinkEmail = inject<() => void>("goStepLinkEmail");
</script>
