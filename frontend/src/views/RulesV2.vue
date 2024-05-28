<template>
  <!--
    <div class="pb-1 lg:pl-20 bg-gray-100">
        <div class="grid grid-cols-8 gap-6 h-72 items-center divide-x-8 divide-indigo-900 bg-blue-400">
            <div class="col-span-3 h-full bg-red-500">
                    
                    <div class="flex">
                        <div class="flex-shrink-0 self-center">
                            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-indigo-800">
                                <span class="text-lg font-medium leading-none text-white">AO</span>
                            </span>
                        </div>
                        <div>
                            <p class="mt-1" id="animated-text" ref="animatedText"></p>
                        </div>
                    </div>
                </div>
            <div class="col-span-5 h-full bg-red-500">
                <p>Test</p>
            </div>
        </div>
    </div>-->
  <div class="flex flex-col justify-center items-center h-screen">
    <div class="flex h-full w-full">
      <div class="w-[90px] bg-white ring-1 shadow-sm ring-black ring-opacity-5">
        <navbar></navbar>
      </div>
      <div class="flex-1 bg-white ring-1 shadow-sm ring-black ring-opacity-5">
        <!-- OLD VALUE w : 1400px or 1424px h : 825px -->
        <div class="flex flex-col h-full relative"> <!-- ADDED relative -->
          <div class="divide-y divide-gray-200">
            <div
              class="flex items-center justify-center h-[70px] 2xl:h-[80px] lg:ring-1 lg:ring-black lg:ring-opacity-5 rounded-t-xl bg-gray-50">
              <!-- bg-gray-200 bg-opacity-50 bg-gray-400 bg-opacity-10-->
              <h1 style="font-family: 'Poppins', sans-serif; font-weight: 500;">{{ $t('Rules_vue.assistant_rules') }}</h1>
            </div>
            <SearchbarV2 @input="updateSearchQuery"></SearchbarV2>
          </div>
          <div v-if="rules.length > 0" class="flex-grow overflow-y-auto"
            style="margin-right: 2px; margin-bottom: 120px;">
            <div class="p-6">
              <!-- IF AT LEAST ONE RULE EXIST -->
              <ul v-if="filteredRules.length > 0" category="list"
                class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
                <li v-for="rule in filteredRules" :key="rule.email"
                  class="col-span-1 rounded-lg bg-white border-2 border-gray-100 hover:border-3 hover:border-gray-800 hover:shadow-sm relative">
                  <div class="absolute right-4 top-4">
                    <PencilSquareIcon @click="editRule(rule)"
                      class="w-6 h-6 text-gray-300 hover:text-gray-800 cursor-pointer" />
                  </div>
                  <div class="flex w-full items-center justify-between space-x-6 p-6">
                    <div class="flex-1 truncate">
                      <div class="flex items-center space-x-3">
                        <h3 class="truncate text-sm font-medium text-gray-900">{{ rule.name }}</h3>
                      </div>
                      <p class="mt-1 mb-4 truncate text-sm text-gray-500">{{ rule.email }}</p>
                      <div v-if="rule.category" class="flex gap-1">
                        <div class="flex space-x-1 items-center">
                          <ArchiveBoxIcon class="w-4 h-4" />
                          <p class="font-semibold text-sm">{{ $t('Rules_vue.catégorie') }}</p>
                        </div>
                        <span
                          class="inline-flex flex-shrink-0 items-center rounded-full bg-gray-50 px-1.5 py-0.5 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/20">{{
                          rule.category }}</span>
                      </div>
                      <div v-if="rule.priority !== ''" class="flex gap-1 mt-2">
                        <div class="flex space-x-1 items-center">
                          <ExclamationCircleIcon class="w-4 h-4" />
                          <p class="font-semibold text-sm">{{ $t('Rules_vue.priotity') }}</p>
                        </div>
                        <span v-if="rule.priority === 'Important'"
                          class="inline-flex flex-shrink-0 items-center rounded-full bg-red-50 px-1.5 py-0.5 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/20">{{
                          rule.priority }}</span>
                        <span v-if="rule.priority === 'Informatif'"
                          class="inline-flex flex-shrink-0 items-center rounded-full bg-blue-50 px-1.5 py-0.5 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-600/20">{{
                          rule.priority }}</span>
                        <span v-if="rule.priority === 'Inutile'"
                          class="inline-flex flex-shrink-0 items-center rounded-full bg-gray-50 px-1.5 py-0.5 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-600/20">{{
                          rule.priority }}</span>
                      </div>
                      <div v-if="rule.mail_stop === true" class="flex gap-1 mt-2">
                        <div class="flex space-x-1 items-center">
                          <ShieldCheckIcon class="w-4 h-4" />
                          <p class="font-semibold text-sm">{{ $t('Rules_vue.blocked_mail') }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
          <div v-if="rules.length == 0" class="flex p-4 w-full h-full">
            <div
              class="cursor-pointer flex items-center justify-center w-full h-full rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 text-center"
              @click="showModal = true">
              <div class="flex-col">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                  stroke="currentColor" class="w-12 h-12 mx-auto text-gray-400">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
                </svg>
                <span class="mt-2 block text-sm font-semibold text-gray-900">{{ $t('Rules_vue.rules') }}</span>
              </div>
            </div>
          </div>
          <div v-if="rules.length > 0"
            class="cursor-pointer flex items-center justify-center w-auto right-6 left-6 absolute bottom-5 h-[85px] rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 text-center"
            @click="showModal = true">
            <div class="flex-col">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1"
                stroke="currentColor" class="w-10 h-10 mx-auto text-gray-400">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
              </svg>
              <span class="mt-2 block text-sm font-semibold text-gray-900">{{ $t('Rules_vue.assistant_rules') }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <ModalSeeRule :isOpen="showModal" @update:isOpen="updateModalStatus" :emailSenders="emailSenders"
    :categories="categories" :sender="senderSelected" @fetch-rules="fetchRules" />
  <UpdateRule :isOpen="showUpdateModal" :rule="ruleSelected" :categories="categories" :emailSenders="emailSenders"
    @update:isOpen="updateModalUpdateStatus" @fetch-rules="fetchRules" />
</template>

<script>
import Navbar from '../components/AppNavbar7.vue';
import Navbar2 from '../components/AppNavbar8.vue';
import SearchbarV2 from '../components/SearchbarV2.vue'
import ModalSeeRule from '../components/SeeRule.vue';
import UpdateRule from '../components/UpdateRule.vue';
import { fetchWithToken } from '../router/index.js';
import { API_BASE_URL } from '@/main';
import {
  ArchiveBoxIcon,
  ExclamationCircleIcon,
  ShieldCheckIcon,
  PencilSquareIcon
} from '@heroicons/vue/24/outline'

export default {
  components: {
    Navbar,
    Navbar2,
    SearchbarV2,
    ArchiveBoxIcon,
    ExclamationCircleIcon,
    ShieldCheckIcon,
    PencilSquareIcon,
    ModalSeeRule,
    UpdateRule
  },
  methods: {
    handleKeyDown(event) {
      if (event.ctrlKey && event.key === 'k') {
        document.getElementById('search-field').focus();
        event.preventDefault();
      }
    },
    updateSearchQuery(event) {
      this.searchQuery = event.target.value;
    },
    updateModalStatus(status) {
      console.log("STATUS", status);
      this.showModal = status;
    },
    updateModalUpdateStatus(status) {
      this.showUpdateModal = status;
    },
    editRule(rule) {
      this.ruleSelected = rule;
      console.log("Rule Selected", this.ruleSelected);
      this.showUpdateModal = true;
    },
    async fetchRules() {
      try {
        const url = `${API_BASE_URL}user/rules/`;

        const rulesData = await fetchWithToken(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        console.log('Rules', rulesData);
        //console.log('Rules name', rulesData[0].category_name);

        this.rules = rulesData.map(rule => ({
          id: rule.id,
          name: rule.sender_name,
          email: rule.sender_email,
          category: rule.category_name,
          priority: rule.priority,
          mail_stop: rule.block
        }));

      } catch (error) {
        console.error('Error fetching rules:', error);
      }
    },
    async fetchRuleById(id_rule) {
      try {
        const url = `${API_BASE_URL}user/rules/${id_rule}/`;

        const ruleData = await fetchWithToken(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        console.log('Rule', ruleData);

        // Assuming you want to set this rule to a property of the class
        this.ruleSelected = {
          id: ruleData.id,
          name: ruleData.sender_name,
          email: ruleData.sender_email,
          category: ruleData.category_name,
          priority: ruleData.priority,
          mail_stop: ruleData.block
        };

      } catch (error) {
        console.error('Error fetching rule:', error);
      }
    },
    async fetchCategories() {
      try {
        const url = `${API_BASE_URL}user/categories/`;

        const data = await fetchWithToken(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        console.log("Categories", data);
        this.categories = data;
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    async fetchEmailSenders() {
      try {
        // Define the URL
        const url = `${API_BASE_URL}user/contacts/`;

        const data = await fetchWithToken(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        console.log("email senders=====>", data);
        this.emailSenders = data;
      } catch (error) {
        console.error('Error fetching email senders:', error);
        // Handle errors appropriately
      }
    }
  },
  mounted() {
    document.addEventListener("keydown", this.handleKeyDown);
    this.bgColor = localStorage.getItem('bgColor');
    this.fetchRules();
    this.fetchEmailSenders();
    this.fetchCategories();

    const urlParams = new URLSearchParams(window.location.search);
    const editRule = urlParams.get('edit_rule');
    const ruleId = urlParams.get('id_rule');
    const name_sender = urlParams.get('rule_name');
    const email_sender = urlParams.get('rule_email');

    // Check if edit_rule is true and rule_id is present
    if (editRule === 'true' && ruleId) {
      // Fetch the rule by ID and then show the update modal
      this.fetchRuleById(ruleId).then(() => {
        this.updateModalUpdateStatus(true);
        // Remove query parameters from URL
        const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
        window.history.replaceState({}, document.title, newUrl);
      }).catch(error => {
        console.error('Error in fetching rule by ID:', error);
      });
    } else if (editRule === 'false' && name_sender && email_sender) {
      this.senderSelected = { username: name_sender, email: email_sender };
      console.log("DEBUG New Rule Auto -------------------->", this.senderSelected);
      this.updateModalStatus(true);
      // Remove query parameters from URL
      const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
      window.history.replaceState({}, document.title, newUrl);
    }
  },
  computed: {
    filteredRules() {
      //console.log("DEBUG =>", this.searchQuery);
      if (this.searchQuery == '') return this.rules;
      return this.rules.filter(rule =>
        rule.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        rule.email.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        (rule.category && rule.category.toLowerCase().includes(this.searchQuery.toLowerCase()))
        // add any other properties you want to include in the search
      );
    },
  },
  data() {
    return {
      showModal: false,
      showUpdateModal: false,
      bgColor: '',
      rules: [], // This will hold the fetched rules
      categories: [],
      emailSenders: [],
      senderSelected: {},
      selectedCategory: '',
      selectedEmailSender: {},
      ruleSelected: null,
      searchQuery: '',
      people: [],
    }
  }
}
</script>