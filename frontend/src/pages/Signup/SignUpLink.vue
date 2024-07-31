<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />
    <div class="h-screen flex flex-col px-6 2xl:py-12 lg:px-8 overflow-y-auto">
        <div class="flex-grow flex flex-col justify-center py-4">
            <div class="w-full flex flex-col items-center">
                <div class="flex flex-col 2xl:mt-0 gap-y-1">
                    <img class="mx-auto h-10 w-auto" :src="logo" alt="Aomail" />
                    <h2 class="text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                        {{ $i18n.global.t("signUpPart1Page.signUp") }}
                    </h2>
                </div>
                <div class="2xl:mt-6 sm:mt-4 sm:mx-auto sm:w-full sm:max-w-[545px]">
                    <div class="flex flex-col">
                        <div class="">
                            <div class="flex items-center justify-center h-[65px]">
                                <nav aria-label="Progress">
                                    <ol
                                        role="list"
                                        class="flex items-center"
                                        v-for="(stepItem, index) in steps"
                                        :key="index"
                                        v-if="step === index"
                                    >
                                        <li v-for="(item, itemIndex) in stepItem" :key="itemIndex" :class="item.class">
                                            <div class="absolute inset-0 flex items-center" aria-hidden="true">
                                                <div class="h-0.5 w-full bg-gray-500"></div>
                                            </div>
                                            <a :class="item.aClass" :aria-current="item.ariaCurrent">
                                                <span
                                                    v-if="item.icon"
                                                    :class="item.iconClass"
                                                    aria-hidden="true"
                                                ></span>
                                                <svg
                                                    v-if="item.svg"
                                                    class="h-5 w-5 text-gray-700"
                                                    viewBox="0 0 20 20"
                                                    fill="currentColor"
                                                    aria-hidden="true"
                                                >
                                                    <path
                                                        fill-rule="evenodd"
                                                        d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                                                        clip-rule="evenodd"
                                                    />
                                                </svg>
                                                <span class="sr-only">{{ item.srOnly }}</span>
                                            </a>
                                        </li>
                                    </ol>
                                </nav>
                            </div>
                            <div class="bg-white px-6 py-4 sm:px-12">
                                <form class="space-y-6">
                                    <div v-if="step === 3">
                                        <div class="flex flex-col">
                                            <StepDivider :text="$t('signUpPart2Page.linkAGmailAccount')" />
                                            <div class="py-4">
                                                <AuthButton
                                                    @click="authorizeGoogle"
                                                    :icon="googleIcon"
                                                    :text="$t('signUpPart2Page.linkYourGmailAccount')"
                                                />
                                            </div>
                                            <StepDivider :text="$t('signUpPart2Page.linkAnOutlookAccount')" />
                                            <div class="pt-4">
                                                <AuthButton
                                                    @click="authorizeMicrosoft"
                                                    :icon="microsoftIcon"
                                                    :text="$t('signUpPart2Page.linkYourOutlookAccount')"
                                                />
                                            </div>
                                            <div>
                                                <div class="pt-10">
                                                    <ContinueButton @click="nextStep3" />
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div v-if="step === 4">
                                        <div class="flex flex-col">
                                            <StepDivider :text="$t('signUpPart2Page.toolsPresentation')" />
                                            <div class="py-6">
                                                <div class="relative items-stretch mt-2">
                                                    <p class="font-semibold">
                                                        {{ $i18n.global.t("constants.workInProgress") }}
                                                    </p>
                                                </div>
                                            </div>
                                            <StepDivider
                                                :text="$t('signUpPart2Page.informationOnDataConfidentiality')"
                                            />
                                            <div class="pt-4">
                                                <div class="relative items-stretch mt-2">
                                                    <p class="font-semibold">
                                                        {{ $i18n.global.t("constants.workInProgress") }}
                                                    </p>
                                                </div>
                                            </div>
                                            <div>
                                                <div class="pt-8">
                                                    <SubmitButton @click="submitSignupData" />
                                                </div>
                                            </div>
                                            <div class="space-y-5 pt-3">
                                                <TermsCheckbox v-model="termsAccepted" />
                                            </div>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                    <p class="mt-6 text-center text-sm text-gray-500">
                        {{ $i18n.global.t("signUpPart1Page.youHaveAnAccount") }}
                        <a href="/" class="font-semibold leading-6 text-gray-900 hover:text-black">
                            {{ $i18n.global.t("constants.userActions.login") }}
                        </a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import NotificationTimer from "@/components/NotificationTimer.vue"
import { useRouter } from "vue-router"
import { API_BASE_URL } from "@/global/const"
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp"
import { i18n } from "@/global/Settings/preferences"
import logo from "@/assets/logo-aomail.png"

const showNotification = ref(false)
const notificationTitle = ref("")
const notificationMessage = ref("")
const backgroundColor = ref("")
const timerId = (ref < NodeJS.Timeout) | (null > null)
const step = ref(3)
const router = useRouter()

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown)
})

function handleKeyDown(event) {
    if (event.key === "Enter") {
        event.preventDefault()

        if (step.value == 3) {
            nextStep3(event)
        }
    }
}
function authorize_google(event) {
    event.preventDefault()
    sessionStorage.setItem("type_api", "google")

    // Redirect the user to the authorization URL
    window.location.replace(`${API_BASE_URL}google/auth_url/`)
}
function authorize_microsoft(event) {
    event.preventDefault()
    sessionStorage.setItem("type_api", "microsoft")

    // Redirect the user to the authorization URL
    window.location.replace(`${API_BASE_URL}microsoft/auth_url/`)
}

