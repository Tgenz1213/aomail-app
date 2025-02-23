<template>
    <transition name="modal-fade">
        <div
            v-if="isOpen"
            @click.self="closeModal"
            class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
        >
            <div class="bg-white rounded-lg relative w-[850px] max-h-[85vh] overflow-y-auto">
                <!-- Header -->
                <div class="sticky top-0 z-10 rounded-t-lg border-b border-gray-200 bg-gray-50">
                    <div class="flex items-center justify-between p-4">
                        <h2 class="text-lg font-semibold text-gray-900">
                            {{ $t("rulesPage.modals.createRule.title") }}
                        </h2>
                        <button @click="closeModal" class="text-gray-400 hover:text-gray-500">
                            <XMarkIcon class="h-6 w-6" />
                        </button>
                    </div>
                </div>

                <!-- Content -->
                <div class="p-4 space-y-6">
                    <div v-if="errorMessage" class="text-red-600 text-sm mb-4">{{ errorMessage }}</div>

                    <!-- Logical Operator (Listbox) -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">
                            {{ $t("rulesPage.modals.common.logicalOperator") }}
                        </label>
                        <Listbox v-model="formData.logicalOperator">
                            <div class="relative">
                                <ListboxButton
                                    class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6"
                                >
                                    <span class="block truncate">
                                        {{
                                            formData.logicalOperator === "AND"
                                                ? $t("rulesPage.modals.common.andOperator")
                                                : $t("rulesPage.modals.common.orOperator")
                                        }}
                                    </span>
                                    <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                                        <ChevronDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                                    </span>
                                </ListboxButton>
                                <transition
                                    leave-active-class="transition ease-in duration-100"
                                    leave-from-class="opacity-100"
                                    leave-to-class="opacity-0"
                                >
                                    <ListboxOptions
                                        class="absolute z-10 max-h-60 w-full rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                                    >
                                        <ListboxOption v-slot="{ active, selected }" :value="'AND'" as="template">
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
                                                    {{ $t("rulesPage.modals.common.andOperator") }}
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
                                        <ListboxOption v-slot="{ active, selected }" :value="'OR'" as="template">
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
                                                    {{ $t("rulesPage.modals.common.orOperator") }}
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
                            </div>
                        </Listbox>
                    </div>

                    <!-- Triggers Section -->
                    <div class="border rounded-md">
                        <button
                            @click="sections.triggers = !sections.triggers"
                            class="w-full flex justify-between items-center p-3 text-left bg-gray-50 rounded-md"
                        >
                            <div class="flex items-center">
                                <InboxArrowDownIcon class="h-5 w-5 text-gray-500 mr-2" />
                                <span class="text-sm font-medium text-gray-900">
                                    {{ $t("rulesPage.modals.common.triggers.title") }}
                                </span>
                            </div>
                            <ChevronDownIcon
                                class="h-5 w-5 text-gray-500"
                                :class="{ 'transform rotate-180': sections.triggers }"
                            />
                        </button>

                        <div v-if="sections.triggers" class="p-4 border-t space-y-4">
                            <div class="space-y-3">
                                <div v-for="(trigger, index) in triggers" :key="index" class="space-y-3">
                                    <!-- Trigger Type Selection (Listbox) -->
                                    <div class="flex items-center gap-4">
                                        <label class="text-sm font-medium text-gray-700 whitespace-nowrap">
                                            {{ `${index + 1}${getOrdinalSuffix(index + 1)} `
                                            }}{{ $t("rulesPage.modals.common.triggers.title").toLowerCase() }}
                                        </label>
                                        <Listbox
                                            v-model="trigger.type"
                                            class="flex-1"
                                            @click="handleTriggerTypeChange(trigger)"
                                        >
                                            <div class="relative">
                                                <ListboxButton
                                                    class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                >
                                                    <span class="block truncate">
                                                        {{
                                                            trigger.type
                                                                ? $t(
                                                                      `rulesPage.modals.common.triggers.types.${trigger.type}.label`
                                                                  )
                                                                : $t("rulesPage.modals.common.selectTriggerType")
                                                        }}
                                                    </span>
                                                    <span
                                                        class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2"
                                                    >
                                                        <ChevronUpDownIcon
                                                            class="h-5 w-5 text-gray-400"
                                                            aria-hidden="true"
                                                        />
                                                    </span>
                                                </ListboxButton>
                                                <transition
                                                    leave-active-class="transition ease-in duration-100"
                                                    leave-from-class="opacity-100"
                                                    leave-to-class="opacity-0"
                                                >
                                                    <ListboxOptions
                                                        class="absolute z-10 overflow-y-auto max-h-[200px] w-full rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                                                    >
                                                        <ListboxOption
                                                            v-for="option in availableTriggerTypes"
                                                            :key="option.value"
                                                            v-slot="{ active, selected }"
                                                            :value="option.value"
                                                            :disabled="isTypeUsed(option.value, index, triggers)"
                                                            as="template"
                                                        >
                                                            <li
                                                                :class="[
                                                                    active ? 'bg-gray-800 text-white' : 'text-gray-900',
                                                                    isTypeUsed(option.value, index, triggers)
                                                                        ? 'opacity-50 cursor-not-allowed'
                                                                        : 'cursor-default',
                                                                    'relative select-none py-2 pl-3 pr-9',
                                                                ]"
                                                            >
                                                                <div class="flex items-center justify-between">
                                                                    <div class="flex items-center">
                                                                        <span
                                                                            :class="[
                                                                                selected
                                                                                    ? 'font-semibold'
                                                                                    : 'font-normal',
                                                                                trigger.type && !selected
                                                                                    ? 'text-gray-400'
                                                                                    : '',
                                                                                'block truncate',
                                                                            ]"
                                                                        >
                                                                            {{
                                                                                $t(
                                                                                    `rulesPage.modals.common.triggers.types.${option.value}.label`
                                                                                )
                                                                            }}
                                                                        </span>
                                                                        <InformationCircleIcon
                                                                            class="h-4 w-4 ml-1.5"
                                                                            :class="[
                                                                                active
                                                                                    ? 'text-gray-300'
                                                                                    : 'text-gray-400',
                                                                                trigger.type && !selected
                                                                                    ? 'text-gray-300'
                                                                                    : '',
                                                                            ]"
                                                                        />
                                                                        <span
                                                                            class="ml-2 text-xs"
                                                                            :class="[
                                                                                active
                                                                                    ? 'text-gray-300'
                                                                                    : 'text-gray-500',
                                                                                trigger.type && !selected
                                                                                    ? 'text-gray-300'
                                                                                    : '',
                                                                            ]"
                                                                        >
                                                                            {{
                                                                                $t(
                                                                                    `rulesPage.modals.common.triggers.types.${option.value}.description`
                                                                                )
                                                                            }}
                                                                        </span>
                                                                    </div>
                                                                    <span
                                                                        v-if="selected"
                                                                        :class="[
                                                                            active ? 'text-gray-300' : 'text-gray-500',
                                                                            'flex items-center pr-4',
                                                                        ]"
                                                                    >
                                                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                                                    </span>
                                                                </div>
                                                            </li>
                                                        </ListboxOption>
                                                    </ListboxOptions>
                                                </transition>
                                            </div>
                                        </Listbox>
                                    </div>

                                    <!-- Trigger Value Input -->
                                    <div v-if="trigger.type" class="pl-4 border-l-2 border-gray-200">
                                        <div v-if="trigger.type === 'domains'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">
                                                {{ $t("rulesPage.modals.common.emailDomains") }}
                                            </label>
                                            <TagInput
                                                v-model="trigger.value"
                                                :placeholder="$t('rulesPage.modals.common.addDomain')"
                                                :validate="validateDomain"
                                            />
                                        </div>
                                        <div v-if="trigger.type === 'senderEmails'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">
                                                {{ $t("rulesPage.modals.common.senderEmails") }}
                                            </label>
                                            <TagInput
                                                v-model="trigger.value"
                                                :placeholder="$t('rulesPage.modals.common.addEmailAddress')"
                                                :validate="validateEmail"
                                            />
                                        </div>
                                        <div v-if="trigger.type === 'hasAttachments'" class="space-y-2">
                                            <div class="flex items-center">
                                                <input
                                                    v-model="trigger.value"
                                                    type="checkbox"
                                                    class="h-4 w-4 rounded border-gray-300 text-gray-600 focus:ring-gray-500"
                                                />
                                                <label class="ml-2 text-sm text-gray-700">
                                                    {{
                                                        $t(
                                                            "rulesPage.modals.common.triggers.types.hasAttachments.label"
                                                        )
                                                    }}
                                                </label>
                                            </div>
                                        </div>
                                        <div v-if="trigger.type === 'categories'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">
                                                {{ $t("constants.category") }}
                                            </label>
                                            <multiselect
                                                v-model="trigger.value"
                                                :options="categoryOptions.map((c) => c.name)"
                                                :multiple="true"
                                                :placeholder="$t('rulesPage.modals.common.selectOptions')"
                                                class="multiselect-gray"
                                            />
                                        </div>
                                        <template
                                            v-for="option in ['priorities', 'answers', 'relevances', 'flags']"
                                            :key="option"
                                        >
                                            <div v-if="trigger.type === option" class="space-y-2">
                                                <label class="block text-sm text-gray-700">
                                                    {{ formatLabel(option) }}
                                                </label>
                                                <multiselect
                                                    v-model="trigger.value"
                                                    :options="getOptionsForType(option)"
                                                    :multiple="true"
                                                    track-by="key"
                                                    label="value"
                                                    :placeholder="$t('rulesPage.modals.common.selectOptions')"
                                                    class="multiselect-gray"
                                                />
                                            </div>
                                        </template>
                                    </div>

                                    <!-- Logical Operator Display Between Triggers -->
                                    <div
                                        v-if="index < triggers.length - 1"
                                        class="flex items-center justify-center py-2"
                                    >
                                        <span
                                            class="px-3 py-1 bg-gray-100 rounded-full text-sm font-medium text-gray-700"
                                        >
                                            {{ formData.logicalOperator }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <!-- Add Trigger Button -->
                            <button
                                @click="addTrigger"
                                class="w-full py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 bg-gray-50"
                                :disabled="!canAddMoreTriggers"
                            >
                                {{ $t("rulesPage.modals.common.triggers.addTrigger") }}
                            </button>
                        </div>
                    </div>

                    <!-- Actions Section -->
                    <div class="border rounded-md">
                        <button
                            @click="sections.actions = !sections.actions"
                            class="w-full flex justify-between items-center p-3 text-left bg-gray-50 rounded-md"
                        >
                            <div class="flex items-center">
                                <BoltIcon class="h-5 w-5 text-gray-500 mr-2" />
                                <span class="text-sm font-medium text-gray-900">
                                    {{ $t("rulesPage.modals.common.actions.title") }}
                                </span>
                            </div>
                            <ChevronDownIcon
                                class="h-5 w-5 text-gray-500"
                                :class="{ 'transform rotate-180': sections.actions }"
                            />
                        </button>

                        <div v-if="sections.actions" class="p-4 border-t space-y-4">
                            <div class="space-y-3">
                                <div v-for="(action, index) in actions" :key="index" class="space-y-3">
                                    <!-- Action Type Selection (Listbox) -->
                                    <div class="flex items-center gap-4">
                                        <label class="text-sm font-medium text-gray-700 whitespace-nowrap">
                                            {{ `${index + 1}${getOrdinalSuffix(index + 1)} `
                                            }}{{ $t("rulesPage.modals.common.actions.title").toLowerCase() }}
                                        </label>
                                        <Listbox
                                            v-model="action.type"
                                            class="flex-1"
                                            @click="handleActionTypeChange(action)"
                                        >
                                            <div class="relative">
                                                <ListboxButton
                                                    class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6"
                                                >
                                                    <span class="block truncate">
                                                        {{
                                                            action.type
                                                                ? $t(
                                                                      `rulesPage.modals.common.actions.types.${action.type}.label`
                                                                  )
                                                                : $t("rulesPage.modals.common.selectActionType")
                                                        }}
                                                    </span>
                                                    <span
                                                        class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2"
                                                    >
                                                        <ChevronUpDownIcon
                                                            class="h-5 w-5 text-gray-400"
                                                            aria-hidden="true"
                                                        />
                                                    </span>
                                                </ListboxButton>
                                                <transition
                                                    leave-active-class="transition ease-in duration-100"
                                                    leave-from-class="opacity-100"
                                                    leave-to-class="opacity-0"
                                                >
                                                    <ListboxOptions
                                                        class="absolute z-10 w-full overflow-y-auto max-h-[150px] rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                                                    >
                                                        <ListboxOption
                                                            v-for="option in availableActionTypes"
                                                            :key="option.value"
                                                            v-slot="{ active, selected }"
                                                            :value="option.value"
                                                            :disabled="isTypeUsed(option.value, index, actions)"
                                                            as="template"
                                                        >
                                                            <li
                                                                :class="[
                                                                    active ? 'bg-gray-800 text-white' : 'text-gray-900',
                                                                    isTypeUsed(option.value, index, actions)
                                                                        ? 'opacity-50 cursor-not-allowed'
                                                                        : 'cursor-default',
                                                                    'relative select-none py-2 pl-3 pr-9',
                                                                ]"
                                                            >
                                                                <div class="flex items-center justify-between">
                                                                    <div class="flex items-center">
                                                                        <span
                                                                            :class="[
                                                                                selected
                                                                                    ? 'font-semibold'
                                                                                    : 'font-normal',
                                                                                'block truncate',
                                                                            ]"
                                                                        >
                                                                            {{
                                                                                $t(
                                                                                    `rulesPage.modals.common.actions.types.${option.value}.label`
                                                                                )
                                                                            }}
                                                                        </span>
                                                                        <InformationCircleIcon
                                                                            class="h-4 w-4 ml-1.5"
                                                                            :class="
                                                                                active
                                                                                    ? 'text-gray-300'
                                                                                    : 'text-gray-400'
                                                                            "
                                                                        />
                                                                        <span
                                                                            class="ml-2 text-xs"
                                                                            :class="
                                                                                active
                                                                                    ? 'text-gray-300'
                                                                                    : 'text-gray-500'
                                                                            "
                                                                        >
                                                                            {{
                                                                                $t(
                                                                                    `rulesPage.modals.common.actions.types.${option.value}.description`
                                                                                )
                                                                            }}
                                                                        </span>
                                                                    </div>
                                                                    <span
                                                                        v-if="selected"
                                                                        :class="[
                                                                            active ? 'text-gray-300' : 'text-gray-500',
                                                                            'flex items-center pr-4',
                                                                        ]"
                                                                    >
                                                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                                                    </span>
                                                                </div>
                                                            </li>
                                                        </ListboxOption>
                                                    </ListboxOptions>
                                                </transition>
                                            </div>
                                        </Listbox>
                                    </div>

                                    <!-- Action Value Input -->
                                    <div v-if="action.type" class="pl-4 border-l-2 border-gray-200">
                                        <div v-if="action.type === 'setFlags'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">
                                                {{ $t("rulesPage.modals.common.actions.types.setFlags.label") }}
                                            </label>
                                            <multiselect
                                                v-model="action.value"
                                                :options="flagOptions"
                                                :multiple="true"
                                                track-by="key"
                                                label="value"
                                                :placeholder="$t('rulesPage.modals.common.selectOptions')"
                                                class="multiselect-gray"
                                            />
                                        </div>

                                        <div v-if="action.type === 'markAs'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">
                                                {{ $t("rulesPage.modals.common.actions.types.markAs.label") }}
                                            </label>
                                            <multiselect
                                                v-model="action.value"
                                                :options="markAsOptions"
                                                :multiple="true"
                                                track-by="key"
                                                label="value"
                                                :placeholder="$t('rulesPage.modals.common.selectOptions')"
                                                class="multiselect-gray"
                                            />
                                        </div>

                                        <div v-if="action.type === 'delete'" class="space-y-2">
                                            <div class="flex items-center">
                                                <input
                                                    v-model="action.value"
                                                    type="checkbox"
                                                    class="h-4 w-4 rounded border-gray-300 text-gray-600 focus:ring-gray-500"
                                                />
                                                <label class="ml-2 text-sm text-gray-700">
                                                    {{ $t("rulesPage.modals.common.deleteEmail") }}
                                                </label>
                                            </div>
                                        </div>

                                        <div v-if="action.type === 'setCategory'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">
                                                {{ $t("rulesPage.modals.common.setCategory") }}
                                            </label>
                                            <select
                                                v-model="action.value"
                                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                            >
                                                <option value="">
                                                    {{ $t("rulesPage.modals.common.selectCategory") }}
                                                </option>
                                                <option
                                                    v-for="category in props.categories"
                                                    :key="category.name"
                                                    :value="category.name"
                                                >
                                                    {{ category.name }}
                                                </option>
                                            </select>
                                        </div>

                                        <div v-if="action.type === 'setPriority'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">
                                                {{ $t("rulesPage.modals.common.setPriority") }}
                                            </label>
                                            <select
                                                v-model="action.value"
                                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                            >
                                                <option value="">
                                                    {{ $t("rulesPage.modals.common.selectPriority") }}
                                                </option>
                                                <option
                                                    v-for="priority in priorityOptions"
                                                    :key="priority.key"
                                                    :value="priority.value"
                                                >
                                                    {{ priority.value }}
                                                </option>
                                            </select>
                                        </div>

                                        <div v-if="action.type === 'setRelevance'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">
                                                {{ $t("rulesPage.modals.common.setRelevance") }}
                                            </label>
                                            <select
                                                v-model="action.value"
                                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                            >
                                                <option value="">
                                                    {{ $t("rulesPage.modals.common.selectRelevance") }}
                                                </option>
                                                <option
                                                    v-for="relevance in relevanceOptions"
                                                    :key="relevance.key"
                                                    :value="relevance.value"
                                                >
                                                    {{ relevance.value }}
                                                </option>
                                            </select>
                                        </div>

                                        <div v-if="action.type === 'setAnswer'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">
                                                {{ $t("rulesPage.modals.common.actions.types.setAnswer.label") }}
                                            </label>
                                            <select
                                                v-model="action.value"
                                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring focus:ring-gray-500 focus:ring-opacity-50"
                                            >
                                                <option value="">
                                                    {{ $t("rulesPage.modals.common.selectOptions") }}
                                                </option>
                                                <option
                                                    v-for="answer in answerOptions"
                                                    :key="answer.key"
                                                    :value="answer.value"
                                                >
                                                    {{ answer.value }}
                                                </option>
                                            </select>
                                        </div>

                                        <div v-if="action.type === 'setTransferRecipients'" class="space-y-2">
                                            <label class="block text-sm text-gray-700">
                                                Transfer recipients emails
                                            </label>
                                            <TagInput
                                                v-model="action.value"
                                                :placeholder="$t('rulesPage.modals.common.addEmailAddress')"
                                                :validate="validateEmail"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- Add Action Button -->
                            <button
                                @click="addAction"
                                class="w-full py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 bg-gray-50"
                                :disabled="!canAddMoreActions"
                            >
                                {{ $t("rulesPage.modals.common.actions.addAction") }}
                            </button>
                        </div>
                    </div>

                    <!-- Submit Button -->
                    <div class="flex justify-end pt-4">
                        <button
                            type="button"
                            class="px-4 py-2 bg-gray-800 text-white rounded-md hover:bg-black focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                            @click="handleSubmit"
                        >
                            {{ $t("rulesPage.modals.createRule.createButton") }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { computed, inject, onMounted, ref, watch } from "vue";
import {
    ChevronDownIcon,
    ChevronUpDownIcon,
    CheckIcon,
    InformationCircleIcon,
    BoltIcon,
    InboxArrowDownIcon,
} from "@heroicons/vue/20/solid";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import { postData } from "@/global/fetchData";
import { Category, EmailSender, KeyValuePair } from "@/global/types";
import { RuleData } from "../utils/types";
import Multiselect from "vue-multiselect";
import TagInput from "./TagInput.vue";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue";
import { i18n } from "@/global/preferences";
import {
    ANSWER_REQUIRED,
    HIGHLY_RELEVANT,
    IMPORTANT,
    INFORMATIVE,
    USELESS,
    MIGHT_REQUIRE_ANSWER,
    NO_ANSWER_REQUIRED,
    NOT_RELEVANT,
    POSSIBLY_RELEVANT,
    SPAM,
    SCAM,
    NEWSLETTER,
    NOTIFICATION,
    MEETING,
} from "@/global/const";

interface Props {
    isOpen: boolean;
    categories: Category[];
    emailSenders: EmailSender[];
}

const props = withDefaults(defineProps<Props>(), {
    isOpen: false,
    categories: () => [],
});

const emit = defineEmits<{
    (e: "update:isOpen", value: boolean): void;
    (e: "fetch-rules"): void;
}>();

const isOpen = ref(props.isOpen);
const errorMessage = ref("");

// Section visibility state
const sections = ref({
    triggers: false,
    actions: false,
});

// Main form data (old logic structure)
const formData = ref<RuleData>({
    logicalOperator: "OR",
    domains: [],
    senderEmails: [],
    hasAttachements: false,
    categories: [],
    priorities: [],
    answers: [],
    relevances: [],
    flags: [],
    emailDealWith: "",
    actionTransferRecipients: [],
    actionSetFlags: [],
    actionMarkAs: [],
    actionDelete: false,
    actionSetCategory: "",
    actionSetPriority: "",
    actionSetRelevance: "",
    actionSetAnswer: "",
    actionReplyPrompt: "",
    actionReplyRecipients: [],
});

// Triggers and Actions arrays (new design)
interface Trigger {
    type: string;
    value: any;
}
const triggers = ref<Trigger[]>([{ type: "", value: null }]);
const actions = ref<Trigger[]>([{ type: "", value: null }]);

const handleActionTypeChange = (action: Trigger) => {
    action.value = null;
};

const handleTriggerTypeChange = (trigger: Trigger) => {
    trigger.value = null;
};

const triggerTypes = [
    {
        value: "domains",
        label: i18n.global.t("rulesPage.modals.common.triggers.types.domains.label"),
        description: i18n.global.t("rulesPage.modals.common.triggers.types.domains.description"),
    },
    {
        value: "senderEmails",
        label: i18n.global.t("rulesPage.modals.common.triggers.types.senderEmails.label"),
        description: i18n.global.t("rulesPage.modals.common.triggers.types.senderEmails.description"),
    },
    {
        value: "hasAttachments",
        label: i18n.global.t("rulesPage.modals.common.triggers.types.hasAttachments.label"),
        description: i18n.global.t("rulesPage.modals.common.triggers.types.hasAttachments.description"),
    },
    {
        value: "categories",
        label: `✨ ${i18n.global.t("constants.category")}`,
        description: i18n.global.t("rulesPage.modals.common.triggers.types.categories.label"),
    },
    {
        value: "priorities",
        label: `✨ ${i18n.global.t("constants.priority")}`,
        description: i18n.global.t("rulesPage.modals.common.triggers.types.priorities.label"),
    },
    {
        value: "answers",
        label: `✨ ${i18n.global.t("rulesPage.modals.common.triggers.types.answers.label")}`,
        description: i18n.global.t("rulesPage.modals.common.triggers.types.answers.description"),
    },
    {
        value: "relevances",
        label: `✨ ${i18n.global.t("rulesPage.modals.common.triggers.types.relevances.label")}`,
        description: i18n.global.t("rulesPage.modals.common.triggers.types.relevances.description"),
    },
    {
        value: "flags",
        label: `✨ ${i18n.global.t("rulesPage.modals.common.triggers.types.flags.label")}`,
        description: i18n.global.t("rulesPage.modals.common.triggers.types.flags.description"),
    },
];
const availableTriggerTypes = computed(() => triggerTypes);

const actionTypes = [
    {
        value: "setFlags",
        label: i18n.global.t("rulesPage.modals.common.actions.types.setFlags.label"),
        description: i18n.global.t("rulesPage.modals.common.actions.types.setFlags.description"),
    },
    {
        value: "markAs",
        label: i18n.global.t("rulesPage.modals.common.actions.types.markAs.label"),
        description: i18n.global.t("rulesPage.modals.common.actions.types.markAs.description"),
    },
    {
        value: "delete",
        label: i18n.global.t("rulesPage.modals.common.actions.types.delete.label"),
        description: i18n.global.t("rulesPage.modals.common.actions.types.delete.description"),
    },
    {
        value: "setCategory",
        label: i18n.global.t("rulesPage.modals.common.setCategory"),
        description: i18n.global.t("rulesPage.modals.common.actions.types.setCategory.description"),
    },
    {
        value: "setPriority",
        label: i18n.global.t("rulesPage.modals.common.setPriority"),
        description: i18n.global.t("rulesPage.modals.common.actions.types.setPriority.description"),
    },
    {
        value: "setRelevance",
        label: i18n.global.t("rulesPage.modals.common.setRelevance"),
        description: i18n.global.t("rulesPage.modals.common.actions.types.setRelevance.description"),
    },
    {
        value: "setAnswer",
        label: i18n.global.t("rulesPage.modals.common.actions.types.setAnswer.label"),
        description: i18n.global.t("rulesPage.modals.common.actions.types.setAnswer.description"),
    },
    {
        value: "setTransferRecipients",
        label: "Transfer to",
        description: "Define the transfer recipients",
    },
    {
        value: "setReplyPrompt",
        label: "Prompt for AI",
        description: "Define how the AI should reply",
    },
    {
        value: "setReplyRecipients",
        label: "Reply to",
        description: "Define how the AI should reply",
    },
];
const availableActionTypes = computed(() => actionTypes);

// Utility functions
const isTypeUsed = (type: string, currentIndex: number, items: Trigger[]) => {
    return items.some((item, index) => index !== currentIndex && item.type === type);
};

const getOrdinalSuffix = (num: number) => {
    const j = num % 10;
    const k = num % 100;
    if (j === 1 && k !== 11) return "st";
    if (j === 2 && k !== 12) return "nd";
    if (j === 3 && k !== 13) return "rd";
    return "th";
};

const formatLabel = (str: string) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
};

