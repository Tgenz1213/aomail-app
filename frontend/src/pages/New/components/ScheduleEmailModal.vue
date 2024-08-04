<template>
    <div v-if="isOpen">
        <transition name="modal-fade">
            <div
                @click.self="closeModal"
                class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            >
                <div class="bg-white rounded-lg relative w-[450px]">
                    <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
                        <button
                            @click="closeModal"
                            type="button"
                            class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                        >
                            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                        </button>
                    </div>
                    <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
                        <div class="ml-8 flex items-center space-x-1">
                            <p
                                class="block leading-6 text-gray-900"
                                style="font-family: 'Poppins', sans-serif; font-weight: 500"
                            >
                                Schedule Email
                            </p>
                        </div>
                    </div>
                    <div class="flex flex-col gap-4 px-8 py-6">
                        <p class="text-red-500" v-if="errorMessage">{{ errorMessage }}</p>
                        <div>
                            <label for="scheduleDatetime" class="block text-sm font-medium leading-6 text-gray-900">
                                Schedule Date and Time
                            </label>
                            <div class="mt-2">
                                <input
                                    id="scheduleDatetime"
                                    v-model="scheduleDatetime"
                                    type="datetime-local"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"
                                />
                            </div>
                        </div>
                        <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
                            <button
                                type="button"
                                class="inline-flex w-full rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:w-auto"
                                @click="scheduleEmail"
                            >
                                Schedule Email
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script lang="ts" setup>
import { ref, defineProps, defineEmits, watch } from "vue"
import XMarkIcon from "@heroicons/vue/20/solid"

const props = defineProps({
    isOpen: Boolean,
})

const emits = defineEmits(["closeModal", "scheduleEmail"])

const scheduleDatetime = ref<string>("")
const errorMessage = ref<string | null>(null)

watch(
    () => props.isOpen,
    (newVal) => {
        if (newVal) {
            scheduleDatetime.value = ""
            errorMessage.value = null
        }
    }
)

const closeModal = () => {
    emits("closeModal")
}

const scheduleEmail = () => {
    if (!scheduleDatetime.value) {
        errorMessage.value = "Please select a date and time."
        return
    }
    emits("scheduleEmail", { datetime: scheduleDatetime.value })
    closeModal()
}
</script>
