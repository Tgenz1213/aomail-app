<template>
  <div>
    <h1>{{ $t('StripepaymentSuccess_vue.payment_successful') }}</h1>
    <p>{{ $t('StripepaymentSuccess_vue.thank_you') }}</p>
    <p>{{ $t('StripepaymentSuccess_vue.product') }}: {{ productName }}</p>
  </div>
</template>

<script>
export default {
  name: 'StripePaymentSuccess',
  data() {
    return {
      productName: null,
    };
  },
  mounted() {
    // Fetch product information from backend
    // You can use Axios or Fetch API to make an API call to your backend
    // Replace 'YOUR_BACKEND_URL' with your actual backend URL
    fetch('YOUR_BACKEND_URL')
      .then(response => response.json())
      .then(data => {
        this.productName = data.productName;
      })
      .catch(error => {
        console.error('Error fetching product information:', error);
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
