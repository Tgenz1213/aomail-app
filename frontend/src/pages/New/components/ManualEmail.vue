<template>
    <div class="flex flex-col h-full w-full">
        <div class="flex items-center h-[65px] justify-center lg:py-5 2xl:h-[80px] min-h-8">
            <div class="flex gap-x-3 items-center">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1"
                    stroke="currentColor"
                    class="w-6 h-6 2xl:w-7 2xl:h-7"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672ZM12 2.25V4.5m5.834.166-1.591 1.591M20.25 10.5H18M7.757 14.743l-1.59 1.59M6 10.5H3.75m4.007-4.243-1.59-1.59"
                    />
                </svg>
                <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500">
                    {{ $t("constants.userActions.enterManually") }}
                </h1>
            </div>
        </div>
        <form class="flex-1 flex flex-col w-full px-10 pt-4 2xl:px-14 2xl:pt-6 overflow-hidden">
            <div class="flex flex-col space-y-5 h-full w-full">
                <div class="">
                    <!--Recipie List and CC List-->
                    <div class="flex flex-wrap">
                        <!-- Main Recipients List -->
                        <div v-if="selectedPeople.length > 0" class="flex items-center mb-1">
                            <div
                                v-for="person in selectedPeople"
                                :key="person.email"
                                class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1 2xl:px-3 2xl:py-2 2xl:mr-2"
                            >
                                {{ person.username || person.email }}
                                <button @click="removePersonFromMain(person)">×</button>
                            </div>
                        </div>
                        <!-- CC Recipients List -->
                        <div v-if="selectedCC.length > 0" class="flex items-center mb-1">
                            <div
                                v-for="person in selectedCC"
                                :key="person.email"
                                class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1 2xl:px-3 2xl:py-2 2xl:mr-2"
                            >
                                <span class="font-semibold mr-1 2xl:mr-2">
                                    {{ $t("constants.sendEmailConstants.carbonCopyInitialsTwoDots") }}
                                </span>
                                {{ person.username || person.email }}
                                <button @click="removePersonFromCC(person)">×</button>
                            </div>
                        </div>
                        <!-- CCI Recipients List -->
                        <div v-if="selectedCCI.length > 0" class="flex items-center mb-1">
                            <div
                                v-for="person in selectedCCI"
                                :key="person.email"
                                class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1 2xl:px-3 2xl:py-2 2xl:mr-2"
                            >
                                <span class="font-semibold mr-1 2xl:mr-2">
                                    {{ $t("constants.sendEmailConstants.blindCarbonCopyInitialsTwoDots") }}
                                </span>
                                {{ person.username || person.email }}
                                <button @click="removePersonFromCCI(person)">×</button>
                            </div>
                        </div>
                    </div>
                    <div class="flex items-stretch gap-1 2xl:gap-2">
                        <div class="flex-grow">
                            <div class="relative items-stretch">
                                <div class="relative w-full">
                                    <div
                                        v-if="!isFocused2"
                                        class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 2xl:ml-3"
                                    >
                                        <UserGroupIcon class="w-4 h-4 pointer-events-none 2xl:w-5 2xl:h-5" />
                                        <label
                                            for="email"
                                            class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none 2xl:text-base"
                                        >
                                            {{ $t("constants.recipient") }}
                                        </label>
                                    </div>
                                    <Combobox as="div" v-model="selectedPerson" @update:model-value="personSelected">
                                        <ComboboxInput
                                            id="recipients"
                                            class="w-full h-10 2xl:h-11 rounded-md border-0 bg-white py-2 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6 2xl:py-3 2xl:pl-4 2xl:pr-14 2xl:text-base"
                                            @change="query = $event.target.value"
                                            :display-value="(person: any) => person?.name"
                                            @focus="handleFocusDestinary"
                                            @blur="handleBlur2($event)"
                                            @keydown.enter="handleEnterKey"
                                        />
                                        <ComboboxButton
                                            class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none 2xl:px-3"
                                        >
                                            <ChevronUpDownIcon
                                                class="h-5 w-5 text-gray-400 2xl:h-6 2xl:w-6"
                                                aria-hidden="true"
                                            />
                                        </ComboboxButton>
                                        <ComboboxOptions
                                            v-if="filteredPeople.length > 0"
                                            class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm 2xl:text-base"
                                            style="z-index: 21"
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
                                    </Combobox>
                                </div>
                            </div>
                        </div>
                        <div class="flex gap-1 2xl:gap-2">
                            <button
                                type="button"
                                @click="toggleCC"
                                :class="[
                                    'inline-flex items-center gap-x-1.5 rounded-md px-2.5 py-1.5 text-sm font-semibold hover:bg-gray-600 hover:text-white',
                                    activeType === 'CC' ? 'bg-gray-500 text-white' : 'bg-gray-100 text-gray-400',
                                ]"
                                class="ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 2xl:px-3 2xl:py-2 2xl:text-base"
                            >
                                {{ $t("newPage.carbonCopyInitials") }}
                            </button>
                            <button
                                type="button"
                                @click="toggleCCI"
                                :class="[
                                    'inline-flex items-center gap-x-1.5 rounded-md px-2.5 py-1.5 text-sm font-semibold hover:bg-gray-600 hover:text-white',
                                    activeType === 'CCI' ? 'bg-gray-500 text-white' : 'bg-gray-100 text-gray-400',
                                ]"
                                class="ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 2xl:px-3 2xl:py-2 2xl:text-base"
                            >
                                {{ $t("newPage.blindCarbonCopyInitials") }}
                            </button>
                        </div>
                    </div>
                </div>
                <div class="">
                    <div class="flex flex-wrap">
                        <div
                            v-for="(file, index) in uploadedFiles"
                            :key="index"
                            class="flex items-center mb-1 mr-1 bg-gray-200 rounded px-2 py-1 2xl:px-3 2xl:py-2 2xl:mr-2"
                        >
                            {{ file.name }}
                            <button @click="removeFile(index)">×</button>
                        </div>
                    </div>
                    <div class="flex items-stretch gap-1 2xl:gap-2">
                        <div class="flex-grow">
                            <div
                                class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 w-full"
                            >
                                <div class="relative w-full">
                                    <div
                                        v-if="!isFocused && !inputValue"
                                        class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 2xl:ml-3 z-10"
                                    >
                                        <Bars2Icon class="w-4 h-4 pointer-events-none 2xl:w-5 2xl:h-5" />
                                        <label
                                            for="username"
                                            class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none 2xl:text-base"
                                        >
                                            {{ $t("constants.subject") }}
                                        </label>
                                    </div>
                                    <input
                                        id="objectInput"
                                        v-model="inputValue"
                                        type="text"
                                        class="block h-10 2xl:h-11 flex-1 border-0 bg-transparent py-2 pl-3 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6 w-full z-20 relative 2xl:py-3 2xl:pl-4 2xl:text-base"
                                        @focus="handleFocusObject"
                                        @blur="handleBlur"
                                    />
                                </div>
                            </div>
                        </div>
                        <div class="flex">
                            <input type="file" ref="fileInput" @change="handleFileUpload" multiple hidden />
                            <button
                                @click="triggerFileInput"
                                type="button"
                                class="inline-flex items-center gap-x-1.5 rounded-md bg-gray-100 px-2.5 py-1.5 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-300 shadow-sm hover:ring-transparent hover:bg-gray-600 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 2xl:px-3 2xl:py-2 2xl:text-base"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1.5"
                                    stroke="currentColor"
                                    class="w-6 h-6 2xl:w-7 2xl:h-7"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13"
                                    />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="flex flex-col h-full space-y-5 pb-4 2xl:pb-6 overflow-hidden">
                    <div class="flex-1 overflow-hidden h-screen border-b-2 rounded-lg">
                        <div id="editor-container" class="flex-1 h-full w-full flex flex-col border-solid">
                            <div id="editor" class="flex-1"></div>
                        </div>
                    </div>
                    <div class="flex gap-x-2 mb-5 2xl:gap-3 2xl:mb-6 items-stretch">
                        <div class="relative flex-grow flex items-stretch">
                            <Listbox as="div" v-model="emailSelected" class="w-full flex flex-col">
                                <ListboxButton
                                    class="relative w-full h-full cursor-default rounded-md bg-white px-6 py-2 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6 2xl:px-7 2xl:py-3 2xl:text-base"
                                >
                                    <span class="block truncate">{{ emailSelected }}</span>
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
                                        class="absolute z-10 mb-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm bottom-full"
                                    >
                                        <ListboxOption
                                            as="template"
                                            v-for="email in emailsLinked"
                                            :key="email.email"
                                            :value="email.email"
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
                                                    {{ email.email }}
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
                            </Listbox>
                        </div>
                        <div class="inline-flex rounded-lg shadow-lg items-stretch">
                            <button
                                @click="sendEmail"
                                class="bg-gray-700 rounded-l-lg px-6 py-2 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center 2xl:px-7 2xl:py-3 2xl:text-lg"
                            >
                                {{ $t("constants.userActions.send") }}
                                <PaperAirplaneIcon class="w-4 2xl:w-5" aria-hidden="true" />
                            </button>
                            <Menu as="div" class="relative -ml-px block items-stretch">
                                <MenuButton
                                    class="relative inline-flex items-center rounded-r-lg px-2 py-2 text-white border-l border-gray-300 bg-gray-700 hover:bg-gray-900 focus:z-10 2xl:px-3 2xl:py-3"
                                >
                                    <span class="sr-only">{{ $t("newPage.openOptions") }}</span>
                                    <ChevronDownIcon class="h-8 w-5 2xl:h-9 2xl:w-6" aria-hidden="true" />
                                </MenuButton>
                                <transition
                                    enter-active-class="transition ease-out duration-100"
                                    enter-from-class="transform opacity-0 -translate-y-2"
                                    enter-to-class="transform opacity-100 translate-y-0"
                                    leave-active-class="transition ease-in duration-75"
                                    leave-from-class="transform opacity-100 translate-y-0"
                                    leave-to-class="transform opacity-0 -translate-y-2"
                                >
                                    <MenuItems
                                        class="absolute right-0 z-10 -mr-1 bottom-full mb-2 w-56 origin-bottom-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                                    >
                                        <div class="py-1">
                                            <button
                                                :class="[
                                                    active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                                                    'block px-4 py-2 text-sm',
                                                ]"
                                                @click="scheduleSend"
                                                >
                                                Schedule send
                                                </button> </div>
                                    </MenuItems>
                                </transition>
                            </Menu>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">
