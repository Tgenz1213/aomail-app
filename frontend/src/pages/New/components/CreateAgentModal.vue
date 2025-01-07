<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
      <h2 class="text-xl font-semibold mb-4">Create New Agent</h2>
      <form @submit.prevent="createAgent">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Agent Name</label>
          <input
            type="text"
            v-model="agentName"
            required
            class="mt-1 block w-full border border-gray-300 rounded-md p-2"
            placeholder="Enter agent name"
          />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Behavior Description (Optional)</label>
          <textarea
            v-model="behaviorDescription"
            class="mt-1 block w-full border border-gray-300 rounded-md p-2"
            placeholder="Describe agent behavior"
          ></textarea>
        </div>

        <div class="flex space-x-4 mb-4">
          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-700">Length</label>
            <select v-model="length" required class="mt-1 block w-full border border-gray-300 rounded-md p-2">
              <option value="very short">Very Short</option>
              <option value="short">Short</option>
              <option value="medium">Medium</option>
            </select>
          </div>

          <div class="flex-1">
            <label class="block text-sm font-medium text-gray-700">Formality</label>
            <select v-model="formality" required class="mt-1 block w-full border border-gray-300 rounded-md p-2">
              <option value="informal">Informal</option>
              <option value="formal">Formal</option>
              <option value="very formal">Very Formal</option>
            </select>
          </div>
        </div>

        <div class="flex justify-end space-x-2">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Create
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

const emit = defineEmits(['created', 'close']);

const agentName = ref("");
const behaviorDescription = ref("");
const length = ref("short");
const formality = ref("formal");

const createAgent = async () => {
  const payload = {
    agent_name: agentName.value,
    behavior_description: behaviorDescription.value,
    length: length.value,
    formality: formality.value,
  };

  const result = await postData("user/agents/create/", payload);

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

<style scoped>
/* Add any necessary styles here */
</style> 