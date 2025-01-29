<template>
    <!-- Email Provider Dashboard Section -->
    <section class="">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">{{ $t('analyticsPage.analytics.emailProviderData') }}</h2>
        <div class="grid grid-cols-2 gap-4">
            <div class="h-[300px]">
                <div :id="chartIds.domainDistribution" class="w-full h-full"></div>
            </div>
            <div class="h-[300px]">
                <div :id="chartIds.senderDistribution" class="w-full h-full"></div>
            </div>
        </div>
    </section>

    <!-- Aomail Dashboard Section -->
    <section class="">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">{{ $t('analyticsPage.analytics.aomailData') }}</h2>
        <div class="grid grid-cols-3 gap-6">
            <div class="bg-gray-50 rounded p-4">
                <h3 class="text-sm font-medium text-gray-600 mb-2">{{ $t('analyticsPage.analytics.importanceDistribution') }}</h3>
                <div :id="chartIds.importance" class="h-[400px]"></div>
            </div>
            <div class="bg-gray-50 rounded p-4">
                <h3 class="text-sm font-medium text-gray-600 mb-2">{{ $t('analyticsPage.analytics.answerRequirementDistribution') }}</h3>
                <div :id="chartIds.answerRequirement" class="h-[400px]"></div>
            </div>
            <div class="bg-gray-50 rounded p-4">
                <h3 class="text-sm font-medium text-gray-600 mb-2">{{ $t('analyticsPage.analytics.relevanceDistribution') }}</h3>
                <div :id="chartIds.relevance" class="h-[400px]"></div>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { getData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";
import * as echarts from "echarts";
import { inject, onMounted, onUnmounted } from "vue";

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
}

interface ImportanceData {
    name: string;
    children: { name: string; value: number }[];
}
let importanceData: ImportanceData[] | undefined;
let answerRequiredData: number[][] = [];
let categoryNames: string[];
let relevanceData: (string | number)[][] = [];

const fetchDashboardData = async () => {
    const response = await getData("user/dashboard_data/");

    if (!response.success) {
        displayPopup?.("error", "Failed to fetch dashboard data", response.error as string);
        return;
    }

    const distributionData = response.data as DashboardData;
    categoryNames = Object.keys(distributionData.distribution);

    const answerRequiredRow = categoryNames.map(
        (category) => distributionData.distribution[category].nbEmailsAnswerRequired
    );
    const mightRequireAnswerRow = categoryNames.map(
        (category) => distributionData.distribution[category].nbEmailsMightRequireAnswer
    );
    const noAnswerRequiredRow = categoryNames.map(
        (category) => distributionData.distribution[category].nbEmailsNoAnswerRequired
    );
    answerRequiredData = [answerRequiredRow, mightRequireAnswerRow, noAnswerRequiredRow];

    importanceData = Object.entries(distributionData.distribution).map(([category, data]) => ({
        name: category,
        children: [
            { name: "Important", value: data.nbEmailsImportant },
            { name: "Informative", value: data.nbEmailsInformative },
            { name: "Useless", value: data.nbEmailsUseless },
        ],
    }));

    categoryNames.forEach((category) => console.log(distributionData.distribution[category].nbEmailsAnswerRequired));

    /// relevant stuff

    // Reset relevanceData before populating
    relevanceData = [];

    // Add header row first
    relevanceData.push(["Category", "Highly Relevant", "Possibly Relevant", "Not Relevant"]);

    // Add data rows
    categoryNames.forEach((category) =>
        relevanceData.push([
            category,
            distributionData.distribution[category].nbEmailsHighlyRelevant,
            distributionData.distribution[category].nbEmailsPossiblyRelevant,
            distributionData.distribution[category].nbEmailsNotRelevant,
        ])
    );
};

const handleResize = () => {
    importanceChart?.resize();
    answerRequirementChart?.resize();
    relevanceChart?.resize();
    domainDistributionChart?.resize();
    senderDistributionChart?.resize();
};

const domainDistributionOptions = {
    title: {
        text: i18n.global.t('analyticsPage.analytics.emailsReceivedPerDomain'),
        textStyle: {
            fontSize: 14,
            fontWeight: "normal",
        },
    },
    tooltip: {
        trigger: "axis",
        axisPointer: {
            type: "shadow",
        },
    },
    grid: {
        top: 40,
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
        data: ["esaip.org", "linkedin.com", "google.com", "sfr.fr", "alphapen.fr"],
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
            data: [40, 45, 32, 26, 32],
        },
    ],
};

const senderDistributionOptions = {
    title: {
        text: i18n.global.t('analyticsPage.analytics.emailsReceivedPerSender'),
        textStyle: {
            fontSize: 14,
            fontWeight: "normal",
        },
    },
    tooltip: {
        trigger: "axis",
        axisPointer: {
            type: "shadow",
        },
        formatter: (params: any) => {
            const data = params[0];
            return `${data.name}: ${data.value}<br/>Email: ${data.axisValue}`;
        },
    },
    grid: {
        top: 40,
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
                const name = value.split(" ")[0] + " " + (value.split(" ")[1] || "");
                return name;
            },
        },
        axisTick: { show: true },
        splitLine: { show: false },
        data: [
            "Augustin ROLET augustin.rolet.pro@gmail.com",
            "notification@linkedin.com",
            "no-reply@google.com",
            "Jean DUPONT bonjour@orange.com",
            "Benoit GIRO colis@amazon.fr",
        ],
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
            data: [22, 4, 27, 11, 13],
        },
    ],
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
        top: 50,
        bottom: 50,
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
            title: "Percentage of emails per category per answer requirement",
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
        legend: {},
        tooltip: {},
        dataset: {
            source: relevanceData,
        },
        xAxis: { type: "category" },
        yAxis: { type: "value" },
        series: [
            { type: "bar", name: "Highly Relevant" },
            { type: "bar", name: "Possibly Relevant" },
            { type: "bar", name: "Not Relevant" },
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
