<template>
  <div>
    <h1>{{ $t('errorWebPagesTemplates.error404Page.pageNotFound') }}</h1>
    <p>{{ $t('errorWebPagesTemplates.error404Page.pageDoesNotExist') }}</p>
  </div>
</template>
  
<script>
// TODO: add automatic redirection to login
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
  