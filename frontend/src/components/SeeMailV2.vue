<template>
  <transition name="modal-fade">
    <div @click.self="closeModal"
      class="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center" v-if="isOpen">
      <div class="bg-white rounded-lg relative w-[800px] h-[600px] 2xl:w-[900px] 2xl:h-[800px]">
        <slot></slot>
        <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
          <button @click="closeModal" type="button"
            class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
            <span class="sr-only">Close</span>
            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
        <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
          <div class="ml-8 flex items-center space-x-2">
            <EnvelopeOpenIcon class="w-6 h-6" />
            <p class="block font-semibold leading-6 text-gray-900">{{ email.subject }}</p>
          </div>
        </div>
        <div class="overflow-auto h-[535px] 2xl:h-[736px]">
          <div class="flex flex-col px-8 py-4">
            <div class="mb-3">
              <div class="flex">
                <div class="flex flex-col gap-y-0">
                  <div class="flex items-center gap-x-2">
                    <p class="text-gray-600 font-semibold">{{ email.name }}</p>
                    <p class="text-gray-600 text-sm">&lt;{{ email.email }}&gt;</p>
                  </div>
                  <!-- <div class="flex items-center gap-x-2">
                    <p class="text-gray-600 font-semibold">CC : </p>
                    <p class="text-gray-600 text-sm">theohubert3@gmx.com</p>
                  </div> -->
                </div>
                <div class="flex items-center ml-auto">
                  <!-- <div class="relative group"> -->
                      <div
                          class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg mt-[-45px] -ml-2">
                          {{ $t('SeeMail_vue.more_actions') }} 
                      </div>
                      <div class="flex justify-center">
                        <span class="isolate inline-flex rounded-2xl">
                          
                          <div class="group action-buttons">
                            <div class="relative group">
                                <!-- Adjusted tooltip positioning -->
                                <div
                                    class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg top-full left-0 translate-y-2">
                                    {{ $t('SeeMail_vue.read') }} 
                                </div>
                                <button
                                    @click="markEmailAsRead(email.id)"
                                    type="button"
                                    class="relative inline-flex items-center rounded-l-2xl px-1.5 py-1 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                    <check-icon
                                    class="w-5 h-5 group-hover:text-white text-grey-400 group-active:text-grey-400 group-focus:text-grey focus:text-grey-400" />
                                </button>
                            </div>
                        </div>
                        <div class="group action-buttons">
                          <div class="relative group">
                              <!-- Updated tooltip positioning -->
                              <div
                                  class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg top-full left-0 translate-y-2">
                                  {{ $t('SeeMail_vue.answer') }} 
                              </div>
                              <button @click="openAnswer(email)"
                                  type="button"
                                  class="relative inline-flex items-center px-1.5 py-1 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                  <arrow-uturn-left-icon
                                  class="w-5 h-5 group-hover:text-white text-grey-400 group-active:text-grey-400 group-focus:text-grey focus:text-grey-400" />
                              </button>
                          </div>
                      </div>
                      <div class="group action-buttons">
                          <div class="relative group">
                              <!-- Updated tooltip positioning -->
                              <div
                                  class="absolute hidden group-hover:block px-4 py-2 bg-black text-white text-sm rounded shadow-lg top-full left-0 translate-y-2">
                                  TODO: Répondre
                              </div>
                              <button @click="openRuleEditor"
                                  type="button"
                                  class="relative inline-flex items-center px-1.5 py-1 text-sm font-semibold text-gray-400 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                  <BeakerIcon
                                  class="w-5 h-5 group-hover:text-white text-grey-400 group-active:text-grey-400 group-focus:text-grey focus:text-grey-400" />
                              </button>
                          </div>
                      </div>
                          <div class="group action-buttons">
                              <div class="relative group">
                                  <div
                                    class="absolute hidden group-hover:block px-2 py-2 bg-black text-white text-sm rounded shadow-lg top-full left-0 translate-y-2 -translate-x-3">
                                    {{ $t('SeeMail_vue.more_actions') }} 
                                </div>
                                  <Menu as="div"
                                      class="relative inline-block text-left">
                                      <div>
                                          <MenuButton
                                              @click="toggleTooltip"
                                              class="relative inline-flex items-center rounded-r-2xl px-1.5 py-1 font-semibold text-gray-400 ring-1 ring-inset ring-gray-400 hover:bg-gray-400 focus:z-10">
                                              <ellipsis-horizontal-icon
                                              class="w-5 h-5 group-hover:text-white text-grey-400 group-active:text-grey-400 group-focus:text-grey focus:text-grey-400" />
                                          </MenuButton>
                                        </div>
                                        <transition
                                            enter-active-class="transition ease-out duration-100"
                                            enter-from-class="transform opacity-0 scale-95"
                                            enter-to-class="transform opacity-100 scale-100"
                                            leave-active-class="transition ease-in duration-75"
                                            leave-from-class="transform opacity-100 scale-100"
                                            leave-to-class="transform opacity-0 scale-95">
                                            <MenuItems v-show="isMenuOpen"
                                                class="absolute right-0 z-10 mt-1 w-48 origin-top-right rounded-md bg-white shadow-sm ring-1 ring-black ring-opacity-5 focus:outline-none cursor-pointer">
                                                <div class="py-1">
                                                    <MenuItem
                                                        v-slot="{ active }">
                                                    <a @click.prevent="markEmailReplyLater(email)"
                                                        :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                        <span
                                                            class="flex gap-x-2 items-center">
                                                            <svg class="w-4 h-4"
                                                                viewBox="0 0 28 28"
                                                                version="1.1"
                                                                stroke="currentColor"
                                                                xmlns="http://www.w3.org/2000/svg"
                                                                xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                xml:space="preserve"
                                                                xmlns:serif="http://www.serif.com/"
                                                                style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                                                                <path
                                                                    d="M13.435,17.391l-6.783,-6.782m0,0l6.783,-6.783m-6.783,6.783l13.565,0c3.721,0 6.783,3.061 6.783,6.782c0,3.721 -3.062,6.783 -6.783,6.783l-3.391,0"
                                                                    style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                <path
                                                                    d="M7.783,17.391l-6.783,-6.782m0,0l6.783,-6.783"
                                                                    style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                            </svg>
                                                            <span>TODO: Répondre
                                                                plus
                                                                tard</span>
                                                        </span>
                                                    </a>
                                                    </MenuItem>
                                                </div>
                                                <div class="py-1">
                                                    <MenuItem
                                                        v-slot="{ active }">
                                                    <a @click.prevent="transferEmail(email)"
                                                        :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-1 text-sm']">
                                                        <span
                                                            class="flex gap-x-2 items-center">
                                                            <svg class="w-4 h-4"
                                                                viewBox="0 0 28 28"
                                                                version="1.1"
                                                                stroke="currentColor"
                                                                xmlns="http://www.w3.org/2000/svg"
                                                                xmlns:xlink="http://www.w3.org/1999/xlink"
                                                                xml:space="preserve"
                                                                xmlns:serif="http://www.serif.com/"
                                                                style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;">
                                                                <path
                                                                    d="M13.435,10.609l6.783,6.782m0,0l-6.783,6.783m6.783-6.783L6.85,17.391c-3.721,0-6.783-3.061-6.783-6.782c0-3.721,3.062-6.783,6.783-6.783l3.391,0"
                                                                    style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                                <path
                                                                    d="M21.197,10.609l6.783,6.782m0,0l-6.783,6.783"
                                                                    style="fill:none;stroke:#000;stroke-width:1.7px;" />
                                                            </svg>
                                                            <span>TODO: Transférer</span>
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
                <!--</div> -->
              </div>
            </div>
            <!-- EN cours de dev
            <div class="mb-4">
                <h3 class="text-lg font-medium text-gray-900">À :</h3>
                <p class="text-gray-600">{{ email.cc }}</p>
            </div>-->
            <div class="mb-4">
              <div v-html="email.html_content"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
