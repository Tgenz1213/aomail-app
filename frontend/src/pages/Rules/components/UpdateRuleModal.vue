<template>
    <transition name="modal-fade">
        <div
            @click.self="closeModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
            v-if="isOpen"
        >
            <div class="bg-white rounded-lg relative w-[600px] max-h-[90vh] overflow-y-auto">
                <!-- Header -->
                <div class="sticky top-0 z-10 bg-white rounded-t-lg border-b border-gray-200">
                    <div class="flex items-center justify-between p-4">
                        <h2 class="text-lg font-semibold text-gray-900">
                            {{ $t("rulesPage.modals.updateRule.modifyTheRule") }}
                        </h2>
                        <button @click="closeModal" class="text-gray-400 hover:text-gray-500">
                            <XMarkIcon class="h-6 w-6" />
                        </button>
                    </div>
                </div>

                <!-- Content -->
                <div class="p-4 space-y-6">
                    <div v-if="errorMessage" class="text-red-600 text-sm mb-4">
                        {{ errorMessage }}
                    </div>

                    <!-- Logical Operator -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Logical Operator</label>
                        <select
                            v-model="formData.logicalOperator"
                            class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                        >
                            <option value="AND">AND - All conditions must match</option>
                            <option value="OR">OR - Any condition can match</option>
                        </select>
                    </div>

                    <!-- Email Sender -->
                    <div>
                        <div class="flex space-x-1 items-center">
                            <UserIcon class="w-4 h-4" />
                            <label class="block text-sm font-medium text-gray-900">
                                {{ $t("rulesPage.contactField") }}
                            </label>
                        </div>
                        <Combobox as="div" v-model="selectedPerson">
                            <div class="relative mt-2">
                                <ComboboxInput
                                    id="inputField"
                                    class="w-full rounded-md border-0 bg-white py-1.5 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                                    @change="query = $event.target.value"
                                    :display-value="displayEmailSender"
                                    @blur="handleBlur($event)"
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
                    </div>

                    <!-- Category -->
                    <div>
                        <div class="flex space-x-1 items-center">
                            <ArchiveBoxIcon class="w-4 h-4" />
                            <label class="block text-sm font-medium text-gray-900">
                                {{ $t("constants.category") }}
                            </label>
                        </div>
                        <select
                            v-model="formData.actionSetCategory"
                            class="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-gray-500 sm:text-sm sm:leading-6"
                        >
                            <option value="">{{ $t("constants.ruleModalConstants.noCategoryDefined") }}</option>
                            <option v-for="category in categories" :key="category.name" :value="category.name">
                                {{ category.name }}
                            </option>
                        </select>
                    </div>

                    <!-- Priority -->
                    <div>
                        <div class="flex space-x-1 items-center">
                            <ExclamationCircleIcon class="w-4 h-4" />
                            <label class="block text-sm font-medium text-gray-900">
                                {{ $t("rulesPage.priorityField") }}
                            </label>
                        </div>
                        <select
                            v-model="formData.actionSetPriority"
                            class="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-gray-500 sm:text-sm sm:leading-6"
                        >
                            <option value="">{{ $t("constants.ruleModalConstants.noPriority") }}</option>
                            <option :value="IMPORTANT">{{ $t("constants.ruleModalConstants.important") }}</option>
                            <option :value="INFORMATIVE">{{ $t("constants.ruleModalConstants.informative") }}</option>
                            <option :value="USELESS">{{ $t("constants.ruleModalConstants.useless") }}</option>
                        </select>
                    </div>

                    <!-- Block Switch -->
                    <SwitchGroup as="div" class="flex items-center pt-2">
                        <Switch
                            v-model="formData.actionDelete"
                            :class="[
                                formData.actionDelete ? 'bg-gray-500' : 'bg-gray-200',
                                'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2',
                            ]"
                        >
                            <span
                                aria-hidden="true"
                                :class="[
                                    formData.actionDelete ? 'translate-x-5' : 'translate-x-0',
                                    'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                                ]"
                            />
                        </Switch>
                        <SwitchLabel as="span" class="ml-3 text-sm">
                            <span class="font-medium text-gray-900">
                                {{ $t("constants.ruleModalConstants.blockTheEmails") }}
                            </span>
                        </SwitchLabel>
                        <ShieldCheckIcon class="ml-1 w-4 h-4" />
                    </SwitchGroup>

                    <!-- Action Buttons -->
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
import { ref, computed, onMounted, watch, inject, Ref } from "vue";
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

