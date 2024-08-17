<template>
    <div class="flex flex-wrap">
        <div
            v-for="(file, index) in uploadedFiles"
            :key="index"
            class="flex items-center mb-1 mr-1 bg-gray-200 rounded px-2 py-1 2xl:px-3 2xl:py-2 2xl:mr-2"
        >
            {{ file.name }}
            <button @click="removeFile(index)">×</button>
        </div>
    </div>
    <div class="flex items-stretch gap-1 2xl:gap-2">
        <div class="flex-grow">
            <div
                class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 w-full"
            >
                <div class="relative w-full">
                    <div
                        v-if="!isFocused && !inputValue"
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
                        id="objectInput"
                        v-model="inputValue"
                        type="text"
                        class="block h-10 2xl:h-11 flex-1 border-0 bg-transparent py-2 pl-3 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6 w-full z-20 relative 2xl:py-3 2xl:pl-4 2xl:text-base"
                        @focus="handleFocusObject"
                        @blur="handleBlur"
                        @input="handleInputUpdateObject"
                    />
                </div>
            </div>
        </div>
        <div class="flex">
            <input type="file" ref="fileInput" @change="handleFileUpload" class="sr-only" />
            <button
                type="button"
                class="h-10 w-10 inline-flex items-center justify-center rounded-md border border-gray-300 bg-gray-50 text-gray-500 shadow-sm ring-1 ring-gray-300 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                @click="() => $refs.fileInput.click()"
            >
                <UploadIcon class="h-6 w-6 2xl:h-7 2xl:w-7 text-gray-500" />
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
const inputValue = ref("");
const uploadedFiles = ref([]);
const isFocused = ref(false);

const handleFileUpload = (event) => {
    // Handle file upload logic
};

const removeFile = (index) => {
    uploadedFiles.value.splice(index, 1);
};

const handleFocusObject = () => {
    isFocused.value = true;
};

const handleBlur = () => {
    isFocused.value = false;
};

const handleInputUpdateObject = (event) => {
    inputValue.value = event.target.value;
};
</script>
