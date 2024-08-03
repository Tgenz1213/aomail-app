<template>
    <transition
        enter-active-class="transition ease-out duration-100"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
    >
        <MenuItems
            v-show="isMenuOpen"
            class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none cursor-pointer"
        >
            <div class="py-1">
                <div v-if="item.rule">
                    <MenuItem v-slot="{ active }">
                        <a
                            @click.prevent="openRuleEditor(item.rule_id)"
                            :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']"
                        >
                            <span class="flex gap-x-2 items-center">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1.5"
                                    stroke="currentColor"
                                    class="w-4 h-4"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
                                    />
                                </svg>
                                <span>
                                    {{ $t("constants.userAction.changeTheRule") }}
                                </span>
                            </span>
                        </a>
                    </MenuItem>
                </div>
                <div v-else>
                    <MenuItem v-slot="{ active }">
                        <a
                            @click.prevent="openNewRule(item.name, item.email)"
                            :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']"
                        >
                            <span class="flex gap-x-2 items-center">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1.5"
                                    stroke="currentColor"
                                    class="w-4 h-4"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
                                    />
                                </svg>
                                <span>
                                    {{ $t("constants.userActions.createARule") }}
                                </span>
                            </span>
                        </a>
                    </MenuItem>
                </div>
            </div>
            <div class="py-1">
                <MenuItem v-slot="{ active }">
                    <a
                        @click.prevent="markEmailReplyLater(item)"
                        :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']"
                    >
                        <span class="flex gap-x-2 items-center">
                            <svg
                                class="w-4 h-4"
                                viewBox="0 0 28 28"
                                version="1.1"
                                stroke="currentColor"
                                xmlns="http://www.w3.org/2000/svg"
                                xmlns:xlink="http://www.w3.org/1999/xlink"
                                xml:space="preserve"
                                xmlns:serif="http://www.serif.com/"
                                style="
                                    fill-rule: evenodd;
                                    clip-rule: evenodd;
                                    stroke-linecap: round;
                                    stroke-linejoin: round;
                                "
                            >
                                <path
                                    d="M13.435,17.391l-6.783,-6.782m0,0l6.783,-6.783m-6.783,6.783l13.565,0c3.721,0 6.783,3.061 6.783,6.782c0,3.721 -3.062,6.783 -6.783,6.783l-3.391,0"
                                    style="fill: none; stroke: #000; stroke-width: 1.7px"
                                />
                                <path
                                    d="M7.783,17.391l-6.783,-6.782m0,0l6.783,-6.783"
                                    style="fill: none; stroke: #000; stroke-width: 1.7px"
                                />
                            </svg>
                            <span>
                                {{ $t("constants.userActions.replyLater") }}
                            </span>
                        </span>
                    </a>
                </MenuItem>
            </div>
            <div class="py-1">
                <MenuItem v-slot="{ active }">
                    <a
                        @click.prevent="transferEmail(item)"
                        :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']"
                    >
                        <span class="flex gap-x-2 items-center">
                            <svg
                                class="w-4 h-4"
                                viewBox="0 0 28 28"
                                version="1.1"
                                stroke="currentColor"
                                xmlns="http://www.w3.org/2000/svg"
                                xmlns:xlink="http://www.w3.org/1999/xlink"
                                xml:space="preserve"
                                xmlns:serif="http://www.serif.com/"
                                style="
                                    fill-rule: evenodd;
                                    clip-rule: evenodd;
                                    stroke-linecap: round;
                                    stroke-linejoin: round;
                                "
                            >
                                <path
                                    d="M13.435,10.609l6.783,6.782m0,0l-6.783,6.783m6.783-6.783L6.85,17.391c-3.721,0-6.783-3.061-6.783-6.782c0-3.721,3.062-6.783,6.783-6.783l3.391,0"
                                    style="fill: none; stroke: #000; stroke-width: 1.7px"
                                />
                                <path
                                    d="M21.197,10.609l6.783,6.782m0,0l-6.783,6.783"
                                    style="fill: none; stroke: #000; stroke-width: 1.7px"
                                />
                            </svg>
                            <span>
                                {{ $t("constants.userActions.transfer") }}
                            </span>
                        </span>
                    </a>
                </MenuItem>
            </div>
        </MenuItems>
    </transition>
</template>

<script setup lang="ts">
import { MenuItem, MenuItems } from "@headlessui/vue"

</script>


<!-- todo: define color of the button as props (analyse what is common and how many color variations are required) -->