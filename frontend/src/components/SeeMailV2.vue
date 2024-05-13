<template>
  <transition name="modal-fade">
    <div class="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center" v-if="isOpen">
      <div class="bg-white rounded-lg relative w-[800px] h-[600px]">
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
        <div class="overflow-auto h-[535px]">
          <div class="flex flex-col px-8">
            <div class="mb-4">
                <div class="flex items-center gap-x-2">
                  <p class="text-gray-600 font-semibold">{{ email.name }}</p>
                  <p class="text-gray-600 text-sm">&lt;{{ email.email }}&gt;</p>
                </div>
            </div>
            <!-- EN cours de dev
            <div class="mb-4">
                <h3 class="text-lg font-medium text-gray-900">À :</h3>
                <p class="text-gray-600">{{ email.cc }}</p>
            </div>-->
            <div class="mb-4">
                <h3 class="text-lg font-medium text-gray-900">Message :</h3>
                <div v-html="email.html_content"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>
    
  <script setup>
  //import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
  //import { ExclamationTriangleIcon, XMarkIcon } from '@heroicons/vue/24/outline'
  </script>
  <script>
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
    XMarkIcon
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
      XMarkIcon
      //HandRaisedIcon,
      //EyeIcon,
      //UserGroupIcon
    },
    props: {
      isOpen: {
        type: Boolean,
        required: true
      },
      email: Object
    },
    methods: {
      closeModal() {
        this.$emit('closeSeeModal');
      }
    }
  }
  </script>