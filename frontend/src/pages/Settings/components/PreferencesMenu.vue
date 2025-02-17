<template>
    <div class="flex-1 h-full">
        <div class="h-full w-full flex items-center justify-center">
            <div class="flex gap-x-10 h-full w-full py-10 px-8 2xl:py-14 2xl:px-12">
                <div class="flex-1 flex-col h-full flex-grow px-4">
                    <div class="relative">
                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                            <div class="w-full border-t border-gray-300"></div>
                        </div>
                        <div class="relative flex justify-center">
                            <span class="bg-gray-100/70 px-4 py-1 text-md text-gray-600 rounded-full backdrop-blur-sm">
                                {{ $t("constants.language") }}
                            </span>
                        </div>
                    </div>
                    <div class="pt-8">
                        <LanguageSelection />
                    </div>

                    <div class="flex-col flex-grow w-full py-12 2xl:py-20">
                        <div class="relative">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t border-gray-300"></div>
                            </div>
                            <div class="relative flex justify-center">
                                <span class="bg-gray-100/70 px-4 py-1 text-md text-gray-600 rounded-full backdrop-blur-sm">
                                    {{ $t("constants.timezone") }}
                                </span>
                            </div>
                        </div>
                        <div class="pt-8">
                            <TimeZoneSelection />
                        </div>
                    </div>

                    <div class="flex-col flex-grow w-full">
                        <div class="relative">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t border-gray-300"></div>
                            </div>
                            <div class="relative flex justify-center">
                                <span class="bg-gray-100/70 px-4 py-1 text-md text-gray-600 rounded-full backdrop-blur-sm">
                                    E-commerce (Vinted)
                                </span>
                            </div>
                        </div>
                        <div class="pt-8 flex justify-center">
                            <a href="/labels" class="rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600">
                                Shipping Labels
                            </a>
                        </div>
                    </div>
                </div>

                <div class="flex-1 flex-col h-full flex-grow px-4">
                    <div class="relative">
                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                            <div class="w-full border-t border-gray-300"></div>
                        </div>
                        <div class="relative flex justify-center">
                            <span class="bg-gray-100/70 px-4 py-1 text-md text-gray-600 rounded-full backdrop-blur-sm">
                                {{ $t("constants.theme") }}
                            </span>
                        </div>
                    </div>
                    <div class="pt-8">
                        <ThemeSelection />
                    </div>

                    <div class="flex-col flex-grow w-full py-12 2xl:py-20">
                        <div class="relative">
                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                <div class="w-full border-t border-gray-300"></div>
                            </div>
                            <div class="relative flex justify-center">
                                <span class="bg-gray-100/70 px-4 py-1 text-md text-gray-600 rounded-full backdrop-blur-sm">
                                    {{ $t("settingsPage.preferencesPage.signatureManagement") }}
                                </span>
                            </div>
                        </div>
                        <div class="pt-8">
                            <Listbox v-model="selectedSignatureId" @update:modelValue="loadSelectedSignature">
                                <div class="relative mt-1">
                                    <ListboxButton
                                        class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6"
                                    >
                                        <span class="block truncate">
                                            {{
                                                selectedSignature
                                                    ? selectedSignature.name || `Signature ${selectedSignature.id}`
                                                    : $t("settingsPage.preferencesPage.signaturePlaceholder")
                                            }}
                                        </span>
                                        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                            <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                                        </span>
                                    </ListboxButton>

                                    <transition
                                        leave-active-class="transition ease-in duration-100"
                                        leave-from-class="opacity-100"
                                        leave-to-class="opacity-0"
                                    >
                                        <ListboxOptions
                                            class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                                        >
                                            <ListboxOption
                                                v-for="signature in signatures"
                                                :key="signature.id"
                                                :value="signature.id"
                                                as="template"
                                                v-slot="{ active, selected }"
                                            >
                                                <li
                                                    :class="[
                                                        active ? 'bg-gray-800 text-white' : 'text-gray-900',
                                                        'relative cursor-default select-none py-2 pl-3 pr-9',
                                                    ]"
                                                >
                                                    <span
                                                        :class="[
                                                            selected ? 'font-semibold' : 'font-normal',
                                                            'block truncate',
                                                        ]"
                                                    >
                                                        {{ signature.name || `Signature ${signature.id}` }}
                                                    </span>
                                                    <span
                                                        v-if="selected"
                                                        :class="[
                                                            active ? 'text-white' : 'text-gray-500',
                                                            'absolute inset-y-0 right-0 flex items-center pr-4',
                                                        ]"
                                                    >
                                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                                    </span>
                                                </li>
                                            </ListboxOption>
                                        </ListboxOptions>
                                    </transition>
                                </div>
                            </Listbox>

                            <div v-if="selectedSignature" class="mt-4">
                                <label class="block text-sm font-medium text-gray-700 mb-2">
                                    {{ $t("settingsPage.preferencesPage.editSignature") }}
                                </label>
                                <div
                                    ref="signatureEditorRef"
                                    contenteditable="true"
                                    class="w-full border border-gray-300 bg-white rounded-md p-2 min-h-[150px] overflow-auto focus:outline-none focus:ring-2 focus:ring-gray-800 focus:border-gray-800"
                                    :placeholder="$t('settingsPage.preferencesPage.signaturePlaceholder')"
                                    @input="handleSignatureInput"
                                    @paste.prevent="handlePaste"
                                    @drop.prevent="handleDrop"
                                ></div>
                                <div class="flex justify-end pt-4">
                                    <button
                                        @click="updateSignature"
                                        class="rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
                                    >
                                        {{ $t("settingsPage.preferencesPage.updateSignature") }}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, inject, onMounted, nextTick } from "vue";
import { getData, putData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import TimeZoneSelection from "@/pages/Settings/components/TimeZoneSelection.vue";
import LanguageSelection from "@/pages/Settings/components/LanguageSelection.vue";
import ThemeSelection from "@/pages/Settings/components/ThemeSelection.vue";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue";
import ChevronUpDownIcon from "@heroicons/vue/24/outline/ChevronUpDownIcon";
import CheckIcon from "@heroicons/vue/24/outline/CheckIcon";

const signatures = ref<any[]>([]);
const selectedSignatureId = ref<string>("");
const selectedSignature = ref<any>(null);
const editedSignatureContent = ref<string>("");

const signatureEditorRef = ref<HTMLElement | null>(null);

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

onMounted(async () => {
    await fetchSignatures();
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
    const sig = signatures.value.find((sig) => sig.id === selectedSignatureId.value);
    if (sig) {
        selectedSignature.value = sig;
        editedSignatureContent.value = sig.signature_content;
        await nextTick();
        if (signatureEditorRef.value) {
            signatureEditorRef.value.innerHTML = sig.signature_content;
        }
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
    if (signatureEditorRef.value) {
        editedSignatureContent.value = signatureEditorRef.value.innerHTML || "";
    }
    range.setStartAfter(img);
    range.setEndAfter(img);
    selection.removeAllRanges();
    selection.addRange(range);
};

const updateSignature = async () => {
    if (!selectedSignature.value) return;

    const payload = {
        signature_id: selectedSignature.value.id,
        signature_content: editedSignatureContent.value,
    };

    try {
        const response = await putData(`user/signatures/update/`, payload);
        if (response.success) {
            const index = signatures.value.findIndex((sig) => sig.id === response.data.id);
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
                response.error || (i18n.global.t("settingsPage.preferencesPage.updateError") as string)
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
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
