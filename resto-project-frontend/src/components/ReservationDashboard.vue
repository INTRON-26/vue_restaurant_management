<template>
  <div class="dashboard-page">
    <header class="dashboard-header">
      <h2>Reservation Dashboard</h2>
      <p class="subtitle">Manage all upcoming and recent reservations.</p>
    </header>

    <section class="dashboard-card">
      <div class="list-header">
        <h3>All Reservations</h3>
        <div class="toolbar">
          <select v-model="statusFilter" class="select-field">
            <option value="">All</option>
            <option value="pending">Pending</option>
            <option value="confirmed">Confirmed</option>
            <option value="cancelled">Cancelled</option>
          </select>
          <button class="outline-btn" v-on:click="fetchReservations">Refresh</button>
        </div>
      </div>

      <div v-if="loading" class="empty">Loading reservations...</div>
      <div v-else-if="filteredItems.length === 0" class="empty">No reservations found.</div>

      <div v-for="item in filteredItems" :key="item.id" class="reservation-item">
        <div class="item-grid">
          <div>
            <p class="label">Date</p>
            <p>{{ formatDate(item.reserved_for) }}</p>
          </div>
          <div>
            <p class="label">Party</p>
            <p>{{ item.party_size }} people</p>
          </div>
          <div>
            <p class="label">Status</p>
            <p class="status">{{ item.status }}</p>
          </div>
          <div>
            <p class="label">Guest</p>
            <p>{{ item.guest_name || 'Account user' }}</p>
          </div>
        </div>
        <div class="item-actions">
          <button class="outline-btn" v-on:click="updateStatus(item, 'confirmed')" :disabled="item.status === 'confirmed'">
            Approve
          </button>
          <button class="danger-btn" v-on:click="updateStatus(item, 'cancelled')" :disabled="item.status === 'cancelled'">
            Cancel
          </button>
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
  name: 'ReservationDashboard',
  data() {
    return {
      loading: false,
      message: '',
      error: '',
      items: [],
      statusFilter: ''
    };
  },
  computed: {
    filteredItems() {
      if (!this.statusFilter) {
        return this.items;
      }
      return this.items.filter(item => item.status === this.statusFilter);
    }
  },
  mounted() {
    this.fetchReservations();
  },
  methods: {
    async fetchReservations() {
      this.message = '';
      this.error = '';
      this.loading = true;
      try {
        const response = await api.get('/reservations/');
        this.items = response.data;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to load reservations.';
      } finally {
        this.loading = false;
      }
    },
    formatDate(value) {
      if (!value) return '';
      return new Date(value).toLocaleString();
    },
    async updateStatus(item, status) {
      this.message = '';
      this.error = '';
      try {
        const response = await api.patch(`/reservations/${item.id}/status`, { status });
        const index = this.items.findIndex(entry => entry.id === item.id);
        if (index !== -1) {
          this.$set(this.items, index, response.data);
        }
        this.message = `Reservation ${status}.`;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to update reservation.';
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

.dashboard-page {
  max-width: 900px;
  margin: 20px auto 60px;
  padding: 0 20px;
  color: #1f2a27;
}

.dashboard-header {
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

.dashboard-card {
  margin-top: 24px;
  padding: 20px;
  border-radius: 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  text-align: left;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.toolbar {
  display: flex;
  gap: 10px;
  align-items: center;
}

.select-field {
  height: 34px;
  border-radius: 6px;
  border: 1px solid var(--border);
  padding: 0 8px;
  color: #1f2a27;
}

.reservation-item {
  padding: 14px 16px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: #ffffff;
  margin-bottom: 12px;
}

.item-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.item-actions {
  display: flex;
  gap: 10px;
  margin-top: 12px;
}

.label {
  color: #6b7b76;
  font-weight: 600;
  margin-bottom: 4px;
}

.status {
  color: var(--primary);
  font-weight: 600;
}

.outline-btn {
  background: #ffffff;
  color: var(--primary);
  border: 1px solid var(--primary);
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
}

.danger-btn {
  background: #ffffff;
  color: #a60000;
  border: 1px solid #a60000;
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
  padding: 16px;
  background: var(--muted);
  border-radius: 10px;
  border: 1px dashed var(--border);
  color: #5a6b66;
}

@media (max-width: 820px) {
  .item-grid {
    grid-template-columns: 1fr 1fr;
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
}

@media (max-width: 520px) {
  .item-grid {
    grid-template-columns: 1fr;
  }

  .item-actions {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
