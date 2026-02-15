<template>
  <div class="auth-card">
    <img class="app-logo" src="../assets/logo.png" alt="Restaurant Logo" />
    <h2>Log In</h2>
    <input type="email" v-model="email" placeholder="Email" class="input-field" />
    <input type="password" v-model="password" placeholder="Password" class="input-field" />
    <button v-on:click="login" class="submit-btn" :disabled="loading">
      {{ loading ? 'Signing in...' : 'Log In' }}
    </button>
    <p class="message" v-if="message">{{ message }}</p>
    <p class="error" v-if="error">{{ error }}</p>
    <p class="switch">
      New here? <router-link to="/signup">Create an account</router-link>
    </p>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      message: '',
      error: ''
    };
  },
  methods: {
    async login() {
      this.message = '';
      this.error = '';
      this.loading = true;
      try {
        const response = await api.post('/auth/login', {
          email: this.email,
          password: this.password
        });
        localStorage.setItem('accessToken', response.data.access_token);
        const me = await api.get('/auth/me');
        localStorage.setItem('userRole', me.data.role);
        this.message = 'Logged in successfully.';
        this.$router.push('/');
      } catch (err) {
        this.error = err.response?.data?.detail || 'Login failed.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style>
.auth-card {
  margin-top: 40px;
  width: 20%;
  text-align: center;
  /* Center the form on the page */
  margin-left: auto;
    margin-right: auto; 
}

.app-logo {
  width: 500px;
}

.input-field {
  width: min(300px, 85%);
  height: 42px;
  padding: 0 16px;
  display: block;
  margin-bottom: 18px;
  margin-right: auto;
  margin-left: auto;
  border: 1px solid #dbe5e2;
  border-radius: 10px;
  background: #ffffff;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.input-field:focus {
  outline: none;
  border-color: #225b48;
  box-shadow: 0 0 0 3px rgba(34, 91, 72, 0.12);
}

.submit-btn {
  width: 320px;
  height: 40px;
  border: 1px solid #225b48;
  background: #225b48;
  color: #ffffff;
  cursor: pointer;
  border-radius: 4px;
  font-size: 16px;
  transition: background 0.3s ease;
}

.submit-btn:hover {
  background: #ffffff;
  color: #225b48;
  border: 2px solid #225b48;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.message {
  margin-top: 12px;
  color: #225b48;
}

.error {
  margin-top: 12px;
  color: #a60000;
}

.switch {
  margin-top: 16px;
}
</style>
