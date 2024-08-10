<template>
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
</template>

<script setup lang="ts">
import { ref } from 'vue';

const maxHeight = ref(250);
const textareaValue = ref("");

const adjustHeight = (event: Event): void => {
    const textarea = event.target as HTMLTextAreaElement;

    textarea.style.height = "auto";

    if (textarea.scrollHeight > maxHeight.value) {
        textarea.style.height = `${maxHeight.value}px`;
        textarea.style.overflowY = "auto";
    } else {
        textarea.style.height = `${textarea.scrollHeight}px`;
        textarea.style.overflowY = "hidden";
    }
};

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
    let imageURL = data.profile_image_url || userDefaultImg;
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
          <p class="font-serif">${userInput}</p>
        </div>
      </div>
    `;

    AIContainer.value.innerHTML += messageHTML;
    textareaValueSave.value = textareaValue.value;
    textareaValue.value = "";
    scrollToBottom();

    setTimeout(async () => {
        if (stepcontainer == 0) {
            if (textareaValueSave.value == "") {
                const message = t("constants.sendEmailConstants.noRecipientsEntered");
                const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />`;
                displayMessage(message, ai_icon);
            } else {
                try {
                    isLoading.value = true;
                    loading();
                    scrollToBottom();
                    const result = await findUser(textareaValueSave.value);

                    hideLoading();

                    let noUsersAdded = true;
                    let WaitforUserChoice = false;
                    if (result.error != "Invalid input or query not about email recipients") {
                        // To update to handle the main error

                        const main_recipients = userSearchResult.value.main_recipients;
                        const cc_recipients = userSearchResult.value.cc_recipients;
                        const bcc_recipients = userSearchResult.value.bcc_recipients;
                        console.log("debug", main_recipients, cc_recipients, bcc_recipients);

                        for (let i = 0; i < main_recipients.length; i++) {
                            const user = main_recipients[i];
                            const emails = user.email;

                            if (emails.length == 1) {
                                const person = { username: user.username, email: emails[0] };
                                selectedPeople.value.push(person);
                                main_recipients.splice(i, 1);
                                noUsersAdded = false;
                                i--;
                            }
                        }

                        for (let i = 0; i < cc_recipients.length; i++) {
                            const user = cc_recipients[i];
                            const emails = user.email;

                            if (emails.length == 1) {
                                const person = { username: user.username, email: emails[0] };
                                selectedCC.value.push(person);
                                delete cc_recipients[i];
                                cc_recipients.splice(i, 1);
                                noUsersAdded = false;
                                i--;
                            }
                        }

                        for (let i = 0; i < bcc_recipients.length; i++) {
                            const user = bcc_recipients[i];
                            const emails = user.email;

                            if (emails.length == 1) {
                                const person = { username: user.username, email: emails[0] };
                                selectedCCI.value.push(person);
                                bcc_recipients.splice(i, 1);
                                noUsersAdded = false;
                                i--;
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
                            `;
                            AIContainer.value.innerHTML += messageHTML;

                            if (main_recipients.length > 0) {
                                WaitforUserChoice = true;
                                const emailList = [];

                                for (const user of main_recipients) {
                                    for (const email of user.email) {
                                        if (user.email !== "") {
                                            // Creating an object for each email and pushing it to the emailList array
                                            const emailMapping = {};
                                            emailMapping[user.username] = email;
                                            emailList.push(emailMapping);
                                            noUsersAdded = false;
                                        }
                                    }
                                }
                                askChoiceRecipier(emailList, "main");
                            }
                            if (cc_recipients.length > 0) {
                                WaitforUserChoice = true;
                                const emailList = [];

                                for (const user of cc_recipients) {
                                    for (const email of user.email) {
                                        if (user.email !== "") {
                                            // Creating an object for each email and pushing it to the emailList array
                                            const emailMapping = {};
                                            emailMapping[user.username] = email;
                                            emailList.push(emailMapping);
                                            noUsersAdded = false;
                                        }
                                    }
                                }
                                askChoiceRecipier(emailList, "cc");
                            }
                            if (bcc_recipients.length > 0) {
                                WaitforUserChoice = true;
                                const emailList = [];

                                for (const user of bcc_recipients) {
                                    for (const email of user.email) {
                                        if (user.email !== "") {
                                            // Creating an object for each email and pushing it to the emailList array
                                            const emailMapping = {};
                                            emailMapping[user.username] = email;
                                            emailList.push(emailMapping);
                                            noUsersAdded = false;
                                        }
                                    }
                                }
                                askChoiceRecipier(emailList, "bcc");
                            }
                            scrollToBottom();
                        }

                        if (noUsersAdded) {
                            console.log("DEBUG");
                            const message = t(
                                "constants.sendEmailConstants.noRecipientsFoundPleaseTryAgainOrEnterManually"
                            );
                            const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
                            displayMessage(message, ai_icon);
                        } else if (!WaitforUserChoice) {
                            stepcontainer = 1;
                        }
                    } else {
                        const message = t(
                            "constants.sendEmailConstants.noRecipientsFoundPleaseTryAgainOrEnterManually"
                        );
                        const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
                        displayMessage(message, ai_icon);
                    }
                } catch (error) {
                    const message = t("constants.sendEmailConstants.processingErrorApology");
                    const ai_icon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
                    displayMessage(message, ai_icon);
                    console.error("Error finding user", error);
                }
            }
        }
    }, 0);
}
</script>
