<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
    />
    <div class="flex flex-col justify-center items-center h-screen">
        <div class="flex h-full w-full relative">
            <div :class="['ring-1 shadow-sm ring-black ring-opacity-5', isNavMinimized ? 'w-20' : 'w-60']">
                <Navbar @update:isMinimized="(value) => (isNavMinimized = value)" />
            </div>
            <div
                :style="{ width: manualEmailWidth + '%' }"
                class="bg-white lg:ring-1 lg:ring-black lg:ring-opacity-5 h-full"
            >
                <ManualEmail />
            </div>

            <!-- Enhanced Draggable Divider with Hidden Area -->
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
        @close="showSignatureModal = false"
        @created="handleSignatureCreated"
    />
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, provide, Ref, onUnmounted, watch, computed, onBeforeUnmount } from "vue";
import Quill from "quill";
import AiEmail from "./components/AiEmail.vue";
import ManualEmail from "@/global/components/ManualEmail/ManualEmail.vue";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { getData, putData, postData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import { Recipient, Agent, EmailLinked, UploadedFile } from "@/global/types";
import Navbar from "@/global/components/Navbar.vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import userImage from "@/assets/user.png";
import SignatureModal from "@/global/components/SignatureModal.vue";
import { API_BASE_URL } from "@/global/const";

const showNotification = ref(false);
const isWriting = ref(false);
const isLoading = ref(false);
const isFirstTimeEmail = ref(true);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const subjectInput = ref("");
const textareaValueSave = ref("");
const emailBody = ref("");
const subject = ref("");
const emailSelected = ref(localStorage.getItem("email") || "");
const selectedLength = ref("short");
const selectedFormality = ref("formal");
const timerId = ref<number | null>(null);
const AIContainer = ref<HTMLElement | null>(null);
const scrollableDiv = ref<HTMLDivElement | null>(null);
const quillContent = ref("");
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
const imageURL = ref<string>(userImage);
const showSignatureModal = ref(false);
const signatures = ref<any[]>([]);
const agents = ref<Agent[]>([]);
const isLoadingAgentSelection = ref(false);
const isInitialized = ref(false);
const isAiWriting = ref(false);
const manualEmailWidth = ref(55);
const aiEmailWidth = ref(45);
const initialContainerWidth = ref(0);
const isNavMinimized = ref(localStorage.getItem("navbarMinimized") === "true");
let quill: Quill | null = null;
const selectedAgent = ref<Agent>({
    id: "",
    agent_name: i18n.global.t("agent.defaultAgent"),
    picture: "/assets/default-agent.png",
    ai_template: "",
    length: "",
    formality: "",
    icon_name: "default-agent.png",
});

const scrollToBottom = async () => {
    await nextTick();
    const element = scrollableDiv.value;
    if (!element) return;
    element.scrollTop = element.scrollHeight;
};

const askContent = () => {
    if (!AIContainer.value) return;
    displayMessage?.(i18n.global.t("constants.sendEmailConstants.draftEmailRequest"), selectedAgent.value.icon_name);
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
        console.error("Could not find animated paragraph element");
    }
};

provide("imageURL", imageURL);
provide("emailSelected", emailSelected);
provide("selectedPeople", selectedPeople);
provide("selectedCC", selectedCC);
provide("selectedBCC", selectedBCC);
provide("stepContainer", stepContainer);
provide("getQuill", getQuill);
provide("AIContainer", AIContainer);
provide("counterDisplay", counterDisplay);
provide("isWriting", isWriting);
provide("uploadedFiles", uploadedFiles);
provide("fileObjects", fileObjects);
provide("subjectInput", subjectInput);
provide("emailsLinked", emailsLinked);
provide("contacts", contacts);
provide("history", history);
provide("emailBody", emailBody);
provide("textareaValueSave", textareaValueSave);
provide("selectedLength", selectedLength);
provide("selectedFormality", selectedFormality);
provide("displayPopup", displayPopup);
provide("displayMessage", displayMessage);
provide("scrollToBottom", scrollToBottom);
provide("loading", loading);
provide("hideLoading", hideLoading);
provide("getProfileImage", getProfileImage);
provide("askContent", askContent);
provide("agents", agents);
provide("selectedAgent", selectedAgent);
provide("setAgentLastUsed", setAgentLastUsed);
provide("signatures", signatures);
provide("isAiWriting", isAiWriting);
provide("isFirstTimeEmail", isFirstTimeEmail);

