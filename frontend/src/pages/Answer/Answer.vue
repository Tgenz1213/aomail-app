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
            <div :class="['bg-white ring-1 shadow-sm ring-black ring-opacity-5', isNavMinimized ? 'w-20' : 'w-60']">
                <Navbar @update:isMinimized="(value) => (isNavMinimized = value)" />
            </div>
            <div
                :style="{ width: manualEmailWidth + '%' }"
                class="bg-white lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full"
            >
                <ManualEmail />
            </div>

            <div class="drag-wrapper">
                <div class="separator"></div>
                <div class="drag-overlay" @mousedown="initDrag"></div>
            </div>

            <div
                :style="{ width: aiEmailWidth + '%' }"
                class="flex flex-col bg-zinc-50 lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full"
            >
                <AiEmail />
            </div>
        </div>
    </div>
    <SignatureModal
        :visible="showSignatureModal"
        :selectedEmail="emailSelected"
        @close="handleSignatureModalClose"
        @created="handleSignatureCreated"
    />
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, provide, onBeforeUnmount } from "vue";
import Quill from "quill";
import AiEmail from "./components/AiEmail.vue";
import ManualEmail from "@/global/components/ManualEmail/ManualEmail.vue";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { getData, postData, putData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import { Recipient, Agent, EmailLinked, UploadedFile } from "@/global/types";
import Navbar from "@/global/components/Navbar.vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { API_BASE_URL, INFORMATIVE } from "@/global/const";
import userImage from "@/assets/user.png";
import SignatureModal from "@/global/components/SignatureModal.vue";

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
const imageURL = ref<string>(userImage);
let quill: Quill | null = null;
const showSignatureModal = ref(false);
const signatures = ref<any[]>([]);
const isLoadingAgentSelection = ref(false);
const agents = ref<Agent[]>([]);
const selectedAgent = ref<Agent>({
    id: "",
    agent_name: i18n.global.t("agent.defaultAgent"),
    picture: "/assets/default-agent.png",
    ai_template: "",
    length: "",
    formality: "",
    icon_name: "default-agent.png",
});
const isNavMinimized = ref(localStorage.getItem("navbarMinimized") === "true");
const manualEmailWidth = ref(55);
const aiEmailWidth = ref(45);
const isDragging = ref(false);
const startX = ref(0);
const startManualWidth = ref(0);
const startAiWidth = ref(0);
const initialContainerWidth = ref(0);

const scrollToBottom = async () => {
    await nextTick();
    const element = scrollableDiv.value;
    if (!element) return;
    element.scrollTop = element.scrollHeight;
};

function getQuill() {
    return quill;
}

const displayMessage = async (message: string, aiIcon: string) => {
    if (!AIContainer.value) {
        console.warn("AIContainer not initialized");
        await nextTick();
        if (!AIContainer.value) return;
    }

    const messageHTML = `
      <div class="flex pb-6">
        <div class="mr-3 flex-shrink-0">
            <span class="inline-flex h-12 w-12 items-center justify-center rounded-full">
                <img src="${API_BASE_URL}agent_icon/${selectedAgent.value.icon_name}" alt="Agent Icon" class="h-12 w-12 rounded-full object-cover">
            </span>
        </div>
        <div class="flex flex-col bg-white rounded-lg p-4 max-w-md border border-gray-200">
          <p ref="animatedText${counterDisplay.value}" class="text-gray-800"></p>
        </div>
      </div>
    `;

    AIContainer.value.innerHTML += messageHTML;
    const animatedParagraph = document.querySelector(`p[ref="animatedText${counterDisplay.value}"]`);
    counterDisplay.value += 1;

    if (animatedParagraph) {
        await animateText(message, animatedParagraph);
        await scrollToBottom();
    } else {
        displayPopup(
            "error",
            i18n.global.t("answerPage.error.title"),
            i18n.global.t("answerPage.error.paragraphNotFound")
        );
    }
};

provide("imageURL", imageURL);
provide("importance", importance);
provide("emailSelected", emailSelected);
provide("selectedPeople", selectedPeople);
provide("selectedCC", selectedCC);
provide("selectedBCC", selectedBCC);
provide("getQuill", getQuill);
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
provide("agents", agents);
provide("selectedAgent", selectedAgent);
provide("setAgentLastUsed", setAgentLastUsed);
provide("signatures", signatures);
provide("emailContent", emailContent);
provide("manualEmailWidth", manualEmailWidth);
provide("aiEmailWidth", aiEmailWidth);
provide("fetchResponseKeywords", fetchResponseKeywords);

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

const capitalize = (str: string) => {
    if (!str) return "";
    return str.charAt(0).toUpperCase() + str.slice(1);
};

const displayAgentSelection = async () => {
    try {
        const response = await getData("user/agents/all_info/");
        agents.value = response.data.map((agent: Agent) => ({
            ...agent,
            picture: agent.picture || "/assets/default-agent.png",
        }));

        const agentButtons = agents.value
            .map(
                (agent) => `
      <button 
        class="flex items-start p-4 border rounded-lg hover:bg-gray-100 transition-colors duration-200 mb-4 w-full" 
        data-agent-id="${agent.id}"
      >
        <img 
          src="${API_BASE_URL}agent_icon/${agent.icon_name}" 
          alt="Agent Icon" 
          class="h-14 w-14 rounded-full mr-4 object-cover flex-shrink-0"
        />
        <div class="flex-1">
          <h3 class="text-xl font-semibold text-left">${agent.agent_name}</h3>
          <p class="text-gray-600 mt-1 text-left">${agent.ai_template}</p>
          <div class="flex text-sm text-gray-500 mt-2">
            <p class="mr-4"><span class="font-medium">Length:</span> ${capitalize(agent.length)}</p>
            <p><span class="font-medium">Formality:</span> ${capitalize(agent.formality)}</p>
          </div>
        </div>
      </button>
    `
            )
            .join("");

        const messageHTML = `
        <div class="mt-0">
          ${agentButtons}
        </div>
    `;

        if (AIContainer.value) {
            AIContainer.value.innerHTML += messageHTML;

            const buttons = AIContainer.value.querySelectorAll("button[data-agent-id]");
            buttons.forEach((button) => {
                button.addEventListener("click", () => {
                    const agentId = button.getAttribute("data-agent-id");
                    const selectedAgentData = agents.value.find((agent) => agent.id.toString() === agentId);
                    if (selectedAgentData) {
                        selectedAgent.value = selectedAgentData;
                        setAgentLastUsed(selectedAgent.value);
                        if (AIContainer.value) {
                            const messages = AIContainer.value.children;
                            if (messages.length > 0) {
                                messages[messages.length - 1].remove();
                            }
                            fetchResponseKeywords();
                        }
                    }
                });
            });
        }
    } catch (error) {
        displayPopup(
            "error",
            i18n.global.t("answerPage.error.title"),
            i18n.global.t("answerPage.error.displayingAgentSelection")
        );
    }
};

const checkLastUsedAgent = async () => {
    try {
        if (!agents.value.length) {
            displayPopup(
                "error",
                i18n.global.t("answerPage.error.title"),
                i18n.global.t("answerPage.error.noAgentsAvailable")
            );
            return;
        }

        const response = await getData("user/agents/check_last_used/");

        if (response.success && response.data.exists) {
            const selectedAgentData = agents.value.find((agent) => agent.id === response.data.agent_id);
            if (selectedAgentData) {
                selectedAgent.value = selectedAgentData;
            }
        } else {
            await displayMessage(i18n.global.t("agent.chooseAiAssistant"), selectedAgent.value.picture);
            await displayAgentSelection();
        }
    } catch (error) {
        displayPopup(
            "error",
            i18n.global.t("answerPage.error.title"),
            i18n.global.t("answerPage.error.checkingLastUsedAgent")
        );
    }
};

async function fetchAgents() {
    try {
        const response = await getData("user/agents/all_info/");
        if (response.success) {
            agents.value = response.data.map((agent: Agent) => ({
                ...agent,
                picture: agent.picture || "/assets/default-agent.png",
            }));
        } else {
            throw new Error(response.error);
        }
    } catch (error) {
        displayPopup(
            "error",
            i18n.global.t("answerPage.error.title"),
            i18n.global.t("answerPage.error.fetchingAgents")
        );
        throw error;
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

async function displayEmailContent() {
    if (!AIContainer.value) return;

    const messageHTML = `
        <div class="flex pb-12">
          <div class="mr-4 flex flex-shrink-0">
            <span class="inline-flex h-12 w-12 items-center justify-center rounded-full">
                <img src="${API_BASE_URL}agent_icon/${
        selectedAgent.value.icon_name
    }" alt="Agent Icon" class="h-12 w-12 rounded-full object-cover">
            </span>
          </div>
          <div class="flex flex-col space-y-1 bg-white rounded-lg p-4 border border-gray-200">
            <p class="my-0 font-bold text-md">${i18n.global.t("answerPage.chatSummarize")}</p>
            <p class="my-0 text-sm">${JSON.parse(sessionStorage.getItem("shortSummary") || "")}</p>
            <div class="mr-4 pt-2">
              <button type="button" class="text-md show-email-btn px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-zinc-800 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
                ${i18n.global.t("answerPage.seeMail")}
              </button>
            </div>
            <div class="email-content hidden mt-4 border-t pt-4">${sessionStorage.getItem("htmlContent") || ""}</div>
          </div>
        </div>
    `;

    AIContainer.value.innerHTML += messageHTML;
    emailContent.value = JSON.parse(sessionStorage.getItem("decodedData") || "");
}

async function displaySubject() {
    if (!AIContainer.value) return;

    const messageHTML = `
        <div class="flex pb-6">
          <div class="mr-4 flex flex-shrink-0">
            <span class="inline-flex h-12 w-12 items-center justify-center rounded-full">
                <img src="${API_BASE_URL}agent_icon/default-agent.png" alt="Default Icon" class="h-12 w-12 rounded-full object-cover">
            </span>
          </div>
          <div class="flex flex-col space-y-1 bg-white rounded-lg p-4 border border-gray-200">
            <p class="my-0 font-semibold text-lg">${subject.value}</p>
          </div>
        </div>
    `;

    AIContainer.value.innerHTML += messageHTML;
}

onMounted(async () => {
    const storedManualWidth = localStorage.getItem("manualEmailWidth");
    const storedAiWidth = localStorage.getItem("aiEmailWidth");
    if (storedManualWidth && storedAiWidth) {
        manualEmailWidth.value = parseInt(storedManualWidth, 10);
        aiEmailWidth.value = parseInt(storedAiWidth, 10);
    }

    const markAsRead = JSON.parse(sessionStorage.getItem("markAsRead") || "false");
    const emailId = JSON.parse(sessionStorage.getItem("emailId") || "null");
    if (markAsRead && emailId) {
        try {
            const result = await putData("user/emails/update/", { 
                ids: [emailId], 
                action: "read" 
            });
            if (!result.success) {
                console.error("Failed to mark email as read:", result.error);
            }
        } catch (error) {
            console.error("Error marking email as read:", error);
        }
    }

    try {
        isLoadingAgentSelection.value = true;

        // Initialize AIContainer first
        AIContainer.value = document.getElementById("AIContainer");
        if (!AIContainer.value) {
            displayPopup(
                "error",
                i18n.global.t("answerPage.error.title"),
                i18n.global.t("answerPage.error.containerNotFound")
            );
            return;
        }

        await Promise.all([fetchSignatures(), fetchAgents()]);

        await Promise.all([initializeQuill(), checkSignature(), getProfileImage(), fetchRecipients()]);

        if (signatures.value.length > 0) {
            insertSignature(signatures.value[0].signature_content);
        }

        document.addEventListener("keydown", handleKeyDown, true);
        window.addEventListener("resize", scrollToBottom);
        window.addEventListener("beforeunload", handleBeforeUnload);

        subject.value = JSON.parse(sessionStorage.getItem("subject") || "");
        subjectInput.value = "Re : " + subject.value;
        selectedPeople.value = [{ email: JSON.parse(sessionStorage.getItem("senderEmail") || "[]") }];
        selectedCC.value = JSON.parse(sessionStorage.getItem("cc") || "[]");
        selectedBCC.value = JSON.parse(sessionStorage.getItem("bcc") || "[]");
        emailSelected.value = JSON.parse(sessionStorage.getItem("emailUser") || "");
        importance.value = JSON.parse(sessionStorage.getItem("importance") || "");

        await fetchSelectedEmailData();

        // Check if there's a last used agent
        const response = await getData("user/agents/check_last_used/");
        if (response.success && response.data.exists) {
            const selectedAgentData = agents.value.find((agent) => agent.id === response.data.agent_id);
            if (selectedAgentData) {
                selectedAgent.value = selectedAgentData;
                await displayEmailContent();
                await fetchResponseKeywords();
            }
        } else {
            await displayEmailContent();
            await displayMessage(i18n.global.t("agent.chooseAiAssistant"), selectedAgent.value.picture);
            await displayAgentSelection();
        }

        document.addEventListener("click", (event: MouseEvent) => {
            const target = event.target as HTMLElement | null;

            if (target && target.classList.contains("show-email-btn")) {
                target.style.display = "none";

                const closestFlex = target.closest(".flex") as HTMLElement | null;
                if (closestFlex) {
                    const emailContent = closestFlex.querySelector(".email-content") as HTMLElement | null;
                    if (emailContent) {
                        emailContent.style.display = "block";
                    }
                }
            }
        });
    } catch (error) {
        displayPopup(
            "error",
            i18n.global.t("answerPage.error.title"),
            i18n.global.t("answerPage.error.initialization")
        );
    } finally {
        isLoadingAgentSelection.value = false;
    }
});

onBeforeUnmount(() => {
    window.removeEventListener("beforeunload", handleBeforeUnload);
    window.removeEventListener("mousemove", onDrag);
    window.removeEventListener("mouseup", stopDrag);
    document.removeEventListener("keydown", handleKeyDown, true);
});

async function getProfileImage() {
    const result = await getData(`user/social_api/get_profile_image/`, { email: emailSelected.value });
    if (!result.success) return;
    imageURL.value = result.data.profileImageUrl;
}

const handleBeforeUnload = (event: BeforeUnloadEvent) => {
    if (
        uploadedFiles.value.length ||
        selectedPeople.value.length ||
        selectedCC.value.length ||
        selectedBCC.value.length ||
        subjectInput.value !== ""
    ) {
        event.preventDefault();
    }
};

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
        quill = new Quill(editorElement, {
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
    const target = event.target as HTMLElement;

    if (showSignatureModal.value || target.closest("#dynamicTextarea")) {
        return;
    }

    if (
        event.key === "Enter" &&
        (target.closest(".ql-editor") || target.matches('input, textarea, [contenteditable="true"]'))
    ) {
        return;
    }

    if (event.key === "Enter") {
        event.preventDefault();
        event.stopPropagation();
        return;
    }

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
                <span class="inline-flex h-12 w-12 items-center justify-center rounded-full">
                    <img src="${API_BASE_URL}agent_icon/${selectedAgent.value.icon_name}" alt="Agent Icon" class="h-12 w-12 rounded-full object-cover">
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

function askContentAdvice(keyword?: string) {
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
                <button type="button" id="responseKeywordButton${index}" data-value="${keyword}" class="px-4 py-2 rounded-xl bg-transparent text-gray-900 hover:bg-zinc-800 hover:text-white border border-gray-900 focus:ring-1 focus:ring-gray-900 focus:ring-inset focus:border-gray-900">
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
            <span class="inline-flex h-12 w-12 items-center justify-center rounded-full">
                <img src="${API_BASE_URL}agent_icon/${selectedAgent.value.icon_name}" alt="Agent Icon" class="h-12 w-12 rounded-full object-cover">
            </span>
          </div>
          <div class="flex flex-col bg-white rounded-lg p-4 border border-gray-200">
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
    const quillInstance = getQuill?.();
    if (isWriting.value || !AIContainer.value || !quillInstance) {
        return;
    }
    isWriting.value = true;

    loading();
    scrollToBottom();

    const result = await postData("generate_email_answer/", {
        subject: subjectInput.value,
        body: emailContent.value,
        keyword: keyword,
        signature: signatures.value[0]?.signature_content || "",
    });

    hideLoading();

    if (!result.success) {
        await displayMessage?.(
            i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain"),
            selectedAgent.value.picture
        );
        return;
    }

    const quillEditorContainer = quillInstance.root;
    quillEditorContainer.innerHTML = result.data.emailAnswer;
    await displayMessage(
        i18n.global.t("constants.sendEmailConstants.doesThisResponseSuitYou"),
        selectedAgent.value.picture
    );
}

async function fetchResponseKeywords() {
    loading();
    const result = await postData("generate_email_response_keywords/", {
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

function insertSignature(signatureContent: string) {
    const quillInstance = quill;
    if (!quillInstance || !signatureContent) return;

    try {
        quillInstance.clipboard.dangerouslyPasteHTML(quillInstance.getLength(), `<p>${signatureContent}</p>`);

        nextTick(() => {
            quillInstance.setSelection(quillInstance.getLength(), 0);
        });
    } catch (error) {
        displayPopup(
            "error",
            i18n.global.t("answerPage.error.title"),
            i18n.global.t("answerPage.error.insertingSignature")
        );
    }
}

const fetchSignatures = async () => {
    const result = await getData("user/signatures/");
    if (result.success) {
        signatures.value = result.data;
    } else {
        displayPopup(
            "error",
            i18n.global.t("answerPage.error.title"),
            i18n.global.t("answerPage.error.fetchSignatures")
        );
    }
};

const checkSignature = () => {
    const hasSignature = signatures.value.length > 0;
    if (!hasSignature) {
        showSignatureModal.value = true;
    }
};

const handleSignatureCreated = async (newSignature: any) => {
    await new Promise((resolve) => setTimeout(resolve, 150));
    signatures.value.push(newSignature);
    if (quill) {
        insertSignature(newSignature.signature_content);
    }
};

async function setAgentLastUsed(agent: Agent) {
    const result = await putData(`user/agents/${agent.id}/update/`, {
        last_used: true,
    });

    if (!result.success) {
        displayPopup(
            "error",
            i18n.global.t("answerPage.error.title"),
            i18n.global.t("answerPage.error.updatingAgentStatus")
        );
        return;
    }

    // Clear the chat container before displaying new content
    if (AIContainer.value) {
        AIContainer.value.innerHTML = "";
    }

    // Display email content after agent is selected and set as last used
    await displayEmailContent();
}

// Ajout des fonctions de glissement
const initDrag = (event: MouseEvent) => {
    isDragging.value = true;
    startX.value = event.clientX;
    startManualWidth.value = manualEmailWidth.value;
    startAiWidth.value = aiEmailWidth.value;

    const container = (event.target as HTMLElement).closest(".flex");
    initialContainerWidth.value = container ? container.clientWidth : 0;

    window.addEventListener("mousemove", onDrag);
    window.addEventListener("mouseup", stopDrag);
};

const onDrag = (event: MouseEvent) => {
    if (!isDragging.value) return;

    const deltaX = event.clientX - startX.value;
    if (initialContainerWidth.value === 0) return;

    const deltaPercent = (deltaX / initialContainerWidth.value) * 100;
    let newManualWidth = startManualWidth.value + deltaPercent;
    let newAiWidth = startAiWidth.value - deltaPercent;

    const MIN_WIDTH = 20;
    const MAX_WIDTH = 80;

    if (newManualWidth < MIN_WIDTH) {
        newManualWidth = MIN_WIDTH;
        newAiWidth = 100 - MIN_WIDTH;
    } else if (newAiWidth < MIN_WIDTH) {
        newAiWidth = MIN_WIDTH;
        newManualWidth = 100 - MIN_WIDTH;
    }

    manualEmailWidth.value = newManualWidth;
    aiEmailWidth.value = newAiWidth;
};

const stopDrag = () => {
    if (isDragging.value) {
        isDragging.value = false;
        saveWidths();
        window.removeEventListener("mousemove", onDrag);
        window.removeEventListener("mouseup", stopDrag);
    }
};

const saveWidths = () => {
    localStorage.setItem("manualEmailWidth", manualEmailWidth.value.toString());
    localStorage.setItem("aiEmailWidth", aiEmailWidth.value.toString());
};

const handleSignatureModalClose = () => {
    showSignatureModal.value = false;
};
</script>

<style scoped>
/* Remove transition effects */
div:nth-child(2),
div:nth-child(4) {
    transition: none !important;
}

/* Draggable Divider Wrapper */
.drag-wrapper {
    position: relative;
    width: 1px;
    height: 100%;
    cursor: col-resize;
}

/* Visible Separator */
.separator {
    position: absolute;
    left: 50%;
    top: 0;
    transform: translateX(-50%);
    width: 0.5px;
    height: 100%;
    background-color: #e0e0e0;
    z-index: 1;
}

/* Transparent Drag Overlay */
.drag-overlay {
    position: absolute;
    left: -3.5px;
    top: 0;
    width: 8px;
    height: 100%;
    background: transparent;
    z-index: 2;
}

/* Optional: Hover effect */
.drag-wrapper:hover .separator {
    background-color: #aaa;
}
</style>
