<template>
    <transition name="modal-fade">
        <div
            @click.self="closeModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            v-if="isOpen"
        >
            <div class="bg-white rounded-lg relative w-[450px]">
                <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
                    <button
                        @click="closeModal"
                        @keydown="handleKeyDown"
                        type="button"
                        class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                    >
                        <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                    </button>
                </div>
                <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
                    <div class="ml-8 flex items-center space-x-1">
                        <p class="block font-semibold leading-6 text-gray-900">
                            {{ $t("rulesPage.modals.createRule.newRule") }}
                        </p>
                    </div>
                </div>
                <div class="flex flex-col gap-4 px-8 py-6">
                    <Combobox as="div" v-model="selectedPerson">
                        <div v-if="errorMessage" class="text-red-600 text-sm mb-4">
                            {{ errorMessage }}
                        </div>
                        <div class="flex space-x-1 items-center">
                            <UserIcon class="w-4 h-4" />
                            <ComboboxLabel class="block text-sm font-medium leading-6 text-gray-900">
                                {{ $t("rulesPage.contactField") }}
                            </ComboboxLabel>
                        </div>
                        <div class="relative mt-2">
                            <ComboboxInput
                                id="inputField"
                                class="w-full rounded-md border-0 bg-white py-1.5 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                                @change="query = $event.target.value"
                                :display-value="getDisplayValue"
                                @blur="handleBlur($event)"
                                @keydown="handleKeyDown"
                            />
                            <ComboboxButton
                                class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none"
                            >
                                <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                            </ComboboxButton>
                            <ComboboxOptions
                                v-if="filteredPeople.length > 0"
                                class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                            >
                                <ComboboxOption
                                    v-for="person in filteredPeople"
                                    :key="person.username"
                                    :value="person"
                                    as="template"
                                    v-slot="{ active, selected }"
                                >
                                    <li
                                        :class="[
                                            'relative cursor-default select-none py-2 pl-3 pr-9',
                                            active ? 'bg-gray-500 text-white' : 'text-gray-900',
                                        ]"
                                    >
                                        <div class="flex">
                                            <span :class="['truncate', selected && 'font-semibold']">
                                                {{ person.username }}
                                            </span>
                                            <span
                                                :class="[
                                                    'ml-2 truncate text-gray-800',
                                                    active ? 'text-gray-200' : 'text-gray-800',
                                                ]"
                                            >
                                                {{ person.email }}
                                            </span>
                                        </div>
                                        <span
                                            v-if="selected"
                                            :class="[
                                                'absolute inset-y-0 right-0 flex items-center pr-4',
                                                active ? 'text-white' : 'text-gray-500',
                                            ]"
                                        >
                                            <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                        </span>
                                    </li>
                                </ComboboxOption>
                            </ComboboxOptions>
                        </div>
                    </Combobox>
                    <div>
                        <div class="flex space-x-1 items-center">
                            <ArchiveBoxIcon class="w-4 h-4" />
                            <label for="category" class="block text-sm font-medium leading-6 text-gray-900">
                                {{ $t("constants.category") }}
                            </label>
                        </div>
                        <select
                            id="category"
                            name="category"
                            v-model="formData.category"
                            class="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-gray-500 sm:text-sm sm:leading-6"
                        >
                            <option value="">{{ $t("constants.ruleModalConstants.noCategoryDefined") }}</option>
                            <option v-for="category in categories" :key="category.name" :value="category.name">
                                {{ category.name }}
                            </option>
                        </select>
                    </div>
                    <div>
                        <div class="flex space-x-1 items-center">
                            <ExclamationCircleIcon class="w-4 h-4" />
                            <label for="priority" class="block text-sm font-medium leading-6 text-gray-900">
                                {{ $t("rulesPage.priorityField") }}
                            </label>
                        </div>
                        <select
                            id="priority"
                            name="priority"
                            v-model="formData.priority"
                            class="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-gray-500 sm:text-sm sm:leading-6"
                        >
                            <option value="">{{ $t("constants.ruleModalConstants.noPriority") }}</option>
                            <option :value="IMPORTANT">{{ $t("constants.ruleModalConstants.important") }}</option>
                            <option :value="INFORMATIVE">{{ $t("constants.ruleModalConstants.informative") }}</option>
                            <option :value="USELESS">{{ $t("constants.ruleModalConstants.useless") }}</option>
                        </select>
                    </div>
                    <SwitchGroup as="div" class="flex items-center pt-2">
                        <Switch
                            v-model="formData.block"
                            :class="[
                                formData.block ? 'bg-gray-500' : 'bg-gray-200',
                                'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2',
                            ]"
                        >
                            <span
                                aria-hidden="true"
                                :class="[
                                    formData.block ? 'translate-x-5' : 'translate-x-0',
                                    'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                                ]"
                            />
                        </Switch>
                        <SwitchLabel as="span" class="ml-3 text-sm">
                            <span class="font-medium text-gray-900">
                                {{ $t("constants.ruleModalConstants.blockTheEmails") }}
                            </span>
                            {{ " " }}
                        </SwitchLabel>
                        <ShieldCheckIcon class="ml-1 w-4 h-4" />
                    </SwitchGroup>
                    <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
                        <button
                            type="button"
                            class="inline-flex w-full justify-center rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:ml-3 sm:w-auto"
                            @click="createEmailSenderRule"
                        >
                            {{ $t("constants.userActions.create") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { ref, computed, watch, inject, onMounted } from "vue";
import { i18n } from "@/global/preferences";
import { Switch, SwitchGroup, SwitchLabel } from "@headlessui/vue";
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/20/solid";
import { XMarkIcon, UserIcon, ArchiveBoxIcon, ShieldCheckIcon, ExclamationCircleIcon } from "@heroicons/vue/24/outline";
import {
    Combobox,
    ComboboxButton,
    ComboboxInput,
    ComboboxLabel,
    ComboboxOptions,
    ComboboxOption,
} from "@headlessui/vue";
import { postData } from "@/global/fetchData";
import { Category, EmailSender } from "@/global/types";
import { IMPORTANT, INFORMATIVE, USELESS } from "@/global/const";

interface Props {
    isOpen: boolean;
    emailSenders: EmailSender[];
    categories: Category[];
    sender: EmailSender | null;
}

const props = withDefaults(defineProps<Props>(), {
    emailSenders: () => [],
    sender: null,
});

const emit = defineEmits<{
    (e: "update:isOpen", value: boolean): void;
    (e: "fetch-rules"): void;
    (e: "update:emailSenders", value: EmailSender[]): void;
}>();

const isOpen = ref(props.isOpen);
const selectedPerson = ref<EmailSender | null>(props.sender);
const query = ref("");
const formData = ref({
    category: "",
    priority: "",
    block: false,
});

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const filteredPeople = computed(() => {
    const normalizedQuery = query.value?.toLowerCase() ?? "";
    return props.emailSenders.filter((person) => person.username?.toLowerCase()?.includes(normalizedQuery) ?? false);
});

const errorMessage = ref("");

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

watch(
    () => props.isOpen,
    (newValue) => {
        isOpen.value = newValue;
    }
);

watch(isOpen, (newValue) => {
    if (!newValue) {
        selectedPerson.value = null;
        query.value = "";
        errorMessage.value = "";
    } else {
        selectedPerson.value = props.sender;
    }
});

watch(selectedPerson, (newValue) => {
    if (newValue) {
        errorMessage.value = "";
    }
});

const closeModal = () => {
    isOpen.value = false;
    errorMessage.value = "";
    emit("update:isOpen", false);
};

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Escape") {
        closeModal();
    } else if (event.key === "Enter") {
        event.preventDefault();
        if ((event.target as HTMLElement).id === "inputField" && !selectedPerson.value) {
            handleBlur(event as unknown as FocusEvent);
        } else {
            createEmailSenderRule();
        }
    }
};

