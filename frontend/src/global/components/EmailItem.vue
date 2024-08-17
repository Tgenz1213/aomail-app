<template>
  <div class="grid grid-cols-10 gap-4 items-center" @mouseenter="isHovered = true" @mouseleave="isHovered = false">
    <div class="col-span-8 cursor-pointer">
      <div @click="toggleShortSummary">
        <div class="flex-auto group">
          <div class="flex gap-x-4">
            <div class="flex items-center">
              <p :class="`text-sm font-semibold leading-6 text-${color}-900 mr-2`">{{ email.sender.name }}</p>
              <p :class="`text-sm leading-6 text-${color}-700 mr-2`">{{ email.sentTime }}</p>
            </div>
            <div :class="`hidden group-hover:block px-2 py-0.5 bg-${color}-300 text-white text-sm shadow rounded-xl`">
              <div class="flex gap-x-1 items-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.042 21.672 13.684 16.6m0 0-2.51 2.225.569-9.47 5.227 7.917-3.286-.672Zm-7.518-.267A8.25 8.25 0 1 1 20.25 10.5M8.288 14.212A5.25 5.25 0 1 1 17.25 10.5" />
                </svg>
                <p>{{ $t('constants.userActions.clickToSeeTheSummary') }}</p>
              </div>
            </div>
          </div>
          <p class="mt-1 text-md text-gray-700 leading-relaxed">{{ email.oneLineSummary }}</p>
        </div>
        <div v-show="isShortSummaryVisible">
          <p class="text-black text-sm/6 pt-1.5">{{ email.shortSummary }}</p>
        </div>
        <div class="flex gap-x-2 pt-1.5">
          <span v-if="email.flags.meeting" class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10">
              {{ $t('homePage.flag.meeting') }}
          </span>
          <span v-if="email.flags.newsletter" class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10">
              {{ $t('homePage.flag.newsletter') }}
          </span>
          <span v-if="email.flags.notification" class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/10">
              {{ $t('homePage.flag.notification') }}
          </span>
          <span v-if="email.flags.scam" class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10">
              {{ $t('homePage.flag.scam') }}
          </span>
          <span v-if="email.flags.spam" class="inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/10">
              {{ $t('homePage.flag.spam') }}
          </span>
        </div>
      </div>
      <div v-if="email.hasAttachments" class="flex pt-2.5 gap-x-2">
        <div
          v-for="attachment in email.attachments"
          :key="attachment.attachmentId"
          class="group flex items-center gap-x-1 bg-gray-100 px-2 py-2 rounded-md hover:bg-gray-600"
          @click.prevent="downloadAttachment(email.id, attachment.attachmentName)"
        >
          <component :is="getIconComponent(attachment.attachmentName)" class="w-5 h-5 text-gray-600 group-hover:text-white" />
          <p class="text-sm text-gray-600 group-hover:text-white">{{ attachment.attachmentName }}</p>
        </div>
      </div>
    </div>
    <div class="col-span-2 z-10">
      <div class="flex justify-center">
        <span class="isolate inline-flex rounded-2xl">
          <div v-show="isHovered" class="group action-buttons">
            <div class="relative group">
              <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-4">
                {{ $t('constants.userActions.open') }}
              </div>
              <button @click="openEmail" type="button"
                :class="`relative inline-flex items-center rounded-l-2xl px-2 py-1.5 text-${color}-400 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`">
                <eye-icon :class="`w-5 h-5 text-${color}-400 group-hover:text-white`" />
              </button>
            </div>
          </div>
          <div v-show="isHovered" class="group action-buttons">
            <div class="relative group">
              <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-2">
                {{ $t('homePage.read') }}
              </div>
              <button @click="markEmailAsRead(email.id)" type="button"
                :class="`relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-${color}-900 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`">
                <check-icon :class="`w-5 h-5 text-${color}-400 group-hover:text-white`" />
              </button>
            </div>
          </div>
          <div v-show="isHovered" class="group action-buttons">
            <div class="relative group">
              <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-7">
                {{ $t('homePage.answer') }}
              </div>
              <button @click="openAnswer" type="button"
                :class="`relative -ml-px inline-flex items-center px-2 py-1.5 text-sm font-semibold text-${color}-900 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`">
                <arrow-uturn-left-icon :class="`w-5 h-5 text-${color}-400 group-hover:text-white`" />
              </button>
            </div>
          </div>
          <div v-show="isHovered" class="group action-buttons">
            <div class="relative group">
              <div class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-center text-sm rounded shadow-lg mt-[-45px] -ml-[115px] w-[185px]">
                {{ $t('constants.additionalActions') }}
              </div>
              <Menu as="div" class="relative inline-block text-left">
                <MenuButton @click="toggleMenu"
                  :class="`relative -ml-px inline-flex items-center rounded-r-2xl px-2 py-1.5 text-${color}-400 ring-1 ring-inset ring-${color}-300 hover:bg-${color}-300 focus:z-10`">
                  <ellipsis-horizontal-icon :class="`w-5 h-5 group-hover:text-white text-${color}-400 group-active:text-${color}-400 group-focus:text-${color} focus:text-${color}-400`" />
                </MenuButton>
                <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95"
                  enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75"
                  leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                  <MenuItems v-show="isMenuOpen"
                    class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none cursor-pointer">
                    <div class="py-1">
                      <div v-if="email.rule.hasRule">
                        <MenuItem
                            v-slot="{ active }">
                        <a @click.prevent="openRuleEditor(email.rule.ruleId)"
                            :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                            <span
                                class="flex gap-x-2 items-center">
                                <svg xmlns="http://www.w3.org/2000/svg"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke-width="1.5"
                                    stroke="currentColor"
                                    class="w-4 h-4">
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                </svg>
                                <span> {{ $t('constants.userActions.changeTheRule') }}</span>
                            </span>
                        </a>
                        </MenuItem>
                      </div>
                      <div v-else>
                          <MenuItem
                              v-slot="{ active }">
                          <a @click.prevent="openNewRule(email.sender.name, email.sender.email)"
                              :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                              <span
                                  class="flex gap-x-2 items-center">
                                  <svg xmlns="http://www.w3.org/2000/svg"
                                      fill="none"
                                      viewBox="0 0 24 24"
                                      stroke-width="1.5"
                                      stroke="currentColor"
                                      class="w-4 h-4">
                                      <path
                                          stroke-linecap="round"
                                          stroke-linejoin="round"
                                          d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                                  </svg>
                                  <span>{{ $t('constants.userActions.createARule') }}</span>
                              </span>
                          </a>
                          </MenuItem>
                      </div>
                    </div>
                    <div class="py-1">
                      <MenuItem v-slot="{ active }">
                        <a @click.prevent="markEmailReplyLater(email.id)"
                          :class="[active ? `bg-gray-100 text-gray-900` : `text-gray-700`, 'block px-4 py-1 text-sm']">
                          <span class="flex gap-x-2 items-center">
                            <svg class="w-4 h-4" viewBox="0 0 28 28" version="1.1" stroke="currentColor"
                              xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                              xml:space="preserve" xmlns:serif="http://www.serif.com/"
                              style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                              <path
                                d="M13.435,17.391l-6.783,-6.782m0,0l6.783,-6.783m-6.783,6.783l13.565,0c3.721,0 6.783,3.061 6.783,6.782c0,3.721 -3.062,6.783 -6.783,6.783l-3.391,0"
                                style="fill:none;stroke:#000;stroke-width:1.7px;" />
                              <path d="M7.783,17.391l-6.783,-6.782m0,0l6.783,-6.783"
                                style="fill:none;stroke:#000;stroke-width:1.7px;" />
                            </svg>
                            <span>{{ $t('constants.userActions.replyLater') }}</span>
                          </span>
                        </a>
                      </MenuItem>
                    </div>
                    <div class="py-1">
                      <MenuItem v-slot="{ active }">
                        <a @click.prevent="transferEmail"
                          :class="[active ? `bg-gray-100 text-gray-900` : `text-gray-700`, 'block px-4 py-1 text-sm']">
                          <span class="flex gap-x-2 items-center">
                            <svg class="w-4 h-4" viewBox="0 0 28 28" version="1.1" stroke="currentColor"
                              xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                              xml:space="preserve" xmlns:serif="http://www.serif.com/"
                              style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                              <path
                                d="M13.435,10.609l6.783,6.782m0,0l-6.783,6.783m6.783-6.783L6.85,17.391c-3.721,0-6.783-3.061-6.783-6.782c0-3.721,3.062-6.783,6.783-6.783l3.391,0"
                                style="fill:none;stroke:#000;stroke-width:1.7px;" />
                              <path d="M21.197,10.609l6.783,6.782m0,0l-6.783,6.783"
                                style="fill:none;stroke:#000;stroke-width:1.7px;" />
                            </svg>
                            <span>{{ $t('constants.userActions.transfer') }}</span>
                          </span>
                        </a>
                      </MenuItem>
                    </div>
                  </MenuItems>
                </transition>
              </Menu>
            </div>
          </div>
        </span>
      </div>
    </div>
  </div>
  <SeeMailModal 
    :isOpen="isSeeMailModalVisible" 
    :email="updatedEmail" 
    @closeModal="closeSeeMailModal"
    @openAnswer="handleOpenAnswer"
    @openRuleEditor="handleOpenRuleEditor"
    @openNewRule="handleOpenNewRule"
    @transferEmail="handleTransferEmail"
  />
  </template>
  
  <script setup lang="ts">
  import { Ref, ref, inject } from 'vue';
  import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue';
  import { EyeIcon, CheckIcon, ArrowUturnLeftIcon, EllipsisHorizontalIcon, DocumentIcon, CameraIcon } from '@heroicons/vue/24/outline';
  import { Email } from '@/global/types';
  import { postData } from '@/global/fetchData';
  import { i18n } from "@/global/preferences";
  import SeeMailModal from './SeeMailModal.vue';
  import router from '../../router/router';
    
  const props = withDefaults(defineProps<{
    email: Email;
    color?: string;
  }>(), {
    color: 'gray'
  });

  const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
  const fetchCategoriesAndTotals = inject('fetchCategoriesAndTotals') as () => Promise<void>;  

  const emit = defineEmits<{
    (e: 'emailUpdated', email: Email): void;
  }>();
  
  const isHovered = ref(false);
  const isMenuOpen = ref(false);
  const isShortSummaryVisible = ref(false);
  const isSeeMailModalVisible = ref(false);
  const updatedEmail = ref<Email | undefined>(undefined);
  
  const toggleShortSummary = () => {
    isShortSummaryVisible.value = !isShortSummaryVisible.value;
  };

  const openEmail = async () => {
    const result = await postData(`user/get_email_content/`, { id: props.email.id });
    
    if (result.success && result.data.content) {
      updatedEmail.value = { ...props.email, htmlContent: result.data.content };
      isSeeMailModalVisible.value = true;
      emit('emailUpdated', updatedEmail.value);
    } else {
      console.error("No HTML content received");
    }
  };

  function openRuleEditor(ruleId: number) {
    if (ruleId) {
        router.push({ name: 'rules', query: { idRule: ruleId, editRule: 'true' } });
    }
  }

  function openNewRule(ruleName: string, ruleEmail: string) {
    if (ruleName && ruleEmail) {
        router.push({ name: 'rules', query: { ruleName: ruleName, ruleEmail: ruleEmail, editRule: 'false' } });
    }
  }

  async function markEmailAsRead(emailId: number) {

    const result = await postData(`user/emails/${emailId}/mark_read/`, {});

    if (!result.success) {
        displayPopup?.("error", i18n.global.t("homepage.markEmailReadFailure"), result.error as string);
    }
    fetchCategoriesAndTotals();
    props.email.read = true;
  }

  async function markEmailReplyLater(emailId: number) {
    const result = await postData(`user/emails/${emailId}/mark_reply_later/`, {});

    if (!result.success) {
      displayPopup?.("error", i18n.global.t("homepage.markEmailReplyLaterFailure"), result.error as string);
    }
    fetchCategoriesAndTotals();
    props.email.read = true;
    props.email.answerLater = true;
  }


  const closeSeeMailModal = () => {
    isSeeMailModalVisible.value = false;
  };

  const handleOpenAnswer = (email: Email) => {
    // TODO
    console.log('Ouverture de la réponse pour l\'email:', email);
  };

  const handleMarkEmailAsRead = (emailId: number) => {
    // TODO
    console.log('Marquer l\'email comme lu:', emailId);
  };

  const handleOpenRuleEditor = (ruleId: number) => {
    // TODO
    console.log('Ouverture de l\'éditeur de règles pour la règle:', ruleId);
  };

  const handleOpenNewRule = (senderName: string, senderEmail: string) => {
    // TODO
    console.log('Ouverture d\'une nouvelle règle pour l\'expéditeur:', senderName, senderEmail);
  };

  const handleMarkEmailReplyLater = (email: Email) => {
    // TODO
    console.log('Marquer l\'email pour répondre plus tard:', email);
  };

  const handleTransferEmail = (email: Email) => {
    // TODO
    console.log('Transfert de l\'email:', email);
  };
  
  const openAnswer = () => {
    console.log('Opening answer for email:', props.email);
    emit('emailUpdated', { ...props.email, read: true });
  };
  
  const markReplyLater = async () => {
    try {
      await postData(`user/emails/${props.email.id}/mark_reply_later`, {});
      emit('emailUpdated', { ...props.email, answer: true });
    } catch (error) {
      console.error('Error marking email for reply later:', error);
    }
  };
  
  const transferEmail = () => {
    console.log('Transferring email:', props.email);
  };
  
  const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value;
  };
    
  const getIconComponent = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    if (['png', 'jpg', 'jpeg', 'gif'].includes(extension || '')) {
      return CameraIcon;
    } else {
      return DocumentIcon;
    }
  };
  
  const downloadAttachment = (emailId: number, attachmentName: string) => {
    console.log(`Downloading attachment ${attachmentName} from email ${emailId}`);
  };
  </script>
  