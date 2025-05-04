<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow custom-card">
          <div class="card-body">
            <h3 class="card-title text-center mb-4 custom-title">Login</h3>
            <form @submit.prevent="login">
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
                <label class="form-label custom-label">Password</label>
                <input
                  v-model="password"
                  type="password"
                  class="form-control custom-input"
                  required
                />
              </div>
              <button class="btn btn-primary w-100 custom-btn">Login</button>
              <div class="text-center mt-3">
                <router-link class="custom-link" to="/register">
                  Don't have an account? Register
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
import axios from "../axios"; // Assuming axios is configured to handle base URL and authentication headers
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const router = useRouter();

const login = async () => {
  try {
    // Send POST request to get the authentication token
    const res = await axios.post("/login/", {
      username: username.value,
      password: password.value,
    });

    // Store the token in localStorage
    localStorage.setItem("token", res.data.token);

    // Set the Authorization header for future requests
    axios.defaults.headers.common["Authorization"] = `Token ${res.data.token}`;

    // Get user details to determine user type (employee or customer)
    const userRes = await axios.get("/users/");
    localStorage.setItem("userType", userRes.data.user_type);

    // Redirect user based on their role (employee/customer)
    if (userRes.data.user_type === "employee") {
      router.push("/employee/products"); // Redirect employee to product management
    } else {
      router.push("/customer/products"); // Redirect customer to product listing
    }
  } catch (err) {
    alert("Invalid credentials or error during login.");
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

.custom-btn {
  background-color: #6b4f3b; /* Earthy brown */
  color: white;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.custom-btn:hover {
  background-color: #4e3629; /* Dark brown */
}

.custom-link {
  font-family: 'Montserrat', sans-serif;
  color: #6b4f3b;
  font-weight: bold;
  text-decoration: none;
}

.custom-link:hover {
  color: #4e3629;
}
</style>
