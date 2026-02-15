<template>
  <div id="app">
    <nav class="nav">
      <router-link class="nav-link" to="/">Home</router-link>
      <router-link class="nav-link" to="/signup">Sign Up</router-link>
      <router-link class="nav-link" to="/login">Log In</router-link>
      <button v-if="isAuthenticated" class="nav-button" v-on:click="logout">Log Out</button>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('accessToken');
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('accessToken');
      this.$router.push('/');
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.nav {
  display: flex;
  gap: 16px;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.nav-link {
  color: #225b48;
  text-decoration: none;
  font-weight: 600;
}

.nav-link.router-link-exact-active {
  text-decoration: underline;
}

.nav-button {
  border: 1px solid #225b48;
  background: #225b48;
  color: #ffffff;
  border-radius: 4px;
  padding: 6px 12px;
  cursor: pointer;
}
</style>
