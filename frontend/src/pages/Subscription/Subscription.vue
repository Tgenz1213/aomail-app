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
            <div :class="['ring-1 shadow-sm ring-black ring-opacity-5', isNavMinimized ? 'w-20' : 'w-60']">
                <Navbar @update:isMinimized="(value) => (isNavMinimized = value)" />
            </div>
            <div class="flex-1 bg-white ring-1 shadow-sm ring-black ring-opacity-5">
                <div class="flex flex-col h-full relative divide-y divide-gray-200">
                    <div class="flex items-center justify-center h-[70px] 2xl:h-[80px] bg-gray-50">
                        <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500">
                            {{ $t("settingsPage.subscriptionPage.subscriptionTitle") }}
                        </h1>
                    </div>
                    <div class="flex-1 overflow-y-auto custom-scrollbar">
                        <div class="px-4 sm:px-6 lg:px-8 py-6">
                            <!-- Banner Section -->
                            <div
                                v-if="userPlan?.isTrial"
                                class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4"
                                role="alert"
                            >
                                <p class="font-bold">{{ $t("settingsPage.subscriptionPage.freeTrialTitle") }}</p>
                                <p v-if="daysLeft(new Date(userPlan.expiresThe)) > 0">
                                    {{
                                        $t("settingsPage.subscriptionPage.freeTrialMessage", {
                                            expiryDate: formatDate(new Date(userPlan.expiresThe)),
                                            daysLeft: daysLeft(new Date(userPlan.expiresThe)),
                                        })
                                    }}
                                </p>
                                <p v-else>
                                    {{ $t("constants.freeTrialExpired") }}
                                    {{ $t("constants.freeTrialExpiredDesc") }}
                                </p>
                            </div>
                            <div
                                v-else-if="!userPlan?.isActive"
                                class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4"
                                role="alert"
                            >
                                <p class="font-bold">{{ $t("settingsPage.subscriptionPage.accountInactive") }}</p>
                                <p>
                                    {{ $t("settingsPage.subscriptionPage.accountInactiveMessage") }}
                                    <span class="font-semibold">{{ userPlan?.plan }}</span>
                                </p>
                            </div>

                            <div class="flex justify-center w-full">
                                <RadioGroup
                                    v-model="selectedFrequency"
                                    class="grid grid-cols-2 gap-x-1 rounded-full p-1 text-center text-xs font-semibold leading-5 ring-1 ring-inset ring-gray-200"
                                >
                                    <RadioGroupLabel class="sr-only"></RadioGroupLabel>
                                    <RadioGroupOption
                                        as="template"
                                        v-for="option in frequencies"
                                        :key="option.key"
                                        :value="option"
                                        v-slot="{ checked }"
                                    >
                                        <div
                                            :class="[
                                                checked ? 'bg-gray-800 text-white' : 'text-gray-500',
                                                'cursor-pointer rounded-full px-2.5 py-1',
                                            ]"
                                        >
                                            <span>{{ $t(option.label) }}</span>
                                        </div>
                                    </RadioGroupOption>
                                </RadioGroup>
                            </div>
                            <div
                                class="flex-1 isolate mx-auto mt-6 h-full grid max-w-md grid-cols-1 gap-8 lg:mx-0 lg:max-w-none lg:grid-cols-3"
                            >
                                <div
                                    v-for="tier in tiers"
                                    :key="tier.name"
                                    :class="[
                                        tier.selected ? 'ring-2 ring-gray-800' : 'ring-1 ring-gray-200',
                                        'rounded-3xl p-8 xl:p-10',
                                    ]"
                                >
                                    <div class="flex items-center justify-between gap-x-4">
                                        <h3
                                            :class="[
                                                tier.selected ? 'text-gray-800' : 'text-gray-900',
                                                'text-lg font-semibold leading-8',
                                            ]"
                                        >
                                            {{ tier.name }}
                                        </h3>
                                    </div>
                                    <p class="mt-4 text-sm leading-6 text-gray-600">{{ tier.description }}</p>
                                    <p class="mt-6 flex items-baseline gap-x-1">
                                        <span class="text-md font-semibold tracking-tight text-gray-900">
                                            {{ tier.price[selectedFrequency.key] }}
                                        </span>
                                        <span class="text-sm font-semibold leading-6 text-gray-600">
                                            {{ $t(selectedFrequency.priceSuffix) }}
                                        </span>
                                    </p>
                                    <div
                                        v-if="!userPlan?.isTrial && userPlan?.isActive"
                                        @click="redirectToPortal"
                                        :class="[
                                            tier.selected
                                                ? 'bg-gray-800 text-white shadow-sm hover:bg-gray-600 cursor-pointer'
                                                : 'text-gray-800 ring-1 ring-inset ring-gray-200 hover:ring-gray-300',
                                            'mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800 cursor-pointer',
                                        ]"
                                    >
                                        {{ getActionLabel(tier.plan as PlanType) }}
                                    </div>

                                    <!-- Select Plan Button -->
                                    <div
                                        v-else
                                        @click="redirectPaymentPage(tier.plan)"
                                        :class="[
                                            tier.selected
                                                ? 'bg-gray-800 text-white shadow-sm hover:bg-gray-600 cursor-pointer'
                                                : 'text-gray-800 ring-1 ring-inset ring-gray-200 hover:ring-gray-300',
                                            'mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800 cursor-pointer',
                                        ]"
                                    >
                                        {{ $t("settingsPage.subscriptionPage.selectPlan") }}
                                    </div>
                                    <ul role="list" class="mt-8 space-y-3 text-sm leading-6 text-gray-600 xl:mt-10">
                                        <li v-for="feature in tier.features" :key="feature" class="flex gap-x-3">
                                            <CheckIcon class="h-6 w-5 flex-none text-gray-800" aria-hidden="true" />
                                            {{ feature }}
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref, watch } from "vue";
import { RadioGroup, RadioGroupLabel, RadioGroupOption } from "@headlessui/vue";
import { CheckIcon } from "@heroicons/vue/20/solid";
import { i18n } from "@/global/preferences";
import { postData, getData } from "@/global/fetchData";
import { loadStripe } from "@stripe/stripe-js";
import { STRIPE_PUBLISHABLE_KEY, SUBSCRIPTION_MANAGEMENT_URL } from "@/global/const";
import { Plan } from "./utils/types";
import Navbar from "@/global/components/Navbar.vue";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";

