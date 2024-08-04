<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />
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
                                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.164.351.061.686.196.982.397a2.45 2.45 0 0 1 1.097 1.21c.213.615.288 1.274.223 1.933a10.71 10.71 0 0 1-.117 1.707m-1.84-4.457a6.27 6.27 0 0 0-1.523-.205c-.297.014-.58.068-.86.14-.579.135-1.103.372-1.586.707-.564.373-1.014.89-1.372 1.483-.366.598-.606 1.269-.748 1.96m-.595 6.736c-.27-.965-.574-1.909-.929-2.832-.265-.579-.59-1.11-.976-1.617-.373-.486-.802-.902-1.275-1.306m-1.102-.982c-.405-.768-.743-1.57-1.023-2.376-.352-.95-.584-1.961-.641-2.97m-1.41-.494c.104-.672.271-1.337.489-2.005a5.97 5.97 0 0 1 .678-1.817m2.908.953c-.307-.623-.661-1.227-1.063-1.794a4.542 4.542 0 0 0-1.203-1.405"
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
import { ref, computed, onMounted, watch } from "vue"
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/20/solid"
import { Switch, SwitchGroup, SwitchLabel } from "@headlessui/vue"
import { API_BASE_URL, IMPORTANT, INFORMATIVE, USELESS } from "@/global/const"
import NotificationTimer from "@/components/NotificationTimer.vue"
import {
    Combobox,
    ComboboxButton,
    ComboboxInput,
    ComboboxLabel,
    ComboboxOption,
    ComboboxOptions,
} from "@headlessui/vue"
import { XMarkIcon, UserIcon, ArchiveBoxIcon, ShieldCheckIcon, ExclamationCircleIcon } from "@heroicons/vue/24/outline"
import { fetchWithToken } from "@/global/security"
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp"
import { i18n } from "@/global/Settings/preferences"
import { EmailSender } from "@/global/types"

interface FormData {
    id: number
    infoAI: string
    priority: string
    block: boolean
    category: string
    errorMessage: string
}

interface Props {
    isOpen: boolean
    emailSenders: EmailSender[]
    rule: any
    categories: { name: string }[]
}

const props = withDefaults(defineProps<Props>(), {
    emailSenders: () => [],
})

const emit = defineEmits(["update:isOpen", "fetchRules"])

const query = ref("")
const errorMessage = ref("")
const selectedPerson = ref<EmailSender | null>(null)
const currentSelectedPersonUsername = ref("")
const formData = ref<FormData>({
    id: 0,
    infoAI: "",
    priority: "",
    block: false,
    category: "",
    errorMessage: "",
})

const filteredPeople = computed(() => {
    const sendersArray = props.emailSenders.map((sender) => ({
        email: sender.email,
        username: sender.username,
    }))

    if (query.value === "") {
        return sendersArray
    } else {
        return sendersArray.filter(
            (person) =>
                person.username.toLowerCase().includes(query.value.toLowerCase()) ||
                person.email.toLowerCase().includes(query.value.toLowerCase())
        )
    }
})

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown)
})

watch(
    () => props.rule,
    (newVal) => {
        if (newVal) {
            formData.value = {
                id: newVal.id,
                category: newVal.category || "",
                priority: newVal.priority,
                block: newVal.mail_stop,
                infoAI: "",
                errorMessage: "",
            }
            selectedPerson.value = {
                username: newVal.name,
                email: newVal.email,
            }
        }
    },
    { immediate: true }
)

function displayEmailSender(item: unknown): string {
    const person = item as EmailSender | null
    if (person) {
        return person.username ? `${person.username} <${person.email || ""}>` : `<${person.email || ""}>`
    }
    return ""
}

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Escape") {
        closeModal()
    } else if (event.key === "Enter") {
        event.preventDefault()
        if ((event.target as HTMLElement).id === "inputField" && !selectedPerson.value) {
            handleBlur(event as unknown as FocusEvent)
        } else {
            updateUserRule()
        }
    } else if (event.key === "Delete") {
        deleteRule()
    }
}

function handleInputClick() {
    currentSelectedPersonUsername.value = selectedPerson.value?.username || ""
    selectedPerson.value = null
}

function handleBlur(event: FocusEvent) {
    const inputValue = (event.target as HTMLInputElement).value.trim().toLowerCase()
    const emailFormat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    if (inputValue === "") {
        selectedPerson.value = {
            email: currentSelectedPersonUsername.value,
            username: currentSelectedPersonUsername.value,
        }
        return
    } else if (filteredPeople.value.length > 0) {
        return
    }

    if (inputValue && emailFormat.test(inputValue)) {
        selectedPerson.value = {
            email: inputValue,
            username: inputValue
                .split("@")[0]
                .split(/\.|-/)
                .map((p) => p.charAt(0).toUpperCase() + p.slice(1))
                .join(" "),
        }
    } else {
        formData.value.errorMessage = i18n.global.t("rulesPage.popUpConstants.errorMessages.emailFormatIncorrect")
    }
}

