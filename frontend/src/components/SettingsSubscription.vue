<template>
  <!-- Template -->
  <div class="mt-6 flex justify-center w-full">
    <RadioGroup v-model="frequency"
      class="grid grid-cols-2 gap-x-1 rounded-full p-1 text-center text-xs font-semibold leading-5 ring-1 ring-inset ring-gray-200">
      <RadioGroupLabel class="sr-only">Payment frequency</RadioGroupLabel>
      <RadioGroupOption as="template" v-for="option in frequencies" :key="option.value" :value="option"
        v-slot="{ checked }">
        <div :class="[checked ? 'bg-gray-800 text-white' : 'text-gray-500', 'cursor-pointer rounded-full px-2.5 py-1']">
          <span>{{ option.label }}</span>
        </div>
      </RadioGroupOption>
    </RadioGroup>
  </div>
  <div class="isolate mx-auto mt-6 grid max-w-md grid-cols-1 gap-8 lg:mx-0 lg:max-w-none lg:grid-cols-3">
    <div v-for="tier in tiers" :key="tier.id"
      :class="[tier.mostPopular ? 'ring-2 ring-gray-800' : 'ring-1 ring-gray-200', 'rounded-3xl p-8 xl:p-10']">
      <div class="flex items-center justify-between gap-x-4">
        <h3 :id="tier.id"
          :class="[tier.mostPopular ? 'text-gray-800' : 'text-gray-900', 'text-lg font-semibold leading-8']">{{
            tier.name
          }}</h3>
        <!-- Hide for test v1 <p v-if="tier.mostPopular" class="rounded-full bg-gray-600/10 px-2.5 py-1 text-xs font-semibold leading-5 text-gray-600">Most popular</p>-->
      </div>
      <p class="mt-4 text-sm leading-6 text-gray-600">{{ tier.description }}</p>
      <p class="mt-6 flex items-baseline gap-x-1">
        <span class="text-4xl font-bold tracking-tight text-gray-900">{{ tier.price[frequency.value] }}</span>
        <span class="text-sm font-semibold leading-6 text-gray-600">{{ frequency.priceSuffix }}</span>
      </p>
      <!-- <a :href="tier.href" :aria-describedby="tier.id"
        :class="[tier.mostPopular ? 'bg-gray-800 text-white shadow-sm hover:bg-gray-600' : 'text-gray-800 ring-1 ring-inset ring-gray-200 hover:ring-gray-300', 'mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800']">Sélectionner</a> -->


      <a @click="$emit('openBillingModal')" :aria-describedby="tier.id"
        :class="[tier.mostPopular ? 'bg-gray-800 text-white shadow-sm hover:bg-gray-600 cursor-pointer' : 'text-gray-800 ring-1 ring-inset ring-gray-200 hover:ring-gray-300', 'mt-6 block rounded-md py-2 px-3 text-center text-sm font-semibold leading-6 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-800 cursor-pointer']">Sélectionner</a>

      <ul role="list" class="mt-8 space-y-3 text-sm leading-6 text-gray-600 xl:mt-10">
        <li v-for="feature in tier.features" :key="feature" class="flex gap-x-3">
          <CheckIcon class="h-6 w-5 flex-none text-gray-800" aria-hidden="true" />
          {{ feature }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { RadioGroup, RadioGroupLabel, RadioGroupOption } from '@headlessui/vue'
import { CheckIcon } from '@heroicons/vue/20/solid'
import { ref } from 'vue';

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
    features: [
      'Nombre d\'email: 1',
      'Modèle IA: Claude',
      'Fournisseurs: Gmail'
    ],
    mostPopular: false,
  },
  {
    name: 'Testeur',
    id: 'tier-startup',
    href: '#',
    price: { monthly: '0€', annually: '0€' },
    description: "Vous utilisez une version test de l'outil",
    features: [
      'Nombre d\'email: 1',
      'Modèles IA: Claude',
      'Fournisseurs: Outlook, Gmail'
    ],
    mostPopular: true,
  },
  // {
  //   name: 'Open Source',
  //   id: 'tier-opensource',
  //   href: '#',
  //   price: { monthly: '0€', annually: '0€' },
  //   description: 'Vous utilisez une version test de l\'outil',
  //   features: [
  //     'Nombre d\'email: 3',
  //     'Modèle IA: Mistral',
  //     'Fournisseurs: Outlook, Gmail, Apple'
  //   ],
  //   mostPopular: false,
  // },
  {
    name: 'Pro',
    id: 'tier-enterprise',
    href: '#',
    price: { monthly: 'x€', annually: 'x€' },
    description: 'En cours de développement',
    features: [
      'Nombre d\'email: 10',
      'Modèles IA: GPT, Claude, Mistral',
      'Support prioritaire',
      'Fournisseurs: Outlook, Gmail, Apple',
      //'Fine-tuning'
    ],
    mostPopular: false,
  },
]

const frequency = ref(frequencies[0])
</script>