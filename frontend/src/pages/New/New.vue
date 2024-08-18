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
import { computed, ref, onMounted, nextTick, provide, Ref, onUnmounted } from "vue";
import Quill from "quill";
import AiEmail from "./components/AiEmail.vue";
import ManualEmail from "./components/ManualEmail.vue";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { getData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import { Recipient, EmailLinked, UploadedFile } from "@/global/types";
import NavBarSmall from "@/global/components/NavBarSmall.vue";

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);
const AIContainer = ref<HTMLElement | null>(document.getElementById("AIContainer"));
const counterDisplay = ref(0);
const scrollableDiv = ref<HTMLDivElement | null>(null);

// let history = ref({});

const emailsLinked = ref<EmailLinked[]>([]);
const emailSelected = ref(localStorage.getItem("email") || "");
const selectedPeople = ref<Recipient[]>([]);
const selectedCC = ref<Recipient[]>([]);
const selectedCCI = ref<Recipient[]>([]);
const quill: Ref<Quill | null> = ref(null);
const stepContainer = ref(0);
const contacts = ref<Recipient[]>([]);
const isAIWriting = ref(false);
const uploadedFiles = ref<UploadedFile[]>([]);
const inputSubject = ref("");

onMounted(async () => {
    fetchEmailLinked();
    fetchRecipients();

    if (!emailSelected.value) {
        const result = await getData("user/get_first_email/");

        if (!result.success) {
            displayPopup(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.primaryEmailFetchError"),
                result.error as string
            );
        }

        emailSelected.value = result.data.email;
        localStorage.setItem("email", result.data.email);
    }

    var toolbarOptions = [
        [{ font: [] }],
        [{ header: [1, 2, 3, 4, 5, 6, false] }],
        ["bold", "italic", "underline"],
        [{ color: [] }, { background: [] }],
        [{ list: "ordered" }, { list: "bullet" }],
        [{ align: [] }],
        ["blockquote", "code-block"],
    ];

    quill.value = new Quill("#editor", {
        theme: "snow",
        modules: {
            toolbar: toolbarOptions,
        },
    });

    window.addEventListener("beforeunload", handleBeforeUnload);
});

onUnmounted(() => {
    window.removeEventListener("beforeunload", handleBeforeUnload);
});

const handleBeforeUnload = (event: BeforeUnloadEvent) => {
    if (
        uploadedFiles.value.length ||
        selectedPeople.value.length ||
        selectedCC.value.length ||
        selectedCCI.value.length ||
        inputSubject.value !== ""
    ) {
        event.preventDefault();
    }
};

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
            isAIWriting.value = false;
        }
    }, 30);
}