const createEmailSenderRule = async () => {
    if (!selectedPerson.value) {
        errorMessage.value = i18n.global.t("rulesPage.popUpConstants.errorMessages.noSelectedEmailAddress");
        return;
    }

    const result = await postData("check_sender", {
        email: selectedPerson.value.email,
    });

    if (!result.success) {
        errorMessage.value = result.error as string;
        return;
    }

    let senderId: number;
    if (!result.data.exists) {
        const senderData = {
            name: selectedPerson.value.username || selectedPerson.value.email.split("@")[0],
            email: selectedPerson.value.email,
        };
        const newSenderResult = await postData("create_sender", senderData);
        if (!newSenderResult.success) {
            errorMessage.value = newSenderResult.error as string;
            return;
        }
        senderId = newSenderResult.data.id;
    } else {
        senderId = result.data.senderId;
    }

    let categoryId: number | undefined;
    if (formData.value.category) {
        const categoryResult = await postData("get_category_id/", {
            categoryName: formData.value.category,
        });
        if (!categoryResult.success) {
            errorMessage.value = categoryResult.error as string;
            return;
        }
        categoryId = categoryResult.data.id;
    }

    const ruleData = {
        id: selectedPerson.value,
        username: selectedPerson.value.username,
        email: selectedPerson.value.email,
        category: categoryId,
        priority: formData.value.priority,
        block: formData.value.block,
        sender: senderId.toString(),
    };

    const ruleResult = await postData("user/create_rule/", ruleData);

    if (!ruleResult.success) {
        errorMessage.value = ruleResult.error as string;
    } else {
        displayPopup?.(
            "success",
            i18n.global.t("constants.popUpConstants.successMessages.success"),
            i18n.global.t("rulesPage.popUpConstants.successMessages.ruleCreatedSuccessfully")
        );
        closeModal();
        emit("fetch-rules");
        errorMessage.value = "";
    }
};

function handleBlur(event: FocusEvent) {
    const inputValue = (event.target as HTMLInputElement).value.trim().toLowerCase();
    const emailFormat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (inputValue === "") {
        return;
    }

    if (emailFormat.test(inputValue)) {
        selectedPerson.value = {
            email: inputValue,
            username: inputValue
                .split("@")[0]
                .split(/\.|-/)
                .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
                .join(" "),
        };
        return;
    }
}

const getDisplayValue = (item: unknown): string => {
    if (item === null || item === undefined) {
        return "No contact selected";
    }

    const person = item as EmailSender;

    if (!person) {
        selectedPerson.value = null;
        return "No contact selected";
    }

    if (typeof person === "object" && "username" in person && typeof person.username === "string") {
        return person.email;
    }

    return "Unknown";
};
</script>
