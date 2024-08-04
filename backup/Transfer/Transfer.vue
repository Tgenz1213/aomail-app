<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />
    <div class="flex flex-col justify-center items-center h-screen">
        <div class="flex h-full w-full">
            <div class="w-[90px] bg-white ring-1 shadow-sm ring-black ring-opacity-5 2xl:w-[100px]">
                <navbar></navbar>
            </div>

            <div
                id="firstMainColumn"
                class="flex flex-col bg-gray-50 lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[700px]"
            >
                <div class="flex items-center justify-center h-[65px] 2xl:h-[80px]">
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
                                d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z"
                            />
                        </svg>
                        <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500">
                            {{ $t("constants.aiAssistant") }}
                        </h1>
                    </div>
                </div>

                <!-- IA assistant-->
                <div class="flex flex-1 flex-col divide-y">
                    <div class="overflow-y-auto flex-1" style="margin-right: 2px" ref="scrollableDiv">
                        <div class="px-10 py-4 2xl:px-13.5 2xl:py-6">
                            <div class="flex-grow">
                                <div id="AIContainer"></div>
                            </div>
                        </div>
                    </div>
                    <div class="flex flex-col h-[22vh] 2xl:h-[23vh]">
                        <textarea
                            id="dynamicTextarea"
                            @input="adjustHeight"
                            v-model="textareaValue"
                            class="overflow-y-hidden pt-4 pl-6 flex-1 w-full border-transparent bg-transparent text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 focus:border-transparent focus:bg-transparent focus:ring-0 2xl:pt-5 2xl:pl-7 2xl:text-base"
                            placeholder="Instruction"
                        ></textarea>
                        <div class="flex justify-end m-3 2xl:m-5">
                            <button
                                type="button"
                                @click="handleAIClick"
                                class="2xl:w-[100px] w-[80px] rounded-md bg-gray-700 px-5.5 py-2.5 2xl:px-6.5 2xl:py-3 2xl:text-base text-sm text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                            >
                                Envoyer
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div
                id="secondMainColumn"
                class="flex-grow bg-white lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[720px]"
            >
                <div class="flex flex-col h-full w-full">
                    <!--titre -->
                    <div class="flex items-center h-[65px] justify-center lg:py-5 2xl:h-[80px] min-h-6">
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
                                {{ $t("constants.manualSearch") }}
                            </h1>
                        </div>
                    </div>

                    <form class="flex flex-grow w-full px-10">
                        <div class="flex flex-col space-y-6 h-full w-full">
                            <div class="pt-8">
                                <div class="flex flex-wrap">
                                    <!-- Main Recipients List -->
                                    <div v-if="selectedPeople.length > 0" class="flex items-center mb-1">
                                        <div
                                            v-for="person in selectedPeople"
                                            :key="person.email"
                                            class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1"
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
                                            class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1"
                                        >
                                            <span class="font-semibold mr-1">CC:</span>
                                            {{ person.username || person.email }}
                                            <button @click="removePersonFromCC(person)">×</button>
                                        </div>
                                    </div>
                                    <!-- CCI Recipients List -->
                                    <div v-if="selectedCCI.length > 0" class="flex items-center mb-1">
                                        <div
                                            v-for="person in selectedCCI"
                                            :key="person.email"
                                            class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1"
                                        >
                                            <span class="font-semibold mr-1">CCI:</span>
                                            {{ person.username || person.email }}
                                            <button @click="removePersonFromCCI(person)">×</button>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex items-stretch gap-1">
                                    <div class="flex-grow">
                                        <div class="relative items-stretch">
                                            <div class="relative w-full">
                                                <div
                                                    v-if="!isFocused2"
                                                    class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2"
                                                >
                                                    <UserGroupIcon class="w-4 h-4 pointer-events-none" />
                                                    <label
                                                        for="email"
                                                        class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none"
                                                    >
                                                        {{ $t("constants.recipient") }}
                                                    </label>
                                                </div>
                                                <Combobox
                                                    as="div"
                                                    v-model="selectedPerson"
                                                    @update:model-value="personSelected"
                                                >
                                                    <ComboboxInput
                                                        id="recipients"
                                                        class="w-full h-10 rounded-md border-0 bg-white py-2 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                                                        @change="query = $event.target.value"
                                                        :display-value="(person) => person?.name"
                                                        @focus="handleFocusDestinary"
                                                        @blur="handleBlur2($event)"
                                                        @keydown.enter="handleEnterKey"
                                                    />
                                                    <ComboboxButton
                                                        class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none"
                                                    >
                                                        <ChevronUpDownIcon
                                                            class="h-5 w-5 text-gray-400"
                                                            aria-hidden="true"
                                                        />
                                                    </ComboboxButton>
                                                    <!-- List possible email according to current input -->
                                                    <!-- && filteredPeople.length <= 10" -->
                                                    <ComboboxOptions
                                                        v-if="filteredPeople.length > 0"
                                                        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
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
                                                                    <span
                                                                        :class="[
                                                                            'truncate',
                                                                            selected && 'font-semibold',
                                                                        ]"
                                                                    >
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
                                    <div class="flex gap-1">
                                        <button
                                            type="button"
                                            @click="toggleCC"
                                            :class="[
                                                'inline-flex items-center gap-x-1.5 rounded-md px-2.5 py-1.5 text-sm font-semibold hover:bg-gray-600 hover:text-white',
                                                activeType === 'CC'
                                                    ? 'bg-gray-500 text-white'
                                                    : 'bg-gray-100 text-gray-400',
                                            ]"
                                            class="ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                                        >
                                            {{ $t("newPage.carbonCopyInitials") }}
                                        </button>

                                        <!-- CCI Button -->
                                        <button
                                            type="button"
                                            @click="toggleCCI"
                                            :class="[
                                                'inline-flex items-center gap-x-1.5 rounded-md px-2.5 py-1.5 text-sm font-semibold hover:bg-gray-600 hover:text-white',
                                                activeType === 'CCI'
                                                    ? 'bg-gray-500 text-white'
                                                    : 'bg-gray-100 text-gray-400',
                                            ]"
                                            class="ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
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
                                        class="flex items-center mb-1 mr-1 bg-gray-200 rounded px-2 py-1"
                                    >
                                        {{ file.name }}
                                        <button @click="removeFile(index)">×</button>
                                    </div>
                                </div>
                                <div class="flex items-stretch gap-1">
                                    <div class="flex-grow">
                                        <div
                                            class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 w-full"
                                        >
                                            <div class="relative w-full">
                                                <div
                                                    v-if="!isFocused && !inputValue"
                                                    class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 z-10"
                                                >
                                                    <Bars2Icon class="w-4 h-4 pointer-events-none" />
                                                    <label
                                                        for="username"
                                                        class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none"
                                                    >
                                                        {{ $t("newPage.subject") }}
                                                    </label>
                                                </div>
                                                <input
                                                    id="objectInput"
                                                    v-model="inputValue"
                                                    type="text"
                                                    class="block h-10 flex-1 border-0 bg-transparent py-2 pl-3 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6 w-full z-20 relative"
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
                                            class="inline-flex items-center gap-x-1.5 rounded-md bg-gray-100 px-2.5 py-1.5 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-300 shadow-sm hover:ring-transparent hover:bg-gray-600 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
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
                                                    d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13"
                                                />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                            </div>
                            <div class="flex flex-col flex-grow">
                                <div class="flex-grow mb-20 h-[200px]">
                                    <div id="editor" class="w-full"></div>
                                </div>
                                <div class="flex mb-4">
                                    <div class="inline-flex rounded-lg shadow-lg">
                                        <button
                                            @click="sendEmail"
                                            :disabled="emailTransfered"
                                            class="bg-gray-700 rounded-l-lg px-6 py-2 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center 2xl:px-7 2xl:py-3 2xl:text-lg"
                                        >
                                            {{ $t("constants.userActions.send") }}
                                        </button>

                                        <Menu as="div" class="relative -ml-px block">
                                            <MenuButton
                                                class="relative inline-flex items-center rounded-r-lg px-2 py-2 text-white border-l border-gray-300 bg-gray-600 hover:bg-gray-700 focus:z-10"
                                            >
                                                <span class="sr-only">Open options</span>
                                                <ChevronDownIcon class="h-9 w-5" aria-hidden="true" />
                                            </MenuButton>
                                            <transition
                                                enter-active-class="transition ease-out duration-100"
                                                enter-from-class="transform opacity-0 scale-95"
                                                enter-to-class="transform opacity-100 scale-100"
                                                leave-active-class="transition ease-in duration-75"
                                                leave-from-class="transform opacity-100 scale-100"
                                                leave-to-class="transform opacity-0 scale-95"
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
                                                        </button>
                                                    </div>
                                                </MenuItems>
                                            </transition>
                                        </Menu>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import NotificationTimer from "@/components/NotificationTimer.vue";
