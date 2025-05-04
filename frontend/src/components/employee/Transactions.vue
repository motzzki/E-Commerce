<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <button class="btn btn-secondary" @click="$router.go(-1)">Back</button> <!-- Back Button -->
      <h2>Transactions</h2>
      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>

    <!-- Filter by Exact Date -->
    <div class="mb-4 row g-3 align-items-center">
      <div class="col-auto">
        <label for="filterDate" class="col-form-label">Select Date:</label>
      </div>
      <div class="col-auto">
        <input
          type="date"
          id="filterDate"
          v-model="filterDate"
          class="form-control"
        />
      </div>
    </div>

    <div v-if="filteredOrders.length === 0">No transactions available.</div>

    <div
      v-for="order in filteredOrders"
      :key="order.id"
      class="card mb-3 shadow-sm"
    >
      <div class="card-body">
        <h5 class="card-title">Order #{{ order.id }}</h5>
        <p class="card-text">Date: {{ formatDate(order.created_at) }}</p>
        
        <!-- Total Price -->
        <p class="card-text">
          Total: ${{ getOrderTotal(order.items).toFixed(2) }}
        </p>

        <button
          class="btn btn-outline-primary"
          @click="toggleProducts(order.id)"
        >
          {{ expandedOrders.includes(order.id) ? "Hide" : "View" }} Products
        </button>

        <div v-if="expandedOrders.includes(order.id)" class="mt-3">
          <ul v-if="order.items && order.items.length">
            <li
              v-for="item in order.items"
              :key="item.product.id"
              class="list-group-item"
            >
               {{ item.product.name }} — ${{ item.product.price }} × {{ item.quantity }}
            </li>
          </ul>
          <div v-else>Loading products...</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../../axios";

export default {
  data() {
    return {
      orders: [],
      expandedOrders: [],
      filterDate: "",
    };
  },
  computed: {
    filteredOrders() {
      if (!this.filterDate) return this.orders;
      return this.orders.filter((order) => {
        const orderDate = new Date(order.created_at).toISOString().split("T")[0];
        return orderDate === this.filterDate;
      });
    },
  },
  methods: {
    async fetchOrders() {
      try {
        const res = await axios.get("/orders/");
        this.orders = res.data;
      } catch (err) {
        alert("Failed to load transactions");
      }
    },
    getOrderTotal(items) {
      if (!items) return 0;
      return items.reduce((total, item) => {
        return total + item.product.price * item.quantity;
      }, 0);
    },
    async toggleProducts(orderId) {
      const index = this.expandedOrders.indexOf(orderId);
      if (index !== -1) {
        this.expandedOrders.splice(index, 1);
      } else {
        const order = this.orders.find((o) => o.id === orderId);
        if (!order.items) {
          try {
            const res = await axios.get(`/orders/${orderId}/`);
            order.items = res.data.items;
          } catch (err) {
            alert("Failed to load products for order");
            return;
          }
        }
        this.expandedOrders.push(orderId);
      }
    },
    formatDate(dateString) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    logout() {
      localStorage.clear(); // or sessionStorage.clear() if you use that
      this.$router.push("/login"); // redirect to login page
    },
  },
  mounted() {
    this.fetchOrders();
  },
};
</script>

<style scoped>
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

.card-title {
  font-family: 'Kalnia', serif;
  color: #6b4f3b; /* Earthy brown */
  font-size: 1.25rem;
  font-weight: bold;
}

.card-text {
  font-family: 'Montserrat', sans-serif;
  color: #4e3629; /* Dark brown */
}

button.btn-outline-primary {
  border-color: #6b4f3b; /* Earthy brown */
  color: #6b4f3b;
  font-weight: 500;
  font-family: 'Montserrat', sans-serif;
  transition: all 0.3s ease;
}

button.btn-outline-primary:hover {
  background-color: #6b4f3b; /* Dark brown on hover */
  color: white;
}

.list-group-item {
  font-family: 'Montserrat', sans-serif;
  background-color: transparent;
  border: none;
  color: #3c2f2f; /* Dark muted brown */
  padding-left: 0;
}

.btn-danger,
.btn-secondary {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  background-color: #6b4f3b; /* Earthy brown */
  color: white;
  border-color: #6b4f3b;
}

.btn-danger:hover,
.btn-secondary:hover {
  background-color: #4e3629; /* Darker brown */
  border-color: #4e3629;
  color: white;
}

h2 {
  font-family: 'Kalnia', serif;
  color: #6b4f3b; /* Earthy brown */
}

button.btn.custom-btn {
  background-color: #6b4f3b; /* Earthy brown */
  color: white;
  font-weight: bold;
  border-radius: 12px;
  transition: background-color 0.3s ease;
}

button.btn.custom-btn:hover {
  background-color: #4e3629; /* Darker brown on hover */
  color: white;
}

/* Styling for date picker input */
input[type="date"] {
  background-color: #fffaf6; /* Match with the card background */
  border: 1px solid #bfa58d; /* Lighter earthy brown border */
  border-radius: 8px;
  padding: 8px;
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  color: #4e3629; /* Dark brown text */
  transition: border-color 0.3s ease, background-color 0.3s ease;
}

input[type="date"]:focus {
  outline: none;
  border-color: #6b4f3b; /* Earthy brown focus border */
  background-color: #f2e6d9; /* Lighter brown on focus */
}

input[type="date"]::-webkit-calendar-picker-indicator {
  background-color: #6b4f3b; /* Earthy brown for calendar icon */
  border-radius: 4px;
}

input[type="date"]:disabled {
  background-color: #e5e0dc; /* Disabled state with a muted color */
  color: #9e9e9e; /* Muted text for disabled input */
}
</style>

