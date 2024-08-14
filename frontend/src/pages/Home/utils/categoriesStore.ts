import { ref } from 'vue';
import { getData, postData } from '@/global/fetchData';
import { Category } from '@/global/types';

const categories = ref<Category[]>([]);
const categoryTotals = ref<{ [key: string]: number }>({});
const isLoading = ref(true);

fetchCategoriesAndTotals();

async function fetchCategoriesAndTotals() {
  try {
    const categoriesResponse = await getData('user/categories');
    categories.value = categoriesResponse.data;

    const totalsPromises = categories.value.map(category => 
      postData('user/emails/', { subject: "", category: category.name, advanced: true })
    );
    const totalsResponses = await Promise.all(totalsPromises);

    categories.value.forEach((category, index) => {
      categoryTotals.value[category.name] = totalsResponses[index].data.count;
    });
  } catch (error) {
    console.error('Error fetching categories and totals:', error);
  } finally {
    isLoading.value = false;
  }
}

export { categories, categoryTotals, isLoading };
