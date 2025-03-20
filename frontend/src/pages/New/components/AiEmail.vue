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

    <div class="flex flex-1 flex-col divide-y overflow-y-auto">
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
                @keydown.enter="handleEnterKey"
                @input="adjustHeight"
                v-model="textareaValue"
                class="overflow-y-hidden pt-4 pl-6 flex-1 w-full border-transparent bg-transparent text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 focus:border-transparent focus:bg-transparent focus:ring-0 2xl:pt-5 2xl:pl-7 2xl:text-base"
                :placeholder="$t('constants.instruction')"
            ></textarea>
            <div class="flex justify-between items-center mt-2 space-x-2">
                <div class="flex space-x-2 mx-3 2xl:mx-5">
                    <div class="flex">
                        <div class="flex my-3 2xl:my-5 relative">
                            <button
                                @click="toggleDropdown"
                                type="button"
                                class="flex items-center rounded-md bg-gray-200 px-3 py-2 text-sm text-gray-700 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500"
                            >
                                <img
                                    v-if="selectedAgent.id"
                                    :src="`${API_BASE_URL}agent_icon/${selectedAgent.icon_name}`"
                                    alt="Agent Icon"
                                    class="w-6 h-6 rounded-full mr-2"
                                />
                                <span>
                                    {{
                                        selectedAgent.id ? selectedAgent.agent_name : i18n.global.t("agent.selectAgent")
                                    }}
                                </span>
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    class="w-4 h-4"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M19 9l-7 7-7-7"
                                    />
                                </svg>
                            </button>
                            <div
                                v-if="isDropdownOpen"
                                class="absolute bottom-full left-0 mb-2 w-48 bg-white border border-gray-200 rounded-md shadow-lg z-50"
                            >
                                <ul>
                                    <li
                                        v-for="agent in agents"
                                        :key="agent.id"
                                        @click="selectAgent(agent)"
                                        class="flex items-center justify-between px-4 py-2 cursor-pointer hover:bg-gray-100"
                                    >
                                        <div class="flex items-center">
                                            <img
                                                :src="`${API_BASE_URL}agent_icon/${agent.icon_name}`"
                                                alt="Agent Icon"
                                                class="w-5 h-5 rounded-full mr-2"
                                            />
                                            <span>{{ agent.agent_name }}</span>
                                        </div>
                                        <button
                                            @click.stop="openUpdateAgentModal(agent)"
                                            class="text-blue-500 hover:text-blue-700"
                                        >
                                            {{ i18n.global.t("agent.edit") }}
                                        </button>
                                    </li>
                                    <li
                                        @click="openCreateAgentModal"
                                        class="flex items-center px-4 py-2 cursor-pointer hover:bg-gray-100"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            class="w-5 h-5 mr-2 text-gray-500"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke="currentColor"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M12 4v16m8-8H4"
                                            />
                                        </svg>
                                        <span>{{ i18n.global.t("agent.createNewAgent") }}</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <SendAiInstructionButton />
                </div>
            </div>
        </div>
    </div>

    <CreateAgentModal v-if="isCreateAgentModalOpen" @created="addAgent" @close="isCreateAgentModalOpen = false" />

    <UpdateAgentModal
        v-if="isUpdateAgentModalOpen"
        :agent="agentToUpdate"
        @updated="updateAgent"
        @deleted="deleteAgent"
        @close="isUpdateAgentModalOpen = false"
    />
</template>

<script setup lang="ts">
import { inject, provide, Ref, ref } from "vue";
import { postData } from "@/global/fetchData";
import SendAiInstructionButton from "@/global/components/SendAiInstructionButton.vue";
import CreateAgentModal from "@/global/components/CreateAgentModal.vue";
import UpdateAgentModal from "@/global/components/UpdateAgentModal.vue";
import { Agent, Recipient, AiRecipient } from "@/global/types";
import { i18n } from "@/global/preferences";
import Quill from "quill";
import { API_BASE_URL } from "@/global/const";