import userDefaultImg from "@/assets/user.png";
import Quill from "quill";
import { Combobox, ComboboxButton, ComboboxInput, ComboboxOption, ComboboxOptions } from "@headlessui/vue";
import NavBarLarge from "@/components/NavBarLarge.vue";
import NavBarSmall from "@/components/NavBarSmall.vue";
import { UserGroupIcon, Bars2Icon, ChevronDownIcon } from "@heroicons/vue/24/outline";
import { fetchWithToken } from "@/global/security";
import { API_BASE_URL } from "@/global/const";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";

const { t } = useI18n();
const router = useRouter();

const isAiWriting = ref(false);
const emailTransfered = ref(false);
const userSearchResult = ref(null);
const people = ref([]);
const selectedPeople = ref([]);
const selectedCc = ref([]);
const selectedCci = ref([]);
const activeType = ref(null);
const query = ref("");
const selectedPerson = ref("");
const inputValue = ref("");
const isFirstTimeDestinary = ref(true);
const isFocused = ref(false);
const isFocused2 = ref(false);
const hasValueEverBeenEntered = ref(false);
const aiContainer = ref(null);
const objectInput = ref(null);
const quill = ref(null);
const scrollableDiv = ref(null);
const textareaValue = ref("");
const textareaValueSave = ref("");
const isLoading = ref(false);
const fileInput = ref(null);
const uploadedFiles = ref([]);
const fileObjects = ref([]);

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<NodeJS.Timeout | null>(null);

const MAX_FILE_SIZE = 25 * 1024 * 1024;
let stepContainer = 0;
let counterDisplay = 0;

const emailReceiver = sessionStorage.getItem("emailReceiver");

