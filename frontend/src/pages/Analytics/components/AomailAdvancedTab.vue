<template>
    <div class="flex flex-col h-full section">
        <!-- Form Section (Dropdowns, Checkboxes) -->
        <div class="grid grid-cols-1 gap-6">
            <!-- Dropdown Menu for Metrics -->
            <div class="w-full">
                <label for="metric-select" class="block text-sm font-medium text-gray-700 mb-2 flex items-center">
                    <i class="fas fa-chart-bar text-gray-900 mr-2"></i>
                    {{ $t("analyticsPage.metrics") }}
                </label>
                <select
                    id="metric-select"
                    v-model="selectedMetric"
                    class="p-3 border border-gray-300 rounded-lg w-full focus:ring-gray-900 focus:border-gray-900"
                >
                    <option v-for="metric in statisticsMetrics" :key="metric" :value="metric">
                        {{ getMetricLabel(metric) }}
                    </option>
                </select>
            </div>

            <!-- Options Container -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Since Selection (Checkbox List) -->
                <div class="bg-gray-50 p-4 rounded-lg">
                    <label class="block text-sm font-medium text-gray-700 mb-3 flex items-center">
                        <i class="fas fa-clock text-gray-900 mr-2"></i>
                        {{ $t("analyticsPage.selectSince") }}
                    </label>
                    <div class="space-y-2">
                        <div v-for="sinceOption in sinceOptions" :key="sinceOption" class="flex items-center">
                            <input
                                type="checkbox"
                                v-model="selectedSinceOptions"
                                :value="sinceOption"
                                class="mr-2 h-4 w-4 text-gray-900 border-gray-300 rounded focus:ring-gray-900"
                            />
                            <span class="text-sm">{{ getMetricLabel(sinceOption) }}</span>
                        </div>
                    </div>
                </div>

                <!-- Period Selection (Checkbox List) -->
                <div class="bg-gray-50 p-4 rounded-lg">
                    <label class="block text-sm font-medium text-gray-700 mb-3 flex items-center">
                        <i class="fas fa-calendar-alt text-gray-900 mr-2"></i>
                        {{ $t("analyticsPage.selectPeriod") }}
                    </label>
                    <div class="space-y-2">
                        <div v-for="periodOption in periodOptions" :key="periodOption" class="flex items-center">
                            <input
                                type="checkbox"
                                v-model="selectedPeriodOptions"
                                :value="periodOption"
                                class="mr-2 h-4 w-4 text-gray-900 border-gray-300 rounded focus:ring-gray-900"
                            />
                            <span class="text-sm">{{ getMetricLabel(periodOption) }}</span>
                        </div>
                    </div>
                </div>

                <!-- Data Options (avg, min, max) -->
                <div class="bg-gray-50 p-4 rounded-lg">
                    <label class="block text-sm font-medium text-gray-700 mb-3 flex items-center">
                        <i class="fas fa-database text-gray-900 mr-2"></i>
                        {{ $t("analyticsPage.selectDataOptions") }}
                    </label>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <input
                                type="checkbox"
                                v-model="selectedDataOptions.avg"
                                class="mr-2 h-4 w-4 text-gray-900 border-gray-300 rounded focus:ring-gray-900"
                            />
                            <span class="text-sm">{{ $t("analyticsPage.average") }}</span>
                        </label>
                        <label class="flex items-center">
                            <input
                                type="checkbox"
                                v-model="selectedDataOptions.min"
                                class="mr-2 h-4 w-4 text-gray-900 border-gray-300 rounded focus:ring-gray-900"
                            />
                            <span class="text-sm">{{ $t("analyticsPage.minimum") }}</span>
                        </label>
                        <label class="flex items-center">
                            <input
                                type="checkbox"
                                v-model="selectedDataOptions.max"
                                class="mr-2 h-4 w-4 text-gray-900 border-gray-300 rounded focus:ring-gray-900"
                            />
                            <span class="text-sm">{{ $t("analyticsPage.maximum") }}</span>
                        </label>
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts Section -->
        <div v-if="data[selectedMetric]" class="flex-1 mt-3">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-8 h-full">
                <!-- Since Bar Chart Container -->
                <div class="p-4 flex flex-col">
                    <h3 class="text-lg font-semibold text-gray-800 mb-2 flex items-center">
                        <i class="fas fa-chart-bar text-green-500 mr-2"></i>
                        {{ $t("analyticsPage.sinceStatistics") }}
                    </h3>
                    <div class="flex-1 min-h-0">
                        <canvas id="sinceBarChart"></canvas>
                    </div>
                </div>

                <!-- Periods Error Bar Chart Container -->
                <div class="p-4 flex flex-col">
                    <h3 class="text-lg font-semibold text-gray-800 mb-2 flex items-center">
                        <i class="fas fa-chart-line text-green-500 mr-2"></i>
                        {{ $t("analyticsPage.periodStatistics") }}
                    </h3>
                    <div class="flex-1 min-h-0">
                        <canvas id="periodsErrorBarChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import { postData } from "@/global/fetchData";
