<template>
    <div class="flex space-x-1 2xl:space-x-2 items-stretch w-full mb-4">
        <div class="relative w-full">
            <div class="flex w-full">
                <div class="relative flex-grow">
                    <div
                        v-if="!isFocused && !inputValue"
                        class="absolute top-0 left-0 flex space-x-1 items-center pointer-events-none opacity-50 transition-opacity duration-200 h-full ml-2 2xl:ml-3"
                    >
                        <magnifying-glass-icon class="w-4 h-4 pointer-events-none 2xl:w-5 2xl:h-5" />
                        <label
                            for="search"
                            class="block text-sm font-medium leading-6 text-gray-900 pointer-events-none 2xl:text-base"
                        >
                            {{ $t("searchPage.searchPlaceholder") }}
                        </label>
                    </div>
                    <input
                        id="searchInput"
                        v-model="inputValue"
                        type="text"
                        class="block rounded-l-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-gray-500 h-10 2xl:h-11 flex-1 border-0 bg-transparent py-2 pl-3 text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 w-full z-20 relative 2xl:py-3 2xl:pl-4 2xl:text-base"
                        @focus="handleFocusSearch"
                        @blur="handleBlur"
                        @input="handleInputUpdateSearch"
                        @change="query = $event.target.value"
                    />
                </div>
                <div class="relative">
                    <button
                        type="button"
                        class="group w-full h-full bg-gray-100 rounded-r-md p-2 text-white shadow-sm hover:bg-gray-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 flex items-center justify-center 2xl:px-3 2xl:py-3 ring-1 ring-inset ring-gray-300 hover:ring-transparent shadow-sm"
                        @click="hideFilters()"
                    >
                        <svg
                            class="w-6 h-5 text-gray-400 group-hover:text-white"
                            aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="currentColor"
                            stroke="none"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M10.83 5a3.001 3.001 0 0 0-5.66 0H4a1 1 0 1 0 0 2h1.17a3.001 3.001 0 0 0 5.66 0H20a1 1 0 1 0 0-2h-9.17ZM4 11h9.17a3.001 3.001 0 0 1 5.66 0H20a1 1 0 1 1 0 2h-1.17a3.001 3.001 0 0 1-5.66 0H4a1 1 0 1 1 0-2Zm1.17 6H4 a1 1 0 1 0 0 2h1.17a3.001 3.001 0 0 0 5.66 0H20a1 1 0 1 0 0-2h-9.17a3.001 3.001 0 0 0-5.66 0Z"
                            />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <div class="flex-grow h-full">
            <button
                type="button"
                @click="searchEmails"
                class="w-full h-full bg-gray-700 rounded-md px-2 2xl:px-4 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 flex gap-x-2 items-center justify-between 2xl:px-7 2xl:text-lg"
            >
                {{ $t("searchPage.searchButton") }}
                <magnifying-glass-icon class="w-4 2xl:w-5" />
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject } from "vue";

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

async function hideFilters() {
    const toggleDiv = document.getElementById("filtres");
    const emailListDiv = document.getElementById("emailList");

    if (!toggleDiv || !emailListDiv) return;

    const isHidden = toggleDiv.classList.contains("hidden");

    if (isHidden) {
        toggleDiv.classList.remove("hidden");
        await delay(10);
        toggleDiv.classList.replace("opacity-0", "opacity-100");
        adjustHeight2(emailListDiv, -185);
    } else {
        toggleDiv.classList.replace("opacity-100", "opacity-0");

        await delay(250);
        toggleDiv.classList.add("hidden");
        adjustHeight2(emailListDiv, 185);
    }
}

async function searchEmails() {
    let fileExt = "";
    // for (const key in attachmentSelected.value) {
    //     if (key === "extension") {
    //         fileExt = attachmentSelected.value[key];
    //     }
    // }

    loading();
    scrollToBottom();

    const result = await postData(`user/emails/`, {
        resultPerPage: 25,
        advanced: false,
        subject: query.value,
        senderEmail: query.value,
        senderName: query.value,
    });

    if (!result.success) {
        displayPopup("error", "Failed to fetch emails", result.error as string);
        return;
    }

    if (result.data.count > 0) {
        const limitedEmails = result.data.ids.slice(0, 25);
        const emailDetails = await fetchEmailDetails(limitedEmails);
        // emailList.value = Object.entries(emailDetails.data).flatMap(([category, priorities]) =>
        //     Object.entries(priorities).flatMap(([priority, emails]) =>
        //         emails.map((email) => ({
        //             ...email,
        //             category: category,
        //             priority: priority,
        //         }))
        //     )
        // );

        hideLoading();

        if (result.data.count == 1) {
            await displayMessage(result.data.count + " email " + i18n.global.t("searchPage.oneDataFound"), aiIcon);
        } else if (result.data.count > 1) {
            await displayMessage(result.data.count + " emails " + i18n.global.t("searchPage.severalDataFound"), aiIcon);
        }
    } else {
        await displayMessage(i18n.global.t("searchPage.noDataFound"), aiIcon);
    }
}
</script>
