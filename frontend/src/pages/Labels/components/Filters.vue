<template>
    <div class="relative">
        <div v-if="isOpen" class="absolute left-0 right-0 z-50">
            <div class="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
                <div class="space-y-4">
                    <h2 class="text-lg font-semibold mb-4">Advanced Filters</h2>
                    <div class="mb-4">
                        <label for="platform" class="block text-sm font-medium text-gray-700">Platform</label>
                        <input
                            id="platform"
                            v-model="platform"
                            type="text"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                        />
                    </div>
                    <div class="mb-4">
                        <label for="itemName" class="block text-sm font-medium text-gray-700">Item Name</label>
                        <input
                            id="itemName"
                            v-model="itemName"
                            type="text"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                        />
                    </div>
                    <div class="mb-4">
                        <label for="carrier" class="block text-sm font-medium text-gray-700">Carrier</label>
                        <input
                            id="carrier"
                            v-model="carrier"
                            type="text"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                        />
                    </div>
                    <div class="mb-4">
                        <label for="postageDeadline" class="block text-sm font-medium text-gray-700">
                            Postage Deadline
                        </label>
                        <Datepicker v-model="postageDeadline" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, inject, Ref } from "vue";
import Datepicker from "@vuepic/vue-datepicker";

const platform = inject<Ref<string>>("platform") || ref("");
const itemName = inject<Ref<string>>("itemName") || ref("");
const carrier = inject<Ref<string>>("carrier") || ref("");
const postageDeadline = inject<Ref<Date | undefined>>("postageDeadline") || ref<Date | undefined>(undefined);

defineProps<{
    isOpen: boolean;
}>();
</script>
