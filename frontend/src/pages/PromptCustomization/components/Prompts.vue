<template>
    <div class="max-w-4xl mx-auto p-6">
        <!-- Header Section -->
        <div class="mb-8">
            <h1 class="text-2xl font-bold mb-4">Prompt Customization</h1>
            <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                            <path
                                fill-rule="evenodd"
                                d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                                clip-rule="evenodd"
                            />
                        </svg>
                    </div>
                    <div class="ml-3">
                        <h3 class="text-sm font-medium text-yellow-800">Important Notice</h3>
                        <div class="mt-2 text-sm text-yellow-700">
                            <p>Modifying default prompts may affect Aomail's functionality. Please note:</p>
                            <ul class="list-disc ml-5 mt-2">
                                <li>Changes are made at your own risk</li>
                                <li>Prompts are tested with Gemini 1.5 Pro and Gemini 2.0 Flash</li>
                                <li>We recommend making minimal changes to default prompts</li>
                                <li>Use the playground (coming soon) to test your changes</li>
                                <li>
                                    Do not change anything after --- as this tells the llm the format of the response
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Prompt Editor Section -->
        <div class="space-y-6">
            <div class="flex justify-between items-center">
                <h2 class="text-lg font-semibold">Edit Prompt</h2>
                <button
                    @click="resetToDefault"
                    class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                    Reset to Default
                </button>
            </div>

            <div class="bg-gray-50 rounded-lg p-4">
                <h3 class="text-sm font-medium text-gray-900 mb-2">Required Variables</h3>
                <div class="flex flex-wrap gap-2">
                    <span
                        v-for="variable in defaultPrompts[0].variables"
                        :key="variable"
                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                    >
                        {{ variable }}
                    </span>
                </div>
            </div>

            <div>
                <label class="typo__label">Select LLM Provider</label>
                <multiselect
                    v-model="llmProvider"
                    :options="llmProviderOptions"
                    track-by="provider"
                    label="provider"
                    :searchable="false"
                    :close-on-select="true"
                    :show-labels="false"
                    placeholder="Pick a value"
                    aria-label="pick a value"
                    @select="changeProvider"
                ></multiselect>
                <pre class="language-json"><code>{{ llmProvider }}</code></pre>
            </div>

            <div v-if="llmProvider">
                <label class="typo__label">Select LLM Model</label>
                <multiselect
                    v-model="llmModel"
                    :options="llmModelOptions"
                    label="name"
                    :searchable="false"
                    :close-on-select="true"
                    :show-labels="false"
                    placeholder="Pick a value"
                    aria-label="pick a value"
                ></multiselect>
                <pre class="language-json"><code>{{ llmModel }}</code></pre>
            </div>

            <div class="space-y-4">
                <textarea
                    v-model="prompt"
                    class="w-full h-64 px-4 py-3 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter your custom prompt here..."
                />

                <div class="flex justify-end">
                    <button
                        @click="savePrompt"
                        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                    >
                        Save Changes
                    </button>
                </div>
            </div>
        </div>

        <!-- Support Links -->
        <div class="mt-8 border-t pt-6">
            <h3 class="text-sm font-medium text-gray-900 mb-2">Need Help?</h3>
            <div class="flex space-x-4">
                <a
                    href="https://discord.com/invite/JxbPZNDd"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-sm text-blue-600 hover:text-blue-500"
                >
                    Join our Discord
                </a>
                <a
                    href="https://github.com/aomail-ai/aomail-app/issues/new?template=feature-request.yml"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-sm text-blue-600 hover:text-blue-500"
                >
                    Submit Feature Request
                </a>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, ref, computed } from "vue";
import Multiselect from "vue-multiselect";

interface Prompt {
    name: string;
    prompt: string;
    variables: string[];
}

interface LLMModel {
    name: string;
    description: string;
}

interface LLMProvider {
    provider: string;
    headquarters: string;
    apiReference: string;
    description: string;
    models: LLMModel[];
}

