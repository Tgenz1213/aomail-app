<template>
    <div class="flex-1 p-4 bg-white">
        <div v-for="(message, index) in messages" :key="index" class="mb-4">
            <ChatBubble :message="message.textHtml" :isUser="message.isUser" />
            <div v-if="message.buttonOptions" class="flex flex-col items-center">
                <div class="flex-row space-x-5">
                    <button
                        v-for="(option, idx) in message.buttonOptions"
                        :key="idx"
                        @click="handleButtonClick(option)"
                        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none"
                    >
                        {{ option }}
                    </button>
                </div>
            </div>
        </div>
        <ChatInput @response="handleUserResponse" />
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, Ref, ref } from "vue";
import ChatInput from "./ChatInput.vue";
import ChatBubble from "./ChatBubble.vue";
import { Category, EmailLinked } from "@/global/types";
import { postData, getData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";

const categories = inject("categories") as Ref<Category[]>;
const emailsLinked = inject("emailsLinked") as Ref<EmailLinked[]>;
const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

type Message = {
    textHtml: string;
    isUser: boolean;
    buttonOptions?: string[];
};

const messages = ref<Message[]>([
    {
        textHtml: "Hello and welcome to the custom email categorization feature",
        isUser: false,
        buttonOptions: ["Yes", "No", "Bof"],
    },
]);

const displayUserMsg = (message: string) => {
    messages.value.push({ textHtml: message, isUser: true });
};

const displayAIMsg = (message: string, options: string[] | undefined = undefined) => {
    messages.value.push({
        textHtml: message,
        isUser: false,
        buttonOptions: options,
    });
};

const handleUserResponse = (response: string) => {
    displayUserMsg(response);
    if (userInputResolver.value) {
        userInputResolver.value(response);
        userInputResolver.value = null;
    }
};

const handleButtonClick = async (option: string) => {
    displayUserMsg(option);
    switch (option.toLowerCase()) {
        case "yes":
            displayAIMsg("Great! No changes will be made.");
            break;
        case "no":
            await userDescriptionWorkflow();
            displayAIMsg(
                "Please list some common topics you would like to categorize your emails into. For each topic, provide a description and examples of emails that would fall into that category."
            );
            const userInput = await waitForUserInput();
            let aiGeneratedCategories = await generateCategoriesScratch(userInput as any);
            validateCategories(aiGeneratedCategories);
            break;
        case "bof":
            await userDescriptionWorkflow();
            let aiFeedback = await generateCategoriesScratch(
                JSON.stringify(categories.value.filter((category) => category.name != "Others"))
            );
            displayAIMsg(`AI feedback: ${JSON.stringify(aiFeedback)}`, ["Yes", "No", "Bof"]);
            break;
        default:
            displayAIMsg("Invalid input. Please choose again.");
    }
};

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
                } else {
                    displayAIMsg("The description is not valid");
                    displayAIMsg(validationResult.data.feedback);
                }
            }
        }
    }
}

const userInputResolver = ref<((value: string) => void) | null>(null);

async function waitForUserInput() {
    return new Promise((resolve) => {
        userInputResolver.value = resolve;
    });
}

onMounted(async () => {
    await fetchEmailsLinked();
    await fetchCategories();

    if (categories.value.length === 1) {
        userDescriptionWorkflow();
        displayAIMsg("You currently have no categories. I can help you create some.");
        displayAIMsg("Please list some topics to categorize your emails.");
        let userInput = await waitForUserInput();
        let aiGeneratedCategories = await generateCategoriesScratch(userInput as any);
        validateCategories(aiGeneratedCategories);
    } else {
        displayAIMsg("Do you like your current email categorization?", ["Yes", "No", "Bof"]);
    }
});

async function generateCategoriesScratch(userTopics: string): Promise<Category[]> {
    const result = await postData("user/generate_categories_scratch/", { userTopics: userTopics });
    return result.data.categories;
}

async function validateCategories(aiGeneratedCategories: any) {
    let userSatisfaction = false;
    while (!userSatisfaction) {
        displayAIMsg("Please review the categories, do you want to keep them?", ["Yes", "No", "Bof"]);

        const userInput = await waitForUserInput();

        if (userInput === "yes") {
            userSatisfaction = true;
            displayAIMsg("Great! Categories have been updated.");
        } else if (userInput === "no") {
            displayAIMsg("Please provide common topics for categorization.");
            const userInputTopics = await waitForUserInput();
            aiGeneratedCategories = await generateCategoriesScratch(userInputTopics as any);
        } else if (userInput === "bof") {
            displayAIMsg("I'll improve them according to your feedback.");
            const feedback = await waitForUserInput();
            aiGeneratedCategories = await generateCategoriesScratch(feedback as any);
        } else {
            displayAIMsg("Invalid input. Please enter 'yes', 'no', or 'bof'.");
        }
    }
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

    categories.value = result.data;
}
</script>
