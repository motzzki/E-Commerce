<template>
  <div class="container mt-5">
    <h2 class="custom-title mb-4">Product List</h2>

    <div class="d-flex flex-column flex-md-row justify-content-between align-items-center mb-4 gap-3">
      <div>
        <button class="custom-btn me-2" @click="logout">Logout</button>
        <router-link to="/customer/cart" class="btn btn-outline-secondary btn-cart">Cart</router-link>
      </div>

      <!-- 🔍 Search Bar -->
      <input
        type="text"
        v-model="searchQuery"
        class="custom-input w-100 w-md-50"
        placeholder="Search products..."
      />
    </div>

    <div class="row g-4">
      <div
        class="col-12 col-sm-6 col-md-4 col-lg-3"
        v-for="product in filteredProducts"
        :key="product.id"
      >
        <div class="card h-100 product-card">
          <img
            v-if="product.image"
            :src="product.image"
            class="card-img-top"
            alt="Product Image"
            style="height: 200px; object-fit: cover;"
          />
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">{{ product.description }}</p>
            <p class="text-primary fw-bold">${{ product.price }}</p>
            <p class="text-muted">Stock: {{ product.stock }}</p>
            <button
              class="custom-btn mt-auto w-100"
              @click="addToCart(product)"
            >
              Add to Cart
            </button>
          </div>
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
      products: [],
      searchQuery: "",
    };
  },
  computed: {
    filteredProducts() {
      if (!this.searchQuery) return this.products;
      return this.products.filter((product) =>
        product.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    fetchProducts() {
      axios.get("products/").then((res) => {
        this.products = res.data;
      });
    },
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
    addToCart(product) {
      let quantity = parseInt(prompt("Enter quantity:"));
      if (isNaN(quantity) || quantity <= 0) {
        alert("Please enter a valid quantity.");
        return;
      }

      const cart = JSON.parse(localStorage.getItem("cart") || "[]");
      const productWithQuantity = { ...product, quantity };
      cart.push(productWithQuantity);
      localStorage.setItem("cart", JSON.stringify(cart));
      alert(`Added ${quantity} of ${product.name} to cart.`);
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>

<style scoped>

/* Earth-Toned Buttons */
.custom-btn {
  font-family: 'Montserrat', sans-serif;
  background-color: #6b4f3b;
  color: #fff;
  border: 2px solid #6b4f3b;
  border-radius: 10px;
  padding: 10px 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-right: 8px;
  margin-bottom: 8px;
  width: 100%;
}

.custom-btn:hover {
  background-color: #3c2f2f;
  border-color: #3c2f2f;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(76, 50, 36, 0.3);
}

/* Secondary Button (Cart) */
.btn-outline-secondary {
  font-family: 'Montserrat', sans-serif;
  border-color: #bfa58d;
  color: #6b4f3b;
  background-color: #fffaf6;
}

.btn-outline-secondary:hover {
  background-color: #e7d6c1;
  border-color: #6b4f3b;
  color: #3c2f2f;
}

/* Inputs */
.custom-input {
  font-family: 'Montserrat', sans-serif;
  border: 2px solid #bfa58d;
  border-radius: 8px;
  padding: 10px;
  font-size: 1rem;
  background-color: #fffaf6;
  color: #4e3629;
  transition: 0.3s ease;
}

.custom-input:focus {
  outline: none;
  border-color: #6b4f3b;
  box-shadow: 0 0 8px rgba(107, 79, 59, 0.3);
  background-color: #f5e8da;
}

/* Cards */
.product-card {
  border-radius: 16px;
  border: 2px solid #e5e0dc;
  background-color: #fffaf6;
  box-shadow: 0 2px 8px rgba(107, 79, 59, 0.1);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.product-card:hover {
  box-shadow: 0 6px 18px rgba(107, 79, 59, 0.25);
  transform: translateY(-5px);
}

/* Price */
.product-card .price {
  color: #b67236; /* warm amber-brown */
  font-weight: bold;
  font-size: 1.1rem;
}

.btn-cart {
  width: 100%;
  font-weight: bold;
}

.card-title{
font-family: 'Kalnia', serif;
font-weight: bold;
color: #6b4f3b;
}
</style>
