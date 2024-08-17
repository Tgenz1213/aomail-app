<template>
    <div class="flex flex-wrap">
        <Recipient :people="selectedPeople" :type="'main'" :removePerson="removePersonFromMain" />
        <Recipient :people="selectedCC" :type="'cc'" :removePerson="removePersonFromCC" />
        <Recipient :people="selectedCCI" :type="'cci'" :removePerson="removePersonFromCCI" />
    </div>
</template>

<script setup>
import Recipient from "./Recipient.vue";
defineProps([
    "selectedPeople",
    "selectedCC",
    "selectedCCI",
    "removePersonFromMain",
    "removePersonFromCC",
    "removePersonFromCCI",
]);


</script>
