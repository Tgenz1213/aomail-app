<template>
    <div class="recipients-container overflow-y-auto max-h-32 flex flex-wrap">
        <RecipientItem :people="selectedPeople" :type="'main'" :removePerson="removePersonFromMain" />
        <RecipientItem :people="selectedCC" :type="'cc'" :removePerson="removePersonFromCC" />
        <RecipientItem :people="selectedBCC" :type="'cci'" :removePerson="removePersonFromCCI" />
    </div>
    <RecipientInputRow />
</template>

<script setup lang="ts">
import { inject, Ref, ref } from "vue";
import RecipientItem from "./RecipientItem.vue";
import RecipientInputRow from "./RecipientInputRow.vue";
import { Recipient } from "@/global/types";

const selectedPeople = inject<Ref<Recipient[]>>("selectedPeople") || ref([]);
const selectedCC = inject<Ref<Recipient[]>>("selectedCC") || ref([]);
const selectedBCC = inject<Ref<Recipient[]>>("selectedBCC") || ref([]);

function removePersonFromMain(personToRemove: Recipient) {
    selectedPeople.value = selectedPeople.value.filter((person) => person !== personToRemove);
}

function removePersonFromCC(personToRemove: Recipient) {
    selectedCC.value = selectedCC.value.filter((person) => person !== personToRemove);
}

function removePersonFromCCI(personToRemove: Recipient) {
    selectedBCC.value = selectedBCC.value.filter((person) => person !== personToRemove);
}
</script>
