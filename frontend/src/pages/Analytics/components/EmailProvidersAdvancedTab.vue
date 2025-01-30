<template>
    <div class="p-6 bg-gray-100 rounded-lg shadow-lg">
        <!-- Toggle Switch for Chart View -->
        <div class="flex items-center justify-between mb-4">
            <span class="text-lg font-medium text-gray-700">View Mode:</span>
            <label class="flex items-center cursor-pointer">
                <input type="checkbox" v-model="isChartView" class="hidden" />
                <div
                    class="relative w-14 h-7 bg-gray-300 rounded-full transition-all duration-300"
                    :class="{ 'bg-blue-500': isChartView }"
                >
                    <div
                        class="absolute left-1 top-1 w-5 h-5 bg-white rounded-full shadow-md transition-all duration-300"
                        :class="{ 'translate-x-7': isChartView }"
                    ></div>
                </div>
                <span class="ml-3 text-gray-700">{{ isChartView ? "Chart" : "Raw" }}</span>
            </label>
        </div>

        <!-- Multiselect Dropdown -->
        <div class="mb-4">
            <label class="block text-lg font-medium text-gray-700">Select Emails</label>
            <multiselect
                id="tagging"
                v-model="selectedEmails"
                tag-placeholder="Add new email"
                placeholder="Search or add an email"
                label="email"
                track-by="email"
                :options="emailsLinked"
                :multiple="true"
                :taggable="true"
                class="mt-2"
                @tag="addEmailTag"
            ></multiselect>
        </div>

        <!-- Fetch Data Button -->
        <button
            @click="fetchCombinedStatistics"
            class="w-full px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600 transition-all"
        >
            Fetch Data
        </button>

        <!-- Display JSON Data -->
        <pre class="p-4 mt-4 text-sm bg-white rounded-lg shadow">{{ selectedEmails }}</pre>

        <!-- Raw Statistics View -->
        <div v-if="!isChartView" class="mt-6">
            <div class="p-4 bg-white shadow rounded-lg mb-4">
                <h2 class="text-xl font-semibold text-gray-800">Aomail Statistics</h2>
                <p>📩 Emails Received: {{ combinedStatistics?.aomailData.nbEmailsReceived }}</p>
                <p>📖 Emails Read: {{ combinedStatistics?.aomailData.nbEmailsRead }}</p>
                <p>📂 Emails Archived: {{ combinedStatistics?.aomailData.nbEmailsArchived }}</p>
                <p>⏳ Emails Reply Later: {{ combinedStatistics?.aomailData.nbEmailsReplyLater }}</p>
            </div>
            <div class="p-4 bg-white shadow rounded-lg">
                <h2 class="text-xl font-semibold text-gray-800">Email Providers Statistics</h2>
                <p>📩 Emails Received: {{ combinedStatistics?.emailProvidersData.nbEmailsReceived }}</p>
                <p>📖 Emails Read: {{ combinedStatistics?.emailProvidersData.nbEmailsRead }}</p>
                <p>📂 Emails Archived: {{ combinedStatistics?.emailProvidersData.nbEmailsArchived }}</p>
                <p>⭐ Emails Starred: {{ combinedStatistics?.emailProvidersData.nbEmailsStarred }}</p>
                <p>📤 Emails Sent: {{ combinedStatistics?.emailProvidersData.nbEmailsSent }}</p>
            </div>
        </div>

        <!-- Bar Chart View -->
        <div v-else class="mt-6">
            <div ref="barChart" class="h-80"></div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick, inject } from "vue";
import * as echarts from "echarts";
import Multiselect from "vue-multiselect";
import { getData, postData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import { EmailLinked } from "@/global/types";

// Refs
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

    const chart = echarts.init(barChart.value);

    const options = {
        title: {
            text: "Email Statistics",
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
</style>