const displayMessage = inject<(message: string, aiIcon: string) => void>("displayMessage");
const scrollToBottom = inject<() => void>("scrollToBottom");
const loading = inject<() => void>("loading");
const hideLoading = inject<() => void>("hideLoading");
const setAgentLastUsed = inject<(agent: Agent) => void>("setAgentLastUsed");
const getQuill = inject<() => Quill | null>("getQuill");
const signatures = inject<Ref<any[]>>("signatures") || ref([]);
const emailSelected = inject<Ref<string>>("emailSelected") || ref("");

const isWriting = inject<Ref<boolean>>("isWriting") || ref(false);
const stepContainer = inject<Ref<number>>("stepContainer") || ref(0);
const history = inject<Ref<Record<string, any>>>("history") || ref({});
const AIContainer =
    inject<Ref<HTMLElement | null>>("AIContainer") || ref<HTMLElement | null>(document.getElementById("AIContainer"));
const textareaValue = ref("");
const selectedPeople = inject<Ref<Recipient[]>>("selectedPeople") || ref([]);
const selectedCC = inject<Ref<Recipient[]>>("selectedCC") || ref([]);
const selectedBCC = inject<Ref<Recipient[]>>("selectedBCC") || ref([]);
const imageURL = inject<Ref<string>>("imageURL") || ref("");
const textareaValueSave = inject<Ref<string>>("textareaValueSave") || ref("");
const subjectInput = inject<Ref<string>>("subjectInput") || ref("");
// const selectedFormality = inject<Ref<string>>("selectedFormality") || ref("");
const selectedLength = inject<Ref<string>>("selectedLength") || ref("");
const emailBody = inject<Ref<string>>("emailBody") || ref("");
// const contacts = inject<Ref<Recipient[]>>("contacts", ref([]));
const agents = inject<Ref<Agent[]>>("agents") || ref<Agent[]>([]);
const selectedAgent =
    inject<Ref<Agent>>("selectedAgent") ||
    ref({
        id: "",
        agent_name: i18n.global.t("agent.defaultAgent"),
        picture: "/assets/default-agent.png",
        ai_template: "",
        length: "",
        formality: "",
        icon_name: "default-agent.png",
    });

const isDropdownOpen = ref(false);
const isCreateAgentModalOpen = ref(false);
const isUpdateAgentModalOpen = ref(false);
const agentToUpdate = ref<Agent>({
    id: "",
    agent_name: "",
    picture: "",
    ai_template: "",
    length: "",
    formality: "",
    icon_name: "",
});

const askContent = inject<() => void>("askContent");

const isAiWriting = inject("isAiWriting") as Ref<boolean>;
const isFirstTimeEmail = inject("isFirstTimeEmail") as Ref<boolean>;

// Provide any additional functions if necessary
provide("handleAIClick", handleAIClick);
provide("selectedLength", selectedLength);

function handleEnterKey(event: any) {
    if (event.target.id === "dynamicTextarea" && event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        handleAIClick();
    }
}

const setWriting = () => {
    isWriting.value = true;
};

function adjustHeight(event: Event) {
    const textarea = event.target as HTMLTextAreaElement;
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}

