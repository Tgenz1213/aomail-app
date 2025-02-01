<template>
    <div class="flex-1 p-4 flex flex-col relative">
        <div class="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200">
            <div v-for="(message, index) in messages" :key="index" class="mb-4">
                <ChatBubble :message="message.textHtml" :isUser="message.isUser" />
                <div v-if="message.buttonOptions" class="flex flex-col items-center">
                    <div class="flex-row space-x-5">
                        <button
                            v-for="(option, idx) in message.buttonOptions"
                            :key="idx"
                            @click="handleButtonClick(option, index)"
                            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none"
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
const displayUserMsg = inject<(message: string) => void>("displayUserMsg")!;
const waitForUserInput = inject<() => Promise<string>>("waitForUserInput")!;

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
            displayAIMsg(
                "Are you satisfied with the way I prioritize your emails according to their importance? Do I often assign the wrong level of importance to your emails?",
                [
                    { key: "yes", value: "Yes" },
                    { key: "no", value: "No" },
                ]
            );
            currentStep.value = "prioritization";
            break;
        }
        case "no": {
            await userDescriptionWorkflow();
            displayAIMsg(
                "Please list some common topics you would like to categorize your emails into. For each topic, provide a description and examples of emails that would fall into that category."
            );
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
            displayAIMsg("Great! Categories have been updated.");
            displayAIMsg(
                "Are you satisfied with the way I prioritize your emails according to their importance? Do I often assign the wrong level of importance to your emails?",
                [
                    { key: "yes", value: "Yes" },
                    { key: "no", value: "No" },
                ]
            );
            currentStep.value = "prioritization";
            break;
        }
        case "no": {
            displayAIMsg(
                "Please list some common topics you would like to categorize your emails into. For each topic, provide a description and examples of emails that would fall into that category."
            );
            const userInputTopics = await waitForUserInput();
            aiGeneratedCategories = await generateCategoriesScratch(userInputTopics);
            categoriesReview(aiGeneratedCategories);
            break;
        }
        case "soso": {
            displayAIMsg("OK, let's improve them. Please improve them according to my feedback.");
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
            displayAIMsg("Happy to hear that! Your email categorization is optimized. You can close this window");
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
                displayAIMsg("Prioritization guidelines updated successfully!");
            } else {
                displayAIMsg(result.error as string);
            }
            break;
        }
        case "no": {
            displayAIMsg("Got it! Let's improve your email prioritization together.");
            displayAIMsg(
                "What types of emails annoy you? How would you describe important emails? Please describe your own preferences in your response."
            );
            displayAIMsg(
                "For example: Meetings and project-related emails for the AlphaPen site redesign are <strong>important</strong>. Marketing or auto-acknowledgement emails are <strong>useless</strong>. The rest is <strong>informative</strong>."
            );
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
                    <th scope="col" class="px-6 py-3">Priority</th>
                    <th scope="col" class="px-6 py-3">Description</th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                    <td class="px-6 py-4">Important</td>
                    <td class="px-6 py-4">${result.data.important}</td>
                </tr>
                <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                    <td class="px-6 py-4">Informative</td>
                    <td class="px-6 py-4">${result.data.informative}</td>
                </tr>
                <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                    <td class="px-6 py-4">Useless</td>
                    <td class="px-6 py-4">${result.data.useless}</td>
                </tr>
            </tbody>
        </table>`
    );
    displayAIMsg("Are you satisfied with my proposition of email prioritization?", [
        { key: "yes", value: "Yes" },
        { key: "no", value: "No" },
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
                    `Please provide a description for this email: ${emailLinked.email}. It should be a short sentence.`
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
                    displayAIMsg("I have updated your description to help me better categorize your emails.");
                } else {
                    displayAIMsg("The description is not valid, Improve it according to my feedback:");
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
        displayAIMsg("You currently have no categories. I can help you create some.");
        displayAIMsg("Please list some topics to categorize your emails.");
        const userInput = await waitForUserInput();
        const aiGeneratedCategories = await generateCategoriesScratch(userInput);
        categoriesReview(aiGeneratedCategories);
    } else {
        waitForButtonClick.value = true;
        displayAIMsg("Do you like your current email categorization?", [
            { key: "yes", value: "Yes" },
            { key: "no", value: "No" },
            { key: "soso", value: "Needs Improvement" },
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
                    <th scope="col" class="px-6 py-3">Name</th>
                    <th scope="col" class="px-6 py-3">Description</th>
                    <th scope="col" class="px-6 py-3">Feedback</th>
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
    displayAIMsg("Please review the categories, do you want to keep them?", [
        { key: "yes", value: "Yes" },
        { key: "no", value: "No" },
        { key: "soso", value: "Needs Improvement" },
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
