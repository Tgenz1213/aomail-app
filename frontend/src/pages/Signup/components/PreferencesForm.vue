<template>
    <div class="flex flex-col">
        <div class="relative">
            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center">
                <span class="bg-white px-2 text-sm text-gray-500">
                    {{ $t("constants.language") }}
                </span>
            </div>
        </div>
        <div class="pt-2 pb-10">
            <div class="relative items-stretch mt-2">
                <LanguageSelection />
            </div>
        </div>

        <div class="relative">
            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center">
                <span class="bg-white px-2 text-sm text-gray-500">
                    {{ $t("constants.timezone") }}
                </span>
            </div>
        </div>
        <div class="pt-2 pb-10">
            <div class="relative items-stretch mt-2">
                <TimeZoneSelection />
            </div>
        </div>

        <div class="relative">
            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center">
                <span class="bg-white px-2 text-sm text-gray-500">
                    {{ $t("constants.theme") }}
                </span>
            </div>
        </div>
        <div class="pt-2 pb-10">
            <div class="relative items-stretch mt-2">
                <ThemeSelection />
            </div>
        </div>
    </div>
    <div>
        <div class="pt-2">
            <button
                @click.prevent="goStepCategories"
                class="flex w-full justify-center rounded-md bg-gray-800 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800"
            >
                {{ $t("signUpPart1Page.continue") }}
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import LanguageSelection from "./LanguageSelection.vue";
import TimeZoneSelection from "./TimeZoneSelection.vue";
import ThemeSelection from "./ThemeSelection.vue";
import { inject } from "vue";

const goStepCategories = inject<() => void>("goStepCategories");
</script>
