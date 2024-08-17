<template>
    <div class="inline-flex rounded-lg shadow-lg items-stretch">
        <button
            @click="sendEmail"
            class="bg-gray-700 rounded-l-lg px-6 py-2 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center 2xl:px-7 2xl:py-3 2xl:text-lg"
        >
            {{ $t("constants.userActions.send") }}
            <PaperAirplaneIcon class="w-4 2xl:w-5" aria-hidden="true" />
        </button>
        <Menu as="div" class="relative -ml-px block items-stretch">
            <MenuButton
                class="relative inline-flex items-center rounded-r-lg px-2 py-2 text-white border-l border-gray-300 bg-gray-700 hover:bg-gray-900 focus:z-10 2xl:px-3 2xl:py-3"
            >
                <span class="sr-only">{{ $t("newPage.openOptions") }}</span>
                <ChevronDownIcon class="h-8 w-5 2xl:h-9 2xl:w-6" aria-hidden="true" />
            </MenuButton>
            <transition
                enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 -translate-y-2"
                enter-to-class="transform opacity-100 translate-y-0"
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 translate-y-0"
                leave-to-class="transform opacity-0 -translate-y-2"
            >
                <MenuItems
                    class="absolute right-0 z-10 -mr-1 bottom-full mb-2 w-56 origin-bottom-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                >
                    <div class="py-1">
                        <button
                            :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']"
                            @click="scheduleSend"
                        >
                            Schedule send
                        </button>
                    </div>
                </MenuItems>
            </transition>
        </Menu>
    </div>
</template>

<script setup>
const sendEmail = () => {
    // Implement send email logic
};
</script>
