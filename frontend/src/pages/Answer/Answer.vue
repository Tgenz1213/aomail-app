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
                class="flex flex-col bg-gray-50 lg:ring-1 lg:ring-black lg:ring-opacity-5 h-screen xl:w-[43vw] 2xl:w-[700px]"
            >
                <AiEmail />
            </div>
            <div
                id="secondMainColumn"
                class="flex-grow bg-white lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full xl:w-[43vw] 2xl:w-[720px]"
            >
                <ManualEmail />
            </div>
        </div>
    </div>
</template>

<script setup>
/* eslint-disable */
import { computed, ref, onMounted, nextTick } from "vue";
import { watch } from "vue";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";
import Quill from "quill";
import NotificationTimer from "@/components/NotificationTimer.vue";
import { Combobox, ComboboxButton, ComboboxInput, ComboboxOption, ComboboxOptions } from "@headlessui/vue";

// Variable to prevent the user from starting a prompt if AI is writing
let isAIWriting = ref(false);

// variables to display a notification
let showNotification = ref(false);
let notificationTitle = ref("");
let notificationMessage = ref("");
let backgroundColor = ref("");
let timerId = ref(null);

let emailAnswered = ref(false);
let history = ref({});

function dismissPopup() {
    showNotification.value = false;
    // Cancel the timer
    clearTimeout(timerId.value);
}
function displayPopup() {
    showNotification.value = true;

    timerId.value = setTimeout(() => {
        dismissPopup();
    }, 4000);
}

// lists of different types of recipients
const people = [];

const requestOptions = {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
    },
};

// request to update the list of contacts (people array)
// fetchWithToken(`${API_BASE_URL}user/contacts/`, requestOptions)
//   .then(response => {
//     people.push(...response);
//   })
//   .catch(error => {
//     console.error("Error fetching contacts:", error);
//     // Show the pop-up
//     backgroundColor = 'bg-red-200/[.89] border border-red-400';
//     notificationTitle = t('constants.popUpConstants.errorMessages.contactFetchError');
//     notificationMessage = error;
//     displayPopup();
//   })

const query = ref("");
const getFilteredPeople = (query, people) => {
    return computed(() => {
        if (query.value === "") {
            return people;
        } else {
            return people.filter((person) => {
                if (person.username === "") {
                    person.username = person.email
                        .split("@")[0]
                        .split(/\.|-/)
                        .map((p) => p.charAt(0).toUpperCase() + p.slice(1))
                        .join(" ");
                }
                // VERY IMPORTANT: this line checks if the input matches either the username or the email
                return (
                    person.username.toLowerCase().includes(query.value.toLowerCase()) ||
                    person.email.toLowerCase().includes(query.value.toLowerCase())
                );
            });
        }
    });
};

const filteredPeople = getFilteredPeople(query, people);
const emit = defineEmits(["update:selectedPerson"]);
const selectedPerson = ref("");

watch(selectedPerson, (newValue) => {
    console.log(selectedPerson);
    hasValueEverBeenEntered.value = true; // to make the icon disappear

    emit("update:selectedPerson", newValue);
});

const inputValue = ref("");
const selectedPeople = ref([]);
const selectedCC = ref([]);
const selectedCCI = ref([]);
const AIContainer = ref(null);
const emailContent = ref(""); // To handle AI answers propositions
const responseKeywords = ref([]); // To handle AI answers propositions
const isFocused = ref(false);
const isFocused2 = ref(false);
const hasValueEverBeenEntered = ref(false);
const quill = ref(null);

const emailReceiver = sessionStorage.getItem("emailReceiver");

// function linked to ENTER key listeners
function handleBlur2(event) {
    // Checks for a valid input email and adds it to the recipients list
    isFocused2.value = false;
    const inputValue = event.target.value.trim().toLowerCase();
    const emailFormat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (inputValue && emailFormat.test(inputValue)) {
        // Add the input email to the list of recipients
        if (!people.find((person) => person.email === inputValue)) {
            const newPerson = { username: "", email: inputValue };
            people.push(newPerson);
            selectedPeople.value.push(newPerson);
        }
    } else if (!filteredPeople.value.length && inputValue) {
        // Show the pop-up
        backgroundColor = "bg-red-200/[.89] border border-red-400";
        notificationTitle.value = t("constants.popUpConstants.errorMessages.invalidEmail");
        notificationMessage.value = t("constants.popUpConstants.errorMessages.emailFormatIncorrect");
        displayPopup();
    }
}

