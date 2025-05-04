<template>
  <EmployeeNav />
  <div class="container mt-5">
    <h2 class="custom-title mb-4 text-center">Product Manager</h2>

    <div class="d-flex justify-content-between mb-4">
      <button class="btn btn-success custom-btn" @click="openCreateForm">
        <i class="bi bi-plus-lg me-1"></i> Add Product
      </button>

      <input
        v-model="searchQuery"
        type="text"
        class="form-control w-50"
        placeholder="Search for products"
      />
    </div>

    <div v-if="filteredProducts.length">
      <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
        <div class="col" v-for="product in filteredProducts" :key="product.id">
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

    <div v-else>
      <p class="text-muted text-center">No products available.</p>
    </div>

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
      searchQuery: "", // Search query for filtering
    };
  },
  computed: {
    // Filter products based on the search query
    filteredProducts() {
      return this.products.filter(
        (product) =>
          product.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          product.description
            .toLowerCase()
            .includes(this.searchQuery.toLowerCase())
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
  color: #6b4f3b;
  font-size: 1.75rem;
  line-height: 1.4;
}

.custom-btn {
  font-family: "Montserrat", sans-serif;
  font-weight: bold;
  font-size: 1rem;
  background-color: #6b4f3b;
  color: white;
  border: 2px solid #6b4f3b;
  border-radius: 12px;
  padding: 10px 20px;
  transition: background-color 0.3s ease, transform 0.2s ease,
    box-shadow 0.3s ease;
}

.custom-btn:hover {
  background-color: #3c2f2f;
  border-color: #3c2f2f;
  transform: scale(1.07);
  box-shadow: 0 4px 12px rgba(76, 50, 36, 0.3);
  cursor: pointer;
}

.custom-btn:active {
  background-color: #2b1d17;
  border-color: #2b1d17;
}

.button-edit {
  font-family: "Montserrat", sans-serif;
  font-weight: 600;
  font-size: 1rem;
  color: #ffffff;
  background-color: #3b2a1f;
  border: 2px solid #6b4f3b;
  border-radius: 10px;
  padding: 3px 16px;
  transition: all 0.3s ease;
}

.btn-edit:hover {
  background-color: #6b4f3b;
  color: #fffaf6;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(107, 79, 59, 0.2);
}

.button-delete {
  font-family: "Montserrat", sans-serif;
  font-weight: 600;
  font-size: 1rem;
  color: #fffaf6;
  background-color: #7b3e2d;
  border: 2px solid #7b3e2d;
  border-radius: 10px;
  padding: 3.5px 16px;
  transition: all 0.3s ease;
}

.button-delete:hover {
  background-color: #4e1f15;
  border-color: #4e1f15;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(76, 37, 25, 0.3);
}

.custom-input {
  font-family: "Montserrat", sans-serif;
  font-weight: 500;
  font-size: 1rem;
  background-color: #fffaf6;
  border: 2px solid #bfa58d;
  border-radius: 8px;
  padding: 10px;
  color: #4e3629;
  transition: border-color 0.3s ease, background-color 0.3s ease,
    box-shadow 0.2s ease;
}

.custom-input:hover {
  border-color: #6b4f3b;
  box-shadow: 0 0 5px rgba(107, 79, 59, 0.25);
}

.custom-input:focus {
  outline: none;
  border-color: #6b4f3b;
  background-color: #f2e6d9;
  box-shadow: 0 0 8px rgba(107, 79, 59, 0.3);
}

.custom-input::placeholder {
  color: #4e3629;
}

.card {
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(107, 79, 59, 0.1);
  border: 2px solid #e5e0dc;
  background-color: #fffaf6;
  transition: box-shadow 0.3s ease, transform 0.3s ease, border-color 0.3s ease;
}

.card:hover {
  box-shadow: 0 6px 18px rgba(107, 79, 59, 0.25);
  border-color: #c7b6a3;
  transform: translateY(-6px);
}

.card-title {
  font-family: "Kalnia", serif;
  color: #6b4f3b;
  font-size: 1.25rem;
  font-weight: bold;
}

.card-text {
  font-family: "Montserrat", sans-serif;
  font-size: 1rem;
  color: #4e3629;
}

.modal-title {
  font-family: "Kalnia", serif;
  color: #6b4f3b;
  font-size: 1.5rem;
}

.modal-body {
  font-family: "Montserrat", sans-serif;
  font-size: 1rem;
  color: #3c2f2f;
}

.list-group-item {
  font-family: "Montserrat", sans-serif;
  background-color: transparent;
  border: none;
  color: #3c2f2f;
  padding-left: 0;
  transition: background-color 0.3s ease, font-weight 0.2s ease;
}

.list-group-item:hover {
  background-color: #e8dac7;
  font-weight: 600;
}

h2 {
  font-family: "Kalnia", serif;
  color: #6b4f3b;
  font-size: 2rem;
  font-weight: bold;
  transition: color 0.3s ease;
}

h2:hover {
  color: #3c2f2f;
}
</style>
