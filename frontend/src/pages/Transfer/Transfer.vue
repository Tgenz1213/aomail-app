<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
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

<script setup lang="ts">
import { ref, onMounted, nextTick, provide, Ref } from "vue";
import Quill from "quill";
import AiEmail from "./components/AiEmail.vue";
import ManualEmail from "@/global/components/ManualEmail/ManualEmail.vue";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { getData, postData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import { Recipient, EmailLinked, UploadedFile } from "@/global/types";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";

const showNotification = ref(false);
const isWriting = ref(false);
const isLoading = ref(false);
const isFirstTimeEmail = ref(true);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const subjectInput = ref("");
const textareaValueSave = ref("");
const AiEmailBody = ref("");
const subject = ref("");
const emailSelected = ref(localStorage.getItem("email") || "");
const selectedLength = ref("short");
const selectedFormality = ref("formal");
const timerId = ref<number | null>(null);
const AIContainer = ref<HTMLElement | null>(null);
const scrollableDiv = ref<HTMLDivElement | null>(null);
const quill: Ref<Quill | null> = ref(null);
const counterDisplay = ref(0);
const history = ref({});
const emailsLinked = ref<EmailLinked[]>([]);
const selectedPeople = ref<Recipient[]>([]);
const selectedCC = ref<Recipient[]>([]);
const selectedBCC = ref<Recipient[]>([]);
const stepContainer = ref(0);
const contacts = ref<Recipient[]>([]);
const uploadedFiles = ref<UploadedFile[]>([]);
const fileObjects = ref<File[]>([]);

const scrollToBottom = async () => {
    await nextTick();
    const element = scrollableDiv.value;
    if (!element) return;
    element.scrollTop = element.scrollHeight;
};

provide("emailSelected", emailSelected);
provide("selectedPeople", selectedPeople);
provide("selectedCC", selectedCC);
provide("selectedBCC", selectedBCC);
provide("quill", quill);
provide("stepContainer", stepContainer);
provide("AIContainer", AIContainer);
provide("counterDisplay", counterDisplay);
provide("isWriting", isWriting);
provide("uploadedFiles", uploadedFiles);
provide("fileObjects", fileObjects);
provide("subjectInput", subjectInput);
provide("emailsLinked", emailsLinked);
provide("contacts", contacts);
provide("history", history);
provide("AiEmailBody", AiEmailBody);
provide("textareaValueSave", textareaValueSave);
provide("selectedLength", selectedLength);
provide("selectedFormality", selectedFormality);
provide("displayPopup", displayPopup);
provide("displayMessage", displayMessage);
provide("scrollToBottom", scrollToBottom);
provide("loading", loading);
provide("hideLoading", hideLoading);

onMounted(async () => {
    AIContainer.value = document.getElementById("AIContainer");

    document.addEventListener("keydown", handleKeyDown);
    localStorage.removeItem("uploadedFiles");
    window.addEventListener("resize", scrollToBottom);

    const message = i18n.global.t("constants.sendEmailConstants.emailRecipientRequest");
    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;

    displayMessage(message, aiIcon);
    fetchRecipients();

    localStorage.removeItem("uploadedFiles");

    document.addEventListener("keydown", handleKeyDown);

    // const subject = JSON.parse(sessionStorage.getItem("subject"));
    const cc = sessionStorage.getItem("cc");
    const bcc = sessionStorage.getItem("bcc");
    // const decoded_data = JSON.parse(sessionStorage.getItem("decoded_data"));
    // const email = JSON.parse(sessionStorage.getItem("email"));
    //const id_provider = JSON.parse(sessionStorage.getItem("id_provider"));
    // const details = JSON.parse(sessionStorage.getItem("details"));
    // const date = JSON.parse(sessionStorage.getItem("date"));

    // Prepare the forwarded email
    inputValue.value = "Tr : " + subject.value;
    // const formattedDateVar = new Date(date);
    const options = {
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
    };

    // TODO: use the selected timezone of the user
    // const formattedDate = formattedDateVar.toLocaleDateString("fr-FR", options);

    let forwardedMessage = "";

    // TODO: use the var from JSON it's ready
    forwardedMessage += "Résumé de l'email:\n";
    // details.forEach((detail) => {
    //     forwardedMessage += `- ${detail.text}\n`;
    // });
    forwardedMessage += "\n\n";
    forwardedMessage += "---------- Message transféré ---------\n";
    // forwardedMessage += `De: ${email}\n`;
    // forwardedMessage += `Date: ${formattedDate}\n`;
    forwardedMessage += `Sujet: ${subject.value}\n`;

    // if (cc.length > 0) {
    //     forwardedMessage += `CC: ${cc}\n`;
    // }

    forwardedMessage += "\n\n";
    // forwardedMessage += decoded_data;
    if (quill.value) {
        quill.value.setText(forwardedMessage);
    }

    await initializeQuill();

    // const message = t("constants.sendEmailConstants.emailRecipientRequest");
    // const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
    // displayMessage(message, ai_icon);
    // objectInput.value = document.getElementById("objectInput");

    // const form = objectInput.value.closest("form");
    // if (form) {
    //     form.addEventListener("submit", function (e) {
    //         e.preventDefault();
    //     });
    // }
});

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

let isAIWriting = ref(false);
const userSearchResult = ref(null);

async function fetchRecipients() {
    const result = await getData(`user/contacts/`);

    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.contactFetchError"),
            result.error as string
        );
        return;
    }

    contacts.value.push(...(result.data as Recipient[]));
}

