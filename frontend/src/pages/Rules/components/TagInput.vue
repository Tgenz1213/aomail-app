<template>
    <div>
        <div
            class="min-h-[38px] w-full rounded-md border border-gray-300 focus-within:border-gray-500 focus-within:ring focus-within:ring-gray-500 focus-within:ring-opacity-50"
        >
            <div class="flex flex-wrap gap-1 p-1">
                <!-- Tags -->
                <div
                    v-for="(tag, index) in modelValue"
                    :key="index"
                    class="flex items-center bg-gray-100 rounded px-2 py-1 text-sm"
                >
                    <span>{{ tag }}</span>
                    <button
                        @click="removeTag(index)"
                        class="ml-1 text-gray-500 hover:text-gray-700"
                    >
                        ×
                    </button>
                </div>

                <!-- Input -->
                <input
                    ref="inputRef"
                    v-model="inputValue"
                    type="text"
                    :placeholder="placeholder"
                    class="flex-1 min-w-[120px] outline-none border-0 bg-transparent p-1"
                    @keydown.enter.prevent="addTag"
                    @keydown.backspace="handleBackspace"
                    @keydown.tab="addTag"
                    @keydown="handleKeydown"
                />
            </div>
        </div>
        <div v-if="error" class="mt-1 text-xs text-red-500">
            {{ error }}
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps<{
    modelValue: string[];
    placeholder?: string;
    validate?: (value: string) => boolean;
}>();

const emit = defineEmits<{
    (e: 'update:modelValue', value: string[]): void;
}>();

const inputRef = ref<HTMLInputElement | null>(null);
const inputValue = ref('');
const error = ref('');

const addTag = () => {
    const value = inputValue.value.trim().replace(',', '');
    
    if (!value) return;
    
    if (props.validate && !props.validate(value)) {
        error.value = 'Invalid format';
        return;
    }

    if (!props.modelValue.includes(value)) {
        emit('update:modelValue', [...props.modelValue, value]);
    }
    
    inputValue.value = '';
    error.value = '';
};

const removeTag = (index: number) => {
    const newTags = [...props.modelValue];
    newTags.splice(index, 1);
    emit('update:modelValue', newTags);
};

const handleBackspace = (event: KeyboardEvent) => {
    if (!inputValue.value && props.modelValue.length > 0) {
        event.preventDefault();
        removeTag(props.modelValue.length - 1);
    }
};

const handleKeydown = (event: KeyboardEvent) => {
    if (event.key === ',') {
        event.preventDefault();
        addTag();
    }
};
</script> 