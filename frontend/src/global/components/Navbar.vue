<template>
    <div class="h-full w-60 bg-gray-50 border-r border-gray-200">
        <!-- Logo section -->
        <div class="px-4 py-4">
            <a href="/" class="flex items-center">
                <img class="h-8 w-auto" :src="logo" alt="Aomail logo" />
            </a>
        </div>

        <!-- Navigation section -->
        <nav class="mt-4">
            <ul role="list" class="space-y-1 px-2">
                <li v-for="item in navigation" :key="item.name">
                    <a
                        :href="item.href"
                        :class="[
                            useRoute().path === item.href
                                ? 'bg-gray-200 text-gray-900'
                                : 'text-gray-700 hover:bg-gray-200 hover:text-gray-900',
                            'group flex items-center gap-x-3 rounded-md px-3 py-2 text-sm font-medium',
                        ]"
                    >
                        <component :is="item.icon" class="h-5 w-5 shrink-0" aria-hidden="true" />
                        {{ item.name }}
                    </a>
                </li>
            </ul>
        </nav>

        <!-- Footer section -->
        <div class="absolute bottom-0 w-60 p-4 border-t border-gray-200">
            <div class="flex items-center justify-between">
                <p class="text-sm text-gray-600 font-medium">{{ VERSION }}</p>
                <a 
                    :href="getGithubLink"
                    target="_blank"
                    class="text-gray-500 hover:text-gray-900 transition-colors"
                >
                    <InformationCircleIcon class="h-5 w-5" />
                </a>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import {
    EnvelopeIcon,
    PencilSquareIcon,
    CogIcon,
    MagnifyingGlassIcon,
    ArrowUturnLeftIcon,
    BeakerIcon,
    InformationCircleIcon,
} from "@heroicons/vue/24/outline";
import { NavigationPage } from "@/global/types";
import logo from "@/assets/logo-aomail.png";
import { i18n } from "@/global/preferences";
import { VERSION } from "@/global/const";

const navigation: NavigationPage[] = [
    { name: i18n.global.t("constants.homeNavbar"), href: "/home", icon: EnvelopeIcon },
    { name: i18n.global.t("constants.newEmailNavbar"), href: "/new", icon: PencilSquareIcon },
    { name: i18n.global.t("constants.searchEmailNavbar"), href: "/search", icon: MagnifyingGlassIcon },
    { name: i18n.global.t("constants.rulesNavbar"), href: "/rules", icon: BeakerIcon },
    { name: i18n.global.t("constants.replyLaterNavbar"), href: "/reply-later", icon: ArrowUturnLeftIcon },
    { name: i18n.global.t("constants.settingsNavbar"), href: "/settings", icon: CogIcon },
];

const route = useRoute();
const getGithubLink = computed(() => {
    const basePath = 'https://info.aomail.ai/article';
    switch (route.path) {
        case '/home':
            return `${basePath}/4/🧐-how-to-use-the-home-page-of-aomail-`;
        case '/new':
            return `${basePath}/5/🧐-how-to-use-the-new-page-of-aomail-`;
        case '/search':
            return `${basePath}/6/🧐-how-to-use-the-search-page-of-aomail-`;
        case '/rules':
            return `${basePath}/7/🧐-how-to-use-the-rules-page-of-aomail-`;
        case '/reply-later':
            return `${basePath}/8/🧐-how-to-use-the-reply-later-page-of-aomail-`;
        case '/settings':
            return `${basePath}/9/🧐-how-to-use-the-settings-page-of-aomail-`;
        default:
            return `${basePath}/4/🧐-how-to-use-the-home-page-of-aomail-`;
    }
});
</script> 