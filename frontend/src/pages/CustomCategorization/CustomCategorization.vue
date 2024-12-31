<template>
    <Menu as="div">
        <div>
            <MenuButton
                class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
            >
                {{ llm.name }}
                <ChevronDownIcon class="-mr-1 size-5 text-gray-400" aria-hidden="true" />
            </MenuButton>
        </div>

        <transition
            enter-active-class="transition ease-out duration-100"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
        >
            <MenuItems
                class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black/5 focus:outline-none"
            >
                <MenuItem v-for="(key, index) in LLM_MODEL_CHOICES" :key="index" v-slot="{ active }">
                    <button
                        @click="() => (llm = key)"
                        :class="[
                            active ? 'bg-gray-100 text-gray-900 outline-none' : 'text-gray-700',
                            'block px-4 py-2 text-sm',
                        ]"
                    >
                        {{ llm }}
                    </button>
                </MenuItem>
            </MenuItems>
        </transition>
    </Menu>
    <div class="flex h-screen">
        <Conversation />
        <History />
    </div>
</template>

<script setup lang="ts">
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import { Category, EmailLinked } from "@/global/types";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import { ChevronDownIcon } from "@heroicons/vue/20/solid";
import { provide, ref } from "vue";
import History from "./components/History.vue";
import Conversation from "./components/Conversation.vue";

type LLM = {
    name: string;
    model: string;
    provider: string;
    description: string;
};

const LLM_MODEL_CHOICES = ref<LLM[]>([
    {
        name: "Swift Thinker",
        model: "gpt-4o-mini",
        provider: "openai",
        description: "Best reasoning and accuracy for understanding your needs",
    },
    {
        name: "Community Pro",
        model: "llama-3.2",
        provider: "groq",
        description: "Open-source AI, reliable for multilingual setups",
    },
    {
        name: "Lightning AI",
        model: "gemini-1.5-flash",
        provider: "google",
        description: "Super-fast and responsive for everyday tasks",
    },
    {
        name: "Cocorico",
        model: "mistral-small-latest",
        provider: "mistral",
        description: "French open source LLM Research",
    },
]);
const llm = ref<LLM>(LLM_MODEL_CHOICES.value[0]);

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

const userInput = ref("")
const categories = ref<Category[]>([]);
const emailsLinked = ref<EmailLinked[]>([]);
provide("categories", categories);
provide("emailsLinked", emailsLinked);
provide("userInput", userInput);
provide("displayPopup", displayPopup);

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
</script>
