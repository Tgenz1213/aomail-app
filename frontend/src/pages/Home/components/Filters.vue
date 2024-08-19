<template>
    <div class="flex items-stretch h-12 2xl:h-14 space-x-2 pr-4">
        <button 
        v-for="(tab, index) in visibleTabs" 
        :key="index"
        @click="setActiveTab(tab.id)"
        :class="[
            'px-3 py-1 focus:outline-none flex items-center relative',
            activeTab === tab.id ? 'text-black' : 'text-gray-600 hover:bg-gray-100'
        ]"
        >
        {{ tab.name }}
        <div v-if="activeTab === tab.id" class="absolute bottom-0 left-0 w-full h-0.5 bg-black"></div>
        </button>
        <div class="relative flex items-center">
        <button 
            v-if="hiddenTabsCount > 0"
            @click="toggleMoreFilters" 
            class="px-2 py-1 text-gray-600 hover:bg-gray-100 focus:outline-none"
            data-more-filters
        >
            {{ hiddenTabsCount }} more...
        </button>
        <!-- Modal to display all tabs -->
        <div 
            v-if="showAllTabsModal" 
            ref="moreFiltersModal"
            class="absolute top-full right-0 mt-1 z-50 w-64 rounded-sm bg-white shadow-sm ring-1 ring-black ring-opacity-10"
        >
            <div class="p-2">
            <h2 class="text-sm font-bold mb-2">All tabs</h2>
            <div class="space-y-1 h-full overflow-y-auto">
                <button 
                v-for="tab in allTabs" 
                :key="tab.id"
                @click="setActiveTab(tab.id)"
                class="w-full text-left px-2 py-1 text-sm hover:bg-gray-100 focus:outline-none rounded"
                >
                {{ tab.name }}
                </button>
            </div>
            </div>
        </div>
        </div>
        <button @click="showAddFilterPopup" class="px-2 py-1 text-gray-600 hover:bg-gray-100 focus:outline-none">+</button>
    </div>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { Tab } from "../utils/types";

const allTabs = ref<Tab[]>([
  { id: 'tab1', name: 'Tab 1' },
  { id: 'tab2', name: 'Tab 2' },
  { id: 'tab3', name: 'Tab 3' },
  { id: 'tab4', name: 'Tab 4' },
  { id: 'tab5', name: 'Tab 5' },
  { id: 'tab6', name: 'Tab 6' },
]);

const activeTab = ref(allTabs.value[0].id);
const showAllTabsModal = ref(false);

const hiddenTabsCount = computed(() => {
  return Math.max(0, allTabs.value.length - visibleTabs.value.length);
});

const visibleTabs = computed(() => {
  return allTabs.value.slice(0, 4);
});

const toggleMoreFilters = () => {
  showAllTabsModal.value = !showAllTabsModal.value;
};

const setActiveTab = (tabId: string) => {
  activeTab.value = tabId;
  showAllTabsModal.value = false;
};

const showAddFilterPopup = () => {
  // Implement the logic to show the add filter popup
  console.log('Show add filter popup');
};

</script>