let isMenuOpen = ref(true);

onMounted(() => {
  document.addEventListener("keydown", handleKeyDown);
});
const emits = defineEmits(['closeModal', 'openAnswer', 'markEmailAsRead', 'openRuleEditor', 'openNewRule', 'markEmailReplyLater']);

const closeModal = () => {
  emits('closeSeeModal');
};

const openAnswer = () => {
  emits('openAnswer', props.email);
}

const openRuleEditor = () => {
  if (props.email.rule) {
    emits('openRuleEditor', props.email.rule_id)
  } else {
    emits('openNewRule', props.email.name, props.email.email)
  }
}

const markEmailAsRead = () => {
  emits('markEmailAsRead', props.email.id);
  closeModal();
}

const markEmailReplyLater = () => {
  emits('markEmailReplyLater', props.email);
  closeModal();
}

const transferEmail = () => {
  emits('transferEmail', props.email);
  closeModal();
}

const props = defineProps({
  isOpen: Boolean,
  email: Object
});

function handleKeyDown(event) {
  if (event.key === 'Escape') {
    closeModal();
  }
}

function toggleTooltip() {
    isMenuOpen.value = true;
}
</script>
<script>
//import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
//import { ExclamationTriangleIcon, XMarkIcon } from '@heroicons/vue/24/outline'
import {
  //ChatBubbleOvalLeftEllipsisIcon,
  //ExclamationTriangleIcon,
  //InformationCircleIcon,
  //TrashIcon,
  ArrowUturnLeftIcon,
  CheckIcon,
  EllipsisHorizontalIcon,
  //HandRaisedIcon,
  //EyeIcon,
  //UserGroupIcon,
  EnvelopeOpenIcon,
  XMarkIcon,
  BeakerIcon
} from '@heroicons/vue/24/outline'

export default {
  components: {
    //ChatBubbleOvalLeftEllipsisIcon,
    //ExclamationTriangleIcon,
    //InformationCircleIcon,
    //TrashIcon,
    ArrowUturnLeftIcon,
    CheckIcon,
    EllipsisHorizontalIcon,
    EnvelopeOpenIcon,
    XMarkIcon,
    BeakerIcon,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    //HandRaisedIcon,
    //EyeIcon,
    //UserGroupIcon
  },
}
</script>