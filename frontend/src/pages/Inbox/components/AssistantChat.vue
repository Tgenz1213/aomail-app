<template>
  <div class="z-30 bg-gray-50 ring-1 shadow-sm ring-black ring-opacity-5 h-full flex flex-col relative w-[325px] 2xl:w-[525px]">
    <div class="flex flex-col h-full">
      <div class="flex-grow">
        <div class="flex p-5">
          <div class="mr-4 flex-shrink-0 self-center">
            <span class="inline-flex h-14 w-14 items-center justify-center rounded-full bg-gray-900 text-white">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
              </svg>
            </span>
          </div>
          <div>
            <p class="mt-1" id="animated-text" ref="animatedText"></p>
          </div>
        </div>
      </div>
      <div class="flex flex-col justify-end h-[160px] border-t">
        <textarea
          id="dynamicTextarea"
          @keydown.enter="handleEnterKey"
          @input="adjustHeight"
          v-model="textareaValue"
          class="overflow-y-hidden flex flex-1 pt-3 pl-5 w-full border-transparent bg-transparent text-gray-900 placeholder:text-gray-400 sm:text-sm sm:leading-6 focus:border-transparent focus:bg-transparent focus:ring-0"
          :placeholder="$t('constants.instruction')"
        ></textarea>
        <div class="flex justify-end m-3">
          <button
            type="button"
            class="w-[80px] rounded bg-gray-700 px-2.5 py-1.5 text-sm text-white shadow-sm hover:bg-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
            @click="sendMessage"
          >
            {{ $t('constants.userActions.send') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const animatedText = ref<HTMLElement | null>(null);
const textareaValue = ref('');

const emit = defineEmits<{
  (e: 'toggle-visibility'): void;
}>();

const adjustHeight = (event: Event) => {
  const textarea = event.target as HTMLTextAreaElement;
  textarea.style.height = 'auto';
  textarea.style.height = `${textarea.scrollHeight}px`;
};

const handleEnterKey = (event: KeyboardEvent) => {
  if (!event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
};

const sendMessage = () => {
  // Implement send message logic here
  console.log('Sending message:', textareaValue.value);
  textareaValue.value = '';
};

const animateText = (text: string) => {
  if (animatedText.value) {
    animatedText.value.textContent = '';
    const characters = text.split('');
    let currentIndex = 0;

    const interval = setInterval(() => {
      if (currentIndex < characters.length) {
        animatedText.value!.textContent += characters[currentIndex];
        currentIndex++;
      } else {
        clearInterval(interval);
      }
    }, 30);
  }
};

</script>