const getOptionsForType = (type: string) => {
    switch (type) {
        case "priorities":
            return priorityOptions;
        case "answers":
            return answerOptions;
        case "relevances":
            return relevanceOptions;
        case "flags":
            return flagOptions;
        default:
            return [];
    }
};

const canAddMoreTriggers = computed(() => {
    return triggers.value.length < triggerTypes.length && triggers.value[triggers.value.length - 1].type !== "";
});
const addTrigger = () => {
    triggers.value.push({ type: "", value: null });
};

const canAddMoreActions = computed(() => {
    return actions.value.length < actionTypes.length && actions.value[actions.value.length - 1].type !== "";
});
const addAction = () => {
    actions.value.push({ type: "", value: null });
};

const priorityOptions: KeyValuePair[] = [
    { key: IMPORTANT, value: i18n.global.t("rulesPage.priorityRule.important") },
    { key: INFORMATIVE, value: i18n.global.t("rulesPage.priorityRule.informative") },
    { key: USELESS, value: i18n.global.t("rulesPage.priorityRule.useless") },
];
const answerOptions: KeyValuePair[] = [
    { key: ANSWER_REQUIRED, value: i18n.global.t("rulesPage.modals.common.triggers.types.answers.options.required") },
    { key: MIGHT_REQUIRE_ANSWER, value: i18n.global.t("rulesPage.modals.common.triggers.types.answers.options.might") },
    { key: NO_ANSWER_REQUIRED, value: i18n.global.t("rulesPage.modals.common.triggers.types.answers.options.none") },
];
const relevanceOptions: KeyValuePair[] = [
    { key: HIGHLY_RELEVANT, value: i18n.global.t("rulesPage.modals.common.triggers.types.relevances.options.high") },
    {
        key: POSSIBLY_RELEVANT,
        value: i18n.global.t("rulesPage.modals.common.triggers.types.relevances.options.possible"),
    },
    { key: NOT_RELEVANT, value: i18n.global.t("rulesPage.modals.common.triggers.types.relevances.options.none") },
];
const flagOptions: KeyValuePair[] = [
    { key: SPAM, value: i18n.global.t("rulesPage.modals.common.triggers.types.flags.options.spam") },
    { key: SCAM, value: i18n.global.t("rulesPage.modals.common.triggers.types.flags.options.scam") },
    { key: NEWSLETTER, value: i18n.global.t("rulesPage.modals.common.triggers.types.flags.options.newsletter") },
    { key: NOTIFICATION, value: i18n.global.t("rulesPage.modals.common.triggers.types.flags.options.notification") },
    { key: MEETING, value: i18n.global.t("rulesPage.modals.common.triggers.types.flags.options.meeting") },
];
const markAsOptions: KeyValuePair[] = [
    { key: "read", value: i18n.global.t("rulesPage.modals.common.actions.types.markAs.options.read") },
    { key: "answerLater", value: i18n.global.t("rulesPage.modals.common.actions.types.markAs.options.answerLater") },
    { key: "archive", value: i18n.global.t("rulesPage.modals.common.actions.types.markAs.options.archive") },
];
const categoryOptions = computed(() => props.categories);

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

