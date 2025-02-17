<template>
    <li
        class="flex flex-row p-8 bg-white border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 relative"
    >
        <div class="absolute top-2 right-2 flex items-center space-x-2">
            <input type="checkbox" class="h-4 w-4" :checked="isSelected" @change="toggleSelection" />
            <button type="button" class="bg-red-600 rounded-full p-1 text-white hover:bg-red-700" @click="deleteLabel">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="w-4 h-4"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                    />
                </svg>
            </button>
        </div>
        <div class="flex-grow grid grid-cols-4 gap-4 items-center text-center">
            <span>{{ label.itemName }}</span>
            <span>{{ label.postageDeadlineDate }} {{ label.postageDeadlineTime }}</span>
            <span>{{ carrierNames[label.carrier] || label.carrier }}</span>
            <span>{{ label.platform }}</span>
        </div>
    </li>
</template>

<script setup lang="ts">
import { inject, Ref, ref, computed } from "vue";
import { LabelData } from "../utils/types";
import { deleteData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";

const selectedLabelIds = inject<Ref<number[]>>("selectedLabelIds") || ref([]);
const labelsData = inject<Ref<LabelData[]>>("labelsData") || ref<LabelData[]>([]);
const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

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

const deleteLabel = async () => {
    const index = labelsData.value.findIndex((label) => label.id === props.label.id);

    if (index !== -1) {
        labelsData.value.splice(index, 1);
    }

    const result = await deleteData("user/delete_labels", { ids: [props.label.id] });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.failedToDeleteLabel"),
            result.error as string
        );
    }
};
</script>
