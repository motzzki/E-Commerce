<template>
  <div class="container mt-4">
    <h2>Product List</h2>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div>
        <button class="btn btn-primary" @click="logout">Logout</button>
        <router-link to="/customer/cart" class="btn btn-secondary ms-2">Cart</router-link>
      </div>
      <!-- 🔍 Search Bar -->
      <input
        type="text"
        v-model="searchQuery"
        class="form-control w-50"
        placeholder="Search products..."
      />
    </div>

    <div class="row">
      <!-- Filtered Products -->
      <div class="col-md-4" v-for="product in filteredProducts" :key="product.id">
        <div class="card mb-4">
          <!-- 🖼️ Product Image -->
          <img
            v-if="product.image"
            :src="product.image"
            class="card-img-top"
            alt="Product Image"
            style="height: 200px; object-fit: cover;"
          />
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">{{ product.description }}</p>
            <p class="text-primary fw-bold">${{ product.price }}</p>
            <button class="btn btn-success w-100" @click="addToCart(product)">
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
      searchQuery: "", // Added search query for filtering
    };
  },
  computed: {
    // Computed property to filter products based on search query
    filteredProducts() {
      if (!this.searchQuery) {
        return this.products; // If no search, return all products
      }
      return this.products.filter((product) => {
        return product.name.toLowerCase().includes(this.searchQuery.toLowerCase()); // Filter products based on search query
      });
    },
  },
  methods: {
    fetchProducts() {
      axios.get("products/").then((res) => {
        this.products = res.data;
      });
    },
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("userType");
      localStorage.removeItem("cart");
      localStorage.removeItem("role");
      localStorage.removeItem("projects");
      this.$router.push("/login");
    },
    addToCart(product) {
      let quantity = prompt("Enter quantity:");

      // Validate input: must be a number > 0 and an integer
      quantity = parseInt(quantity);
      if (isNaN(quantity) || quantity <= 0) {
        alert("Please enter a valid quantity (a number greater than 0).");
        return;
      }

      const cart = JSON.parse(localStorage.getItem("cart") || "[]");

      // Clone product and add quantity field
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
