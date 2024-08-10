<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismiss-popup="dismissPopup"
    />
    <div class="flex flex-col justify-center items-center h-screen">
        <div class="flex h-full w-full">
            <div class="w-[90px] 2xl:w-[100px] bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <NavBarSmall />
            </div>
            <div class="flex-1 bg-white ring-1 ring-black ring-opacity-5">
                <div class="flex flex-col h-full">
                    <main class="bg-gray-50 ring-1 ring-black ring-opacity-5">
                        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                            <div class="flex items-center">
                                <div class="w-full flex items-center justify-center py-6 2xl:py-7">
                                    <div class="sm:hidden"></div>
                                    <div class="hidden sm:block w-full">
                                        <nav class="flex justify-center space-x-4 w-full" aria-label="Tabs">
                                            <!-- Current: "bg-gray-200 text-gray-800", Default: "text-gray-600 hover:text-gray-800" -->
                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    {
                                                        'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12':
                                                            activeSection === 'account',
                                                        'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8':
                                                            activeSection !== 'account',
                                                    },
                                                ]"
                                                @click="setActiveSection('account')"
                                            >
                                                <user-icon class="w-4 h-4" />
                                                <a
                                                    :class="{
                                                        'text-gray-800': activeSection === 'account',
                                                        'text-gray-600': activeSection !== 'account',
                                                    }"
                                                    class="text-sm font-medium"
                                                >
                                                    {{ $t("settingsPage.accountPage.myAccountTitle") }}
                                                </a>
                                            </div>
                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    {
                                                        'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12':
                                                            activeSection === 'preferences',
                                                        'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8':
                                                            activeSection !== 'preferences',
                                                    },
                                                ]"
                                                @click="setActiveSection('preferences')"
                                            >
                                                <adjustments-vertical-icon class="w-4 h-4" />
                                                <a
                                                    :class="{
                                                        'text-gray-800': activeSection === 'preferences',
                                                        'text-gray-600': activeSection !== 'preferences',
                                                    }"
                                                >
                                                    {{ $t("settingsPage.preferencesPage.preferencesTitle") }}
                                                </a>
                                            </div>
                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    {
                                                        'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12':
                                                            activeSection === 'subscription',
                                                        'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8':
                                                            activeSection !== 'subscription',
                                                    },
                                                ]"
                                                @click="setActiveSection('subscription')"
                                            >
                                                <credit-card-icon class="w-4 h-4" />
                                                <a
                                                    :class="{
                                                        'text-gray-800': activeSection === 'subscription',
                                                        'text-gray-600': activeSection !== 'subscription',
                                                    }"
                                                    class="text-sm font-medium"
                                                >
                                                    {{ $t("settingsPage.subscriptionPage.subscriptionTitle") }}
                                                </a>
                                            </div>

                                            <div
                                                class="text-sm font-medium cursor-pointer"
                                                :class="[
                                                    'flex space-x-2 items-center rounded-md py-2',
                                                    {
                                                        'bg-gray-500 bg-opacity-10 hover:text-gray-800 px-12':
                                                            activeSection === 'data',
                                                        'hover:bg-gray-500 hover:bg-opacity-10 hover:text-gray-800 px-8':
                                                            activeSection !== 'data',
                                                    },
                                                ]"
                                                @click="setActiveSection('data')"
                                            >
                                                <circle-stack-icon class="w-4 h-4" />
                                                <a
                                                    :class="{
                                                        'text-gray-800': activeSection === 'data',
                                                        'text-gray-600': activeSection !== 'data',
                                                    }"
                                                    class="text-sm font-medium"
                                                >
                                                    {{ $t("settingsPage.dataPage.myData") }}
                                                </a>
                                            </div>
                                        </nav>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </main>

                    <div v-if="activeSection === 'account'">
                        <MyAccountMenu />
                    </div>

                    <div v-if="activeSection === 'subscription'" class="flex-1 section mx-8 my-8 2xl:mx-12 2xl:my-12">
                        <SubscriptionMenu />
                    </div>

                    <div v-if="activeSection === 'data'" class="flex flex-col h-full section">
                        <MyDataMenu />
                    </div>

                    <div v-if="activeSection === 'preferences'" class="flex-1 section">
                        <PreferencesMenu />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
