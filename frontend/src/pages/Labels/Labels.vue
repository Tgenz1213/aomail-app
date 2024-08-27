<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
    />
    <div class="max-w-2xl mx-auto p-4 border border-gray-200 rounded-lg">
        <h1 class="text-center text-2xl font-semibold mb-4">Label Search</h1>
        <input
            type="text"
            v-model="searchQuery"
            placeholder="Search labels..."
            @keyup.enter="searchLabels"
            class="w-3/4 p-2 border border-gray-300 rounded-md"
        />
        <button @click="searchLabels" class="ml-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
            Search
        </button>

        <!-- Flex container for Print and Delete buttons with 80-20 width ratio -->
        <div class="flex mt-4 space-x-2">
            <!-- Print button takes 80% of the width -->
            <button @click="printLabels" class="w-4/5 px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600">
                Print
            </button>
            <!-- Delete button takes 20% of the width -->
            <button
                type="button"
                class="w-1/5 flex justify-center items-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700"
                @click="deleteLabels"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="w-6 h-6"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                    />
                </svg>
            </button>
        </div>

        <div v-if="loading" class="text-center mt-4">Loading...</div>
        <div v-if="labelsData.length > 0" class="mt-4">
            <ul class="list-none p-0">
                <Label v-for="label in labelsData" :key="label.id" :label="label" />
            </ul>
        </div>
        <div v-if="!loading && labelsData.length === 0" class="text-center mt-4">No labels found.</div>
        <div ref="loadingIndicator" class="text-center mt-4" v-if="loadingMore">Loading more labels...</div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, provide, watch } from "vue";
import { deleteData, postData } from "@/global/fetchData";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import Label from "./components/Label.vue";
import { LabelData } from "./utils/types";
import { fetchWithToken } from "@/global/security";
import { API_BASE_URL } from "@/global/const";
import { PDFDocument } from "pdf-lib";

const showNotification = ref<boolean>(false);
const notificationTitle = ref<string>("");
const notificationMessage = ref<string>("");
const backgroundColor = ref<string>("");
const timerId = ref<number | null>(null);
const searchQuery = ref("");
const labelsData = ref<LabelData[]>([]);
const loading = ref<boolean>(false);
const loadingMore = ref<boolean>(false);
const ids = ref<number[]>([]);
const selectedLabelIds = ref<number[]>([]);
const page = ref<number>(1);

provide("selectedLabelIds", selectedLabelIds);
provide("displayPopup", displayPopup);

onMounted(() => {
    searchLabels();
    setupInfiniteScroll();
});

function dismissPopup() {
    showNotification.value = false;
    if (timerId.value !== null) {
        clearTimeout(timerId.value);
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

const isFirefox = () => {
    return navigator.userAgent.toLowerCase().indexOf("firefox") > -1;
};

watch(searchQuery, () => {
    page.value = 1;
    labelsData.value = [];
    searchLabels();
});

const setupInfiniteScroll = () => {
    const observer = new IntersectionObserver(
        (entries) => {
            if (entries[0].isIntersecting && !loading.value && !loadingMore.value) {
                fetchMoreLabels();
            }
        },
        {
            rootMargin: "100px",
        }
    );

    if (typeof window !== "undefined") {
        const loadingIndicator = document.querySelector(".text-center.mt-4");
        if (loadingIndicator) {
            observer.observe(loadingIndicator);
        }
    }
};

const fetchMoreLabels = async () => {
    loadingMore.value = true;

    const result = await postData("user/labels_data", {
        ids: ids.value.slice((page.value - 1) * 25, page.value * 25),
    });

    loadingMore.value = false;

    if (!result.success) {
        displayPopup("error", "Failed to fetch label data", result.error as string);
        return;
    }

    labelsData.value.push(...result.data.labelsData);
    page.value += 1;
};

const searchLabels = async () => {
    loading.value = true;

    const resultIds = await postData("user/label_ids", {
        search: searchQuery.value,
    });

    if (!resultIds.success) {
        displayPopup("error", "Failed to fetch label IDs", resultIds.error as string);
        loading.value = false;
        return;
    }

    ids.value = resultIds.data.ids;

    const result = await postData("user/labels_data", {
        ids: resultIds.data.ids.slice(0, 25),
    });

    loading.value = false;

    if (!result.success) {
        displayPopup("error", "Failed to fetch label data", resultIds.error as string);
        return;
    }

    labelsData.value = result.data.labelsData;
};

const printLabels = async () => {
    const labelsToPrint = selectedLabelIds.value.length > 0 ? selectedLabelIds.value : ids.value;

    try {
        const pdfDoc = await PDFDocument.create();
        let totalPages = 0;

        for (const labelId of labelsToPrint) {
            const pdfBlob = await getLabelPdf(labelId);
            if (pdfBlob) {
                const existingPdf = await PDFDocument.load(await pdfBlob.arrayBuffer());
                const copiedPages = await pdfDoc.copyPages(existingPdf, existingPdf.getPageIndices());
                copiedPages.forEach((page: any) => pdfDoc.addPage(page));
                totalPages += copiedPages.length;
            }
        }

        if (totalPages === 0) {
            displayPopup("error", "No labels to print", "No valid labels were found to print.");
            return;
        }

        const pdfBytes = await pdfDoc.save();
        const pdfUrl = URL.createObjectURL(new Blob([pdfBytes], { type: "application/pdf" }));

        if (isFirefox()) {
            const iframe = document.createElement("iframe");
            iframe.style.display = "none";
            document.body.appendChild(iframe);

            iframe.onload = () => {
                try {
                    iframe.contentWindow?.print();
                } catch (error) {
                    displayPopup(
                        "error",
                        "Print error",
                        "Unable to automatically trigger printing. Please check your browser settings."
                    );
                }
                setTimeout(() => {
                    URL.revokeObjectURL(pdfUrl);
                    document.body.removeChild(iframe);
                }, 1000);
            };

            iframe.src = pdfUrl;
        } else {
            const printWindow = window.open(pdfUrl, "_blank");
            if (printWindow) {
                printWindow.onload = () => {
                    printWindow.print();
                    URL.revokeObjectURL(pdfUrl);
                };
            } else {
                displayPopup("error", "Print error", "Unable to open print window. Please check your popup blocker.");
            }
        }
    } catch (error) {
        displayPopup("error", "Print error", "An error occurred while preparing the labels for printing.");
    }
};

const getLabelPdf = async (id: number) => {
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: id }),
    };

    try {
        const response = await fetchWithToken(`${API_BASE_URL}user/label_pdf`, requestOptions);

        if (!response) {
            displayPopup(
                "error",
                "Print Error",
                "No response received from the server while preparing the labels for printing."
            );
            return null;
        }

        if (response.ok) {
            const pdfBlob = await response.blob();
            return pdfBlob;
        } else {
            const data = await response.json();
            displayPopup("error", "Print Error", `Failed to fetch label PDF data: ${data.error || "Unknown error"}`);
            return null;
        }
    } catch (error) {
        if (error instanceof Error) {
            displayPopup("error", "Print Error", `Error fetching PDF for label: ${error.message}`);
        } else {
            displayPopup("error", "Print Error", "An unknown error occurred while fetching the PDF.");
        }
        return null;
    }
};

const deleteLabels = async () => {
    if (selectedLabelIds.value.length === 0) {
        displayPopup("error", "No label selected", "Please select at least one label");
        return;
    }

    const result = await deleteData("user/delete_labels", { ids: [selectedLabelIds.value] });

    if (!result.success) {
        displayPopup("error", "Failed to delete label", result.error as string);
    }
};
</script>