const PLAN_LEVELS = {
    start: 0,
    premium: 1,
    entreprise: 2,
} as const;

type PlanType = keyof typeof PLAN_LEVELS;

interface Frequency {
    key: "monthly" | "yearly";
    label: string;
    priceSuffix: string;
}

interface Tier {
    name: string;
    plan: string;
    price: { monthly: string; yearly: string };
    description: string;
    features: string[];
    selected: boolean;
    mostPopular: boolean;
}

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

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

const userPlan = ref<Plan | null>(null);
const isNavMinimized = ref(false);

onMounted(() => {
    getUserPlan();
    checkStripePaymentStatus();
});

function checkStripePaymentStatus() {
    const regrantConsent = sessionStorage.getItem("regrantConsent");

    if (regrantConsent === "true") {
        return;
    }
    const urlParams = new URLSearchParams(window.location.search);
    const stripePaymentSuccess = urlParams.get("stripe-payment-success");

    const modifiedUrl = window.location.origin + window.location.pathname;
    window.history.replaceState({}, document.title, modifiedUrl);
    if (stripePaymentSuccess) {
        if (stripePaymentSuccess === "true") {
            displayPopup(
                "success",
                i18n.global.t("settingsPage.subscriptionPage.paymentSuccessful"),
                i18n.global.t("settingsPage.subscriptionPage.paymentSuccessfulMessage")
            );
        } else if (stripePaymentSuccess === "false") {
            displayPopup(
                "error",
                i18n.global.t("settingsPage.subscriptionPage.paymentFailed"),
                i18n.global.t("settingsPage.subscriptionPage.paymentFailedMessage")
            );
        }
    }
}

