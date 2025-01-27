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

            <div class="flex gap-x-10 w-full">
                <div class="flex-1 flex flex-col">
                    <div class="relative">
                        <div class="absolute inset-0 flex items-center" aria-hidden="true">
                            <div class="w-full border-t border-gray-300"></div>
                        </div>
                        <div class="relative flex justify-center">
                            <span class="bg-white px-2 text-sm text-gray-500">E-commerce (Vinted)</span>
                        </div>
                    </div>
                    <a
                        href="/labels"
                        class="rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600"
                    >
                        Shipping Labels
                    </a>
                </div>
            </div>
            <div
                class="flex-1 w-full h-full rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 text-center"
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
                            d="M11.42 15.17 17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 0 0 4.486-6.336l-3.276 3.277a3.004 3.004 0 0 1-2.25-2.25l3.276-3.276a4.5 4.5 0 0 0-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437 1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008Z"
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
