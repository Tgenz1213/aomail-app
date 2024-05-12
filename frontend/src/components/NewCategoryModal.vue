<template>
    <div v-if="props.isOpen">
        <transition name="modal-fade">
            <div @click.self="closeModal" class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
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
                                <input id="categoryName" v-model="categoryName"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6"
                                    placeholder="Administratifs">
                            </div>
                        </div>
                        <div>
                            <label for="about" class="block text-sm font-medium leading-6 text-gray-900">Description
                                brève
                                de la catégorie</label>
                            <div class="mt-2">
                                <textarea id="categoryDescription" v-model="categoryDescription" rows="3"
                                    style="min-height: 60px"
                                    class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:text-sm sm:leading-6">
                                </textarea>
                            </div>
                            <p class="mt-3 text-sm leading-6 text-gray-600">Cette description permettra à l'assitant à
                                comprendre la catégorie</p>
                        </div>
                        <div class="mt-2 sm:mt-2 sm:flex sm:flex-row-reverse">
                            <button type="button" class="inline-flex w-full rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:w-auto"
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
import { ref } from 'vue';
import { XMarkIcon } from '@heroicons/vue/20/solid';
import { onMounted } from 'vue';
import { API_BASE_URL } from '@/main';

const props = defineProps({
    isOpen: Boolean,
    errorMessage: String
});

const emits = defineEmits(['closeModal', 'addCategory']);

let categoryName = ref('');
let categoryDescription = ref('');
let errorMessage = ref('');

const closeModal = () => {
    errorMessage.value = '';
    emits('closeModal');
};

onMounted(() => {
    document.addEventListener("keydown", handleKeyDown);
});

async function addCategory() {
    errorMessage.value = '';

    // if (/[^a-zA-Z\s]/.test(categoryName.value)) {
    //     errorMessage.value = 'Le nom de la catégorie contient un caractère interdit : lettres et espaces uniquement';
    // } else 
    if (categoryDescription.value.length > 300) {
        errorMessage.value = "Pas plus de 300 caractères pour la description";
    } else if (categoryName.value.length > 50) {
        errorMessage.value = "Pas plus de 50 caractères pour le nom";
    } else if (!categoryName.value.trim() || !categoryDescription.value.trim()) {
        errorMessage.value = "Veuillez remplir tous les champs";
    } else {
        try {
            const fetchedCategories = await fetchWithToken(`${API_BASE_URL}user/categories/`);

            for (let i = 0; i < fetchedCategories.length; i++) {
                if (fetchedCategories[i]['name'] == categoryName.value) {
                    console.log('La catégorie: ' + categoryName.value + ' existe déjà')
                    errorMessage.value = 'La catégorie: ' + categoryName.value + ' existe déjà'
                    return;
                }
            }

            // Create the category
            emits('addCategory', { name: categoryName.value, description: categoryDescription.value });
            categoryDescription.value = '';
            categoryName.value = '';

        } catch (error) {
            emits('addCategory', { error: 'Erreur vérification catégories existantes', description: error });
            categoryDescription.value = '';
            categoryName.value = '';
            return;
        }
    }
}

function handleKeyDown(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
    else if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        addCategory();
    } else if (event.key === 'Tab' && props.isOpen) {
        event.preventDefault();

        if (categoryName.value == '' && document.activeElement.id != 'categoryName') {
            document.getElementById('categoryName').focus();
        } else if (categoryDescription.value == '' && document.activeElement.id != 'categoryDescription') {
            document.getElementById('categoryDescription').focus();
        } else if (document.activeElement.id === 'categoryName') {
            document.getElementById('categoryDescription').focus();
        } else {
            document.getElementById('categoryName').focus();
        }
    }
}
</script>