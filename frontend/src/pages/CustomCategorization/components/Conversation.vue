<template>
    <div class="flex-1 p-4 flex flex-col bg-zinc-50 bg-opacity-40 h-full relative">
        <div
            class="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200 mt-8 2xl:mt-12"
        >
            <div v-for="(message, index) in messages" :key="index" class="mb-6">
                <ChatBubble :message="message.textHtml" :isUser="message.isUser" :agentIcon="selectedAgent.icon_name" />
                <div v-if="message.buttonOptions" class="flex flex-col items-center mt-4">
                    <div class="flex-row space-x-5">
                        <button
                            v-for="(option, idx) in message.buttonOptions"
                            :key="idx"
                            @click="handleButtonClick(option, index)"
                            class="px-4 py-2 rounded-md bg-zinc-800 text-sm text-white shadow-sm hover:bg-gray-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                        >
                            {{ option.value }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, Ref, ref } from "vue";
import ChatBubble from "@/global/components/Conversation/ChatBubble.vue";
import { Category, EmailLinked, KeyValuePair, Message } from "@/global/types";
import { postData, getData, putData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import { DEFAULT_CATEGORY } from "@/global/const";
import { createDefaultFilters } from "@/global/filters";
import { Agent } from "@/global/types";

type CategoryByAI = Category & {
    feedback: string;
};

type Guideline = {
    importantGuidelines: string;
    informativeGuidelines: string;
    uselessGuidelines: string;
};

const currentStep = ref<"userDescription" | "categories" | "prioritization">("userDescription");
const currentUserCategories = ref<Category[]>([]);
const categories = ref<Category[]>([]);
const emailsLinked = ref<EmailLinked[]>([]);
const messages = inject("messages") as Ref<Message[]>;
const guidelines = ref<Guideline>({ importantGuidelines: "", informativeGuidelines: "", uselessGuidelines: "" });
const waitForButtonClick = inject("waitForButtonClick") as Ref<boolean>;
const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
// eslint-disable-next-line @typescript-eslint/no-empty-function
const displayUserMsg = inject<(message: string) => void>("displayUserMsg") || ((message: string) => {});
// eslint-disable-next-line @typescript-eslint/no-empty-function
const waitForUserInput = inject<() => Promise<string>>("waitForUserInput") || (() => Promise.resolve(""));
const selectedAgent =
    inject<Ref<Agent>>("selectedAgent") ||
    ref<Agent>({
        id: "",
        agent_name: i18n.global.t("agent.defaultAgent"),
        picture: "/assets/default-agent.png",
        ai_template: "",
        length: "",
        formality: "",
        icon_name: "default-agent.png",
    });

const displayAIMsg = (message: string, options: KeyValuePair[] | undefined = undefined) => {
    messages.value.push({
        textHtml: message,
        isUser: false,
        buttonOptions: options,
    });
};

const handleButtonClick = async (option: KeyValuePair, index: number) => {
    waitForButtonClick.value = false;
    displayUserMsg(option.value);
    // remove the button options after clicking
    messages.value[index].buttonOptions = undefined;

    switch (currentStep.value) {
        case "userDescription":
            await handleUserDescription(option);
            break;
        case "categories":
            await handleCategories(option);
            break;
        case "prioritization":
            await handlePrioritization(option);
            break;
        default:
            console.error("Unexpected step in handleButtonClick:", currentStep.value);
    }
};

const handleUserDescription = async (option: KeyValuePair) => {
    let aiGeneratedCategories;
    switch (option.key) {
        case "yes": {
            displayAIMsg(i18n.global.t("customCategorization.prioritizationQuestion"), [
                { key: "yes", value: i18n.global.t("customCategorization.buttons.yes") },
                { key: "no", value: i18n.global.t("customCategorization.buttons.no") },
            ]);
            currentStep.value = "prioritization";
            break;
        }
        case "no": {
            await userDescriptionWorkflow();
            displayAIMsg(i18n.global.t("customCategorization.listTopicsRequest"));
            const userInput = await waitForUserInput();
            aiGeneratedCategories = await generateCategoriesScratch(userInput);
            categoriesReview(aiGeneratedCategories);
            break;
        }
        case "soso": {
            await userDescriptionWorkflow();
            aiGeneratedCategories = await generateCategoriesScratch(
                JSON.stringify(categories.value.filter((category) => category.name != DEFAULT_CATEGORY))
            );
            categoriesReview(aiGeneratedCategories);
            break;
        }
    }
};

const handleCategories = async (option: KeyValuePair) => {
    let aiGeneratedCategories;
    switch (option.key) {
        case "yes": {
            categories.value.map(async (category) => {
                if (
                    currentUserCategories.value.filter(
                        (currentUserCategory) => currentUserCategory.name === category.name
                    ).length > 0
                ) {
                    await putData(`update_category/`, {
                        newCategoryName: category.name,
                        description: category.description,
                        categoryName: category.name,
                    });
                } else {
                    await postData(`create_categories/`, {
                        categories: [
                            {
                                name: category.name,
                                description: category.description,
                            },
                        ],
                    });

                    await createDefaultFilters(category.name);
                }
            });
            displayAIMsg(i18n.global.t("customCategorization.categoriesUpdated"));
            displayAIMsg(i18n.global.t("customCategorization.prioritizationQuestion"), [
                { key: "yes", value: i18n.global.t("customCategorization.buttons.yes") },
                { key: "no", value: i18n.global.t("customCategorization.buttons.no") },
            ]);
            currentStep.value = "prioritization";
            break;
        }
        case "no": {
            displayAIMsg(i18n.global.t("customCategorization.listTopicsRequest"));
            const userInputTopics = await waitForUserInput();
            aiGeneratedCategories = await generateCategoriesScratch(userInputTopics);
            categoriesReview(aiGeneratedCategories);
            break;
        }
        case "soso": {
            displayAIMsg(i18n.global.t("customCategorization.improveCategories"));
            const feedback = await waitForUserInput();
            aiGeneratedCategories = await generateCategoriesScratch(feedback, messages.value);
            categoriesReview(aiGeneratedCategories);
            break;
        }
    }
};

const handlePrioritization = async (option: KeyValuePair) => {
    switch (option.key) {
        case "yes": {
            displayAIMsg(i18n.global.t("customCategorization.optimizationComplete"));
            let payload: Guideline = { importantGuidelines: "", informativeGuidelines: "", uselessGuidelines: "" };
            if (guidelines.value.importantGuidelines) {
                payload.importantGuidelines = guidelines.value.importantGuidelines;
            }
            if (guidelines.value.informativeGuidelines) {
                payload.informativeGuidelines = guidelines.value.informativeGuidelines;
            }
            if (guidelines.value.uselessGuidelines) {
                payload.uselessGuidelines = guidelines.value.uselessGuidelines;
            }

            const result = await postData("user/preferences/prioritization/", payload);

            if (result.success) {
                displayAIMsg(i18n.global.t("customCategorization.prioritizationUpdated"));
            } else {
                displayAIMsg(result.error as string);
            }
            break;
        }
        case "no": {
            displayAIMsg(i18n.global.t("customCategorization.improvePrioritization"));
            displayAIMsg(i18n.global.t("customCategorization.prioritizationExample"));
            displayAIMsg(i18n.global.t("customCategorization.prioritizationExampleDetails"));
            prioritizationReview();
            break;
        }
    }
};

async function prioritizationReview() {
    const userInput = await waitForUserInput();
    const result = await postData("user/generate_prioritization_scratch/", {
        userInput: userInput,
    });
    guidelines.value.importantGuidelines = result.data.important;
    guidelines.value.informativeGuidelines = result.data.informative;
    guidelines.value.uselessGuidelines = result.data.useless;

    displayAIMsg(
        `<table class="rounded text-left border border-separate border-tools-table-outline border-black border-1">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">${i18n.global.t("customCategorization.table.priority")}</th>
                    <th scope="col" class="px-6 py-3">${i18n.global.t("customCategorization.table.description")}</th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                    <td class="px-6 py-4">${i18n.global.t("constants.ruleModalConstants.important")}</td>
                    <td class="px-6 py-4">${result.data.important}</td>
                </tr>
                <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                    <td class="px-6 py-4">${i18n.global.t("constants.ruleModalConstants.informative")}</td>
                    <td class="px-6 py-4">${result.data.informative}</td>
                </tr>
                <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                    <td class="px-6 py-4">${i18n.global.t("constants.ruleModalConstants.useless")}</td>
                    <td class="px-6 py-4">${result.data.useless}</td>
                </tr>
            </tbody>
        </table>`
    );
    displayAIMsg(i18n.global.t("customCategorization.reviewCategories"), [
        { key: "yes", value: i18n.global.t("customCategorization.buttons.yes") },
        { key: "no", value: i18n.global.t("customCategorization.buttons.no") },
    ]);
}

async function userDescriptionWorkflow() {
    for (const emailLinked of emailsLinked.value) {
        const result = await postData(`user/social_api/get_user_description/`, { email: emailLinked.email });
        let description = result.data.description;

        if (!description) {
            let valid = false;

            while (!valid) {
                displayAIMsg(
                    i18n.global.t("customCategorization.emailDescriptionRequest", { email: emailLinked.email })
                );

                const userInput = await waitForUserInput();
                description = userInput;

                const validationResult = await postData(`user/social_api/review_user_description/`, { description });

                if (validationResult.data.valid) {
                    valid = true;
                    await postData(`user/social_api/update_user_description/`, {
                        userDescription: description,
                        email: emailLinked.email,
                    });
                    displayAIMsg(i18n.global.t("customCategorization.descriptionUpdated"));
                } else {
                    displayAIMsg(i18n.global.t("customCategorization.descriptionInvalid"));
                    displayAIMsg(validationResult.data.feedback);
                }
            }
        }
    }
    currentStep.value = "categories";
}

onMounted(async () => {
    await fetchEmailsLinked();
    await fetchCategories();

    await customCategorizationWorkflow();
});

async function customCategorizationWorkflow() {
    // No categories have been created (only Others as default)
    if (categories.value.length === 1) {
        await userDescriptionWorkflow();
        displayAIMsg(i18n.global.t("customCategorization.noCategories"));
        displayAIMsg(i18n.global.t("customCategorization.listTopics"));
        const userInput = await waitForUserInput();
        const aiGeneratedCategories = await generateCategoriesScratch(userInput);
        categoriesReview(aiGeneratedCategories);
    } else {
        waitForButtonClick.value = true;
        displayAIMsg(i18n.global.t("customCategorization.currentCategorization"), [
            { key: "yes", value: i18n.global.t("customCategorization.buttons.yes") },
            { key: "no", value: i18n.global.t("customCategorization.buttons.no") },
            { key: "soso", value: i18n.global.t("customCategorization.buttons.needsImprovement") },
        ]);
    }
}

async function generateCategoriesScratch(
    userTopics: string,
    chatHistory: Message[] | undefined = undefined
): Promise<CategoryByAI[]> {
    const result = await postData("user/generate_categories_scratch/", {
        userTopics: userTopics,
        chatHistory: chatHistory,
    });
    // update categories locally in case User had None when starting
    categories.value = [
        ...categories.value.filter((category) => category.name !== DEFAULT_CATEGORY),
        ...result.data.categories.map((category: Category) => ({
            name: category.name,
            description: category.description,
        })),
    ];
    return result.data.categories;
}

async function categoriesReview(aiGeneratedCategories: CategoryByAI[]) {
    displayAIMsg(
        `<table class="rounded text-left border border-separate border-tools-table-outline border-black border-1">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">${i18n.global.t("customCategorization.table.name")}</th>
                    <th scope="col" class="px-6 py-3">${i18n.global.t("customCategorization.table.description")}</th>
                    <th scope="col" class="px-6 py-3">${i18n.global.t("customCategorization.table.feedback")}</th>
                </tr>
            </thead>
            <tbody>${aiGeneratedCategories
                .map(
                    (category) =>
                        `<tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                            <td class="px-6 py-4">${category.name}</td>
                            <td class="px-6 py-4">${category.description}</td>
                            <td class="px-6 py-4">${category.feedback}</td>
                        </tr>`
                )
                .join("")}
            </tbody>
        </table>`
    );
    waitForButtonClick.value = true;
    displayAIMsg(i18n.global.t("customCategorization.reviewCategories"), [
        { key: "yes", value: i18n.global.t("customCategorization.buttons.yes") },
        { key: "no", value: i18n.global.t("customCategorization.buttons.no") },
        { key: "soso", value: i18n.global.t("customCategorization.buttons.needsImprovement") },
    ]);
}

async function fetchEmailsLinked() {
    const result = await getData(`user/emails_linked/`);

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailLinkedFetchError"),
            result.error as string
        );
        return;
    }

    emailsLinked.value = result.data;
}

async function fetchCategories() {
    const result = await getData("user/categories/");
    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("rulesPage.popUpConstants.errorMessages.failedToFetchCategories"),
            result.error as string
        );
        return;
    }
    currentUserCategories.value = result.data;
    categories.value = result.data;
}
</script>
