<template>
    <navbar></navbar>
    <main class="py-7 lg:pl-20">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-6 gap-6">
                <div class="col-span-2">
                    <!-- Assistant Up -->
                    <div class="flex pb-6">
                        <div class="mr-4 flex-shrink-0 self-center">
                            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-indigo-600">
                                <span class="text-lg font-medium leading-none text-white">AO</span>
                            </span>
                        </div>
                        <div>
                            <p class="mt-1">Bonjour ! Vous avez reçu 4 nouveau mail. Rien d'urgent à signaler</p>
                        </div>
                    </div>
                </div>
                <div class="col-span-4 pt-8">
                    <div class="grid grid-cols-4 gap-0 flex flex-col justify-center h-full">
                        
                        <div class="flex flex-col justify-center items-center h-full bg-white rounded-t-lg border-l-2 border-l-yellow-600/20 border-opacity-40 border-r-2 border-r-yellow-600/20 border-t-2 border-t-yellow-600/20 z-10 pt-2">
                            <span class="inline-flex items-center justify-center text-center rounded-md bg-yellow-50  w-10/12 h-5/6 text-md font-medium text-yellow-800 ring-1 ring-inset ring-yellow-600/20">ESAIP</span>
                        </div>
                        <div class="flex flex-col justify-center items-center h-full bg-indigo-600/20 rounded-t-lg">
                            <span class="inline-flex items-center rounded-md text-md font-medium text-indigo-600">Entrepreneuriat</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="inline-block min-h-[81vh] w-full px-8 pb-8 rounded-lg bg-white ring-2 ring-yellow-600/20 ring-opacity-40">
                <!-- Content goes here -->
                <ul role="list" class="divide-y divide-gray-200">
                    <li class="py-10">
                        <!-- Your content -->
                        <div class="grid grid-cols-12 gap-0">
                            <div class="col-span-1">
                                <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-red-400">
                                    <span class="text-lg font-medium leading-none text-white">AO</span>
                                </span>
                            </div>
                            <div class="col-span-11">
                                <div class="overflow-hidden rounded-md bg-red-50 shadow">
                                    <ul role="list" class="divide-y divide-gray-200">
                                        <li class="px-6 py-4">
                                        <!-- Your content -->
                                        </li>

                                        <!-- More items... -->
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </li>
                    <!-- More items... -->
                </ul>
            </div>
      </div>
    </main>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  components: {
    Navbar
  }
}
</script>
