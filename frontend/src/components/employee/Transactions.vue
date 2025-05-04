<template>
  <EmployeeNav />
  <div class="container mt-5">
    <h2 class="custom-title">Transactions</h2>

    <!-- Filter by Exact Date -->
    <div class="mb-4 row g-3 align-items-center">
      <div class="col-auto">
        <label for="filterDate" class="col-form-label custom-label"
          >Select Date:</label
        >
      </div>
      <div class="col-auto">
        <input
          type="date"
          id="filterDate"
          v-model="filterDate"
          class="form-control custom-input"
        />
      </div>
    </div>

    <div v-if="filteredOrders.length === 0" class="text-muted">
      No transactions available.
    </div>

    <!-- Cards in two columns -->
    <div class="row">
      <div
        v-for="order in filteredOrders"
        :key="order.id"
        class="col-md-6 mb-4"
      >
        <div class="card shadow-lg rounded">
          <div class="card-body">
            <h5 class="card-title custom-card-title">Order #{{ order.id }}</h5>
            <p class="card-text custom-text">
              Date: {{ formatDate(order.created_at) }}
            </p>

            <!-- Total Price -->
            <p class="card-text custom-total-price">
              Total: ${{ getOrderTotal(order.items).toFixed(2) }}
            </p>

            <button
              class="btn btn-outline-primary custom-btn-toggle"
              @click="toggleProducts(order.id)"
            >
              {{ expandedOrders.includes(order.id) ? "Hide" : "View" }} Products
            </button>

            <div v-if="expandedOrders.includes(order.id)" class="mt-3">
              <ul v-if="order.items && order.items.length">
                <li
                  v-for="item in order.items"
                  :key="item.product.id"
                  class="list-group-item custom-list-item"
                >
                  {{ item.product.name }} — ${{ item.product.price }} ×
                  {{ item.quantity }}
                </li>
              </ul>
              <div v-else class="text-muted">Loading products...</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../../axios";
import EmployeeNav from "./EmployeeNav.vue";

export default {
  components: {
    EmployeeNav,
  },
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
        const orderDate = new Date(order.created_at)
          .toISOString()
          .split("T")[0];
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
.custom-title {
  font-family: "Roboto", sans-serif;
  font-weight: 700;
  color: #333;
  margin-bottom: 2rem;
}

.custom-label {
  font-family: "Roboto", sans-serif;
  font-weight: 500;
  color: #555;
}

.custom-input {
  border-radius: 8px;
  border-color: #ddd;
  font-size: 1rem;
}

.custom-card-title {
  font-family: "Roboto", sans-serif;
  font-weight: 600;
  color: #333;
}

.custom-text {
  font-family: "Roboto", sans-serif;
  font-weight: 400;
  color: #555;
}

.custom-total-price {
  font-family: "Roboto", sans-serif;
  font-weight: 600;
  color: #007bff;
}

.custom-btn-toggle {
  border-radius: 20px;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.custom-btn-toggle:hover {
  background-color: #007bff;
  color: white;
}

.custom-list-item {
  font-family: "Roboto", sans-serif;
  color: #333;
  font-size: 1rem;
  padding: 0.75rem 1rem;
}

.card-body {
  padding: 1.5rem;
}

.card {
  border-radius: 15px;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-body p {
  font-size: 1.1rem;
}

.card-body h5 {
  font-size: 1.25rem;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .custom-title {
    font-size: 1.5rem;
  }

  .custom-text {
    font-size: 1rem;
  }

  .custom-total-price {
    font-size: 1.1rem;
  }
}
</style>