const llmProviderOptions: LLMProvider[] = [
    {
        provider: "google",
        headquarters: "Mountain View, CA, USA",
        apiReference: "https://ai.google.dev/gemini-api/docs/models/gemini",
        description: "Google's AI model provider",
        models: [
            {
                name: "gemini-1.5-pro",
                description:
                    "Most capable model for highly complex tasks, with improved performance in coding, math, and reasoning. Supports text, images, and function calling.",
            },
            {
                name: "gemini-2.0-flash",
                description:
                    "Latest model optimized for speed and efficiency. Best for real-time applications requiring fast responses while maintaining high quality output.",
            },
        ],
    },
    {
        provider: "openai",
        headquarters: "San Francisco, CA, USA",
        apiReference: "https://platform.openai.com/docs/models#gpt-4o",
        description: "OpenAI's AI model provider",
        models: [
            {
                name: "gpt-4o-mini",
                description:
                    "Most capable multimodal model, optimized for both vision and language tasks. Excels at complex reasoning and creative generation.",
            },
        ],
    },
    {
        provider: "anthropic",
        headquarters: "San Francisco, CA, USA",
        description: "Anthropic's AI model provider",
        apiReference: "https://docs.anthropic.com/en/docs/about-claude/models/all-models",
        models: [
            {
                name: "claude-3-5-haiku-latest",
                description:
                    "Fastest and most cost-effective Claude model. Optimized for quick responses while maintaining high accuracy on common tasks.",
            },
        ],
    },
    {
        provider: "mistral",
        headquarters: "Paris, France",
        description: "Mistral's AI model provider",
        apiReference: "https://docs.mistral.ai/getting-started/models/models_overview/",
        models: [
            {
                name: "ministral-8b-latest",
                description:
                    "Efficient 8B parameter model optimized for edge deployment. Excellent performance-to-size ratio for local inference.",
            },
            {
                name: "mistral-small-latest",
                description:
                    "Compact but powerful model with strong reasoning capabilities. Ideal for production deployments requiring balance of speed and quality.",
            },
        ],
    },
];

function changeProvider() {
    llmModel.value = llmProvider.value.models[0];
}
const llmModel = ref<LLMModel>(llmProviderOptions[0].models[0]);
const llmProvider = ref<LLMProvider>(llmProviderOptions[0]);
const llmModelOptions = computed(() => {
    const provider = llmProviderOptions.find((p) => p.provider === llmProvider.value.provider);
    return provider ? provider.models : [];
});

