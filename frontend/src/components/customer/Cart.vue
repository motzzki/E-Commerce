<template>
  <CustomerNav />
  <div class="container mt-4">
    <router-link to="/customer/products" class="btn btn-secondary mb-3">
      ← Back to Products
    </router-link>

    <h2>Your Cart</h2>

    <table class="table" v-if="cart.length">
      <thead>
        <tr>
          <th>Product</th>
          <th>Price</th>
          <th>Quantity</th>
          <th>Subtotal</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in cart" :key="index">
          <td>{{ item.name }}</td>
          <td>${{ item.price }}</td>
          <td>{{ item.quantity }}</td>
          <td>${{ (item.price * item.quantity).toFixed(2) }}</td>
          <td>
            <button class="btn btn-sm btn-danger" @click="removeItem(index)">
              Remove
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else>
      <p>Your cart is empty.</p>
    </div>

    <div class="mt-3" v-if="cart.length">
      <h5>Total: ${{ total }}</h5>
      <router-link to="/customer/checkout" class="btn btn-primary">
        Proceed to Checkout
      </router-link>
    </div>
  </div>
</template>

<script>
import CustomerNav from "./CustomerNav.vue";

export default {
  components: {
    CustomerNav,
  },
  data() {
    return {
      cart: [],
    };
  },
  computed: {
    total() {
      return this.cart
        .reduce((sum, item) => sum + item.price * item.quantity, 0)
        .toFixed(2);
    },
  },
  methods: {
    loadCart() {
      const rawCart = JSON.parse(localStorage.getItem("cart") || "[]");
      this.cart = rawCart.map((item) => ({
        ...item,
        quantity: item.quantity || 1,
      }));
    },
    removeItem(index) {
      this.cart.splice(index, 1);
      localStorage.setItem("cart", JSON.stringify(this.cart));
    },
  },
  mounted() {
    this.loadCart();
  },
};
</script>
