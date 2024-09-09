<template>
    <UnlinkEmailModal :isOpen="isUnlinkEmailModalOpen" @closeModal="closeUnlinkEmailModal" />
    <UpdateUserDescriptionModal
        :isOpen="isUpdateUserDescriptionModalOpen"
        @closeModal="closeUpdateUserDescriptionModal"
    />
    <div class="flex items-center justify-center w-full">
        <svg
            v-if="email.typeApi === 'microsoft'"
            xmlns="http://www.w3.org/2000/svg"
            width="21"
            height="21"
            viewBox="0 0 21 21"
        >
            <rect x="1" y="1" width="9" height="9" fill="#f25022" />
            <rect x="1" y="11" width="9" height="9" fill="#00a4ef" />
            <rect x="11" y="1" width="9" height="9" fill="#7fba00" />
            <rect x="11" y="11" width="9" height="9" fill="#ffb900" />
        </svg>
        <svg
            v-if="email.typeApi === 'google'"
            class="-ml-0.5 h-5 w-5"
            aria-hidden="true"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
        >
            <path
                d="M23.4392061,12.2245191 C23.4392061,11.2412519 23.3594198,10.5237252 23.1867481,9.77963359 L11.9587786,9.77963359 L11.9587786,14.2176183 L18.5493435,14.2176183 C18.4165191,15.3205191 17.6989924,16.9814656 16.104458,18.0975573 L16.0821069,18.2461374 L19.6321832,20.9963359 L19.8781374,21.0208855 C22.1369771,18.9347176 23.4392061,15.8652824 23.4392061,12.2245191"
                id="Shape"
                fill="#4285F4"
            ></path>
            <path
                d="M11.9587786,23.9175573 C15.1876031,23.9175573 17.898229,22.8545038 19.8781374,21.0208855 L16.104458,18.0975573 C15.094626,18.8018015 13.7392672,19.2934351 11.9587786,19.2934351 C8.79636641,19.2934351 6.11230534,17.2073588 5.15551145,14.3239695 L5.01526718,14.3358779 L1.32384733,17.1927023 L1.27557252,17.3269008 C3.24210687,21.2334046 7.28152672,23.9175573 11.9587786,23.9175573"
                id="Shape"
                fill="#34A853"
            ></path>
            <path
                d="M5.15551145,14.3239695 C4.90305344,13.5798779 4.75694656,12.7825649 4.75694656,11.9587786 C4.75694656,11.1349008 4.90305344,10.3376794 5.14222901,9.59358779 L5.13554198,9.4351145 L1.3978626,6.53239695 L1.27557252,6.59056489 C0.465068702,8.21166412 0,10.0320916 0,11.9587786 C0,13.8854656 0.465068702,15.7058015 1.27557252,17.3269008 L5.15551145,14.3239695"
                id="Shape"
                fill="#FBBC05"
            ></path>
            <path
                d="M11.9587786,4.62403053 C14.2043359,4.62403053 15.719084,5.59401527 16.5828092,6.40461069 L19.9578321,3.10928244 C17.8850382,1.18259542 15.1876031,0 11.9587786,0 C7.28152672,0 3.24210687,2.68406107 1.27557252,6.59056489 L5.14222901,9.59358779 C6.11230534,6.71019847 8.79636641,4.62403053 11.9587786,4.62403053"
                id="Shape"
                fill="#EB4335"
            ></path>
        </svg>
        <div class="flex-grow"></div>
        <span>{{ email.email }}</span>
        <div class="flex-grow"></div>
        <div>
            <button
                type="button"
                class="inline-flex justify-center items-center rounded-md px-3 py-2 text-sm font-semibold text-gray-800 hover:text-black"
                @click.stop="openUserDescriptionModal?.(email.email)"
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
                        d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
                    />
                </svg>
            </button>
            <button
                type="button"
                class="inline-flex justify-center items-center rounded-md px-3 py-2 text-sm font-semibold text-red-600 hover:text-red-700 hover:bg-transparent"
                @click="openUnLinkModal?.(email.email)"
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
                        d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                    />
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { inject, Ref, ref } from "vue";
import UnlinkEmailModal from "./UnlinkEmailModal.vue";
import UpdateUserDescriptionModal from "./UpdateUserDescriptionModal.vue";
import { EmailLinked } from "@/global/types";

const isUnlinkEmailModalOpen = inject<Ref<boolean>>("isUnlinkEmailModalOpen", ref(false));
const isUpdateUserDescriptionModalOpen = inject<Ref<boolean>>("isUpdateUserDescriptionModalOpen", ref(false));
const openUnLinkModal = inject<(email: string) => void>("openUnLinkModal");
const openUserDescriptionModal = inject<(email: string) => void>("openUserDescriptionModal");
const closeUnlinkEmailModal = inject<() => void>("closeUnlinkEmailModal");
const closeUpdateUserDescriptionModal = inject<() => void>("closeUpdateUserDescriptionModal");

defineProps<{
    email: EmailLinked;
}>();
</script>
