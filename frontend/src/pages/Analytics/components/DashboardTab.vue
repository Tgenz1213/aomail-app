<template>
    <!-- Email Provider Dashboard Section -->
    <section class="">
        <div class="grid grid-cols-2 gap-10">
            <div class="h-[34vh]">
                <ChartTitle>
                    {{ $t("analyticsPage.analytics.emailsReceivedPerDomain") }}
                </ChartTitle>
                <div :id="chartIds.domainDistribution" class="w-full h-full pt-6"></div>
            </div>
            <div class="h-[34vh]">
                <ChartTitle>
                    {{ $t("analyticsPage.analytics.emailsReceivedPerSender") }}
                </ChartTitle>
                <div :id="chartIds.senderDistribution" class="w-full h-full pt-6"></div>
            </div>
        </div>
    </section>

    <!-- Aomail Dashboard Section -->
    <section class="pt-10">
        <div class="grid grid-cols-3 gap-10">
            <div class="h-[43vh]">
                <ChartTitle>
                    {{ $t("analyticsPage.analytics.importanceDistribution") }}
                </ChartTitle>
                <div :id="chartIds.importance" class="w-full h-full pt-4"></div>
            </div>
            <div class="h-[43vh]">
                <ChartTitle>
                    {{ $t("analyticsPage.analytics.answerRequirementDistribution") }}
                </ChartTitle>
                <div :id="chartIds.answerRequirement" class="w-full h-full pt-4"></div>
            </div>
            <div class="h-[43vh]">
                <ChartTitle>
                    {{ $t("analyticsPage.analytics.relevanceDistribution") }}
                </ChartTitle>
                <div :id="chartIds.relevance" class="w-full h-full pt-4"></div>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { getData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import * as echarts from "echarts";
import { inject, onMounted, onUnmounted } from "vue";
import ChartTitle from "./CharTitle.vue";

let importanceChart: echarts.ECharts;
let answerRequirementChart: echarts.ECharts;
let relevanceChart: echarts.ECharts;
let domainDistributionChart: echarts.ECharts;
let senderDistributionChart: echarts.ECharts;

const chartIds = {
    importance: "importanceChart",
    answerRequirement: "answerRequirementChart",
    relevance: "relevanceChart",
    domainDistribution: "domainDistributionChart",
    senderDistribution: "senderDistributionChart",
} as const;

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

interface DashboardData {
    distribution: {
        [key: string]: {
            nbEmailsImportant: number;
            nbEmailsInformative: number;
            nbEmailsUseless: number;
            nbEmailsAnswerRequired: number;
            nbEmailsMightRequireAnswer: number;
            nbEmailsNoAnswerRequired: number;
            nbEmailsHighlyRelevant: number;
            nbEmailsPossiblyRelevant: number;
            nbEmailsNotRelevant: number;
        };
    };
    emailsReceivedData: {
        orderedDomains: string[];
        orderedDomainsNbEmails: number[];
        orderedSenders: { email: string; name: string; value: number }[];
        orderedSendersNbEmails: number[];
    };
}

interface ImportanceData {
    name: string;
    children: { name: string; value: number }[];
}
let importanceData: ImportanceData[] | undefined;
let answerRequiredData: number[][] = [];
let categoryNames: string[];
let relevanceData: (string | number)[][] = [];
let orderedDomains: string[];
let orderedDomainsNbEmails: number[];
let orderedSenders: { email: string; name: string; value: number }[];
let orderedSendersNbEmails: number[];

const fetchDashboardData = async () => {
    const response = await getData("user/dashboard_data/");

    if (!response.success) {
        displayPopup?.("error", "Failed to fetch dashboard data", response.error as string);
        return;
    }

    const dashboardData = response.data as DashboardData;
    categoryNames = Object.keys(dashboardData.distribution);

    const answerRequiredRow = categoryNames.map(
        (category) => dashboardData.distribution[category].nbEmailsAnswerRequired
    );
    const mightRequireAnswerRow = categoryNames.map(
        (category) => dashboardData.distribution[category].nbEmailsMightRequireAnswer
    );
    const noAnswerRequiredRow = categoryNames.map(
        (category) => dashboardData.distribution[category].nbEmailsNoAnswerRequired
    );
    answerRequiredData = [answerRequiredRow, mightRequireAnswerRow, noAnswerRequiredRow];

    importanceData = Object.entries(dashboardData.distribution).map(([category, data]) => ({
        name: category,
        children: [
            { name: "Important", value: data.nbEmailsImportant },
            { name: "Informative", value: data.nbEmailsInformative },
            { name: "Useless", value: data.nbEmailsUseless },
        ],
    }));

    // Reset relevanceData before populating
    relevanceData = [];

    // Add header row first
    relevanceData.push(["Category", "Highly Relevant", "Possibly Relevant", "Not Relevant"]);

    // Add data rows
    categoryNames.forEach((category) =>
        relevanceData.push([
            category,
            dashboardData.distribution[category].nbEmailsHighlyRelevant,
            dashboardData.distribution[category].nbEmailsPossiblyRelevant,
            dashboardData.distribution[category].nbEmailsNotRelevant,
        ])
    );

    orderedDomains = dashboardData.emailsReceivedData.orderedDomains;
    orderedDomainsNbEmails = dashboardData.emailsReceivedData.orderedDomainsNbEmails;
    orderedSenders = dashboardData.emailsReceivedData.orderedSenders;
    orderedSendersNbEmails = dashboardData.emailsReceivedData.orderedSendersNbEmails;
};

const handleResize = () => {
    importanceChart?.resize();
    answerRequirementChart?.resize();
    relevanceChart?.resize();
    domainDistributionChart?.resize();
    senderDistributionChart?.resize();
};

onMounted(async () => {
    // First fetch the data
    await fetchDashboardData();

    const importanceChartEl = document.getElementById(chartIds.importance);
    const answerRequirementChartEl = document.getElementById(chartIds.answerRequirement);
    const relevanceChartEl = document.getElementById(chartIds.relevance);
    const domainDistributionChartEl = document.getElementById(chartIds.domainDistribution);
    const senderDistributionChartEl = document.getElementById(chartIds.senderDistribution);

    if (
        !importanceChartEl ||
        !answerRequirementChartEl ||
        !relevanceChartEl ||
        !domainDistributionChartEl ||
        !senderDistributionChartEl ||
        !importanceData // Add check for data
    )
        return;

    // Initialize charts with data
    importanceChart = echarts.init(importanceChartEl, null, {
        renderer: "canvas",
        useDirtyRect: false,
    });
    importanceChart.setOption({
        tooltip: {
            trigger: "item",
            formatter: "{b}: {c}",
        },
        legend: {
            title: "Percentage of emails per category per importance",
        },
        series: {
            type: "sunburst",
            data: importanceData,
            radius: [0, "90%"],
            label: {
                rotate: "radial",
                minAngle: 10,
            },
        },
    });

    ////// answer req part
    const totalData: number[] = [];
    for (let i = 0; i < answerRequiredData[0].length; ++i) {
        let sum = 0;
        for (let j = 0; j < answerRequiredData.length; ++j) {
            sum += answerRequiredData[j][i];
        }
        totalData.push(sum);
    }
    const grid = {
        left: 100,
        right: 100,
        top: 20,
        bottom: 80,
    };
    const answerRequirementSeries = ["Answer Required", "Might Require Answer", "No Answer Required"].map(
        (name, sid) => {
            return {
                name,
                type: "bar",
                stack: "total",
                barWidth: "60%",
                label: {
                    show: true,
                    formatter: (params: { value: number }) => Math.round(params.value * 1000) / 10 + "%",
                },
                data: answerRequiredData[sid].map((d, did) => (totalData[did] <= 0 ? 0 : d / totalData[did])),
            };
        }
    );
    const answerRequirementChartOptions = {
        tooltip: {
            trigger: "item",
            formatter: (params: any) => `${params.seriesName}: ${params.value * totalData[params.dataIndex]}`,
        },
        legend: {
            bottom: 10,
            selectedMode: true,
        },
        grid,
        yAxis: {
            type: "value",
        },
        xAxis: {
            type: "category",
            data: categoryNames,
        },
        series: answerRequirementSeries,
    };
    //// reevance part

    const relevanceChartOptions = {
        legend: {
            bottom: 10,
        },
        tooltip: {},
        dataset: {
            source: relevanceData,
        },
        grid,
        xAxis: { type: "category" },
        yAxis: { type: "value" },
        series: [
            { type: "bar", name: "Highly Relevant" },
            { type: "bar", name: "Possibly Relevant" },
            { type: "bar", name: "Not Relevant" },
        ],
    };

    /// emails received daaa

    const domainDistributionOptions = {
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow",
            },
        },
        grid: {
            top: 20,
            bottom: 20,
            left: 100,
            right: 20,
        },
        xAxis: {
            type: "value",
            position: "top",
            splitLine: {
                lineStyle: {
                    type: "dashed",
                },
            },
        },
        yAxis: {
            type: "category",
            axisLine: { show: true },
            axisLabel: { show: true },
            axisTick: { show: true },
            splitLine: { show: false },
            data: orderedDomains,
        },
        series: [
            {
                name: "Number of emails",
                type: "bar",
                stack: "Total",
                label: {
                    show: true,
                    position: "right",
                },
                data: orderedDomainsNbEmails,
            },
        ],
    };

    const senderDistributionOptions = {
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow",
            },
        },
        grid: {
            top: 20,
            bottom: 20,
            left: 120,
            right: 20,
        },
        xAxis: {
            type: "value",
            position: "top",
            splitLine: {
                lineStyle: {
                    type: "dashed",
                },
            },
        },
        yAxis: {
            type: "category",
            axisLine: { show: true },
            axisLabel: {
                show: true,
                formatter: (value: string) => {
                    const sender = orderedSenders.find((s) => s.email === value);
                    return sender?.name;
                },
            },
            axisTick: { show: true },
            splitLine: { show: false },
            data: orderedSenders.map((sender) => sender.email),
        },
        series: [
            {
                color: "#4f46e5",
                name: "Number of emails",
                type: "bar",
                stack: "Total",
                label: {
                    show: true,
                    position: "right",
                },
                data: orderedSendersNbEmails,
            },
        ],
    };

    domainDistributionChart = echarts.init(domainDistributionChartEl, null, {
        renderer: "canvas",
        useDirtyRect: false,
    });
    domainDistributionChart.setOption(domainDistributionOptions);

    senderDistributionChart = echarts.init(senderDistributionChartEl, null, {
        renderer: "canvas",
        useDirtyRect: false,
    });
    senderDistributionChart.setOption(senderDistributionOptions);

    answerRequirementChart = echarts.init(answerRequirementChartEl, null, {
        renderer: "canvas",
        useDirtyRect: false,
    });
    answerRequirementChart.setOption(answerRequirementChartOptions);

    relevanceChart = echarts.init(relevanceChartEl, null, {
        renderer: "canvas",
        useDirtyRect: false,
    });
    relevanceChart.setOption(relevanceChartOptions);

    window.addEventListener("resize", handleResize);
});

onUnmounted(() => {
    window.removeEventListener("resize", handleResize);
    importanceChart?.dispose();
    answerRequirementChart?.dispose();
    relevanceChart?.dispose();
    domainDistributionChart?.dispose();
    senderDistributionChart?.dispose();
});
</script>
