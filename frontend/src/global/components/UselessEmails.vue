<template>
    <div v-if="hasEmails" class="px-6 py-6">
      <div class="bg-gray-100 bg-opacity-90 rounded-md">
        <div class="flex px-2 py-2">
          <p class="flex-1 text-sm font-semibold leading-6 text-gray-600">
            {{ $t('constants.ruleModalConstants.useless') }}
          </p>
          <div class="ml-auto">
            <trash-icon class="w-6 h-6 text-gray-500" />
          </div>
        </div>
      </div>
      <div class="flex gap-x-2">
        <div class="flex gap-x-2 px-6 pt-5 w-full group" @click="toggleEmailVisibility">
          <p
              class="cursor-pointer"> {{ $t('homePage.youReceived') }}
              <span
                  class="font-semibold text-gray-900 dark:text-white hover:text-gray-700 w-full">
                  {{ emails.length }}
              </span>
              <span>
                  {{ $t('homePage.uselessEmails') }}
              </span>
          </p>
          <div :class="`hidden group-hover:block px-2 py-0.5 bg-gray-300 text-white text-sm shadow rounded-xl`">
            <div class="flex gap-x-1 items-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
              </svg>
              <p>{{ $t('constants.userActions.clickToSeeUselessEmails') }}</p>
            </div>
          </div>
        </div>
        <div
            class="hidden group-hover/main:block px-2 py-0.5 bg-gray-400 text-white text-sm shadow rounded-xl">
            <div class="flex gap-x-1 items-center">
                <svg xmlns="http://www.w3.org/2000/svg"
                    fill="none" viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="w-4 h-4">
                    <path stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                </svg>
                <!-- remove @click="toggleEmailVisibility"-->
                <p @click="toggleEmailVisibility"
                    class="cursor-pointer">{{ $t('homePage.clickToSeeTheEmail') }}</p>
            </div>
        </div>
      </div>
      <div v-if="showEmailDescriptions" v-for="(emailsByDate, date) in groupedEmails" :key="date">
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
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-400">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-white">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
              </svg>
            </span>
          </div>
          <div class="ml-6 flex-grow">
            <div class="overflow-hidden border-l-4 hover:rounded-l-xl border-gray-300" style="overflow: visible;">
              <ul role="list" class="divide-y divide-gray-200">
                <li v-for="email in emailsByDate" :key="email.id" class="px-6 md:py-5 2xl:py-6">
                    <EmailItem 
                      :email="email"
                      :block=true
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
  import { computed, ref, watch } from 'vue';
  import { TrashIcon } from '@heroicons/vue/24/outline';
  import { Email } from '@/global/types';
  import EmailItem from '@/global/components/EmailItem.vue';
  
  const props = defineProps<{
    emails: Email[];
  }>();
  
  let showEmailDescriptions = ref(false);
  const localEmails = ref<Email[]>([]);

  watch(() => props.emails, (newEmails) => {
    localEmails.value = [...newEmails];
  }, { immediate: true, deep: true });

  const groupedEmails = computed(() => {
    const grouped: Record<string, Email[]> = {};
    localEmails.value.forEach(email => {
      if (!email.read) {
        const sentDate = email.sentDate || 'Unknown Date';
        if (!grouped[sentDate]) {
          grouped[sentDate] = [];
        }
        grouped[sentDate].push(email);
      }
    });
    return grouped;
  });

  const hasEmails = computed(() => {
    return Object.keys(groupedEmails.value).length > 0;
  });
  function toggleEmailVisibility() {
    showEmailDescriptions.value = !showEmailDescriptions.value;
    /*
    if (readEmailsInSelectedTopic() == 0) {
        scrollToBottom();
    } else {
        scrollAlmostToBottom();
    }*/
  }
  </script>
  
