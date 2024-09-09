<template>
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
                        @click="setEmailSelected"
                    >
                        <li
                            :class="[
                                active ? 'bg-gray-800 text-white' : 'text-gray-900',
                                'relative cursor-default select-none py-2 pl-3 pr-9',
                            ]"
                        >
                            <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
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
</template>

<script setup lang="ts">
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue";
import { ChevronUpDownIcon } from "@heroicons/vue/24/outline";
import { EmailLinked } from "@/global/types";
import { inject, Ref, ref } from "vue";

const emailSelected = inject<Ref<string>>("emailSelected") || ref("");
const emailsLinked = inject<Ref<EmailLinked[]>>("emailsLinked", ref([]));

function setEmailSelected() {
    localStorage.setItem("email", emailSelected.value);
}
</script>
