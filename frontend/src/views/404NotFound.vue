<template>
  <div>
    <h1>{{ $t('"404_vue.titre') }}</h1>
    <p>{{ $t('"404_vue.titre2') }}</p>
  </div>
</template>
  
<script>
export default {
  name: 'NotFound',
};
</script>
  
<style scoped>
body {
  font-family: 'Arial', sans-serif;
  text-align: center;
  padding: 50px;
  background-color: #f0f0f0;
}

h1 {
  font-size: 3em;
  color: #333;
  margin-bottom: 10px;
}

p {
  font-size: 1.2em;
  color: #555;
  margin-top: 0;
}
</style>
  