onMounted(async () => {
    try {
        isLoadingAgentSelection.value = true;

        // Initialize AIContainer first
        AIContainer.value = document.getElementById("AIContainer");
        if (!AIContainer.value) {
            console.error("AIContainer element not found");
            return;
        }

        const storedManualWidth = localStorage.getItem("manualEmailWidth");
        const storedAiWidth = localStorage.getItem("aiEmailWidth");
        if (storedManualWidth && storedAiWidth) {
            manualEmailWidth.value = parseInt(storedManualWidth, 10);
            aiEmailWidth.value = parseInt(storedAiWidth, 10);
        }

        // Rest of the initialization...
        await Promise.all([fetchSignatures(), fetchAgents()]);

        await Promise.all([
            checkSignature(),
            getProfileImage(),
            initializeQuill(),
            checkLastUsedAgent(),
            fetchEmailLinked(),
            fetchRecipients(),
            fetchPrimaryEmail(),
        ]);

        if (signatures.value.length > 0) {
            insertSignature(signatures.value[0].signature_content);
        }

        document.addEventListener("keydown", handleKeyDown);
        localStorage.removeItem("uploadedFiles");
        window.addEventListener("resize", scrollToBottom);
        window.addEventListener("beforeunload", handleBeforeUnload);

        isInitialized.value = true;
    } catch (error) {
        displayPopup("error", i18n.global.t("newPage.error.title"), i18n.global.t("newPage.error.initialization"));
    } finally {
        isLoadingAgentSelection.value = false;
    }
});

onUnmounted(() => {
    window.removeEventListener("beforeunload", handleBeforeUnload);
});

watch(emailSelected, () => {
    getProfileImage();
    checkSignature();
});

async function getProfileImage() {
    const result = await getData(`user/social_api/get_profile_image/`, { email: emailSelected.value });
    if (!result.success) return;
    imageURL.value = result.data.profileImageUrl;
}

/**
 * Normalizes and tokenizes a string.
 * @param str - The string to process.
 * @returns An array of tokens.
 */
function tokenize(str: string): string[] {
    const withoutHtml = str.replace(/<[^>]*>/g, " ");
    const lowerCased = withoutHtml.toLowerCase();
    return lowerCased.split(/\s+/).filter((word) => word.length > 0);
}

/**
 * Calculates the Jaccard Similarity between two strings.
 * @param a - First string.
 * @param b - Second string.
 * @returns Similarity score between 0 and 1.
 */
function jaccardSimilarity(a: string, b: string): number {
    const tokensA = new Set(tokenize(a));
    const tokensB = new Set(tokenize(b));

    const intersection = new Set([...tokensA].filter((word) => tokensB.has(word)));
    const union = new Set([...tokensA, ...tokensB]);

    if (union.size === 0) return 1; // Both strings are empty

    return intersection.size / union.size;
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
        quill = new Quill(editorElement, {
            theme: "snow",
            modules: { toolbar: toolbarOptions },
        });

        quill.on("text-change", () => {
            quillContent.value = quill?.root.innerHTML ?? "";
            emailBody.value = quillContent.value;

            if (isFirstTimeEmail.value && !isAiWriting.value) {
                const currentContent = quillContent.value.trim();

                const signatureContentRaw = signatures.value.length > 0 ? signatures.value[0].signature_content : "";

                const plainTextContent = currentContent.replace(/<[^>]*>/g, "").trim();
                const signaturePlainText = signatureContentRaw.replace(/<[^>]*>/g, "").trim();

                const similarity = jaccardSimilarity(plainTextContent, signaturePlainText);

                const SIMILARITY_THRESHOLD = 0.9;

                if (
                    plainTextContent.length >= 8 && // Minimum meaningful characters
                    similarity < SIMILARITY_THRESHOLD // Less than 90% similarity
                ) {
                    handleInputUpdateMailContent(quillContent.value);
                }
            } else {
                isAiWriting.value = false;
            }
        });
    }
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
        console.error("Error inserting signature:", error);
    }
}

function handleInputUpdateMailContent(newMessage: string) {
    if (newMessage !== "") {
        askContentAdvice();
        scrollToBottom();
        isFirstTimeEmail.value = false;
    }
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
                resolve();
            }
        }, 20);
    });
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
            i18n.global.t("constants.popUpConstants.errorMessages.agentsFetchError"),
            error instanceof Error ? error.message : i18n.global.t("answerPage.error.unknownError")
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
            selectedBCC.value.length === 0 &&
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

