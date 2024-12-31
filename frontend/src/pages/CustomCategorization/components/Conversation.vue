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
        displayAIMsg("user categorization workflow under development")
    } else {
        displayAIMsg("Do you like your current email categorization");
        const userInput = await waitForUserInput();

        // todo: replace with clean buttons
        if (userInput === "yes") {
            // starts user categorization workflow
            displayAIMsg("user categorization workflow under development")
        } else if (userInput === "no") {
            userDescriptionWorkflow();
        } else if (userInput === "bof") {
            userDescriptionWorkflow();
        }
    }
});

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
