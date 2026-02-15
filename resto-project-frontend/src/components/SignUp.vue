<template>
    <div class="register">
        <img class="app-logo" src="../assets/logo.png" alt="Restaurant Logo">
        <h2>Create Account</h2>
        <input type="text" v-model="name" placeholder="Name" class="input-field" />
        <input type="email" v-model="email" placeholder="Email" class="input-field" />
        <input type="password" v-model="password" placeholder="Password" class="input-field" />
        <button v-on:click="signUp" class="submit-btn" :disabled="loading">
            {{ loading ? 'Creating account...' : 'Sign Up' }}
        </button>
        <p class="message" v-if="message">{{ message }}</p>
        <p class="error" v-if="error">{{ error }}</p>
        <p class="switch">
            Already have an account? <router-link to="/login">Log in</router-link>
        </p>
    </div>
</template>

<script>
import api from '../services/api';

export default {
    name: 'SignUp',
    data() {
        return {
            name: '',
            email: '',
            password: '',
            loading: false,
            message: '',
            error: ''
        }
    },
    methods: {
        async signUp() {
            this.message = '';
            this.error = '';
            this.loading = true;
            try {
                await api.post('/auth/signup', {
                    name: this.name,
                    email: this.email,
                    password: this.password
                });
                this.message = 'Account created. Please log in.';
                this.$router.push('/login');
            } catch (err) {
                this.error = err.response?.data?.detail || 'Signup failed.';
            } finally {
                this.loading = false;
            }
        }

    }
}
</script>
<style>
.register {
    /* Center the form on the page */
    margin-top: 50px;
    text-align: center;

}

.app-logo {
    width: 500px;
}

.input-field {
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-right: auto;
    margin-left: auto;
    border: 1px solid #225b48;
    border-radius: 4px;
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