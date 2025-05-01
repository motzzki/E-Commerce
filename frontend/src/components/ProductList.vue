<template>
  <div class="container mt-4">
    <h2 class="text-center">Product Management</h2>
    <div v-if="userIsEmployee">
      <button class="btn btn-primary mb-3" @click="showAddModal">
        Add Product
      </button>
    </div>

    <div class="row">
      <div v-for="product in products" :key="product.id" class="col-md-4">
        <div class="card mb-4">
          <img :src="product.image" class="card-img-top" alt="Product Image" />
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">{{ product.description }}</p>
            <p class="card-text">Price: ${{ product.price }}</p>
            <p class="card-text">Stock: {{ product.stock }}</p>
            <button class="btn btn-warning" @click="editProduct(product)">
              Edit
            </button>
            <button class="btn btn-danger" @click="deleteProduct(product.id)">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Product Modal -->
    <div class="modal" tabindex="-1" role="dialog" v-if="showModal">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Product</h5>
            <button
              type="button"
              class="close"
              @click="closeModal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addProduct">
              <div class="form-group">
                <label for="productName">Product Name</label>
                <input
                  type="text"
                  id="productName"
                  class="form-control"
                  v-model="newProduct.name"
                  required
                />
              </div>
              <div class="form-group">
                <label for="productDescription">Description</label>
                <textarea
                  id="productDescription"
                  class="form-control"
                  v-model="newProduct.description"
                  required
                ></textarea>
              </div>
              <div class="form-group">
                <label for="productPrice">Price</label>
                <input
                  type="number"
                  id="productPrice"
                  class="form-control"
                  v-model="newProduct.price"
                  required
                />
              </div>
              <div class="form-group">
                <label for="productStock">Stock</label>
                <input
                  type="number"
                  id="productStock"
                  class="form-control"
                  v-model="newProduct.stock"
                  required
                />
              </div>
              <div class="form-group">
                <label for="productImage">Product Image URL</label>
                <input
                  type="text"
                  id="productImage"
                  class="form-control"
                  v-model="newProduct.image"
                />
              </div>
              <button type="submit" class="btn btn-success mt-3">
                Add Product
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Imports
import { ref, onMounted } from "vue";
import axios from "axios"; // Axios configuration

// Data
const products = ref([]);
const showModal = ref(false);
const userIsEmployee = ref(localStorage.getItem("user_type") === "employee");
const newProduct = ref({
  name: "",
  description: "",
  price: 0,
  stock: 0,
  image: "",
});

// Methods
const fetchProducts = async () => {
  try {
    const response = await axios.get("products/");
    products.value = response.data;
  } catch (error) {
    console.error("There was an error fetching the products:", error);
  }
};

const showAddModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  resetForm();
};

const addProduct = async () => {
  try {
    const response = await axios.post("products/", newProduct.value);
    products.value.push(response.data);
    closeModal();
  } catch (error) {
    console.error("There was an error adding the product:", error);
  }
};

const editProduct = (product) => {
  // Handle edit functionality (you can create a similar modal as AddProduct)
};

const deleteProduct = async (productId) => {
  try {
    await axios.delete(`products/${productId}/`);
    products.value = products.value.filter(
      (product) => product.id !== productId
    );
  } catch (error) {
    console.error("There was an error deleting the product:", error);
  }
};

const resetForm = () => {
  newProduct.value = {
    name: "",
    description: "",
    price: 0,
    stock: 0,
    image: "",
  };
};

// On Mounted
onMounted(fetchProducts);
</script>

<style scoped>
.card-img-top {
  height: 200px;
  object-fit: cover;
}
</style>
