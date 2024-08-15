<template>
  <NotificationTimer
    :showNotification="showNotification"
    :notificationTitle="notificationTitle"
    :notificationMessage="notificationMessage"
    :backgroundColor="backgroundColor"
    @dismissPopup="dismissPopup"
    />
  <div class="flex flex-col justify-center items-center h-screen">
    <div class="flex h-full w-full">
      <div class="w-[90px] 2xl:w-[100px] bg-white ring-1 shadow-sm ring-black ring-opacity-5">
        <NavBarSmall />
      </div>
      <div class="flex-1 bg-white ring-1 shadow-sm ring-black ring-opacity-5">
        <div class="flex flex-col h-full relative">
          <Categories 
            :selected-category="selectedCategory"
            :category-totals="categoryTotals"
            @select-category="selectCategory"
            @open-new-category-modal="openNewCategoryModal"
            @open-update-category-modal="openUpdateCategoryModal"
          />
          <!--<SearchBar @input="updateSearchQuery" />-->
          <div v-if="categoryTotals[selectedCategory] === 0" class="flex-1">
            <div class="flex flex-col w-full h-full rounded-xl">
              <div class="flex flex-col justify-center items-center h-full m-5 rounded-lg border-2 border-dashed border-gray-400 p-12 text-center hover:border-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                    stroke-width="1" stroke="currentColor" class="mx-auto h-14 w-14 text-gray-400">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                </svg>
                <span class="mt-2 block text-md font-semibold text-gray-900">{{ $t('homePage.noNewEmail') }}</span>
              </div>
            </div>
          </div>
          <div v-else class="flex-1 overflow-y-auto custom-scrollbar">
            <ImportantEmail 
              :emails="importantEmails" 
              @markRead="markEmailAsRead"
              @markReplyLater="markEmailReplyLater"
            />
            <InformativeEmail 
              :emails="informativeEmails"
              @markRead="markEmailAsRead"
              @markReplyLater="markEmailReplyLater" 
            />
            <UselessEmail 
              :emails="uselessEmails" 
            />
            <RedEmail 
              :emails="redEmails" 
            />
          </div>
        </div>
      </div>
      <AssistantChat v-if="!isHidden" @toggle-visibility="toggleVisibility" />
    </div>
    <NewCategoryModal
      :isOpen="isModalNewCategoryOpen"
      @close="closeNewCategoryModal"
    />
    <UpdateCategoryModal
      :isOpen="isModalUpdateCategoryOpen"
      :category="categoryToUpdate"
      @close="closeUpdateCategoryModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, provide, onMounted } from 'vue';
import { getData, postData } from '@/global/fetchData';
import { Email, Category } from '@/global/types';
import { displayErrorPopup, displaySuccessPopup } from "@/global/popUp";
import NotificationTimer from "@/global/components/NotificationTimer.vue";
import NavBarSmall from "@/global/components/NavBarSmall.vue";
import NewCategoryModal from "./components/NewCategoryModal.vue";
import UpdateCategoryModal from "./components/UpdateCategoryModal.vue";
import ImportantEmail from "@/global/components/ImportantEmails.vue";
import InformativeEmail from "@/global/components/InformativeEmails.vue";
import UselessEmail from "@/global/components/UselessEmails.vue";
import RedEmail from "./components/RedEmails.vue";
import AssistantChat from "./components/AssistantChat.vue";
import Categories from './components/Categories.vue';

const showNotification = ref(false);
const notificationTitle = ref("");
const notificationMessage = ref("");
const backgroundColor = ref("");
const timerId = ref<number | null>(null);

const emails = ref<{ [key: string]: { [key: string]: Email[] } }>({});
const selectedCategory = ref<string>('');
const categoryToUpdate = ref<Category | null>(null);
const isModalNewCategoryOpen = ref(false);
const isModalUpdateCategoryOpen = ref(false);
const isHidden = ref(false);
const categories = ref<Category[]>([]);
const categoryTotals = ref<{ [key: string]: number }>({});

const fetchEmailsData = async (categoryName: string) => {
  try {
    const response = await postData('user/emails/', { subject: "", category:categoryName, advanced:true });
    const emails_details = await postData('user/get_emails_data/', {ids:response.data.ids});
    emails.value = emails_details.data.data;
    console.log("CHECK EMAILS", emails.value);
  } catch (error) {
    console.error('Error fetching emails:', error);
  }
};

async function fetchCategoriesAndTotals() {
  const categoriesResponse = await getData('user/categories');
  categories.value = categoriesResponse.data;

  const totalsPromises = categories.value.map(category => 
    postData('user/emails/', { subject: "", category: category.name, read:false, advanced: true })
  );
  const totalsResponses = await Promise.all(totalsPromises);

  categories.value.forEach((category, index) => {
    categoryTotals.value[category.name] = totalsResponses[index].data.count;
  });
}

