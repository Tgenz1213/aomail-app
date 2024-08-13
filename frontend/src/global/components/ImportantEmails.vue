<template>
    <div v-if="emails.length > 0" class="px-6 py-6 ">
      <div class="bg-orange-100 bg-opacity-90 rounded-md">
        <div class="flex px-3 py-2">
          <p class="flex-1 text-sm font-semibold leading-6 text-orange-600">
            {{ $t('constants.ruleModalConstants.important') }}
          </p>
          <div class="ml-auto">
            <exclamation-triangle-icon class="w-6 h-6 text-orange-500" />
          </div>
        </div>
      </div>
      <div v-for="(emailsByDate, date) in groupedEmails" :key="date">
        <div class="pt-3 px-4">
          <div class="relative">
            <div class="absolute inset-0 z-0 flex items-center" aria-hidden="true">
              <div class="w-full border-t border-gray-200"></div>
            </div>
            <div class="relative flex justify-center">
              <span class="bg-white px-2 text-xs text-gray-500">{{ date }}</span>
            </div>
          </div>
        </div>
        <div class="flex px-4 pt-4">
          <div class="flex">
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-orange-300">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-white">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
              </svg>
            </span>
          </div>
          <div class="ml-6 flex-grow">
            <div class="overflow-hidden border-l-4 border-orange-300 hover:rounded-l-xl" style="overflow: visible;">
              <ul role="list" class="divide-y divide-gray-200">
                <li v-for="email in emailsByDate" :key="email.id" class="px-6 md:py-5 2xl:py-6 hover:bg-opacity-70 grid grid-cols-10 gap-4 items-center" @mouseover="setHoveredItem(email.id)" @mouseleave="clearHoveredItem">
                    <EmailItem 
                        :email="email" 
                        @emailUpdated="updateEmail"
                    />
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed, ref } from 'vue';
  import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline';
  import { Email } from '@/global/types';
  import EmailItem from '@/global/components/EmailItem.vue';
  
  const props = defineProps<{
    emails: Email[];
  }>();

  const updateEmail = (updatedEmail: Email) => {
    const index = props.emails.findIndex(e => e.id === updatedEmail.id);
    if (index !== -1) {
        props.emails[index] = updatedEmail;
    }
  };
  
  const hoveredItemId = ref<number | null>(null);
  
  const groupedEmails = computed(() => {
    const grouped: Record<string, Email[]> = {};
    props.emails.forEach(email => {
      const sentDate = email.sentDate || 'Unknown Date';
      if (!grouped[sentDate]) {
        grouped[sentDate] = [];
      }
      grouped[sentDate].push(email);
    });
    return grouped;
  });

  
  const setHoveredItem = (id: number) => {
    hoveredItemId.value = id;
  };
  
  const clearHoveredItem = () => {
    hoveredItemId.value = null;
  };
  </script>
  