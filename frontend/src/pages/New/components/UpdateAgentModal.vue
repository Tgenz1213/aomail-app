<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Update Agent</h2>
        <button
          type="button"
          @click="$emit('close')"
          class="text-gray-500 hover:text-gray-700"
        >
          <XMarkIcon class="h-6 w-6" aria-hidden="true" />
        </button>
      </div>

      <form @submit.prevent="updateAgent">
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
                  <span class="text-white text-xs">Upload</span>
                </label>
              </div>
            </div>
            <div class="flex-grow">
              <label class="block text-sm font-medium text-gray-700">Agent Name</label>
              <input
                type="text"
                v-model="agentName"
                required
                class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:border-gray-900 focus:ring-gray-900 focus:outline-none"
                placeholder="Enter agent name"
              />
            </div>
          </div>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Behavior Description (Optional)</label>
          <textarea
            v-model="behaviorDescription"
            class="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:border-gray-900 focus:ring-gray-900 focus:outline-none"
            placeholder="Describe agent behavior"
          ></textarea>
        </div>

        <div class="flex space-x-4 mb-4">
          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-700">Length</label>
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
            <label class="block text-sm font-medium text-gray-700">Formality</label>
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

        <div class="flex justify-between items-center">
          <button
            type="button"
            @click="deleteAgent"
            class="inline-flex rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700"
          >
            Delete
          </button>
          <div class="flex space-x-2">
            <button
              type="button"
              @click="$emit('close')"
              class="inline-flex rounded-md bg-gray-300 px-3 py-2 text-sm font-semibold text-gray-700 shadow-sm hover:bg-gray-400"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="inline-flex rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black"
            >
              Update
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue';
import { ChevronUpDownIcon, CheckIcon, XMarkIcon } from '@heroicons/vue/20/solid';
import { putData, deleteData } from "@/global/fetchData";
import { Agent } from "@/global/types";

const emit = defineEmits(['updated', 'deleted', 'close']);

const props = defineProps({
  agent: {
    type: Object as () => Agent,
    required: true,
  },
});

const agentName = ref(props.agent.agent_name);
const behaviorDescription = ref(props.agent.ai_template || "");
const length = ref(props.agent.length);
const formality = ref(props.agent.formality);
const previewImage = ref(props.agent.picture || "");
const selectedFile = ref<File | null>(null);

watch(
  () => props.agent,
  (newAgent) => {
    agentName.value = newAgent.agent_name;
    behaviorDescription.value = newAgent.ai_template || "";
    length.value = newAgent.length;
    formality.value = newAgent.formality;
  }
);

const updateAgent = async () => {
  const formData = new FormData();
  formData.append("agent_name", agentName.value);
  formData.append("ai_template", behaviorDescription.value);
  formData.append("length", length.value);
  formData.append("formality", formality.value);
  if (selectedFile.value) {
    formData.append("picture", selectedFile.value);
  }

  console.log(props.agent.id);

  const result = await putData(`user/agents/${props.agent.id}/update/`, formData, true);

  console.log(result);

  if (result.success) {
    const updatedAgent: Agent = {
      ...result.data,
      picture: result.data.picture || "/assets/default-agent.png",
    };
    emit("updated", updatedAgent);
    emit("close");
  } else {
    alert(result.error || "Failed to update agent.");
  }
};

const deleteAgent = async () => {

  const result = await deleteData(`user/agents/${props.agent.id}/delete/`);

  if (result.success) {
    emit("deleted", props.agent.id);
    emit("close");
  } else {
    alert(result.error || "Failed to delete agent.");
  }
};

const handleImageUpload = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    selectedFile.value = input.files[0];
    previewImage.value = URL.createObjectURL(input.files[0]);
  }
};
</script>