async function handleAIClick() {
    if (!AIContainer.value) return;
    if (isWriting.value) {
        return;
    }

    // If no agent is selected (default agent), clear chat and select the second agent
    if (!selectedAgent.value.id && agents.value.length >= 2) {
        AIContainer.value.innerHTML = "";
        const aoAgent = agents.value[1];
        selectedAgent.value = aoAgent;
        setAgentLastUsed?.(aoAgent);
    }

    setWriting();
    displayUserMessage();

    try {
        const response = await postData("handle_email_action/", {
            user_input: textareaValueSave.value,
            subject: subjectInput.value,
            email_content: emailBody.value,
            history: history.value,
            destinary: selectedPeople.value.map((person) => ({
                username: person.username,
                email: person.email,
            })),
            signature: signatures.value.find((sig) => sig.id)?.signature_content,
        });

        console.log("response", response.data);

        if (!response.success) {
            displayMessage?.(
                i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain"),
                selectedAgent.value.picture
            );
            return;
        }

        const data = response.data;
        history.value = data.history;
        isAiWriting.value = false;

        switch (data.scenario) {
            case 1: {
                // Scenario 1: Extract Contacts
                const noUsersAdded = handleScenarioExtractContacts(data);
                if (noUsersAdded) {
                    displayMessage?.(
                        i18n.global.t("constants.sendEmailConstants.draftEmailRequest"),
                        selectedAgent.value.picture
                    );
                } else {
                    displayMessage?.(
                        i18n.global.t("newPage.noRecipientsFoundPleaseTryAgainOrEnterManually"),
                        selectedAgent.value.picture
                    );
                }
                break;
            }
            case 2: {
                // Scenario 2: Extract Contacts and Generate Email
                const recipientsAdded = handleScenarioExtractContacts(data);
                if (!recipientsAdded) {
                    displayMessage?.(
                        i18n.global.t("newPage.noRecipientsFoundPleaseTryAgainOrEnterManually"),
                        selectedAgent.value.picture
                    );
                }
                handleScenarioGenerateEmail(data);
                displayMessage?.(i18n.global.t("newPage.emailGenerated"), selectedAgent.value.picture);
                break;
            }
            case 3: {
                // 3: Generate Email
                handleScenarioGenerateEmail(data);
                displayMessage?.(i18n.global.t("newPage.emailGenerated"), selectedAgent.value.picture);
                break;
            }
            case 4: {
                // Scenario 4: Improve Draft
                handleScenarioImproveDraft(data);
                break;
            }
            default: {
                const defaultIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
                displayMessage?.(i18n.global.t("constants.sendEmailConstants.unrecognizedScenario"), defaultIcon);
            }
        }
    } catch (error) {
        console.error("Error handling AI click:", error);
        displayMessage?.(
            i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain"),
            selectedAgent.value.picture
        );
    } finally {
        isWriting.value = false;
        isFirstTimeEmail.value = true;
        isAiWriting.value = true;
    }
}

function handleScenarioExtractContacts(data: any): boolean {
    const mainRecipients = data.mainRecipients || [];
    const ccRecipients = data.ccRecipients || [];
    const bccRecipients = data.bccRecipients || [];

    console.log("mainRecipients", mainRecipients);

    let noUsersAdded = true;
    let waitforUserChoice = false;

    noUsersAdded = processSingleEmailRecipients(mainRecipients, selectedPeople.value) && noUsersAdded;
    noUsersAdded = processSingleEmailRecipients(ccRecipients, selectedCC.value) && noUsersAdded;
    noUsersAdded = processSingleEmailRecipients(bccRecipients, selectedBCC.value) && noUsersAdded;

    if (mainRecipients.length > 0 || ccRecipients.length > 0 || bccRecipients.length > 0) {
        waitforUserChoice = processMultipleEmailRecipients(mainRecipients, "main") || waitforUserChoice;
        waitforUserChoice = processMultipleEmailRecipients(ccRecipients, "cc") || waitforUserChoice;
        waitforUserChoice = processMultipleEmailRecipients(bccRecipients, "bcc") || waitforUserChoice;

        scrollToBottom?.();
    }

    if (noUsersAdded && !waitforUserChoice) {
        return false;
    }
    return true;
}

function processSingleEmailRecipients(recipients: AiRecipient[], selectedGroup: Recipient[]) {
    let noUsersAdded = true;
    for (let i = 0; i < recipients.length; i++) {
        const user = recipients[i];
        const emails = user.email;
        if (emails.length === 1) {
            const emailValue = typeof emails[0] === "string" ? emails[0] : emails[0].email;
            selectedGroup.push({ username: user.username, email: emailValue });
            recipients.splice(i, 1);
            noUsersAdded = false;
            i--;
        }
    }
    return noUsersAdded;
}

function processMultipleEmailRecipients(recipients: AiRecipient[], type: string): boolean {
    if (recipients.length === 0) return false;

    console.log("emailList", recipients);
    askChoiceRecipier(recipients, type);
    return true;
}

