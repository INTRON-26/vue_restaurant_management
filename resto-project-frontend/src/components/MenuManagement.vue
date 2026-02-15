<template>
  <div class="menu-page">
    <header class="menu-header">
      <h2>Menu Management</h2>
      <p class="subtitle">Add, update, or remove menu items.</p>
    </header>

    <section class="menu-card">
      <h3>New Item</h3>
      <div class="form-grid">
        <input v-model="form.name" type="text" placeholder="Name" class="input-field" />
        <input v-model.number="form.price" type="number" min="0" step="0.01" placeholder="Price" class="input-field" />
        <input v-model="form.description" type="text" placeholder="Description" class="input-field full" />
        <div class="upload-row full">
          <input type="file" accept="image/*" v-on:change="handleNewImage" />
          <img v-if="form.image_url" :src="imageUrl(form.image_url)" class="preview" alt="Preview" />
        </div>
        <label class="checkbox">
          <input v-model="form.is_available" type="checkbox" />
          Available
        </label>
      </div>
      <button class="submit-btn" v-on:click="createItem" :disabled="loading">
        {{ loading ? 'Saving...' : 'Add Item' }}
      </button>
      <p class="message" v-if="message">{{ message }}</p>
      <p class="error" v-if="error">{{ error }}</p>
    </section>

    <section class="menu-list">
      <div class="list-header">
        <h3>Current Menu</h3>
        <button class="outline-btn" v-on:click="fetchMenu">Refresh</button>
      </div>

      <div v-if="items.length === 0" class="empty">No menu items found.</div>

      <div v-for="item in items" :key="item.id" class="menu-item">
        <div class="item-info">
          <input v-model="item.name" class="input-field" />
          <input v-model.number="item.price" type="number" min="0" step="0.01" class="input-field" />
          <input v-model="item.description" class="input-field" />
          <div class="upload-row">
            <input type="file" accept="image/*" v-on:change="handleExistingImage($event, item)" />
            <img v-if="item.image_url" :src="imageUrl(item.image_url)" class="preview" alt="Preview" />
          </div>
        </div>
        <div class="item-actions">
          <label class="checkbox">
            <input v-model="item.is_available" type="checkbox" />
            Available
          </label>
          <button class="submit-btn" v-on:click="updateItem(item)">Update</button>
          <button class="danger-btn" v-on:click="deleteItem(item)">Delete</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'MenuManagement',
  data() {
    return {
      items: [],
      loading: false,
      message: '',
      error: '',
      form: {
        name: '',
        description: '',
        price: null,
        image_url: '',
        is_available: true
      }
    };
  },
  mounted() {
    this.fetchMenu();
  },
  methods: {
    async fetchMenu() {
      this.message = '';
      this.error = '';
      try {
        const response = await api.get('/menu/');
        this.items = response.data;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to load menu.';
      }
    },
    async createItem() {
      this.message = '';
      this.error = '';
      this.loading = true;
      try {
        const payload = {
          name: this.form.name,
          description: this.form.description,
          price: this.form.price,
          image_url: this.form.image_url,
          is_available: this.form.is_available
        };
        const response = await api.post('/menu/', payload);
        this.items.unshift(response.data);
        this.form = { name: '', description: '', price: null, image_url: '', is_available: true };
        this.message = 'Menu item added.';
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to add item.';
      } finally {
        this.loading = false;
      }
    },
    async updateItem(item) {
      this.message = '';
      this.error = '';
      try {
        await api.put(`/menu/${item.id}`, {
          name: item.name,
          description: item.description,
          price: item.price,
          image_url: item.image_url,
          is_available: item.is_available
        });
        this.message = 'Menu item updated.';
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to update item.';
      }
    },
    async deleteItem(item) {
      this.message = '';
      this.error = '';
      try {
        await api.delete(`/menu/${item.id}`);
        this.items = this.items.filter(entry => entry.id !== item.id);
        this.message = 'Menu item deleted.';
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to delete item.';
      }
    },
    imageUrl(path) {
      if (!path) return '';
      const base = api.defaults.baseURL || '';
      return `${base.replace('/api/v1', '')}${path}`;
    },
    async handleNewImage(event) {
      const file = event.target.files?.[0];
      if (!file) return;
      const url = await this.uploadImage(file);
      if (url) {
        this.form.image_url = url;
      }
    },
    async handleExistingImage(event, item) {
      const file = event.target.files?.[0];
      if (!file) return;
      const url = await this.uploadImage(file);
      if (url) {
        this.$set(item, 'image_url', url);
      }
    },
    async uploadImage(file) {
      this.message = '';
      this.error = '';
      try {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post('/menu/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data.url;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to upload image.';
        return '';
      }
    }
  }
};
</script>

<style>
:root {
  --primary: #225b48;
  --surface: #ffffff;
  --muted: #f4f7f6;
  --border: #dbe5e2;
}

.menu-page {
  max-width: 960px;
  margin: 20px auto 60px;
  padding: 0 20px;
  color: #1f2a27;
}

.menu-header {
  background: var(--muted);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid var(--border);
  text-align: left;
}

.subtitle {
  margin-top: 6px;
  color: #4b5f59;
}

.menu-card {
  margin-top: 24px;
  padding: 20px;
  border-radius: 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  text-align: left;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 12px;
}

.form-grid .full {
  grid-column: span 2;
}

.menu-list {
  margin-top: 28px;
  text-align: left;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.menu-item {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
  padding: 16px;
  margin-bottom: 12px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--surface);
}

.item-info {
  display: grid;
  gap: 8px;
}

.upload-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.preview {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid var(--border);
}

.item-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-start;
}

.input-field {
  width: 100%;
  height: 38px;
  padding-left: 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
}

.submit-btn,
.outline-btn,
.danger-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  border: 1px solid var(--primary);
}

.submit-btn {
  background: var(--primary);
  color: #ffffff;
}

.outline-btn {
  background: #ffffff;
  color: var(--primary);
}

.danger-btn {
  background: #ffffff;
  color: #a60000;
  border-color: #a60000;
}

.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #4b5f59;
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
  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-grid .full {
    grid-column: span 1;
  }

  .menu-item {
    grid-template-columns: 1fr;
  }
}
</style>