const getFilteredPeople = computed(() => {
  if (query.value === "") {
    return people.value;
  } else {
    return people.value.filter((person) => {
      if (person.username === "") {
        person.username = person.email
          .split("@")[0]
          .split(/\.|-/)
          .map((p) => p.charAt(0).toUpperCase() + p.slice(1))
          .join(" ");
      }
      return (
        person.username.toLowerCase().includes(query.value.toLowerCase()) ||
        person.email.toLowerCase().includes(query.value.toLowerCase())
      );
    });
  }
});

const emit = defineEmits(["update:selectedPerson"]);

watch(selectedPerson, (newValue) => {
  hasValueEverBeenEntered.value = true;
  emit("update:selectedPerson", newValue);
});

onMounted(() => {
  localStorage.removeItem("uploadedFiles");
  quill.value = new Quill("#editor", {
    theme: "snow",
    modules: {
      toolbar: toolbarOptions,
    },
  });

  document.addEventListener("keydown", handleKeyDown);

  const subject = JSON.parse(sessionStorage.getItem("subject") || "");
  const cc = sessionStorage.getItem("cc");
  const bcc = sessionStorage.getItem("bcc");
  const decodedData = JSON.parse(sessionStorage.getItem("decoded_data") || "");
  const email = JSON.parse(sessionStorage.getItem("email") || "");
  const details = JSON.parse(sessionStorage.getItem("details") || "");
  const date = JSON.parse(sessionStorage.getItem("date") || "");

  inputValue.value = "Tr : " + subject;
  const formattedDateVar = new Date(date);
  const options: Intl.DateTimeFormatOptions = {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  };

  const formattedDate = formattedDateVar.toLocaleDateString("fr-FR", options);

  let forwardedMessage = "";

  forwardedMessage += i18n.global.t("constants.sendEmailConstants.emailSummary") + "\n";
  details.forEach((detail) => {
    forwardedMessage += `- ${detail.text}\n`;
  });
  forwardedMessage += "\n\n";
  forwardedMessage += i18n.global.t("constants.sendEmailConstants.forwardedMessage") + "\n";
  forwardedMessage += i18n.global.t("constants.sendEmailConstants.from") + ` ${email}\n`;
  forwardedMessage += i18n.global.t("constants.sendEmailConstants.date") + ` ${formattedDate}\n`;
  forwardedMessage += i18n.global.t("constants.sendEmailConstants.subject") + ` ${subject}\n`;

  if (cc.length > 0) {
    forwardedMessage += `CC: ${cc}\n`;
  }

  forwardedMessage += "\n\n";
  forwardedMessage += decodedData;

  quill.value.setText(forwardedMessage);

  loadFileMetadataFromLocalStorage();

  window.addEventListener("resize", scrollToBottom);

  aiContainer.value = document.getElementById("AIContainer");

  const message = i18n.global.t("constants.sendEmailConstants.emailRecipientRequest");
  const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
  displayMessage(message, aiIcon);
  objectInput.value = document.getElementById("objectInput");

  const form = objectInput.value.closest("form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
    });
  }
});

watch(
  uploadedFiles,
  () => {
    saveFileMetadataToLocalStorage();
  },
  { deep: true }
);

function handleFocusObject() {
  isFocused.value = true;
}

function handleBlur() {
  isFocused.value = false;
}

function handleFocusDestinary() {
  isFocused2.value = true;
}

function askChoiceRecipient(list: Array<Record<string, string>>, type: "main" | "cc" | "bcc"): void {
  let buttonsHTML = "";

  const firstUsername = Object.keys(list[0])[0];
  const userLabel = type === "main" 
    ? i18n.global.t("newPage.mainRecipient")
    : type === "cc" 
    ? i18n.global.t("newPage.ccRecipient")
    : i18n.global.t("newPage.bccRecipient");
  const usernameHTML = `<div>${i18n.global.t("newPage.forUser")}<strong>${firstUsername}</strong> [${userLabel}]</div>`;

  list.forEach((item, index) => {
    const username = Object.keys(item)[0];
    const email = item[username];
    const buttonLabel = type === "main" ? "main" : type === "cc" ? "cc" : "bcc";
    const buttonId = `button-${buttonLabel}-${index}`;

    if (index % 2 === 0) {
      buttonsHTML += '<div class="mr-4">';
    }

    buttonsHTML += `
      <div class="mr-4">
        <button type="button" id="${buttonId}" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
          ${email}
        </button>
      </div>
    `;

    if (index % 2 == 1 || index === list.length - 1) {
      buttonsHTML += "</div>";
    }
  });

  const messageHTML = `
    <div class="flex pb-1 pl-[72px]">
      <div class="flex flex-col">
        ${usernameHTML}
        <br>
        ${buttonsHTML}
      </div>
    </div>
    <br>
  `;

  aiContainer.value.innerHTML += messageHTML;

  list.forEach((item, index) => {
    const buttonLabel = type === "main" ? "main" : type === "cc" ? "cc" : "bcc";
    const buttonId = `button-${buttonLabel}-${index}`;

    setTimeout(() => {
      const button = document.getElementById(buttonId);

      button?.addEventListener("click", () => {
        const username = Object.keys(item)[0];
        const email = item[username];

        const person = { username, email };
        const targetArray = type === "main" ? selectedPeople : type === "cc" ? selectedCc : selectedCci;
        
        if (!targetArray.value.some(p => p.email === person.email)) {
          targetArray.value.push(person);
        }
      });
    }, 0);
  });
}

