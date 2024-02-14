<template>
    <div v-if="props.isOpen">
        <transition name="modal-fade">
            <div class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
                v-if="isOpen">
                <div class="bg-white rounded-lg relative w-[450px]">
                    <slot></slot>
                    <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block p-8">
                        <button @click="closeModal" type="button"
                            class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                            <span class="sr-only">Close</span>
                            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                        </button>
                    </div>
                    <div class="flex items-center w-full h-16 bg-gray-50 ring-1 ring-black ring-opacity-5 rounded-t-lg">
                        <div class="ml-8 flex items-center space-x-1">
                            <p class="block leading-6 text-gray-900"
                                style="font-family: 'Poppins', sans-serif; font-weight: 500;">Nouvelle catégorie</p>
                        </div>
                    </div>
                    <div class="flex flex-col gap-4 px-8 py-6">
                        <p class="text-red-500" v-if="errorMessage">{{ errorMessage }}</p>
                        <div>
                            <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Nom de la
                                catégorie</label>
                            <div class="mt-2">
                                <input v-model="categoryName" name="email" id="email"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"
                                    placeholder="Administratifs">
                            </div>
                        </div>
                        <div>
                            <label for="about" class="block text-sm font-medium leading-6 text-gray-900">Description brève
                                de la catégorie</label>
                            <div class="mt-2">
                                <textarea v-model="categoryDescription" id="about" name="about" rows="3"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"></textarea>
                            </div>
                            <p class="mt-3 text-sm leading-6 text-gray-600">Cette description permettra à l'assitant à
                                comprendre la catégorie</p>
                        </div>
                        <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
                            <button type="button"
                                class="inline-flex w-full justify-center rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:ml-3 sm:w-auto"
                                @click="addCategory">Créer</button>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { fetchWithToken } from '../router/index.js';
import { ref, defineProps, defineEmits } from 'vue';
import { XMarkIcon } from '@heroicons/vue/20/solid';

const props = defineProps({
    isOpen: Boolean,
    errorMessage: String
});

const emits = defineEmits(['closeModal', 'addCategory']);

const categoryName = ref('');
const categoryDescription = ref('');

const closeModal = () => {
    emits('closeModal');
};

async function addCategory() {

    if (/[,;:/\\.]/.test(categoryName.value)) {
        // TODO emits with different params => show a pop-up with this error
        console.log("Name not accepted. It contains a special character.");
    } else {
        try {
            const fetchedCategories = await fetchWithToken(`http://localhost:9000/MailAssistant/user/categories/`);

            for (let i = 0; i < fetchedCategories.length; i++) {
                if (fetchedCategories[i]['name'] == categoryName.value) {
                    emits('addCategory', { error: 'Category already exists', categoryName: categoryName.value });
                    return;
                }
            }

            // Create the category
            emits('addCategory', { name: categoryName.value, description: categoryDescription.value });
            categoryDescription.value = '';
            categoryName.value = '';

        } catch (error) {
            console.error("Error checking existing categories:", error);
            // TODO: pop-up the error
            return;
        }
    }
}
</script>