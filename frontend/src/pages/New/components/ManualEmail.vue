<template>
    <div class="flex flex-col h-full w-full">
        <div class="flex items-center h-[65px] justify-center lg:py-5 2xl:h-[80px] min-h-8">
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
                        d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672ZM12 2.25V4.5m5.834.166-1.591 1.591M20.25 10.5H18M7.757 14.743l-1.59 1.59M6 10.5H3.75m4.007-4.243-1.59-1.59"
                    />
                </svg>
                <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500">
                    {{ $t("constants.userActions.enterManually") }}
                </h1>
            </div>
        </div>
        <form class="flex-1 flex flex-col w-full px-10 pt-4 2xl:px-14 2xl:pt-6 overflow-hidden">
            <div class="flex flex-col space-y-5 h-full w-full">
                <div class="">
                    <RecipientsSection />
                </div>
                <div class="">
                    <SubjectAttachmentsSection />
                </div>
                <div class="flex flex-col h-full space-y-5 pb-4 2xl:pb-6 overflow-hidden">
                    <div class="flex-1 overflow-hidden h-screen border-b-2 rounded-lg">
                        <div id="editor-container" class="flex-1 h-full w-full flex flex-col border-solid">
                            <div id="editor" class="flex-1"></div>
                        </div>
                    </div>
                    <div class="flex gap-x-2 mb-5 2xl:gap-3 2xl:mb-6 items-stretch">
                        <div class="relative flex-grow flex items-stretch">
                            <Listbox as="div" v-model="emailSelected" class="w-full flex flex-col">
                                <ListboxButton
                                    class="relative w-full h-full cursor-default rounded-md bg-white px-6 py-2 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6 2xl:px-7 2xl:py-3 2xl:text-base"
                                >
                                    <span class="block truncate">{{ emailSelected }}</span>
                                    <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                                    </span>
                                </ListboxButton>
                                <transition
                                    leave-active-class="transition ease-in duration-100"
                                    leave-from-class="opacity-100"
                                    leave-to-class="opacity-0"
                                >
                                    <ListboxOptions
                                        class="absolute z-10 mb-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm bottom-full"
                                    >
                                        <ListboxOption
                                            as="template"
                                            v-for="email in emailsLinked"
                                            :key="email.email"
                                            :value="email.email"
                                            v-slot="{ active, selected }"
                                        >
                                            <li
                                                :class="[
                                                    active ? 'bg-gray-800 text-white' : 'text-gray-900',
                                                    'relative cursor-default select-none py-2 pl-3 pr-9',
                                                ]"
                                            >
                                                <span
                                                    :class="[
                                                        selected ? 'font-semibold' : 'font-normal',
                                                        'block truncate',
                                                    ]"
                                                >
                                                    {{ email.email }}
                                                </span>
                                                <span
                                                    v-if="selected"
                                                    :class="[
                                                        active ? 'text-white' : 'text-gray-500',
                                                        'absolute inset-y-0 right-0 flex items-center pr-4',
                                                    ]"
                                                >
                                                    <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                                </span>
                                            </li>
                                        </ListboxOption>
                                    </ListboxOptions>
                                </transition>
                            </Listbox>
                        </div>
                        <SendEmailButtons />
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">
import { MICROSOFT } from "@/global/const";
import { postData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import { Recipient, EmailLinked, UploadedFile } from "@/global/types";
import Quill from "quill";
import { computed, inject, provide, ref, Ref } from "vue";
import SendEmailButtons from "./SendEmailButtons.vue";
import { Menu, MenuButton, MenuItems } from "@headlessui/vue";
import {
    Combobox,
    ComboboxButton,
    ComboboxInput,
    ComboboxOption,
    Listbox,
    ListboxButton,
    ListboxOptions,
    ListboxOption,
    ComboboxOptions,
} from "@headlessui/vue";
import { ChevronUpDownIcon } from "@heroicons/vue/24/outline";
import SubjectAttachmentsSection from "./SubjectAttachmentsSection.vue";
import RecipientsSection from "./RecipientsSection.vue";

const isFocused = ref(false);
const inputValue = ref("");
const emailsLinked = inject<Ref<EmailLinked[]>>("emailsLinked", ref([]));
const emailSelected = inject<Ref<string>>("emailSelected") || ref("");
const selectedPeople = inject<Ref<Recipient[]>>("selectedPeople") || ref([]);
const selectedCC = inject<Ref<Recipient[]>>("selectedCC") || ref([]);
const selectedCCI = inject<Ref<Recipient[]>>("selectedCCI") || ref([]);
const quill = inject<Ref<Quill | null>>("quill");
const stepContainer = inject<Ref<number>>("stepContainer") || ref(0);
const fileObjects = ref<File[]>([]);

provide("inputValue", inputValue);
provide("fileObjects", fileObjects);

// todo: trigger each time an email is selected
// function setEmailSelected() {
//     localStorage.setItem("email", emailSelected.value);
// }
</script>
