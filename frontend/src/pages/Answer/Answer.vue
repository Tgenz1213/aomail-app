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
import { INFORMATIVE } from "@/global/const";

const showNotification = ref(false);
const isWriting = ref(false);
const isLoading = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const subjectInput = ref("");
const textareaValueSave = ref("");
const subject = ref("");
const importance = ref(INFORMATIVE);
const emailSelected = ref("");
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
const emailContent = ref("");
const responseKeywords = ref([]);

const scrollToBottom = async () => {
    await nextTick();
    const element = scrollableDiv.value;
    if (!element) return;
    element.scrollTop = element.scrollHeight;
};

provide("importance", importance);
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
provide("textareaValueSave", textareaValueSave);
provide("selectedLength", selectedLength);
provide("selectedFormality", selectedFormality);
provide("displayPopup", displayPopup);
provide("displayMessage", displayMessage);
provide("scrollToBottom", scrollToBottom);
provide("loading", loading);
provide("hideLoading", hideLoading);

async function fetchSelectedEmailData() {
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
    const selectedEmail = emailsLinked.value.find((tupleEmail) => emailSelected.value === tupleEmail.email);

    if (selectedEmail) {
        emailsLinked.value = [selectedEmail];
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

onMounted(async () => {
    await initializeQuill();

    AIContainer.value = document.getElementById("AIContainer");
    document.addEventListener("keydown", handleKeyDown);
    localStorage.removeItem("uploadedFiles");
    window.addEventListener("resize", scrollToBottom);

    fetchRecipients();

    subject.value = JSON.parse(sessionStorage.getItem("subject") || "");
    selectedPeople.value = [{ email: JSON.parse(sessionStorage.getItem("senderEmail") || "[]") }];
    selectedCC.value = JSON.parse(sessionStorage.getItem("cc") || "[]");
    selectedBCC.value = JSON.parse(sessionStorage.getItem("bcc") || "[]");
    emailSelected.value = JSON.parse(sessionStorage.getItem("emailUser") || "");
    importance.value = JSON.parse(sessionStorage.getItem("importance") || "");
    const decodedData = JSON.parse(sessionStorage.getItem("decodedData") || "");
    const htmlContent = sessionStorage.getItem("htmlContent" || "");
    const shortSummary = JSON.parse(sessionStorage.getItem("shortSummary") || "");

    await fetchSelectedEmailData();

    const messageHTML = `
    <div class="flex pb-12">
      <div class="mr-4 flex flex-shrink-0">
        <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
          </svg>
        </span>
      </div>
      <div class="flex flex-col space-y-1">
        <p class="my-0">${subject.value}</p>
        <p class="my-0 font-bold text-md">${i18n.global.t("answerPage.chatSummarize")}</p>
        <p class="my-0 text-sm">${shortSummary}</p>
        <div class="mr-4 pt-2">
          <button type="button" class="text-md show-email-btn px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
            ${i18n.global.t("answerPage.seeMail")}
          </button>
        </div>
        <div class="email-content hidden mt-4 border-t pt-4">${htmlContent}</div>
      </div>
    </div>
  `;

    document.addEventListener("click", (event: any) => {
        if (event.target.classList.contains("show-email-btn")) {
            event.target.style.display = "none";
            event.target.closest(".flex").querySelector(".email-content").style.display = "block";
        }
    });

    if (AIContainer.value) AIContainer.value.innerHTML += messageHTML;
    emailContent.value = decodedData;
    subjectInput.value = "Re : " + subject.value;

    fetchResponseKeywords();
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
    if (!AIContainer.value || isWriting.value) {
        return;
    }

    isWriting.value = true;

    const message = i18n.global.t("answerPage.chatKeyWordIntroduction");

    let buttonsHTML = "";
    responseKeywords.value.forEach((keyword, index) => {
        if (index % 2 === 0) {
            buttonsHTML += index > 0 ? "</div>" : "";
            buttonsHTML += index > 0 ? '<div class="flex mt-4">' : '<div class="flex">';
        }

        buttonsHTML += `
            <div class="mr-4">
                <button type="button" id="responseKeywordButton${index}" data-value="${keyword}" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-gray-900 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                    ${keyword}
                </button>
            </div>
        `;

        if (index === responseKeywords.value.length - 1) {
            buttonsHTML += "</div>";
        }
    });

    const messageHTML = `
        <div class="flex pb-12">
          <div class="mr-4 flex-shrink-0">
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900">
              <span class="text-lg font-medium leading-none text-white">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
                </svg>
              </span>
            </span>
          </div>
          <div class="flex flex-col">
            <p ref="animatedText${counterDisplay.value}" class="mt-0"></p>
            <div class="flex flex-col mt-2">
              ${buttonsHTML}
            </div>
          </div>
        </div>
    `;

    AIContainer.value.innerHTML += messageHTML;

    responseKeywords.value.forEach((_keyword, index) => {
        setTimeout(() => {
            const keywordButton = document.getElementById(`responseKeywordButton${index}`);
            if (keywordButton) {
                keywordButton.addEventListener("click", () => {
                    handleButtonClick(keywordButton.getAttribute("data-value"));
                });
            }
        }, 0);
    });

    const animatedParagraph = document.querySelector(`p[ref="animatedText${counterDisplay.value}"]`);
    counterDisplay.value += 1;
    animateText(message, animatedParagraph);
}

async function handleButtonClick(keyword: string | null) {
    if (isWriting.value || !AIContainer.value || !quill?.value) {
        return;
    }
    isWriting.value = true;

    loading();
    scrollToBottom();

    const result = await postData("api/generate_email_answer/", {
        subject: subjectInput.value,
        body: emailContent.value,
        keyword: keyword,
    });

    hideLoading();

    if (!result.success) {
        const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />`;
        displayMessage?.(i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain"), aiIcon);
        return;
    }

    const quillEditorContainer = quill.value.root;
    quillEditorContainer.innerHTML = result.data.emailAnswer;
    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
    await displayMessage(i18n.global.t("constants.sendEmailConstants.doesThisResponseSuitYou"), aiIcon);
}

async function fetchResponseKeywords() {
    loading();
    const result = await postData("api/generate_email_response_keywords/", {
        subject: subject.value,
        body: emailContent.value,
    });
    hideLoading();

    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.primaryEmailFetchError"),
            result.error as string
        );
        return;
    }
    responseKeywords.value = result.data.responseKeywords;
    askContentAdvice();
}

async function animateText(text: string, target: Element | null) {
    return new Promise<void>((resolve) => {
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
                resolve();
            }
        }, 30);
    });
}

async function displayMessage(message: string, aiIcon: string) {
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
    await animateText(message, animatedParagraph);
    scrollToBottom();
}
</script>
