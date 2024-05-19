<template>
  <div>
    <h1>{{ $t('"401_vue.titre') }}</h1>
    <p>{{ $t('"401_vue.titre2') }} {{ countdown }} seconds</p>
  </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue';

const countdown = ref(5);
const instance = getCurrentInstance();

const updateCountdown = () => {
  countdown.value--;

  if (countdown.value < 0) {
    // REDIRECTION TO LOGIN PAGE
    instance.appContext.config.globalProperties.$router.push({ name: 'login' });
  } else {
    setTimeout(updateCountdown, 1000); // Call itself after 1 second
  }
};

// Start countdown on component mount
updateCountdown();
</script>