function handleBlur2(event: Event) {
  isFocused2.value = false;
  const inputValue = (event.target as HTMLInputElement).value.trim().toLowerCase();
  const emailFormat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (inputValue && emailFormat.test(inputValue)) {
    if (!people.value.find((person) => person.email === inputValue)) {
      const newPerson = { username: "", email: inputValue };
      people.value.push(newPerson);
      selectedPeople.value.push(newPerson);
    }
  } else if (!getFilteredPeople.value.length && inputValue) {
    displayPopup("error", i18n.global.t("constants.sendEmailConstants.popUpConstants.invalidEmail"), i18n.global.t("constants.sendEmailConstants.popUpConstants.emailFormatIncorrect"));
  }
}

function triggerFileInput() {
  fileInput.value.click();
}


function scrollToBottom(): void {
  nextTick(() => {
    if (scrollableDiv.value) {
      scrollableDiv.value.scrollTop = scrollableDiv.value.scrollHeight;
    }
  });
}

function handleFileUpload(event: Event) {
  const files = Array.from((event.target as HTMLInputElement).files || []);
  files.forEach((file) => {
    if (file.size <= MAX_FILE_SIZE) {
      let localStorageUploadedFiles = JSON.parse(localStorage.getItem("uploadedFiles") || "[]");

      if (localStorageUploadedFiles.some((currentFile: { name: string }) => currentFile.name === file.name)) {
        displayPopup("error", i18n.global.t("constants.popUpConstants.errorMessages.duplicateFile"), i18n.global.t("constants.popUpConstants.errorMessages.fileAlreadyInserted"));
        return;
      }
      uploadedFiles.value.push({ name: file.name, size: file.size });
      fileObjects.value.push(file);
    } else {
      displayPopup("error", i18n.global.t("constants.popUpConstants.errorMessages.fileTooLarge"), i18n.global.t("constants.popUpConstants.errorMessages.fileSizeExceedsLimit"));
      console.error("File size exceeds Gmail's limit");
      return;
    }
  });
  saveFileMetadataToLocalStorage();
}

function removeFile(index: number) {
  uploadedFiles.value.splice(index, 1);
  fileObjects.value.splice(index, 1);
  saveFileMetadataToLocalStorage();
}

function saveFileMetadataToLocalStorage() {
  localStorage.setItem("uploadedFiles", JSON.stringify(uploadedFiles.value));
}

function loadFileMetadataFromLocalStorage() {
  const files = JSON.parse(localStorage.getItem("uploadedFiles") || "[]");
  uploadedFiles.value = files;
}

function handleEnterKey(event: KeyboardEvent) {
  if (event.target.id === "dynamicTextarea" && event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    handleAiClick();
  } else if (isFocused2.value) {
    event.preventDefault();
    handleBlur2(event);
    handleFocusDestinary();
  }
}

function displayMessage(message: string, aiIcon: string) {
  const messageHTML = `
    <div class="flex pb-12">
      <div class="mr-4 flex">
        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            ${aiIcon}
          </svg>
        </span>   
      </div>
      <div>
        <p ref="animatedText${counterDisplay}"></p>
      </div>
    </div>
  `;
  aiContainer.value.innerHTML += messageHTML;
  const animatedParagraph = document.querySelector(`p[ref="animatedText${counterDisplay}"]`);
  counterDisplay += 1;
  animateText(message, animatedParagraph);
  scrollToBottom();
}

async function findUser(searchQuery: string) {
  const requestOptions = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  };

  try {
    const data = await fetchWithToken(
      `${API_BASE_URL}api/find_user_ai/?query=` + encodeURIComponent(searchQuery),
      requestOptions
    );
    console.log(data);
    userSearchResult.value = data;
    return data;
  } catch (error) {
    console.error("Error fetching user information:", error.message);
  }
}


