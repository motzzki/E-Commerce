<template>
  <EmployeeNav />
  <div class="container mt-5">
    <!-- Page Title -->
    <h2 class="custom-title mb-4">Product Manager</h2>

    <div class="mb-3">
      <!-- Add Product Button -->
      <button class="btn btn-success custom-btn" @click="openCreateForm">
        <i class="bi bi-plus-lg me-1"></i> Add Product
      </button>
    </div>

    <!-- Product Table -->
    <div v-if="products.length">
      <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
        <div class="col" v-for="product in products" :key="product.id">
          <div class="card h-100">
            <img
              :src="
                product.image ||
                'https://via.placeholder.com/286x180.png?text=No+Image'
              "
              class="card-img-top"
              alt="Product Image"
              style="object-fit: cover; height: 180px"
            />
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">{{ product.name }}</h5>
              <p class="card-text">{{ product.description }}</p>
              <p class="fw-bold mb-1">Price: ${{ product.price }}</p>
              <p class="text-muted mb-2">Stock: {{ product.stock }}</p>
              <!-- Stock added here -->
              <div class="mt-auto">
                <button
                  class="btn btn-sm btn-warning me-2"
                  @click="openEditForm(product)"
                >
                  Edit
                </button>
                <button
                  class="btn btn-sm btn-danger"
                  @click="deleteProduct(product.id)"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Products Available -->
    <div v-else>
      <p class="text-muted">No products available.</p>
    </div>

    <!-- Modal for Create/Edit -->
    <div v-if="showModal" class="modal d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
          <form @submit.prevent="submitProduct">
            <div class="modal-header">
              <h5 class="modal-title custom-title">
                {{ isEditing ? "Edit" : "Add" }} Product
              </h5>
              <button
                type="button"
                class="btn-close"
                @click="closeModal"
              ></button>
            </div>
            <div class="modal-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Name</label>
                  <input
                    v-model="form.name"
                    class="form-control custom-input"
                    placeholder="Enter product name"
                    required
                  />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Price</label>
                  <input
                    type="number"
                    v-model="form.price"
                    class="form-control custom-input"
                    placeholder="e.g. 29.99"
                    required
                  />
                </div>
                <div class="col-12">
                  <label class="form-label">Description</label>
                  <textarea
                    v-model="form.description"
                    class="form-control custom-input"
                    placeholder="Product details"
                    rows="3"
                    required
                  ></textarea>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Stock</label>
                  <input
                    type="number"
                    v-model="form.stock"
                    class="form-control custom-input"
                    required
                  />
                </div>
                <div class="col-md-6">
                  <label class="form-label">Image</label>
                  <input
                    type="file"
                    @change="handleImage"
                    class="form-control custom-input"
                  />
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="closeModal">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary custom-btn">
                {{ isEditing ? "Update" : "Create" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-backdrop fade show"></div>
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
      products: [],
      showModal: false,
      isEditing: false,
      selectedId: null,
      form: {
        name: "",
        description: "",
        price: "",
        stock: "",
        image: null,
      },
    };
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
      this.$router.push("/login");
    },
    openCreateForm() {
      this.resetForm();
      this.isEditing = false;
      this.showModal = true;
    },
    openEditForm(product) {
      this.form = { ...product, image: null };
      this.selectedId = product.id;
      this.isEditing = true;
      this.showModal = true;
    },
    openTransaction() {
      this.$router.push("transactions");
    },
    handleImage(e) {
      this.form.image = e.target.files[0];
    },
    closeModal() {
      this.showModal = false;
    },
    resetForm() {
      this.form = {
        name: "",
        description: "",
        price: "",
        stock: "",
        image: null,
      };
      this.selectedId = null;
    },
    submitProduct() {
      const formData = new FormData();
      formData.append("name", this.form.name);
      formData.append("description", this.form.description);
      formData.append("price", this.form.price);
      formData.append("stock", this.form.stock);
      if (this.form.image) {
        formData.append("image", this.form.image);
      }

      if (this.isEditing) {
        axios.put(`products/${this.selectedId}/`, formData).then(() => {
          this.fetchProducts();
          this.closeModal();
        });
      } else {
        axios.post("products/", formData).then(() => {
          this.fetchProducts();
          this.closeModal();
        });
      }
    },
    deleteProduct(id) {
      if (confirm("Are you sure you want to delete this product?")) {
        axios
          .delete(`products/${id}/`)
          .then(() => {
            this.fetchProducts();
          })
          .catch((err) => {
            alert(err.response.data.error || "Failed to delete product.");
          });
      }
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>

<style scoped>
.custom-title {
  font-family: "Kalnia", sans-serif;
  font-weight: bold;
  color: #6b4f3b; /* Earthy brown */
}

.custom-btn {
  background-color: #6b4f3b; /* Earthy brown */
  color: white;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.custom-btn:hover {
  background-color: #4e3629; /* Dark brown */
}

.custom-input {
  border-color: #bfa58d; /* Lighter brown for input border */
}

.img-thumbnail {
  border: 1px solid #ccc;
  border-radius: 0.5rem;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #00000050;
  z-index: 1040;
}

.modal {
  z-index: 1050;
}
</style>
