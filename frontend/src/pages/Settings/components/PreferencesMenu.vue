<template>
    <div class="mx-auto w-full h-full px-8 2xl:px-12 pt-10">
        <div class="flex flex-col h-full pb-6">
            <div class="flex gap-x-10 w-full">
                <div class="flex-1 flex flex-col">
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
                    <div class="pt-10 pb-10">
                        <LanguageSelection />
                    </div>
                </div>
                <div class="flex-1 flex flex-col">
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
                    <div class="pt-10 pb-10">
                        <ThemeSelection />
                    </div>
                </div>
            </div>
            <div class="flex gap-x-10 w-full mt-6">
                <div class="flex-1 flex flex-col">
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
                    <div class="pt-10 pb-10">
                        <TimeZoneSelection />
                    </div>
                </div>
            </div>
            <div class="flex gap-x-10 w-full mt-6">
                <div class="flex-1 flex flex-col">
                    <div class="relative">
                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                            <div class="w-full border-t border-gray-300"></div>
                        </div>
                        <div class="relative flex justify-center">
                            <span class="bg-white px-2 text-sm text-gray-500">
                                {{ $t("settingsPage.preferencesPage.signatureManagement") }}
                            </span>
                        </div>
                    </div>
                    <div class="pt-10 pb-10">
                        <select
                            v-model="selectedSignatureId"
                            class="mb-4 w-full p-2 border rounded-md"
                            @change="loadSelectedSignature"
                        >
                            <option disabled value="">{{ $t("settingsPage.preferencesPage.signaturePlaceholder") }}</option>
                            <option v-for="signature in signatures" :key="signature.id" :value="signature.id">
                                {{ signature.name || `Signature ${signature.id}` }}
                            </option>
                        </select>
                        <div v-if="selectedSignature" class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                {{ $t("settingsPage.preferencesPage.editSignature") }}
                            </label>
                            <div
                                ref="signatureEditorRef"
                                contenteditable="true"
                                class="w-full border rounded p-2 min-h-[150px] overflow-auto"
                                :placeholder="$t('settingsPage.preferencesPage.signaturePlaceholder')"
                                @input="handleSignatureInput"
                            >{{ editedSignatureContent }}</div>
                        </div>
                        <button
                            v-if="selectedSignature"
                            @click="updateSignature"
                            class="mt-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                        >
                            {{ $t("settingsPage.preferencesPage.updateSignature") }}
                        </button>
                    </div>
                </div>
            </div>
            <div
                class="flex-1 w-full h-full rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 text-center mt-6"
            >
                <div class="flex flex-col h-full items-center justify-center">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke-width="1"
                        stroke="currentColor"
                        class="w-12 h-12 mx-auto text-gray-400"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M11.42 15.17L17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 0 0 4.486-6.336l-3.276 3.277a3.004 3.004 0 0 1-2.25-2.25l3.276-3.276a4.5 4.5 0 0 0-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085M9.117 19.125h.008v.008H9.117v-.008Z"
                        />
                    </svg>
                    <span class="mt-2 block text-sm font-semibold text-gray-900">
                        {{ $t("constants.underDevelopment") }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { getData, putData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";

import TimeZoneSelection from "@/pages/Settings/components/TimeZoneSelection.vue";
import LanguageSelection from "@/pages/Settings/components/LanguageSelection.vue";
import ThemeSelection from "@/pages/Settings/components/ThemeSelection.vue";

const signatures = ref<any[]>([]);
const selectedSignatureId = ref<string>("");
const selectedSignature = ref<any>(null);
const editedSignatureContent = ref<string>("");

const signatureEditorRef = ref<HTMLElement | null>(null);

onMounted(async () => {
    await fetchSignatures();
});

watch(selectedSignatureId, () => {
    loadSelectedSignature();
});

const fetchSignatures = async () => {
    const result = await getData("user/signatures/");
    if (result.success) {
        signatures.value = result.data;
    } else {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.preferencesPage.fetchFailed") as string,
            result.error as string
        );
    }
};

const loadSelectedSignature = () => {
    if (!selectedSignatureId.value) {
        selectedSignature.value = null;
        editedSignatureContent.value = "";
        if (signatureEditorRef.value) {
            signatureEditorRef.value.innerHTML = "";
        }
        return;
    }
    const sig = signatures.value.find(sig => sig.id === selectedSignatureId.value);
    if (sig) {
        selectedSignature.value = sig;
        editedSignatureContent.value = sig.signature_content;
        if (signatureEditorRef.value) {
            signatureEditorRef.value.innerHTML = sig.signature_content;
        }
    }
};

const handleSignatureInput = (event: Event) => {
    const target = event.target as HTMLElement;
    editedSignatureContent.value = target.innerHTML;
};

const updateSignature = async () => {
    if (!selectedSignature.value) return;

    const payload = {
        id: selectedSignature.value.id,
        signature_content: editedSignatureContent.value,
    };

    try {
        const response = await putData(`user/signatures/update/${selectedSignature.value.id}/`, payload);
        if (response.success) {
            const index = signatures.value.findIndex(sig => sig.id === response.data.id);
            if (index !== -1) {
                signatures.value[index] = response.data;
            }
            displayPopup?.(
                "success",
                i18n.global.t("settingsPage.preferencesPage.updateSuccess") as string,
                i18n.global.t("settingsPage.preferencesPage.updateSuccess") as string
            );
        } else {
            displayPopup?.(
                "error",
                i18n.global.t("settingsPage.preferencesPage.updateError") as string,
                response.error || i18n.global.t("settingsPage.preferencesPage.updateError") as string
            );
        }
    } catch (error) {
        displayPopup?.(
            "error",
            i18n.global.t("settingsPage.preferencesPage.updateError") as string,
            i18n.global.t("settingsPage.preferencesPage.updateError") as string
        );
    }
};

const displayPopup = (type: "success" | "error", title: string, message: string) => {
    console.log(`[${type.toUpperCase()}] ${title}: ${message}`);
};
</script>