async function deleteRule() {
    try {
        if (!formData.value.id) {
            displayPopup(
                "error",
                i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleDeletionError"),
                "Rule ID is required for deletion."
            )
            return
        }

        const deleteUrl = `${API_BASE_URL}user/delete_rules/${formData.value.id}`
        const response = await fetchWithToken(deleteUrl, { method: "DELETE" })

        if (!response) {
            displayPopup(
                "error",
                i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleDeletionError"),
                "No response from server"
            )
            return
        }

        if (!response.ok) {
            displayPopup(
                "error",
                i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleDeletionError"),
                `HTTP error! status: ${response.status}`
            )
            return
        }

        const deleteResponse = await response.json()

        if (deleteResponse.message) {
            selectedPerson.value = null
            displayPopup(
                "success",
                i18n.global.t("constants.popUpConstants.successMessages.success"),
                i18n.global.t("rulesPage.popUpConstants.successMessages.ruleDeletedSuccessfully")
            )
            closeModal()
            emit("fetchRules")
        } else {
            displayPopup(
                "error",
                i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleDeletionError"),
                deleteResponse.error || "Unknown error occurred while deleting the rule"
            )
        }
    } catch (error) {
        console.error("Error in deleting rule:", error)
        displayPopup(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleDeletionError"),
            error instanceof Error ? error.message : String(error)
        )
    }
}

async function postSender() {
    if (!selectedPerson.value) {
        formData.value.errorMessage = i18n.global.t("rulesPage.popUpConstants.errorMessages.noSelectedEmailAddress")
        return null
    }

    const senderData = {
        name: selectedPerson.value.username,
        email: selectedPerson.value.email,
    }

    try {
        const url = `${API_BASE_URL}api/create_sender`
        const response = await fetchWithToken(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(senderData),
        })

        if (!response) {
            displayPopup("error", "Failed to update category", "No response from server")
            closeModal()
            return
        }

        if (!response.ok) {
            displayPopup("error", "Network error", response?.status.toString())
            closeModal()
            return
        }

        const responseData = await response.json()
        return responseData.id
    } catch (error) {
        console.error(`Error in postSender: ${error}`)
        displayPopup(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.senderCreationError"),
            error instanceof Error ? error.message : String(error)
        )
        closeModal()
        return
    }
}

async function checkSenderExists() {
    if (!selectedPerson.value) {
        formData.value.errorMessage = i18n.global.t("rulesPage.popUpConstants.errorMessages.noSelectedEmailAddress")
        return
    }

    const senderData = { email: selectedPerson.value.email }

    try {
        const url = `${API_BASE_URL}api/check_sender`
        const response = await fetchWithToken(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(senderData),
        })

        if (!response) {
            displayPopup(
                "error",
                i18n.global.t("rulesPage.popUpConstants.errorMessages.senderExistenceCheckError"),
                "No response from server"
            )
            return { exists: false }
        }

        const data = await response.json()
        return data.exists ? { exists: data.exists, senderId: data.sender_id } : { exists: false }
    } catch (error) {
        console.error(`Error in checkSenderExists: ${error}`)
        displayPopup(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.senderExistenceCheckError"),
            error instanceof Error ? error.message : String(error)
        )
        closeModal()
        return { exists: false }
    }
}

async function updateUserRule() {
    try {
        if (!formData.value.id) {
            displayPopup(
                "error",
                i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError"),
                i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleIdRequiredForUpdate")
            )
            return
        }

        let { exists, senderId } = (await checkSenderExists()) || { exists: false, senderId: null }

        if (!exists) {
            senderId = await postSender()
        }

        if (!senderId) {
            displayPopup(
                "error",
                i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError"),
                "Failed to obtain sender ID"
            )
            return
        }

        let ruleData: any = { ...formData.value, sender: senderId, infoAI: "" }

        if (formData.value.category) {
            const categoryUrl = `${API_BASE_URL}api/get_category_id/`
            const categoryResponse = await fetchWithToken(categoryUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ categoryName: formData.value.category }),
            })

            if (!categoryResponse || !categoryResponse.ok) {
                displayPopup(
                    "error",
                    i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError"),
                    "Failed to fetch category ID"
                )
                return
            }

            const categoryData = await categoryResponse.json()
            ruleData.category = categoryData.id
        }

        const ruleResponse = await fetchWithToken(`${API_BASE_URL}user/update_rule/`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(ruleData),
        })

        if (!ruleResponse || !ruleResponse.ok) {
            displayPopup(
                "error",
                i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError"),
                `HTTP error! status: ${ruleResponse?.status}`
            )
            return
        }

        const ruleResponseData = await ruleResponse.json()

        if ("error" in ruleResponseData) {
            displayPopup(
                "error",
                i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError"),
                ruleResponseData.error === "A rule already exists for that sender"
                    ? i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleAlreadyExistsForSender")
                    : ruleResponseData.error
            )
            return
        }

        selectedPerson.value = null
        displayPopup(
            "success",
            i18n.global.t("constants.popUpConstants.successMessages.success"),
            i18n.global.t("rulesPage.popUpConstants.successMessages.ruleUpdatedSuccessfully")
        )
        closeModal()
        emit("fetchRules")
    } catch (error) {
        console.error("Error in updating rule:", error)
        displayPopup(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.ruleUpdateError"),
            error instanceof Error ? error.message : String(error)
        )
    } finally {
        closeModal()
    }
}

function closeModal() {
    formData.value.errorMessage = ""
    emit("update:isOpen", false)
}

const showNotification = ref(false)
const notificationTitle = ref("")
const notificationMessage = ref("")
const backgroundColor = ref("")
const timerId = ref<NodeJS.Timeout | null>(null)

function displayPopup(type: "success" | "error", title: string, message: string) {
    if (type === "error") {
        displayErrorPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message)
    } else {
        displaySuccessPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message)
    }
    timerId.value = setTimeout(dismissPopup, 4000)
}

function dismissPopup() {
    showNotification.value = false
    if (timerId.value !== null) {
        clearTimeout(timerId.value)
    }
}
</script>
