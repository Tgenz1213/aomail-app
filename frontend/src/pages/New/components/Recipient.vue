<template>
    <div v-if="people.length > 0" class="flex items-center mb-1">
        <div
            v-for="person in people"
            :key="person.email"
            class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1 2xl:px-3 2xl:py-2 2xl:mr-2"
        >
            <span v-if="type === 'cc'" class="font-semibold mr-1 2xl:mr-2">
                {{ $t("constants.sendEmailConstants.carbonCopyInitialsTwoDots") }}
            </span>
            <span v-if="type === 'cci'" class="font-semibold mr-1 2xl:mr-2">
                {{ $t("constants.sendEmailConstants.blindCarbonCopyInitialsTwoDots") }}
            </span>
            {{ person.username || person.email }}
            <button @click="() => removePerson(person)">×</button>
        </div>
    </div>
</template>

<script setup>
defineProps(["people", "type", "removePerson"]);
</script>
