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
                <NavBarSmall />
            </div>

            <div
                id="firstMainColumn"
                class="flex flex-col bg-gray-50 lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[700px]"
            >
                <ManualEmail />
            </div>

            <div
                id="secondMainColumn"
                class="flex-grow bg-white lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[720px]"
            >
                <AiEmail />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
/* eslint-disable */
import { ref, computed, onMounted, nextTick, watch } from "vue";
import { useRouter } from "vue-router";
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
import ManualEmail from "@/pages/Transfer/components/ManualEmail.vue";
import AiEmail from "@/pages/Transfer/components/AiEmail.vue";

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
const timerId = ref<number | null>(null);

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
    const userLabel =
        type === "main"
            ? i18n.global.t("newPage.mainRecipient")
            : type === "cc"
            ? i18n.global.t("newPage.ccRecipient")
            : i18n.global.t("newPage.bccRecipient");
    const usernameHTML = `<div>${i18n.global.t(
        "newPage.forUser"
    )}<strong>${firstUsername}</strong> [${userLabel}]</div>`;

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

                if (!targetArray.value.some((p) => p.email === person.email)) {
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
        displayPopup(
            "error",
            i18n.global.t("constants.sendEmailConstants.popUpConstants.invalidEmail"),
            i18n.global.t("constants.sendEmailConstants.popUpConstants.emailFormatIncorrect")
        );
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
                displayPopup(
                    "error",
                    i18n.global.t("constants.popUpConstants.errorMessages.duplicateFile"),
                    i18n.global.t("constants.popUpConstants.errorMessages.fileAlreadyInserted")
                );
                return;
            }
            uploadedFiles.value.push({ name: file.name, size: file.size });
            fileObjects.value.push(file);
        } else {
            displayPopup(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.fileTooLarge"),
                i18n.global.t("constants.popUpConstants.errorMessages.fileSizeExceedsLimit")
            );
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


onMounted(() => {
    localStorage.removeItem("uploadedFiles");
    // Initialize Quill editor
    quill.value = new Quill("#editor", {
        theme: "snow",
        modules: {
            toolbar: toolbarOptions,
        },
    });

    document.addEventListener("keydown", handleKeyDown);

    const subject = JSON.parse(sessionStorage.getItem("subject"));
    const cc = sessionStorage.getItem("cc");
    const bcc = sessionStorage.getItem("bcc");
    const decoded_data = JSON.parse(sessionStorage.getItem("decoded_data"));
    const email = JSON.parse(sessionStorage.getItem("email"));

    const details = JSON.parse(sessionStorage.getItem("details"));

    const date = JSON.parse(sessionStorage.getItem("date"));

    // Prepare the forwarded email
    inputValue.value = "Tr : " + subject;
    const formattedDateVar = new Date(date);
    const options = {
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
    };

    const formattedDate = formattedDateVar.toLocaleDateString("fr-FR", options);

    let forwardedMessage = "";

    forwardedMessage += "Résumé de l'email:\n";
    details.forEach((detail) => {
        forwardedMessage += `- ${detail.text}\n`;
    });
    forwardedMessage += "\n\n";
    forwardedMessage += "---------- Message transféré ---------\n";
    forwardedMessage += `De: ${email}\n`;
    forwardedMessage += `Date: ${formattedDate}\n`;
    forwardedMessage += `Sujet: ${subject}\n`;

    if (cc.length > 0) {
        forwardedMessage += `CC: ${cc}\n`;
    }

    forwardedMessage += "\n\n";
    forwardedMessage += decoded_data;

    quill.value.setText(forwardedMessage);

    loadFileMetadataFromLocalStorage();

    window.addEventListener("resize", scrollToBottom);

    var toolbarOptions = [
        [{ font: [] }],
        [{ header: [1, 2, 3, 4, 5, 6, false] }],
        ["bold", "italic", "underline"],
        [{ color: [] }, { background: [] }],
        [{ list: "ordered" }, { list: "bullet" }],
        [{ align: [] }],
        ["blockquote", "code-block"],
    ];

    // DOM-related code
    AIContainer.value = document.getElementById("AIContainer");

    const message = t("constants.sendEmailConstants.emailRecipientRequest");
    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
    displayMessage(message, ai_icon);
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
    if (!person) return;

    switch (activeType.value) {
        case "CC":
            if (!selectedCC.value.includes(person)) {
                selectedCC.value.push(person);
            }
            break;
        case "CCI":
            if (!selectedCCI.value.includes(person)) {
                selectedCCI.value.push(person);
            }
            break;
        default:
            if (!selectedPeople.value.includes(person)) {
                selectedPeople.value.push(person);
            }
    }

    if (isFirstTimeDestinary.value) {
        stepcontainer = 1;
        isFirstTimeDestinary.value = false;
    }

    selectedPerson.value = null;
}

function toggleCC() {
    activeType.value = activeType.value === "CC" ? null : "CC";
}

function toggleCCI() {
    activeType.value = activeType.value === "CCI" ? null : "CCI";
}

function removePersonFromMain(personToRemove) {
    selectedPeople.value = selectedPeople.value.filter((person) => person !== personToRemove);
}

function removePersonFromCC(personToRemove) {
    selectedCC.value = selectedCC.value.filter((person) => person !== personToRemove);
}

function removePersonFromCCI(personToRemove) {
    selectedCCI.value = selectedCCI.value.filter((person) => person !== personToRemove);
}

// To display the button for one choice of the recipier for the user
function askChoiceRecipier(list, type) {
    let buttonsHTML = "";

    const firstUsername = Object.keys(list[0])[0];
    // Display the type of recipient
    const userLabel =
        type === "main"
            ? t("newPage.mainRecipient")
            : type === "cc"
            ? t("newPage.ccRecipient")
            : t("newPage.bccRecipient");
    // Display the username before the list of emails
    const usernameHTML = `<div>${t("newPage.forUser")}<strong>${firstUsername}</strong> [${userLabel}]</div>`;

    list.forEach((item, index) => {
        // Extract the first (and presumably only) key in the dictionary, which is the username
        const username = Object.keys(item)[0];
        // Accessing the email using the username key
        const email = item[username];
        // Generating a unique ID for each button based on the index to ensure it's unique
        const buttonLabel = type === "main" ? "main" : type === "cc" ? "cc" : "bcc";
        const buttonId = `button-${buttonLabel}-${index}`;

        // if index is a even number
        if (index % 2 === 0) {
            // open the div
            buttonsHTML += '<div class="mr-4">';
        }

        buttonsHTML += `
            <div class="mr-4">
                <button type="button" id="${buttonId}" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                    ${email}
                </button>
            </div>
        `;

        // if index is an odd number or its the last element
        if (index % 2 == 1 || index === list.length - 1) {
            // close the div
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

    AIContainer.value.innerHTML += messageHTML;

    list.forEach((item, index) => {
        const buttonLabel = type === "main" ? "main" : type === "cc" ? "cc" : "bcc";
        const buttonId = `button-${buttonLabel}-${index}`;

        setTimeout(() => {
            const button = document.getElementById(buttonId);

            button.addEventListener("click", () => {
                const username = Object.keys(item)[0];
                const email = item[username];

                if (type === "main") {
                    const person = { username: username, email: email };
                    const isPersonAlreadySelected = selectedPeople.value.some((p) => p.email === person.email);
                    if (!isPersonAlreadySelected) {
                        selectedPeople.value.push(person);
                    }
                } else if (type === "cc") {
                    const person = { username: username, email: email };
                    const isPersonAlreadySelected = selectedCC.value.some((p) => p.email === person.email);
                    if (!isPersonAlreadySelected) {
                        selectedCC.value.push(person);
                    }
                } else {
                    const person = { username: username, email: email };
                    const isPersonAlreadySelected = selectedCCI.value.some((p) => p.email === person.email);
                    if (!isPersonAlreadySelected) {
                        selectedCCI.value.push(person);
                    }
                }
            });
        }, 0);
    });
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
    `;

    AIContainer.value.innerHTML += messageHTML;
}
// function loading(): void {
//   const messageHTML = `
//     <div id="dynamicLoadingIndicator" class="pb-12">
//       <div class="flex">
//         <div class="mr-4">
//           <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900">
//             <span class="text-lg font-medium leading-none text-white">
//               <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
//                 <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15a4.5 4.5 0 0 0 4.5 4.5H18a3.75 3.75 0 0 0 1.332-7.257 3 3 0 0 0-3.758-3.848 5.25 5.25 0 0 0-10.233 2.33A4.502 4.502 0 0 0 2.25 15Z" />
//               </svg>
//             </span>
//           </span>
//         </div>
//         <div>
//           <div class="loading-spinner"></div>
//         </div>
//       </div>
//     </div>
//   `;

//   aiContainer.value.innerHTML += messageHTML;
// }

function hideLoading(): void {
    const loadingElement = document.getElementById("dynamicLoadingIndicator");
    if (loadingElement) {
        loadingElement.remove();
    }
}

async function scheduleSend(): Promise<void> {
    const emailSubject = inputValue.value;
    const emailBody = quill.value.root.innerHTML;

    const selectedEmail = emailsLinked.value.find((tuple) => tuple.email === emailSelected.value);
    if (selectedEmail && selectedEmail.typeApi !== MICROSOFT) {
        displayPopup(
            "error",
            "Email service provider not supported",
            "Scheduled send is only available for Outlook accounts"
        );
        return;
    }

    if (!emailSubject.trim()) {
        displayPopup(
            "error",
            t("constants.popUpConstants.errorMessages.emailSendError"),
            t("constants.popUpConstants.errorMessages.emailSendErrorNoSubject")
        );
        return;
    } else if (emailBody === "<p><br></p>") {
        displayPopup(
            "error",
            t("constants.popUpConstants.errorMessages.emailSendError"),
            t("constants.popUpConstants.errorMessages.emailSendErrorNoObject")
        );
        return;
    } else if (selectedPeople.value.length === 0) {
        displayPopup(
            "error",
            t("constants.popUpConstants.errorMessages.emailSendError"),
            t("constants.popUpConstants.errorMessages.emailSendErrorNoRecipient")
        );
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
            displayPopup("success", "Email scheduled successfully!", "Your email will be sent on time");

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
            displayPopup("error", t("constants.popUpConstants.errorMessages.emailSendError"), response.error);
        }
    } catch (error) {
        displayPopup("error", t("constants.popUpConstants.errorMessages.emailSendError"), (error as Error).message);
    }
}

async function sendEmail(): Promise<void> {
    const emailSubject = inputValue.value;
    const emailBody = quill.value.root.innerHTML;

    if (!emailSubject.trim()) {
        displayPopup(
            "error",
            t("constants.popUpConstants.errorMessages.emailSendError"),
            t("constants.popUpConstants.errorMessages.emailSendErrorNoSubject")
        );
        return;
    } else if (emailBody === "<p><br></p>") {
        displayPopup(
            "error",
            t("constants.popUpConstants.errorMessages.emailSendError"),
            t("constants.popUpConstants.errorMessages.emailSendErrorNoObject")
        );
        return;
    } else if (selectedPeople.value.length === 0) {
        displayPopup(
            "error",
            t("constants.popUpConstants.errorMessages.emailSendError"),
            t("constants.popUpConstants.errorMessages.emailSendErrorNoRecipient")
        );
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
            displayPopup("success", t("transferPage.emailTransferred"), t("constants.redirectionInProgress"));
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
            displayPopup("error", t("constants.popUpConstants.errorMessages.emailSendError"), errorMessage);
        }
    } catch (error) {
        displayPopup("error", t("constants.popUpConstants.errorMessages.emailSendError"), error as string);
    }
}


function displayPopup(type: "success" | "error", title: string, message: string) {
    if (type === "error") {
        displayErrorPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    } else {
        displaySuccessPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    }
    timerId.value = setTimeout(dismissPopup, 4000);
}

function dismissPopup() {
    showNotification.value = false;
    if (timerId.value !== null) {
        clearTimeout(timerId.value);
    }
}


</script>

<!-- TODO: FOLLOW these guidelines anyway
the import of constants and function are correct. You must do the following operations:
 
FOR popup use ONLY this function displayPopup
put everything under script setup if its more optimal and easier to manage  
use strictly camelCase 
use i18n.global.t( ONLY to display the translation
add the types as we are working with TypeScript
use strictly ONLY script setup
remove all comments -->
