<template>
  <div v-if="visible" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white rounded-lg shadow-lg w-11/12 md:w-2/3 lg:w-1/2 xl:w-1/3 p-6 relative">
      <h2 class="text-xl font-semibold mb-4">{{ $t("newPage.signatureModal.title") }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">{{ $t("newPage.signatureModal.signatureContentLabel") }}</label>
          <div
            ref="editorRef"
            contenteditable="true"
            class="w-full border rounded p-2 min-h-[150px] overflow-auto"
            :placeholder="$t('newPage.signatureModal.signaturePlaceholder')"
            @input="handleInput"
            @paste="handlePaste"
            @dragover.prevent
            @drop="handleDrop"
          ></div>
        </div>
        <div class="flex items-center gap-x-1 mb-4 text-sm text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 my-auto">
            <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
          </svg>
          <span class="my-auto">{{ $t("newPage.signatureModal.editLaterInfo") }}</span>
        </div>
        <div class="flex justify-end">
          <button 
            type="button" 
            class="inline-flex w-full rounded-md bg-gray-200 px-3 py-2 text-sm font-semibold text-gray-700 shadow-sm hover:bg-gray-300 sm:w-auto mr-2"
            @click="handleEmptySignature"
          >
            {{ $t("newPage.signatureModal.cancel") }}
          </button>
          <button 
            type="submit" 
            class="inline-flex w-full rounded-md bg-gray-800 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black sm:w-auto"
          >
            {{ $t("newPage.signatureModal.create") }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, ref } from "vue";
import { postData } from "@/global/fetchData";
import { i18n } from "@/global/preferences";

const displayPopup = inject<(type: "success" | "error", title: string, message: string) => void>("displayPopup");
const editorRef = ref<HTMLDivElement | null>(null);
const signatureContent = ref("");

const props = defineProps({
  visible: {
    type: Boolean,
    required: true,
  },
  selectedEmail: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(["close", "created"]);

const handleInput = (e: Event) => {
  const target = e.target as HTMLDivElement;
  signatureContent.value = target.innerHTML;
};

const handlePaste = async (e: ClipboardEvent) => {
  e.preventDefault();
  
  if (e.clipboardData?.items) {
    for (const item of Array.from(e.clipboardData.items)) {
      if (item.type.startsWith('image/')) {
        const file = item.getAsFile();
        if (file) {
          const reader = new FileReader();
          reader.onload = (event) => {
            const img = document.createElement('img');
            img.src = event.target?.result as string;
            img.style.maxWidth = '100%';
            editorRef.value?.appendChild(img);
            signatureContent.value = editorRef.value?.innerHTML || '';
          };
          reader.readAsDataURL(file);
          return;
        }
      }
    }
  }
  
  const text = e.clipboardData?.getData('text/html') || e.clipboardData?.getData('text');
  if (text && editorRef.value) {
    const selection = window.getSelection();
    const range = selection?.getRangeAt(0);
    if (range) {
      range.deleteContents();
      const div = document.createElement('div');
      div.innerHTML = text;
      range.insertNode(div);
      signatureContent.value = editorRef.value.innerHTML;
    }
  }
};

const handleDrop = async (e: DragEvent) => {
  e.preventDefault();
  
  if (e.dataTransfer?.files) {
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const img = document.createElement('img');
        img.src = event.target?.result as string;
        img.style.maxWidth = '100%';
        editorRef.value?.appendChild(img);
        signatureContent.value = editorRef.value?.innerHTML || '';
      };
      reader.readAsDataURL(file);
      return;
    }
  }
};

const handleSubmit = async () => {
  if (!props.selectedEmail) {
    displayPopup?.("error", 
      i18n.global.t("newPage.signatureModal.error.noEmailSelected") as string, 
      i18n.global.t("newPage.signatureModal.error.noEmailSelectedMessage") as string
    );
    return;
  }

  const payload = {
    email: props.selectedEmail,
    signature_content: signatureContent.value,
  };

  try {
    const response = await postData("user/signatures/create/", payload);
    if (response.success) {
      displayPopup?.("success", 
        i18n.global.t("newPage.signatureModal.success.title") as string, 
        i18n.global.t("newPage.signatureModal.success.message") as string
      );
      emit("created", response.data);
      emit("close");
    } else {
      displayPopup?.("error", 
        i18n.global.t("newPage.signatureModal.error.creationFailed") as string, 
        response.error || i18n.global.t("newPage.signatureModal.error.creationFailedMessage") as string
      );
    }
  } catch (error) {
    displayPopup?.("error", 
      i18n.global.t("newPage.signatureModal.error.unexpected") as string, 
      i18n.global.t("newPage.signatureModal.error.unexpectedMessage") as string
    );
  }
};

const handleEmptySignature = async () => {
  if (!props.selectedEmail) {
    displayPopup?.("error", 
      i18n.global.t("newPage.signatureModal.error.noEmailSelected") as string, 
      i18n.global.t("newPage.signatureModal.error.noEmailSelectedMessage") as string
    );
    return;
  }

  const payload = {
    email: props.selectedEmail,
    signature_content: "",
  };

  try {
    const response = await postData("user/signatures/create/", payload);
    if (response.success) {
      emit("created", response.data);
      emit("close");
    }
  } catch (error) {
    console.error(i18n.global.t("newPage.signatureModal.error.emptyCreationFailed") as string, error);
  }
  
  emit("close");
};
</script>

<style scoped>
[contenteditable]:empty:before {
  content: attr(placeholder);
  color: #9ca3af;
  cursor: text;
}
</style>