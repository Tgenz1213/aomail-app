<template>
    <li
        class="flex flex-col p-4 bg-white border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 relative"
    >
        <input type="checkbox" class="absolute top-2 right-2 h-4 w-4" :checked="isSelected" @change="toggleSelection" />
        <div class="text-gray-700 mb-2">
            <strong>Item Name:</strong>
            {{ label.itemName }}
        </div>
        <div class="text-gray-700 mb-2">
            <strong>Postage Deadline:</strong>
            {{ label.postageDeadlineDate }} {{ label.postageDeadlineTime }}
        </div>
        <div class="text-gray-700 mb-2">
            <strong>Carrier:</strong>
            {{ carrierNames[label.carrier] || label.carrier }}
        </div>
        <div class="text-gray-700 mb-2">
            <strong>Platform:</strong>
            {{ label.platform }}
        </div>
    </li>
</template>

<script setup lang="ts">
import { defineProps, inject, Ref, ref, computed } from "vue";
import { LabelData } from "../utils/types";

const selectedLabelIds = inject<Ref<number[]>>("selectedLabelIds") || ref([]);

const carrierNames: Record<string, string> = {
    mondial_relay: "Mondial Relay",
    ups: "UPS",
    la_poste: "La Poste",
    chronopost: "Chronopost",
    relais_colis: "Relais Colis",
};

const props = defineProps<{
    label: LabelData;
}>();

const isSelected = computed(() => selectedLabelIds.value.includes(props.label.id));

const toggleSelection = () => {
    if (isSelected.value) {
        selectedLabelIds.value = selectedLabelIds.value.filter((id) => id !== props.label.id);
    } else {
        selectedLabelIds.value.push(props.label.id);
    }
};
</script>