watch(
    triggers,
    (newTriggers) => {
        newTriggers.forEach((trigger) => {
            if ((trigger.type === "domains" || trigger.type === "senderEmails") && trigger.value === null) {
                trigger.value = [];
            }
        });
    },
    { deep: true }
);

watch(
    actions,
    (newActions) => {
        newActions.forEach((action) => {
            if (action.type === "setTransferRecipients" && action.value === null) {
                action.value = [];
            }
        });
    },
    { deep: true }
);

// Watch prop changes for isOpen
watch(
    () => props.isOpen,
    (newValue) => {
        isOpen.value = newValue;
    }
);

const closeModal = () => {
    errorMessage.value = "";
    emit("update:isOpen", false);
};

const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === "Escape") {
        closeModal();
    }
};

const handleSubmit = async () => {
    triggers.value.forEach((trigger) => {
        switch (trigger.type) {
            case "domains":
                formData.value.domains = trigger.value;
                break;
            case "senderEmails":
                formData.value.senderEmails = trigger.value;
                break;
            case "hasAttachments":
                formData.value.hasAttachements = trigger.value;
                break;
            case "categories":
                formData.value.categories = trigger.value;
                break;
            case "priorities":
                formData.value.priorities = trigger.value.map((item: any) => item.key || item);
                break;
            case "answers":
                formData.value.answers = trigger.value.map((item: any) => item.key || item);
                break;
            case "relevances":
                formData.value.relevances = trigger.value.map((item: any) => item.key || item);
                break;
            case "flags":
                formData.value.flags = trigger.value.map((item: any) => item.key || item);
                break;
        }
    });

    actions.value.forEach((action) => {
        switch (action.type) {
            case "setFlags":
                formData.value.actionSetFlags = action.value.map((item: any) => item.key || item);
                break;
            case "markAs":
                formData.value.actionMarkAs = action.value.map((item: any) => item.key || item);
                break;
            case "delete":
                formData.value.actionDelete = action.value;
                break;
            case "setCategory":
                formData.value.actionSetCategory = action.value;
                break;
            case "setPriority":
                formData.value.actionSetPriority = action.value;
                break;
            case "setRelevance":
                formData.value.actionSetRelevance = action.value;
                break;
            case "setAnswer":
                formData.value.actionSetAnswer = action.value;
                break;
            case "setTransferRecipients":
                formData.value.actionTransferRecipients = action.value;
        }
    });

    const result = await postData("user/rules/", formData.value);
    if (!result.success) {
        errorMessage.value = result.error as string;
        return;
    }
    displayPopup?.(
        "success",
        i18n.global.t("constants.popUpConstants.successMessages.success"),
        i18n.global.t("rulesPage.popUpConstants.successMessages.ruleCreatedSuccessfully")
    );
    emit("fetch-rules");
    closeModal();
};