/* eslint-disable */
import { ref, onMounted } from "vue";
import { API_BASE_URL } from "@/global/const";
import { fetchWithToken } from "@/global/security";
import "@fortawesome/fontawesome-free/css/all.css";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { XMarkIcon } from "@heroicons/vue/24/outline";
// import SubscriptionSelection from "@/pages/Settings/components/SubscriptionSelection.vue"
import {
    AdjustmentsVerticalIcon,
    UserIcon,
    EnvelopeIcon,
    KeyIcon,
    CreditCardIcon,
    CircleStackIcon,
} from "@heroicons/vue/24/outline";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import PreferencesMenu from "@/pages/Settings/components/PreferencesMenu.vue";
import MyDataMenu from "@/pages/Settings/components/MyDataMenu.vue";
import SubscriptionMenu from "@/pages/Settings/components/SubscriptionMenu.vue";
import MyAccountMenu from "@/pages/Settings/components/MyAccountMenu.vue";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import NavBarLarge from "@/global/components/NavBarSmall.vue";

// const router = useRouter();

const activeSection = ref("account");
const userData = ref("");
// const userEmailDescription = ref("")
const emailsLinked = ref<string[]>([]);
const newPassword = ref("");
const confirmPassword = ref("");
const isModalOpen = ref(false);
const isModalUserDescriptionOpen = ref(false);
const isUnlinkModalOpen = ref(false);
const isModalAddUserDescriptionOpen = ref(false);
const emailSelected = ref("");
const userDescription = ref("");
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

const intervalId = setInterval(checkAuthorizationCode, 1000);

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
    // fetchEmailLinked();
    // fetchUserData();
});

function togglePasswordVisibility(event: Event) {
    event.preventDefault();
    showPassword.value = !showPassword.value;
}

function toggleConfirmPasswordVisibility() {
    showConfirmPassword.value = !showConfirmPassword.value;
}

async function openUnLinkModal(email: string) {
    emailSelected.value = email;
    isUnlinkModalOpen.value = true;

    if (emailsLinked.value.length === 1) {
        displayPopup(
            "error",
            t("settingsPage.accountPage.unableToDeletePrimaryEmail"),
            t("settingsPage.accountPage.deleteAccountInstruction")
        );
        closeUnlinkModal();
        return;
    }
}

async function unLinkAccount() {
    const requestOptions = {
        headers: { "Content-Type": "application/json" },
        method: "POST",
        body: JSON.stringify({ email: emailSelected.value }),
    };

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/social_api/unlink/`, requestOptions);

        if (!response) {
            displayPopup("error", "No response from server", "Verify your internet connection");
            return;
        }

        if (!response.ok) {
            displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`);
            return;
        }

        const data = await response.json();

        if ("error" in data) {
            displayPopup("error", t("settingsPage.accountPage.errorUnlinkingEmailAddress"), data.error);
        } else if (data.message === "Email unlinked successfully!") {
            fetchEmailLinked();
            displayPopup(
                "success",
                t("constants.popUpConstants.successMessages.success"),
                t("settingsPage.accountPage.emailUnlinkedSuccess")
            );
        }
    } catch (error) {
        displayPopup("error", t("settingsPage.accountPage.errorUnlinkingEmailAddress"), (error as Error).message);
    }
    closeUnlinkModal();
}

function linkNewEmail() {
    const typeApi = sessionStorage.getItem("typeApi");

    if (typeApi === "google") {
        caches.keys().then((keyList) => Promise.all(keyList.map((key) => caches.delete(key))));
        window.location.replace(`${API_BASE_URL}google/auth_url_link_email/`);
    } else if (typeApi === "microsoft") {
        window.location.replace(`${API_BASE_URL}microsoft/auth_url_link_email/`);
    }
}