const scrollToBottom = async () => {
    await nextTick();
    const element = scrollableDiv.value;
    if (!element) return;
    element.scrollTop = element.scrollHeight;
};

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
          <p ref="animatedText${counterDisplay}"></p>
        </div>
      </div>
    `;

    AIContainer.value.innerHTML += messageHTML;
    const animatedParagraph = document.querySelector(`p[ref="animatedText${counterDisplay}"]`);
    counterDisplay.value += 1;
    animateText(message, animatedParagraph);
    scrollToBottom();
}

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

async function fetchEmailLinked() {
    const result = await getData(`user/emails_linked/`);

    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailLinkedFetchError"),
            result.error as string
        );
        return;
    }

    emailsLinked.value = result.data;
}

provide("displayPopup", displayPopup);
provide("emailSelected", emailSelected);
provide("selectedPeople", selectedPeople);
provide("selectedCC", selectedCC);
provide("selectedCCI", selectedCCI);
provide("quill", quill);
provide("stepContainer", stepContainer);
provide("AIContainer", AIContainer);
provide("counterDisplay", counterDisplay);
provide("isAIWriting", isAIWriting);
provide("displayMessage", displayMessage);
provide("uploadedFiles", uploadedFiles);
provide("inputSubject", inputSubject);
provide("contacts", contacts);

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

// const query = ref("");
// const getFilteredPeople = (query, contacts) => {
//     return computed(() => {
//         if (query.value === "") {
//             return contacts;
//         } else {
//             return contacts.filter((person) => {
//                 if (!person.username) {
//                     if (person.email) {
//                         person.username = person.email
//                             .split("@")[0]
//                             .split(/\.|-/)
//                             .map((p) => p.charAt(0).toUpperCase() + p.slice(1))
//                             .join(" ");
//                     } else {
//                         person.username = "";
//                     }
//                 }
//                 const usernameLower = person.username ? person.username.toLowerCase() : "";
//                 const emailLower = person.email ? person.email.toLowerCase() : "";
//                 return (
//                     usernameLower.includes(query.value.toLowerCase()) || emailLower.includes(query.value.toLowerCase())
//                 );
//             });
//         }
//     });
// };

// const filteredPeople = getFilteredPeople(query, contacts);
// const emit = defineEmits(["update:selectedPerson"]);
// const selectedPerson = ref("");

// watch(selectedPerson, (newValue) => {
//     // console.log(selectedPerson.value);
//     hasValueEverBeenEntered.value = true; // to make the icon disappear
//     /*if (selectedPerson.value && selectedPerson.value.username) {
//         //handleInputUpdate(selectedPerson.value.username);
//     }  */
//     emit("update:selectedPerson", newValue);
// });

// const isFirstTimeDestinary = ref(true); // to detect first letter object input
// const isFirstTimeEmail = ref(true); // to detect first letter email content input
// const hasValueEverBeenEntered = ref(false);

// const objectInput = ref(null);
// const mailInput = ref(null);
// //const new_idea_icon = ref(require('@/assets/new_idea.png'));
// const prompt_error_icon = ref(require("@/assets/prompt_error.png"));
// const happy_icon = ref(require("@/assets/happy.png"));
// const neutral_icon = ref(require("@/assets/neutral.png"));

// // To keep the navbar always at the bottom when new content is added

// // AI instruction textarea input

// // AI instruction button parameters

// // AI instruction to do revision on the mail
// const subject = ref("");
// const mail = ref("");
// const MailCreatedByAI = ref(false); // to check if the AI create the Mail or not

// // Loading animation

// /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// // function linked to ENTER key listeners

// function displayMessage_old(message, ai_icon) {
//     // Function to display a message from the AI Assistant

//     const messageHTML = `
//       <div class="flex pb-12">
//         <div class="mr-4 flex">
//           <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
//             <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
//               ${ai_icon}
//             </svg>
//           </span>
//         </div>
//         <div>
//           <p ref="animatedText${counter_display}"></p>
//         </div>
//       </div>
//     `;
//     AIContainer.value.innerHTML += messageHTML;
//     const animatedParagraph = document.querySelector(`p[ref="animatedText${counter_display}"]`);
//     counter_display += 1;
//     animateText(message, animatedParagraph);
//     scrollToBottom();
// }

// onMounted(() => {
//     document.addEventListener("keydown", handleKeyDown);
//     localStorage.removeItem("uploadedFiles");

//     //fetchEmailSenders();
//     loadFileMetadataFromLocalStorage(); // For uploaded file

//     window.addEventListener("resize", scrollToBottom); // To keep the scroll in the scrollbar at the bottom even when viewport change

//

//     const message = t("constants.sendEmailConstants.emailRecipientRequest");
//     const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
//     //const ai_icon = happy_icon;
//     displayMessage(message, ai_icon);
//     objectInput.value = document.getElementById("objectInput");

//     quill.value.on("text-change", function () {
//         mailInput.value = quill.value.root.innerHTML;
//         // console.log("MAIL", MailCreatedByAI.value);
//         // console.log("First", isFirstTimeEmail.value);
//         if (isFirstTimeEmail.value && !MailCreatedByAI.value) {
//             const quillContent = quill.value.root.innerHTML;
//             if (quillContent.trim() !== "<p><br></p>") {
//                 mail.value = quillContent;
//                 handleInputUpdateMailContent(quillContent);
//                 isFirstTimeEmail.value = false;
//             }
//         }
//         MailCreatedByAI.value = false;
//     });

