<template>
    <div class="relative">
        <div
            class="min-h-[38px] w-full rounded-md border border-gray-300 focus-within:border-gray-500 focus-within:ring focus-within:ring-gray-500 focus-within:ring-opacity-50"
        >
            <div class="flex flex-wrap gap-1 p-1">
                <span
                    v-for="(tag, index) in modelValue"
                    :key="index"
                    class="inline-flex items-center px-2 py-1 rounded-md text-sm bg-gray-100"
                >
                    {{ tag }}
                    <button
                        @click="removeTag(index)"
                        class="ml-1 text-gray-500 hover:text-gray-700"
                    >
                        ×
                    </button>
                </span>
                <input
                    ref="input"
                    v-model="newTag"
                    :placeholder="placeholder"
                    @keydown.enter.prevent="addTag"
                    @keydown.backspace="handleBackspace"
                    class="flex-1 min-w-[60px] outline-none border-0 bg-transparent p-1"
                />
            </div>
        </div>
        <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
    </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps<{
    modelValue: string[];
    placeholder?: string;
    validate?: (value: string) => boolean;
}>();

const emit = defineEmits(['update:modelValue']);

const input = ref<HTMLInputElement | null>(null);
const newTag = ref('');
const error = ref('');

const addTag = () => {
    if (newTag.value.trim()) {
        if (props.validate && !props.validate(newTag.value.trim())) {
            error.value = 'Invalid format';
            return;
        }
        
        const updatedTags = [...props.modelValue, newTag.value.trim()];
        emit('update:modelValue', updatedTags);
        newTag.value = '';
        error.value = '';
    }
};

const removeTag = (index: number) => {
    const updatedTags = props.modelValue.filter((_, i) => i !== index);
    emit('update:modelValue', updatedTags);
};

const handleBackspace = (event: KeyboardEvent) => {
    if (newTag.value === '' && props.modelValue.length > 0) {
        event.preventDefault();
        removeTag(props.modelValue.length - 1);
    }
};
</script> 