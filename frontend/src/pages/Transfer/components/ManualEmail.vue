<template>
    <div class="flex flex-col h-full w-full">
        <div class="flex items-center h-[65px] justify-center lg:py-5 2xl:h-[80px] min-h-6">
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
                    {{ $t("constants.manualSearch") }}
                </h1>
            </div>
        </div>
        <form class="flex flex-grow w-full px-10">
            <div class="flex flex-col space-y-6 h-full w-full">
                <div class="pt-8">
                    <div class="flex flex-wrap">
                        <div v-if="selectedPeople.length > 0" class="flex items-center mb-1">
                            <div
                                v-for="person in selectedPeople"
                                :key="person.email"
                                class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1"
                            >
                                {{ person.username || person.email }}
                                <button @click="removePersonFromMain(person)">×</button>
                            </div>
                        </div>
                        <div v-if="selectedCC.length > 0" class="flex items-center mb-1">
                            <div
                                v-for="person in selectedCC"
                                :key="person.email"
                                class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1"
                            >
                                <span class="font-semibold mr-1">CC:</span>
                                {{ person.username || person.email }}
                                <button @click="removePersonFromCC(person)">×</button>
                            </div>
                        </div>
                        <div v-if="selectedCCI.length > 0" class="flex items-center mb-1">
                            <div
                                v-for="person in selectedCCI"
                                :key="person.email"
                                class="flex items-center bg-gray-200 rounded px-2 py-1 mr-1"
                            >
                                <span class="font-semibold mr-1">CCI:</span>
                                {{ person.username || person.email }}
                                <button @click="removePersonFromCCI(person)">×</button>
                            </div>
                        </div>
                    </div>
                    <div class="flex items-stretch gap-1">
                        <div class="flex-grow">
                            <div class="relative items-stretch">
                                <div class="relative w-full">
                                    <div
                                        v-if="!isFocused2"
                                        class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2"
                                    >
                                        <UserGroupIcon class="w-4 h-4 pointer-events-none" />
                                        <label
                                            for="email"
                                            class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none"
                                        >
                                            {{ $t("constants.recipient") }}
                                        </label>
                                    </div>
                                    <Combobox as="div" v-model="selectedPerson" @update:model-value="personSelected">
                                        <ComboboxInput
                                            id="recipients"
                                            class="w-full h-10 rounded-md border-0 bg-white py-2 pl-3 pr-12 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-gray-500 sm:text-sm sm:leading-6"
                                            @change="query = $event.target.value"
                                            :display-value="(person) => person?.name"
                                            @focus="handleFocusDestinary"
                                            @blur="handleBlur2($event)"
                                            @keydown.enter="handleEnterKey"
                                        />
                                        <ComboboxButton
                                            class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none"
                                        >
                                            <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                                        </ComboboxButton>
                                        <ComboboxOptions
                                            v-if="filteredPeople.length > 0"
                                            class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                                            style="z-index: 21"
                                        >
                                            <ComboboxOption
                                                v-for="person in filteredPeople"
                                                :key="person.username"
                                                :value="person"
                                                as="template"
                                                v-slot="{ active, selected }"
                                            >
                                                <li
                                                    :class="[
                                                        'relative cursor-default select-none py-2 pl-3 pr-9',
                                                        active ? 'bg-gray-500 text-white' : 'text-gray-900',
                                                    ]"
                                                >
                                                    <div class="flex">
                                                        <span :class="['truncate', selected && 'font-semibold']">
                                                            {{ person.username }}
                                                        </span>
                                                        <span
                                                            :class="[
                                                                'ml-2 truncate text-gray-800',
                                                                active ? 'text-gray-200' : 'text-gray-800',
                                                            ]"
                                                        >
                                                            {{ person.email }}
                                                        </span>
                                                    </div>
                                                    <span
                                                        v-if="selected"
                                                        :class="[
                                                            'absolute inset-y-0 right-0 flex items-center pr-4',
                                                            active ? 'text-white' : 'text-gray-500',
                                                        ]"
                                                    >
                                                        <CheckIcon class="h-5 w-5" aria-hidden="true" />
                                                    </span>
                                                </li>
                                            </ComboboxOption>
                                        </ComboboxOptions>
                                    </Combobox>
                                </div>
                            </div>
                        </div>
                        <div class="flex gap-1">
                            <button
                                type="button"
                                @click="toggleCC"
                                :class="[
                                    'inline-flex items-center gap-x-1.5 rounded-md px-2.5 py-1.5 text-sm font-semibold hover:bg-gray-600 hover:text-white',
                                    activeType === 'CC' ? 'bg-gray-500 text-white' : 'bg-gray-100 text-gray-400',
                                ]"
                                class="ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                            >
                                {{ $t("newPage.carbonCopyInitials") }}
                            </button>
                            <button
                                type="button"
                                @click="toggleCCI"
                                :class="[
                                    'inline-flex items-center gap-x-1.5 rounded-md px-2.5 py-1.5 text-sm font-semibold hover:bg-gray-600 hover:text-white',
                                    activeType === 'CCI' ? 'bg-gray-500 text-white' : 'bg-gray-100 text-gray-400',
                                ]"
                                class="ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
                            >
                                {{ $t("newPage.blindCarbonCopyInitials") }}
                            </button>
                        </div>
                    </div>
                </div>
                <div class="">
                    <div class="flex flex-wrap">
                        <div
                            v-for="(file, index) in uploadedFiles"
                            :key="index"
                            class="flex items-center mb-1 mr-1 bg-gray-200 rounded px-2 py-1"
                        >
                            {{ file.name }}
                            <button @click="removeFile(index)">×</button>
                        </div>
                    </div>
                    <div class="flex items-stretch gap-1">
                        <div class="flex-grow">
                            <div
                                class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 w-full"
                            >
                                <div class="relative w-full">
                                    <div
                                        v-if="!isFocused && !inputValue"
                                        class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 z-10"
                                    >
                                        <Bars2Icon class="w-4 h-4 pointer-events-none" />
                                        <label
                                            for="username"
                                            class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none"
                                        >
                                            {{ $t("newPage.subject") }}
                                        </label>
                                    </div>
                                    <input
                                        id="objectInput"
                                        v-model="inputValue"
                                        type="text"
                                        class="block h-10 flex-1 border-0 bg-transparent py-2 pl-3 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm sm:leading-6 w-full z-20 relative"
                                        @focus="handleFocusObject"
                                        @blur="handleBlur"
                                    />
                                </div>
                            </div>
                        </div>
                        <div class="flex">
                            <input type="file" ref="fileInput" @change="handleFileUpload" multiple hidden />
                            <button
                                @click="triggerFileInput"
                                type="button"
                                class="inline-flex items-center gap-x-1.5 rounded-md bg-gray-100 px-2.5 py-1.5 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-300 shadow-sm hover:ring-transparent hover:bg-gray-600 hover:text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1.5"
                                    stroke="currentColor"
                                    class="w-6 h-6"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13"
                                    />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="flex flex-col flex-grow">
                    <div class="flex-grow mb-20 h-[200px]">
                        <div id="editor" class="w-full"></div>
                    </div>
                    <div class="flex mb-4">
                        <div class="inline-flex rounded-lg shadow-lg">
                            <button
                                @click="sendEmail"
                                :disabled="emailTransfered"
                                class="bg-gray-700 rounded-l-lg px-6 py-2 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center 2xl:px-7 2xl:py-3 2xl:text-lg"
                            >
                                {{ $t("constants.userActions.send") }}
                            </button>

                            <Menu as="div" class="relative -ml-px block">
                                <MenuButton
                                    class="relative inline-flex items-center rounded-r-lg px-2 py-2 text-white border-l border-gray-300 bg-gray-600 hover:bg-gray-700 focus:z-10"
                                >
                                    <span class="sr-only">Open options</span>
                                    <ChevronDownIcon class="h-9 w-5" aria-hidden="true" />
                                </MenuButton>
                                <transition
                                    enter-active-class="transition ease-out duration-100"
                                    enter-from-class="transform opacity-0 scale-95"
                                    enter-to-class="transform opacity-100 scale-100"
                                    leave-active-class="transition ease-in duration-75"
                                    leave-from-class="transform opacity-100 scale-100"
                                    leave-to-class="transform opacity-0 scale-95"
                                >
                                    <MenuItems
                                        class="absolute right-0 z-10 -mr-1 bottom-full mb-2 w-56 origin-bottom-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                                    >
                                        <div class="py-1">
                                            <button
                                                :class="[
                                                    active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                                                    'block px-4 py-2 text-sm',
                                                ]"
                                                @click="scheduleSend"
                                            >
                                                Schedule send
                                            </button>
                                        </div>
                                    </MenuItems>
                                </transition>
                            </Menu>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">

