<template>
    <div class="flex flex-col justify-center items-center h-screen" :class="bgColor">
      <div class="grid grid-cols-11 2xl:grid-cols-7 gap-8 2xl:gap-6">
        <div class="col-span-1 2xl:col-span-1">
          <div class="2xl:hidden h-full">
            <navbar></navbar>
          </div>
          <div class="hidden 2xl:block h-full">
            <navbar2></navbar2>
          </div>
        </div>
        <div class="col-span-10 2xl:col-span-6 bg-white rounded-xl lg:ring-1 lg:ring-black lg:ring-opacity-5 shadow hover:shadow-lg xl:h-[93vh] xl:w-[86vw] 2xl:h-[825px] 2xl:w-[1450px]">
          <div class="flex flex-col h-full divide-y divide-gray-200">
            <div class="flex items-center justify-center h-[65px] 2xl:h-[75px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-50">
              <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">Abonnements</h1>
            </div>
            <!-- Subscriptions section moved above -->
            <div class="mt-6 flex justify-center w-full">
              <RadioGroup v-model="frequency" class="grid grid-cols-2 gap-x-1 rounded-full p-1 text-center text-xs font-semibold leading-5 ring-1 ring-inset ring-gray-200">
                <RadioGroupLabel class="sr-only">Payment frequency</RadioGroupLabel>
                <RadioGroupOption as="template" v-for="option in frequencies" :key="option.value" :value="option" v-slot="{ checked }">
                  <div :class="[checked ? 'bg-gray-800 text-white' : 'text-gray-500', 'cursor-pointer rounded-full px-2.5 py-1']">
                    <span>{{ option.label }}</span>
                  </div>
                </RadioGroupOption>
              </RadioGroup>
            </div>
            <div class="isolate mx-auto mt-6 grid max-w-md grid-cols-1 gap-8 lg:mx-0 lg:max-w-none lg:grid-cols-3">
              <div v-for="tier in tiers" :key="tier.id" :class="[tier.mostPopular ? 'ring-2 ring-gray-800' : 'ring-1 ring-gray-200', 'rounded-3xl p-8 xl:p-10']">
                <div class="flex items-center justify-between gap-x-4">
                  <h3 :id="tier.id" :class="[tier.mostPopular ? 'text-gray-800' : 'text-gray-900', 'text-lg font-semibold leading-8']">{{ tier.name }}</h3>
                </div>
                <p class="mt-4 text-sm leading-6 text-gray-600">{{ tier.description }}</p>
                <p class="mt-6 flex items-baseline gap-x-1">
                  <span class="text-4xl font-bold tracking-tight text-gray-900">{{ tier.price[frequency.value] }}</span>
                  <span class="text-sm font-semibold leading-6 text-gray-600">{{ frequency.priceSuffix }}</span>
                </p>
                <a :href="tier.href" :aria-describedby="tier.id" :class="[tier.mostPopular ? 'bg-gray-800 text-white shadow-sm hover:bg-gray-600' : 'text-gray-800 ring-1 ring-inset ring-gray-200 hover:ring-gray-300', 'mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800']">Sélectionner</a>
                <ul role="list" class="mt-8 space-y-3 text-sm leading-6 text-gray-600 xl:mt-10">
                  <li v-for="feature in tier.features" :key="feature" class="flex gap-x-3">
                    <CheckIcon class="h-6 w-5 flex-none text-gray-800" aria-hidden="true" />
                    {{ feature }}
                  </li>
                </ul>
              </div>
            </div>
            <div class="flex-grow overflow-y-auto" style="margin-right: 2px;">
              <div class="px-4 py-2 h-full">
              </div>
            </div>            
          </div>
        </div>
      </div>
    </div>
  </template>
  

<script setup>
import { ref } from 'vue'
import { RadioGroup, RadioGroupLabel, RadioGroupOption } from '@headlessui/vue'
import { CheckIcon } from '@heroicons/vue/20/solid'


let bgColor = ref('');
bgColor = localStorage.getItem('bgColor');

const frequencies = [
    { value: 'monthly', label: 'Mensuel', priceSuffix: '/mois' },
    { value: 'annually', label: 'Annuel', priceSuffix: '/an' },
]
const tiers = [
    {
        name: 'Start',
        id: 'tier-freelancer',
        href: '#',
        price: { monthly: 'x€', annually: 'x€' },
        description: 'En cours de développement',
        features: [],
        mostPopular: false,
    },
    {
        name: 'Testeur',
        id: 'tier-startup',
        href: '#',
        price: { monthly: '0€', annually: '0€' },
        description: "Vous utilisez une version test de l'outil",
        features: [],
        mostPopular: true,
    },
    {
        name: 'Pro',
        id: 'tier-enterprise',
        href: '#',
        price: { monthly: 'x€', annually: 'x€' },
        description: 'En cours de développement',
        features: [
          'Unlimited products',
          'Unlimited subscribers',
          'Advanced analytics',
          '1-hour, dedicated support response time',
          'Marketing automations',
          'Custom reporting tools',
        ],
        mostPopular: false,
    },
]

const frequency = ref(frequencies[0])
</script>

<script>
import { onMounted, ref } from 'vue';
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';
import { fetchWithToken, getBackgroundColor } from '../router/index.js';
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue';
import { API_BASE_URL } from '@/main';
import {
  TrashIcon,
  ArrowUturnLeftIcon,
  EllipsisHorizontalIcon,
  EyeIcon,
  InformationCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline';

export default {
  components: {
    Navbar,
    Navbar2,
    MenuItem,
    MenuItems,
    Menu,
    MenuButton,
    TrashIcon,
    ArrowUturnLeftIcon,
    EllipsisHorizontalIcon,
    EyeIcon,
    InformationCircleIcon,
    ExclamationTriangleIcon
  }
}
</script>