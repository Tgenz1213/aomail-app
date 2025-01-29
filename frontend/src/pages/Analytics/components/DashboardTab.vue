<template>
    <!-- Email Provider Dashboard Section -->
    <section class="">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">Email Provider Dashboard</h2>
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
        <h2 class="text-xl font-semibold mb-4 text-gray-800">Aomail Dashboard</h2>
        <div class="grid grid-cols-3 gap-6">
            <div class="bg-gray-50 rounded p-4">
                <h3 class="text-sm font-medium text-gray-600 mb-2">Importance distribution per category</h3>
                <div :id="chartIds.importance" class="h-[400px]"></div>
            </div>
            <div class="bg-gray-50 rounded p-4">
                <h3 class="text-sm font-medium text-gray-600 mb-2">Answer Requirements distribution per category</h3>
                <div :id="chartIds.answerRequirement" class="h-[400px]"></div>
            </div>
            <div class="bg-gray-50 rounded p-4">
                <h3 class="text-sm font-medium text-gray-600 mb-2">Email Relevance distribution per category</h3>
                <div :id="chartIds.relevance" class="h-[400px]"></div>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import * as echarts from "echarts";
import { onMounted, onUnmounted } from "vue";

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

const importanceData = [
    {
        name: "Others",
        children: [
            { name: "Important", value: 43 },
            { name: "Informative", value: 87 },
            { name: "Useless", value: 36 },
        ],
    },
    {
        name: "ESAIP",
        children: [
            { name: "Important", value: 12 },
            { name: "Informative", value: 32 },
            { name: "Useless", value: 56 },
        ],
    },
    {
        name: "Aomail Startup",
        children: [
            { name: "Important", value: 67 },
            { name: "Informative", value: 2 },
            { name: "Useless", value: 21 },
        ],
    },
];

const importanceChartOptions = {
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
};

const handleResize = () => {
    importanceChart?.resize();
    answerRequirementChart?.resize();
    relevanceChart?.resize();
    domainDistributionChart?.resize();
    senderDistributionChart?.resize();
};

const rawData = [
    [100, 302, 301],
    [320, 132, 101],
    [220, 182, 191],
];
const totalData: number[] = [];
for (let i = 0; i < rawData[0].length; ++i) {
    let sum = 0;
    for (let j = 0; j < rawData.length; ++j) {
        sum += rawData[j][i];
    }
    totalData.push(sum);
}
const grid = {
    left: 100,
    right: 100,
    top: 50,
    bottom: 50,
};
const answerRequirementSeries = ["Answer Required", "Might Require Answer", "No Answer Required"].map((name, sid) => {
    return {
        name,
        type: "bar",
        stack: "total",
        barWidth: "60%",
        label: {
            show: true,
            formatter: (params: { value: number }) => Math.round(params.value * 1000) / 10 + "%",
        },
        data: rawData[sid].map((d, did) => (totalData[did] <= 0 ? 0 : d / totalData[did])),
    };
});
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
        data: ["Others", "ESAIP", "Aomail Startup"],
    },
    series: answerRequirementSeries,
};

const relevanceChartOptions = {
    legend: {},
    tooltip: {
        formatter: (params: any) => `${params.seriesName}: ${params.value}%`,
    },
    dataset: {
        source: [
            ["category", "Others", "ESAIP", "Aomail Startup"],
            ["Highly Relevant", 41.1, 30.4, 65.1],
            ["Possibly Relevant", 86.5, 92.1, 85.7],
            ["Not Relevant", 24.1, 67.2, 79.5],
        ],
    },
    xAxis: { type: "category" },
    yAxis: { type: "value", show: false },
    grid: { bottom: "55%" },
    series: [
        { type: "bar", seriesLayoutBy: "row" },
        { type: "bar", seriesLayoutBy: "row" },
        { type: "bar", seriesLayoutBy: "row" },
    ],
};

const domainDistributionOptions = {
    title: {
        text: "Emails received per domain",
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
        text: "Emails received per sender",
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

onMounted(() => {
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
        !senderDistributionChartEl
    )
        return;

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

    importanceChart = echarts.init(importanceChartEl, null, {
        renderer: "canvas",
        useDirtyRect: false,
    });
    importanceChart.setOption(importanceChartOptions);

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
