<template>
    <SeeMailModal
        v-if="isSeeMailOpen"
        :isOpen="isSeeMailOpen"
        :email="localEmail"
        @closeModal="closeSeeMailModal"
        @openRule="openRule"
        @markEmailAsRead="markEmailAsRead"
        @markEmailReplyLater="markEmailReplyLater"
        @openAnswer="openAnswer"
        @transferEmail="transferEmail"
    />
    <li class="group flex justify-between items-center py-2 email-item" @click="toggleShowShortSummary()">
        <div class="flex flex-col justify-center">
            <span class="font-semibold text-sm leading-6">
                {{ localEmail.sender.name }}
                - {{ localEmail.sender.email }}
                <span class="font-normal ml-2 text-gray-600 text-xs">
                    {{ localEmail.sentDate }}
                </span>
            </span>
            <span class="text-sm gray-600">{{ localEmail.subject }} - {{ localEmail.oneLineSummary }}</span>
            <div v-if="showShortSummary" class="py-1">
                <p class="text-xs">{{ localEmail.shortSummary }}</p>
            </div>
            <div class="mt-1 flex space-x-2">
                <span
                    v-if="localEmail.priority === 'important'"
                    class="inline-flex items-center rounded-md bg-orange-50 px-2 py-1 text-xs font-medium text-orange-700 ring-1 ring-inset ring-orange-600/10"
                >
                    {{ $t("constants.ruleModalConstants.important") }}
                </span>
                <span
                    v-else-if="localEmail.priority === 'informative'"
                    class="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10"
                >
                    {{ $t("constants.ruleModalConstants.informative") }}
                </span>
                <span
                    v-else
                    class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10"
                >
                    {{ $t("constants.ruleModalConstants.useless") }}
                </span>
                <span
                    class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10"
                >
                    {{ localEmail.category }}
                </span>
                <span
                    v-if="localEmail.read"
                    class="inline-flex items-center rounded-md bg-stone-50 px-2 py-1 text-xs font-medium text-stone-600 ring-1 ring-inset ring-stone-500/10"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke-width="1.5"
                        stroke="currentColor"
                        class="h-4 w-4 mr-1"
                    >
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                    </svg>
                    {{ $t("searchPage.searchIn.read") }}
                </span>
                <span
                    v-bind:class="{
                        'hidden group-hover:block px-1.5 text-white shadow rounded-xl inline-flex': true,
                        'bg-orange-300': localEmail.priority === 'important',
                        'bg-blue-300': localEmail.priority === 'informative',
                        'bg-gray-300': localEmail.priority !== 'important' && localEmail.priority !== 'informative',
                    }"
                >
                    <div class="flex gap-x-1 items-center justify-center h-full">
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
                                d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5"
                            />
                        </svg>
                        <p class="text-xs">
                            {{ $t("constants.userActions.clickToSeeTheSummary") }}
                        </p>
                    </div>
                </span>
            </div>
        </div>
        <span class="isolate inline-flex items-center rounded-2xl">
            <div class="relative group">
                <button
                    @click.stop="openSeeMailModal()"
                    class="border border-black text-black rounded-full px-2 py-1 hover:bg-gray-200 focus:outline-none focus:border-gray-500 flex items-center gap-x-2 justify-center"
                >
                    <EyeIcon class="w-5 h-5" />
                    {{ $t("constants.userActions.see") }}
                </button>
            </div>
        </span>
    </li>
</template>

<script setup lang="ts">
import { getData, postData } from "@/global/fetchData";
import { inject, ref, watch } from "vue";
import { EyeIcon } from "@heroicons/vue/24/outline";
import { Email } from "@/global/types";
import SeeMailModal from "@/global/components/SeeMailModal.vue";
import router from "@/router/router";
import { i18n } from "@/global/preferences";

const props = defineProps<{
    email: Email;
}>();

const showShortSummary = ref(false);
const isSeeMailOpen = ref(false);
const localEmail = ref({ ...props.email });
const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

watch(
    () => props.email,
    (newEmail) => {
        localEmail.value = { ...newEmail };
    },
    { deep: true }
);

function toggleShowShortSummary() {
    showShortSummary.value = !showShortSummary.value;
}

function closeSeeMailModal() {
    isSeeMailOpen.value = false;
}

async function openSeeMailModal() {
    const result = await postData("user/get_email_content/", { id: props.email.id });
    if (!result.success) {
        displayPopup?.("error", "Failed to fetch email content", result.error as string);
        return;
    }
    localEmail.value.htmlContent = result.data.content;
    isSeeMailOpen.value = true;
}

function openRule() {
    if (localEmail.value.rule.hasRule) {
        openRuleEditor();
    } else {
        openNewRule();
    }
}

function openRuleEditor() {
    router.push({ name: "rules", query: { idRule: localEmail.value.rule.ruleId, editRule: "true" } });
}

function openNewRule() {
    router.push({
        name: "rules",
        query: { ruleName: localEmail.value.sender.name, ruleEmail: localEmail.value.sender.email, editRule: "false" },
    });
}

async function markEmailAsRead() {
    const result = await postData(`user/emails/${localEmail.value.id}/mark_read/`, {});
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailReadFailure"), result.error as string);
        return;
    }
    localEmail.value.read = true;
}

async function markEmailReplyLater() {
    const result = await postData(`user/emails/${localEmail.value.id}/mark_reply_later/`, {});
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailReplyLaterFailure"), result.error as string);
        return;
    }
    localEmail.value.answerLater = true;
}

async function openAnswer() {
    const result = await getData(`api/get_mail_by_id?email_id=${localEmail.value.providerId}`);
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("constants.popUpConstants.openReplyPageFailure"), result.error as string);
        return;
    }

    sessionStorage.setItem("subject", JSON.stringify(result.data.subject));
    sessionStorage.setItem("cc", result.data.cc);
    sessionStorage.setItem("bcc", result.data.bcc);
    sessionStorage.setItem("decodedData", JSON.stringify(result.data.decodedData));
    sessionStorage.setItem("emailUser", JSON.stringify(result.data.emailUser));
    sessionStorage.setItem("senderEmail", JSON.stringify(localEmail.value.sender.email));
    sessionStorage.setItem("providerId", JSON.stringify(localEmail.value.providerId));
    sessionStorage.setItem("shortSummary", JSON.stringify(localEmail.value.shortSummary));
    sessionStorage.setItem("importance", JSON.stringify(localEmail.value.priority));

    router.push({ name: "answer" });
}

async function transferEmail() {
    const result = await getData(`api/get_mail_by_id?email_id=${localEmail.value.providerId}`);
    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.transferEmailFailure"), result.error as string);
        return;
    }

    sessionStorage.setItem("subject", JSON.stringify(result.data.email.subject));
    sessionStorage.setItem("cc", result.data.email.cc);
    sessionStorage.setItem("bcc", result.data.email.bcc);
    sessionStorage.setItem("decodedData", JSON.stringify(result.data.email.decodedData));
    sessionStorage.setItem("date", JSON.stringify(result.data.email.date));
    sessionStorage.setItem("providerId", JSON.stringify(localEmail.value.providerId));
    sessionStorage.setItem("email", JSON.stringify(localEmail.value.sender.email));

    router.push({ name: "transfer" });
}
</script>
