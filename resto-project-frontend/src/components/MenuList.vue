<template>
  <div class="menu-page">
    <header class="menu-header">
      <h2>Menu</h2>
      <p class="subtitle">Browse available items.</p>
    </header>

    <section class="menu-list">
      <div class="list-header">
        <h3>Available Items</h3>
        <button class="outline-btn" v-on:click="fetchMenu">Refresh</button>
      </div>

      <div class="menu-grid">
        <div v-if="loading" class="empty">Loading menu...</div>
        <div v-else-if="items.length === 0" class="empty">No menu items found.</div>

        <div v-for="item in items" :key="item.id" class="menu-item">
          <img v-if="item.image_url" :src="imageUrl(item.image_url)" class="menu-image" alt="Menu item" />
          <div class="item-info">
            <div class="item-title">
              <h4>{{ item.name }}</h4>
              <span class="price">${{ item.price.toFixed(2) }}</span>
            </div>
            <p class="description">{{ item.description || 'No description available.' }}</p>
          </div>
        </div>
      </div>

      <p class="message" v-if="message">{{ message }}</p>
      <p class="error" v-if="error">{{ error }}</p>
    </section>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'MenuList',
  data() {
    return {
      items: [],
      loading: false,
      message: '',
      error: ''
    };
  },
  mounted() {
    this.fetchMenu();
  },
  methods: {
    async fetchMenu() {
      this.message = '';
      this.error = '';
      this.loading = true;
      try {
        const response = await api.get('/menu/');
        this.items = response.data.filter(item => item.is_available);
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to load menu.';
      } finally {
        this.loading = false;
      }
    },
    imageUrl(path) {
      if (!path) return '';
      const base = api.defaults.baseURL || '';
      return `${base.replace('/api/v1', '')}${path}`;
    }
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&display=swap');

:root {
  --primary: #225b48;
  --surface: #ffffff;
  --muted: #f4f7f6;
  --border: #dbe5e2;
  --shadow: 0 16px 32px rgba(34, 91, 72, 0.08);
}

.menu-page {
  max-width: 960px;
  margin: 20px auto 60px;
  padding: 0 20px;
  color: #1f2a27;
  font-family: 'Manrope', sans-serif;
}

.menu-header {
  background: linear-gradient(135deg, #ffffff 0%, #f4f7f6 100%);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid var(--border);
  text-align: left;
  box-shadow: var(--shadow);
}

.subtitle {
  margin-top: 6px;
  color: #4b5f59;
}

.menu-list {
  margin-top: 24px;
  text-align: left;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.menu-item {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 18px;
  padding: 18px;
  border: 1px solid rgba(34, 91, 72, 0.12);
  border-radius: 16px;
  background: var(--surface);
  box-shadow: var(--shadow);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.menu-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 40px rgba(34, 91, 72, 0.12);
}

.menu-image {
  width: 120px;
  height: 90px;
  object-fit: cover;
  border-radius: 14px;
  border: 1px solid rgba(34, 91, 72, 0.2);
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.price {
  color: var(--primary);
  font-weight: 700;
}

.description {
  color: #5a6b66;
}

.outline-btn {
  background: #ffffff;
  color: var(--primary);
  border: 1px solid var(--primary);
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
}

.message {
  margin-top: 12px;
  color: var(--primary);
}

.error {
  margin-top: 12px;
  color: #a60000;
}

.empty {
  padding: 20px;
  background: var(--muted);
  border-radius: 12px;
  border: 1px dashed var(--border);
  color: #5a6b66;
}

@media (max-width: 720px) {
  .menu-grid {
    grid-template-columns: 1fr;
  }

  .menu-item {
    grid-template-columns: 1fr;
  }

  .menu-image {
    width: 100%;
    height: 190px;
  }
}
</style>
