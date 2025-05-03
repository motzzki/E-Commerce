<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">Register</h3>
            <form @submit.prevent="register">
              <div class="mb-3">
                <label class="form-label">Username</label>
                <input
                  v-model="username"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input
                  v-model="email"
                  type="email"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Password</label>
                <input
                  v-model="password"
                  type="password"
                  class="form-control"
                  required
                />
              </div>
              <button class="btn btn-success w-100">Register</button>
              <div class="text-center mt-3">
                <router-link to="/login"
                  >Already have an account? Login</router-link
                >
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "../axios.js"; // Make sure axios is configured correctly
import { useRouter } from "vue-router";

const username = ref("");
const email = ref("");
const password = ref("");
const user_type = ref("customer"); // You can change this to employee if needed
const router = useRouter();

const register = async () => {
  try {
    await axios.post("/register/", {
      username: username.value,
      email: email.value,
      password: password.value,
      user_type: user_type.value,
    });
    router.push("/login"); // Redirect to login after successful registration
  } catch (err) {
    alert("Registration failed");
  }
};
</script>
