<template>
  <div class="reservations-page">
    <header class="reservations-header">
      <h2>My Reservations</h2>
      <p class="subtitle">Your upcoming and recent bookings.</p>
    </header>

    <section class="reservations-card">
      <div class="list-header">
        <h3>Reservations</h3>
        <button class="outline-btn" v-on:click="fetchReservations">Refresh</button>
      </div>

      <div v-if="loading" class="empty">Loading reservations...</div>
      <div v-else-if="items.length === 0" class="empty">No reservations found.</div>

      <div v-for="item in items" :key="item.id" class="reservation-item">
        <div class="item-row">
          <span class="label">Date</span>
          <span>{{ formatDate(item.reserved_for) }}</span>
        </div>
        <div class="item-row">
          <span class="label">Party</span>
          <span>{{ item.party_size }} people</span>
        </div>
        <div class="item-row">
          <span class="label">Status</span>
          <span class="status">{{ item.status }}</span>
        </div>
        <div class="item-actions">
          <button
            class="danger-btn"
            v-on:click="openCancelModal(item)"
            :disabled="item.status === 'cancelled'"
          >
            {{ item.status === 'cancelled' ? 'Cancelled' : 'Cancel' }}
          </button>
        </div>
      </div>

      <p class="message" v-if="message">{{ message }}</p>
      <p class="error" v-if="error">{{ error }}</p>
    </section>

    <div v-if="showCancelModal" class="modal-backdrop" v-on:click.self="closeCancelModal">
      <div class="modal-card">
        <h3>Cancel reservation?</h3>
        <p>This action cannot be undone.</p>
        <div class="modal-actions">
          <button class="outline-btn" v-on:click="closeCancelModal">Keep</button>
          <button class="danger-btn" v-on:click="confirmCancel" :disabled="cancelLoading">
            {{ cancelLoading ? 'Cancelling...' : 'Cancel reservation' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'MyReservations',
  data() {
    return {
      loading: false,
      message: '',
      error: '',
      items: [],
      showCancelModal: false,
      cancelLoading: false,
      selectedReservation: null
    };
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
        const response = await api.get('/reservations/me');
        this.items = response.data;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to load reservations.';
      } finally {
        this.loading = false;
      }
    },
    formatDate(value) {
      if (!value) return '';
      const date = new Date(value);
      return date.toLocaleString();
    },
    openCancelModal(item) {
      if (item.status === 'cancelled') {
        return;
      }
      this.selectedReservation = item;
      this.showCancelModal = true;
    },
    closeCancelModal() {
      this.showCancelModal = false;
      this.selectedReservation = null;
    },
    async confirmCancel() {
      if (!this.selectedReservation) {
        return;
      }
      this.message = '';
      this.error = '';
      this.cancelLoading = true;
      try {
        const response = await api.patch(`/reservations/${this.selectedReservation.id}/cancel`);
        const index = this.items.findIndex(entry => entry.id === this.selectedReservation.id);
        if (index !== -1) {
          this.$set(this.items, index, response.data);
        }
        this.message = 'Reservation cancelled.';
        this.closeCancelModal();
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to cancel reservation.';
      } finally {
        this.cancelLoading = false;
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

.reservations-page {
  max-width: 860px;
  margin: 20px auto 60px;
  padding: 0 20px;
  color: #1f2a27;
}

.reservations-header {
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

.reservations-card {
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

.reservation-item {
  padding: 14px 16px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: #ffffff;
  margin-bottom: 12px;
}

.item-actions {
  margin-top: 10px;
}

.item-row {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
}

.label {
  color: #6b7b76;
  font-weight: 600;
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

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  width: 100%;
  max-width: 360px;
  text-align: left;
  border: 1px solid var(--border);
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 16px;
  justify-content: flex-end;
}
</style>