const quill = ref(null);


onMounted(() => {
    localStorage.removeItem("uploadedFiles");
    quill.value = new Quill("#editor", {
        theme: "snow",
        modules: {
            toolbar: toolbarOptions,
        },
    });

    document.addEventListener("keydown", handleKeyDown);

    const subject = JSON.parse(sessionStorage.getItem("subject") || "");
    const cc = sessionStorage.getItem("cc");
    const bcc = sessionStorage.getItem("bcc");
    const decodedData = JSON.parse(sessionStorage.getItem("decoded_data") || "");
    const email = JSON.parse(sessionStorage.getItem("email") || "");
    const details = JSON.parse(sessionStorage.getItem("details") || "");
    const date = JSON.parse(sessionStorage.getItem("date") || "");

    inputValue.value = "Tr : " + subject;
    const formattedDateVar = new Date(date);
    const options: Intl.DateTimeFormatOptions = {
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
    };

    const formattedDate = formattedDateVar.toLocaleDateString("fr-FR", options);

    let forwardedMessage = "";

    forwardedMessage += i18n.global.t("constants.sendEmailConstants.emailSummary") + "\n";
    details.forEach((detail) => {
        forwardedMessage += `- ${detail.text}\n`;
    });
    forwardedMessage += "\n\n";
    forwardedMessage += i18n.global.t("constants.sendEmailConstants.forwardedMessage") + "\n";
    forwardedMessage += i18n.global.t("constants.sendEmailConstants.from") + ` ${email}\n`;
    forwardedMessage += i18n.global.t("constants.sendEmailConstants.date") + ` ${formattedDate}\n`;
    forwardedMessage += i18n.global.t("constants.sendEmailConstants.subject") + ` ${subject}\n`;

    if (cc.length > 0) {
        forwardedMessage += `CC: ${cc}\n`;
    }

    forwardedMessage += "\n\n";
    forwardedMessage += decodedData;

    quill.value.setText(forwardedMessage);

    loadFileMetadataFromLocalStorage();

    window.addEventListener("resize", scrollToBottom);

    aiContainer.value = document.getElementById("AIContainer");

    const message = i18n.global.t("constants.sendEmailConstants.emailRecipientRequest");
    const aiIcon = `<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />`;
    displayMessage(message, aiIcon);
    objectInput.value = document.getElementById("objectInput");

    const form = objectInput.value.closest("form");
    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
        });
    }
});

