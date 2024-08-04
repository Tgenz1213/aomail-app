<template>
    <span class="isolate inline-flex rounded-2xl">
        <div v-show="hoveredItemId === item.id" class="group action-buttons">
            <div class="relative group">
                <div
                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4 z-40"
                >
                    {{ $t("constants.userActions.open") }}
                </div>
                <button
                    @click="$emit('openSeeModal', item)"
                    type="button"
                    :class="`relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-gray-400 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`"
                >
                    <eye-icon :class="`w-5 h-5 text-${color}-400 group-hover:text-white`" />
                </button>
            </div>
        </div>
        <div v-show="hoveredItemId === item.id" class="group action-buttons">
            <div class="relative group">
                <div
                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-2"
                >
                    {{ $t("homePage.read") }}
                </div>
                <button
                    @click="$emit('markEmailAsRead', item.id)"
                    type="button"
                    :class="`relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`"
                >
                    <check-icon :class="`w-5 h-5 text-${color}-400 group-hover:text-white`" />
                </button>
            </div>
        </div>
        <div v-show="hoveredItemId === item.id" class="group action-buttons">
            <div class="relative group">
                <div
                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7"
                >
                    {{ $t("homePage.answer") }}
                </div>
                <button
                    @click="$emit('openAnswer', item)"
                    type="button"
                    :class="`relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`"
                >
                    <arrow-uturn-left-icon :class="`w-5 h-5 text-${color}-400 group-hover:text-white`" />
                </button>
            </div>
        </div>
        <div v-show="hoveredItemId === item.id" class="group action-buttons">
            <div class="relative group">
                <div
                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-center text-sm rounded shadow-lg mt-[-45px] -ml-[125px] w-[185px]"
                >
                    {{ $t("constants.additionalActions") }}
                </div>
                <Menu as="div" class="relative inline-block text-left">
                    <div>
                        <MenuButton
                            @click="$emit('toggleTooltip')"
                            :class="`relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-${color}-400 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`"
                        >
                            <ellipsis-horizontal-icon
                                :class="`w-5 h-5 group-hover:text-white text-${color}-400 group-active:text-${color}-400 group-focus:text-red focus:text-${color}-400`"
                            />
                        </MenuButton>
                    </div>
                    <ToolTipActionButtons
                        :isMenuOpen="isMenuOpen"
                        :showRuleOptions="showRuleOptions"
                        :ruleActionText="ruleActionText"
                        :item="item"
                        @handleRuleAction="$emit('handleRuleAction', $event)"
                        @handleReplyLater="$emit('handleReplyLater', $event)"
                        @handleTransfer="$emit('handleTransfer', $event)"
                    />
                </Menu>
            </div>
        </div>
    </span>
</template>

<script setup lang="ts">
import { Menu, MenuButton } from "@headlessui/vue";
import { EyeIcon, CheckIcon, ArrowUturnLeftIcon, EllipsisHorizontalIcon } from "@heroicons/vue/24/outline";
import ToolTipActionButtons from "./ToolTipActionButtons.vue";

interface Props {
    hoveredItemId: string | null;
    item: any; // Replace with the actual type of your item
    color: "blue" | "orange" | "stone"; // Add more color options as needed
    isMenuOpen: boolean;
    showRuleOptions: boolean;
    ruleActionText: string;
}

const props = defineProps<Props>();

const emit = defineEmits<{
    (e: "openSeeModal", item: any): void;
    (e: "markEmailAsRead", id: string): void;
    (e: "openAnswer", item: any): void;
    (e: "toggleTooltip"): void;
    (e: "handleRuleAction", item: any): void;
    (e: "handleReplyLater", item: any): void;
    (e: "handleTransfer", item: any): void;
}>();
</script>
