<template>
    <div class="flex flex-col h-full section bg-white rounded-lg shadow-lg p-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Dropdown Menu for Metrics -->
            <div>
                <label for="metric-select" class="block text-sm font-medium text-gray-700 mb-2 flex items-center">
                    <i class="fas fa-chart-bar text-blue-500 mr-2"></i>
                    Metrics
                </label>
                <select
                    id="metric-select"
                    v-model="selectedMetric"
                    class="p-3 border border-gray-300 rounded-lg w-full focus:ring-blue-500 focus:border-blue-500"
                >
                    <option v-for="metric in statisticsMetrics" :key="metric" :value="metric">
                        {{ metricLabelTranslations[metric] || metric }}
                    </option>
                </select>
            </div>
            <!-- Since Selection (Checkbox List) -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2 flex items-center">
                    <i class="fas fa-clock text-blue-500 mr-2"></i>
                    Select Since
                </label>
                <div class="grid grid-cols-2 gap-2">
                    <div v-for="sinceOption in sinceOptions" :key="sinceOption" class="flex items-center mb-2">
                        <input
                            type="checkbox"
                            v-model="selectedSinceOptions"
                            :value="sinceOption"
                            class="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span class="text-sm">{{ metricLabelTranslations[sinceOption] || sinceOption }}</span>
                    </div>
                </div>
            </div>
            <!-- Period Selection (Checkbox List) -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2 flex items-center">
                    <i class="fas fa-calendar-alt text-blue-500 mr-2"></i>
                    Select Period
                </label>
                <div class="grid grid-cols-2 gap-2">
                    <div v-for="periodOption in periodOptions" :key="periodOption" class="flex items-center mb-2">
                        <input
                            type="checkbox"
                            v-model="selectedPeriodOptions"
                            :value="periodOption"
                            class="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span class="text-sm">{{ metricLabelTranslations[periodOption] || periodOption }}</span>
                    </div>
                </div>
            </div>
            <!-- Data Options (avg, min, max) -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2 flex items-center">
                    <i class="fas fa-database text-blue-500 mr-2"></i>
                    Select Data Options
                </label>
                <div class="flex space-x-4">
                    <label class="flex items-center">
                        <input
                            type="checkbox"
                            v-model="selectedDataOptions.avg"
                            class="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span class="text-sm">Avg</span>
                    </label>
                    <label class="flex items-center">
                        <input
                            type="checkbox"
                            v-model="selectedDataOptions.min"
                            class="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span class="text-sm">Min</span>
                    </label>
                    <label class="flex items-center">
                        <input
                            type="checkbox"
                            v-model="selectedDataOptions.max"
                            class="mr-2 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span class="text-sm">Max</span>
                    </label>
                </div>
            </div>
        </div>
        <div v-if="data[selectedMetric]" class="mt-8 bg-gray-50 p-6 rounded-lg shadow-md">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                <i class="fas fa-chart-line text-green-500 mr-2"></i>
                Statistics for {{ metricLabelTranslations[selectedMetric] || selectedMetric }}
            </h3>
            <!-- Scrollable content container for statistics -->
            <div class="overflow-y-auto max-h-80">
                <!-- Display since values -->
                <div class="mb-4">
                    <h4 class="text-sm font-medium text-gray-600 mb-2">Since:</h4>
                    <ul class="space-y-2">
                        <li v-for="(value, key) in data[selectedMetric]?.since" :key="key" class="flex justify-between">
                            <span>{{ metricLabelTranslations[key as MetricKeys] || key }}</span>
                            <span class="font-semibold">{{ value }}</span>
                        </li>
                    </ul>
                </div>
                <!-- Display periods values -->
                <div>
                    <h4 class="text-sm font-medium text-gray-600 mb-2">Periods:</h4>
                    <ul class="space-y-2">
                        <li
                            v-for="(period, key) in data[selectedMetric]?.periods"
                            :key="key"
                            class="flex justify-between"
                        >
                            <span>{{ metricLabelTranslations[key as MetricKeys] || key }}</span>
                            <span>
                                Avg:
                                <strong>{{ period.avg }}</strong>
                                , Min:
                                <strong>{{ period.min }}</strong>
                                , Max:
                                <strong>{{ period.max }}</strong>
                            </span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from "vue";
import { postData } from "@/global/fetchData";
import { inject } from "vue";

type MetricKeys = keyof typeof metricLabelTranslations;

interface Metric {
    since?: Record<string, number>;
    periods?: Record<string, { avg?: number; min?: number; max?: number }>;
}

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const metricLabelTranslations = {
    nbMightRequireAnswer: "Number of emails that might require an answer",
    nbEmailsReceived: "Number of emails received",
    nbAnswerRequired: "Number of emails requiring an answer",
    nbNoAnswerRequired: "Number of emails not requiring an answer",
    nbHighlyRelevant: "Number of highly relevant emails",
    nbPossiblyRelevant: "Number of possibly relevant emails",
    nbNotRelevant: "Number of not relevant emails",
    nbEmailsImportant: "Number of important emails",
    nbEmailsInformative: "Number of informative emails",
    nbEmailsUseless: "Number of useless emails",
    nbScam: "Number of scam emails",
    nbSpam: "Number of spam emails",
    nbNewsletter: "Number of newsletters",
    nbNotification: "Number of notifications",
    nbMeeting: "Number of meeting-related emails",
    join: "Since joining",
    today: "Today",
    monday: "Monday",
    mtd: "Month to date",
    ytd: "Year to date",
    "24Hours": "24 hours",
    "7Days": "7 days",
    "30Days": "30 days",
    "3Months": "3 months",
    "6Months": "6 months",
    "1year": "1 year",
    "5years": "5 years",
} as const;

const statisticsMetrics: MetricKeys[] = [
    "nbEmailsReceived",
    "nbMightRequireAnswer",
    "nbAnswerRequired",
    "nbNoAnswerRequired",
    "nbHighlyRelevant",
    "nbPossiblyRelevant",
    "nbNotRelevant",
    "nbEmailsImportant",
    "nbEmailsInformative",
    "nbEmailsUseless",
    "nbScam",
    "nbSpam",
    "nbNewsletter",
    "nbNotification",
    "nbMeeting",
];
const sinceOptions: MetricKeys[] = ["join", "today", "monday", "mtd", "ytd"];
const periodOptions: MetricKeys[] = ["24Hours", "7Days", "30Days", "3Months", "6Months", "1year", "5years"];
const data = ref<Record<string, Metric>>({});
const selectedMetric = ref<MetricKeys>(statisticsMetrics[0]);
const selectedSinceOptions = ref<MetricKeys[]>(sinceOptions);
const selectedPeriodOptions = ref<MetricKeys[]>(periodOptions);
const selectedDataOptions = ref<{ avg: boolean; min: boolean; max: boolean }>({
    avg: true,
    min: true,
    max: true,
});

const fetchStatistics = async () => {
    const result = await postData("user/statistics/", {
        [selectedMetric.value]: {
            since: selectedSinceOptions.value,
            periods: Object.fromEntries(
                selectedPeriodOptions.value.map((period) => [
                    period,
                    (Object.keys(selectedDataOptions.value) as Array<keyof typeof selectedDataOptions.value>).filter(
                        (option) => selectedDataOptions.value[option]
                    ),
                ])
            ),
        },
    });

    if (!result.success) {
        displayPopup?.("error", "Failed to fetch statistics", result.error as string);
    } else {
        data.value = result.data.stats;
    }
};

onMounted(fetchStatistics);
watch([selectedMetric, selectedSinceOptions, selectedPeriodOptions, selectedDataOptions], fetchStatistics);
</script>
