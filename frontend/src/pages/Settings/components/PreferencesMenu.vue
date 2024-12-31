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
                            class="mb-4 w-full p-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
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
                                class="w-full border border-gray-300 bg-white rounded-md p-2 min-h-[150px] overflow-auto focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                :placeholder="$t('settingsPage.preferencesPage.signaturePlaceholder')"
                                @input="handleSignatureInput"
                                @paste.prevent="handlePaste"
                                @drop.prevent="handleDrop"
                            ></div>
                            <button
                                v-if="selectedSignature"
                                @click="updateSignature"
                                class="mt-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                {{ $t("settingsPage.preferencesPage.updateSignature") }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex-1 flex gap-x-10 w-full mt-6 h-full">
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
    </div>
</template>

<script setup lang="ts">
import { ref, inject, onMounted, watch, nextTick } from "vue";
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

const displayPopup = inject<Function>("displayPopup");

// Optional: For managing a selected image
// const selectedImage = ref<HTMLImageElement | null>(null);

onMounted(async () => {
    await fetchSignatures();
});

watch(selectedSignatureId, async () => {
    await loadSelectedSignature();
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

const loadSelectedSignature = async () => {
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
        await nextTick();
        placeCursorAtEnd();
    }
};

const handleSignatureInput = () => {
    if (signatureEditorRef.value) {
        editedSignatureContent.value = signatureEditorRef.value.innerHTML;
    }
};

const handlePaste = (event: ClipboardEvent) => {
    const items = event.clipboardData?.items;
    if (!items) return;

    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        if (item.type.indexOf("image") !== -1) {
            const file = item.getAsFile();
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const img = document.createElement("img");
                    img.src = e.target?.result as string;
                    insertImageAtCursor(img);
                };
                reader.readAsDataURL(file);
            }
        }
    }
};

const handleDrop = (event: DragEvent) => {
    const files = event.dataTransfer?.files;
    if (!files) return;

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (file.type.startsWith("image/")) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement("img");
                img.src = e.target?.result as string;
                img.alt = "Image insérée";
                insertImageAtCursor(img);
            };
            reader.readAsDataURL(file);
        }
    }
};

const insertImageAtCursor = (img: HTMLImageElement) => {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) return;

    const range = selection.getRangeAt(0);
    range.collapse(false);
    range.insertNode(img);
    editedSignatureContent.value = signatureEditorRef.value?.innerHTML || "";
    range.setStartAfter(img);
    range.setEndAfter(img);
    selection.removeAllRanges();
    selection.addRange(range);
};

// Optional : Method to delete a selected image
/*
const deleteSelectedImage = () => {
    if (selectedImage.value && signatureEditorRef.value) {
        selectedImage.value.remove();
        editedSignatureContent.value = signatureEditorRef.value.innerHTML;
        selectedImage.value = null;
    }
};

// Écouter les clics pour sélectionner une image
const handleEditorClick = (event: MouseEvent) => {
    const target = event.target as HTMLElement;
    if (target.tagName === "IMG") {
        selectedImage.value = target as HTMLImageElement;
    } else {
        selectedImage.value = null;
    }
};
*/

const updateSignature = async () => {
    console.log("selectedSignature.value", selectedSignature.value);
    if (!selectedSignature.value) return;

    const payload = {
        signature_id: selectedSignature.value.id,
        signature_content: editedSignatureContent.value,
    };

    try {
        const response = await putData(`user/signatures/update/`, payload);
        console.log("response", response);
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

const placeCursorAtEnd = () => {
    if (signatureEditorRef.value) {
        const range = document.createRange();
        const sel = window.getSelection();
        range.selectNodeContents(signatureEditorRef.value);
        range.collapse(false);
        sel?.removeAllRanges();
        sel?.addRange(range);
    }
};

onMounted(() => {
    if (signatureEditorRef.value) {
        // Additional mounted logic if needed
    }
});
</script>