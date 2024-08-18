<template>
    <div class="flex flex-wrap">
        <div
            v-for="(file, index) in uploadedFiles"
            :key="index"
            class="flex items-center mb-1 mr-1 bg-gray-200 rounded px-2 py-1 2xl:px-3 2xl:py-2 2xl:mr-2"
        >
            {{ file.name }}
            <button
                @click="removeFile(index)"
                class="ml-2 text-gray-500 hover:text-red-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 rounded-full p-1 transition-colors duration-300"
                aria-label="Remove file"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="2"
                    stroke="currentColor"
                    class="w-4 h-4"
                >
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
    </div>
    <div class="flex items-stretch gap-1 2xl:gap-2">
        <div class="flex-grow">
            <div
                class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 w-full"
            >
                <div class="relative w-full">
                    <div
                        v-if="!isFocused && !inputSubject"
                        class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 2xl:ml-3 z-10"
                    >
                        <Bars2Icon class="w-4 h-4 pointer-events-none 2xl:w-5 2xl:h-5" />
                        <label
                            for="username"
                            class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none 2xl:text-base"
                        >
                            {{ $t("constants.subject") }}
                        </label>
                    </div>
                    <input
                        id="inputSubject"
                        v-model="inputSubject"
                        type="text"
                        class="block h-10 2xl:h-11 flex-1 border-0 bg-transparent py-2 pl-3 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6 w-full z-20 relative 2xl:py-3 2xl:pl-4 2xl:text-base"
                        @focus="handleFocusObject"
                        @blur="handleBlur"
                    />
                </div>
            </div>
        </div>
        <div class="flex">
            <input type="file" ref="fileInput" @change="handleFileUpload" multiple hidden />
            <button
                @click="triggerFileInput"
                type="button"
                class="inline-flex items-center gap-x-1.5 rounded-md bg-gray-100 px-2.5 py-1.5 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-300 shadow-sm hover:ring-transparent hover:bg-gray-600 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 2xl:px-3 2xl:py-2 2xl:text-base"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="w-6 h-6 2xl:w-7 2xl:h-7"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13"
                    />
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { i18n } from "@/global/preferences";
import { UploadedFile } from "@/global/types";
import { inject, onMounted, ref, Ref } from "vue";

const inputSubject = inject<Ref<string>>("inputSubject", ref(""));
const uploadedFiles = inject<Ref<UploadedFile[]>>("uploadedFiles", ref([]));
const fileObjects = inject<Ref<File[]>>("fileObjects", ref([]));
const isFocused = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);
const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25MB, Gmail's limit

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const handleFileUpload = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (!input?.files) return;

    const files = Array.from(input.files);
    files.forEach((file) => {
        if (file.size <= MAX_FILE_SIZE) {
            const existingFiles = JSON.parse(localStorage.getItem("uploadedFiles") || "[]");

            if (existingFiles.some((existingFile: UploadedFile) => existingFile.name === file.name)) {
                displayPopup?.(
                    "error",
                    i18n.global.t("constants.popUpConstants.errorMessages.duplicateFile"),
                    i18n.global.t("constants.popUpConstants.errorMessages.fileAlreadyInserted")
                );
                return;
            }

            uploadedFiles.value.push({ name: file.name, size: file.size });
            fileObjects.value.push(file);
        } else {
            displayPopup?.(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.fileTooLarge"),
                i18n.global.t("constants.popUpConstants.errorMessages.fileSizeExceedsLimit")
            );
        }
    });

    saveFileMetadataToLocalStorage();
};

const triggerFileInput = () => fileInput.value?.click();

const removeFile = (index: number) => {
    uploadedFiles.value.splice(index, 1);
    fileObjects.value.splice(index, 1);
    saveFileMetadataToLocalStorage();
};

const saveFileMetadataToLocalStorage = () => {
    localStorage.setItem("uploadedFiles", JSON.stringify(uploadedFiles.value));
};

const handleFocusObject = () => {
    isFocused.value = true;
};
const handleBlur = () => {
    isFocused.value = false;
};

const handleBeforeUnload = (event: BeforeUnloadEvent) => {
    if (uploadedFiles.value.length) {
        event.preventDefault();
    }
};

onMounted(() => {
    window.addEventListener("beforeunload", handleBeforeUnload);
});
</script>