//     const form = objectInput.value.closest("form");
//     if (form) {
//         form.addEventListener("submit", function (e) {
//             e.preventDefault();
//         });
//     }
// });

// watch(
//     uploadedFiles,
//     () => {
//         saveFileMetadataToLocalStorage();
//     },
//     { deep: true }
// );

// function handleInputUpdateObject() {
//     /* OLD OPTIONAL =>
//     if ((selectedPeople.value.length > 0 || selectedCC.value.length > 0 || selectedCCI.value.length > 0)) {
//       if (isFirstTimeObject.value && stepContainer == 0) {
//         askContent();
//         stepContainer = 1;
//         isFirstTimeObject.value = false;
//       }
//     } */
// }

// function handleInputUpdateMailContent(newMessage) {
//     if (newMessage !== "") {
//         if (selectedPeople.value.length > 0 || selectedCC.value.length > 0 || selectedCCI.value.length > 0) {
//             askContentAdvice();
//             stepContainer = 2;

//             scrollToBottom(); // To scroll to the bottom
//         }
//     }
// }

// function askContentAdvice() {
//     // TODO: check if subject has been entered => if no => answer please enter it
//     // Your previous code to display the message when the component is mounted
//     const message = t("constants.sendEmailConstants.emailCompositionAssistance"); // Older : const message = "Pouvez-vous fournir un brouillon de l'email que vous souhaitez rédiger ?";

//     const ai_icon = happy_icon;
//     const messageHTML = `
//       <div class="pb-12">
//         <div class="flex">
//             <div class="mr-4">
//                 <!--
//                 <span class="inline-flex h-14 w-14 items-center justify-center rounded-full overflow-hidden">
//                     <img src="${ai_icon._value}" alt="ai_icon" class="max-w-full max-h-full rounded-full">
//                 </span>-->
//                 <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
//                   <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
//                     <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
//                   </svg>
//                 </span>
//             </div>
//             <div>
//                 <div class="flex flex-col">
//                   <p ref="animatedText${counter_display}"></p>
//                   <div class="flex mt-4">
//                     <div class="mr-4">
//                       <button type="button" id="spellCheckButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
//                         ${t("newPage.correctSpelling")}
//                       </button>
//                     </div>
//                     <div>
//                       <button type="button" id="CopyWritingCheckButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
//                         ${t("newPage.checkCopywriting")}
//                       </button>
//                     </div>
//                   </div>
//                   <div class="flex mt-4">
//                     <div class="mr-4">
//                       <button type="button" id="WriteBetterButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
//                         ${t("newPage.improveWriting")}
//                       </button>
//                     </div>
//                   </div>
//                 </div>
//             </div>
//         </div>
//       </div>
//     `;
//     AIContainer.value.innerHTML += messageHTML;

//     // To check the ortgraph of the subject and the mail
//     setTimeout(() => {
//         const spellCheckButton = document.getElementById("spellCheckButton");
//         if (spellCheckButton) {
//             spellCheckButton.addEventListener("click", checkSpelling);
//         }
//     }, 0);

//     setTimeout(() => {
//         const CopyWritingCheckButton = document.getElementById("CopyWritingCheckButton");
//         if (CopyWritingCheckButton) {
//             CopyWritingCheckButton.addEventListener("click", checkCopyWriting);
//         }
//     }, 0);

//     setTimeout(() => {
//         const WriteBetterButton = document.getElementById("WriteBetterButton");
//         if (WriteBetterButton) {
//             WriteBetterButton.addEventListener("click", WriteBetter);
//         }
//     }, 0);

//     const animatedParagraph = document.querySelector(`p[ref="animatedText${counter_display}"]`);
//     counter_display += 1;
//     animateText(message, animatedParagraph);
// }

// async function checkSpelling() {
//     try {
//         loading();
//         scrollToBottom();

//         const requestOptions = {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({
//                 email_subject: inputValue.value,
//                 email_body: mailInput.value,
//             }),
//         };