// function linked to ENTER key listeners
function handleEnterKey(event) {
    // Allow pressing Enter with Shift to create a line break
    if (event.target.id === "dynamicTextarea" && event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        handleAIClick();
    } else if (isFocused2.value) {
        handleBlur2(event);
        // the user is still on the input
        handleFocusDestinary();
    }
}

function handleKeyDown(event) {
    if (event.ctrlKey) {
        switch (event.key) {
            case "b":
                quill.value.focus();
                event.preventDefault();
                break;
            case "d":
                document.getElementById("recipients").focus();
                event.preventDefault();
                break;
            case "k":
                document.getElementById("dynamicTextarea").focus();
                event.preventDefault();
                break;
            case "o":
                document.getElementById("objectInput").focus();
                event.preventDefault();
                break;
            case "Enter":
                sendEmail();
                break;
        }
    }
}

function parseEmails(emailData) {
    console.log("parsing emails", emailData);
    if (!emailData) {
        return [];
    }
    if (typeof emailData === "string") {
        // Handle the case where emailData is just an email string
        return [{ email: emailData, username: emailData.split("@")[0] }];
    } else if (Array.isArray(emailData)) {
        // Handle the case where emailData is an array of emails
        return emailData.map((data) => {
            return {
                email: data,
                username: "",
            };
        });
    } else if (typeof emailData === "object") {
        // Handle the case where emailData is a single tuple
        const [name, email] = emailData;
        return [
            {
                email: email || "",
                username: name || email.split("@")[0],
            },
        ];
    }

    return [];
}

function handleFocusObject() {
    isFocused.value = true;
}

function handleBlur() {
    isFocused.value = false;
}

function handleFocusDestinary() {
    isFocused2.value = true;
}

let counter_display = 0;

// To handle animations
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

function hideLoading() {
    const loadingElement = document.getElementById("dynamicLoadingIndicator");
    if (loadingElement) {
        loadingElement.remove();
    }
}

let stepcontainer = 0;

////////////////////////////////////////////////////// To Handle files upload ///////////////////////////////////////////////////////
const fileInput = ref(null);
const uploadedFiles = ref([]);
const fileObjects = ref([]);
const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25MB, Gmail's limit

const triggerFileInput = () => {
    fileInput.value.click();
};

const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    files.forEach((file) => {
        if (file.size <= MAX_FILE_SIZE) {
            let localStorageuploadedFiles = localStorage.getItem("uploadedFiles");

            for (const currentFile of localStorageuploadedFiles) {
                if (currentFile.name == file) {
                    // Show the pop-up
                    backgroundColor = "bg-red-200/[.89] border border-red-400";
                    notificationTitle = t("constants.popUpConstants.errorMessages.duplicateFile");
                    notificationMessage = t("constants.popUpConstants.errorMessages.fileAlreadyInserted");
                    displayPopup();
                    return;
                }
            }
            uploadedFiles.value.push({ name: file.name, size: file.size });
            fileObjects.value.push(file);
        } else {
            // Show the pop-up
            backgroundColor = "bg-red-200/[.89] border border-red-400";
            notificationTitle = t("constants.popUpConstants.errorMessages.fileTooLarge");
            notificationMessage = t("constants.popUpConstants.errorMessages.fileSizeExceedsLimit");
            displayPopup();
            console.error("File size exceeds Gmail's limit");
            return;
        }
    });
    saveFileMetadataToLocalStorage();
};

const removeFile = (index) => {
    uploadedFiles.value.splice(index, 1);
    fileObjects.value.splice(index, 1);
    saveFileMetadataToLocalStorage();
};

const saveFileMetadataToLocalStorage = () => {
    localStorage.setItem("uploadedFiles", JSON.stringify(uploadedFiles.value));
};

const loadFileMetadataFromLocalStorage = () => {
    const files = JSON.parse(localStorage.getItem("uploadedFiles")) || [];
    uploadedFiles.value = files;
};

////////////////////////////////////////////////////// To Select recipiers, CC and CCI ///////////////////////////////////////////////////////
const activeType = ref(null);

