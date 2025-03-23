<template>
    <div class="overflow-y-auto max-h-32 flex flex-wrap gap-1">
        <div
            v-for="(file, index) in uploadedFiles"
            :key="file.name"
            class="flex flex-col gap-0.5 px-1 py-0.5 rounded-md bg-gray-50 border border-gray-200"
        >
            <div class="flex items-center gap-0.5">
                <span class="cursor-pointer text-sm">{{ file.name }}</span>
                <button
                    @click="removeFile(index)"
                    class="text-gray-400 hover:text-gray-600 focus:outline-none"
                    aria-label="Remove file"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-2.5 w-2.5"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                    >
                        <path
                            fill-rule="evenodd"
                            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                            clip-rule="evenodd"
                        />
                    </svg>
                </button>
            </div>
            
            <!-- File Preview Thumbnail -->
            <div v-if="isImageFile(file.name)" class="w-16 h-12 overflow-hidden rounded-md">
                <img 
                    :src="getFilePreview(fileObjects[index])" 
                    class="w-full h-full object-contain"
                    alt="File preview"
                />
            </div>
        </div>
    </div>
    <div class="flex items-stretch gap-1 2xl:gap-2">
        <div class="flex-grow">
            <div class="relative w-full">
                <div
                    v-if="!isFocused && !subjectInput"
                    class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full z-10"
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
                    id="subjectInput"
                    v-model="subjectInput"
                    type="text"
                    class="block h-10 2xl:h-11 flex-1 border-0 bg-transparent py-2 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6 w-full z-20 relative 2xl:py-3 2xl:text-base border-b border-gray-200 focus:border-gray-400 transition-colors duration-200"
                    @focus="handleFocusObject"
                    @blur="handleBlur"
                />
            </div>
        </div>
        <div class="flex">
            <input type="file" ref="fileInput" @change="handleFileUpload" multiple hidden />
            <button
                @click="triggerFileInput"
                type="button"
                class="inline-flex items-center justify-center rounded-full w-10 h-10 2xl:w-11 2xl:h-11 bg-gray-100 text-gray-400 hover:bg-gray-200 transition-all duration-200 focus:outline-none"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="w-5 h-5 2xl:w-6 2xl:h-6"
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
import { inject, onMounted, onUnmounted, ref, Ref } from "vue";

const subjectInput = inject<Ref<string>>("subjectInput", ref(""));
const uploadedFiles = inject<Ref<UploadedFile[]>>("uploadedFiles", ref([]));
const fileObjects = inject<Ref<File[]>>("fileObjects", ref([]));
const isFocused = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);
const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25MB, Gmail's limit

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const isImageFile = (filename: string) => {
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'];
    return imageExtensions.some(ext => filename.toLowerCase().endsWith(ext));
};

const getFilePreview = (file: File) => {
    if (!file) return '';
    return URL.createObjectURL(file);
};

// Clean up object URLs when component is unmounted
onUnmounted(() => {
    fileObjects.value.forEach(file => {
        if (isImageFile(file.name)) {
            URL.revokeObjectURL(getFilePreview(file));
        }
    });
});

const handleFileUpload = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (!input?.files) return;

    const files = Array.from(input.files);

    console.log("files", files.values);
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
            console.log("fileObjects", fileObjects.value);
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