watch(userPlan, () => {
    if (userPlan.value && userPlan.value.isActive) {
        for (const tier of tiers) {
            if (tier.plan === userPlan.value.plan) {
                tier.selected = true;
            }
        }
    }
});

const frequencies: Frequency[] = [
    {
        key: "monthly",
        label: "settingsPage.subscriptionPage.monthly",
        priceSuffix: i18n.global.t("settingsPage.subscriptionPage.perMonth"),
    },
    {
        key: "yearly",
        label: "settingsPage.subscriptionPage.yearly",
        priceSuffix: i18n.global.t("settingsPage.subscriptionPage.perYear"),
    },
];

const tiers: Tier[] = reactive([
    {
        name: "Start",
        plan: "start",
        price: { monthly: "15$", yearly: "120$" },
        description: i18n.global.t("settingsPage.subscriptionPage.basic.description"),
        features: i18n.global.tm("settingsPage.subscriptionPage.basic.features"),
        selected: false,
        mostPopular: false,
    },
    {
        name: "Premium",
        plan: "premium",
        price: { monthly: "20$", yearly: "180$" },
        description: i18n.global.t("settingsPage.subscriptionPage.premium.description"),
        features: i18n.global.tm("settingsPage.subscriptionPage.premium.features"),
        selected: false,
        mostPopular: true,
    },
    {
        name: "Entreprise",
        plan: "entreprise",
        price: { monthly: "contact us", yearly: "contact us" },
        description: i18n.global.t("settingsPage.subscriptionPage.entreprise.description"),
        features: i18n.global.tm("settingsPage.subscriptionPage.entreprise.features"),
        selected: false,
        mostPopular: false,
    },
]);

const selectedFrequency = ref<Frequency>(frequencies[0]);

const getActionLabel = (plan: PlanType): string => {
    const currentPlanLevel = PLAN_LEVELS[userPlan.value?.plan as PlanType];
    const targetPlanLevel = PLAN_LEVELS[plan];

    if (currentPlanLevel === targetPlanLevel) {
        return i18n.global.t("settingsPage.subscriptionPage.manage");
    }

    return currentPlanLevel < targetPlanLevel
        ? i18n.global.t("settingsPage.subscriptionPage.upgrade")
        : i18n.global.t("settingsPage.subscriptionPage.downgrade");
};

function formatDate(date: Date): string {
    return date.toLocaleDateString();
}

function daysLeft(expirationDate: Date): number {
    const today = new Date();
    const timeDiff = expirationDate.getTime() - today.getTime();
    return Math.ceil(timeDiff / (1000 * 3600 * 24));
}

async function getUserPlan() {
    const result = await getData("user/preferences/plan/");
    if (!result.success) {
        displayPopup("error", i18n.global.t("settingsPage.subscriptionPage.failedToFetchPlan"), result.error as string);
    } else {
        userPlan.value = result.data;
    }
}

const redirectPaymentPage = async (product: string) => {
    const result = await postData("stripe/create_checkout_session/", {
        product,
        frequency: selectedFrequency.value.key,
    });

    if (!result.success) {
        displayPopup(
            "error", 
            i18n.global.t("settingsPage.subscriptionPage.failedToCreateSession"), 
            result.error as string
        );
        return;
    }

    const sessionId = result.data.id;

    const stripe = await loadStripe(STRIPE_PUBLISHABLE_KEY);
    if (!stripe) {
        displayPopup(
            "error",
            i18n.global.t("settingsPage.subscriptionPage.stripeInitError"),
            i18n.global.t("settingsPage.subscriptionPage.stripeInitErrorMessage")
        );
        return;
    }
    await stripe.redirectToCheckout({ sessionId });
};

const redirectToPortal = () => {
    window.location.href = SUBSCRIPTION_MANAGEMENT_URL;
};
</script>