function personSelected(person) {
    if (!person) return;

    switch (activeType.value) {
        case "CC":
            if (!selectedCC.value.includes(person)) {
                selectedCC.value.push(person);

                console.log("CC", person.name);
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

    selectedPerson.value = null;
}

////////////////////////////////////////////////////// To handle AI Button click ///////////////////////////////////////////////////////

const subject = ref("");
const mail = ref("");
const mail_to_answer = ref("");

function displayMessage(message, ai_icon) {
    // Function to display a message from the AI Assistant
    const messageHTML = `
    <div class="flex pb-12">
      <div class="mr-4 flex">
        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            ${ai_icon}
          </svg>
        </span>   
      </div>
      <div>
        <p ref="animatedText${counter_display}"></p>
      </div>
    </div>
  `;
    AIContainer.value.innerHTML += messageHTML;
    const animatedParagraph = document.querySelector(`p[ref="animatedText${counter_display}"]`);
    counter_display += 1;
    animateText(message, animatedParagraph);
    scrollToBottom();
}

async function handleAIClick() {
    if (isAIWriting.value) {
        return;
    }

    isAIWriting.value = true;
    // Declare variables outside the fetch scope
    let messageHTML = "";
    let userInput = textareaValue.value;

    // Fetches the profile image URL from the server
    const requestOptions = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            email: emailReceiver,
        },
    };

    const data = await fetchWithToken(`${API_BASE_URL}user/social_api/get_profile_image/`, requestOptions);
    let imageURL = data.profile_image_url || require("@/assets/user.png");
    const profileImageHTML = `
    <img src="${imageURL}" alt="Profile Image" class="h-14 w-14 rounded-full">
  `;

    // Create the complete message HTML with the profile image and text
    messageHTML = `
    <div class="flex pb-12">
      <div class="mr-4 flex">
        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
          ${profileImageHTML}
        </span>
      </div>
      <div>
        <p class="font-serif" >${userInput}</p>
      </div>
    </div>
  `;
    AIContainer.value.innerHTML += messageHTML;

    textareaValueSave.value = textareaValue.value;
    textareaValue.value = "";
    console.log("textareaValueSave", textareaValueSave.value);

    setTimeout(async () => {
        if (stepcontainer == 0) {
            if (textareaValueSave.value == "") {
                const message = t("constants.sendEmailConstants.noSuggestionsEnteredPleaseTryAgain");
                const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`;
                displayMessage(message, ai_icon);
            } else {
                try {
                    MailCreatedByAI.value = true;
                    loading();
                    scrollToBottom();
                    const result = await fetchWithToken(`${API_BASE_URL}api/get_new_email_response/`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            body: quill.value.root.innerHTML,
                            userInput: textareaValueSave.value,
                            subject: inputValue.value,
                            importance: "Important", // TODO: get the importance of the email
                            history: history.value,
                        }),
                    });
                    hideLoading();
                    console.log("Generated Email Response:", result);

                    mail.value = result.email_body;
                    history.value = result.history;
                    const formattedMail = result.email_body.replace(/\n/g, "<br>");
                    const messageHTML = `
              <div class="flex pb-12">
                  <div class="mr-4 flex">
                      <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                        </svg>
                      </span>   
                  </div>
                  <div>
                      <p><strong>${t("answerPage.emailTwoDots")}</strong>${formattedMail}</p>
                  </div>
              </div>
          `;
                    AIContainer.value.innerHTML += messageHTML;
                    const quillEditorContainer = quill.value.root;
                    quillEditorContainer.innerHTML = result.email_body.replace(
                        /(<ul>|<ol>|<\/li>)(?:[\s]+)(<li>|<\/ul>|<\/ol>)/g,
                        "$1$2"
                    );

                    const message = "TODO Est-ce que cette réponse vous convient ?";
                    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
                    displayMessage(message, ai_icon);
                } catch (error) {
                    console.log("ERROR", error);
                    hideLoading();
                    const message =
                        "TODO Je m'excuse, j'ai fait une erreur de traitement. Est-ce que vous pouvez réessayer ?";
                    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
                    displayMessage(message, ai_icon);
                }
            }
        } else if (stepcontainer == 1) {
            // if the user enter an empty value
            if (textareaValueSave.value == "") {
                const message = "TODO Vous n'avez saisi aucune suggestion, veuillez réessayer";
                const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`;
                displayMessage(message, ai_icon);
            } else {
                console.log("MAIL CONTENT:", quill.value.root.innerHTML);
                console.log("EMAIL SUBJECT:", inputValue.value);
                console.log("USER RECOMMENDATION", textareaValueSave.value);
                try {
                    MailCreatedByAI.value = true;
                    loading();
                    scrollToBottom();
                    const result = await fetchWithToken(`${API_BASE_URL}api/get_new_email_response/`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            body: quill.value.root.innerHTML,
                            userInput: textareaValueSave.value,
                            subject: inputValue.value,
                            importance: "Important", // TODO: get the importance of the email
                            history: history.value,
                        }),
                    });
                    hideLoading();
                    mail.value = result.email_body;
                    history.value = result.history;
                    console.log("DEBUG ai conv step 1", result);
                    if (result.email_body) {
                        // TO FINISH => animation
                        hideLoading();
                        const formattedMail = result.email_body.replace(/\n/g, "<br>");
                        const messageHTML = `
                    <div class="flex pb-12">
                        <div class="mr-4 flex">
                            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                              </svg>
                            </span>   
                        </div>
                        <div>
                            <p><strong>${t("answerPage.emailTwoDots")}</strong>${formattedMail}</p>
                        </div>
                    </div>
                `;
                        AIContainer.value.innerHTML += messageHTML;
                        const quillEditorContainer = quill.value.root;
                        quillEditorContainer.innerHTML = result.email_body;

                        const message = "TODO Est-ce que ce mail vous convient mieux ?";
                        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
                        displayMessage(message, ai_icon);
                    } else {
                        hideLoading();
                        const message =
                            "TODO Je m'excuse, j'ai fait une erreur de traitement. Est-ce que vous pouvez réessayer ?";
                        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
                        displayMessage(message, ai_icon);
                        console.log("body is missing in the response");
                    }
                } catch (error) {
                    hideLoading();
                    const message =
                        "TODO Je m'excuse, j'ai fait une erreur de traitement. Est-ce que vous pouvez réessayer ?";
                    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
                    displayMessage(message, ai_icon);
                    console.error("There was a problem with the fetch operation: ", error);
                }
            }
        }
    }, 400);
}

