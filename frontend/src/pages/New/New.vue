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
import { ref, onMounted, nextTick, provide, Ref, onUnmounted } from "vue";
import Quill from "quill";
import AiEmail from "./components/AiEmail.vue";
import ManualEmail from "./components/ManualEmail.vue";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { getData, postData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import { Recipient, EmailLinked, UploadedFile } from "@/global/types";
import NavBarSmall from "@/global/components/NavBarSmall.vue";

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
const selectedCCI = ref<Recipient[]>([]);
const stepContainer = ref(0);
const contacts = ref<Recipient[]>([]);
const uploadedFiles = ref<UploadedFile[]>([]);

const scrollToBottom = async () => {
    await nextTick();
    const element = scrollableDiv.value;
    if (!element) return;
    element.scrollTop = element.scrollHeight;
};

provide("emailSelected", emailSelected);
provide("selectedPeople", selectedPeople);
provide("selectedCC", selectedCC);
provide("selectedCCI", selectedCCI);
provide("quill", quill);
provide("stepContainer", stepContainer);
provide("AIContainer", AIContainer);
provide("counterDisplay", counterDisplay);
provide("isWriting", isWriting);
provide("uploadedFiles", uploadedFiles);
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
    window.addEventListener("beforeunload", handleBeforeUnload);

    const message = i18n.global.t("constants.sendEmailConstants.emailRecipientRequest");
    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;

    displayMessage(message, aiIcon);
    fetchEmailLinked();
    fetchRecipients();
    fetchPrimaryEmail();

    await initializeQuill();
});

onUnmounted(() => {
    window.removeEventListener("beforeunload", handleBeforeUnload);
});

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

function handleInputUpdateMailContent(newMessage: string) {
    if (newMessage !== "") {
        if (selectedPeople.value.length > 0 || selectedCC.value.length > 0 || selectedCCI.value.length > 0) {
            askContentAdvice();
            stepContainer.value = 2;
            scrollToBottom();
        }
    }
}

const handleBeforeUnload = (event: BeforeUnloadEvent) => {
    if (
        uploadedFiles.value.length ||
        selectedPeople.value.length ||
        selectedCC.value.length ||
        selectedCCI.value.length ||
        subjectInput.value !== ""
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
            isWriting.value = false;
        }
    }, 30);
}

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

async function fetchPrimaryEmail() {
    if (!emailSelected.value) {
        const result = await getData("user/get_first_email/");

        if (!result.success) {
            displayPopup(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.primaryEmailFetchError"),
                result.error as string
            );
        } else {
            emailSelected.value = result.data.email;
            localStorage.setItem("email", result.data.email);
        }
    }
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

async function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Tab") {
        event.preventDefault();

        const editor = document.getElementById("editor");
        const recipients = document.getElementById("recipients");
        const dynamicTextarea = document.getElementById("dynamicTextarea");
        const subjectInput = document.getElementById("subjectInput") as HTMLInputElement | null;

        if (editor && editor.contains(document.activeElement)) {
            return;
        }

        if (
            selectedCCI.value.length === 0 &&
            selectedCC.value.length === 0 &&
            selectedPeople.value.length === 0 &&
            document.activeElement?.id !== "recipients"
        ) {
            recipients?.focus();
        } else if (subjectInput && subjectInput.value === "") {
            subjectInput.focus();
        } else {
            if (document.activeElement?.id === "recipients") {
                subjectInput?.focus();
            } else if (document.activeElement?.id === "dynamicTextarea") {
                recipients?.focus();
            } else {
                dynamicTextarea?.focus();
            }
        }
    } else if (event.ctrlKey) {
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

function displayErrorProcessingMessage() {
    const message = i18n.global.t("constants.sendEmailConstants.processingErrorApology");
    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
    displayMessage(message, aiIcon);
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

function askContentAdvice() {
    if (!AIContainer.value) return;

    const message = i18n.global.t("constants.sendEmailConstants.emailCompositionAssistance");
    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;

    const messageHTML = `
      <div class="pb-12">
        <div class="flex">
            <div class="mr-4">
                <!--
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full overflow-hidden">
                    <img src="${aiIcon}" alt="aiIcon" class="max-w-full max-h-full rounded-full">
                </span>-->
                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
                  </svg>
                </span>
            </div>
            <div>
                <div class="flex flex-col">
                  <p ref="animatedText${counterDisplay.value}"></p>
                  <div class="flex mt-4">
                    <div class="mr-4">
                      <button type="button" id="spellCheckButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                        ${i18n.global.t("newPage.correctSpelling")}
                      </button>
                    </div>
                    <div>
                      <button type="button" id="CopyWritingCheckButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                        ${i18n.global.t("newPage.checkCopywriting")}
                      </button>
                    </div>
                  </div>
                  <div class="flex mt-4">
                    <div class="mr-4">
                      <button type="button" id="writeBetterButton" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                        ${i18n.global.t("newPage.improveWriting")}
                      </button>
                    </div>
                  </div>
                </div>
            </div>
        </div>
      </div>
    `;
    AIContainer.value.innerHTML += messageHTML;

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
        const writeBetterButton = document.getElementById("writeBetterButton");
        if (writeBetterButton) {
            writeBetterButton.addEventListener("click", writeBetter);
        }
    }, 0);

    const animatedParagraph = document.querySelector(`p[ref="animatedText${counterDisplay.value}"]`);
    counterDisplay.value += 1;
    animateText(message, animatedParagraph);
}

