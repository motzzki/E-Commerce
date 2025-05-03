<template>
  <div class="container mt-4">
    <h2>Store</h2>
    <div class="row">
      <div class="col-md-4" v-for="product in products" :key="product.id">
        <div class="card mb-4">
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
    };
  },
  methods: {
    fetchProducts() {
      axios.get("products/").then((res) => {
        this.products = res.data;
      });
    },
    addToCart(product) {
      const cart = JSON.parse(localStorage.getItem("cart") || "[]");
      cart.push(product);
      localStorage.setItem("cart", JSON.stringify(cart));
      alert("Added to cart");
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>
