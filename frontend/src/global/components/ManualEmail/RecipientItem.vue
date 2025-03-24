<template>
    <div v-if="people.length > 0" class="flex items-center mb-1 gap-2">
        <div
            v-for="person in people"
            :key="person.email"
            class="flex items-center gap-2 px-2 py-1 rounded-md bg-gray-50 border border-gray-200"
            :class="{
                'bg-red-50 border-red-200': isInvalid,
                'bg-green-50 border-green-200': isValid,
            }"
            v-tooltip="person.username ? person.email : ''"
        >
            <span v-if="type === 'cc'" class="font-semibold mr-1 2xl:mr-2">
                {{ $t("constants.sendEmailConstants.carbonCopyInitialsTwoDots") }}
            </span>
            <span v-if="type === 'bcc'" class="font-semibold mr-1 2xl:mr-2">
                {{ $t("constants.sendEmailConstants.blindCarbonCopyInitialsTwoDots") }}
            </span>
            {{ person.username || person.email }}

            <button @click="removePerson(person)" class="text-gray-400 hover:text-gray-600 focus:outline-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path
                        fill-rule="evenodd"
                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                        clip-rule="evenodd"
                    />
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
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