provide("displayPopup", displayPopup);
provide("fetchEmailsData", fetchEmailsData);
provide("fetchCategoriesAndTotals", fetchCategoriesAndTotals);
provide("categories", categories);
provide("selectedCategory", selectedCategory);

const addCategoryToEmails = (emailList: Email[], category: string): Email[] => {
  return emailList.map(email => ({
    ...email,
    category: category
  }));
};

const importantEmails = computed(() => {
  if (!emails.value || !selectedCategory.value) return [];
  const categoryEmails = emails.value[selectedCategory.value]?.important || [];
  const unreadEmails = categoryEmails.filter(email => !email.read);
  return addCategoryToEmails(unreadEmails, selectedCategory.value);
});

const informativeEmails = computed(() => {
  if (!emails.value || !selectedCategory.value) return [];
  const categoryEmails = emails.value[selectedCategory.value]?.informative || [];
  const unreadEmails = categoryEmails.filter(email => !email.read);
  return addCategoryToEmails(unreadEmails, selectedCategory.value);
});

const uselessEmails = computed(() => {
  if (!emails.value || !selectedCategory.value) return [];
  const categoryEmails = emails.value[selectedCategory.value]?.useless || [];
  const unreadEmails = categoryEmails.filter(email => !email.read);
  return addCategoryToEmails(unreadEmails, selectedCategory.value);
});

const redEmails = computed(() => {
  if (!emails.value || !selectedCategory.value) return [];
  const categoryEmails = [
    ...(emails.value[selectedCategory.value]?.important || []),
    ...(emails.value[selectedCategory.value]?.informative || []),
    ...(emails.value[selectedCategory.value]?.useless || [])
  ];
  const filteredEmails = categoryEmails.filter(email => email.flags.scam || email.flags.spam);
  return addCategoryToEmails(filteredEmails, selectedCategory.value);
});

const markEmailAsRead = async (email: Email) => {
  try {
    await postData(`user/emails/${email.id}/mark_read/`, {});

    const categoryEmails = emails.value[selectedCategory.value];
    if (categoryEmails) {
      ['important', 'informative', 'useless'].forEach((type) => {
        if (categoryEmails[type]) {
          const emailIndex = categoryEmails[type].findIndex(e => e.id === email.id);
          if (emailIndex !== -1) {
            categoryEmails[type][emailIndex].read = true;
            categoryTotals.value[selectedCategory.value] -= 1;
          }
        }
      });
    }
  } catch (error) {
    console.error('Error marking email as read:', error);
  }
};

const markEmailReplyLater = async (email: Email) => {
  try {
    await postData(`user/emails/${email.id}/mark_read/`, {});
    await postData(`user/emails/${email.id}/mark_reply_later`, {});

    const categoryEmails = emails.value[selectedCategory.value];
    if (categoryEmails) {
      ['important', 'informative', 'useless'].forEach((type) => {
        if (categoryEmails[type]) {
          const emailIndex = categoryEmails[type].findIndex(e => e.id === email.id);
          if (emailIndex !== -1) {
            categoryEmails[type][emailIndex].read = true;
            categoryEmails[type][emailIndex].answerLater = true; 
            categoryTotals.value[selectedCategory.value] -= 1;
          }
        }
      });
    }
  } catch (error) {
    console.error('Error marking email for reply later:', error);
  }
};

const toggleVisibility = () => {
  isHidden.value = !isHidden.value;
};

const selectCategory = (category: Category) => {
  selectedCategory.value = category.name;
  fetchEmailsData(selectedCategory.value);
  localStorage.setItem('selectedCategory', category.name);
};

const openNewCategoryModal = () => {
  isModalNewCategoryOpen.value = true;
};

const closeNewCategoryModal = () => {
  isModalNewCategoryOpen.value = false;
};

const openUpdateCategoryModal = (category: Category) => {
  categoryToUpdate.value = category;
  isModalUpdateCategoryOpen.value = true;
};

const closeUpdateCategoryModal = () => {
  isModalUpdateCategoryOpen.value = false;
  categoryToUpdate.value = null;
};

function displayPopup(type: "success" | "error", title: string, message: string) {
    if (type === "error") {
        displayErrorPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    } else {
        displaySuccessPopup(showNotification, notificationTitle, notificationMessage, backgroundColor, title, message);
    }
    timerId.value = setTimeout(dismissPopup, 4000);
}

function dismissPopup() {
    showNotification.value = false;
    if (timerId.value !== null) {
        clearTimeout(timerId.value);
    }
}

onMounted(async () => {
  fetchCategoriesAndTotals();
  const storedTopic = localStorage.getItem('selectedCategory');
  if (storedTopic) {
    selectedCategory.value = storedTopic;
  } else {
    selectedCategory.value = 'Others';
  }
  fetchEmailsData(selectedCategory.value);
});
</script>