//         const result = await fetchWithToken(`${API_BASE_URL}api/correct_email_language/`, requestOptions);

//         hideLoading();

//         console.log(result);
//         if (result.corrected_subject && result.corrected_body) {
//             // TO FINISH => animation
//             const formattedMail = result.corrected_body.replace(/\n/g, "<br>");
//             const messageHTML = `
//               <div class="flex pb-12">
//                   <div class="mr-4 flex">
//                       <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
//                         <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
//                           <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
//                         </svg>
//                       </span>
//                   </div>
//                   <div>
//                       <p><strong>${t("newPage.subject")}</strong> ${result.corrected_subject}</p>
//                       <p><strong>${t("newPage.emailContent")}</strong> ${formattedMail}</p>
//                   </div>
//               </div>
//           `;
//             AIContainer.value.innerHTML += messageHTML;
//             inputValue.value = result.corrected_subject;
//             const quillEditorContainer = quill.value.root;
//             quillEditorContainer.innerHTML = result.corrected_body;

//             // TO FINISH => create button with new options to reformat quickly the email written (more short, more formal, more strict)
//             const message = t("constants.sendEmailConstants.spellingCorrectionRequest");
//             const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
//             //const ai_icon = happy_icon;
//             displayMessage(message, ai_icon);
//         } else {
//             hideLoading();
//             const message = t("constants.sendEmailConstants.processingErrorApology");
//             const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
//             //const ai_icon = prompt_error_icon;
//             displayMessage(message, ai_icon);
//             console.log("Subject or Email is missing in the response");
//         }
//     } catch (error) {
//         console.error("Error:", error);
//         hideLoading();
//         const message = t("constants.sendEmailConstants.processingErrorApology");
//         const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
//         //const ai_icon = prompt_error_icon;
//         displayMessage(message, ai_icon);
//     }
// }

// async function checkCopyWriting() {
//     try {
//         loading();
//         scrollToBottom();

//         const requestOptions = {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({
//                 email_subject: inputValue.value,
//                 email_body: mailInput.value,
//             }),
//         };

//         const result = await fetchWithToken(`${API_BASE_URL}api/check_email_copywriting/`, requestOptions);

//         hideLoading();

//         console.log(result);
//         if (result.feedback_copywriting) {
//             // TO FINISH => animation
//             const formattedCopWritingOutput = result.feedback_copywriting.replace(/\n/g, "<br>");

//             const messageHTML = `
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
//             AIContainer.value.innerHTML += messageHTML;

//             // TO FINISH => create button with new options to reformat quickly the email written (more short, more formal, more strict)
//             const message = t("constants.sendEmailConstants.copywritingCheckRequest");
//             const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
//             //const ai_icon = happy_icon;
//             displayMessage(message, ai_icon);
//         } else {
//             hideLoading();
//             const message = t("constants.sendEmailConstants.processingErrorApology");
//             const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
//             //const ai_icon = prompt_error_icon;
//             displayMessage(message, ai_icon);
//             console.log("Subject or Email is missing in the response");
//         }
//     } catch (error) {
//         console.error("Error:", error);
//         hideLoading();
//         const message = t("constants.sendEmailConstants.processingErrorApology");
//         const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
//         //const ai_icon = prompt_error_icon;
//         displayMessage(message, ai_icon);
//     }
// }

// async function WriteBetter() {
//     try {
//         loading();
//         scrollToBottom();
//         const requestOptions = {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({
//                 userInput: textareaValueSave.value,
//                 length: lengthValue.value,
//                 formality: formalityValue.value,
//                 subject: inputValue.value,
//                 body: mail.value,
//                 history: history.value,
//             }),
//         };

//         const result = await fetchWithToken(`${API_BASE_URL}api/improve_draft/`, requestOptions);

