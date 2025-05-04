<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm mb-4">
    <div class="container">
      <span class="navbar-brand">Glam Shop</span>

      <div class="collapse navbar-collapse">
        <ul class="navbar-nav ms-auto">
          <!-- Employee Links -->
          <template v-if="isCustomer">
            <li class="nav-item">
              <router-link class="nav-link" to="/customer/products"
                >Products</router-link
              >
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/customer/cart"
                >Cart</router-link
              >
            </li>
          </template>

          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="confirmLogout"
              >Logout</a
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import Swal from "sweetalert2";

const router = useRouter();

// Computed properties for login state and user type
const isLoggedIn = computed(() => !!localStorage.getItem("token"));
const userType = computed(() => localStorage.getItem("userType"));

const isCustomer = computed(
  () => isLoggedIn.value && userType.value === "customer"
);

// Logout logic with SweetAlert2 confirmation
const confirmLogout = () => {
  Swal.fire({
    title: "Are you sure?",
    text: "Do you want to log out?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, log out",
    cancelButtonText: "Cancel",
  }).then((result) => {
    if (result.isConfirmed) {
      logout();
    }
  });
};

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("userType");
  router.push("/login");
};
</script>

<style scoped>
.navbar-brand {
  font-weight: bold;
}
</style>