////////////////////////////////////////////////////// To handle mail answer proposal ///////////////////////////////////////////////////////

// To display the propositions => buttons
function askContentAdvice() {
    if (isAIWriting.value) {
        return;
    }

    isAIWriting.value = true;

    const message = "TODO Comment puis-je vous aider à rédiger une réponse à cet email ?";

    let buttonsHTML = "";

    responseKeywords.value.forEach((keyword, index) => {
        // Start a new row for every two buttons
        if (index % 2 === 0) {
            buttonsHTML += index > 0 ? "</div>" : ""; // Close the previous row except for the first time
            buttonsHTML += '<div class="flex mt-4">'; // Start a new row
        }

        // Add the button to the current row
        buttonsHTML += `
          <div class="mr-4">
              <button type="button" id="responseKeywordButton${index}" data-value="${keyword}" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                  ${keyword}
              </button>
          </div>
      `;

        // Close the last row after adding the last button
        if (index === responseKeywords.value.length - 1) {
            buttonsHTML += "</div>";
        }
    });

    const messageHTML = `
      <div class="flex pb-12">
        <div class="mr-4 flex">
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900">
                <span class="text-lg font-medium leading-none text-white">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
                </svg>
                </span>
            </span>   
        </div>
        <div>
          <p ref="animatedText${counter_display}"></p>
          <div class="flex flex-col mt-4">
              ${buttonsHTML}
          </div>
        </div>
      </div>
  `;

    AIContainer.value.innerHTML += messageHTML;

    // Add event listeners to the buttons
    responseKeywords.value.forEach((keyword, index) => {
        setTimeout(() => {
            const keywordButton = document.getElementById(`responseKeywordButton${index}`);
            if (keywordButton) {
                keywordButton.addEventListener("click", () => {
                    handleButtonClick(keywordButton.getAttribute("data-value"));
                });
            }
        }, 0);
    });

    const animatedParagraph = document.querySelector(`p[ref="animatedText${counter_display}"]`);
    counter_display += 1;
    animateText(message, animatedParagraph);

    const message2 = "Quelle longueur de mail et formalité souhaitez vous ?";
    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
    displayMessage(message2, ai_icon);
}

