<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
      <h2 class="text-xl font-semibold mb-4">Update Agent</h2>
      <form @submit.prevent="updateAgent">
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

        <div class="flex justify-between items-center">
          <button
            type="button"
            @click="deleteAgent"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
          >
            Delete
          </button>
          <div class="flex space-x-2">
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
import { postData, deleteData } from "@/global/fetchData";
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
  const payload = {
    agent_name: agentName.value,
    behavior_description: behaviorDescription.value,
    length: length.value,
    formality: formality.value,
  };

  const result = await postData(`user/agents/update/${props.agent.id}/`, payload);

  if (result.success) {
    const updatedAgent: Agent= {
      ...result.data,
      pictureUrl: result.data.picture || "/assets/default-agent.png",
    };
    emit("updated", updatedAgent);
    emit("close");
  } else {
    alert(result.error || "Failed to update agent.");
  }
};

const deleteAgent = async () => {
  if (!confirm("Are you sure you want to delete this agent?")) return;

  const result = await deleteData(`user/agents/delete/${props.agent.id}/`);

  if (result.success) {
    emit("deleted", props.agent.id);
    emit("close");
  } else {
    alert(result.error || "Failed to delete agent.");
  }
};
</script>

<style scoped>
/* Add any necessary styles here */
</style> 