const emailReceiver = sessionStorage.getItem("emailReceiver");
const activeType = ref(null);
const emit = defineEmits(["update:selectedPerson"]);
const selectedPerson = ref("");
const inputValue = ref("");
const isFirstTimeDestinary = ref(true);
const isFocused = ref(false);
let stepcontainer = 0;
const objectInput = ref(null);

function displayMessage(message: string, aiIcon: string) {
    if (!AIContainer.value) return;

    const messageHTML = `
      <div class="flex pb-12">
        <div class="mr-4 flex">
            <!--
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full overflow-hidden">
              <img src="${aiIcon}" alt="aiIcon" class="max-w-full max-h-full rounded-full">
            </span>-->
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                ${aiIcon}
                </svg>
            </span>
        </div>
        <div>
          <p ref="animatedText${counterDisplay.value}"></p>
        </div>
      </div>
    `;

    AIContainer.value.innerHTML += messageHTML;
    const animatedParagraph = document.querySelector(`p[ref="animatedText${counterDisplay.value}"]`);
    counterDisplay.value += 1;
    animateText(message, animatedParagraph);
    scrollToBottom();
}

function displayErrorProcessingMessage() {
    const message = i18n.global.t("constants.sendEmailConstants.processingErrorApology");
    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
    displayMessage(message, aiIcon);
}

async function findUser(searchQuery: string) {
    const result = await getData("api/find_user_ai/?query=" + encodeURIComponent(searchQuery));

    if (!result.success) {
        displayErrorProcessingMessage();
        return;
    }

    userSearchResult.value = result.data;
    return result.data;
}

