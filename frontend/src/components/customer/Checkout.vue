<template>
  <div class="container mt-4">
    <h2>Checkout</h2>
    <p>Total amount: ${{ total }}</p>

    <form @submit.prevent="submitOrder">
      <div class="mb-3">
        <label for="address" class="form-label">Shipping Address</label>
        <input v-model="address" id="address" class="form-control" required />
      </div>
      <button type="submit" class="btn btn-success">Place Order</button>
    </form>
  </div>
</template>

<script>
import axios from "../../axios";

export default {
  data() {
    return {
      cart: [],
      address: "",
    };
  },
  computed: {
    total() {
      return this.cart
        .reduce((sum, item) => sum + parseFloat(item.price), 0)
        .toFixed(2);
    },
  },
  methods: {
    submitOrder() {
      const orderData = {
        address: this.address,
        items: this.cart.map((item) => item.id),
      };

      axios
        .post("orders/", orderData)
        .then(() => {
          alert("Order placed successfully!");
          localStorage.removeItem("cart");
          this.$router.push("/customer/products");
        })
        .catch(() => alert("Something went wrong"));
    },
  },
  mounted() {
    this.cart = JSON.parse(localStorage.getItem("cart") || "[]");
  },
};
</script>