async function nextStep3(event) {
    event.preventDefault()
    // After redirection, get the authorization code from the current URL
    const urlParams = new URLSearchParams(window.location.search)
    const authorizationCode = urlParams.gei18n.global.t("code")

    if (authorizationCode) {
        sessionStorage.setItem("code", authorizationCode)
        step.value++
    } else {
        // Show the pop-up
        backgroundColor.value = "bg-red-200/[.89] border border-red-400"
        notificationTitle.value = i18n.global.t("signUpPart2Page.authorizationError")
        notificationMessage.value = i18n.global.t("signUpPart2Page.authorizationCodeNotFound")
        displayPopup()
    }
}

async function submitSignupData(event) {
    event.preventDefault()

    const checkbox = document.getElementById("comments")
    const label = document.querySelector('label[for="comments"]')
    const link = document.querySelector('label[for="comments"] a')

    // Vérifier si la checkbox est cochée
    if (!checkbox.checked) {
        console.log("The user has not accepted our terms")
        label.classList.add("text-red-500")
        label.classList.remove("text-gray-500")
        link.classList.add("text-red-500")
        link.classList.remove("text-black")

        // Show the pop-up
        backgroundColor.value = "bg-red-200/[.89] border border-red-400"
        notificationTitle = i18n.global.t("signUpPart2Page.AcceptTerms")
        displayPopup()

        return
    } else {
        console.log("The user has accepted our terms")
        label.classList.remove("text-red-500")
        label.classList.add("text-gray-500")
        link.classList.remove("text-red-500")
        link.classList.add("text-black")
    }

    // Show the pop-up
    backgroundColor.value = "bg-green-200/[.89] border border-green-400"
    notificationTitle.value = "Création de compte en cours..."
    notificationMessage.value = "Attente de réponse de la base de données"
    displayPopup()

    try {
        // Prepare the data for registration
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                login: sessionStorage.getItem("login"),
                password: sessionStorage.getItem("password"),
                timezone: localStorage.getItem("timezone"),
                language: localStorage.getItem("language"),
                theme: localStorage.getItem("theme"),
                color: localStorage.getItem("bgColor"),
                categories: localStorage.getItem("categories"),
                code: sessionStorage.getItem("code"),
                type_api: sessionStorage.getItem("type_api"),
                userDescription: sessionStorage.getItem("userDescription"),
            }),
        }

        // READY TO REGISTER THE USER IN DATABASE
        const response = await fetch(`${API_BASE_URL}signup/`, requestOptions)
        const data = await response.json()

        if (response.status === 201) {
            // Django access token
            localStorage.setItem("access_token", data.access_token)
            sessionStorage.clear()
            localStorage.removeItem("categories")
            // Redirect to the home page once signed in
            router.push({ name: "home" })
        } else if (data.error == "Email address already used") {
            // Show the pop-up
            backgroundColor.value = "bg-red-200/[.89] border border-red-400"
            notificationTitle.value = i18n.global.t("signUpPart2Page.accountCreationError")
            notificationMessage.value = i18n.global.t("constants.popUpConstants.errorMessages.emailAlreadyUsed")
            displayPopup()
        } else {
            // Show the pop-up
            backgroundColor.value = "bg-red-200/[.89] border border-red-400"
            notificationTitle.value = i18n.global.t("signUpPart2Page.accountCreationError")
            notificationMessage.value = data.error
            displayPopup()
        }
    } catch (error) {
        // Show the pop-up
        backgroundColor.value = "bg-red-200/[.89] border border-red-400"
        notificationTitle.value = i18n.global.t("signUpPart2Page.accountCreationError")
        notificationMessage.value = error
        displayPopup()
    }
}

function displayPopup(type: "success" | "error", title: string, message: string) {
    if (type === "error") {
        displayErrorPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message)
    } else {
        displaySuccessPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message)
    }
    timerId.value = setTimeout(dismissPopup, 4000)
}

function dismissPopup() {
    showNotification.value = false
    if (timerId.value !== null) {
        clearTimeout(timerId.value)
    }
}

const showNotification = ref < boolean > false
const notificationTitle = ref < string > ""
const notificationMessage = ref < string > ""
const backgroundColor = ref < string > ""
const timerId = (ref < NodeJS.Timeout) | (null > null)
</script>

<script>
export default {
    data() {
        return {
            isOpen: false, 
        }
    },
    methods: {
        closeModal() {
            this.isOpen = false
        },
    },
}
</script>

<!-- TODO: FOLLOW these guidelines anyway
the import of constants and function are correct. You must do the following operations:
 
put EVERYTHING under script setup for consitency
remove all comments no execption
use strictly camelCase for vars and functions
we are using TypeScript so migrate everything where its needed using interfaces or types -->

everywhere 
// Show the pop-up is written you must use the function that I coded 

like that for example: displayPopup("error", "userLoginPage.loginError", "userLoginPage.maxUsernameLength")

<!-- 
REMOVE THIS and only use script setup

export default {
  data() {
      return {
          isOpen: false, 
      }
  },
  methods: {
      closeModal() {
          this.isOpen = false
      },
  },
} -->