async function handleAIClick() {
    // if (isAIWriting.value) {
    //     return;
    // }
    // isAIWriting.value = true;
    // // Declare variables outside the fetch scope
    // let messageHTML = "";
    // let userInput = textareaValue.value;
    // // Fetches the profile image URL from the server
    // const requestOptions = {
    //     method: "GET",
    //     headers: {
    //         "Content-Type": "application/json",
    //         email: emailReceiver,
    //     },
    // };
    // const data = await fetchWithToken(`${API_BASE_URL}user/social_api/get_profile_image/`, requestOptions);
    // let imageURL = data.profile_image_url || require("@/assets/user.png");
    // const profileImageHTML = `
    //   <img src="${imageURL}" alt="Profile Image" class="h-14 w-14 rounded-full">
    // `;
    // // Create the complete message HTML with the profile image and text
    // messageHTML = `
    //   <div class="flex pb-12">
    //     <div class="mr-4 flex">
    //       <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
    //         ${profileImageHTML}
    //       </span>
    //     </div>
    //     <div>
    //       <p class="font-serif">${userInput}</p>
    //     </div>
    //   </div>
    // `;
    // AIContainer.value.innerHTML += messageHTML;
    // textareaValueSave.value = textareaValue.value;
    // textareaValue.value = "";
    // scrollToBottom();
    // setTimeout(async () => {
    //     if (stepcontainer == 0) {
    //         if (textareaValueSave.value == "") {
    //             const message = t("constants.sendEmailConstants.noRecipientsEntered");
    //             const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`;
    //             displayMessage(message, ai_icon);
    //         } else {
    //             try {
    //                 isLoading.value = true;
    //                 loading();
    //                 scrollToBottom();
    //                 const result = await findUser(textareaValueSave.value);
    //                 hideLoading();
    //                 //textareaValue.value = ''; // TO REINIT => CREATE A WASTE OF TIME => DO NOT USE BUT KEEP IF NEEDED
    //                 let noUsersAdded = true;
    //                 let WaitforUserChoice = false;
    //                 if (result.error != "Invalid input or query not about email recipients") {
    //                     // To update to handle the main error
    //                     const main_recipients = userSearchResult.value.main_recipients;
    //                     const cc_recipients = userSearchResult.value.cc_recipients;
    //                     const bcc_recipients = userSearchResult.value.bcc_recipients;
    //                     console.log("debug", main_recipients, cc_recipients, bcc_recipients);
    //                     for (let i = 0; i < main_recipients.length; i++) {
    //                         const user = main_recipients[i];
    //                         const emails = user.email;
    //                         if (emails.length == 1) {
    //                             const person = { username: user.username, email: emails[0] };
    //                             selectedPeople.value.push(person);
    //                             main_recipients.splice(i, 1);
    //                             noUsersAdded = false;
    //                             i--;
    //                         }
    //                     }
    //                     for (let i = 0; i < cc_recipients.length; i++) {
    //                         const user = cc_recipients[i];
    //                         const emails = user.email;
    //                         if (emails.length == 1) {
    //                             const person = { username: user.username, email: emails[0] };
    //                             selectedCC.value.push(person);
    //                             delete cc_recipients[i];
    //                             cc_recipients.splice(i, 1);
    //                             noUsersAdded = false;
    //                             i--;
    //                         }
    //                     }
    //                     for (let i = 0; i < bcc_recipients.length; i++) {
    //                         const user = bcc_recipients[i];
    //                         const emails = user.email;
    //                         if (emails.length == 1) {
    //                             const person = { username: user.username, email: emails[0] };
    //                             selectedBCC.value.push(person);
    //                             bcc_recipients.splice(i, 1);
    //                             noUsersAdded = false;
    //                             i--;
    //                         }
    //                     }
    //                     // This condition is used to display the diffrent mail possibilities
    //                     if (main_recipients.length > 0 || cc_recipients.length > 0 || bcc_recipients.length > 0) {
    //                         const messageHTML = `
    //                             <div class="flex pb-2">
    //                                 <div class="mr-4 flex">
    //                                     <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
    //                                         <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
    //                                         <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
    //                                         </svg>
    //                                     </span>
    //                                 </div>
    //                                 <div>
    //                                     <p>${t("constants.sendEmailConstants.multipleEmailsFoundForSomeRecipients")}</p>
    //                                 </div>
    //                             </div>
    //                         `;
    //                         AIContainer.value.innerHTML += messageHTML;
    //                         if (main_recipients.length > 0) {
    //                             WaitforUserChoice = true;
    //                             const emailList = [];
    //                             for (const user of main_recipients) {
    //                                 for (const email of user.email) {
    //                                     if (user.email !== "") {
    //                                         // Creating an object for each email and pushing it to the emailList array
    //                                         const emailMapping = {};
    //                                         emailMapping[user.username] = email;
    //                                         emailList.push(emailMapping);
    //                                         noUsersAdded = false;
    //                                     }
    //                                 }
    //                             }
    //                             askChoiceRecipier(emailList, "main");
    //                         }
    //                         if (cc_recipients.length > 0) {
    //                             WaitforUserChoice = true;
    //                             const emailList = [];
    //                             for (const user of cc_recipients) {
    //                                 for (const email of user.email) {
    //                                     if (user.email !== "") {
    //                                         // Creating an object for each email and pushing it to the emailList array
    //                                         const emailMapping = {};
    //                                         emailMapping[user.username] = email;
    //                                         emailList.push(emailMapping);
    //                                         noUsersAdded = false;
    //                                     }
    //                                 }
    //                             }
    //                             askChoiceRecipier(emailList, "cc");
    //                         }
    //                         if (bcc_recipients.length > 0) {
    //                             WaitforUserChoice = true;
    //                             const emailList = [];
    //                             for (const user of bcc_recipients) {
    //                                 for (const email of user.email) {
    //                                     if (user.email !== "") {
    //                                         // Creating an object for each email and pushing it to the emailList array
    //                                         const emailMapping = {};
    //                                         emailMapping[user.username] = email;
    //                                         emailList.push(emailMapping);
    //                                         noUsersAdded = false;
    //                                     }
    //                                 }
    //                             }
    //                             askChoiceRecipier(emailList, "bcc");
    //                         }
    //                         scrollToBottom();
    //                     }
    //                     if (noUsersAdded) {
    //                         console.log("DEBUG");
    //                         const message = t(
    //                             "constants.sendEmailConstants.noRecipientsFoundPleaseTryAgainOrEnterManually"
    //                         );
    //                         const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
    //                         displayMessage(message, ai_icon);
    //                     } else if (!WaitforUserChoice) {
    //                         stepcontainer = 1;
    //                     }
    //                 } else {
    //                     const message = t(
    //                         "constants.sendEmailConstants.noRecipientsFoundPleaseTryAgainOrEnterManually"
    //                     );
    //                     const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
    //                     displayMessage(message, ai_icon);
    //                 }
    //             } catch (error) {
    //                 const message = t("constants.sendEmailConstants.processingErrorApology");
    //                 const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
    //                 displayMessage(message, ai_icon);
    //                 console.error("Error finding user", error);
    //             }
    //         }
    //     }
    // }, 0);
}