function authorize(type: "google" | "microsoft") {
    saveVariables(type);
    isModalAddUserDescriptionOpen.value = true;
}

function saveVariables(typeApi: string) {
    sessionStorage.setItem("typeApi", typeApi);
    sessionStorage.setItem("userDescription", userEmailDescription.value);
}

function checkAuthorizationCode() {
    const urlParams = new URLSearchParams(window.location.search);
    const authorizationCode = urlParams.get("code");

    if (authorizationCode) {
        clearInterval(intervalId);
        linkEmail(authorizationCode);
    }
}

async function linkEmail(authorizationCode: string) {
    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            code: authorizationCode,
            typeApi: sessionStorage.getItem("typeApi"),
            user_description: sessionStorage.getItem("userDescription"),
        }),
    };
    const response = await fetchWithToken(`${API_BASE_URL}user/social_api/link/`, requestOptions);

    if (!response) {
        displayPopup("error", "No response from server", "Verify your internet connection");
        return;
    }

    if (!response.ok) {
        displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`);
        return;
    }

    const data = await response.json();

    if (data.message === "Email linked to account successfully!") {
        fetchEmailLinked();
        displayPopup(
            "success",
            t("constants.popUpConstants.successMessages.success"),
            t("settingsPage.accountPage.emailLinkedSuccess")
        );
    } else {
        displayPopup("error", t("settingsPage.accountPage.emailLinkingFailure"), data.error);
    }
    sessionStorage.clear();
    const currentUrl = window.location.href;
    const modifiedUrl = currentUrl.replace(/(\?)code=.*(&|$)/, "?").replace(/(\?)state=.*(&|$)/, "?");
    window.history.replaceState({}, document.title, modifiedUrl);
}

async function fetchEmailLinked() {
    const requestOptions = {
        headers: { "Content-Type": "application/json" },
    };

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/emails_linked/`, requestOptions);

        if (!response) {
            displayPopup("error", "No response from server", "Verify your internet connection");
            return;
        }

        if (!response.ok) {
            displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`);
            return;
        }

        const data = await response.json();

        if ("error" in data) {
            displayPopup("error", t("constants.popUpConstants.primaryEmailFetchError"), data.error);
        } else {
            emailsLinked.value = data;
        }
    } catch (error) {
        displayPopup("error", t("constants.popUpConstants.primaryEmailFetchError"), (error as Error).message);
    }
}

function openModal() {
    const isChecked = document.querySelector('input[name="choice"]:checked');

    if (isChecked) {
        isModalOpen.value = true;
    } else {
        displayPopup(
            "error",
            t("settingsPage.accountPage.confirmationRequired"),
            t("settingsPage.accountPage.checkBoxApprovalDeletion")
        );
    }
}

function closeAddUserDescriptionModal() {
    isModalAddUserDescriptionOpen.value = false;
}

function closeUnlinkModal() {
    isUnlinkModalOpen.value = false;
}

function closeUserDescriptionModal() {
    isModalUserDescriptionOpen.value = false;
}

async function openUserDescriptionModal(email: string) {
    emailSelected.value = email;

    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email }),
    };

    const response = await fetchWithToken(`${API_BASE_URL}user/social_api/get_user_description/`, requestOptions);

    if (!response) {
        displayPopup("error", "No response from server", "Verify your internet connection");
        return;
    }

    if (!response.ok) {
        displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`);
        return;
    }

    const data = await response.json();

    if (data.data || !data.data.trim()) {
        isModalUserDescriptionOpen.value = true;
        userDescription.value = data.data;
    } else {
        displayPopup("error", t("settingsPage.accountPage.errorUnlinkingEmailAddress"), data.error);
    }
}