function askChoiceRecipier(recipients: AiRecipient[], type: string) {
    if (!recipients.length) return;

    // const userLabel =
    //     type === "main"
    //         ? i18n.global.t("newPage.mainRecipient")
    //         : type === "cc"
    //         ? i18n.global.t("newPage.ccRecipient")
    //         : i18n.global.t("newPage.bccRecipient");
 

    const messageHTML = `
      <div class="flex pb-6">
        <div class="mr-3 flex-shrink-0">
          <span class="inline-flex h-12 w-12 items-center justify-center rounded-full">
            <img src="${API_BASE_URL}agent_icon/${
        selectedAgent.value.icon_name
    }" alt="Agent Icon" class="h-12 w-12 rounded-full object-cover">
          </span>
        </div>
        <div class="flex flex-col bg-white rounded-lg p-4 max-w-md border border-gray-200">
          <div class="mb-3">
            ${i18n.global.t("newPage.severalUser")} 
          </div>
          ${
              Array.isArray(recipients[0].email)
                  ? recipients[0].email
                        .map((emailItem, index) => {
                            console.log("recipient", emailItem.email);
                            const buttonLabel = type === "main" ? "main" : type === "cc" ? "cc" : "bcc";
                            const buttonId = `button-${buttonLabel}-0-${index}`;

                            return `
                      <div class="mb-4 last:mb-0">
                        <div class="space-y-2">
                          <button 
                            type="button" 
                            id="${buttonId}" 
                            class="w-full px-4 py-2 text-left rounded-lg bg-white border border-gray-300 text-gray-900 hover:bg-gray-100 focus:ring-1 focus:ring-gray-900 focus:border-gray-900"
                          >
                            <div class="text-sm font-medium text-gray-900">
                              ${emailItem.username}
                            </div>
                            <div class="text-sm text-gray-500">
                              ${emailItem.email}
                            </div>
                          </button>
                        </div>
                      </div>
                    `;
                        })
                        .join("")
                  : `
                <div class="mb-6 last:mb-0">
                  <div class="space-y-2">
                    <button 
                      type="button" 
                      id="button-${type}-0"
                      class="w-full px-4 py-2 text-left rounded-lg bg-white border border-gray-300 text-gray-900 hover:bg-gray-100 focus:ring-1 focus:ring-gray-900 focus:border-gray-900"
                    >
                      <div class="text-sm text-gray-500">
                        ${recipients[0].email}
                      </div>
                    </button>
                  </div>
                </div>
              `
          }
        </div>
      </div>
    `;

    if (!AIContainer.value) return;
    AIContainer.value.innerHTML += messageHTML;

    recipients.forEach((recipient, recipientIndex) => {
        const buttonLabel = type === "main" ? "main" : type === "cc" ? "cc" : "bcc";

        if (Array.isArray(recipient.email)) {
            recipient.email.forEach((emailItem, emailIndex) => {
                const buttonId = `button-${buttonLabel}-${recipientIndex}-${emailIndex}`;

                setTimeout(() => {
                    const button = document.getElementById(buttonId);
                    if (!button) return;

                    button.addEventListener("click", () => {
                        const person: Recipient = {
                            username: emailItem.username,
                            email: emailItem.email,
                        };

                        if (type === "main") {
                            const isPersonAlreadySelected = selectedPeople.value.some((p) => p.email === person.email);
                            if (!isPersonAlreadySelected) {
                                selectedPeople.value.push(person);
                            }
                        } else if (type === "cc") {
                            const isPersonAlreadySelected = selectedCC.value.some((p) => p.email === person.email);
                            if (!isPersonAlreadySelected) {
                                selectedCC.value.push(person);
                            }
                        } else {
                            const isPersonAlreadySelected = selectedBCC.value.some((p) => p.email === person.email);
                            if (!isPersonAlreadySelected) {
                                selectedBCC.value.push(person);
                            }
                        }
                    });
                }, 0);
            });
        }
    });
}

