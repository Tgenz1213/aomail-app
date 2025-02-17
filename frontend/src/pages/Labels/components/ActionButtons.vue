<template>
    <div class="flex mt-4 space-x-2">
        <button @click="printLabels" class="w-full px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600">
            {{ i18n.global.t("constants.userActions.print") }}
        </button>
        <button @click="toggleSelectAll" class="w-2/5 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
            {{ selectAllText }}
        </button>
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
</template>

<script setup lang="ts">
import { inject, Ref, ref, computed } from "vue";
import { deleteData } from "@/global/fetchData";
import { fetchWithToken } from "@/global/security";
import { API_BASE_URL } from "@/global/const";
import { PDFDocument } from "pdf-lib";
import { LabelData } from "../utils/types";
import { i18n } from "@/global/preferences";

const selectedLabelIds = inject<Ref<number[]>>("selectedLabelIds") || ref([]);
const ids = inject<Ref<number[]>>("ids") || ref([]);
const labelsData = inject<Ref<LabelData[]>>("labelsData") || ref<LabelData[]>([]);

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");

const selectAllText = computed(() =>
    selectedLabelIds.value.length !== labelsData.value.length
        ? i18n.global.t("constants.userActions.selectAll")
        : i18n.global.t("constants.userActions.unselectAll")
);

const toggleSelectAll = () => {
    if (selectedLabelIds.value.length !== labelsData.value.length) {
        selectedLabelIds.value = labelsData.value.map((label) => label.id);
    } else {
        selectedLabelIds.value = [];
    }
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
            displayPopup?.(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.noLabelsFound"),
                i18n.global.t("constants.popUpConstants.errorMessages.noLabelsFoundDesc")
            );
            return;
        }

        const pdfBytes = await pdfDoc.save();
        const pdfUrl = URL.createObjectURL(new Blob([pdfBytes], { type: "application/pdf" }));

        const printWindow = window.open(pdfUrl, "_blank");
        if (printWindow) {
            printWindow.onload = () => {
                printWindow.print();
                URL.revokeObjectURL(pdfUrl);
            };
        } else {
            displayPopup?.(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.printError"),
                i18n.global.t("constants.popUpConstants.errorMessages.printWindowError")
            );
        }
    } catch (error) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.printError"),
            i18n.global.t("constants.popUpConstants.errorMessages.printPreparationError")
        );
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
            displayPopup?.(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.printServerError"),
                i18n.global.t("constants.popUpConstants.errorMessages.noServerResponse")
            );
            return null;
        }

        if (response.ok) {
            const pdfBlob = await response.blob();
            return pdfBlob;
        } else {
            const data = await response.json();
            displayPopup?.(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.printServerError"),
                i18n.global.t("constants.popUpConstants.errorMessages.pdfFetchError", {
                    error: data.error || "Unknown error",
                })
            );
            return null;
        }
    } catch (error) {
        if (error instanceof Error) {
            displayPopup?.(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.printServerError"),
                i18n.global.t("constants.popUpConstants.errorMessages.pdfFetchError", { error: error.message })
            );
        } else {
            displayPopup?.(
                "error",
                i18n.global.t("constants.popUpConstants.errorMessages.printServerError"),
                i18n.global.t("constants.popUpConstants.errorMessages.unknownPdfError")
            );
        }
        return null;
    }
};

const deleteLabels = async () => {
    if (selectedLabelIds.value.length === 0) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.noLabelSelected"),
            i18n.global.t("constants.popUpConstants.errorMessages.selectAtLeastOneLabel")
        );
        return;
    }

    selectedLabelIds.value.forEach((id) => {
        const index = labelsData.value.findIndex((label) => label.id === id);

        if (index !== -1) {
            labelsData.value.splice(index, 1);
        }
    });

    const result = await deleteData("user/delete_labels", { ids: selectedLabelIds.value });

    if (!result.success) {
        displayPopup?.(
            "error",
            i18n.global.t("constants.popUpConstants.errorMessages.failedToDeleteLabels"),
            result.error as string
        );
    } else {
        selectedLabelIds.value = [];
    }
};
</script>