async function updateUserDescription() {
    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            email: emailSelected.value,
            user_description: userDescription.value.trim() ? userDescription.value.trim() : "",
        }),
    };

    const response = await fetchWithToken(`${API_BASE_URL}user/social_api/update_user_description/`, requestOptions);

    if (!response) {
        displayPopup("error", "No response from server", "Verify your internet connection");
        return;
    }

    if (!response.ok) {
        displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`);
        return;
    }

    const data = await response.json();

    if (data.message === "User description updated") {
        displayPopup(
            "success",
            t("constants.popUpConstants.successMessages.success"),
            t("settingsPage.accountPage.emailDescriptionUpdated")
        );
    } else {
        displayPopup("error", t("settingsPage.accountPage.errorUpdatingDescription"), data.error);
    }
    closeUserDescriptionModal();
}

function handleKeyDown(event: KeyboardEvent) {
    if (event.key === "Tab" && !isModalOpen.value) {
        event.preventDefault();
        switchActiveSection();
    } else if (event.key === "Escape") {
        if (isModalOpen.value) {
            closeModal();
        } else if (isModalUserDescriptionOpen.value) {
            closeUserDescriptionModal();
        } else if (isUnlinkModalOpen.value) {
            closeUnlinkModal();
        } else if (isModalAddUserDescriptionOpen.value) {
            closeAddUserDescriptionModal();
        }
    } else if (event.key === "Enter") {
        if (isModalUserDescriptionOpen.value) {
            updateUserDescription();
        } else if (isModalAddUserDescriptionOpen.value) {
            linkNewEmail();
        }
    }
}

function switchActiveSection() {
    const nextSection: { [key: string]: string } = {
        account: "preferences",
        preferences: "subscription",
        subscription: "data",
        data: "account",
    };

    setActiveSection(nextSection[activeSection.value]);
}

function setActiveSection(section: string) {
    if (section === "account") {
        // fetchUserData();
    }
    activeSection.value = section;
}

async function fetchUserData() {
    const requestOptions = {
        headers: { "Content-Type": "application/json" },
    };

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/preferences/username/`, requestOptions);

        if (!response) {
            displayPopup("error", "No response from server", "Verify your internet connection");
            return;
        }

        if (!response.ok) {
            displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`);
            return;
        }

        const data = await response.json();

        userData.value = data.username;
    } catch (error) {
        displayPopup("error", t("settingsPage.accountPage.errorRetrievingUsername"), (error as Error).message);
    }
}

async function getUsername(): Promise<string | undefined> {
    const requestOptions = {
        headers: { "Content-Type": "application/json" },
    };

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/preferences/username/`, requestOptions);

        if (!response) {
            displayPopup("error", "No response from server", "Verify your internet connection");
            return;
        }

        if (!response.ok) {
            displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`);
            return;
        }

        const data = await response.json();

        return data.username;
    } catch (error) {
        displayPopup("error", t("settingsPage.accountPage.errorRetrievingUsername"), (error as Error).message);
    }
}

async function handleSubmit() {
    const requestOptions = {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    };

    try {
        const response = await fetchWithToken(`${API_BASE_URL}check_username/`, requestOptions);

        if (!response) {
            displayPopup("error", "No response from server", "Verify your internet connection");
            return;
        }

        if (!response.ok) {
            displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`);
            return;
        }

        const data = await response.json();

        if (data.available === false) {
            displayPopup(
                "error",
                t("settingsPage.accountPage.usernameAlreadyExists"),
                t("settingsPage.accountPage.pleaseChooseDifferentUsername")
            );
            return;
        }

        const currentUsername = await getUsername();

        if (userData.value !== currentUsername) {
            if (userData.value.length <= 150 && !/\s/.test(userData.value)) {
                await updateUsername();
            } else {
                if (userData.value.length > 150) {
                    displayPopup(
                        "error",
                        t(
                            "settingsPage.preferencesPage.popUpConstants.errorMessages.usernameMustNotExceed150Characters"
                        ),
                        t("settingsPage.preferencesPage.popUpConstants.errorMessages.chooseAShorterUsername")
                    );
                } else if (/\s/.test(userData.value)) {
                    displayPopup(
                        "error",
                        t("settingsPage.preferencesPage.popUpConstants.errorMessages.usernameMustNotContainSpaces"),
                        t("settingsPage.preferencesPage.popUpConstants.errorMessages.chooseAUsernameWithoutSpaces")
                    );
                }
            }
        }

        if (
            newPassword.value &&
            newPassword.value === confirmPassword.value &&
            newPassword.value.length >= 8 &&
            newPassword.value.length <= 32
        ) {
            await updatePassword();
        } else {
            if (!newPassword.value || newPassword.value !== confirmPassword.value) {
                displayPopup(
                    "error",
                    t("settingsPage.preferencesPage.popUpConstants.errorMessages.errorPasswordDontCorrespond"),
                    t("settingsPage.preferencesPage.popUpConstants.errorMessages.checkPassword")
                );
            } else if (newPassword.value.length < 8 || newPassword.value.length > 32) {
                displayPopup(
                    "error",
                    t(
                        "settingsPage.preferencesPage.popUpConstants.errorMessages.passwordMustBeBetween8And32Characters"
                    ),
                    t(
                        "settingsPage.preferencesPage.popUpConstants.errorMessages.chooseAPasswordWithTheAppropriateLength"
                    )
                );
            }
        }
    } catch (error) {
        displayPopup("error", t("settingsPage.accountPage.usernameCheckError"), (error as Error).message);
    }
}

