<template>
    <transition name="modal-fade">
        <div
            @click.self="closeModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            v-if="isOpen"
        >
            <div class="bg-white rounded-lg relative w-[450px]">
                <slot></slot>
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
                            {{ $t("rulesPage.modals.updateRule.modifyTheRule") }}
                        </p>
                    </div>
                </div>
                <div class="flex flex-col gap-4 px-8 py-6">
                    <Combobox as="div" v-model="selectedPerson">
                        <p class="text-red-500" v-if="errorMessage">{{ errorMessage }}</p>
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
                                :display-value="displayEmailSender"
                                @blur="handleBlur($event)"
                                @click="handleInputClick"
                                @keydown="handleKeyDown($event)"
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
                            class="ml-auto rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                            @click="updateUserRule"
                        >
                            {{ $t("constants.userActions.modify") }}
                        </button>
                        <button
                            type="button"
                            class="inline-flex w-full justify-center items-center gap-x-1 rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 sm:w-auto"
                            @click="deleteRule"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke-width="1.5"
                                stroke="currentColor"
                                class="w-6 h-6"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                                />
                            </svg>
                            {{ $t("constants.userActions.delete") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, inject } from "vue";
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/20/solid";
import { Switch, SwitchGroup, SwitchLabel } from "@headlessui/vue";
import { IMPORTANT, INFORMATIVE, USELESS } from "@/global/const";
import { postData, putData, deleteData } from "@/global/fetchData";
import {
    Combobox,
    ComboboxButton,
    ComboboxInput,
    ComboboxLabel,
    ComboboxOption,
    ComboboxOptions,
} from "@headlessui/vue";
import { XMarkIcon, UserIcon, ArchiveBoxIcon, ShieldCheckIcon, ExclamationCircleIcon } from "@heroicons/vue/24/outline";
import { i18n } from "@/global/preferences";
import { EmailSender, Category } from "@/global/types";
import { RuleData } from "../utils/types";

interface FormData {
    id?: string;
    category: string;
    priority: string;
    block: boolean;
    infoAI: string;
    errorMessage: string;
}

interface Props {
    isOpen: boolean;
    rule: RuleData | null;
    categories: Category[];
    emailSenders: EmailSender[];
}

const props = withDefaults(defineProps<Props>(), {
    emailSenders: () => [],
    rule: null,
});

const emit = defineEmits<{
    (e: "update:isOpen", value: boolean): void;
    (e: "fetch-rules"): void;
}>();

const query = ref("");
const errorMessage = ref("");
const currentSelectedPersonUsername = ref("");
const selectedPerson = ref<EmailSender | null>(null);
const formData = ref<FormData>({
    category: "",
    priority: "",
    block: false,
    infoAI: "",
    errorMessage: "",
});

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const filteredPeople = computed(() => {
    const sendersArray = props.emailSenders.map((sender) => ({
        email: sender.email,
        username: sender.username,
    }));

    return query.value === ""
        ? sendersArray
        : sendersArray.filter(
              (person) =>
                  person.username.toLowerCase().includes(query.value.toLowerCase()) ||
                  person.email.toLowerCase().includes(query.value.toLowerCase())
          );
});

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

watch(
    () => props.rule,
    (newVal) => {
        if (newVal) {
            formData.value = {
                id: newVal.id,
                category: newVal.category || "",
                priority: newVal.priority,
                block: newVal.mailStop,
                infoAI: "",
                errorMessage: "",
            };
            selectedPerson.value = {
                username: newVal.username,
                email: newVal.email,
            };
        }
    },
    { immediate: true }
);

function displayEmailSender(item: unknown): string {
    const person = item as EmailSender | null;
    return person ? (person.username ? `${person.username} <${person.email || ""}>` : `<${person.email || ""}>`) : "";
}

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Escape") {
        closeModal();
    } else if (event.key === "Enter") {
        event.preventDefault();
        if ((event.target as HTMLElement).id === "inputField" && !selectedPerson.value) {
            handleBlur(event as unknown as FocusEvent);
        } else {
            updateUserRule();
        }
    } else if (event.key === "Delete") {
        deleteRule();
    }
}

function handleInputClick() {
    currentSelectedPersonUsername.value = selectedPerson.value?.username || "";
    selectedPerson.value = null;
}

