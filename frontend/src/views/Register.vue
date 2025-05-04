<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow custom-card">
          <div class="card-body">
            <h3 class="card-title text-center mb-4 custom-title">Register</h3>
            <form @submit.prevent="register">
              <div class="mb-3">
                <label class="form-label custom-label">Username</label>
                <input
                  v-model="username"
                  type="text"
                  class="form-control custom-input"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label custom-label">Email</label>
                <input
                  v-model="email"
                  type="email"
                  class="form-control custom-input"
                  required
                />
              </div>
              <div class="mb-3 position-relative">
                <label class="form-label custom-label">Password</label>
                <div class="input-group">
                  <input
                    v-model="password"
                    :type="showPassword ? 'text' : 'password'"
                    class="form-control custom-input"
                    required
                  />
                  <button
                    class="btn btn-outline-secondary custom-btn"
                    type="button"
                    @click="showPassword = !showPassword"
                  >
                    {{ showPassword ? 'Hide' : 'Show' }}
                  </button>
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label custom-label d-block">User Type</label>
                <div class="form-check form-check-inline">
                  <input
                    class="form-check-input"
                    type="radio"
                    id="customer"
                    value="customer"
                    v-model="user_type"
                  />
                  <label class="form-check-label" for="customer">Customer</label>
                </div>
                <div class="form-check form-check-inline">
                  <input
                    class="form-check-input"
                    type="radio"
                    id="employee"
                    value="employee"
                    v-model="user_type"
                  />
                  <label class="form-check-label" for="employee">Employee</label>
                </div>
              </div>

              <button class="btn btn-success w-100 custom-btn">Register</button>
              <div class="text-center mt-3">
                <router-link class="custom-link" to="/login">
                  Already have an account? Login
                </router-link>
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
import axios from "../axios.js";
import { useRouter } from "vue-router";

const username = ref("");
const email = ref("");
const password = ref("");
const showPassword = ref(false);
const user_type = ref("customer"); // default selection

const router = useRouter();

const register = async () => {
  try {
    await axios.post("/register/", {
      username: username.value,
      email: email.value,
      password: password.value,
      user_type: user_type.value,
    });
    router.push("/login");
  } catch (err) {
    alert("Registration failed");
  }
};
</script>

<style scoped>
.custom-card {
  background-color: #f5f5f5;
  border-color: #6b4f3b; /* Earthy brown */
}

.custom-title {
  font-family: 'Kalnia', sans-serif;
  font-weight: bold;
  color: #6b4f3b;
}

.custom-label {
  font-family: 'Montserrat', sans-serif;
  font-weight: bold;
  color: #4e3629; /* Dark brown */
}

.custom-input {
  border-color: #bfa58d; /* Lighter brown */
}

/* Custom Button */
.custom-btn {
  background-color: #6b4f3b; /* Earthy brown */
  color: white;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.custom-btn:hover {
  background-color: #4e3629; /* Dark brown */
}

/* Custom Link */
.custom-link {
  font-family: 'Montserrat', sans-serif;
  color: #6b4f3b;
  font-weight: bold;
  text-decoration: none;
}

.custom-link:hover {
  color: #4e3629;
}

/* Custom Radio Button */
input[type="radio"] {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid #6b4f3b; /* Earthy brown border */
  background-color: #fffaf6; /* Light earthy tone */
  position: relative;
  cursor: pointer;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

input[type="radio"]:checked {
  background-color: #6b4f3b; /* Earthy brown */
  border-color: #6b4f3b; /* Darker brown border on checked */
}

input[type="radio"]:checked::after {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: white;
}

input[type="radio"]:focus {
  outline: none;
  border-color: #4e3629; /* Darker brown on focus */
}

input[type="radio"]:disabled {
  background-color: #e5e0dc; /* Disabled state with a muted color */
  border-color: #bfa58d; /* Lighter earthy brown */
  cursor: not-allowed;
}
</style>

