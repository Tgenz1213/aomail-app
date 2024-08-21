<template>
    <div v-if="people.length > 0" class="flex items-center mb-1">
        <div
            v-for="person in people"
            :key="person.email"
            class="relative flex items-center bg-gray-200 rounded px-2 py-1 mr-1 2xl:px-3 2xl:py-2 2xl:mr-2"
            v-tooltip="person.username ? person.email : ''"
        >
            <span v-if="type === 'cc'" class="font-semibold mr-1 2xl:mr-2">
                {{ $t("constants.sendEmailConstants.carbonCopyInitialsTwoDots") }}
            </span>
            <span v-if="type === 'cci'" class="font-semibold mr-1 2xl:mr-2">
                {{ $t("constants.sendEmailConstants.blindCarbonCopyInitialsTwoDots") }}
            </span>
            {{ person.username || person.email }}

            <button
                @click="removePerson(person)"
                class="ml-2 text-gray-500 hover:text-red-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 rounded-full p-1 transition-colors duration-300"
                aria-label="Remove file"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="2"
                    stroke="currentColor"
                    class="w-4 h-4"
                >
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineExpose, ref, watch } from "vue";
import tippy, { Instance } from "tippy.js";
import "tippy.js/dist/tippy.css";
import { Recipient } from "@/global/types";

interface Props {
    people: Recipient[];
    type: string;
    removePerson: (person: Recipient) => void;
}

const props = defineProps<Props>();

interface TippyElement extends HTMLElement {
    _tippy?: Instance;
}

const localPeople = ref<Recipient[]>([...props.people]);

watch(
    () => props.people,
    (newPeople) => {
        localPeople.value = [...newPeople];
    },
    { deep: true }
);

const vTooltip = {
    mounted(el: TippyElement, binding: { value: string }) {
        if (binding.value) {
            el._tippy = tippy(el, {
                content: binding.value,
                placement: "top",
                arrow: true,
                theme: "light",
            });
        }
    },
    updated(el: TippyElement, binding: { value: string }) {
        if (el._tippy) {
            el._tippy.setContent(binding.value);
        }
    },
    unmounted(el: TippyElement) {
        if (el._tippy) {
            el._tippy.destroy();
        }
    },
};

defineExpose({ directives: { tooltip: vTooltip } });

function removePerson(person: Recipient) {
    localPeople.value = localPeople.value.filter((p) => p.email !== person.email);
    props.removePerson(person);
}
</script>