async function handleAIClick() {
    if (isAIWriting.value) {
        return
    }
    isAIWriting.value = true

    // Declare variables outside the fetch scope
    let messageHTML = ""
    let userInput = textareaValue.value

    // Fetches the profile image URL from the server
    const requestOptions = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            email: emailReceiver,
        },
    }

    const data = await fetchWithToken(`${API_BASE_URL}user/social_api/get_profile_image/`, requestOptions)
    let imageURL = data.profile_image_url || userDefaultImg
    const profileImageHTML = `
      <img src="${imageURL}" alt="Profile Image" class="h-14 w-14 rounded-full">
    `

    // Create the complete message HTML with the profile image and text
    messageHTML = `
      <div class="flex pb-12">
        <div class="mr-4 flex">
          <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
            ${profileImageHTML}
          </span>
        </div>
        <div>
          <p class="font-serif">${userInput}</p>
        </div>
      </div>
    `

    AIContainer.value.innerHTML += messageHTML
    textareaValueSave.value = textareaValue.value
    textareaValue.value = ""
    scrollToBottom()

    setTimeout(async () => {
        if (stepcontainer == 0) {
            if (textareaValueSave.value == "") {
                const message = t("constants.sendEmailConstants.noRecipientsEntered")
                const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`
                displayMessage(message, ai_icon)
            } else {
                try {
                    isLoading.value = true
                    loading()
                    scrollToBottom()
                    const result = await findUser(textareaValueSave.value)

                    hideLoading()

                    let noUsersAdded = true
                    let WaitforUserChoice = false
                    if (result.error != "Invalid input or query not about email recipients") {
                        // To update to handle the main error

                        const main_recipients = userSearchResult.value.main_recipients
                        const cc_recipients = userSearchResult.value.cc_recipients
                        const bcc_recipients = userSearchResult.value.bcc_recipients
                        console.log("debug", main_recipients, cc_recipients, bcc_recipients)

                        for (let i = 0; i < main_recipients.length; i++) {
                            const user = main_recipients[i]
                            const emails = user.email

                            if (emails.length == 1) {
                                const person = { username: user.username, email: emails[0] }
                                selectedPeople.value.push(person)
                                main_recipients.splice(i, 1)
                                noUsersAdded = false
                                i--
                            }
                        }

                        for (let i = 0; i < cc_recipients.length; i++) {
                            const user = cc_recipients[i]
                            const emails = user.email

                            if (emails.length == 1) {
                                const person = { username: user.username, email: emails[0] }
                                selectedCC.value.push(person)
                                delete cc_recipients[i]
                                cc_recipients.splice(i, 1)
                                noUsersAdded = false
                                i--
                            }
                        }

                        for (let i = 0; i < bcc_recipients.length; i++) {
                            const user = bcc_recipients[i]
                            const emails = user.email

                            if (emails.length == 1) {
                                const person = { username: user.username, email: emails[0] }
                                selectedCCI.value.push(person)
                                bcc_recipients.splice(i, 1)
                                noUsersAdded = false
                                i--
                            }
                        }

                        // This condition is used to display the diffrent mail possibilities
                        if (main_recipients.length > 0 || cc_recipients.length > 0 || bcc_recipients.length > 0) {
                            const messageHTML = `
                                <div class="flex pb-2">
                                    <div class="mr-4 flex">
                                        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
                                            </svg>
                                        </span>   
                                    </div>
                                    <div>
                                        <p>${t("constants.sendEmailConstants.multipleEmailsFoundForSomeRecipients")}</p>
                                    </div>
                                </div>
                            `
                            AIContainer.value.innerHTML += messageHTML

                            if (main_recipients.length > 0) {
                                WaitforUserChoice = true
                                const emailList = []

                                for (const user of main_recipients) {
                                    for (const email of user.email) {
                                        if (user.email !== "") {
                                            // Creating an object for each email and pushing it to the emailList array
                                            const emailMapping = {}
                                            emailMapping[user.username] = email
                                            emailList.push(emailMapping)
                                            noUsersAdded = false
                                        }
                                    }
                                }
                                askChoiceRecipier(emailList, "main")
                            }
                            if (cc_recipients.length > 0) {
                                WaitforUserChoice = true
                                const emailList = []

                                for (const user of cc_recipients) {
                                    for (const email of user.email) {
                                        if (user.email !== "") {
                                            // Creating an object for each email and pushing it to the emailList array
                                            const emailMapping = {}
                                            emailMapping[user.username] = email
                                            emailList.push(emailMapping)
                                            noUsersAdded = false
                                        }
                                    }
                                }
                                askChoiceRecipier(emailList, "cc")
                            }
                            if (bcc_recipients.length > 0) {
                                WaitforUserChoice = true
                                const emailList = []

                                for (const user of bcc_recipients) {
                                    for (const email of user.email) {
                                        if (user.email !== "") {
                                            // Creating an object for each email and pushing it to the emailList array
                                            const emailMapping = {}
                                            emailMapping[user.username] = email
                                            emailList.push(emailMapping)
                                            noUsersAdded = false
                                        }
                                    }
                                }
                                askChoiceRecipier(emailList, "bcc")
                            }
                            scrollToBottom()
                        }

                        if (noUsersAdded) {
                            console.log("DEBUG")
                            const message = t(
                                "constants.sendEmailConstants.noRecipientsFoundPleaseTryAgainOrEnterManually"
                            )
                            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
                            displayMessage(message, ai_icon)
                        } else if (!WaitforUserChoice) {
                            stepcontainer = 1
                        }
                    } else {
                        const message = t("constants.sendEmailConstants.noRecipientsFoundPleaseTryAgainOrEnterManually")
                        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
                        displayMessage(message, ai_icon)
                    }
                } catch (error) {
                    const message = t("constants.sendEmailConstants.processingErrorApology")
                    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
                    displayMessage(message, ai_icon)
                    console.error("Error finding user", error)
                }
            }
        }
    }, 0)
}







onMounted(() => {
    localStorage.removeItem("uploadedFiles")
    // Initialize Quill editor
    quill.value = new Quill("#editor", {
        theme: "snow",
        modules: {
            toolbar: toolbarOptions,
        },
    })

    document.addEventListener("keydown", handleKeyDown)

    const subject = JSON.parse(sessionStorage.getItem("subject"))
    const cc = sessionStorage.getItem("cc")
    const bcc = sessionStorage.getItem("bcc")
    const decoded_data = JSON.parse(sessionStorage.getItem("decoded_data"))
    const email = JSON.parse(sessionStorage.getItem("email"))

    const details = JSON.parse(sessionStorage.getItem("details"))

    const date = JSON.parse(sessionStorage.getItem("date"))

    // Prepare the forwarded email
    inputValue.value = "Tr : " + subject
    const formattedDateVar = new Date(date)
    const options = {
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
    }

    const formattedDate = formattedDateVar.toLocaleDateString("fr-FR", options)

    let forwardedMessage = ""

    forwardedMessage += "Résumé de l'email:\n"
    details.forEach((detail) => {
        forwardedMessage += `- ${detail.text}\n`
    })
    forwardedMessage += "\n\n"
    forwardedMessage += "---------- Message transféré ---------\n"
    forwardedMessage += `De: ${email}\n`
    forwardedMessage += `Date: ${formattedDate}\n`
    forwardedMessage += `Sujet: ${subject}\n`

    if (cc.length > 0) {
        forwardedMessage += `CC: ${cc}\n`
    }

    forwardedMessage += "\n\n"
    forwardedMessage += decoded_data

    quill.value.setText(forwardedMessage)

    loadFileMetadataFromLocalStorage()

    window.addEventListener("resize", scrollToBottom)

    var toolbarOptions = [
        [{ font: [] }],
        [{ header: [1, 2, 3, 4, 5, 6, false] }],
        ["bold", "italic", "underline"],
        [{ color: [] }, { background: [] }],
        [{ list: "ordered" }, { list: "bullet" }],
        [{ align: [] }],
        ["blockquote", "code-block"],
    ]

    // DOM-related code
    AIContainer.value = document.getElementById("AIContainer")

    const message = t("constants.sendEmailConstants.emailRecipientRequest")
    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
    displayMessage(message, ai_icon)
    objectInput.value = document.getElementById("objectInput")

    const form = objectInput.value.closest("form")
    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault()
        })
    }
})

watch(
    uploadedFiles,
    () => {
        saveFileMetadataToLocalStorage()
    },
    { deep: true }
)

function animateText(text: string, target: Element | null): void {
  if (!target) return;
  
  let characters = text.split("");
  let currentIndex = 0;
  const interval = setInterval(() => {
    if (currentIndex < characters.length) {
      target.textContent += characters[currentIndex];
      currentIndex++;
    } else {
      clearInterval(interval);
      isAiWriting.value = false;
    }
  }, 30);
}

function personSelected(person) {
    if (!person) return

    switch (activeType.value) {
        case "CC":
            if (!selectedCC.value.includes(person)) {
                selectedCC.value.push(person)
            }
            break
        case "CCI":
            if (!selectedCCI.value.includes(person)) {
                selectedCCI.value.push(person)
            }
            break
        default:
            if (!selectedPeople.value.includes(person)) {
                selectedPeople.value.push(person)
            }
    }

    if (isFirstTimeDestinary.value) {
        stepcontainer = 1
        isFirstTimeDestinary.value = false
    }

    selectedPerson.value = null
}

function toggleCC() {
    activeType.value = activeType.value === "CC" ? null : "CC"
}

function toggleCCI() {
    activeType.value = activeType.value === "CCI" ? null : "CCI"
}

function removePersonFromMain(personToRemove) {
    selectedPeople.value = selectedPeople.value.filter((person) => person !== personToRemove)
}

function removePersonFromCC(personToRemove) {
    selectedCC.value = selectedCC.value.filter((person) => person !== personToRemove)
}

function removePersonFromCCI(personToRemove) {
    selectedCCI.value = selectedCCI.value.filter((person) => person !== personToRemove)
}

// To display the button for one choice of the recipier for the user
function askChoiceRecipier(list, type) {
    let buttonsHTML = ""

    const firstUsername = Object.keys(list[0])[0]
    // Display the type of recipient
    const userLabel =
        type === "main"
            ? t("newPage.mainRecipient")
            : type === "cc"
            ? t("newPage.ccRecipient")
            : t("newPage.bccRecipient")
    // Display the username before the list of emails
    const usernameHTML = `<div>${t("newPage.forUser")}<strong>${firstUsername}</strong> [${userLabel}]</div>`

    list.forEach((item, index) => {
        // Extract the first (and presumably only) key in the dictionary, which is the username
        const username = Object.keys(item)[0]
        // Accessing the email using the username key
        const email = item[username]
        // Generating a unique ID for each button based on the index to ensure it's unique
        const buttonLabel = type === "main" ? "main" : type === "cc" ? "cc" : "bcc"
        const buttonId = `button-${buttonLabel}-${index}`

        // if index is a even number
        if (index % 2 === 0) {
            // open the div
            buttonsHTML += '<div class="mr-4">'
        }

        buttonsHTML += `
            <div class="mr-4">
                <button type="button" id="${buttonId}" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                    ${email}
                </button>
            </div>
        `

        // if index is an odd number or its the last element
        if (index % 2 == 1 || index === list.length - 1) {
            // close the div
            buttonsHTML += "</div>"
        }
    })

    const messageHTML = `
        <div class="flex pb-1 pl-[72px]">
            <div class="flex flex-col">
                ${usernameHTML}
                <br>
                ${buttonsHTML}
            </div>
        </div>
        <br>
    `

    AIContainer.value.innerHTML += messageHTML

    list.forEach((item, index) => {
        const buttonLabel = type === "main" ? "main" : type === "cc" ? "cc" : "bcc"
        const buttonId = `button-${buttonLabel}-${index}`

        setTimeout(() => {
            const button = document.getElementById(buttonId)

            button.addEventListener("click", () => {
                const username = Object.keys(item)[0]
                const email = item[username]

                if (type === "main") {
                    const person = { username: username, email: email }
                    const isPersonAlreadySelected = selectedPeople.value.some((p) => p.email === person.email)
                    if (!isPersonAlreadySelected) {
                        selectedPeople.value.push(person)
                    }
                } else if (type === "cc") {
                    const person = { username: username, email: email }
                    const isPersonAlreadySelected = selectedCC.value.some((p) => p.email === person.email)
                    if (!isPersonAlreadySelected) {
                        selectedCC.value.push(person)
                    }
                } else {
                    const person = { username: username, email: email }
                    const isPersonAlreadySelected = selectedCCI.value.some((p) => p.email === person.email)
                    if (!isPersonAlreadySelected) {
                        selectedCCI.value.push(person)
                    }
                }
            })
        }, 0)
    })
}

function loading() {
    // Use `nbr` in the template literal to set the reference dynamically
    const messageHTML = `
      <div id="dynamicLoadingIndicator" class="pb-12">
        <div class="flex">
            <div class="mr-4">
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900">
                    <span class="text-lg font-medium leading-none text-white">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15a4.5 4.5 0 0 0 4.5 4.5H18a3.75 3.75 0 0 0 1.332-7.257 3 3 0 0 0-3.758-3.848 5.25 5.25 0 0 0-10.233 2.33A4.502 4.502 0 0 0 2.25 15Z" />
                      </svg>
                    </span>
                </span>
            </div>
            <div>
              <div class="loading-spinner"></div>
            </div>
        </div>
      </div>
    `

    AIContainer.value.innerHTML += messageHTML
}
function loading(): void {
  const messageHTML = `
    <div id="dynamicLoadingIndicator" class="pb-12">
      <div class="flex">
        <div class="mr-4">
          <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900">
            <span class="text-lg font-medium leading-none text-white">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15a4.5 4.5 0 0 0 4.5 4.5H18a3.75 3.75 0 0 0 1.332-7.257 3 3 0 0 0-3.758-3.848 5.25 5.25 0 0 0-10.233 2.33A4.502 4.502 0 0 0 2.25 15Z" />
              </svg>
            </span>
          </span>
        </div>
        <div>
          <div class="loading-spinner"></div>
        </div>
      </div>
    </div>
  `;

  aiContainer.value.innerHTML += messageHTML;
}

function hideLoading(): void {
  const loadingElement = document.getElementById("dynamicLoadingIndicator");
  if (loadingElement) {
    loadingElement.remove();
  }
}


async  function scheduleSend(): Promise<void>  {
  const emailSubject = inputValue.value;
  const emailBody = quill.value.root.innerHTML;

  const selectedEmail = emailsLinked.value.find(tuple => tuple.email === emailSelected.value);
  if (selectedEmail && selectedEmail.typeApi !== MICROSOFT) {
    displayPopup('error', "Email service provider not supported", "Scheduled send is only available for Outlook accounts");
    return;
  }

  if (!emailSubject.trim()) {
    displayPopup('error', t("constants.popUpConstants.errorMessages.emailSendError"), t("constants.popUpConstants.errorMessages.emailSendErrorNoSubject"));
    return;
  } else if (emailBody === "<p><br></p>") {
    displayPopup('error', t("constants.popUpConstants.errorMessages.emailSendError"), t("constants.popUpConstants.errorMessages.emailSendErrorNoObject"));
    return;
  } else if (selectedPeople.value.length === 0) {
    displayPopup('error', t("constants.popUpConstants.errorMessages.emailSendError"), t("constants.popUpConstants.errorMessages.emailSendErrorNoRecipient"));
    return;
  }

  const formData = new FormData();

  formData.append("subject", emailSubject);
  formData.append("message", emailBody);
  fileObjects.value.forEach((file) => formData.append("attachments", file));

  selectedPeople.value.forEach((person) => formData.append("to", person.email));

  if (selectedCC.value.length > 0) {
    selectedCC.value.forEach((person) => formData.append("cc", person.email));
  }
  if (selectedCCI.value.length > 0) {
    selectedCCI.value.forEach((person) => formData.append("cci", person.email));
  }
  formData.append("email", emailSelected.value);
  formData.append("datetime", "2024-07-02T10:00:00Z"); // todo: Update this with the user-provided date and time

  try {
    const response = await fetchWithToken(`${API_BASE_URL}user/social_api/send_schedule_email/`, {
      method: "POST",
      body: formData,
    });

    if (response.message === "Email scheduled successfully!") {
      displayPopup('success', "Email scheduled successfully!", "Your email will be sent on time");

      // Reset form and state
      inputValue.value = "";
      quill.value.root.innerHTML = "";
      selectedPeople.value = [];
      selectedCC.value = [];
      selectedCCI.value = [];
      stepcontainer = 0;
      if (AIContainer.value) AIContainer.value.innerHTML = "";
      AIContainer.value = document.getElementById("AIContainer");

      localStorage.removeItem("uploadedFiles");
      uploadedFiles.value = [];
      fileObjects.value = [];

      const message = t("constants.sendEmailConstants.emailRecipientRequest");
      const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;

      displayMessage(message, ai_icon);
    } else {
      displayPopup('error', t("constants.popUpConstants.errorMessages.emailSendError"), response.error);
    }
  } catch (error) {
    displayPopup('error', t("constants.popUpConstants.errorMessages.emailSendError"), (error as Error).message);
  }
};
 
async function sendEmail(): Promise<void>  {
  const emailSubject = inputValue.value;
  const emailBody = quill.value.root.innerHTML;

  if (!emailSubject.trim()) {
    displayPopup('error', t("constants.popUpConstants.errorMessages.emailSendError"), t("constants.popUpConstants.errorMessages.emailSendErrorNoSubject"));
    return;
  } else if (emailBody === "<p><br></p>") {
    displayPopup('error', t("constants.popUpConstants.errorMessages.emailSendError"), t("constants.popUpConstants.errorMessages.emailSendErrorNoObject"));
    return;
  } else if (selectedPeople.value.length === 0) {
    displayPopup('error', t("constants.popUpConstants.errorMessages.emailSendError"), t("constants.popUpConstants.errorMessages.emailSendErrorNoRecipient"));
    return;
  }

  const formData = new FormData();

  formData.append("subject", emailSubject);
  formData.append("message", emailBody);
  fileObjects.value.forEach((file) => formData.append("attachments", file));

  selectedPeople.value.forEach((person) => formData.append("to", person.email));

  if (selectedCC.value.length > 0) {
    selectedCC.value.forEach((person) => formData.append("cc", person.email));
  }

  if (selectedCCI.value.length > 0) {
    selectedCCI.value.forEach((person) => formData.append("bcc", person.email));
  }

  formData.append("email", emailReceiver.value);

  try {
    const response = await fetchWithToken(`${API_BASE_URL}user/social_api/send_email/`, {
      method: "POST",
      body: formData,
    });

    if (response.message === "Email sent successfully!") {
      displayPopup('success', t("transferPage.emailTransferred"), t("constants.redirectionInProgress"));
      emailTransfered.value = true;
      localStorage.removeItem("uploadedFiles");
      uploadedFiles.value = [];
      fileObjects.value = [];

      setTimeout(() => {
        router.push({ name: "home" });
      }, 3000);
    } else {
      let errorMessage = response.error;
      if (response.error === "recipient is missing") {
        errorMessage = t("constants.popUpConstants.errorMessages.emailSendErrorNoRecipient");
      } else if (response.error === "subject is missing") {
        errorMessage = t("constants.popUpConstants.errorMessages.emailSendErrorNoObject");
      }
      displayPopup('error', t("constants.popUpConstants.errorMessages.emailSendError"), errorMessage);
    }
  } catch (error) {
    displayPopup('error', t("constants.popUpConstants.errorMessages.emailSendError"), error as string);
  }
};

function handleKeyDown(event: KeyboardEvent): void  {
  if (event.key === "Tab") {
    event.preventDefault();

    const editor = document.getElementById("editor");
    const recipients = document.getElementById("recipients");
    const objectInput = document.getElementById("objectInput");
    const dynamicTextarea = document.getElementById("dynamicTextarea");

    if (editor?.contains(document.activeElement)) {
      return;
    } else if (
      selectedCCI.value.length === 0 &&
      selectedCC.value.length === 0 &&
      selectedPeople.value.length === 0 &&
      document.activeElement?.id !== "recipients"
    ) {
      activeType.value = null;
      recipients?.focus();
    } else if (inputValue.value === "" && !isFocused.value) {
      objectInput?.focus();
    } else if (quill.value.root.innerHTML === "<p><br></p>") {
      quill.value.focus();
    } else {
      if (document.activeElement?.id === "recipients") {
        objectInput?.focus();
      } else if (document.activeElement?.id === "dynamicTextarea") {
        recipients?.focus();
      } else {
        dynamicTextarea?.focus();
      }
    }
  } else if (event.ctrlKey) {
    switch (event.key) {
      case "b":
        quill.value.focus();
        event.preventDefault();
        break;
      case "d":
        document.getElementById("recipients")?.focus();
        event.preventDefault();
        break;
      case "k":
        document.getElementById("dynamicTextarea")?.focus();
        event.preventDefault();
        break;
      case "o":
        document.getElementById("objectInput")?.focus();
        event.preventDefault();
        break;
      case "Enter":
        sendEmail();
        break;
    }
  }
};




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

const maxHeight = ref(250);

const adjustHeight = (event: Event): void => {
  const textarea = event.target as HTMLTextAreaElement;
   
  textarea.style.height = "auto";

  if (textarea.scrollHeight > maxHeight.value) {
    textarea.style.height = `${maxHeight.value}px`;
    textarea.style.overflowY = "auto";  } else {
    textarea.style.height = `${textarea.scrollHeight}px`;
    textarea.style.overflowY = "hidden";    }
};
</script>


 


<!-- TODO: FOLLOW these guidelines anyway
the import of constants and function are correct. You must do the following operations:
 
FOR popup use ONLY this function displayPopup
put everything under script setup if its more optimal and easier to manage  
use strictly camelCase 
use i18n.global.t( ONLY to display the translation
add the types as we are working with TypeScript
use strictly ONLY script setup
remove all comments

