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
                                    :src="selectedAgent.picture"
                                    alt="Agent Icon"
                                    class="w-6 h-6 rounded-full"
                                />
                                <span>{{ selectedAgent.id ? selectedAgent.agent_name : 'Select Agent' }}</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>
                            <div v-if="isDropdownOpen" class="absolute bottom-full left-0 mb-2 w-48 bg-white border border-gray-200 rounded-md shadow-lg z-50">
                                <ul>
                                    <li
                                        v-for="agent in agents"
                                        :key="agent.id"
                                        @click="selectAgent(agent)"
                                        class="flex items-center justify-between px-4 py-2 cursor-pointer hover:bg-gray-100"
                                    >
                                        <div class="flex items-center">
                                            <img :src="agent.picture" alt="Agent Icon" class="w-5 h-5 rounded-full mr-2" />
                                            <span>{{ agent.agent_name }}</span>
                                        </div>
                                        <button @click.stop="openUpdateAgentModal(agent)" class="text-blue-500 hover:text-blue-700">
                                            Edit
                                        </button>
                                    </li>
                                    <li
                                        @click="openCreateAgentModal"
                                        class="flex items-center px-4 py-2 cursor-pointer hover:bg-gray-100"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                                        </svg>
                                        <span>Create New Agent</span>
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

    <CreateAgentModal
        v-if="isCreateAgentModalOpen"
        @created="addAgent"
        @close="isCreateAgentModalOpen = false"
    />

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

const textareaValue = ref("");
const isWriting = inject<Ref<boolean>>("isWriting") || ref(false);
const AIContainer =
    inject<Ref<HTMLElement | null>>("AIContainer") || ref<HTMLElement | null>(document.getElementById("AIContainer"));
const textareaValueSave = inject<Ref<string>>("textareaValueSave") || ref("");
const history = inject<Ref<Record<string, any>>>("history") || ref({});
const subjectInput = inject<Ref<string>>("subjectInput") || ref("");
const importance = inject<Ref<string>>("importance") || ref("");
const imageURL = inject<Ref<string>>("imageURL") || ref("");
const setAgentLastUsed = inject<(agent: Agent) => void>("setAgentLastUsed");

const scrollToBottom = inject<() => void>("scrollToBottom");
const displayMessage = inject<(message: string, aiIcon: string) => void>("displayMessage");
const hideLoading = inject<() => void>("hideLoading");
const loading = inject<() => void>("loading");

const getQuill = inject<() => Quill | null>("getQuill");
const signatures = inject<Ref<any[]>>("signatures") || ref([]);
const emailContent = inject<Ref<string>>("emailContent") || ref("");
const agents = inject<Ref<Agent[]>>("agents") || ref<Agent[]>([]);
const selectedAgent = inject<Ref<Agent>>("selectedAgent") || ref<Agent>({
    id: "",
    agent_name: "Default Agent",
    picture: "/assets/default-agent.png",
    ai_template: "",
    length: "",
    formality: "",
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
});

function handleEnterKey(event: KeyboardEvent) {
    const target = event.target as HTMLElement | null;

    if (target && target.id === "dynamicTextarea" && event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        handleAIClick();
    }
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

function handleAIClick() {
    if (isWriting.value) {
        return;
    }
    setWriting();
    displayUserMessage();

    if (textareaValueSave.value == "") {
        displayMessage?.(i18n.global.t("constants.sendEmailConstants.noSuggestionsEnteredPleaseTryAgain"), selectedAgent.value.picture);
        return;
    }

    generateNewEmailResponse();
}

const generateNewEmailResponse = async () => {
    const quillInstance = getQuill?.();
    if (!AIContainer.value || !quillInstance) return;

    loading?.();
    scrollToBottom?.();

    const result = await postData("get_new_email_response/", {
        body: quillInstance.root.innerHTML,
        emailBody: emailContent.value,
        userInput: textareaValueSave.value,
        subject: subjectInput.value,
        importance: importance.value,
        history: history.value,
        signature: signatures.value[0].signature_content,
    });

    hideLoading?.();

    if (!result.success) {
        displayMessage?.(i18n.global.t("constants.sendEmailConstants.processingErrorTryAgain"), selectedAgent.value.picture);
        return;
    }

    history.value = result.data.history;
    const quillEditorContainer = quillInstance.root;
    quillEditorContainer.innerHTML = result.data.emailBody.replace(
        /(<ul>|<ol>|<\/li>)(?:[\s]+)(<li>|<\/ul>|<\/ol>)/g,
        "$1$2"
    );

    displayMessage?.(i18n.global.t("constants.sendEmailConstants.doesThisResponseSuitYou"), selectedAgent.value.picture);
};

const setWriting = () => {
    isWriting.value = true;
};

function adjustHeight(event: Event) {
    const textarea = event.target as HTMLTextAreaElement | null;

    if (textarea) {
        textarea.style.height = "auto";
        textarea.style.overflowY = "auto";
    }
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
    const index = agents.value.findIndex(agent => agent.id === updatedAgent.id);
    if (index !== -1) {
        agents.value[index] = updatedAgent;
        selectedAgent.value = updatedAgent;
    }
}

function deleteAgent(agentId: string) {
    agents.value = agents.value.filter(agent => agent.id !== agentId);
    if (selectedAgent.value.id === agentId) {
        selectedAgent.value = {
            id: "",
            agent_name: "Default Agent",
            picture: "/assets/default-agent.png",
            ai_template: "",
            length: "",
            formality: "",
        };
    }
}
</script>
