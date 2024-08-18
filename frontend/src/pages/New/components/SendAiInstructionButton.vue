<template>
    <div v-if="stepContainer == 1" class="flex justify-end m-3 2xl:m-5">
        <div class="flex mt-4 space-x-4 items-center">
            <div>
                <select
                    id="lengthSelect"
                    class="h-10 px-8 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white focus:bg-gray-900 focus:text-white border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900"
                    v-model="selectedLength"
                >
                    <option v-for="option in emailLengthOptions" :key="option.key" :value="option.key">
                        {{ option.value }}
                    </option>
                </select>
            </div>
            <div>
                <select
                    id="formalitySelect"
                    class="h-10 px-8 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white focus:bg-gray-900 focus:text-white border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900"
                    v-model="selectedFormality"
                >
                    <option v-for="option in formalityOptions" :key="option.key" :value="option.key">
                        {{ option.value }}
                    </option>
                </select>
            </div>
            <div class="flex items-center">
                <button
                    @click="handleAIClick"
                    type="button"
                    class="2xl:w-[100px] w-[100px] rounded-md bg-gray-700 px-6 py-2.5 2xl:px-6 2xl:py-3 text-sm 2xl:text-base text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                >
                    {{ $t("constants.userActions.send") }}
                </button>
            </div>
        </div>
    </div>
    <div v-else class="flex justify-end m-3 2xl:m-5">
        <button
            @click="handleAIClick"
            type="button"
            class="2xl:w-[100px] w-[80px] rounded-md bg-gray-700 px-5.5 py-2.5 2xl:px-6.5 2xl:py-3 2xl:text-base text-sm text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
        >
            {{ $t("constants.userActions.send") }}
        </button>
    </div>
</template>

<script setup lang="ts">
import { i18n } from "@/global/preferences";
import { KeyValuePair } from "@/global/types";
import { inject, Ref, ref } from "vue";

const stepContainer = inject<Ref<number>>("stepContainer") || ref(0);
const selectedLength = ref("short");
const selectedFormality = ref("formal");

const emailLengthOptions: KeyValuePair[] = [
    { key: "very short", value: i18n.global.t("newPage.veryBrief") },
    { key: "short", value: i18n.global.t("newPage.brief") },
    { key: "long", value: i18n.global.t("newPage.long") },
];

const formalityOptions: KeyValuePair[] = [
    { key: "very informal", value: i18n.global.t("newPage.informal") },
    { key: "formal", value: i18n.global.t("newPage.formal") },
    { key: "very formal", value: i18n.global.t("newPage.veryFormal") },
];