import { inject } from "vue";
import { Chart, registerables } from "chart.js";
import { i18n } from "@/global/preferences";

Chart.register(...registerables);

type MetricKey =
    | "nbMightRequireAnswer"
    | "nbEmailsReceived"
    | "nbAnswerRequired"
    | "nbNoAnswerRequired"
    | "nbHighlyRelevant"
    | "nbPossiblyRelevant"
    | "nbNotRelevant"
    | "nbEmailsImportant"
    | "nbEmailsInformative"
    | "nbEmailsUseless"
    | "nbScam"
    | "nbSpam"
    | "nbNewsletter"
    | "nbNotification"
    | "nbMeeting"
    | "join"
    | "today"
    | "monday"
    | "mtd"
    | "ytd"
    | "24Hours"
    | "7Days"
    | "30Days"
    | "3Months"
    | "6Months"
    | "1year"
    | "5years";

interface Metric {
    since?: Record<string, number>;
    periods?: Record<string, { avg?: number; min?: number; max?: number }>;
}

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const getMetricLabel = (key: MetricKey) => {
    if (key.startsWith("nb")) {
        return i18n.global.t(`analyticsPage.metricLabels.${key}`);
    }
    return i18n.global.t(`analyticsPage.timeLabels.${key}`);
};

const statisticsMetrics: MetricKey[] = [
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
const sinceOptions: MetricKey[] = ["join", "today", "monday", "mtd", "ytd"];
const periodOptions: MetricKey[] = ["24Hours", "7Days", "30Days", "3Months", "6Months", "1year", "5years"];
const data = ref<Record<string, Metric>>({});
const selectedMetric = ref<MetricKey>(statisticsMetrics[0]);
const selectedSinceOptions = ref<MetricKey[]>(sinceOptions);
const selectedPeriodOptions = ref<MetricKey[]>(periodOptions);
const selectedDataOptions = ref<{ avg?: boolean; min?: boolean; max?: boolean }>({
    avg: true,
    min: true,
    max: true,
});

let sinceChart: Chart | null = null;
let periodsChart: Chart | null = null;

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
        displayPopup?.("error", i18n.global.t("analyticsPage.failedToFetchStatistics"), result.error as string);
    } else {
        data.value = result.data.stats;
    }
};

const renderSinceBarChart = () => {
    const ctx = document.getElementById("sinceBarChart") as HTMLCanvasElement;
    if (!ctx) return;

    if (sinceChart) {
        sinceChart.destroy();
    }
    sinceChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: selectedSinceOptions.value.map((option) => getMetricLabel(option)),
            datasets: [
                {
                    label: i18n.global.t("analyticsPage.sinceStatistics"),
                    data: selectedSinceOptions.value.map(
                        (option) => data.value[selectedMetric.value]?.since?.[option] || 0
                    ),
                    backgroundColor: "rgba(54, 162, 235, 0.2)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
};

const renderPeriodsErrorBarChart = () => {
    const ctx = document.getElementById("periodsErrorBarChart") as HTMLCanvasElement;
    if (!ctx) return;

    if (periodsChart) {
        periodsChart.destroy();
    }
    periodsChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: selectedPeriodOptions.value.map((option) => getMetricLabel(option)),
            datasets: [
                {
                    label: "Avg",
                    data: selectedPeriodOptions.value.map(
                        (option) => data.value[selectedMetric.value]?.periods?.[option]?.avg || 0
                    ),
                    backgroundColor: "rgba(54, 162, 235, 0.2)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1,
                },
                {
                    label: "Min",
                    data: selectedPeriodOptions.value.map(
                        (option) => data.value[selectedMetric.value]?.periods?.[option]?.min || 0
                    ),
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderColor: "rgba(75, 192, 192, 1)",
                    borderWidth: 1,
                },
                {
                    label: "Max",
                    data: selectedPeriodOptions.value.map(
                        (option) => data.value[selectedMetric.value]?.periods?.[option]?.max || 0
                    ),
                    backgroundColor: "rgba(255, 99, 132, 0.2)",
                    borderColor: "rgba(255, 99, 132, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
};

// Clean up chart instances when the component is unmounted
onBeforeUnmount(() => {
    if (sinceChart) {
        sinceChart.destroy();
    }
    if (periodsChart) {
        periodsChart.destroy();
    }
});

onMounted(() => {
    fetchStatistics().then(() => {
        renderSinceBarChart();
        renderPeriodsErrorBarChart();
    });
});

watch([selectedMetric, selectedSinceOptions, selectedPeriodOptions], () => {
    fetchStatistics().then(() => {
        renderSinceBarChart();
        renderPeriodsErrorBarChart();
    });
});

watch(
    () => selectedDataOptions.value,
    () => {
        fetchStatistics().then(() => {
            renderSinceBarChart();
            renderPeriodsErrorBarChart();
        });
    },
    { deep: true }
);
</script>