async function checkSpelling() {
    if (!AIContainer.value || !quill.value) return;
    loading();

    const result = await postData("api/correct_email_language/", {
        subject: subjectInput.value,
        body: AiEmailBody.value,
    });

    hideLoading();
    if (!result.success) {
        displayErrorProcessingMessage();
        return;
    }

    const formattedBody = result.data.correctedBody.replace(/\n/g, "<br>");
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
                      <p><strong>${i18n.global.t("newPage.subject")}</strong> ${result.data.correctedSubject}</p>
                      <p><strong>${i18n.global.t("newPage.emailContent")}</strong> ${formattedBody}</p>
                  </div>
              </div>
          `;
    AIContainer.value.innerHTML += messageHTML;
    subjectInput.value = result.data.correctedSubject;
    const quillEditorContainer = quill.value.root;
    quillEditorContainer.innerHTML = result.data.correctedBody;

    const message = i18n.global.t("constants.sendEmailConstants.spellingCorrectionRequest");
    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;

    displayMessage(message, aiIcon);
}

async function checkCopyWriting() {
    if (!AIContainer.value) return;
    loading();

    const result = await postData("api/check_email_copywriting/", {
        email_subject: subjectInput.value,
        email_body: AiEmailBody.value,
    });

    hideLoading();

    if (!result.success) {
        displayErrorProcessingMessage();
        return;
    }

    const formattedCopWritingOutput = result.data.feedbackCopywriting.replace(/\n/g, "<br>");
    const messageHTML = `
              <div class="flex pb-12">
                  <div class="mr-4 flex">
                      <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                        </svg>
                      </span>
                  </div>
                  <div>
                      <p>${formattedCopWritingOutput}</p>
                  </div>
              </div>
          `;
    AIContainer.value.innerHTML += messageHTML;

    const message = i18n.global.t("constants.sendEmailConstants.copywritingCheckRequest");
    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
    displayMessage(message, aiIcon);
}

async function writeBetter() {
    if (!AIContainer.value || !quill.value) return;
    loading();

    const result = await postData("api/improve_draft/", {
        userInput: textareaValueSave.value,
        length: selectedLength.value,
        formality: selectedFormality.value,
        subject: subjectInput.value,
        body: AiEmailBody.value,
        history: history.value,
    });

    if (!result.success) {
        displayErrorProcessingMessage();
        return;
    }

    hideLoading();
    subject.value = result.data.subject;
    AiEmailBody.value = result.data.emailBody;
    history.value = result.data.history;

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
                    <p><strong>${i18n.global.t("newPage.subject")}</strong> ${result.data.subject}</p>
                    <p><strong>${i18n.global.t("newPage.emailContent")}</strong> ${result.data.emailBody}</p>
                </div>
            </div>
        `;
    AIContainer.value.innerHTML += messageHTML;
    subjectInput.value = result.data.subject;
    const quillEditorContainer = quill.value.root;
    quillEditorContainer.innerHTML = result.data.emailBody;

    const message = i18n.global.t("constants.sendEmailConstants.betterEmailFeedbackRequest");
    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
    displayMessage(message, aiIcon);
}
</script>