async function displayErrorProcessingMessage() {
    const message = i18n.global.t("constants.sendEmailConstants.processingErrorApology");
    await displayMessage(message, selectedAgent.value.icon_name);
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

function askContentAdvice() {
    if (!AIContainer.value) return;

    const message = i18n.global.t("constants.sendEmailConstants.emailCompositionAssistance");

    const messageHTML = `
      <div class="pb-12">
        <div class="flex">
            <div class="mr-4">
                <span class="inline-flex h-12 w-12 items-center justify-center rounded-full">
                    <img src="${API_BASE_URL}agent_icon/${
        selectedAgent.value.icon_name
    }" alt="Agent Icon" class="h-12 w-12 rounded-full object-cover">
                </span>
            </div>
            <div class="flex flex-col bg-white rounded-lg p-4 border border-gray-200">
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
    if (!AIContainer.value || !quill) return;
    loading();

    console.log("subjectInput.value", subjectInput.value);
    console.log("emailBody", emailBody.value);

    const result = await postData("correct_email_language/", {
        subject: subjectInput.value || "",
        body: emailBody.value,
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
                      <span class="inline-flex h-12 w-12 items-center justify-center rounded-full">
                        <img src="${API_BASE_URL}agent_icon/${
        selectedAgent.value.icon_name
    }" alt="Agent Icon" class="h-12 w-12 rounded-full object-cover">
                      </span>
                  </div>
                  <div class="flex flex-col bg-white rounded-lg p-4 border border-gray-200">
                      <p><strong>${i18n.global.t("newPage.subject")}</strong> ${result.data.correctedSubject}</p>
                      <p><strong>${i18n.global.t("newPage.emailContent")}</strong> ${formattedBody}</p>
                  </div>
              </div>
          `;
    AIContainer.value.innerHTML += messageHTML;
    subjectInput.value = result.data.correctedSubject;
    const quillEditorContainer = quill.root;
    quillEditorContainer.innerHTML = result.data.correctedBody;

    const message = i18n.global.t("constants.sendEmailConstants.spellingCorrectionRequest");

    await displayMessage(message, selectedAgent.value.icon_name);
}

async function checkCopyWriting() {
    if (!AIContainer.value) return;
    loading();

    const result = await postData("check_email_copywriting/", {
        subject: subjectInput.value,
        body: emailBody.value,
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
                        <span class="inline-flex h-12 w-12 items-center justify-center rounded-full">
                            <img src="${API_BASE_URL}agent_icon/${selectedAgent.value.icon_name}" alt="Agent Icon" class="h-12 w-12 rounded-full object-cover">
                        </span>
                  </div>
                  <div class="flex flex-col bg-white rounded-lg p-4 border border-gray-200">
                      <p>${formattedCopWritingOutput}</p>
                  </div>
              </div>
          `;
    AIContainer.value.innerHTML += messageHTML;

    const message = i18n.global.t("constants.sendEmailConstants.copywritingCheckRequest");
    await displayMessage(message, selectedAgent.value.icon_name);
}

async function writeBetter() {
    if (!AIContainer.value || !quill) return;
    loading();

    const result = await postData("improve_draft/", {
        userInput: textareaValueSave.value,
        length: selectedLength.value,
        formality: selectedFormality.value,
        subject: subjectInput.value,
        body: emailBody.value,
        history: history.value,
    });

    if (!result.success) {
        displayErrorProcessingMessage();
        return;
    }

    hideLoading();
    subject.value = result.data.subject;
    emailBody.value = result.data.emailBody;
    history.value = result.data.history;

    const messageHTML = `
            <div class="flex pb-12">
                <div class="mr-4 flex">
                    <span class="inline-flex h-12 w-12 items-center justify-center rounded-full">
                        <img src="${API_BASE_URL}agent_icon/${
        selectedAgent.value.icon_name
    }" alt="Agent Icon" class="h-12 w-12 rounded-full object-cover">
                    </span>
                </div>
                <div class="flex flex-col bg-white rounded-lg p-4 border border-gray-200">
                    <p><strong>${i18n.global.t("newPage.subject")}</strong> ${result.data.subject}</p>
                    <p><strong>${i18n.global.t("newPage.emailContent")}</strong> ${result.data.emailBody}</p>
                </div>
            </div>
        `;
    AIContainer.value.innerHTML += messageHTML;
    subjectInput.value = result.data.subject;
    const quillEditorContainer = quill.root;
    quillEditorContainer.innerHTML = result.data.emailBody;

    await displayMessage(
        i18n.global.t("constants.sendEmailConstants.betterEmailFeedbackRequest"),
        selectedAgent.value.picture
    );
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
          class="h-12 h-12 rounded-full mr-4 object-cover flex-shrink-0"
        />
        <div class="flex-1">
          <h3 class="text-xl font-semibold text-left">${agent.agent_name}</h3>
          <p class="text-gray-600 mt-1 text-left">${agent.ai_template}</p>
          <div class="flex text-sm text-gray-500 mt-2">
            <p class="mr-4"><span class="font-medium">${i18n.global.t("newPage.length")}:</span> ${capitalize(
                    agent.length
                )}</p>
            <p><span class="font-medium">${i18n.global.t("newPage.formality")}:</span> ${capitalize(
                    agent.formality
                )}</p>
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
                        displayMessage(i18n.global.t("agent.AiGreeting"), selectedAgent.value.icon_name);
                        setAgentLastUsed(selectedAgent.value);
                    }
                });
            });
        }
    } catch (error) {
        displayPopup(
            "error",
            i18n.global.t("newPage.error.title"),
            i18n.global.t("newPage.error.displayingAgentSelection")
        );
    }
};

const checkLastUsedAgent = async () => {
    try {
        if (!agents.value.length) {
            displayPopup(
                "error",
                i18n.global.t("newPage.error.title"),
                i18n.global.t("newPage.error.noAgentsAvailable")
            );
            return;
        }

        const response = await getData("user/agents/check_last_used/");
        if (response.success && response.data.exists) {
            const selectedAgentData = agents.value.find((agent) => agent.id === response.data.agent_id);
            if (selectedAgentData) {
                selectedAgent.value = selectedAgentData;
                await displayMessage(i18n.global.t("agent.AiGreeting"), selectedAgent.value.icon_name);
            }
        } else {
            await displayMessage(i18n.global.t("agent.chooseAiAssistant"), selectedAgent.value.icon_name);
            await displayAgentSelection();
        }
    } catch (error) {
        displayPopup(
            "error",
            i18n.global.t("newPage.error.title"),
            i18n.global.t("newPage.error.checkingLastUsedAgent")
        );
    }
};

const fetchSignatures = async () => {
    const result = await getData("user/signatures/");
    if (result.success) {
        signatures.value = result.data;
    } else {
        displayPopup("error", i18n.global.t("newPage.error.title"), i18n.global.t("newPage.error.fetchSignatures"));
    }
};

const checkSignature = () => {
    const hasSignature = signatures.value.length > 0;
    if (!hasSignature) {
        showSignatureModal.value = true;
    }
};

const handleSignatureCreated = (newSignature: any) => {
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
        displayPopup("error", i18n.global.t("newPage.error.title"), i18n.global.t("newPage.error.updatingAgentStatus"));
    }
}

const isDragging = ref(false);
const startX = ref(0);
const startManualWidth = ref(0);
const startAiWidth = ref(0);

const initDrag = (event: MouseEvent) => {
    isDragging.value = true;
    startX.value = event.clientX;
    startManualWidth.value = manualEmailWidth.value;
    startAiWidth.value = aiEmailWidth.value;

    // Store the container width at the start
    const container = (event.target as HTMLElement).closest(".flex");
    initialContainerWidth.value = container ? container.clientWidth : 0;

    window.addEventListener("mousemove", onDrag);
    window.addEventListener("mouseup", stopDrag);
};

const onDrag = (event: MouseEvent) => {
    if (!isDragging.value) return;

    const deltaX = event.clientX - startX.value;

    // Prevent division by zero
    if (initialContainerWidth.value === 0) return;

    const deltaPercent = (deltaX / initialContainerWidth.value) * 100;

    let newManualWidth = startManualWidth.value + deltaPercent;
    let newAiWidth = startAiWidth.value - deltaPercent;

    // Set boundaries to prevent widths from becoming too small or too large
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

onBeforeUnmount(() => {
    window.removeEventListener("mousemove", onDrag);
    window.removeEventListener("mouseup", stopDrag);
});

const saveWidths = () => {
    localStorage.setItem("manualEmailWidth", manualEmailWidth.value.toString());
    localStorage.setItem("aiEmailWidth", aiEmailWidth.value.toString());
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
    width: 1px; /* Same as the visible separator */
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
    left: -3.5px; /* (8px - 1px) / 2 */
    top: 0;
    width: 8px; /* Hidden draggable area width */
    height: 100%;
    background: transparent;
    z-index: 2;
}

/* Optional: Hover effect for better UX */
.drag-wrapper:hover .separator {
    background-color: #aaa; /* Slight color change on hover for subtle feedback */
}
</style>