async function handleButtonClick(keyword) {
    if (isAIWriting.value) {
        return;
    }

    isAIWriting.value = true;

    console.log("Button clicked with keyword:", keyword);
    try {
        MailCreatedByAI.value = true;
        loading();
        scrollToBottom();
        const result = await fetchWithToken(`${API_BASE_URL}api/generate_email_answer/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email_subject: inputValue.value,
                email_content: emailContent.value,
                response_type: keyword,
            }),
        });
        hideLoading();
        console.log("Generated Email Response:", result);
        const formattedMail = result.email_answer.replace(/\n/g, "<br>");
        const messageHTML = `
        <div class="flex pb-12">
            <div class="mr-4 flex">
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                  </svg>
                </span>   
            </div>
            <div>
                <p><strong>${t("answerPage.emailTwoDots")}</strong>${formattedMail}</p>
            </div>
        </div>
    `;
        AIContainer.value.innerHTML += messageHTML;
        const quillEditorContainer = quill.value.root;
        quillEditorContainer.innerHTML = result.email_answer;

        const message = "TODO Est-ce que cette réponse vous convient ?";
        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
        displayMessage(message, ai_icon);
    } catch (error) {
        console.log("ERROR", error);
        hideLoading();
        const message = "TODO Je m'excuse, j'ai fait une erreur de traitement. Est-ce que vous pouvez réessayer ?";
        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
        displayMessage(message, ai_icon);
    }
}

async function fetchResponseKeywords(subject) {
    try {
        loading();
        const data = await fetchWithToken(`${API_BASE_URL}api/generate_email_response_keywords/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email_subject: subject, email_content: emailContent.value }),
        });
        hideLoading();
        console.log("DEBUG ANSWER PROPOSAL", data);

        console.log("DEBUG 2", data.response_keywords);
        responseKeywords.value = data.response_keywords;
        console.log(typeof data.response_keywords);
        console.log(Array.isArray(data.response_keywords));
        askContentAdvice();
    } catch (error) {
        console.error("Error fetching response keywords:", error.message);
    }
}

////////////////////////////////////////////////////// To handle the user writing his own answer  ///////////////////////////////////////////////////////

const MailCreatedByAI = ref(false);
const isFirstTimeEmail = ref(true);

function handleInputUpdateMailContent(newMessage) {
    if (newMessage !== "") {
        if (isFirstTimeEmail.value && !MailCreatedByAI.value) {
            askContentAdviceUser();
            isFirstTimeEmail.value = false;
            stepcontainer = 1;
            scrollToBottom();
        }
    }
    MailCreatedByAI.value = false;
}

function askContentAdviceUser() {
    const message = t("constants.sendEmailConstants.emailCompositionAssistance");

    const messageHTML = `
      <div class="pb-12">
        <div class="flex">
            <div class="mr-4">
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
                  </svg>
                </span>
            </div>
            <div>
                <div class="flex flex-col">
                  <p ref="animatedText${counter_display}"></p>
                  <div class="flex mt-4">
                    <div class="mr-4">
                      <button type="button" id="spellCheckButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                        ${t("newPage.correctSpelling")}
                      </button>
                    </div>
                    <div>
                      <button type="button" id="CopyWritingCheckButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                        ${t("newPage.checkCopywriting")}
                      </button>
                    </div>
                  </div>
                  <div class="flex mt-4">
                    <div class="mr-4">
                      <button type="button" id="WriteBetterButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                        ${t("newPage.improveWriting")}
                      </button>
                    </div>
                  </div>
                </div>
            </div>
        </div>
      </div>
    `;

    AIContainer.value.innerHTML += messageHTML;

    // To check the ortgraph of the subject and the mail
    setTimeout(() => {
        const spellCheckButton = document.getElementById("spellCheckButton");
        if (spellCheckButton) {
            spellCheckButton.addEventListener("click", checkSpelling);
        }
    }, 0);

    setTimeout(() => {
        const CopyWritingCheckButton = document.getElementById("CopyWritingCheckButton");
        if (CopyWritingCheckButton) {
            CopyWritingCheckButton.addEventListener("click", checkCopyWriting);
        }
    }, 0);

    setTimeout(() => {
        const WriteBetterButton = document.getElementById("WriteBetterButton");
        if (WriteBetterButton) {
            WriteBetterButton.addEventListener("click", WriteBetter);
        }
    }, 0);

    const animatedParagraph = document.querySelector(`p[ref="animatedText${counter_display}"]`);
    counter_display += 1;
    animateText(message, animatedParagraph);
}