const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

const validateDomain = (domain: string) => {
    const cleanDomain = domain.startsWith("@") ? domain.slice(1) : domain;
    const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9](\.[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])+$/;
    return domainRegex.test(cleanDomain);
};

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});
</script>

<style>
/* Styles for vue-multiselect with a neutral (gray) scheme */
.multiselect-gray {
    --ms-font-size: 0.875rem;
}

.multiselect-gray .multiselect__tags {
    min-height: 38px;
    padding: 0.375rem 0.75rem;
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: var(--ms-font-size);
    display: flex;
    align-items: center;
}

.multiselect-gray .multiselect__placeholder {
    color: #6b7280;
    margin: 0;
    padding: 0;
}

.multiselect-gray .multiselect__input {
    background: transparent;
    font-size: var(--ms-font-size);
    margin: 0;
    padding: 0;
}

.multiselect-gray .multiselect__single {
    margin: 0;
    padding: 0;
    line-height: normal;
}

.multiselect-gray .multiselect__tags-wrap {
    display: inline-flex;
    align-items: center;
    margin: 0;
    padding: 0;
}

.multiselect-gray .multiselect__tag {
    background-color: #f3f4f6;
    color: #374151;
    border-radius: 0.25rem;
    margin: 2px 4px 2px 0;
    padding: 4px 8px;
    padding-right: 2rem;
    position: relative;
    display: inline-block;
}

