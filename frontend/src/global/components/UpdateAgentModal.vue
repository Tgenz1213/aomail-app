<template>
    <div
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
        @click.self="$emit('close')"
    >
        <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-semibold">{{ $t("newPage.updateAgent.title") }}</h2>
                <button type="button" @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
                    <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                </button>
            </div>

            <form @submit.prevent="updateAgent">
                <div class="mb-4">
                    <div class="flex items-end space-x-4">
                        <div class="flex-shrink-0">
                            <div class="relative h-[4rem] w-[4rem]">
                                <img
                                    :src="previewImage"
                                    class="h-[4rem] w-[4rem] rounded-lg object-cover"
                                    alt="Agent icon"
                                />
                                <label
                                    class="absolute inset-0 flex items-center justify-center cursor-pointer bg-black bg-opacity-50 rounded-lg opacity-0 hover:opacity-100 transition-opacity"
                                >
                                    <input type="file" accept="image/*" class="hidden" @change="handleImageUpload" />
                                    <span class="text-white text-xs">{{ $t("newPage.updateAgent.upload") }}</span>
                                </label>
                            </div>
                        </div>
                        <div class="flex-grow">
                            <label class="block text-sm font-medium text-gray-700">
                                {{ $t("newPage.updateAgent.agentName") }}
                            </label>
                            <p v-if="showNameError" class="text-red-500 text-xs mt-1">
                                {{ $t("newPage.updateAgent.agentNameError") }}
                            </p>
                            <input
                                type="text"
                                v-model="agentName"
                                required
                                @input="showNameError = false"
                                class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:border-gray-900 focus:ring-gray-900 focus:outline-none"
                                :placeholder="$t('newPage.updateAgent.agentNamePlaceholder')"
                            />
                        </div>
                    </div>
                </div>

                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700">
                        {{ $t("newPage.updateAgent.behaviorDescription") }}
                    </label>
                    <textarea
                        v-model="behaviorDescription"
                        class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:border-gray-900 focus:ring-gray-900 focus:outline-none"
                        :placeholder="$t('newPage.updateAgent.behaviorPlaceholder')"
                    ></textarea>
                </div>

                <div class="mb-4">
                    <button
                        type="button"
                        @click="showEmailExample = !showEmailExample"
                        class="text-sm text-gray-500 hover:text-gray-700 flex items-center"
                    >
                        <PlusIcon v-if="!showEmailExample" class="h-4 w-4 mr-1" />
                        <MinusIcon v-else class="h-4 w-4 mr-1" />
                        {{ $t("newPage.updateAgent.emailExample") }}
                    </button>

                    <transition
                        enter-active-class="transition ease-out duration-200"
                        enter-from-class="transform opacity-0 scale-95"
                        enter-to-class="transform opacity-100 scale-100"
                        leave-active-class="transition ease-in duration-75"
                        leave-from-class="transform opacity-100 scale-100"
                        leave-to-class="transform opacity-0 scale-95"
                    >
                        <textarea
                            v-if="showEmailExample"
                            v-model="emailExample"
                            rows="6"
                            class="mt-2 block w-full border border-gray-300 rounded-md p-2 focus:border-gray-900 focus:ring-gray-900 focus:outline-none min-h-[150px]"
                            :placeholder="$t('newPage.updateAgent.emailExamplePlaceholder')"
                        ></textarea>
                    </transition>
                </div>

                <div class="flex space-x-4 mb-4">
                    <div class="flex-1">
                        <label class="block text-sm font-medium text-gray-700">
                            {{ $t("newPage.updateAgent.length") }}
                        </label>
                        <Listbox v-model="length">
                            <div class="relative mt-1">
                                <ListboxButton
                                    class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6"
                                >
                                    <span class="block truncate">
                                        {{ length.charAt(0).toUpperCase() + length.slice(1) }}
                                    </span>
                                    <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                                    </span>
                                </ListboxButton>

                                <transition
                                    leave-active-class="transition ease-in duration-100"
                                    leave-from-class="opacity-100"
                                    leave-to-class="opacity-0"
                                >
                                    <ListboxOptions
                                        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                                    >
                                        <ListboxOption
                                            v-for="option in ['very short', 'short', 'medium']"
                                            :key="option"
                                            :value="option"
                                            v-slot="{ active, selected }"
                                        >
                                            <li
                                                :class="[
                                                    active ? 'bg-gray-800 text-white' : 'text-gray-900',
                                                    'relative cursor-default select-none py-2 pl-3 pr-9',
                                                ]"
                                            >
                                                <span
                                                    :class="[
                                                        selected ? 'font-semibold' : 'font-normal',
                                                        'block truncate',
                                                    ]"
                                                >
                                                    {{ option.charAt(0).toUpperCase() + option.slice(1) }}
                                                </span>
                                                <span
                                                    v-if="selected"
                                                    :class="[
                                                        active ? 'text-white' : 'text-gray-500',
                                                        'absolute inset-y-0 right-0 flex items-center pr-4',
                                                    ]"
                                                >
                                                    <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                                </span>
                                            </li>
                                        </ListboxOption>
                                    </ListboxOptions>
                                </transition>
                            </div>
                        </Listbox>
                    </div>

                    <div class="flex-1">
                        <label class="block text-sm font-medium text-gray-700">
                            {{ $t("newPage.updateAgent.formality") }}
                        </label>
                        <Listbox v-model="formality">
                            <div class="relative mt-1">
                                <ListboxButton
                                    class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6"
                                >
                                    <span class="block truncate">
                                        {{ formality.charAt(0).toUpperCase() + formality.slice(1) }}
                                    </span>
                                    <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                                    </span>
                                </ListboxButton>

                                <transition
                                    leave-active-class="transition ease-in duration-100"
                                    leave-from-class="opacity-100"
                                    leave-to-class="opacity-0"
                                >
                                    <ListboxOptions
                                        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                                    >
                                        <ListboxOption
                                            v-for="option in ['informal', 'formal', 'very formal']"
                                            :key="option"
                                            :value="option"
                                            v-slot="{ active, selected }"
                                        >
                                            <li
                                                :class="[
                                                    active ? 'bg-gray-800 text-white' : 'text-gray-900',
                                                    'relative cursor-default select-none py-2 pl-3 pr-9',
                                                ]"
                                            >
                                                <span
                                                    :class="[
                                                        selected ? 'font-semibold' : 'font-normal',
                                                        'block truncate',
                                                    ]"
                                                >
                                                    {{ option.charAt(0).toUpperCase() + option.slice(1) }}
                                                </span>
                                                <span
                                                    v-if="selected"
                                                    :class="[
                                                        active ? 'text-white' : 'text-gray-500',
                                                        'absolute inset-y-0 right-0 flex items-center pr-4',
                                                    ]"
                                                >
                                                    <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                                </span>
                                            </li>
                                        </ListboxOption>
                                    </ListboxOptions>
                                </transition>
                            </div>
                        </Listbox>
                    </div>
                </div>

                <div class="flex justify-between items-center">
                    <button
                        type="button"
                        @click="deleteAgent"
                        class="inline-flex rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700"
                    >
                        {{ $t("newPage.updateAgent.delete") }}
                    </button>
                    <div class="flex space-x-2">
                        <button
                            type="button"
                            @click="$emit('close')"
                            class="inline-flex rounded-md bg-gray-300 px-3 py-2 text-sm font-semibold text-gray-700 shadow-sm hover:bg-gray-400"
                        >
                            {{ $t("newPage.updateAgent.cancel") }}
                        </button>
                        <button
                            type="submit"
                            class="inline-flex rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black"
                        >
                            {{ $t("newPage.updateAgent.update") }}
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from "vue";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue";
import { ChevronUpDownIcon, CheckIcon, XMarkIcon, PlusIcon, MinusIcon } from "@heroicons/vue/20/solid";
import { putData, deleteData } from "@/global/fetchData";
import { Agent } from "@/global/types";
import { i18n } from "../preferences";
import { inject } from "vue";
import { API_BASE_URL } from "@/global/const";