import { MICROSOFT } from "@/global/const";
import { postData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import { Contact, EmailLinked, Recipient, UploadedFile } from "@/global/types";
import Quill from "quill";
import { computed, inject, ref, Ref } from "vue";
import { Menu, MenuButton, MenuItems } from "@headlessui/vue";
import {
    Combobox,
    ComboboxButton,
    ComboboxInput,
    ComboboxOption,
    Listbox,
    ListboxButton,
    ListboxOptions,
    ListboxOption,
    // ChevronUpDownIcon,
    ComboboxOptions,
} from "@headlessui/vue";

const selectedPerson = ref("");
const isFocused2 = ref(false);
const query = ref("");
const inputValue = ref("");
const active = ref(false);

const isFocused = ref(false); 
function handleFocusObject() {
    isFocused.value = true;
}
function handleBlur() {
    isFocused.value = false;
}


function handleFocusDestinary() {
    // isFocused2.value = true;
}


function toggleCC() { 
    activeType.value = activeType.value === "CC" ? "" : "CC";
}

function toggleCCI() {  
    activeType.value = activeType.value === "CCI" ? "" : "CCI";
}

const getFilteredPeople = (query: Ref<string>, contacts: any) => {
    return computed(() => {
        if (query.value === "") {
            return contacts;
        } else {
            return contacts.filter((person: Recipient) => {
                if (!person.username) {
                    if (person.email) {
                        person.username = person.email
                            .split("@")[0]
                            .split(/\.|-/)
                            .map((p) => p.charAt(0).toUpperCase() + p.slice(1))
                            .join(" ");
                    } else {
                        person.username = "";
                    }
                }
                const usernameLower = person.username ? person.username.toLowerCase() : "";
                const emailLower = person.email ? person.email.toLowerCase() : "";
                return (
                    usernameLower.includes(query.value.toLowerCase()) || emailLower.includes(query.value.toLowerCase())
                );
            });
        }
    });
};


function handleEnterKey(event: any) {
    // // Allow pressing Enter with Shift to create a line break
    // if (event.target.id === "dynamicTextarea" && event.key === "Enter" && !event.shiftKey) {
    //     event.preventDefault();
    //     handleAIClick();
    // } else if (isFocused2.value) {
    //     event.preventDefault();
    //     handleBlur2(event);
    //     // the user is still on the input
    //     handleFocusDestinary();
    // }
}

function handleBlur2(event: any) {
    // // Checks for a valid input email and adds it to the recipients list
    // isFocused2.value = false;
    // const inputValue = event.target.value.trim().toLowerCase();
    // const emailFormat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // if (inputValue && emailFormat.test(inputValue)) {
    //     if (!contacts.find((person) => person.email === inputValue)) {
    //         const newPerson = { username: "", email: inputValue };
    //         contacts.push(newPerson);
    //         selectedPeople.value.push(newPerson);
    //     }
    // } else if (!filteredPeople.value.length && inputValue) {
    //     // Show the pop-up
    //     backgroundColor = "bg-red-200/[.89] border border-red-400";
    //     notificationTitle.value = t("constants.popUpConstants.errorMessages.invalidEmail");
    //     notificationMessage.value = t("constants.popUpConstants.errorMessages.emailFormatIncorrect");
    //     displayPopup();
    // }
}

function personSelected(person: any) {
    // if (!person) return;

    // switch (activeType.value) {
    //     case "CC":
    //         if (!selectedCC.value.includes(person)) {
    //             selectedCC.value.push(person);
    //         }
    //         break;
    //     case "CCI":
    //         if (!selectedCCI.value.includes(person)) {
    //             selectedCCI.value.push(person);
    //         }
    //         break;
    //     default:
    //         if (!selectedPeople.value.includes(person)) {
    //             selectedPeople.value.push(person);
    //             // console.log("DEBUG People -->", selectedPeople.value);
    //         }
    // }

    // if (isFirstTimeDestinary.value) {
    //     // askContent(); OLD
    //     stepContainer = 1;
    //     askContent(); // NEW (move the 2 buttons len + formality)
    //     isFirstTimeDestinary.value = false;
    // }

    // selectedPerson.value = null;

}




const contacts =  inject<Ref<Contact[]>>("contacts", ref([]))
const emailsLinked = inject<Ref<EmailLinked[]>>("emailsLinked", ref([]));
const emailSelected = inject<Ref<string>>("emailSelected") || ref("");
const selectedPeople = inject<Ref<Recipient[]>>("selectedPeople") || ref([]);
const selectedCC = inject<Ref<Recipient[]>>("selectedCC") || ref([]);
const selectedCCI = inject<Ref<Recipient[]>>("selectedCCI") || ref([]);
const quill = inject<Ref<Quill | null>>("quill");
const stepContainer = inject<Ref<number>>("stepContainer") || ref(0);
const fileInput = ref(null);
const uploadedFiles = ref<UploadedFile[]>([]);
let fileObjects = ref<File[]>([]);
const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25MB, Gmail's limit
const activeType = ref("");



const filteredPeople = getFilteredPeople(query, contacts);

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
// todo: trigger each time an email is selected
// function setEmailSelected() {
//     localStorage.setItem("email", emailSelected.value);
// }

function removePersonFromMain(personToRemove: Recipient) {
    selectedPeople.value = selectedPeople.value.filter((person) => person !== personToRemove);
}

function removePersonFromCC(personToRemove: Recipient) {
    selectedCC.value = selectedCC.value.filter((person) => person !== personToRemove);
}

function removePersonFromCCI(personToRemove: Recipient) {
    selectedCCI.value = selectedCCI.value.filter((person) => person !== personToRemove);
}

async function scheduleSend() {
    // if (!AIContainer.value || !quill?.value) return;
    // const emailSubject = inputValue.value;
    // const emailBody = quill.value.root.innerHTML;

    // for (const tupleEmail of emailsLinked.value) {
    //     if (emailSelected.value === tupleEmail.email && tupleEmail.typeApi !== MICROSOFT) {
    //         displayPopup?.(
    //             "error",
    //             "Email service provider not supported",
    //             "Scheduled send is only available for Outlook accounts"
    //         );
    //         return;
    //     }
    // }

    // if (!emailSubject.trim()) {
    //     displayPopup?.(
    //         "error",
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoSubject")
    //     );
    //     return;
    // } else if (emailBody == "<p><br></p>") {
    //     displayPopup?.(
    //         "error",
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoObject")
    //     );
    //     return;
    // } else if (selectedPeople.value.length == 0) {
    //     displayPopup?.(
    //         "error",
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoRecipient")
    //     );
    //     return;
    // }

    // const formData = new FormData();

    // formData.append("subject", emailSubject);
    // formData.append("message", emailBody);
    // fileObjects.value.forEach((file) => formData.append("attachments", file));

    // selectedPeople.value.forEach((person) => formData.append("to", person.email));
    // if (selectedCC.value.length > 0) {
    //     selectedCC.value.forEach((person) => formData.append("cc", person.email));
    // }
    // if (selectedCCI.value.length > 0) {
    //     selectedCCI.value.forEach((person) => formData.append("cci", person.email));
    // }
    // formData.append("email", emailSelected.value);
    // // TODO: add a modal - for now its HARD coded values! DO NOT PUSH THAT IN PRODUCTION
    // formData.append("datetime", "2024-07-02T10:00:00Z");

    // const result = await postData(`user/social_api/send_schedule_email/`, {
    //     body: formData,
    // });

    // if (!result.success) {
    //     displayPopup?.(
    //         "error",
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
    //         result.error as string
    //     );
    // }

    // displayPopup?.("success", "Email scheduled successfully!", "Your email will be send on time");

    // inputValue.value = "";
    // quill.value.root.innerHTML = "";
    // selectedPeople.value = [];
    // selectedCC.value = [];
    // selectedCCI.value = [];
    // stepContainer.value = 0;
    // AIContainer.value.innerHTML = "";
    // AIContainer.value = document.getElementById("AIContainer");

    // localStorage.removeItem("uploadedFiles");
    // uploadedFiles.value = [];
    // fileObjects.value = [];

    // const message = i18n.global.t("constants.sendEmailConstants.emailRecipientRequest");
    // const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;

    // displayMessage(message, ai_icon);
}

async function sendEmail() {
    // if (!quill?.value) return;
    // const emailSubject = inputValue.value;
    // const emailBody = quill.value.root.innerHTML;

    // if (!emailSubject.trim()) {
    //     displayPopup?.(
    //         "error",
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoSubject")
    //     );
    //     return;
    // }
    // if (emailBody === "<p><br></p>") {
    //     displayPopup?.(
    //         "error",
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoObject")
    //     );
    //     return;
    // }
    // if (selectedPeople.value.length === 0) {
    //     displayPopup?.(
    //         "error",
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendErrorNoRecipient")
    //     );
    //     return;
    // }

    // const formData = new FormData();

    // formData.append("subject", emailSubject);
    // formData.append("message", emailBody);
    // fileObjects.value.forEach((file) => formData.append("attachments", file));

    // selectedPeople.value.forEach((person) => formData.append("to", person.email));
    // if (selectedCC.value.length > 0) {
    //     selectedCC.value.forEach((person) => formData.append("cc", person.email));
    // }
    // if (selectedCCI.value.length > 0) {
    //     selectedCCI.value.forEach((person) => formData.append("cci", person.email));
    // }
    // formData.append("email", emailSelected.value);

    // const result = await postData(`user/social_api/send_email/`, {
    //     body: formData,
    // });

    // if (!result.success) {
    //     displayPopup?.(
    //         "error",
    //         i18n.global.t("constants.popUpConstants.errorMessages.emailSendError"),
    //         result.error as string
    //     );
    //     return;
    // }

    // displayPopup?.(
    //     "success",
    //     i18n.global.t("constants.popUpConstants.successMessages.success"),
    //     i18n.global.t("constants.popUpConstants.successMessages.emailSuccessfullySent")
    // );

    // inputValue.value = "";
    // quill.value.root.innerHTML = "";
    // selectedPeople.value = [];
    // selectedCC.value = [];
    // selectedCCI.value = [];
    // stepContainer = 0;
    // AIContainer.value.innerHTML = "";
    // AIContainer.value = document.getElementById("AIContainer");

    // localStorage.removeItem("uploadedFiles");
    // uploadedFiles.value = [];
    // fileObjects.value = [];

    // const message = i18n.global.t("constants.sendEmailConstants.emailRecipientRequest");
    // const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;

    // displayMessage(message, ai_icon);
}

const triggerFileInput = () => {
    // fileInput.value.click();
};

const handleFileUpload = (event: Event) => {
    const input = event.target as HTMLInputElement;
    if (!input || !input.files) return;  

    const files = Array.from(input.files);

    files.forEach((file) => {
        if (file.size <= MAX_FILE_SIZE) {
            const localStorageUploadedFiles = localStorage.getItem("uploadedFiles");
            const existingFiles: UploadedFile[] = localStorageUploadedFiles
                ? JSON.parse(localStorageUploadedFiles)
                : [];

            if (existingFiles.some((existingFile) => existingFile.name === file.name)) {
                displayPopup?.(
                    "error",
                    i18n.global.t("constants.popUpConstants.errorMessages.duplicateFile"),
                    i18n.global.t("constants.popUpConstants.errorMessages.fileAlreadyInserted")
                );
                return;
            }

            uploadedFiles.value.push({ name: file.name, size: file.size });
            fileObjects.value.push(file);
        } else {
            displayPopup?.(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.fileTooLarge"),
                i18n.global.t("constants.popUpConstants.errorMessages.fileSizeExceedsLimit")
            );
            return;
        }
    });

    saveFileMetadataToLocalStorage();
};


const removeFile = (index: number) => {
    uploadedFiles.value.splice(index, 1);
    fileObjects.value.splice(index, 1);
    saveFileMetadataToLocalStorage();
};

const saveFileMetadataToLocalStorage = () => {
    localStorage.setItem("uploadedFiles", JSON.stringify(uploadedFiles.value));
};
</script>