// async function checkSpelling() {
//   try {
//     loading();
//     scrollToBottom();
//     const result = await fetchWithToken(`${API_BASE_URL}api/correct_email_language/`, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({
//         email_subject: inputValue.value,
//         email_body: quill.value.root.innerHTML,
//       }),
//     });
//     hideLoading();

//     console.log(result);
//     if (result.corrected_subject && result.corrected_body) {

//       const formattedMail = result.corrected_body.replace(/\n/g, '<br>');
//       const messageHTML = `
//               <div class="flex pb-12">
//                   <div class="mr-4 flex">
//                       <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
//                         <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
//                           <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
//                         </svg>
//                       </span>
//                   </div>
//                   <div>
//                       <p><strong>${t('newPage.subject')}</strong>${result.corrected_subject}</p>
//                       <p><strong>${t('newPage.emailContent')}</strong>${formattedMail}</p>
//                   </div>
//               </div>
//           `;
//       AIContainer.value.innerHTML += messageHTML;
//       inputValue.value = result.corrected_subject;
//       const quillEditorContainer = quill.value.root;
//       quillEditorContainer.innerHTML = result.corrected_body;

//       const message = "TODO J'ai corrigé l'orthographe, est-ce que souhaitez autre chose ?";
//       const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
//       displayMessage(message, ai_icon);
//     } else {
//       hideLoading();
//       const message = "TODO Je m'excuse, j'ai fait une erreur de traitement."
//       const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
//       displayMessage(message, ai_icon);
//       console.log('Subject or Email is missing in the response');
//     }

//   } catch (error) {
//     console.error('Error:', error);
//     hideLoading();
//     const message = "TODO Je m'excuse, j'ai fait une erreur de traitement."
//     const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
//     displayMessage(message, ai_icon);
//   }
// }

// async function checkCopyWriting() {
//   try {
//     loading();
//     scrollToBottom();
//     const result = await fetchWithToken(`${API_BASE_URL}api/check_email_copywriting/`, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({
//         email_subject: inputValue.value,
//         email_body: quill.value.root.innerHTML,
//       }),
//     });
//     hideLoading();

//     console.log(result);
//     if (result.feedback_copywriting) {

//       const formattedCopWritingOutput = result.feedback_copywriting.replace(/\n/g, '<br>');

//       const messageHTML = `
//               <div class="flex pb-12">
//                   <div class="mr-4 flex">
//                       <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
//                         <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
//                           <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
//                         </svg>
//                       </span>
//                   </div>
//                   <div>
//                       <p>${formattedCopWritingOutput}</p>
//                   </div>
//               </div>
//           `;
//       AIContainer.value.innerHTML += messageHTML;
//       const message = "TODO J'ai vérifié le copywriting, est-ce que souhaitez autre chose ?";
//       const messageHTML2 = `
//               <div class="flex pb-12">
//                   <div class="mr-4 flex">
//                       <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
//                         <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
//                           <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
//                         </svg>
//                       </span>
//                   </div>
//                   <div>
//                     <p ref="animatedText${counter_display}"></p>
//                   </div>
//               </div>
//           `;
//       AIContainer.value.innerHTML += messageHTML2;
//       const animatedParagraph = document.querySelector(`p[ref="animatedText${counter_display}"]`);
//       counter_display += 1;
//       animateText(message, animatedParagraph);

//       scrollToBottom();
//     } else {
//       hideLoading();
//       const message = "TODO Je m'excuse, j'ai fait une erreur de traitement."
//       const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
//       displayMessage(message, ai_icon);
//       console.log('Subject or Email is missing in the response');
//     }

