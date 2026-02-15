<template>
  <div class="reservation-page">
    <header class="reservation-header">
      <h2>Book a Reservation</h2>
      <p class="subtitle">Reserve your table in a few quick steps.</p>
    </header>

    <section class="reservation-card">
      <div class="form-grid">
        <input v-model.number="form.partySize" type="number" min="1" placeholder="Party size" class="input-field" />
        <input v-model="form.dateTime" type="datetime-local" class="input-field" />
      </div>

      <div v-if="!isAuthenticated" class="guest-info">
        <h3>Guest Details</h3>
        <div class="form-grid">
          <input v-model="form.guestName" type="text" placeholder="Guest name" class="input-field" />
          <input v-model="form.guestEmail" type="email" placeholder="Guest email" class="input-field" />
          <input v-model="form.guestPhone" type="text" placeholder="Guest phone" class="input-field full" />
        </div>
      </div>

      <button class="submit-btn" v-on:click="submitReservation" :disabled="loading">
        {{ loading ? 'Submitting...' : 'Book Reservation' }}
      </button>
      <p class="message" v-if="message">{{ message }}</p>
      <p class="error" v-if="error">{{ error }}</p>
    </section>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'ReservationForm',
  data() {
    return {
      loading: false,
      message: '',
      error: '',
      form: {
        partySize: 2,
        dateTime: '',
        guestName: '',
        guestEmail: '',
        guestPhone: ''
      }
    };
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('accessToken');
    }
  },
  methods: {
    async submitReservation() {
      this.message = '';
      this.error = '';

      if (!this.form.partySize || this.form.partySize < 1) {
        this.error = 'Please enter a valid party size.';
        return;
      }

      if (!this.form.dateTime) {
        this.error = 'Please select a reservation date and time.';
        return;
      }

      if (!this.isAuthenticated) {
        if (!this.form.guestName || !this.form.guestEmail) {
          this.error = 'Guest name and email are required.';
          return;
        }
      }

      this.loading = true;
      try {
        const payload = {
          party_size: this.form.partySize,
          reserved_for: new Date(this.form.dateTime).toISOString()
        };

        if (!this.isAuthenticated) {
          payload.guest_name = this.form.guestName;
          payload.guest_email = this.form.guestEmail;
          payload.guest_phone = this.form.guestPhone;
        }

        await api.post('/reservations/', payload);
        this.message = 'Reservation booked successfully.';
        this.form = {
          partySize: 2,
          dateTime: '',
          guestName: '',
          guestEmail: '',
          guestPhone: ''
        };
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to book reservation.';
      } finally {
        this.loading = false;
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

.reservation-page {
  max-width: 860px;
  margin: 20px auto 60px;
  padding: 0 20px;
  color: #1f2a27;
}

.reservation-header {
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

.reservation-card {
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

.input-field {
  width: 100%;
  height: 38px;
  padding-left: 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
}

.submit-btn {
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  border: 1px solid var(--primary);
  background: var(--primary);
  color: #ffffff;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.guest-info {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

.message {
  margin-top: 12px;
  color: var(--primary);
}

.error {
  margin-top: 12px;
  color: #a60000;
}

@media (max-width: 720px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-grid .full {
    grid-column: span 1;
  }
}
</style>
