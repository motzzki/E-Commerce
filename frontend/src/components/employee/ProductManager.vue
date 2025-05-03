<template>
  <div class="container mt-4">
    <h2>Product Manager</h2>
    <button class="btn btn-primary mb-3" @click="openCreateForm">
      Add Product
    </button>

    <div v-if="products.length">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Name</th>
            <th>Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.name }}</td>
            <td>{{ product.price }}</td>
            <td>
              <button class="btn btn-sm btn-warning me-2">Edit</button>
              <button
                class="btn btn-sm btn-danger"
                @click="deleteProduct(product.id)"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else>
      <p>No products available.</p>
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
    deleteProduct(id) {
      axios.delete(`products/${id}/`).then(() => {
        this.fetchProducts();
      });
    },
    openCreateForm() {
      // Show create product form modal (optional)
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>
