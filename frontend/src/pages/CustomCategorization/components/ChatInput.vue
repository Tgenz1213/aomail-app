<template>
    <div class="max-h-[22vh] h-full bg-zinc-50 bg-opacity-40 border-t border-gray-200">
        <div class="flex justify-center h-full">
            <div class="w-full max-w-5xl h-full">
                <div class="flex flex-col h-full">
                    <textarea
                        v-model="userInput"
                        @keydown.enter="handleKeyDown"
                        @input="adjustHeight"
                        class="overflow-y-hidden pt-4 pl-6 flex-1 w-full border-transparent bg-transparent text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 focus:border-transparent focus:bg-transparent focus:ring-0 2xl:pt-5 2xl:pl-7 2xl:text-base"
                        :placeholder="$t('chatInput.typePlaceholder')"
                    ></textarea>
                    <div class="flex justify-start m-3 2xl:m-5">
                        <button
                            @click="submitResponse"
                            :disabled="!userInput.trim()"
                            class="2xl:w-[100px] w-[80px] rounded-md bg-zinc-800 px-5.5 py-2.5 2xl:px-6.5 2xl:py-3 2xl:text-base text-sm text-white shadow-sm hover:bg-gray-700 disabled:bg-gray-300 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                        >
                            {{ $t("constants.userActions.send") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

const emit = defineEmits(["response"]);

const userInput = ref("");

function submitResponse() {
    if (userInput.value.trim()) {
        emit("response", userInput.value.trim());
        userInput.value = "";
    }
}

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        submitResponse();
    }
}

function adjustHeight(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}
</script>
