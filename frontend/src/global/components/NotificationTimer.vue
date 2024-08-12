<template>
    <div
        aria-live="assertive"
        class="pointer-events-none fixed inset-0 flex items-end px-4 py-6 sm:items-start sm:p-6"
        style="z-index: 50"
    >
        <div class="flex w-full flex-col items-center space-y-4 sm:items-end">
            <transition
                enter-active-class="transform ease-out duration-300 transition"
                enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
                enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
                leave-active-class="transition ease-in duration-100"
                leave-from-class="opacity-100"
                leave-to-class="opacity-0"
            >
                <div
                    v-if="showNotificationInternal"
                    :class="[
                        'pointer-events-auto',
                        'w-full',
                        'max-w-sm',
                        'overflow-hidden',
                        'rounded-lg',
                        backgroundColor,
                        'shadow-lg',
                        'ring-1',
                        'ring-black',
                        'ring-opacity-5',
                    ]"
                >
                    <div class="p-4">
                        <div class="flex items-start">
                            <div class="flex-shrink-0">
                                <CheckCircleIcon class="h-6 w-6 text-gray-900" aria-hidden="true" />
                            </div>
                            <div class="ml-3 w-0 flex-1 pt-0.5">
                                <p class="text-sm font-medium text-gray-900">{{ notificationTitle }}</p>
                                <p class="mt-1 text-sm text-gray-900">{{ notificationMessage }}</p>
                            </div>
                            <div class="ml-4 flex flex-shrink-0">
                                <button
                                    type="button"
                                    @click="dismissPopup"
                                    class="inline-flex rounded-md text-gray-900 hover:text-black focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2"
                                >
                                    <XMarkIcon class="h-5 w-5 text-gray-900" aria-hidden="true" />
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </transition>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";
import CheckCircleIcon from "@heroicons/vue/20/solid/CheckCircleIcon";
import XMarkIcon from "@heroicons/vue/20/solid/XMarkIcon";

export default defineComponent({
    props: {
        showNotification: {
            type: Boolean,
            required: true,
        },
        notificationTitle: {
            type: String,
            required: false,
        },
        notificationMessage: {
            type: String,
            required: false,
        },
        backgroundColor: {
            type: String,
            required: false,
        },
    },
    setup(props, { emit }) {
        const showNotificationInternal = ref(props.showNotification);
        let timerId: ReturnType<typeof setTimeout>;

        const showPopupWithTimer = () => {
            showNotificationInternal.value = true;
            timerId = setTimeout(() => {
                dismissPopup();
            }, 4000);
        };

        const dismissPopup = () => {
            showNotificationInternal.value = false;
            emit("dismissPopup");
            clearTimeout(timerId);
        };

        watch(
            () => props.showNotification,
            (newVal) => {
                showNotificationInternal.value = newVal;
                if (newVal) {
                    showPopupWithTimer();
                }
            }
        );

        return {
            showNotificationInternal,
            dismissPopup,
            CheckCircleIcon,
            XMarkIcon,
        };
    },
});
</script>
