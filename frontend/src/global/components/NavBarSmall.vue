<template>
    <div class="h-full">
        <TransitionRoot as="template" :show="sidebarOpen">
            <Dialog as="div" class="relative z-50 lg:hidden" @close="sidebarOpen = false">
                <TransitionChild
                    as="template"
                    enter="transition-opacity ease-linear duration-300"
                    enter-from="opacity-0"
                    enter-to="opacity-100"
                    leave="transition-opacity ease-linear duration-300"
                    leave-from="opacity-100"
                    leave-to="opacity-0"
                >
                    <div class="fixed inset-0 bg-gray-900/80" />
                </TransitionChild>

                <div class="fixed inset-0 flex">
                    <TransitionChild
                        as="template"
                        enter="transition ease-in-out duration-300 transform"
                        enter-from="-translate-x-full"
                        enter-to="translate-x-0"
                        leave="transition ease-in-out duration-300 transform"
                        leave-from="translate-x-0"
                        leave-to="-translate-x-full"
                    >
                        <DialogPanel class="relative mr-16 flex w-full max-w-xs flex-1">
                            <TransitionChild
                                as="template"
                                enter="ease-in-out duration-300"
                                enter-from="opacity-0"
                                enter-to="opacity-100"
                                leave="ease-in-out duration-300"
                                leave-from="opacity-100"
                                leave-to="opacity-0"
                            >
                                <div class="absolute left-full top-0 flex w-16 justify-center pt-5">
                                    <button type="button" class="-m-2.5 p-2.5" @click="sidebarOpen = false">
                                        <span class="sr-only">Close sidebar</span>
                                        <XMarkIcon class="h-6 w-6 text-white" aria-hidden="true" />
                                    </button>
                                </div>
                            </TransitionChild>

                            <div
                                class="flex grow flex-col gap-y-5 overflow-y-auto bg-indigo-500 px-6 pb-2 ring-1 ring-white/10"
                            >
                                <div class="flex h-16 shrink-0 items-center">
                                    <img
                                        class="h-8 w-auto"
                                        src="https://tailwindui.com/img/logos/mark.svg?color=white"
                                        alt="Your Company"
                                    />
                                </div>
                                <nav class="flex flex-1 flex-col">
                                    <ul role="list" class="-mx-2 flex-1 space-y-1">
                                        <li v-for="item in navigation" :key="item.name">
                                            <a
                                                :href="item.href"
                                                :class="[
                                                    item.current
                                                        ? 'bg-gray-50 text-white'
                                                        : 'text-gray-700 hover:text-white hover:bg-indigo-600',
                                                    'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold',
                                                ]"
                                            >
                                                <component
                                                    :is="item.icon"
                                                    class="h-6 w-6 shrink-0"
                                                    aria-hidden="true"
                                                />
                                                {{ item.name }}
                                            </a>
                                        </li>
                                    </ul>
                                </nav>
                            </div>
                        </DialogPanel>
                    </TransitionChild>
                </div>
            </Dialog>
        </TransitionRoot>
        <div class="flex flex-col items-center justify-center h-full">
            <a href="/" class="button">
                <button type="button" class="h-8 w-auto">
                    <img class="h-8 w-auto" :src="logo" alt="LOGO Mail Assistant" />
                </button>
            </a>
            <nav class="h-5/6 flex items-center justify-center">
                <ul role="list" class="flex flex-col space-y-1">
                    <li v-for="item in navigation" :key="item.name">
                        <a
                            :href="item.href"
                            :class="[
                                useRoute().path === item.href
                                    ? 'bg-gray-100 text-gray-900 lg:ring-1 lg:ring-black lg:ring-opacity-5'
                                    : 'text-gray-500 hover:text-black hover:bg-gray-100',
                                'group flex gap-x-3 rounded-lg p-3 text-sm leading-6 font-semibold',
                            ]"
                        >
                            <component :is="item.icon" class="h-6 w-6 shrink-0" aria-hidden="true" />
                            <span class="sr-only">{{ item.name }}</span>
                        </a>
                    </li>
                </ul>
            </nav>
            <div class="flex justify-center">
                <p class="text-gray-900 font-semibold">v 1.0.0</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
import { Dialog, DialogPanel, TransitionChild, TransitionRoot } from "@headlessui/vue";
import {
    EnvelopeIcon,
    PencilSquareIcon,
    XMarkIcon,
    CogIcon,
    MagnifyingGlassIcon,
    ArrowUturnLeftIcon,
    BeakerIcon,
} from "@heroicons/vue/24/outline";
import { NavigationPage } from "@/global/types";
import logo from "@/assets/logo-aomail.png";
import { i18n } from "@/global/preferences";

const sidebarOpen = ref(false);

const navigation: NavigationPage[] = [
    { name: i18n.global.t("constants.homeNavbar"), href: "/home", icon: EnvelopeIcon },
    { name: i18n.global.t("constants.newEmailNavbar"), href: "/new", icon: PencilSquareIcon },
    { name: i18n.global.t("constants.searchEmailNavbar"), href: "/search", icon: MagnifyingGlassIcon },
    { name: i18n.global.t("constants.rulesNavbar"), href: "/rules", icon: BeakerIcon },
    { name: i18n.global.t("constants.replyLaterNavbar"), href: "/reply-later", icon: ArrowUturnLeftIcon },
    { name: i18n.global.t("constants.settingsNavbar"), href: "/settings", icon: CogIcon },
];
</script>
