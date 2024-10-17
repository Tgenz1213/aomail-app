<template>
    <div v-if="stepContainer == 1" class="flex justify-end m-3 2xl:m-5">
        <div class="flex mt-4 space-x-4 items-center">
            <div>
                <select
                    id="lengthSelect"
                    class="h-10 px-8 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white focus:bg-gray-900 focus:text-white border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900"
                    v-model="selectedLength"
                >
                    <option v-for="option in emailLengthOptions" :key="option.key" :value="option.key">
                        {{ option.value }}
                    </option>
                </select>
            </div>
            <div>
                <select
                    id="formalitySelect"
                    class="h-10 px-8 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white focus:bg-gray-900 focus:text-white border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900"
                    v-model="selectedFormality"
                >
                    <option v-for="option in formalityOptions" :key="option.key" :value="option.key">
                        {{ option.value }}
                    </option>
                </select>
            </div>
            <div class="flex items-center">
                <button
                    @click="handleAIClick"
                    type="button"
                    class="2xl:w-[100px] w-[100px] rounded-md bg-gray-700 px-6 py-2.5 2xl:px-6 2xl:py-3 text-sm 2xl:text-base text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                >
                    {{ $t("constants.userActions.ask") }}
                </button>
            </div>
        </div>
    </div>
    <div v-else class="flex justify-end m-3 2xl:m-5">
        <button
            @click="handleAIClick"
            type="button"
            class="2xl:w-[100px] w-[80px] rounded-md bg-gray-700 px-5.5 py-2.5 2xl:px-6.5 2xl:py-3 2xl:text-base text-sm text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
        >
            {{ $t("constants.userActions.ask") }}
        </button>
    </div>
</template>

<script setup lang="ts">
import { i18n } from "@/global/preferences";
import { KeyValuePair } from "@/global/types";
import { inject, Ref, ref } from "vue";

const stepContainer = inject<Ref<number>>("stepContainer") || ref(0);
const selectedFormality = inject<Ref<string>>("selectedFormality") || ref("");
const selectedLength = inject<Ref<string>>("selectedLength") || ref("");

const handleAIClick = inject<() => void>("handleAIClick");

const emailLengthOptions: KeyValuePair[] = [
    { key: "very short", value: i18n.global.t("newPage.veryBrief") },
    { key: "short", value: i18n.global.t("newPage.brief") },
    { key: "long", value: i18n.global.t("newPage.long") },
];

const formalityOptions: KeyValuePair[] = [
    { key: "very informal", value: i18n.global.t("newPage.informal") },
    { key: "formal", value: i18n.global.t("newPage.formal") },
    { key: "very formal", value: i18n.global.t("newPage.veryFormal") },
];
</script>