const emit = defineEmits(["updated", "deleted", "close"]);

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const props = defineProps({
    agent: {
        type: Object as () => Agent,
        required: true,
    },
});

const agentName = ref(props.agent.agent_name);
const behaviorDescription = ref(props.agent.ai_template || "");
const length = ref(props.agent.length);
const formality = ref(props.agent.formality);
const previewImage = ref(`${API_BASE_URL}agent_icon/${props.agent.picture}`);
const selectedFile = ref<File | null>(null);
const showEmailExample = ref(false);
const emailExample = ref(props.agent.email_example || "");
const showNameError = ref(false);

watch(
    () => props.agent,
    (newAgent) => {
        agentName.value = newAgent.agent_name;
        behaviorDescription.value = newAgent.ai_template || "";
        length.value = newAgent.length;
        formality.value = newAgent.formality;
        emailExample.value = newAgent.email_example || "";
    }
);

const updateAgent = async () => {
    if (!agentName.value.trim()) {
        showNameError.value = true;
        return;
    }

    const formData = new FormData();
    formData.append("agent_name", agentName.value);
    formData.append("ai_template", behaviorDescription.value);
    formData.append("email_example", emailExample.value);
    formData.append("length", length.value);
    formData.append("formality", formality.value);
    if (selectedFile.value) {
        formData.append("picture", selectedFile.value);
    }

    const result = await putData(`user/agents/${props.agent.id}/update/`, formData, true);

    if (result.success) {
        const updatedAgent: Agent = {
            ...result.data,
            picture: result.data.picture || "/assets/default-agent.png",
        };
        displayPopup?.(
            "success",
            i18n.global.t("constants.popUpConstants.successMessages.agentUpdated"),
            i18n.global.t("constants.popUpConstants.successMessages.agentUpdatedDesc")
        );
        emit("updated", updatedAgent);
        emit("close");
    } else {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.updateAgentError"),
            result.error as string
        );
    }
};

const deleteAgent = async () => {
    const result = await deleteData(`user/agents/${props.agent.id}/delete/`);

    if (result.success) {
        displayPopup?.(
            "success",
            i18n.global.t("constants.popUpConstants.successMessages.agentDeleted"),
            i18n.global.t("constants.popUpConstants.successMessages.agentDeletedDesc")
        );
        emit("deleted", props.agent.id);
        emit("close");
    } else {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.deleteAgentError"),
            result.error as string
        );
    }
};

const handleImageUpload = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
        selectedFile.value = input.files[0];
        previewImage.value = URL.createObjectURL(input.files[0]);
    }
};

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Escape") {
        event.preventDefault();
        emit("close");
    }
};

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

onUnmounted(() => {
    document.removeEventListener("keydown", handleKeyDown);
});
</script>
