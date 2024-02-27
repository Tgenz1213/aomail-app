<template>
    <div v-if="localShowPopup" class="popup">
        <p>{{ message }}</p>
        <button @click="dismissPopup">Close</button>
    </div>
</template>
  
<script>
export default {
    props: {
        showPopup: Boolean,
        message: String,
        duration: {
            type: Number,
            default: 5000,
        },
    },
    data() {
        return {
            localShowPopup: this.showPopup,
        };
    },
    watch: {
        showPopup(newVal) {
            this.localShowPopup = newVal;
            if (newVal) {
                this.showPopupWithTimer();
            }
        },
    },
    methods: {
        showPopupWithTimer() {
            this.localShowPopup = true;

            // Set a timeout for auto-dismiss
            this.timerId = setTimeout(() => {
                console.log("THE TIMER HAS BEEN TRIGGERED")
                this.dismissPopup();
            }, this.duration);
        },

        dismissPopup() {
            // Dismiss the popup
            console.log("CLOSING");
            this.localShowPopup = false;
            this.$emit('updateShowPopup', false);

            // Cancel the timer
            clearTimeout(this.timerId);
        },
    },
};
</script>
  
<style scoped>
.popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ccc;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    text-align: center;
}
</style>
  