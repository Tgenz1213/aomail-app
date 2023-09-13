<template>
    <navbar></navbar>
    <Searchbar></Searchbar>
    <div class="lg:pl-20">
        <div class="px-10 py-10">
          <ul role="list" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <li v-for="person in paginatedData" :key="person.email" class="col-span-1 divide-y divide-gray-200 rounded-lg bg-white hover:shadow">
            <div class="flex w-full items-center justify-between space-x-6 p-6">
              <div class="flex-1 truncate">
                <div class="flex items-center space-x-3">
                  <h3 class="truncate text-sm font-medium text-gray-900">{{ person.name }}</h3>
                  <span class="inline-flex flex-shrink-0 items-center rounded-full bg-green-50 px-1.5 py-0.5 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20">{{ person.role }}</span>
                </div>
                <p class="mt-1 truncate text-sm text-gray-500">{{ person.title }}</p>
              </div>
              <img class="h-10 w-10 flex-shrink-0 rounded-full bg-gray-300" :src="person.imageUrl" alt="" />
            </div>
            <div>
              <div class="-mt-px flex divide-x divide-gray-200">
                <div class="flex w-0 flex-1">
                  <div class="relative inline-flex w-0 flex-1 items-center justify-center gap-x-3 rounded-br-lg border border-transparent py-4 text-sm font-semibold text-gray-900">
                    <Bars3CenterLeftIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </div>
                </div>
                <div class="flex w-0 flex-1">
                  <div class="relative inline-flex w-0 flex-1 items-center justify-center gap-x-3 rounded-br-lg border border-transparent py-4 text-sm font-semibold text-gray-900">
                    <EnvelopeIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </div>
                </div>
                <div class="flex w-0 flex-1">
                  <div class="relative inline-flex w-0 flex-1 items-center justify-center gap-x-3 rounded-br-lg border border-transparent py-4 text-sm font-semibold text-gray-900">
                    <Cog8ToothIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </div>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
      <nav class="fixed inset-x-0 bottom-0 left-[5rem] flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6" aria-label="Pagination">
        <div class="hidden sm:block">
          <p class="text-sm text-gray-700">
            Showing
            <span class="font-medium">{{ startItem }}</span>
            to
            <span class="font-medium">{{ endItem }}</span>
            of
            <span class="font-medium">{{ totalItems }}</span>
            results
          </p>
        </div>
        <div class="flex flex-1 justify-between sm:justify-end">
          <a href="#" @click.prevent="previousPage" class="relative inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus-visible:outline-offset-0">Précédent</a>
          <a href="#" @click.prevent="nextPage" class="relative ml-3 inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus-visible:outline-offset-0">Suivant</a>
        </div>
      </nav>
    </div>
</template>

<script setup>
import { EnvelopeIcon, Cog8ToothIcon, Bars3CenterLeftIcon } from '@heroicons/vue/20/solid'
import { ref, computed, onMounted, onUnmounted } from 'vue';