//   } catch (error) {
//     console.error('Error:', error);
//     hideLoading();
//     const message = "TODO Je m'excuse, j'ai fait une erreur de traitement."
//     const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
//     displayMessage(message, ai_icon);
//   }
// }

// async function WriteBetter() {
//   // TODO for Jean & Théo: THIS FUNCTION IS NOT WORKING: must implement api/improve_draft/
//   // check New.vue (must implement a system of memory)
//   try {
//     loading();
//     scrollToBottom();
//     const result = await fetchWithToken(`${API_BASE_URL}api/new_email_recommendations/`, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({
//         mail_content: quill.value.root.innerHTML,
//         user_recommendation: t('constants.sendEmailConstants.improveEmailWriting'),
//         email_subject: inputValue.value,
//       }),
//     });
//     hideLoading();
//     subject.value = result.subject;
//     mail.value = result.email_body;
//     console.log(result);
//     if (result.subject && result.email_body) {

//       const formattedMail = result.email_body.replace(/\n/g, '<br>');
//       const messageHTML = `
//             <div class="flex pb-12">
//                 <div class="mr-4 flex">
//                     <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
//                       <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
//                         <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
//                       </svg>
//                     </span>
//                 </div>
//                 <div>
//                   <p><strong>${t('newPage.subject')}</strong>${result.subject}</p>
//                   <p><strong>${t('newPage.emailContent')}</strong>${formattedMail}</p>
//                 </div>
//             </div>
//         `;
//       AIContainer.value.innerHTML += messageHTML;
//       inputValue.value = result.subject;
//       const quillEditorContainer = quill.value.root;
//       quillEditorContainer.innerHTML = result.email_body;

//       const message = "TODO Est-ce que ce mail vous convient mieux ?";
//       const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`
//       displayMessage(message, ai_icon);
//     } else {
//       hideLoading();
//       const message = "TODO Je m'excuse, j'ai fait une erreur de traitement. Est-ce que vous pouvez réessayer ?"
//       const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
//       displayMessage(message, ai_icon);
//       console.log('Subject or Email is missing in the response');
//     }
//   } catch (error) {
//     console.error('Error:', error);
//     hideLoading();
//     const message = "TODO Je m'excuse, j'ai fait une erreur de traitement. Est-ce que vous pouvez réessayer ?"
//     const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`
//     displayMessage(message, ai_icon);
//     console.error('There was a problem with the fetch operation: ', error);
//   }
// }

////////////////////////////////////////////////////// To handle sending the email  ///////////////////////////////////////////////////////

const router = useRouter();

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// To keep the navbar always at the bottom when new content is added
const scrollableDiv = ref(null);
const scrollToBottom = async () => {
    await nextTick();
    const element = scrollableDiv.value;
    element.scrollTop = element.scrollHeight;
};

// AI instruction textarea input
const textareaValue = ref("");
const textareaValueSave = ref("");
const bgColor = ref(""); // Initialize a reactive variable
const route = useRoute();

