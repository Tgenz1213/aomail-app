<template>
    <TransitionRoot appear :show="isOpen" as="template">
        <Dialog as="div" @close="closeModal" class="relative z-[200]">
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
                                <div class="flex items-center space-x-2">
                                    <!-- Action Buttons -->
                                    <div class="flex space-x-1">
                                        <!-- Read/Unread Button -->
                                        <div class="relative group">
                                            <button
                                                @click="email.read ? markEmailAsUnread() : markEmailAsRead()"
                                                class="flex text-gray-600 hover:text-gray-800 rounded-full p-2.5 hover:bg-gray-200/80 focus:outline-none items-center justify-center"
                                            >
                                                <CheckIcon v-if="!email.read" class="w-5 h-5 text-gray-600" />
                                                <svg
                                                    v-else
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    viewBox="0 0 24 24"
                                                    fill="none"
                                                    stroke="currentColor"
                                                    stroke-width="2"
                                                    stroke-linecap="round"
                                                    stroke-linejoin="round"
                                                    class="w-5 h-5 text-gray-600"
                                                >
                                                    <path d="M5 9l5 5 9-9"></path>
                                                    <path d="M5 16l5 5 9-9"></path>
                                                </svg>
                                            </button>
                                        </div>

                                        <!-- Answer Button -->
                                        <div class="relative group">
                                            <button
                                                @click="openAnswer"
                                                class="flex text-gray-600 hover:text-gray-800 rounded-full p-2.5 hover:bg-gray-200/80 focus:outline-none items-center justify-center"
                                            >
                                                <ArrowUturnLeftIcon class="w-5 h-5" />
                                            </button>
                                        </div>

                                        <!-- More Actions Menu -->
                                        <Menu as="div" class="relative">
                                            <MenuButton
                                                class="flex text-gray-600 hover:text-gray-800 rounded-full p-2.5 hover:bg-gray-200/80 focus:outline-none items-center justify-center"
                                            >
                                                <EllipsisHorizontalIcon class="w-5 h-5" />
                                            </MenuButton>
                                            <transition
                                                enter-active-class="transition ease-out duration-100"
                                                enter-from-class="transform opacity-0 scale-95"
                                                enter-to-class="transform opacity-100 scale-100"
                                                leave-active-class="transition ease-in duration-75"
                                                leave-from-class="transform opacity-100 scale-100"
                                                leave-to-class="transform opacity-0 scale-95"
                                            >
                                                <MenuItems class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none cursor-pointer">
                                                    <!-- Archive/Unarchive Option -->
                                                    <div class="py-1">
                                                        <MenuItem v-slot="{ active }">
                                                            <a
                                                                @click.prevent="email.archive ? unarchiveEmail() : archiveEmail()"
                                                                :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']"
                                                            >
                                                                <span class="flex gap-x-2 items-center">
                                                                    <ArchiveBoxIcon class="w-4 h-4" />
                                                                    <span>
                                                                        {{ email.archive ? $t("constants.userActions.unarchive") : $t("constants.userActions.archive") }}
                                                                    </span>
                                                                </span>
                                                            </a>
                                                        </MenuItem>
                                                    </div>

                                                    <!-- Reply Later Options -->
                                                    <div class="py-1">
                                                        <MenuItem v-slot="{ active }">
                                                            <a
                                                                @click.prevent="email.answerLater ? markEmailAsUnreplyLater() : markEmailReplyLater()"
                                                                :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']"
                                                            >
                                                                <span class="flex gap-x-2 items-center">
                                                                    <ClockIcon class="w-4 h-4" />
                                                                    <span>
                                                                        {{ email.answerLater ? $t("constants.userActions.unreplyLater") : $t("constants.userActions.replyLater") }}
                                                                    </span>
                                                                </span>
                                                            </a>
                                                        </MenuItem>
                                                    </div>

                                                    <!-- Transfer Option -->
                                                    <div class="py-1">
                                                        <MenuItem v-slot="{ active }">
                                                            <a
                                                                @click.prevent="transferEmail"
                                                                :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']"
                                                            >
                                                                <span class="flex gap-x-2 items-center">
                                                                    <ArrowPathRoundedSquareIcon class="w-4 h-4" />
                                                                    <span>{{ $t("constants.userActions.transfer") }}</span>
                                                                </span>
                                                            </a>
                                                        </MenuItem>
                                                    </div>

                                                    <!-- Delete Option -->
                                                    <div class="py-1">
                                                        <MenuItem v-slot="{ active }">
                                                            <a
                                                                @click.prevent="deleteEmail"
                                                                :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']"
                                                            >
                                                                <span class="flex gap-x-2 items-center">
                                                                    <TrashIcon class="w-4 h-4" />
                                                                    <span>{{ $t("constants.userActions.delete") }}</span>
                                                                </span>
                                                            </a>
                                                        </MenuItem>
                                                    </div>
                                                </MenuItems>
                                            </transition>
                                        </Menu>
                                    </div>
                                    
                                    <button
                                        @click="closeModal"
                                        class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none"
                                    >
                                        <XMarkIcon class="h-6 w-6" />
                                    </button>
                                </div>
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

                                <div class="mt-4 border-t pt-4 max-h-[60vh] overflow-y-auto">
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
import { ref } from 'vue';
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot, Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue';
import {
    XMarkIcon,
    CheckIcon,
    ArrowUturnLeftIcon,
    EllipsisHorizontalIcon,
    ArchiveBoxIcon,
    TrashIcon,
    ClockIcon,
    ArrowPathRoundedSquareIcon,
} from '@heroicons/vue/24/outline';
import { Email } from '@/global/types';
import { formatSentDateAndTime } from '@/global/formatters';

const props = defineProps<{
    isOpen: boolean;
    email: Email;
}>();

const emit = defineEmits<{
    (e: 'closeModal'): void;
    (e: 'markEmailAsRead'): void;
    (e: 'markEmailAsUnread'): void;
    (e: 'archiveEmail'): void;
    (e: 'unarchiveEmail'): void;
    (e: 'deleteEmail'): void;
    (e: 'markEmailReplyLater'): void;
    (e: 'markEmailAsUnreplyLater'): void;
    (e: 'openAnswer'): void;
    (e: 'transferEmail'): void;
}>();

const closeModal = () => {
    emit('closeModal');
};

const markEmailAsRead = () => {
    emit('markEmailAsRead');
    closeModal();
};

const markEmailAsUnread = () => {
    emit('markEmailAsUnread');
    closeModal();
};

const archiveEmail = () => {
    emit('archiveEmail');
    closeModal();
};

const unarchiveEmail = () => {
    emit('unarchiveEmail');
    closeModal();
};

const deleteEmail = () => {
    emit('deleteEmail');
    closeModal();
};

const markEmailReplyLater = () => {
    emit('markEmailReplyLater');
    closeModal();
};

const markEmailAsUnreplyLater = () => {
    emit('markEmailAsUnreplyLater');
    closeModal();
};

const openAnswer = () => {
    emit('openAnswer');
    closeModal();
};

const transferEmail = () => {
    emit('transferEmail');
    closeModal();
};

const formatCCRecipients = (cc: { email: string; name: string }[]) => {
    return cc.map(recipient => `${recipient.name} (${recipient.email})`).join(', ');
};
</script>
