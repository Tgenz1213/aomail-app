<template>
    <div class="flex flex-col h-full">
        <div class="p-6 bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col h-full overflow-hidden">
            <!-- View Mode Toggle -->
            <div class="flex items-center justify-between mb-6 flex-shrink-0">
                <span class="text-sm font-medium text-gray-700">{{ $t('emailProvidersAdvancedTab.viewMode') }}</span>
                <label class="flex items-center cursor-pointer">
                    <input type="checkbox" v-model="isChartView" class="hidden" />
                    <div
                        class="relative w-11 h-6 rounded-full transition-all duration-300"
                        :class="{ 'bg-gray-900': isChartView, 'bg-gray-200': !isChartView }"
                    >
                        <div
                            class="absolute left-1 top-1 w-4 h-4 bg-white rounded-full shadow-sm transition-all duration-300"
                            :class="{ 'translate-x-5': isChartView }"
                        ></div>
                    </div>
                    <span class="ml-3 text-sm text-gray-600">{{ isChartView ? $t('emailProvidersAdvancedTab.chart') : $t('emailProvidersAdvancedTab.raw') }}</span>
                </label>
            </div>

            <!-- Email Selection and Fetch Data Container -->
            <div class="mb-6 flex-shrink-0">
                <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('emailProvidersAdvancedTab.selectEmails') }}</label>
                <div class="flex gap-x-4">
                    <multiselect
                        v-model="selectedEmails"
                        :tag-placeholder="$t('emailProvidersAdvancedTab.addNewEmail')"
                        :placeholder="$t('emailProvidersAdvancedTab.searchOrAddEmail')"
                        label="email"
                        track-by="email"
                        :options="emailsLinked"
                        :multiple="true"
                        :taggable="true"
                        class="multiselect-gray flex-1"
                        style="height: 38px"
                        @tag="addEmailTag"
                    ></multiselect>
                    <button
                        @click="fetchCombinedStatistics"
                        class="bg-gray-700 rounded-lg px-6 text-md font-semibold text-white hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600 2xl:px-7 2xl:text-lg"
                        style="height: 38px"
                    >
                        {{ $t('emailProvidersAdvancedTab.fetchData') }}
                    </button>
                </div>
            </div>

            <!-- Statistics Display -->
            <div class="mt-6 flex-1 overflow-auto">
                <div v-if="!isChartView" class="space-y-4">
                    <!-- Aomail Stats Card -->
                    <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
                        <h2 class="text-base font-semibold text-gray-900 mb-4">{{ $t('emailProvidersAdvancedTab.statistics.aomailTitle') }}</h2>
                        <div class="space-y-3">
                            <div class="flex items-center text-sm text-gray-600">
                                <span class="mr-2">📩</span>
                                <span>{{ $t('emailProvidersAdvancedTab.statistics.emailsReceived') }}: {{ combinedStatistics?.aomailData.nbEmailsReceived }}</span>
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <span class="mr-2">📖</span>
                                <span>{{ $t('emailProvidersAdvancedTab.statistics.emailsRead') }}: {{ combinedStatistics?.aomailData.nbEmailsRead }}</span>
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <span class="mr-2">📂</span>
                                <span>{{ $t('emailProvidersAdvancedTab.statistics.emailsArchived') }}: {{ combinedStatistics?.aomailData.nbEmailsArchived }}</span>
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <span class="mr-2">⏳</span>
                                <span>{{ $t('emailProvidersAdvancedTab.statistics.emailsReplyLater') }}: {{ combinedStatistics?.aomailData.nbEmailsReplyLater }}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Email Providers Stats Card -->
                    <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
                        <h2 class="text-base font-semibold text-gray-900 mb-4">{{ $t('emailProvidersAdvancedTab.statistics.emailProvidersTitle') }}</h2>
                        <div class="space-y-3">
                            <div class="flex items-center text-sm text-gray-600">
                                <span class="mr-2">📩</span>
                                <span>{{ $t('emailProvidersAdvancedTab.statistics.emailsReceived') }}: {{ combinedStatistics?.emailProvidersData.nbEmailsReceived }}</span>
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <span class="mr-2">📖</span>
                                <span>{{ $t('emailProvidersAdvancedTab.statistics.emailsRead') }}: {{ combinedStatistics?.emailProvidersData.nbEmailsRead }}</span>
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <span class="mr-2">📂</span>
                                <span>{{ $t('emailProvidersAdvancedTab.statistics.emailsArchived') }}: {{ combinedStatistics?.emailProvidersData.nbEmailsArchived }}</span>
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <span class="mr-2">⭐</span>
                                <span>{{ $t('emailProvidersAdvancedTab.statistics.emailsStarred') }}: {{ combinedStatistics?.emailProvidersData.nbEmailsStarred }}</span>
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <span class="mr-2">📤</span>
                                <span>{{ $t('emailProvidersAdvancedTab.statistics.emailsSent') }}: {{ combinedStatistics?.emailProvidersData.nbEmailsSent }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Chart View -->
                <div v-else class="h-full">
                    <div ref="barChart" class="h-full w-full"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick, inject } from "vue";