onMounted(() => {
    localStorage.removeItem("uploadedFiles");
    document.addEventListener("keydown", handleKeyDown);

    bgColor.value = localStorage.getItem("bgColor");
    loadFileMetadataFromLocalStorage(); // For uploaded file

    const subject = JSON.parse(sessionStorage.getItem("subject"));
    const cc = sessionStorage.getItem("cc");
    const bcc = sessionStorage.getItem("bcc");
    const decoded_data = JSON.parse(sessionStorage.getItem("decodedData"));
    const email = JSON.parse(sessionStorage.getItem("email"));
    //const idProvider = JSON.parse(sessionStorage.getItem("idProvider"));
    const details = JSON.parse(sessionStorage.getItem("details"));

    console.log("DEBUG CC------------------");
    console.log(cc);

    console.log("DEBUG BCC------------------");
    console.log(bcc);
    // Initialize Quill editor
    quill.value = new Quill("#editor", {
        theme: "snow",
        modules: {
            toolbar: toolbarOptions,
        },
    });

    window.addEventListener("resize", scrollToBottom); // To keep the scroll in the scrollbar at the bottom even when viewport change

    var toolbarOptions = [
        [{ font: [] }],
        [{ header: [1, 2, 3, 4, 5, 6, false] }],
        ["bold", "italic", "underline"],
        [{ color: [] }, { background: [] }],
        [{ list: "ordered" }, { list: "bullet" }],
        [{ align: [] }],
        ["blockquote", "code-block"],
    ];

    mail_to_answer.value = decoded_data;

    // DOM-related code
    AIContainer.value = document.getElementById("AIContainer");

    // Construct the email HTML
    let emailHTML = `
    <div class="flex pb-12">
        <div class="mr-4 flex">
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                </svg>
            </span>   
        </div>
        <div>
            <p><strong>${subject}</strong></p>
            <br>
            <div>${decoded_data.replace(/\n/g, "<br>")}</div>
        </div>
    </div>
`;

    // Append the email HTML to the container
    AIContainer.value.innerHTML += emailHTML;

    const message = "Résumé de l'email : ";

    // Start with the initial HTML structure
    let messageHTML = `
    <div class="flex pb-12">
        <div class="mr-4 flex">
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
            </svg>
            </span>   
        </div>
        <div>
            <p class="font-bold">${message}</p>
            <ul>
    `;

    // Add each bullet point to the HTML
    details.forEach((detail) => {
        messageHTML += `<li class="pt-2">
                        <p><span class="font-bold text-2xl">-</span> ${detail.text}</p>
                    </li>`;
    });

    // Close the HTML structure
    messageHTML += `
            </ul>
        </div>
    </div>
    `;

    AIContainer.value.innerHTML += messageHTML;

    emailContent.value = details.map((item) => item.text).join(" "); // USELESS => To Optimize
    fetchResponseKeywords(subject);

    quill.value.on("text-change", function () {
        const quillContent = quill.value.root.innerHTML;
        if (quillContent.trim() !== "<p><br></p>") {
            mail.value = quillContent;
            handleInputUpdateMailContent(quillContent);
        }
    });

    if (email) {
        selectedPeople.value = parseEmails(email);
        console.log("SELECTED PEOPLE", selectedPeople.value);
    }
    if (cc) {
        selectedCC.value = parseEmails(cc);
    }
    if (bcc) {
        selectedCCI.value = parseEmails(bcc);
    }

    inputValue.value = "Re : " + subject;
});

function animateText(text, target) {
    let characters = text.split("");
    let currentIndex = 0;
    const interval = setInterval(() => {
        if (currentIndex < characters.length) {
            target.textContent += characters[currentIndex];
            currentIndex++;
        } else {
            // AI has finished to write its message
            clearInterval(interval);
            // reset the status
            isAIWriting.value = false;
        }
    }, 30);
}
</script>

<script>
import NavBarLarge from "@/global/components/NavBarLarge.vue";
import NavBarSmall from "@/global/components/NavBarSmall.vue";

import { UserGroupIcon, Bars2Icon } from "@heroicons/vue/24/outline";
import { fetchWithToken } from "@/global/security";
import { API_BASE_URL } from "@/global/const";
import ManualEmail from "./components/ManualEmail.vue";
import NavBarSmall from "@/global/components/NavBarSmall.vue";

export default {
    components: {
        NavBarLarge,
        NavBarSmall,
        UserGroupIcon,
        Bars2Icon,
    },
    methods: {
        adjustHeight(event) {
            const textarea = event.target;
            const maxHeight = 250; // Set your desired max height in pixels. TO SET DEPENDING OF THE SIZE OF THE VIEWPORT

            // Reset height to auto to correctly calculate the new scrollHeight
            textarea.style.height = "auto";

            if (textarea.scrollHeight > maxHeight) {
                textarea.style.height = maxHeight + "px";
                textarea.style.overflowY = "auto"; // Enable scrolling when content exceeds maxHeight.
            } else {
                textarea.style.height = textarea.scrollHeight + "px";
                textarea.style.overflowY = "hidden"; // Hide the scrollbar when content is below maxHeight.
            }
        },
    },
    mounted() {},
};
</script>

<!-- TODO: FOLLOW these guidelines anyway
the import of constants and function are correct. You must do the following operations:

if possible put everything under script setup if its more optimal and easier to manage
remove all comments (unless those who mentionned Théo & Jean) you DELETE the rest no execption
optimize the code
use strictly camelCase
we are using TypeScript so migrate everything where its needed using interfaces or types -->