const editingPrompt = ref<boolean>(false);

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const customizablePrompts = ref<Prompt[]>([
    {
        name: "IMPROVE_EMAIL_DRAFT_PROMPT",
        prompt: "",
        variables: ["language", "agent_settings", "subject", "body", "history", "user_input", "length", "formality"],
    },
    {
        name: "IMPROVE_EMAIL_RESPONSE_PROMPT",
        prompt: `You are Ao, an email assistant, following these agent guidelines: {agent_settings}, who helps a user reply to an {importance} email they received.
The user has already entered the recipients and the subject: '{subject}' of the email.
Improve the email response following the user's guidelines.

Current email body response:
{body}

Current Conversation:
{history}
User: {user_input}

The response must retain the core information and incorporate the required user changes.
If you hesitate or there is contradictory information, always prioritize the last user input.

---
Answer must ONLY be in JSON format with one key: body in HTML.
`,
        variables: ["agent_settings", "importance", "subject", "body", "history", "user_input"],
    },
    {
        name: "CATEGORIZE_AND_SUMMARIZE_EMAIL_PROMPT",
        prompt: `You are a smart email assistant acting as if you were a secretary, summarizing an email for the recipient orally.
    
Given the following email:

Sender:
{sender}

Subject:
{subject}

Text:
{decoded_data}

User description:
{user_description}

Using the provided categories:

Topic Categories:
{category_dict}

Response Categories:
{response_list}

Relevance Categories:
{relevance_list}

Follow those rules:
"important" emails: {important_guidelines}
"informative" emails: {informative_guidelines}
"useless" emails: {useless_guidelines}

Complete the following tasks in same language used in the email:
- Categorize the email according to the user description (if provided) and given categories.
- Summarize the email without adding any greetings.
- If the email explicitly mentions the name of the user (provided with user description), then use 'You' instead of the name of the user.
- Provide a short sentence (up to 10 words) summarizing the core content of the email.
- Define the importance level of the email with one keyword: "important", "informative" or "useless".
- If the email appears to be a response or a conversation, summarize only the last email and IGNORE the previous ones.
- The summary should objectively reflect the most important information of the email without making subjective judgments.    

---
Return this JSON object completed with the requested information:
{{
    "topic": Selected Category,
    "response": Response,
    "relevance": Relevance,
    "importance": Importance of the email,
    "flags": {{
        "spam": bool,
        "scam": bool,
        "newsletter": bool,
        "notification": bool,
        "meeting": bool
    }},
    "summary": {{
        "one_line": One sentence summary,
        "short": Short summary of the email
    }}
}}`,
        variables: [
            "sender",
            "subject",
            "decoded_data",
            "user_description",
            "category_dict",
            "response_list",
            "relevance_list",
            "important_guidelines",
            "informative_guidelines",
            "useless_guidelines",
        ],
    },
    {
        name: "GENERATE_EMAIL_RESPONSE_PROMPT",
        prompt: `As a smart email assistant, following these agent guidelines: {agent_settings}, and based on the email with the subject: '{input_subject}' and body: '{input_body}'.
Craft a response strictly in the language used in the email following the user instruction: '{user_instruction}'.
0. Pay attention if the email appears to be a conversation. You MUST only reply to the last email and do NOT summarize the conversation at all.
1. Ensure the response is structured as an HTML email. Make sure to create a brief response that is straight to the point unless a contradictory guideline is explicitly mentioned by the user.
2. Respect the tone employed in the subject and body, as well as the relationship and respectful markers between recipients.
{signature_instruction}

---
Answer must ONLY be in JSON format with one key: body in HTML.
`,
        variables: ["agent_settings", "input_subject", "input_body", "user_instruction", "signature_instruction"],
    },
    {
        name: "GENERATE_EMAIL_PROMPT",
        prompt: `As an email assistant, following these agent guidelines: {agent_settings}, write a {length} and {formality} email in {language}.
Improve the QUANTITY and QUALITY in {language} according to the user guideline: '{input_data}'.
It must strictly contain only the information that is present in the input.
{signature_instruction}

---
Answer must ONLY be in JSON format with two keys: subject (STRING) and body in HTML format without spaces and unusual line breaks.
`,
        variables: ["agent_settings", "length", "formality", "language", "input_data", "signature_instruction"],
    },
    {
        name: "GENERATE_RESPONSE_KEYWORDS_PROMPT",
        prompt: `As an email assistant, analyze the email with the subject: '{input_subject}' and body: '{input_email}'.

IDENTIFY exactly 5 distinct ways to respond. For each scenario:
**Provide "keywords":** a list of short phrases (fragments) describing the approach. These should **not form complete sentences** but should contain multiple words to effectively convey the strategy. Ensure that the keywords are **in the same language** as the original email. For example:
- "can't attend 5pm, need new schedule, request confirmation"
- "appreciate feedback, will implement changes, thank you"

---
Answer must always be a Json format matching this template:
{{
    "keywords_list": [Python list]
}}
`,
        variables: ["input_subject", "input_email"],
    },
]);

const defaultPrompts = ref<Prompt[]>([
    {
        name: "IMPROVE_EMAIL_DRAFT_PROMPT",
        prompt: `You are an email assistant, who helps a user redact an email in {language}, following these agent guidelines: {agent_settings}.
The user has already entered the recipients and the subject: '{subject}' of the email.
Improve the email body and subject following the user's guidelines.

Current email body:
{body}

Current Conversation:
{history}
User: {user_input}

The response must retain the core information and incorporate the required user changes.
If you hesitate or there is contradictory information, always prioritize the last user input.
Keep the same email body length: '{length}' AND level of speech: '{formality}' unless a change is explicitly mentioned by the user.

---
Answer must ONLY be in JSON format with two keys: subject (STRING) and body in HTML format without spaces and unusual line breaks.
`,
        variables: ["language", "agent_settings", "body", "history", "user_input", "length", "formality"],
    },
]);

const prompt = ref(defaultPrompts.value[0].prompt);

function resetToDefault() {
    prompt.value = defaultPrompts.value[0].prompt;
}

function savePrompt() {
    if (!editingPrompt.value) {
        displayPopup?.("error", "No prompt selected", "No prompt selected");
        return;
    }

    const promptData = defaultPrompts.value[0];
    const missingVariables = promptData.variables.filter((variable) => !prompt.value.includes(`{${variable}}`));

    if (missingVariables.length > 0) {
        displayPopup?.(
            "error",
            "Missing required variables",
            `Missing required variables: ${missingVariables.join(", ")}`
        );
        return;
    }

    // TODO: Implement actual saving logic here
    displayPopup?.("success", "Prompt saved successfully!", "Prompt saved successfully!");
}

onMounted(() => {
    document.addEventListener("keydown", (event) => {
        if (event.ctrlKey && event.key === "s") {
            event.preventDefault();

            if (editingPrompt.value) {
                savePrompt();
            }
        }
    });
});
</script>
