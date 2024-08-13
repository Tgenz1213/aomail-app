<template>
  <div class="flex flex-col justify-center items-center h-screen">
    <div class="flex h-full w-full">
      <div class="w-[90px] 2xl:w-[100px] bg-white ring-1 shadow-sm ring-black ring-opacity-5">
        <NavBarSmall />
      </div>
      <div class="flex-1 bg-white ring-1 shadow-sm ring-black ring-opacity-5">
        <div class="flex flex-col h-full relative">
          <!--<SearchBar @input="updateSearchQuery" />-->
          <ImportantEmail 
            :emails="importantEmails" 
          />
          <InformativeEmail 
            :emails="informativeEmails" 
          />
          <UselessEmail 
            :emails="uselessEmails" 
          />
          <RedEmail 
            :emails="redEmails" 
          />
        </div>
      </div>
      <AssistantChat v-if="!isHidden" @toggle-visibility="toggleVisibility" />
    </div>
    <NewCategoryModal
      :is-open="isModalOpen"
      @close-modal="closeModal"
    />
    <UpdateCategoryModal
      :is-open="isModalUpdateOpen"
      :category="categoryToUpdate"
      @close-modal="closeUpdateModal"
      @update-category="handleUpdateCategory"
      @delete-category="handleCategoryDelete"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getData, postData, deleteData } from '@/global/fetchData';
import { Email, Category } from '@/global/types';
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import NewCategoryModal from "./components/NewCategoryModal.vue";
import UpdateCategoryModal from "./components/UpdateCategoryModal.vue";
import ImportantEmail from "./components/ImportantEmails.vue";
import InformativeEmail from "./components/InformativeEmails.vue";
import UselessEmail from "./components/UselessEmails.vue";
import RedEmail from "./components/RedEmails.vue";
import AssistantChat from "./components/AssistantChat.vue";

const emails = ref<Email[]>([]);
const categories = ref<Category[]>([]);
const isModalOpen = ref(false);
const isModalUpdateOpen = ref(false);
const categoryToUpdate = ref<Category | null>(null);
const isHidden = ref(false);

const importantEmails = computed(() => emails.value.filter(email => email.priority === 'important'));
const informativeEmails = computed(() => emails.value.filter(email => email.priority === 'informative'));
const uselessEmails = computed(() => emails.value.filter(email => email.priority === 'useless'));
const redEmails = computed(() => emails.value.filter(email => email.flags.scam || email.flags.spam));

const fetchEmails = async () => {
  try {
    const response = await getData('user/emails');
    emails.value = response.data;
  } catch (error) {
    console.error('Error fetching emails:', error);
  }
};

const markEmailAsRead = async (emailId: number) => {
  try {
    await postData(`user/emails/${emailId}/mark_read`, {});
    const emailIndex = emails.value.findIndex(email => email.id === emailId);
    if (emailIndex !== -1) {
      emails.value[emailIndex].read = true;
    }
  } catch (error) {
    console.error('Error marking email as read:', error);
  }
};

const openEmail = (email: Email) => {
  // Implement email opening logic
};

const openAnswer = (email: Email) => {
  // Implement answer opening logic
  console.log('Opening answer for email:', email);
};

const markEmailReplyLater = async (email: Email) => {
  try {
    await postData(`user/emails/${email.id}/mark_reply_later`, {});
    // Update local state
    const emailIndex = emails.value.findIndex(e => e.id === email.id);
    if (emailIndex !== -1) {
      emails.value[emailIndex].answer = true;
    }
  } catch (error) {
    console.error('Error marking email for reply later:', error);
  }
};

const transferEmail = (email: Email) => {
  // Implement email transfer logic
  console.log('Transferring email:', email);
};

const updateSearchQuery = (query: string) => {
  // Implement search logic
};

const toggleVisibility = () => {
  isHidden.value = !isHidden.value;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const closeUpdateModal = () => {
  isModalUpdateOpen.value = false;
};

const handleAddCategory = async (category: Category) => {
  try {
    await postData('user/categories', category);
    await fetchCategories();
  } catch (error) {
    console.error('Error adding category:', error);
  }
};

const handleUpdateCategory = async (category: Category) => {
  try {
    await postData(`user/categories/${category.name}`, category);
    await fetchCategories();
  } catch (error) {
    console.error('Error updating category:', error);
  }
};

const handleCategoryDelete = async (categoryName: string) => {
  try {
    await deleteData(`user/categories/${categoryName}`);
    await fetchCategories();
  } catch (error) {
    console.error('Error deleting category:', error);
  }
};

const fetchCategories = async () => {
  try {
    const response = await getData('user/categories');
    categories.value = response.data;
  } catch (error) {
    console.error('Error fetching categories:', error);
  }
};

onMounted(async () => {
  await fetchEmails();
  await fetchCategories();
});
</script>
