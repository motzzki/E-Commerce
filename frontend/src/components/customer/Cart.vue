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

    <!-- Cart Total and Checkout Button -->
    <div class="mt-3" v-if="cart.length">
      <h5>Total: ${{ total }}</h5>
      <router-link to="/customer/checkout" class="btn custom-btn">
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

<style scoped>
/* Card Styles */
.card {
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(107, 79, 59, 0.1); /* Earthy brown shadow */
  border: 1px solid #e5e0dc;
  background-color: #fffaf6; /* Light earthy tone */
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 16px rgba(107, 79, 59, 0.15);
}

/* Title */
h2 {
  font-family: "Kalnia", serif;
  color: #6b4f3b; /* Earthy brown */
  font-size: 1.75rem;
  font-weight: bold;
}

/* Table Styles */
.table th,
.table td {
  font-family: "Montserrat", sans-serif;
  color: #4e3629; /* Dark brown */
}

/* Buttons */
.btn-danger {
  font-family: "Montserrat", sans-serif;
  font-weight: 600;
  background-color: #6b4f3b; /* Earthy brown */
  color: white;
  border-color: #6b4f3b;
}

.btn-danger:hover {
  background-color: #4e3629; /* Darker brown */
  border-color: #4e3629;
  color: white;
}

.btn-secondary {
  font-family: "Montserrat", sans-serif;
  font-weight: 600;
  background-color: #fffaf6;
  color: #6b4f3b; /* Earthy brown */
  border-color: #e5e0dc;
}

.btn-secondary:hover {
  background-color: #e5e0dc;
  color: #6b4f3b;
}

/* Custom Checkout Button */
.custom-btn {
  background-color: #6b4f3b; /* Earthy brown */
  color: white;
  font-weight: bold;
  border-radius: 12px;
  transition: background-color 0.3s ease;
}

.custom-btn:hover {
  background-color: #4e3629; /* Darker brown on hover */
  color: white;
}
</style>
