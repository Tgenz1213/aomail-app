<template>
    <div>
        <h1>{{ $t('StripepaymentF_vue.titre') }}</h1>
        <p>{{ $t('StripepaymentF_vue.titre2') }}</p>
        <p>{{ $t('StripepaymentF_vue.product') }}: {{ errorMessage }}</p>
    </div>
</template>

<script>
export default {
    name: 'StripePaymentFailed',
    data() {
        return {
            errorMessage: null,
        };
    },
    mounted() {
        // Fetch error message from backend
        // You can use Axios or Fetch API to make an API call to your backend
        // Replace 'YOUR_BACKEND_URL' with your actual backend URL
        fetch('YOUR_BACKEND_URL')
            .then(response => response.json())
            .then(data => {
                this.errorMessage = data.error;
            })
            .catch(error => {
                console.error('Error fetching error message:', error);
            });
    },
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