async function initializeQuill() {
    const toolbarOptions = [
        [{ font: [] }],
        [{ header: [1, 2, 3, 4, 5, 6, false] }],
        ["bold", "italic", "underline"],
        [{ color: [] }, { background: [] }],
        [{ list: "ordered" }, { list: "bullet" }],
        [{ align: [] }],
        ["blockquote", "code-block"],
    ];

    const editorElement = document.getElementById("editor");
    if (editorElement) {
        quill.value = new Quill(editorElement, {
            theme: "snow",
            modules: { toolbar: toolbarOptions },
        });
    }

    if (quill.value) {
        quill.value.on("text-change", function () {
            AiEmailBody.value = quill.value?.root.innerHTML ?? "";
            if (isFirstTimeEmail.value) {
                const quillContent = quill.value?.root.innerHTML ?? "";
                if (quillContent.trim() !== "<p><br></p>") {
                    AiEmailBody.value = quillContent;
                    handleInputUpdateMailContent(quillContent);
                    isFirstTimeEmail.value = false;
                }
            }
        });
    }
}

function askContentAdvice() {}

function handleInputUpdateMailContent(newMessage: string) {
    if (newMessage !== "") {
        if (selectedPeople.value.length > 0 || selectedCC.value.length > 0 || selectedBCC.value.length > 0) {
            askContentAdvice();
            stepContainer.value = 2;
            scrollToBottom();
        }
    }
}

function animateText(text: string, target: Element | null) {
    let characters = text.split("");
    let currentIndex = 0;
    const interval = setInterval(() => {
        if (currentIndex < characters.length) {
            if (!target) return;
            target.textContent += characters[currentIndex];
            currentIndex++;
        } else {
            clearInterval(interval);
            isWriting.value = false;
        }
    }, 30);
}

function loading() {
    isLoading.value = true;
    if (!AIContainer.value) return;

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
    scrollToBottom();
}

function hideLoading() {
    const loadingElement = document.getElementById("dynamicLoadingIndicator");
    if (loadingElement) {
        loadingElement.remove();
    }
}

function handleKeyDown(event: KeyboardEvent) {
    if (event.ctrlKey) {
        const recipients = document.getElementById("recipients");
        const subjectInput = document.getElementById("subjectInput") as HTMLInputElement | null;
        const dynamicTextarea = document.getElementById("dynamicTextarea");

        switch (event.key) {
            case "d":
                recipients?.focus();
                event.preventDefault();
                break;
            case "k":
                dynamicTextarea?.focus();
                event.preventDefault();
                break;
            case "o":
                subjectInput?.focus();
                event.preventDefault();
                break;
        }
    }
}
</script>
