<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />
    <div class="flex flex-col justify-center bg-white items-center h-screen">
        <div class="flex h-full w-full">
            <div class="w-[90px] 2xl:w-[100px] ring-1 ring-black ring-opacity-5">
                <NavBarSmall />
            </div>
            <div class="flex-1">
                <div class="flex flex-col h-full divide-y divide-gray-200">
                    <div class="flex items-center justify-center h-[70px] 2xl:h-[80px] border-l bg-gray-50">
                        <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500">
                            {{ $t("constants.userActions.replyLater") }}
                        </h1>
                    </div>
                    <div class="flex-grow overflow-y-auto" style="margin-right: 2px">
                        <div class="px-4 py-2 h-full">
                            <div v-if="nbrReplyAnswer == 0" class="py-2 w-full h-full">
                                <div
                                    class="flex items-center justify-center w-full h-full rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 text-center"
                                    @click="showModal = true"
                                >
                                    <div class="flex-col">
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke-width="1.5"
                                            stroke="currentColor"
                                            class="w-12 h-12 mx-auto text-gray-400"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                d="M9 15 3 9m0 0 6-6M3 9h12a6 6 0 0 1 0 12h-3"
                                            />
                                        </svg>
                                        <span class="mt-2 block text-sm font-semibold text-gray-900">
                                            {{ $t("replyLaterPage.noEmailsToReplyLater") }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div v-if="nbrReplyAnswer > 0">
                                <ul role="list" class="flex flex-col w-full h-full rounded-xl">
                                    <div class="pt-6">
                                        <li v-if="emails[IMPORTANT] && emails[IMPORTANT].length > 0" class="">
                                            <div class="px-6 pb-6">
                                                <div class="bg-orange-100 bg-opacity-90 rounded-md">
                                                    <div class="flex px-3 py-2">
                                                        <p
                                                            class="flex-1 text-sm font-semibold leading-6 text-orange-600"
                                                        >
                                                            {{ $t("constants.ruleModalConstants.important") }}
                                                        </p>

                                                        <div class="ml-auto">
                                                            <exclamation-triangle-icon
                                                                class="w-6 h-6 text-orange-500"
                                                            />
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="flex px-4 pt-4">
                                                    <div class="flex">
                                                        <span
                                                            class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-orange-300"
                                                        >
                                                            <svg
                                                                xmlns="http://www.w3.org/2000/svg"
                                                                fill="none"
                                                                viewBox="0 0 24 24"
                                                                stroke-width="1.5"
                                                                stroke="currentColor"
                                                                class="w-6 h-6 text-white"
                                                            >
                                                                <path
                                                                    stroke-linecap="round"
                                                                    stroke-linejoin="round"
                                                                    d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z"
                                                                />
                                                            </svg>
                                                        </span>
                                                    </div>
                                                    <div class="ml-6 flex-grow">
                                                        <div
                                                            class="overflow-hidden border-l-4 border-orange-300 hover:rounded-l-xl"
                                                            style="overflow: visible"
                                                        >
                                                            <ul
                                                                role="list"
                                                                class="divide-y divide-gray-200 dark:divide-white"
                                                            >
                                                                <li
                                                                    v-for="email in emails[IMPORTANT]"
                                                                    :key="email.id"
                                                                    class="px-6 md:py-2 2xl:py-4 hover:bg-opacity-70 grid grid-cols-10 gap-4 items-center"
                                                                >
                                                                    <Email :email="email" :color="orange" />
                                                                    <!-- <ImportantEmail :email="email" /> -->
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </li>
                                        <li v-if="emails[INFORMATIVE] && emails[INFORMATIVE].length > 0" class="">
                                            <div class="px-6 pb-6">
                                                <div class="bg-blue-100 bg-opacity-90 rounded-md">
                                                    <div class="flex px-2 py-2">
                                                        <p class="flex-1 text-sm font-semibold leading-6 text-blue-600">
                                                            {{ $t("constants.ruleModalConstants.informative") }}
                                                        </p>

                                                        <div class="ml-auto">
                                                            <information-circle-icon class="w-6 h-6 text-blue-500" />
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="flex px-4 pt-4">
                                                    <div class="flex">
                                                        <span
                                                            class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-blue-400 dark:bg-blue-200"
                                                        >
                                                            <svg
                                                                xmlns="http://www.w3.org/2000/svg"
                                                                fill="none"
                                                                viewBox="0 0 24 24"
                                                                stroke-width="1.5"
                                                                stroke="currentColor"
                                                                class="w-6 h-6 text-white"
                                                            >
                                                                <path
                                                                    stroke-linecap="round"
                                                                    stroke-linejoin="round"
                                                                    d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z"
                                                                />
                                                            </svg>
                                                        </span>
                                                    </div>
                                                    <div class="ml-6 flex-grow">
                                                        <div
                                                            class="overflow-hidden border-l-4 hover:rounded-l-xl border-blue-300"
                                                            style="overflow: visible"
                                                        >
                                                            <ul
                                                                role="list"
                                                                class="divide-y divide-gray-200 dark:divide-white"
                                                            >
                                                                <li
                                                                    v-for="email in emails[INFORMATIVE]"
                                                                    :key="email.id"
                                                                    class="px-6 md:py-2 2xl:py-4 hover:bg-opacity-70 dark:hover:bg-blue-500 dark:hover:bg-opacity-100 grid grid-cols-10 gap-4 items-center"
                                                                >
                                                                    <Email :email="email" :color="blue" />
                                                                    <!-- <InformativeEmail :email="email" /> -->
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </li>
                                        <div v-if="emails[USELESS] && emails[USELESS].length > 0" class="">
                                            <div class="px-6 pb-6">
                                                <div class="bg-gray-200 bg-opacity-90 rounded-md">
                                                    <div class="flex px-2 py-2">
                                                        <p class="flex-1 text-sm font-semibold leading-6 text-gray-600">
                                                            {{ $t("constants.ruleModalConstants.useless") }}
                                                        </p>

                                                        <div class="ml-auto">
                                                            <trash-icon class="w-6 h-6 text-gray-500" />
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="flex px-4 pt-4">
                                                    <div class="flex">
                                                        <span
                                                            class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-500"
                                                        >
                                                            <svg
                                                                xmlns="http://www.w3.org/2000/svg"
                                                                fill="none"
                                                                viewBox="0 0 24 24"
                                                                stroke-width="1.5"
                                                                stroke="currentColor"
                                                                class="w-6 h-6 text-white"
                                                            >
                                                                <path
                                                                    stroke-linecap="round"
                                                                    stroke-linejoin="round"
                                                                    d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z"
                                                                />
                                                            </svg>
                                                        </span>
                                                    </div>
                                                    <div class="ml-6 flex-grow">
                                                        <div
                                                            class="overflow-hidden border-l-4 hover:rounded-l-xl border-gray-400"
                                                            style="overflow: visible"
                                                        >
                                                            <ul
                                                                role="list"
                                                                class="divide-y divide-gray-200 dark:divide-white"
                                                            >
                                                                <li
                                                                    v-for="email in emails[USELESS]"
                                                                    :key="email.id"
                                                                    class="px-6 md:py-2 2xl:py-4 hover:bg-opacity-70 grid grid-cols-10 gap-4 items-center"
                                                                >
                                                                    <Email :email="email" :color="gray" />
                                                                    <!-- <UselessEmail :email="email" /> -->
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
/* eslint-disable */
import { ref, onMounted } from "vue";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import {
    ChatBubbleOvalLeftEllipsisIcon,
    TrashIcon,
    ArrowUturnLeftIcon,
    EllipsisHorizontalIcon,
    EyeIcon,
    InformationCircleIcon,
    ExclamationTriangleIcon,
} from "@heroicons/vue/24/outline";
import NavBarSmall from "@/components/NavBarSmall.vue";
import { fetchWithToken } from "@/global/security";
import { API_BASE_URL, IMPORTANT, INFORMATIVE, USELESS } from "@/global/const";
import { useRouter } from "vue-router";
import { i18n } from "@/global/Settings/preferences";

// const router = useRouter()

// interface Email {
//     id: string
//     email: string
//     id_provider: string
//     details: string
// }

// interface EmailsData {
//     [key: string]: Email[]
// }

// const showModal = ref<boolean>(false)

// const answerLaterEmails = ref<EmailsData>({})
// const emails = ref<EmailsData>({})
// const nbrReplyAnswer = ref(0)
// const showHiddenParagraphs = ref<{ [key: number]: boolean }>({})
// const animationTriggered = ref<boolean[]>([false, false, false])
// const hoveredItemId = ref<string | null>(null)
// const showTooltip = ref(true)
// const isDropdownOpen = ref(false)
// const isMenuOpen = ref(true)

// const showNotification = ref(false)
// const notificationTitle = ref("")
// const notificationMessage = ref("")
// const backgroundColor = ref("")
// const timerId = ref<number | null>(null)

// onMounted(() => {
//     fetchAnswerLaterEmails()
// })

// function computeEmailsLength(data: EmailsData): number {
//     return Object.values(data).reduce((total, ids) => total + ids.length, 0)
// }

// async function fetchAnswerLaterEmails() {
//     try {
//         const response = await fetchWithToken(`${API_BASE_URL}user/get_answer_later_emails/`, {
//             method: "GET",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//         })

//         if (!response) {
//             displayPopup("error", "No response from server", "Verify your internet connection")
//             return
//         }

//         if (!response.ok) {
//             displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`)
//             return
//         }

//         const data = await response.json()

//         emails.value = data
//         nbrReplyAnswer.value = computeEmailsLength(data)
//         answerLaterEmails.value = data
//     } catch (error) {
//         console.error(error)
//     }
// }

// function toggleHiddenParagraph(index: number) {
//     showHiddenParagraphs.value[index] = !showHiddenParagraphs.value[index]
// }

// function animateHiddenText(element: HTMLElement, delay = 0) {
//     const characters = element.dataset.text?.split("") || []
//     const duration = characters.length * 5
//     setTimeout(() => {
//         element.textContent = ""
//         let currentIndex = 0
//         const interval = setInterval(() => {
//             if (currentIndex < characters.length) {
//                 element.textContent += characters[currentIndex]
//                 currentIndex++
//             } else {
//                 clearInterval(interval)
//             }
//         }, 5)
//     }, delay)
//     return duration
// }

// function openRuleEditor(ruleId: string) {
//     if (ruleId) {
//         router.push({ name: "rules", query: { id_rule: ruleId, edit_rule: "true" } })
//     }
// }

// function openNewRule(ruleName: string, ruleEmail: string) {
//     if (ruleName && ruleEmail) {
//         router.push({ name: "rules", query: { rule_name: ruleName, rule_email: ruleEmail, edit_rule: "false" } })
//     }
// }

// function setHoveredItem(id: string) {
//     hoveredItemId.value = id
// }

// function clearHoveredItem() {
//     hoveredItemId.value = null
// }

// function toggleTooltip() {
//     showTooltip.value = false
//     isDropdownOpen.value = true
// }

// function openInNewWindow() {
//     console.log("TODO: use the modal Théo has created")
// }

// async function unmarkReplyLater(emailId: string) {
//     deleteEmailFromState(emailId)

//     try {
//         const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/unmark_reply-later/`, {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//         })

//         if (!response) {
//             displayPopup("error", "No response from server", "Verify your internet connection")
//             return
//         }

//         if (!response.ok) {
//             displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`)
//             return
//         }

//         const data = await response.json()

//         if (data.answer_later !== false) {
//             displayPopup("error", i18n.global.t("replyLaterPage.markEmailNotReplyLaterFailure"), JSON.stringify(data))
//         }
//     } catch (error) {
//         displayPopup("error", i18n.global.t("replyLaterPage.markEmailNotReplyLaterFailure"), (error as Error).message)
//     }
//     fetchAnswerLaterEmails()
// }

// async function openAnswer(email: Email) {
//     const url = `${API_BASE_URL}api/get_mail_by_id?email_id=${email.id_provider}`

//     try {
//         const response = await fetchWithToken(url, {
//             method: "GET",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//         })

//         if (!response) {
//             displayPopup("error", "No response from server", "Verify your internet connection")
//             return
//         }

//         if (!response.ok) {
//             displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`)
//             return
//         }

//         const data = await response.json()

//         let cleanedCc =
//             data.email.cc && data.email.cc.length > 0
//                 ? JSON.stringify(data.email.cc[0].split(",").map((email: string) => email.trim()))
//                 : "[]"

//         router.push({
//             name: "answer",
//             query: {
//                 subject: JSON.stringify(data.email.subject),
//                 cc: cleanedCc,
//                 bcc: JSON.stringify(data.email.bcc),
//                 decoded_data: JSON.stringify(data.email.decoded_data),
//                 email: JSON.stringify(email.email),
//                 id_provider: JSON.stringify(email.id_provider),
//                 details: JSON.stringify(email.details),
//             },
//         })
//     } catch (error) {
//         displayPopup(
//             "error",
//             i18n.global.t("constants.popUpConstants.errorMessages.openReplyPageFailure"),
//             (error as Error).message
//         )
//     }
// }

// async function transferEmail(email: Email) {
//     const url = `${API_BASE_URL}api/get_mail_by_id?email_id=${email.id_provider}`

//     try {
//         const response = await fetchWithToken(url, {
//             method: "GET",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//         })

//         if (!response) {
//             displayPopup("error", "No response from server", "Verify your internet connection")
//             return
//         }

//         if (!response.ok) {
//             displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`)
//             return
//         }

//         const data = await response.json()

//         let cleanedCc =
//             data.email.cc && data.email.cc.length > 0
//                 ? JSON.stringify(data.email.cc[0].split(",").map((email: string) => email.trim()))
//                 : "[]"

//         router.push({
//             name: "transfer",
//             query: {
//                 subject: JSON.stringify(data.email.subject),
//                 cc: cleanedCc,
//                 decoded_data: JSON.stringify(data.email.decoded_data),
//                 email: JSON.stringify(email.email),
//                 details: JSON.stringify(email.details),
//                 date: JSON.stringify(data.email.date),
//             },
//         })
//     } catch (error) {
//         displayPopup(
//             "error",
//             i18n.global.t("constants.popUpConstants.errorMessages.openTransferPageFailure"),
//             (error as Error).message
//         )
//     }
// }

// async function deleteEmail(emailId: string) {
//     deleteEmailFromState(emailId)

//     try {
//         const response = await fetchWithToken(`${API_BASE_URL}user/emails/${emailId}/delete/`, {
//             method: "DELETE",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//         })

//         if (!response) {
//             displayPopup("error", "No response from server", "Verify your internet connection")
//             return
//         }

//         if (!response.ok) {
//             displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`)
//             return
//         }

//         const data = await response.json()

//         if (data.message) {
//             nbrReplyAnswer.value -= 1
//         } else {
//             displayPopup(
//                 "error",
//                 i18n.global.t("constants.popUpConstants.errorMessages.deleteEmailFailure"),
//                 data.error
//             )
//         }
//     } catch (error) {
//         displayPopup(
//             "error",
//             i18n.global.t("constants.popUpConstants.errorMessages.deleteEmailFailure"),
//             (error as Error).message
//         )
//     }
// }

// function deleteEmailFromState(emailId: string) {
//     for (const category in emails.value) {
//         const emailIndex = emails.value[category].findIndex((email) => email.id === emailId)
//         if (emailIndex !== -1) {
//             emails.value[category].splice(emailIndex, 1)
//             return
//         }
//     }
// }

// function displayPopup(type: "success" | "error", title: string, message: string) {
//     showNotification.value = true
//     notificationTitle.value = title
//     notificationMessage.value = message
//     backgroundColor.value = type === "error" ? "bg-red-500" : "bg-green-500"
//     timerId.value = setTimeout(dismissPopup, 4000)
// }

// function dismissPopup() {
//     showNotification.value = false
//     if (timerId.value !== null) {
//         clearTimeout(timerId.value)
//     }
// }
</script>