function handleScenarioGenerateEmail(data: any) {
    const quillInstance = getQuill?.();
    if (!AIContainer.value || !quillInstance) return;

    const formattedContent = data.emailBody
        .replace(/<\/p>(?!<div>)/g, "</p><p></p>")
        .replace(/<div>/g, "<p>")
        .replace(/<\/div>/g, "</p>");

    quillInstance.root.innerHTML = formattedContent;
    subjectInput.value = data.subject;
    emailBody.value = data.emailBody;

    scrollToBottom?.();
}

function handleScenarioImproveDraft(data: any) {
    const quillInstance = getQuill?.();
    if (!quillInstance || !AIContainer.value) return;

    quillInstance.root.innerHTML = data.emailBody.replace(/<\/p>/g, "</p><p></p>");
    subjectInput.value = data.subject;
    emailBody.value = data.emailBody;

    displayImprovedDraft();
    stepContainer.value += 1;
    scrollToBottom?.();
}

function displayUserMessage() {
    if (!AIContainer.value) return;

    const messageHTML = `
        <div class="flex pb-6 justify-end">
            <div class="max-w-md">
                <div class="flex items-start gap-x-3 justify-end">
                    <div class="bg-blue-100 border border-blue-200 p-4 rounded-lg">
                        <p class="text-gray-800">${textareaValue.value}</p>
                    </div>
                    <span class="inline-flex h-12 w-12 items-center justify-center rounded-full flex-shrink-0">
                        <img src="${imageURL.value}" alt="Profile Image" class="h-12 w-12 rounded-full object-cover">
                    </span>
                </div>
            </div>
        </div>
    `;
    AIContainer.value.innerHTML += messageHTML;
    textareaValueSave.value = textareaValue.value;
    textareaValue.value = "";
    scrollToBottom?.();
}

// function displayMultipleEmailsMessage() {
//     if (!AIContainer.value) return;
//     const messageHTML = `
//         <div class="flex pb-6">
//             <div class="mr-3 flex-shrink-0">
//                 <span class="inline-flex h-12 w-12 items-center justify-center rounded-full bg-gray-900 text-white">
//                     <img src="${API_BASE_URL}agent_icon/${selectedAgent.value.icon_name}" alt="Agent Icon" class="h-12 w-12 rounded-full object-cover">
//                 </span>
//             </div>
//             <div class="flex flex-col bg-white rounded-lg p-4 max-w-md border border-gray-200">
//                 <p class="text-gray-800">I found the following recipients:</p>
//                 <ul class="mt-2 list-disc pl-4">
//                     <li>Main recipient: Fabien fasson</li>
//                 </ul>
//                 <p class="mt-2 text-gray-800">Would you like me to help you compose an email for these recipients?</p>
//             </div>
//         </div>
//     `;
//     AIContainer.value.innerHTML += messageHTML;
// }

function displayImprovedDraft() {
    displayMessage?.(i18n.global.t("newPage.draftImproved"), selectedAgent.value.picture);
}

function toggleDropdown() {
    isDropdownOpen.value = !isDropdownOpen.value;
}

function selectAgent(agent: Agent) {
    selectedAgent.value = agent;
    setAgentLastUsed?.(agent);
    isDropdownOpen.value = false;
}

function openCreateAgentModal() {
    isCreateAgentModalOpen.value = true;
    isDropdownOpen.value = false;
}

function openUpdateAgentModal(agent: Agent) {
    agentToUpdate.value = agent;
    isUpdateAgentModalOpen.value = true;
}

function addAgent(newAgent: Agent) {
    agents.value.push(newAgent);
    selectedAgent.value = newAgent;
}

function updateAgent(updatedAgent: Agent) {
    const index = agents.value.findIndex((agent) => agent.id === updatedAgent.id);
    if (index !== -1) {
        agents.value[index] = updatedAgent;
        selectedAgent.value = updatedAgent;
    }
}

function deleteAgent(agentId: string) {
    agents.value = agents.value.filter((agent) => agent.id !== agentId);
    if (selectedAgent.value.id === agentId) {
        selectedAgent.value = {
            id: "",
            agent_name: i18n.global.t("agent.defaultAgent"),
            picture: "/assets/default-agent.png",
            ai_template: "",
            length: "",
            formality: "",
            icon_name: "default-agent.png",
        };
    }
}
</script>