function handleBlur(event: FocusEvent) {
    const inputValue = (event.target as HTMLInputElement).value.trim().toLowerCase();
    const emailFormat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (inputValue === "") {
        selectedPerson.value = {
            email: currentSelectedPersonUsername.value,
            username: currentSelectedPersonUsername.value,
        };
        return;
    } else if (filteredPeople.value.length > 0) {
        return;
    }

    if (inputValue && emailFormat.test(inputValue)) {
        selectedPerson.value = {
            email: inputValue,
            username: inputValue
                .split("@")[0]
                .split(/\.|-/)
                .map((p) => p.charAt(0).toUpperCase() + p.slice(1))
                .join(" "),
        };
    } else {
        formData.value.errorMessage = i18n.global.t("rulesPage.popUpConstants.errorMessages.emailFormatIncorrect");
    }
}

async function deleteRule() {
    if (!formData.value.id) {
        displayPopup?.(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleDeletionError"),
            "Rule ID is required for deletion."
        );
        return;
    }

    const result = await deleteData(`user/delete_rules/${formData.value.id}/`);

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleDeletionError"),
            result.error as string
        );
        return;
    }

    selectedPerson.value = null;
    displayPopup?.(
        "success",
        i18n.global.t("constants.popUpConstants.successMessages.success"),
        i18n.global.t("rulesPage.popUpConstants.successMessages.ruleDeletedSuccessfully")
    );
    closeModal();
    emit("fetch-rules");
}

async function postSender(): Promise<number | null> {
    if (!selectedPerson.value) {
        formData.value.errorMessage = i18n.global.t("rulesPage.popUpConstants.errorMessages.noSelectedEmailAddress");
        return null;
    }

    const senderData = {
        name: selectedPerson.value.username,
        email: selectedPerson.value.email,
    };

    const result = await postData(`create_sender`, senderData);

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.senderCreationError"),
            result.error as string
        );
        closeModal();
        return null;
    }

    return result.data.id;
}

async function checkSenderExists(): Promise<{ exists: boolean; senderId?: number }> {
    if (!selectedPerson.value) {
        formData.value.errorMessage = i18n.global.t("rulesPage.popUpConstants.errorMessages.noSelectedEmailAddress");
        return { exists: false };
    }

    const senderData = { email: selectedPerson.value.email };

    const result = await postData(`check_sender`, senderData);

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.senderExistenceCheckError"),
            result.error as string
        );
        return { exists: false };
    }

    return result.data.exists ? { exists: result.data.exists, senderId: result.data.senderId } : { exists: false };
}

async function updateUserRule() {
    if (!formData.value.id) {
        displayPopup?.(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError"),
            i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleIdRequiredForUpdate")
        );
        return;
    }

    let { exists, senderId } = await checkSenderExists();

    console.log("DEBUG exists ", exists, "senderId ", senderId);

    if (!exists) {
        const newSenderId = await postSender();
        if (newSenderId === null) {
            displayPopup?.(
                "error",
                i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError"),
                "Failed to create new sender"
            );
            return;
        }
        senderId = newSenderId;
    }

    if (senderId === undefined) {
        displayPopup?.(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError"),
            "Failed to obtain sender ID"
        );
        return;
    }

    let ruleData: any = { ...formData.value, sender: senderId, infoAI: "" };

    if (formData.value.category) {
        const categoryResult = await postData(`get_category_id/`, { categoryName: formData.value.category });

        if (!categoryResult.success) {
            displayPopup?.(
                "error",
                i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError"),
                "Failed to fetch category ID"
            );
            return;
        }

        ruleData.category = categoryResult.data.id;
    }

    const ruleResult = await putData(`user/update_rule/`, ruleData);

    if (!ruleResult.success) {
        displayPopup?.(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError"),
            ruleResult.error === "A rule already exists for that sender"
                ? i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleAlreadyExistsForSender")
                : (ruleResult.error as string)
        );
        return;
    }

    selectedPerson.value = null;
    displayPopup?.(
        "success",
        i18n.global.t("constants.popUpConstants.successMessages.success"),
        i18n.global.t("rulesPage.popUpConstants.successMessages.ruleUpdatedSuccessfully")
    );
    closeModal();
    emit("fetch-rules");
}

function closeModal() {
    formData.value.errorMessage = "";
    emit("update:isOpen", false);
}
</script>