import { init } from "echarts/core";
import { BarChart } from "echarts/charts";
import {
    TitleComponent,
    TooltipComponent,
    GridComponent,
    LegendComponent,
} from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import { use } from "echarts/core";
import Multiselect from "vue-multiselect";
import { getData, postData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import { EmailLinked } from "@/global/types";

use([
    TitleComponent,
    TooltipComponent,
    GridComponent,
    LegendComponent,
    BarChart,
    CanvasRenderer
]);

const emailsLinked = ref<EmailLinked[]>([]);
const combinedStatistics = ref<CombinedStatistics | undefined>();
const isChartView = ref(false);
const selectedEmails = ref<string[]>([]);
const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

// Chart container reference
const barChart = ref<HTMLElement | null>(null);

interface CombinedStatistics {
    aomailData: {
        nbEmailsReceived: number;
        nbEmailsRead: number;
        nbEmailsArchived: number;
        nbEmailsReplyLater: number;
    };
    emailProvidersData: {
        nbEmailsReceived: number;
        nbEmailsRead: number;
        nbEmailsArchived: number;
        nbEmailsStarred: number;
        nbEmailsSent: number;
    };
}

async function fetchEmailLinked() {
    const result = await getData(`user/emails_linked/`);

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.emailLinkedFetchError"),
            result.error as string
        );
        return;
    }

    emailsLinked.value = result.data;
    selectedEmails.value = result.data;
}

const addEmailTag = (newEmail: string) => {
    selectedEmails.value.push(newEmail);
};

const fetchCombinedStatistics = async () => {
    const result = await postData("user/combined_statistics/", {
        emailsSelected: selectedEmails.value.map((socialApi: any) => socialApi.email),
    });

    if (!result.success) {
        displayPopup?.("error", "Failed to fetch combined statistics", result.error as string);
        return;
    }

    combinedStatistics.value = result.data;
    nextTick(() => {
        renderBarChart(); // Call to render chart after DOM updates
    });
};

const renderBarChart = () => {
    if (!combinedStatistics.value || !barChart.value) return;

    const chartData = {
        categories: ["Read", "Archived", "Starred", "Sent"],
        values: [
            combinedStatistics.value.emailProvidersData.nbEmailsRead,
            combinedStatistics.value.emailProvidersData.nbEmailsArchived,
            combinedStatistics.value.emailProvidersData.nbEmailsStarred,
            combinedStatistics.value.emailProvidersData.nbEmailsSent,
        ],
    };

    const chart = init(barChart.value);

    const options = {
        title: {
            text: i18n.global.t('emailProvidersAdvancedTab.chart_title'),
            left: "center",
            textStyle: {
                fontSize: 18,
                fontWeight: "bold",
            },
        },
        tooltip: {
            trigger: "axis",
        },
        xAxis: {
            type: "category",
            data: chartData.categories,
            axisLabel: {
                fontSize: 12,
            },
        },
        yAxis: {
            type: "value",
            axisLabel: {
                fontSize: 12,
            },
        },
        series: [
            {
                data: chartData.values,
                type: "bar",
                barWidth: "50%",
                itemStyle: {
                    color: "#4CAF50",
                },
            },
        ],
    };

    chart.setOption(options);
};

onMounted(async () => {
    await fetchEmailLinked();
});

watch(isChartView, (newValue) => {
    if (newValue) {
        nextTick(() => {
            renderBarChart(); // Re-render chart when switching to chart view
        });
    }
});
</script>

<style scoped>
@import "vue-multiselect/dist/vue-multiselect.css";

.multiselect-gray {
    --ms-tag-bg: #f3f4f6;
    --ms-tag-color: #111827;
    --ms-tag-radius: 0.375rem;
    --ms-option-bg-selected: #111827;
}
</style>