//         hideLoading();
//         console.log(result);
//         subject.value = result.subject;
//         mail.value = result.email_body;
//         history.value = result.history;
//         if (result.subject && result.email_body) {
//             // TO FINISH => animation
//             const messageHTML = `
//             <div class="flex pb-12">
//                 <div class="mr-4 flex">
//                     <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
//                       <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
//                         <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
//                       </svg>
//                     </span>
//                 </div>
//                 <div>
//                     <p><strong>${t("newPage.subject")}</strong> ${result.subject}</p>
//                     <p><strong>${t("newPage.emailContent")}</strong> ${result.email_body}</p>
//                 </div>
//             </div>
//         `;
//             AIContainer.value.innerHTML += messageHTML;
//             inputValue.value = result.subject;
//             const quillEditorContainer = quill.value.root;
//             quillEditorContainer.innerHTML = result.email_body;

//             // TO FINISH => create button with new options to reformat quickly the email written (more short, more formal, more strict)
//             const message = t("constants.sendEmailConstants.betterEmailFeedbackRequest");
//             const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
//             //const ai_icon = happy_icon;
//             displayMessage(message, ai_icon);
//         } else {
//             hideLoading();
//             const message = t("constants.sendEmailConstants.processingErrorTryAgain");
//             const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
//             //const ai_icon = prompt_error_icon;
//             displayMessage(message, ai_icon);
//             console.log("Subject or Email is missing in the response");
//         }
//     } catch (error) {
//         console.error("Error:", error);
//         hideLoading();
//         // Handling error => TO PUT IN A FUNCTION
//         const message = t("constants.sendEmailConstants.processingErrorTryAgain");
//         const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
//         //const ai_icon = prompt_error_icon;
//         displayMessage(message, ai_icon);
//         console.error("There was a problem with the fetch operation: ", error);
//     }
// }

// function handleKeyDown(event) {
//     if (event.key == "Tab") {
//         event.preventDefault();

//         if (document.getElementById("editor").contains(document.activeElement)) {
//             return;
//         } else if (
//             selectedCCI.value.length == 0 &&
//             selectedCC.value.length == 0 &&
//             selectedPeople.value.length == 0 &&
//             document.activeElement.id != "recipients"
//         ) {
//             activeType.value = null;
//             document.getElementById("recipients").focus();
//         } else if (inputValue.value == "" && isFocused.value == false) {
//             document.getElementById("objectInput").focus();
//         } else if (quill.value.root.innerHTML == "<p><br></p>") {
//             quill.value.focus();
//         } else {
//             // Logic to rotate
//             if (document.activeElement.id === "recipients") {
//                 document.getElementById("objectInput").focus();
//             } else if (document.activeElement.id === "dynamicTextarea") {
//                 document.getElementById("recipients").focus();
//             } else {
//                 document.getElementById("dynamicTextarea").focus();
//             }
//         }
//     } else if (event.ctrlKey) {
//         switch (event.key) {
//             case "b":
//                 quill.value.focus();
//                 event.preventDefault();
//                 break;
//             case "d":
//                 document.getElementById("recipients").focus();
//                 event.preventDefault();
//                 break;
//             case "k":
//                 document.getElementById("dynamicTextarea").focus();
//                 event.preventDefault();
//                 break;
//             case "o":
//                 document.getElementById("objectInput").focus();
//                 event.preventDefault();
//                 break;
//             case "Enter":
//                 sendEmail();
//                 break;
//         }
//     }
// }
</script>

<!-- <script>
import Navbar from "../components/AppNavbar7.vue";
import Navbar2 from "../components/AppNavbar8.vue";
import {
    UserGroupIcon,
    Bars2Icon,
    //Bars3BottomLeftIcon,
    //ChatBubbleOvalLeftEllipsisIcon,
    ChevronDownIcon,
} from "@heroicons/vue/24/outline";

import { PaperAirplaneIcon } from "@heroicons/vue/24/solid";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";

export default {
    components: {
        Navbar,
        Navbar2,
        UserGroupIcon,
        Bars2Icon,
        ChevronDownIcon,
        PaperAirplaneIcon,
        // ChatBubbleOvalLeftEllipsisIcon,
        // Bars3BottomLeftIcon
    },
    methods: {
        
    },
};
</script> -->
