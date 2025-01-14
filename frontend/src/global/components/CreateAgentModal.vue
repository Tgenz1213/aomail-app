<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">{{ $t('newPage.createAgent.title') }}</h2>
        <button
          type="button"
          @click="$emit('close')"
          class="text-gray-500 hover:text-gray-700"
        >
          <XMarkIcon class="h-6 w-6" aria-hidden="true" />
        </button>
      </div>
      <form @submit.prevent="createAgent">
        <div class="mb-4">
          <div class="flex items-end space-x-4">
            <div class="flex-shrink-0">
              <div class="relative h-[4rem] w-[4rem]">
                <img
                  :src="previewImage || '/assets/default-agent.png'"
                  class="h-[4rem] w-[4rem] rounded-lg object-cover"
                  alt="Agent icon"
                />
                <label class="absolute inset-0 flex items-center justify-center cursor-pointer bg-black bg-opacity-50 rounded-lg opacity-0 hover:opacity-100 transition-opacity">
                  <input
                    type="file"
                    accept="image/*"
                    class="hidden"
                    @change="handleImageUpload"
                  />
                  <span class="text-white text-xs">{{ $t('newPage.createAgent.upload') }}</span>
                </label>
              </div>
            </div>
            <div class="flex-grow">
              <label class="block text-sm font-medium text-gray-700">{{ $t('newPage.createAgent.agentName') }}</label>
              <p v-if="showNameError" class="text-red-500 text-xs mt-1">
                {{ $t('newPage.createAgent.agentNameError') }}
              </p>
              <input
                type="text"
                v-model="agentName"
                required
                @input="showNameError = false"
                class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:border-gray-900 focus:ring-gray-900 focus:outline-none"
                :placeholder="$t('newPage.createAgent.agentNamePlaceholder')"
              />
            </div>
          </div>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">{{ $t('newPage.createAgent.behaviorDescription') }}</label>
          <textarea
            v-model="behaviorDescription"
            class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:border-gray-900 focus:ring-gray-900 focus:outline-none"
            :placeholder="$t('newPage.createAgent.behaviorPlaceholder')"
          ></textarea>
        </div>

        <div class="mb-4">
          <button
            type="button"
            @click="showEmailExample = !showEmailExample"
            class="text-sm text-gray-500 hover:text-gray-700 flex items-center"
          >
            <PlusIcon v-if="!showEmailExample" class="h-4 w-4 mr-1" />
            <MinusIcon v-else class="h-4 w-4 mr-1" />
            {{ $t('newPage.createAgent.emailExample') }}
          </button>
          
          <transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
          >
            <textarea
              v-if="showEmailExample"
              v-model="emailExample"
              rows="6"
              class="mt-2 block w-full border border-gray-300 rounded-md p-2 focus:border-gray-900 focus:ring-gray-900 focus:outline-none min-h-[150px]"
              :placeholder="$t('newPage.createAgent.emailExamplePlaceholder')"
            ></textarea>
          </transition>
        </div>

        <div class="flex space-x-4 mb-4">
          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-700">{{ $t('newPage.createAgent.length') }}</label>
            <Listbox v-model="length">
              <div class="relative mt-1">
                <ListboxButton class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6">
                  <span class="block truncate">{{ length.charAt(0).toUpperCase() + length.slice(1) }}</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </span>
                </ListboxButton>

                <transition
                  leave-active-class="transition ease-in duration-100"
                  leave-from-class="opacity-100"
                  leave-to-class="opacity-0"
                >
                  <ListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption v-for="option in ['very short', 'short', 'medium']" :key="option" :value="option" v-slot="{ active, selected }">
                      <li :class="[active ? 'bg-gray-800 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                        <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                          {{ option.charAt(0).toUpperCase() + option.slice(1) }}
                        </span>
                        <span v-if="selected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                          <CheckIcon class="h-5 w-5" aria-hidden="true" />
                        </span>
                      </li>
                    </ListboxOption>
                  </ListboxOptions>
                </transition>
              </div>
            </Listbox>
          </div>

          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-700">{{ $t('newPage.createAgent.formality') }}</label>
            <Listbox v-model="formality">
              <div class="relative mt-1">
                <ListboxButton class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-800 sm:text-sm sm:leading-6">
                  <span class="block truncate">{{ formality.charAt(0).toUpperCase() + formality.slice(1) }}</span>
                  <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                  </span>
                </ListboxButton>

                <transition
                  leave-active-class="transition ease-in duration-100"
                  leave-from-class="opacity-100"
                  leave-to-class="opacity-0"
                >
                  <ListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    <ListboxOption v-for="option in ['informal', 'formal', 'very formal']" :key="option" :value="option" v-slot="{ active, selected }">
                      <li :class="[active ? 'bg-gray-800 text-white' : 'text-gray-900', 'relative cursor-default select-none py-2 pl-3 pr-9']">
                        <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                          {{ option.charAt(0).toUpperCase() + option.slice(1) }}
                        </span>
                        <span v-if="selected" :class="[active ? 'text-white' : 'text-gray-500', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                          <CheckIcon class="h-5 w-5" aria-hidden="true" />
                        </span>
                      </li>
                    </ListboxOption>
                  </ListboxOptions>
                </transition>
              </div>
            </Listbox>
          </div>
        </div>

        <div class="flex justify-end space-x-2">
          <button
            type="button"
            @click="$emit('close')"
            class="inline-flex w-full rounded-md bg-gray-300 px-3 py-2 text-sm font-semibold text-gray-700 shadow-sm hover:bg-gray-400 sm:w-auto"
          >
            {{ $t('newPage.createAgent.cancel') }}
          </button>
          <button
            type="submit"
            class="inline-flex w-full rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:w-auto"
          >
            {{ $t('newPage.createAgent.create') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { postData } from "@/global/fetchData";
import { Agent } from "@/global/types";
import { XMarkIcon } from "@heroicons/vue/20/solid";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'
import { ChevronUpDownIcon, CheckIcon, PlusIcon, MinusIcon } from '@heroicons/vue/20/solid'
import { i18n } from "@/global/preferences";

const emit = defineEmits(['created', 'close']);

const agentName = ref("");
const behaviorDescription = ref("");
const length = ref("short");
const formality = ref("formal");
const showEmailExample = ref(false);
const emailExample = ref("");
const previewImage = ref("");
const selectedFile = ref<File | null>(null);
const showNameError = ref(false);

const handleImageUpload = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    selectedFile.value = input.files[0];
    previewImage.value = URL.createObjectURL(input.files[0]);
  }
};

const createAgent = async () => {
  if (!agentName.value.trim()) {
    showNameError.value = true;
    return;
  }
  
  const formData = new FormData();
  formData.append("agent_name", agentName.value);
  formData.append("agent_ai_model", "gemini");
  formData.append("ai_template", behaviorDescription.value);
  formData.append("email_example", emailExample.value);
  formData.append("length", length.value);
  formData.append("formality", formality.value);
  formData.append("language", i18n.global.locale);
  if (selectedFile.value) {
    formData.append("picture", selectedFile.value);
  }

  const result = await postData("user/agents/create/", formData, true);

  if (result.success) {
    const newAgent: Agent = {
      ...result.data,
      pictureUrl: result.data.picture || "/assets/default-agent.png",
    };
    emit("created", newAgent);
    emit("close");
  } else {
    alert(result.error || "Failed to create agent.");
  }
};
</script>