async function updatePassword() {
    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password: newPassword.value }),
    };

    try {
        await fetchWithToken(`${API_BASE_URL}user/preferences/update_password/`, requestOptions);
        displayPopup(
            "success",
            t("constants.popUpConstants.successMessages.success"),
            t("settingsPage.accountPage.passwordUpdatedSuccess")
        );
    } catch (error) {
        displayPopup("error", t("settingsPage.accountPage.errorUpdatingPassword"), (error as Error).message);
    }
}

async function updateUsername() {
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: userData.value }),
    };

    try {
        await fetchWithToken(`${API_BASE_URL}user/preferences/update_username/`, requestOptions);
        displayPopup(
            "success",
            t("constants.popUpConstants.successMessages.success"),
            t("settingsPage.accountPage.usernameUpdatedSuccess")
        );
    } catch (error) {
        displayPopup("error", t("settingsPage.accountPage.errorUpdatingUsername"), (error as Error).message);
    }
}

async function deleteAccount() {
    try {
        const url = `${API_BASE_URL}api/delete_account/`;
        const requestOptions = {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
        };

        const response = await fetchWithToken(url, requestOptions);

        if (!response) {
            displayPopup("error", "No response from server", "Verify your internet connection");
            return;
        }

        if (!response.ok) {
            displayPopup("error", "Error in response", `HTTP error! status: ${response.status}`);
            return;
        }

        const data = await response.json();

        if (data && data.message === "User successfully deleted") {
            localStorage.clear();
            closeModal();
            displayPopup(
                "success",
                t("settingsPage.accountPage.redirectionInProgress"),
                t("settingsPage.accountPage.accountDeletedSuccess")
            );

            setTimeout(() => {
                router.push({ name: "login" });
            }, 4000);
        } else {
            displayPopup("error", t("settingsPage.accountPage.errorDeletingAccount"), data.error);
        }
    } catch (error) {
        displayPopup("error", t("settingsPage.accountPage.errorDeletingAccount"), (error as Error).message);
    }
}

function closeModal() {
    isModalOpen.value = false;
    const checkbox = document.querySelector('input[name="choice"]') as HTMLInputElement;
    if (checkbox) {
        checkbox.checked = false;
    }
}

function displayPopup(type: "success" | "error", title: string, message: string) {
    if (type === "error") {
        displayErrorPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    } else {
        displaySuccessPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    }
    timerId.value = setTimeout(dismissPopup, 4000);
}

function dismissPopup() {
    showNotification.value = false;
    if (timerId.value !== null) {
        clearTimeout(timerId.value);
    }
}
</script>