function handleKeyDown(event: KeyboardEvent): void {
    if (event.key === "Tab") {
        event.preventDefault();

        const editor = document.getElementById("editor");
        const recipients = document.getElementById("recipients");
        const objectInput = document.getElementById("objectInput");
        const dynamicTextarea = document.getElementById("dynamicTextarea");

        if (editor?.contains(document.activeElement)) {
            return;
        } else if (
            selectedCCI.value.length === 0 &&
            selectedCC.value.length === 0 &&
            selectedPeople.value.length === 0 &&
            document.activeElement?.id !== "recipients"
        ) {
            activeType.value = null;
            recipients?.focus();
        } else if (inputValue.value === "" && !isFocused.value) {
            objectInput?.focus();
        } else if (quill.value.root.innerHTML === "<p><br></p>") {
            quill.value.focus();
        } else {
            if (document.activeElement?.id === "recipients") {
                objectInput?.focus();
            } else if (document.activeElement?.id === "dynamicTextarea") {
                recipients?.focus();
            } else {
                dynamicTextarea?.focus();
            }
        }
    } else if (event.ctrlKey) {
        switch (event.key) {
            case "b":
                quill.value.focus();
                event.preventDefault();
                break;
            case "d":
                document.getElementById("recipients")?.focus();
                event.preventDefault();
                break;
            case "k":
                document.getElementById("dynamicTextarea")?.focus();
                event.preventDefault();
                break;
            case "o":
                document.getElementById("objectInput")?.focus();
                event.preventDefault();
                break;
            case "Enter":
                sendEmail();
                break;
        }
    }
}
</script>
