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
    <section class="pt-12">
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
import { init, EChartsType } from "echarts/core";
import { BarChart, SunburstChart } from "echarts/charts";
import {
    TitleComponent,
    TooltipComponent,
    GridComponent,
    DatasetComponent,
    LegendComponent,
} from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import { inject, onMounted, onUnmounted } from "vue";
import ChartTitle from "./CharTitle.vue";
import { use } from "echarts/core";

use([
    TitleComponent,
    TooltipComponent,
    GridComponent,
    DatasetComponent,
    LegendComponent,
    BarChart,
    SunburstChart,
    CanvasRenderer
]);

const modernColorPalette = [
    'rgba(59, 130, 246, 0.6)',   
    'rgba(16, 185, 129, 0.6)',   
    'rgba(245, 158, 11, 0.6)',   
    'rgba(239, 68, 68, 0.6)',    
    'rgba(139, 92, 246, 0.6)',   
    'rgba(20, 184, 166, 0.6)',   
    'rgba(249, 115, 22, 0.6)',   
    'rgba(99, 102, 241, 0.6)',   
    'rgba(236, 72, 153, 0.6)'   
];

const barSeriesDefaultOptions = {
    type: 'bar',
    itemStyle: {
        borderColor: 'rgba(0, 0, 0, 0.2)',
        borderWidth: 1,
        borderRadius: 2,
    }
};

let importanceChart: EChartsType;
let answerRequirementChart: EChartsType;
let relevanceChart: EChartsType;
let domainDistributionChart: EChartsType;
let senderDistributionChart: EChartsType;

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
            { name: i18n.global.t("analyticsPage.analytics.charts.importance.important"), value: data.nbEmailsImportant },
            { name: i18n.global.t("analyticsPage.analytics.charts.importance.informative"), value: data.nbEmailsInformative },
            { name: i18n.global.t("analyticsPage.analytics.charts.importance.useless"), value: data.nbEmailsUseless },
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
    importanceChart = init(importanceChartEl, null, {
        renderer: "canvas",
        useDirtyRect: false,
    });
    importanceChart.setOption({
        color: modernColorPalette,
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
                color: 'rgba(0, 0, 0, 0.75)', // Slightly softer black
                fontWeight: '500' // Medium weight instead of bold
            },
        },
    });

    // Answer Requirement Chart
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
        (name, sid) => ({
            ...barSeriesDefaultOptions,
            name,
            stack: "total",
            barWidth: "60%",
            label: {
                show: true,
                formatter: (params: { value: number }) =>
                    Math.round(params.value * 1000) / 10 + "%",
                color: 'rgba(0, 0, 0, 0.75)', // Slightly softer black
                fontWeight: '500' // Medium weight instead of bold
            },
            data: answerRequiredData[sid].map((d, did) =>
                totalData[did] <= 0 ? 0 : d / totalData[did]
            ),
        })
    );
    const answerRequirementChartOptions = {
        color: modernColorPalette,
        tooltip: {
            trigger: "item",
            formatter: (params: any) =>
                `${params.seriesName}: ${params.value * totalData[params.dataIndex]}`,
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

    // Relevance Chart
    const relevanceChartOptions = {
        color: modernColorPalette,
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
            { ...barSeriesDefaultOptions, name: i18n.global.t("analyticsPage.analytics.charts.relevance.highlyRelevant") },
            { ...barSeriesDefaultOptions, name: i18n.global.t("analyticsPage.analytics.charts.relevance.possiblyRelevant") },
            { ...barSeriesDefaultOptions, name: i18n.global.t("analyticsPage.analytics.charts.relevance.notRelevant") },
        ],
    };

    // Domain Distribution Chart
    const domainDistributionOptions = {
        color: modernColorPalette,
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
                ...barSeriesDefaultOptions,
                name: "Number of emails",
                stack: "Total",
                label: {
                    show: true,
                    position: "right",
                },
                data: orderedDomainsNbEmails,
            },
        ],
    };

    // Sender Distribution Chart
    const senderDistributionOptions = {
        color: modernColorPalette,
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
                ...barSeriesDefaultOptions,
                name: "Number of emails",
                stack: "Total",
                label: {
                    show: true,
                    position: "right",
                },
                data: orderedSendersNbEmails,
            },
        ],
    };

    domainDistributionChart = init(domainDistributionChartEl, null, {
        renderer: "canvas",
        useDirtyRect: false,
    });
    domainDistributionChart.setOption(domainDistributionOptions);

    senderDistributionChart = init(senderDistributionChartEl, null, {
        renderer: "canvas",
        useDirtyRect: false,
    });
    senderDistributionChart.setOption(senderDistributionOptions);

    answerRequirementChart = init(answerRequirementChartEl, null, {
        renderer: "canvas",
        useDirtyRect: false,
    });
    answerRequirementChart.setOption(answerRequirementChartOptions);

    relevanceChart = init(relevanceChartEl, null, {
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