async function handleAIClick() {
    // if (isAIWriting.value) {
    //     return;
    // }
    // isAIWriting.value = true;
    // let messageHTML = "";
    // let userInput = textareaValue.value;
    // messageHTML = `
    //   <div class="flex pb-12">
    //     <div class="mr-4 flex">
    //       <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
    //         <img src="${imageURL}" alt="Profile Image" class="h-14 w-14 rounded-full">
    //       </span>
    //     </div>
    //     <div>
    //       <p class="font-serif">${userInput}</p>
    //     </div>
    //   </div>
    // `;
    // if (!AIContainer.value) return;
    // AIContainer.value.innerHTML += messageHTML;
    // textareaValueSave.value = textareaValue.value;
    // textareaValue.value = "";
    // scrollToBottom();
    // setTimeout(async () => {
    //     if (stepContainer == 0) {
    //         if (textareaValueSave.value == "") {
    //             const message = i18n.global.t("constants.sendEmailConstants.noRecipientsEntered");
    //             const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`;
    //             displayMessage(message, aiIcon);
    //         } else {
    //             loading();
    //             scrollToBottom();
    //             const result = await postData("api/find_user_ai/", { query: textareaValueSave.value });
    //             if (!result.success) {
    //                 const message = i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain");
    //                 const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
    //                 displayMessage(message, aiIcon);
    //             }
    //             hideLoading();
    //             let noUsersAdded = true;
    //             let waitforUserChoice = false;
    //             const mainRecipients = result.data.mainRecipients;
    //             const ccRecipients = result.data.ccRecipients;
    //             const bccRecipients = result.data.bccRecipients;
    //             for (let i = 0; i < mainRecipients.length; i++) {
    //                 const user = mainRecipients[i];
    //                 const emails = user.email;
    //                 if (emails.length == 1) {
    //                     const person = { username: user.username, email: emails[0] };
    //                     selectedPeople.value.push(person);
    //                     mainRecipients.splice(i, 1);
    //                     noUsersAdded = false;
    //                     i--;
    //                 }
    //             }
    //             for (let i = 0; i < ccRecipients.length; i++) {
    //                 const user = ccRecipients[i];
    //                 const emails = user.email;
    //                 if (emails.length == 1) {
    //                     const person = { username: user.username, email: emails[0] };
    //                     selectedCC.value.push(person);
    //                     delete ccRecipients[i];
    //                     ccRecipients.splice(i, 1);
    //                     noUsersAdded = false;
    //                     i--;
    //                 }
    //             }
    //             for (let i = 0; i < bccRecipients.length; i++) {
    //                 const user = bccRecipients[i];
    //                 const emails = user.email;
    //                 if (emails.length == 1) {
    //                     const person = { username: user.username, email: emails[0] };
    //                     selectedCCI.value.push(person);
    //                     bccRecipients.splice(i, 1);
    //                     noUsersAdded = false;
    //                     i--;
    //                 }
    //             }
    //             if (!AIContainer.value) return;
    //             if (mainRecipients.length > 0 || ccRecipients.length > 0 || bccRecipients.length > 0) {
    //                 const messageHTML = `
    //                             <div class="flex pb-2">
    //                                 <div class="mr-4 flex">
    //                                     <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
    //                                         <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
    //                                         <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
    //                                         </svg>
    //                                     </span>
    //                                 </div>
    //                                 <div>
    //                                     <p>${i18n.global.t(
    //                                         "constants.sendEmailConstants.multipleEmailsFoundForSomeRecipients"
    //                                     )}</p>
    //                                 </div>
    //                             </div>
    //                         `;
    //                 AIContainer.value.innerHTML += messageHTML;
    //                 if (mainRecipients.length > 0) {
    //                     waitforUserChoice = true;
    //                     const emailList: EmailMapping[] = [];
    //                     for (const user of mainRecipients) {
    //                         for (const email of user.email) {
    //                             if (email !== "") {
    //                                 const emailMapping: EmailMapping = {};
    //                                 emailMapping[user.username] = email;
    //                                 emailList.push(emailMapping);
    //                                 noUsersAdded = false;
    //                             }
    //                         }
    //                     }
    //                     askChoiceRecipier(emailList, "main");
    //                 }
    //                 if (ccRecipients.length > 0) {
    //                     waitforUserChoice = true;
    //                     const emailList: EmailMapping[] = [];
    //                     for (const user of ccRecipients) {
    //                         for (const email of user.email) {
    //                             if (email !== "") {
    //                                 const emailMapping: EmailMapping = {};
    //                                 emailMapping[user.username] = email;
    //                                 emailList.push(emailMapping);
    //                                 noUsersAdded = false;
    //                             }
    //                         }
    //                     }
    //                     askChoiceRecipier(emailList, "cc");
    //                 }
    //                 if (bccRecipients.length > 0) {
    //                     waitforUserChoice = true;
    //                     const emailList: EmailMapping[] = [];
    //                     for (const user of bccRecipients) {
    //                         for (const email of user.email) {
    //                             if (email !== "") {
    //                                 const emailMapping: EmailMapping = {};
    //                                 emailMapping[user.username] = email;
    //                                 emailList.push(emailMapping);
    //                                 noUsersAdded = false;
    //                             }
    //                         }
    //                     }
    //                     askChoiceRecipier(emailList, "bcc");
    //                 }
    //                 nextStepRecipier();
    //                 scrollToBottom();
    //             }
    //             if (noUsersAdded) {
    //                 const message = i18n.global.t(
    //                     "constants.sendEmailConstants.noRecipientsFoundPleaseTryAgainOrEnterManually"
    //                 );
    //                 const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
    //                 displayMessage(message, aiIcon);
    //             } else if (!waitforUserChoice) {
    //                 stepContainer = 1;
    //                 askContent();
    //             }
    //         }
    //     } else if (stepContainer == 1) {
    //         if (!AIContainer.value || !quill?.value) return;
    //         if (textareaValueSave.value == "") {
    //             const message = i18n.global.t("constants.sendEmailConstants.noDraftsEnteredPleaseTryAgain");
    //             const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`;
    //             displayMessage(message, aiIcon);
    //         } else {
    //             loading();
    //             scrollToBottom();
    //             const result = await postData("api/new_email_ai/", {
    //                 inputData: textareaValueSave.value,
    //                 length: selectedLength.value,
    //                 formality: selectedFormality.value,
    //             });
    //             hideLoading();
    //             if (!result.success) {
    //                 const message = i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain");
    //                 const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
    //                 displayMessage(message, aiIcon);
    //             }
    //             subject.value = result.data.subject;
    //             mail.value = result.data.mail;
    //             stepContainer = 2;
    //             const formattedMail = result.data.mail.replace(/\n/g, "<br>");
    //             const messageHTML = `
    //                   <div class="flex pb-12">
    //                       <div class="mr-4 flex">
    //                           <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
    //                             <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
    //                               <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
    //                             </svg>
    //                           </span>
    //                       </div>
    //                       <div>
    //                           <p><strong>${i18n.global.t("newPage.subject")}</strong> ${result.data.subject}</p>
    //                           <p><strong>${i18n.global.t("newPage.emailContent")}</strong> ${formattedMail}</p>
    //                       </div>
    //                   </div>
    //               `;
    //             AIContainer.value.innerHTML += messageHTML;
    //             inputValue.value = result.data.subject;
    //             MailCreatedByAI.value = true;
    //             const quillEditorContainer = quill.value.root;
    //             quillEditorContainer.innerHTML = result.data.mail.replace(/<\/p>/g, "</p><p></p>");
    //             const message = i18n.global.t("constants.sendEmailConstants.emailFeedbackRequest");
    //             const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
    //             displayMessage(message, aiIcon);
    //         }
    //     } else if (stepContainer == 2) {
    //         if (textareaValueSave.value == "") {
    //             const message = i18n.global.t("constants.sendEmailConstants.noSuggestionsEnteredPleaseTryAgain");
    //             const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`;
    //             displayMessage(message, aiIcon);
    //         } else {
    //             try {
    //                 loading();
    //                 scrollToBottom();
    //                 const requestOptions = {
    //                     method: "POST",
    //                     headers: {
    //                         "Content-Type": "application/json",
    //                     },
    //                     body: JSON.stringify({
    //                         userInput: textareaValueSave.value,
    //                         length: lengthValue.value,
    //                         formality: formalityValue.value,
    //                         subject: inputValue.value,
    //                         body: mail.value,
    //                         history: history.value,
    //                     }),
    //                 };
    //                 const result = await fetchWithToken(`${API_BASE_URL}api/improve_draft/`, requestOptions);
    //                 hideLoading();
    //                 subject.value = result.subject;
    //                 mail.value = result.email_body;
    //                 history.value = result.history;
    //                 if (result.subject && result.email_body) {
    //                     hideLoading();
    //                     const formattedMail = result.email_body.replace(/\n/g, "<br>");
    //                     const messageHTML = `
    //                   <div class="flex pb-12">
    //                       <div class="mr-4 flex">
    //                           <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
    //                             <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
    //                               <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
    //                             </svg>
    //                           </span>
    //                       </div>
    //                       <div>
    //                           <p><strong>${t("newPage.subject")}</strong> ${result.subject}</p>
    //                           <p><strong>${t("newPage.emailContent")}</strong> ${formattedMail}</p>
    //                       </div>
    //                   </div>
    //               `;
    //                     AIContainer.value.innerHTML += messageHTML;
    //                     inputValue.value = result.subject;
    //                     const quillEditorContainer = quill.value.root;
    //                     quillEditorContainer.innerHTML = result.email_body;
    //                     quillEditorContainer.style.cssText = "p { margin-bottom: 20px; }";
    //                     const message = i18n.global.t("constants.sendEmailConstants.betterEmailFeedbackRequest");
    //                     const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
    //                     displayMessage_old(message, aiIcon);
    //                 } else {
    //                     hideLoading();
    //                     const message = i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain");
    //                     const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
    //                     displayMessage(message, aiIcon);
    //                 }
    //             } catch (error) {
    //                 hideLoading();
    //                 const message = i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain");
    //                 const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
    //                 displayMessage(message, aiIcon);
    //             }
    //         }
    //     }
    // }, 0);
}
</script>
