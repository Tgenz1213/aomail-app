<template>
    <NotificationTimer
        :showNotification="showNotification"
        :notificationTitle="notificationTitle"
        :notificationMessage="notificationMessage"
        :backgroundColor="backgroundColor"
        @dismissPopup="dismissPopup"
    />
    <div class="max-w-2xl mx-auto p-4 border border-gray-200 rounded-lg">
        <SearchMenu />
        <ActionButtons />
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
import { postData } from "@/global/fetchData";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import Label from "./components/Label.vue";
import ActionButtons from "./components/ActionButtons.vue";
import SearchMenu from "./components/SearchMenu.vue";
import { LabelData } from "./utils/types";

const showNotification = ref<boolean>(false);
const notificationTitle = ref<string>("");
const notificationMessage = ref<string>("");
const backgroundColor = ref<string>("");
const timerId = ref<number | null>(null);
const searchQuery = ref<string>("");
const labelsData = ref<LabelData[]>([]);
const loading = ref<boolean>(false);
const loadingMore = ref<boolean>(false);
const ids = ref<number[]>([]);
const selectedLabelIds = ref<number[]>([]);
const page = ref<number>(1);
const sort = ref<string>("carrier");
const order = ref<string>("asc");
const platform = ref("");
const itemName = ref("");
const carrier = ref("");
const postageDeadline = ref<Date | undefined>(undefined);

const searchLabels = async () => {
    loading.value = true;
    labelsData.value = [];

    const payload: any = {
        sort: sort.value,
        order: order.value,
    };

    if (searchQuery.value.trim() !== "") {
        payload.search = searchQuery.value;
    }
    if (platform.value) {
        payload.platform = platform.value;
    }
    if (itemName.value) {
        payload.itemName = itemName.value;
    }
    if (carrier.value) {
        payload.carrier = carrier.value;
    }
    if (postageDeadline.value) {
        payload.postageDeadline = new Date(postageDeadline.value).toISOString();
    }
    if (platform.value || itemName.value || carrier.value || postageDeadline.value) {
        payload.advanced = true;
    }

    const resultIds = await postData("user/label_ids", payload);

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

provide("selectedLabelIds", selectedLabelIds);
provide("ids", ids);
provide("sort", sort);
provide("order", order);
provide("searchQuery", searchQuery);
provide("platform", platform);
provide("itemName", itemName);
provide("carrier", carrier);
provide("postageDeadline", postageDeadline);
provide("displayPopup", displayPopup);
provide("searchLabels", searchLabels);

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
</script>