const people = ref([
  {
    name: 'Jane Cooper',
    title: 'janecooper@example.com',
    role: 'Admin',
    email: 'janecooper@example.com',
    telephone: '+1-202-555-0170',
    imageUrl:
      'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=4&w=256&h=256&q=60',
  },
  {
    name: 'John Doe',
    title: 'johndoe@example.com',
    role: 'User',
    email: 'johndoe@example.com',
    telephone: '+1-202-555-0123',
    imageUrl: 'https://randomuser.me/api/portraits/men/0.jpg',
  },
  {
    name: 'Alice Johnson',
    title: 'alicejohnson@example.com',
    role: 'Admin',
    email: 'alicejohnson@example.com',
    telephone: '+1-202-555-0155',
    imageUrl: 'https://randomuser.me/api/portraits/women/1.jpg',
  },
  {
    name: 'Bob Smith',
    title: 'bobsmith@example.com',
    role: 'User',
    email: 'bobsmith@example.com',
    telephone: '+1-202-555-0188',
    imageUrl: 'https://randomuser.me/api/portraits/men/2.jpg',
  },
  {
    name: 'Charlie Brown',
    title: 'charliebrown@example.com',
    role: 'Admin',
    email: 'charliebrown@example.com',
    telephone: '+1-202-555-0199',
    imageUrl: 'https://randomuser.me/api/portraits/men/3.jpg',
  },
  {
    name: 'Diana Prince',
    title: 'dianaprince@example.com',
    role: 'User',
    email: 'dianaprince@example.com',
    telephone: '+1-202-555-0234',
    imageUrl: 'https://randomuser.me/api/portraits/women/4.jpg',
  },
  {
    name: 'Ella Fitzgerald',
    title: 'ellafitzgerald@example.com',
    role: 'Admin',
    email: 'ellafitzgerald@example.com',
    telephone: '+1-202-555-0277',
    imageUrl: 'https://randomuser.me/api/portraits/women/5.jpg',
  },
  {
    name: 'Frank Sinatra',
    title: 'franksinatra@example.com',
    role: 'User',
    email: 'franksinatra@example.com',
    telephone: '+1-202-555-0310',
    imageUrl: 'https://randomuser.me/api/portraits/men/6.jpg',
  },
  {
    name: 'Grace Hopper',
    title: 'gracehopper@example.com',
    role: 'Admin',
    email: 'gracehopper@example.com',
    telephone: '+1-202-555-0344',
    imageUrl: 'https://randomuser.me/api/portraits/women/7.jpg',
  },
  {
    name: 'Harry Potter',
    title: 'harrypotter@example.com',
    role: 'User',
    email: 'harrypotter@example.com',
    telephone: '+1-202-555-0377',
    imageUrl: 'https://randomuser.me/api/portraits/men/8.jpg',
  },
  {
    name: 'Harry Potter',
    title: 'harrypotter@example.com',
    role: 'User',
    email: 'harrypotter@example.com',
    telephone: '+1-202-555-0377',
    imageUrl: 'https://randomuser.me/api/portraits/men/8.jpg',
  },
  {
    name: 'Harry Potter',
    title: 'harrypotter@example.com',
    role: 'User',
    email: 'harrypotter@example.com',
    telephone: '+1-202-555-0377',
    imageUrl: 'https://randomuser.me/api/portraits/men/8.jpg',
  },
  {
    name: 'Harry Potter',
    title: 'harrypotter@example.com',
    role: 'User',
    email: 'harrypotter@example.com',
    telephone: '+1-202-555-0377',
    imageUrl: 'https://randomuser.me/api/portraits/men/8.jpg',
  }
]);


const currentPage = ref(1);
let itemsPerPage = ref(9); // Default value

const setItemsPerPage = () => {
    if (window.innerWidth <= 640) { // Small screens (sm)
        itemsPerPage.value = 3;
    } else if (window.innerWidth <= 768) { // Medium screens (md)
        itemsPerPage.value = 6;
    } else if (window.innerWidth <= 1600) { // Large screens (lg)
        itemsPerPage.value = 9;
    } else { // 2XL and above
        itemsPerPage.value = 12;
    }
    console.log("New itemsPerPage value:", itemsPerPage.value);
};

onMounted(() => {
    console.log('Component has been mounted!');  // This message should appear in the console when the component is mounted
    console.log(window.innerWidth);
    setItemsPerPage(); // Initial set

    // Adjust itemsPerPage dynamically when window resizes
    window.addEventListener('resize', setItemsPerPage);
});

// Cleanup the event listener when component is destroyed
onUnmounted(() => {
    window.removeEventListener('resize', setItemsPerPage);
})

const totalPages = computed(() => {
  return Math.ceil(people.value.length / itemsPerPage.value);
});

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return people.value.slice(start, end);
});

const startItem = computed(() => (currentPage.value - 1) * itemsPerPage.value + 1);
const endItem = computed(() => Math.min(currentPage.value * itemsPerPage.value, people.value.length));
const totalItems = computed(() => people.value.length);

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const goToPage = (page) => {
  currentPage.value = page;
};

</script>

<script>
import Navbar from './components/Navbar.vue';
import Searchbar from './components/Searchbar.vue';
import {
  ChatBubbleOvalLeftEllipsisIcon,
} from '@heroicons/vue/24/outline'

export default {
  components: {
    Navbar,
    ChatBubbleOvalLeftEllipsisIcon,
    Searchbar,
  },
  data() {
    return {
      showHiddenParagraphs: [false, false, false],
      animationTriggered: [false, false, false]
    }
  },
}
</script>
