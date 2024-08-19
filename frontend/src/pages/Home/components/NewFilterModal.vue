<template>
<div class="absolute left-0 right-0 mt-1 bg-white border border-gray-300 shadow-lg rounded-md z-50" style="width: 90%;">
    <div class="p-4">
      <div class="grid grid-cols-3 gap-4 text-sm">
        <div v-for="(field, index) in filterFields" :key="index" class="flex flex-col">
          <label :for="field.name" class="mb-1 text-sm font-medium text-gray-700">{{ field.label }}</label>
          <input v-if="field.type === 'text'" :type="field.type" :placeholder="field.placeholder" :id="field.name" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
          <div v-if="field.type === 'checkbox'" class="flex items-center">
            <input :type="field.type" :id="field.name" class="form-checkbox h-4 w-4 text-indigo-600 mr-2">
            <span class="text-sm text-gray-700">{{ field.label }}</span>
          </div>
          <select v-if="field.type === 'select'" :id="field.name" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
            <option v-for="option in field.options" :key="option.value" :value="option.value">{{ option.label }}</option>
          </select>
        </div>
      </div>
      <div class="mt-4 flex justify-end space-x-3 text-sm">
        <button @click="toggleFilterPopup" class="px-3 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500">
          Annuler
        </button>
        <button @click="applyFilters" class="px-3 py-2 bg-gray-800 text-white rounded-md hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
          Rechercher
        </button>
      </div>
    </div>
</div>
</template>
<script setup lang="ts">
// IN DEV ==================================================================================>
import { ref } from 'vue';

const filterFields=[
    { name: 'from', label: 'De', type: 'text', placeholder: 'De' },
    { name: 'to', label: 'À', type: 'text', placeholder: 'À' },
    { name: 'subject', label: 'Objet', type: 'text', placeholder: 'Objet' },
    { name: 'contains', label: 'Contient les mots', type: 'text', placeholder: 'Contient les mots' },
    { name: 'doesNotContain', label: 'Ne contient pas', type: 'text', placeholder: 'Ne contient pas' },
    { name: 'size', label: 'Taille', type: 'select', options: [{ value: 'greater', label: 'supérieure à' }, { value: 'less', label: 'inférieure à' }] },
    { name: 'dateRange', label: 'Plage de dates', type: 'select', options: [{ value: '1day', label: '1 jour' }, { value: '1week', label: '1 semaine' }, { value: '1month', label: '1 mois' }, { value: '1year', label: '1 an' }] },
    { name: 'searchIn', label: 'Rechercher', type: 'select', options: [{ value: 'all', label: 'Tous les messages' }, { value: 'read', label: 'Messages lus' }, { value: 'unread', label: 'Messages non lus' }] },
    { name: 'hasAttachment', label: 'Contenant une pièce jointe', type: 'checkbox' },
    { name: 'excludeChats', label: 'Ne pas inclure les chats', type: 'checkbox' }
]

const showFilterPopup = ref(false);

const toggleFilterPopup = () => {
  showFilterPopup.value = !showFilterPopup.value;
};

const applyFilters = () => {
  // Logique pour appliquer les filtres
  showFilterPopup.value = false;
};

</script>