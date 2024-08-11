<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />

    <div class="relative">
        <Listbox as="div" v-model="selectedTimeZone">
            <!-- Add a search input above the ListboxButton -->
            <div class="mb-2">
                <input
                    type="text"
                    v-model="searchQuery"
                    placeholder="Search time zones..."
                    class="w-full p-2 border rounded-md"
                    @focus="selectAllText"
                />
            </div>

            <ListboxButton
                class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6"
            >
                <span class="block truncate">{{ selectedTimeZone || 'Select a timezone' }}</span>
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
                    @scroll="handleScroll"
                    class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                >
                    <template v-if="filteredTimezones.length">
                        <ListboxOption
                            as="template"
                            v-for="timezone in filteredTimezones"
                            :key="timezone"
                            :value="timezone"
                            v-slot="{ active, selected }"
                        >
                            <li
                                :class="[
                                    active ? 'bg-gray-800 text-white' : 'text-gray-900',
                                    'relative cursor-default select-none py-2 pl-3 pr-9',
                                ]"
                            >
                                <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                                    {{ timezone }}
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
                    </template>
                    <li v-else class="relative cursor-default select-none py-2 pl-3 pr-9 text-gray-500">
                        No results found
                    </li>
                </ListboxOptions>
            </transition>
        </Listbox>
    </div>
</template>
