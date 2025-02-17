<template>
    <TransitionRoot appear :show="isOpen" as="template">
        <Dialog as="div" @close="closeModal" class="relative z-50">
            <TransitionChild
                as="template"
                enter="duration-300 ease-out"
                enter-from="opacity-0"
                enter-to="opacity-100"
                leave="duration-200 ease-in"
                leave-from="opacity-100"
                leave-to="opacity-0"
            >
                <div class="fixed inset-0 bg-black/25" />
            </TransitionChild>

            <div class="fixed inset-0 overflow-y-auto">
                <div class="flex min-h-full items-center justify-center p-4">
                    <TransitionChild
                        as="template"
                        enter="duration-300 ease-out"
                        enter-from="opacity-0 scale-95"
                        enter-to="opacity-100 scale-100"
                        leave="duration-200 ease-in"
                        leave-from="opacity-100 scale-100"
                        leave-to="opacity-0 scale-95"
                    >
                        <DialogPanel class="w-full max-w-4xl transform overflow-hidden rounded-2xl bg-white py-6 shadow-xl transition-all">
                            <div class="flex justify-between items-center mb-4 px-6">
                                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                                    {{ email.subject }}
                                </DialogTitle>
                                <button
                                    @click="closeModal"
                                    class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none"
                                >
                                    <XMarkIcon class="h-6 w-6" />
                                </button>
                            </div>

                            <div class="space-y-4">
                                <div class="flex items-center space-x-2 text-sm text-gray-500 px-6">
                                    <span class="font-semibold">{{ $t("transferPage.from") }}</span>
                                    <span>{{ email.sender.name }} ({{ email.sender.email }})</span>
                                </div>

                                <div class="flex items-center space-x-2 text-sm text-gray-500 px-6">
                                    <span class="font-semibold">{{ $t("transferPage.date") }}</span>
                                    <span>{{ formatSentDateAndTime(email.sentDate, email.sentTime) }}</span>
                                </div>

                                <div v-if="email.cc?.length" class="flex items-center space-x-2 text-sm text-gray-500 px-6">
                                    <span class="font-semibold">{{ $t("transferPage.cc") }}</span>
                                    <span>{{ formatCCRecipients(email.cc) }}</span>
                                </div>

                                <div class="mt-4 border-t pt-4 max-h-[60vh] overflow-y-auto ">
                                    <div v-html="email.htmlContent" class="prose max-w-none px-6 pr-0 mr-0 custom-email-content"></div>
                                </div>
                            </div>
                        </DialogPanel>
                    </TransitionChild>
                </div>
            </div>
        </Dialog>
    </TransitionRoot>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { XMarkIcon } from '@heroicons/vue/24/outline';
import { Email } from '@/global/types';
import { formatSentDateAndTime } from '@/global/formatters';
import { getData } from '@/global/fetchData';
import { inject } from 'vue';

const props = defineProps<{
    isOpen: boolean;
    email: Email;
}>();

console.log(props.email);

const emit = defineEmits<{
    (e: 'closeModal'): void;
}>();

const closeModal = () => {
    emit('closeModal');
};

const formatCCRecipients = (cc: { email: string; name: string }[]) => {
    return cc.map(recipient => `${recipient.name} (${recipient.email})`).join(', ');
};
</script> 