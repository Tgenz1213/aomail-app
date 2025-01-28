<template>
    <div
        :class="[
            'relative h-full bg-white border-r border-gray-200 flex flex-col transition-width duration-300',
            isMinimized ? 'w-20' : 'w-60',
        ]"
    >
        <!-- Logo section -->
        <div class="px-4 pt-4 pb-8">
            <a href="/" class="flex items-center justify-center">
                <img class="h-8 w-auto" :src="logo" alt="Aomail logo" />
                <!--<span v-if="!isMinimized" class="ml-2 text-xl font-bold">Aomail</span>-->
            </a>
        </div>

        <!-- New Email Button -->
        <div :class="[isMinimized ? 'px-4' : 'px-4', 'py-2']">
            <a
                href="/new"
                :class="[
                    'bg-black text-white py-2 rounded-md flex items-center transition-colors',
                    isMinimized ? 'justify-center w-12 mx-auto' : 'justify-center w-full hover:bg-gray-800',
                ]"
            >
                <PencilSquareIcon class="h-5 w-5" :class="{ 'mr-2': !isMinimized }" />
                <span v-if="!isMinimized">{{ i18n.global.t("constants.newEmailNavbar") }}</span>
            </a>
        </div>

        <!-- Main Navigation section -->
        <nav class="mt-4 flex-1">
            <ul role="list" class="space-y-1" :class="{ 'px-4': isMinimized, 'px-2': !isMinimized }">
                <li v-for="item in mainNavigation" :key="item.name">
                    <a
                        :href="item.href"
                        :class="[
                            useRoute().path === item.href
                                ? 'bg-gray-200 text-gray-900'
                                : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900',
                            'group flex items-center rounded-md py-2 text-sm font-medium',
                            isMinimized ? 'justify-center w-12 mx-auto' : 'px-3 gap-x-3',
                        ]"
                    >
                        <component :is="item.icon" class="h-5 w-5 shrink-0" aria-hidden="true" />
                        <span v-if="!isMinimized">{{ item.name }}</span>
                    </a>
                </li>
            </ul>
        </nav>

        <!-- Bottom Navigation section -->
        <nav class="p-2">
            <ul role="list" class="space-y-1">
                <li v-for="item in bottomNavigation" :key="item.name">
                    <a
                        :href="item.href"
                        :class="[
                            useRoute().path === item.href
                                ? 'bg-gray-200 text-gray-900'
                                : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900',
                            'group flex items-center rounded-md py-2 text-sm font-medium',
                            isMinimized ? 'justify-center w-12 mx-auto' : 'px-3 gap-x-3',
                        ]"
                        :target="item.target || '_self'"
                        :rel="item.target === '_blank' ? 'noopener noreferrer' : undefined"
                    >
                        <component :is="item.icon" class="h-5 w-5 shrink-0" aria-hidden="true" />
                        <span v-if="!isMinimized">{{ item.name }}</span>
                    </a>
                </li>
            </ul>
        </nav>

        <!-- Toggle Button -->
        <button
            @click="toggleMinimize"
            class="absolute right-0 top-1/2 transform -translate-y-1/2 rounded-l-sm flex items-center justify-center w-8 h-8 border-t border-l border-b border-gray-300 rounded-none focus:outline-none hover:bg-gray-100"
            :aria-label="isMinimized ? 'Expand Navbar' : 'Minimize Navbar'"
        >
            <ChevronDoubleLeftIcon v-if="!isMinimized" class="h-5 w-5 text-gray-700" />
            <ChevronDoubleRightIcon v-else class="h-5 w-5 text-gray-700" />
        </button>

        <!-- Footer section -->
        <div class="w-full p-4 border-t border-gray-200">
            <div class="flex items-center justify-between">
                <p class="text-sm text-gray-500 font-medium">{{ VERSION }}</p>
                <a
                    v-if="!isMinimized"
                    :href="getHelpLink"
                    target="_blank"
                    class="text-gray-500 hover:text-gray-700 transition-colors"
                >
                    <InformationCircleIcon class="h-5 w-5" />
                </a>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import {
    SparklesIcon,
    PencilSquareIcon,
    CogIcon,
    MagnifyingGlassIcon,
    ArrowUturnLeftIcon,
    ChartBarIcon,
    InformationCircleIcon,
    InboxIcon,
    RocketLaunchIcon,
    ChatBubbleLeftRightIcon,
    ChevronDoubleLeftIcon,
    ChevronDoubleRightIcon,
} from "@heroicons/vue/24/outline";
import { NavigationPage } from "@/global/types";
import logo from "@/assets/logo-aomail.png";
import { i18n } from "@/global/preferences";
import { VERSION } from "@/global/const";

// Add this near the top of the script section
const emit = defineEmits(["update:isMinimized"]);

// State for minimizing the navbar
const isMinimized = ref(false);

// Modify the toggleMinimize function
const toggleMinimize = () => {
    isMinimized.value = !isMinimized.value;
    localStorage.setItem("navbarMinimized", isMinimized.value.toString());
    emit("update:isMinimized", isMinimized.value);
};

// Add a watch to emit initial state
onMounted(() => {
    const storedState = localStorage.getItem("navbarMinimized");
    if (storedState !== null) {
        isMinimized.value = storedState === "true";
        emit("update:isMinimized", isMinimized.value);
    }
});

// Main navigation items (excluding 'New Email')
const mainNavigation: NavigationPage[] = [
    { name: i18n.global.t("constants.AiNavbar"), href: "/ai-assistant", icon: SparklesIcon },
    { name: i18n.global.t("constants.inboxNavbar"), href: "/inbox", icon: InboxIcon },
    { name: "Analytics", href: "/analytics", icon: ChartBarIcon },
    { name: i18n.global.t("constants.searchEmailNavbar"), href: "/search", icon: MagnifyingGlassIcon },
    { name: i18n.global.t("constants.replyLaterNavbar"), href: "/reply-later", icon: ArrowUturnLeftIcon },
];

// Bottom navigation items
const bottomNavigation: NavigationPage[] = [
    { name: i18n.global.t("constants.settingsNavbar"), href: "/settings", icon: CogIcon },
    { name: i18n.global.t("constants.subscriptionNavbar"), href: "/subscription", icon: RocketLaunchIcon },
    {
        name: i18n.global.t("constants.discordNavbar"),
        href: "https://discord.gg/JxbPZNDd",
        icon: ChatBubbleLeftRightIcon,
        target: "_blank",
    },
    // Add more bottom tabs here
    // Example:
    // { name: i18n.global.t("constants.helpNavbar"), href: "/help", icon: HelpIcon },
];

const route = useRoute();
const getHelpLink = computed(() => {
    const basePath = "https://info.aomail.ai/article";
    switch (route.path) {
        case "/home":
            return `${basePath}/4/how-to-use-the-home-page-of-aomail`;
        case "/new":
            return `${basePath}/5/how-to-use-the-new-page-of-aomail`;
        case "/search":
            return `${basePath}/6/how-to-use-the-search-page-of-aomail`;
        case "/rules":
            return `${basePath}/7/how-to-use-the-rules-page-of-aomail`;
        case "/reply-later":
            return `${basePath}/8/how-to-use-the-reply-later-page-of-aomail`;
        case "/settings":
            return `${basePath}/9/how-to-use-the-settings-page-of-aomail`;
        default:
            return `${basePath}/4/how-to-use-the-home-page-of-aomail`;
    }
});
</script>

<style scoped>
.transition-width {
    transition: width 0.3s ease;
}
</style>
