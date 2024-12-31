<template>
    <div class="flex-1 p-4 bg-white">
        <div v-for="(message, index) in messages" :key="index" class="mb-4">
            <div :class="['p-2 rounded-md', message.isUser ? 'bg-blue-500 text-white' : 'bg-gray-300']">
                <p>{{ message.text }}</p>
            </div>
        </div>
        <chat-input @response="handleUserResponse" />
    </div>
</template>

<script setup lang="ts">
import { inject, onMounted, Ref, ref } from "vue";
import ChatInput from "./ChatInput.vue";
import { Category, EmailLinked } from "@/global/types";
import { postData, getData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";

const categories = inject("categories") as Ref<Category[]>;
const emailsLinked = inject("emailsLinked") as Ref<EmailLinked[]>;
const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const messages = ref([{ text: "Hello and welcome to the custom email categorization feature", isUser: false }]);

const displayUserMsg = (message: string) => {
    messages.value.push({ text: message, isUser: true });
};

const displayAIMsg = (message: string) => {
    messages.value.push({ text: message, isUser: false });
};

// Declare `userInputResolver` as a Ref that can hold a function or null
const userInputResolver = ref<((value: string) => void) | null>(null);

async function waitForUserInput() {
    return new Promise((resolve) => {
        userInputResolver.value = resolve; // Store the resolve function
    });
}

const handleUserResponse = (response: string) => {
    displayUserMsg(response);
    if (userInputResolver.value) {
        userInputResolver.value(response); // Resolve the promise with user input
        userInputResolver.value = null; // Reset the resolver
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
                    `Please provide a description for this email: ${emailLinked.email}.
  It should be a short sentence describing yourself using the third person. Here are some good examples:
  - 'Augustin ROLET is a student at ESAIP (Engineering School specialized in Computer Science),
  - Augustin ROLET is an Integration Development Intern at CDS (Cognitive Design Systems is a company that creates software for 3D printing).'`
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
                    displayAIMsg("The description provided is not valid");
                    displayAIMsg(validationResult.data.feedback);
                }
            }
        } else {
            const validationResult = await postData(`user/social_api/review_user_description/`, { description });
            let valid = validationResult.data.valid;

            if (!valid) {
                displayAIMsg("The description provided is not valid");
                displayAIMsg(validationResult.data.feedback);

                while (!valid) {
                    displayAIMsg(
                        `Please provide a description for this email: ${emailLinked.email}.
  It should be a short sentence describing yourself using the third person. Here are some good examples:
  - 'Augustin ROLET is a student at ESAIP (Engineering School specialized in Computer Science),
  - Augustin ROLET is an Integration Development Intern at CDS (Cognitive Design Systems is a company that creates software for 3D printing).'`
                    );

                    const userInput = await waitForUserInput();
                    description = userInput;

                    const validationResult = await postData(`user/social_api/review_user_description/`, {
                        description,
                    });

                    if (validationResult.data.valid) {
                        valid = true;
                        await postData(`user/social_api/update_user_description/`, {
                            userDescription: description,
                            email: emailLinked.email,
                        });
                    } else {
                        displayAIMsg("The description provided is not valid");
                        displayAIMsg(validationResult.data.feedback);
                    }
                }
            }
        }
    }
}

onMounted(async () => {
    await fetchEmailsLinked();
    await fetchCategories();

    if (categories.value.length === 1) {
        userDescriptionWorkflow();
        displayAIMsg("You currently have no categories. I can help you create some.");
        displayAIMsg(
            "Please list some common topics you would like to categorize your emails into. For each topic, provide a description and examples of emails that would fall into that category."
        );

        let userInput = await waitForUserInput();
        let aiGeneratedCategories = await generateCategoriesScratch(userInput as any);
        validateCategories(aiGeneratedCategories);
    } else {
        displayAIMsg("Do you like your current email categorization");
        const userInput = await waitForUserInput();

        // todo: replace with clean buttons
        if (userInput === "yes") {
            // user likes its email categorization, no need to change anything. User can close the page
        } else if (userInput === "no") {
            userDescriptionWorkflow();
            displayAIMsg(
                "Please list some common topics you would like to categorize your emails into. For each topic, provide a description and examples of emails that would fall into that category."
            );

            let userInput = await waitForUserInput();
            let aiGeneratedCategories = await generateCategoriesScratch(userInput as any);
            validateCategories(aiGeneratedCategories);
        } else if (userInput === "bof") {
            userDescriptionWorkflow();

            // in this case we first need to get Ai feedback and Then wxe can ask user input
            let aiGeneratedCategories = await generateCategoriesScratch(
                categories.value.filter((category) => {
                    category.name != "Others";
                }) as any
            );
            // todo: display the categories as a table
            displayAIMsg(`Categories: ${JSON.stringify(aiGeneratedCategories.categories)}`);

            let userInput = await waitForUserInput();
            aiGeneratedCategories = await generateCategoriesScratch(userInput as any);
            validateCategories(aiGeneratedCategories);
        }
    }
});

async function generateCategoriesScratch(userTopics: string) {
    const result = await postData("user/generate_categories_scratch/", { userTopics: userTopics });
    return result.data.categories;
}

async function validateCategories(aiGeneratedCategories: any) {
    let userSatisfaction = false;
    while (!userSatisfaction) {
        displayAIMsg("Please review the categories, do you want to keep them?");
        // todo: display the categories as a table
        displayAIMsg(`Categories: ${JSON.stringify(aiGeneratedCategories.categories)}`);

        const userInput = await waitForUserInput();

        if (userInput === "yes") {
            userSatisfaction = true;
            displayAIMsg("Great!");
            displayAIMsg("Email prioritization workflow implementation coming soon!");
        } else if (userInput === "no") {
            displayAIMsg(
                "Please list some common topics you would like to categorize your emails into. For each topic, provide a description and examples of emails that would fall into that category."
            );
            const userInputTopics = waitForUserInput();
            aiGeneratedCategories = await generateCategoriesScratch(userInputTopics as any);
        } else if (userInput === "bof") {
            displayAIMsg("OK, let's improve them. Please improve them according to my feedback.");
            displayAIMsg(`AI feedback: ${JSON.stringify(aiGeneratedCategories)}`);
            const userInputTopics = waitForUserInput();
            aiGeneratedCategories = await generateCategoriesScratch(userInputTopics as any);
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
