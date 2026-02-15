<template>
  <div id="app">
    <nav class="nav">
      <div class="nav-inner">
        <div class="brand">CHEFSTACK</div>
        <div class="nav-links">
          <router-link class="nav-link" to="/">Home</router-link>
          <router-link class="nav-link" to="/menu">Menu</router-link>
          <router-link class="nav-link" to="/reservations">Reservations</router-link>
          <router-link v-if="isAuthenticated" class="nav-link" to="/my-reservations">My Reservations</router-link>
          <router-link v-if="isStaffOrAdmin" class="nav-link" to="/reservation-dashboard">Dashboard</router-link>
          <router-link v-if="isStaffOrAdmin" class="nav-link" to="/menu-management">Manage Menu</router-link>
          <router-link class="nav-link" to="/signup">Sign Up</router-link>
          <router-link class="nav-link" to="/login">Log In</router-link>
          <button v-if="isAuthenticated" class="nav-button" v-on:click="logout">Log Out</button>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      hasToken: false,
      userRole: ''
    };
  },
  computed: {
    isAuthenticated() {
      return this.hasToken;
    },
    isStaffOrAdmin() {
      return this.hasToken && ['admin', 'staff'].includes(this.userRole);
    }
  },
  created() {
    this.loadAuthState();
  },
  watch: {
    $route() {
      this.loadAuthState();
    }
  },
  methods: {
    loadAuthState() {
      this.hasToken = !!localStorage.getItem('accessToken');
      this.userRole = localStorage.getItem('userRole') || '';
    },
    logout() {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('userRole');
      this.loadAuthState();
      this.$router.push('/');
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700&display=swap');

#app {
  font-family: 'Manrope', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #1f2a27;
  margin-top: 90px;
  min-height: 100vh;
  background: linear-gradient(180deg, #ffffff 0%, #f4f7f6 100%);
}

.nav {
  position: sticky;
  top: 16px;
  z-index: 10;
  margin: 0 auto 32px;
  max-width: 1040px;
  padding: 10px 18px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(34, 91, 72, 0.18);
  border-radius: 999px;
  box-shadow: 0 20px 40px rgba(34, 91, 72, 0.12);
  backdrop-filter: blur(12px);
}

.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.brand {
  font-weight: 700;
  letter-spacing: 0.18em;
  color: #225b48;
  padding: 6px 12px;
  background: rgba(34, 91, 72, 0.1);
  border-radius: 999px;
  font-size: 12px;
}

.nav-links {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.nav-link {
  color: #225b48;
  text-decoration: none;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 999px;
  transition: background 0.2s ease, color 0.2s ease, transform 0.2s ease;
  background: rgba(34, 91, 72, 0.08);
}

.nav-link.router-link-exact-active {
  background: #225b48;
  color: #ffffff;
}

.nav-button {
  border: 1px solid #225b48;
  background: #225b48;
  color: #ffffff;
  border-radius: 999px;
  padding: 6px 16px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.nav-link:hover,
.nav-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 16px rgba(34, 91, 72, 0.12);
}

@media (max-width: 720px) {
  .nav {
    border-radius: 22px;
    padding: 12px 16px;
  }

  .nav-inner {
    justify-content: center;
  }

  .brand {
    order: -1;
  }
}
</style>
