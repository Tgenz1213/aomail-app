<template>
    <li :class="wrapperClass" :aria-current="ariaCurrent">
        <div class="absolute inset-0 flex items-center" aria-hidden="true" v-if="!isLastStep">
            <div class="h-0.5 w-full bg-gray-500"></div>
        </div>
        <a @click="handleClick" :class="markerClass">
            <svg
                v-if="isCompleted"
                class="h-5 w-5 text-gray-700"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
            >
                <path
                    fill-rule="evenodd"
                    d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                    clip-rule="evenodd"
                />
            </svg>
            <span v-if="!isCompleted" :class="dotClass" aria-hidden="true"></span>
        </a>
    </li>
</template>

<script setup lang="ts">
import { computed, defineProps, defineEmits } from "vue";

const props = defineProps({
    isCurrentStep: { type: Boolean, default: false },
    isCompleted: { type: Boolean, default: false },
    isLastStep: { type: Boolean, default: false },
    onClick: Function,
});

const emits = defineEmits(["click"]);

const handleClick = (event: Event) => {
    if (props.onClick) {
        props.onClick(event);
    }
    emits("click", event);
};

const ariaCurrent = computed(() => {
    return props.isCurrentStep ? "step" : undefined;
});

const wrapperClass = computed(() => ["relative", !props.isLastStep ? "pr-6 sm:pr-16" : ""]);

const markerClass = computed(() => [
    "relative flex h-8 w-8 items-center justify-center rounded-full border-2",
    props.isCompleted ? "bg-white hover:bg-gray-200 border-gray-700" : "border-gray-700 bg-white",
    props.isCurrentStep ? "aria-current" : "group",
]);

const dotClass = computed(() => [
    "h-2.5 w-2.5 rounded-full",
    props.isCompleted ? "bg-gray-700" : props.isCurrentStep ? "bg-gray-700" : "bg-transparent group-hover:bg-gray-300",
]);
</script>