interface FormData extends RuleData {
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
const totalRules = inject<Ref<number>>("totalRules") || ref(0);
const formData = ref<FormData>({
    id: -1,
    logicalOperator: "AND",
    domains: [],
    senderEmails: [],
    hasAttachements: false,
    categories: [],
    priorities: [],
    answers: [],
    relevances: [],
    flags: [],
    emailDealWith: "",
    actionTransferRecipients: [],
    actionSetFlags: [],
    actionMarkAs: [],
    actionDelete: false,
    actionSetCategory: undefined,
    actionSetPriority: "",
    actionSetRelevance: "",
    actionSetAnswer: "",
    actionReplyPrompt: "",
    actionReplyRecipients: [],
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
                logicalOperator: newVal.logicalOperator || "AND",
                domains: newVal.domains || [],
                senderEmails: newVal.senderEmails || [],
                hasAttachements: newVal.hasAttachements || false,
                categories: newVal.categories || [],
                priorities: newVal.priorities || [],
                answers: newVal.answers || [],
                relevances: newVal.relevances || [],
                flags: newVal.flags || [],
                emailDealWith: newVal.emailDealWith || "",
                actionTransferRecipients: newVal.actionTransferRecipients || [],
                actionSetFlags: newVal.actionSetFlags || [],
                actionMarkAs: newVal.actionMarkAs || [],
                actionDelete: newVal.actionDelete || false,
                actionSetCategory: newVal.actionSetCategory,
                actionSetPriority: newVal.actionSetPriority || "",
                actionSetRelevance: newVal.actionSetRelevance || "",
                actionSetAnswer: newVal.actionSetAnswer || "",
                actionReplyPrompt: newVal.actionReplyPrompt || "",
                actionReplyRecipients: newVal.actionReplyRecipients || [],
                errorMessage: "",
            };
            selectedPerson.value = newVal.senderEmails?.[0]
                ? {
                      username: newVal.senderEmails[0],
                      email: newVal.senderEmails[0],
                  }
                : null;
        }
    },
    { immediate: true }
);

function displayEmailSender(item: unknown): string {
    const person = item as EmailSender | null;

    if (!person) {
        selectedPerson.value = null;
        return "";
    }

    return person.email;
}

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Escape") {
        closeModal();
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
        errorMessage.value = i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleDeletionError");
        return;
    }

    const result = await deleteData(`user/rules/`, { ids: [formData.value.id] });

    if (!result.success) {
        errorMessage.value = result.error as string;
        return;
    }

    totalRules.value -= 1;
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
        errorMessage.value = i18n.global.t("rulesPage.popUpConstants.errorMessages.noSelectedEmailAddress");
        return null;
    }

    const senderData = {
        name: selectedPerson.value.username,
        email: selectedPerson.value.email,
    };

    const result = await postData(`create_sender`, senderData);

    if (!result.success) {
        errorMessage.value = result.error as string;
        return null;
    }

    return result.data.id;
}

async function updateUserRule() {
    if (!formData.value.id) {
        errorMessage.value = i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError");
        return;
    }

    if (selectedPerson.value) {
        formData.value.senderEmails = [selectedPerson.value.email];
    }

    const result = await putData(`user/rules/`, { ids: [formData.value.id], ...formData.value });

    if (!result.success) {
        errorMessage.value = result.error as string;
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
    errorMessage.value = "";
    emit("update:isOpen", false);
}
</script>
