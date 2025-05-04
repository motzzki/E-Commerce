
  <CustomerNav />
  <div class="container mt-4">
    <router-link to="/customer/products" class="btn btn-secondary mb-3">
      ← Back to Products
    </router-link>

    <h2 class="checkout-title">Checkout</h2>
    <p class="total-amount">Total amount: ${{ total }}</p>

    <form @submit.prevent="submitOrder" class="checkout-form">
      <div class="mb-3">
        <label for="address" class="form-label">Shipping Address</label>
        <input v-model="address" id="address" class="form-control" required />
      </div>
      <button type="submit" class="btn custom-btn">Place Order</button>
    </form>
  </div>
</template>

<script>
import axios from "../../axios";
import CustomerNav from "./CustomerNav.vue";

export default {
  components: {
    CustomerNav,
  },
  data() {
    return {
      cart: [],
      address: "",
      customerId: null,
    };
  },
  computed: {
    total() {
      return this.cart
        .reduce((sum, item) => sum + parseFloat(item.price) * item.quantity, 0)
        .toFixed(2);
    },
  },
  methods: {
    submitOrder() {
      if (this.cart.length === 0) {
        alert("Your cart is empty. Please add items before placing an order.");
        return;
      }

      const orderData = {
        customer: this.customerId,
        write_items: this.cart.map((item) => ({
          product: item.id,
          quantity: item.quantity,
        })),
      };

      axios
        .post("orders/", orderData)
        .then(() => {
          alert("Order placed successfully!");
          localStorage.removeItem("cart");
          this.$router.push("/customer/products");
        })
        .catch((err) => {
          console.error(err);
          alert("Something went wrong");
        });
    },
    getUserInfo() {
      axios
        .get("/users/")
        .then((res) => {
          this.customerId = res.data.customerId;
        })
        .catch(() => {
          alert("Could not get user info");
        });
    },
  },
  mounted() {
    this.cart = JSON.parse(localStorage.getItem("cart") || "[]");
    this.getUserInfo();
  },
};
</script>

<style scoped>
/* Checkout Title */
.checkout-title {
  font-family: "Kalnia", serif;
  color: #6b4f3b; /* Earthy brown */
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 20px;
}

/* Total Amount */
.total-amount {
  font-family: "Montserrat", sans-serif;
  color: #4e3629; /* Dark brown */
  font-size: 1.25rem;
  margin-bottom: 30px;
}

/* Form Styles */
.checkout-form {
  background-color: #fffaf6; /* Light earthy tone */
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(107, 79, 59, 0.1); /* Earthy brown shadow */
  padding: 20px;
  margin-bottom: 30px;
}

.checkout-form .form-label {
  font-family: "Montserrat", sans-serif;
  color: #6b4f3b; /* Earthy brown */
  font-weight: 600;
}

.checkout-form .form-control {
  font-family: "Montserrat", sans-serif;
  background-color: #fffaf6;
  border: 1px solid #bfa58d; /* Lighter earthy brown border */
  color: #4e3629; /* Dark brown text */
  padding: 8px;
  border-radius: 8px;
}

.checkout-form .form-control:focus {
  outline: none;
  border-color: #6b4f3b; /* Earthy brown focus border */
  background-color: #f2e6d9; /* Lighter brown on focus */
}

/* Custom Button */
.custom-btn {
  background-color: #6b4f3b; /* Earthy brown */
  color: white;
  font-weight: bold;
  border-radius: 12px;
  transition: background-color 0.3s ease;
}

.custom-btn:hover {
  background-color: #4e3629; /* Darker brown on hover */
  color: white;
}

/* Back Button */
.btn-secondary {
  background-color: #e5e0dc; /* Lighter brown */
  border-color: #6b4f3b; /* Earthy brown border */
  color: #6b4f3b; /* Earthy brown text */
  font-family: "Montserrat", sans-serif;
  font-weight: 600;
  margin-bottom: 20px;
  padding: 8px 16px;
  border-radius: 12px;
  transition: background-color 0.3s ease;
}

.btn-secondary:hover {
  background-color: #6b4f3b; /* Darker earthy brown on hover */
  color: white;
}
</style>