.multiselect-gray .multiselect__tag-icon {
    position: absolute;
    right: 0.5rem;
    top: 6.5px;
    transform: translateY(-50%);
    color: #374151 !important;
    cursor: pointer;
}

.multiselect-gray .multiselect__tag-icon:hover {
    background: none !important;
    color: #111827 !important;
}

.multiselect-gray .multiselect__tag-icon:after {
    color: inherit !important;
}

.multiselect-gray .multiselect__tag-icon[title] {
    pointer-events: none;
}

.multiselect-gray .multiselect__content-wrapper {
    border: 1px solid #e5e7eb;
    border-top: none;
    border-radius: 0 0 0.375rem 0.375rem;
}

.multiselect-gray .multiselect__option {
    padding: 0.5rem 0.75rem;
    font-size: var(--ms-font-size);
    color: #374151;
    min-height: 40px;
    display: flex;
    align-items: center;
}

.multiselect-gray .multiselect__option--selected {
    background-color: #f9fafb;
    color: #111827;
    font-weight: 500;
}

.multiselect-gray .multiselect__option--highlight {
    background-color: #f3f4f6;
    color: #111827;
}

.multiselect-gray .multiselect__option--selected.multiselect__option--highlight {
    background-color: #f3f4f6;
    color: #111827;
}

.multiselect-gray .multiselect--active .multiselect__tags {
    outline: none;
}

.multiselect-gray .multiselect__tags:focus-within {
    outline: none;
    box-shadow: 0 0 0 2px rgb(31 41 55 / 0.2);
}

.multiselect-gray .multiselect__input:focus {
    outline: none;
    box-shadow: none;
}

.multiselect-gray.multiselect--active {
    outline: none;
}

.multiselect-gray .multiselect__option:after {
    display: none;
}

.multiselect-gray .multiselect__option {
    padding-right: 0.75rem !important;
}
</style>
