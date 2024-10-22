<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
    />
    <div class="flex flex-col justify-center items-center h-screen">
        <div class="flex h-full w-full">
            <div class="w-[90px] 2xl:w-[100px] bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <NavBarSmall />
            </div>
            <div class="flex-1 bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <div class="flex flex-col h-full relative divide-y divide-gray-200">
                    <div class="flex items-center justify-center h-[70px] 2xl:h-[80px] bg-gray-50">
                        <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500">
                            {{ $t("constants.userActions.replyLater") }}
                        </h1>
                    </div>
                    <div v-if="!hasEmails" class="flex-1">
                        <div class="flex flex-col w-full h-full rounded-xl">
                            <div
                                class="flex flex-col justify-center items-center h-full m-5 rounded-lg border-2 border-dashed border-gray-400 p-12 text-center hover:border-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1"
                                    stroke="currentColor"
                                    class="mx-auto h-14 w-14 text-gray-400"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
                                    />
                                </svg>
                                <span class="mt-2 block text-md font-semibold text-gray-900">
                                    {{ $t("replyLaterPage.noEmailsToReplyLater") }}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div v-else class="flex-1 overflow-y-auto custom-scrollbar">
                        <ImportantEmail :emails="importantEmails" :replyLater="true" />
                        <InformativeEmail :emails="informativeEmails" :replyLater="true" />
                        <UselessEmail :emails="uselessEmails" :replyLater="true" />
                    </div>
                </div>
            </div>
            <!-- NOT FOR v1 
            <AssistantChat v-if="!isHidden" @toggle-visibility="toggleVisibility" />-->
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, provide } from "vue";
import { postData } from "@/global/fetchData";
import ImportantEmail from "@/global/components/ImportantEmails.vue";
import InformativeEmail from "@/global/components/InformativeEmails.vue";
import UselessEmail from "@/global/components/UselessEmails.vue";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import { Email, FetchDataResult } from "@/global/types";

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);
const emails = ref<{ [key: string]: { [key: string]: Email[] } }>({});
const currentPage = ref(1);
const allEmailIds = ref<string[]>([]);
const isLoading = ref(false);
const emailsPerPage = 10;

provide("emails", emails);

const fetchEmailsData = async () => {
    currentPage.value = 1;
    emails.value = {};
    allEmailIds.value = [];
    let response: FetchDataResult;

    response = await postData("user/emails_ids/", { advanced: true, replyLater: true });

    allEmailIds.value = response.data.ids;

    await loadMoreEmails();
};

const loadMoreEmails = async () => {
    if (isLoading.value) return;
    isLoading.value = true;

    const startIndex = (currentPage.value - 1) * emailsPerPage;
    const endIndex = startIndex + emailsPerPage;
    const idsToFetch = allEmailIds.value.slice(startIndex, endIndex);

    if (idsToFetch.length > 0) {
        const emails_details = await postData("user/get_emails_data/", { ids: idsToFetch });
        const newEmails = emails_details.data.data;

        for (const category in newEmails) {
            if (!emails.value[category]) {
                emails.value[category] = {};
            }
            for (const type in newEmails[category]) {
                if (!emails.value[category][type]) {
                    emails.value[category][type] = [];
                }
                emails.value[category][type].push(...newEmails[category][type]);
            }
        }

        currentPage.value++;
    }

    isLoading.value = false;
};

const handlescroll = () => {
    const container = document.querySelector(".custom-scrollbar");
    if (container) {
        const { scrollTop, scrollHeight, clientHeight } = container;
        const threshold = 250;
        if (scrollTop + clientHeight >= scrollHeight - threshold && !isLoading.value) {
            loadMoreEmails();
        }
    }
};

const scroll = () => {
    const container = document.querySelector(".custom-scrollbar");
    if (container) {
        container.addEventListener("scroll", handlescroll);
    }
};

const importantEmails = computed(() => {
    if (!emails.value) return [];
    const allEmails = Object.values(emails.value).flatMap((category) => category.important || []);
    return allEmails.filter((email) => email.answerLater && !email.read && !email.archive);
});

const informativeEmails = computed(() => {
    if (!emails.value) return [];
    const allEmails = Object.values(emails.value).flatMap((category) => category.informative || []);
    return allEmails.filter((email) => email.answerLater && !email.read && !email.archive);
});

const uselessEmails = computed(() => {
    if (!emails.value) return [];
    const allEmails = Object.values(emails.value).flatMap((category) => category.useless || []);
    return allEmails.filter((email) => email.answerLater && !email.read && !email.archive);
});

const hasEmails = computed(() => {
    if (!emails.value) return false;
    const allEmails = Object.values(emails.value).flatMap((category) => [
        ...(category.important || []),
        ...(category.informative || []),
        ...(category.useless || []),
    ]);
    return allEmails.some((email) => email.answerLater && !email.read && !email.archive);
});

function dismissPopup() {
    showNotification.value = false;
    if (timerId.value !== null) {
        clearTimeout(timerId.value);
    }
}

onMounted(async () => {
    await fetchEmailsData();

    scroll();
});
</script>
