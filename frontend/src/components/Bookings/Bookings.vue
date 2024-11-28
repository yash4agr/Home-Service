<script setup>
import { ref, computed, watch } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'

const store = useStore()
const router = useRouter()
const route = useRoute()

const props = defineProps({
  isBookingsOpen: {
    type: Boolean,
    required: true,
  }
})

const emit = defineEmits(['update:isBookingsOpen'])

// Bookings data from store
const bookings = computed(() => store.getters['module2/bookingsItems'])
const reviewData = ref({
  rating: 1,
  comment: ''
})

// Review modal state
const isReviewModalOpen = ref(false)
const currentBooking = ref(null)

const toggleBookings = () => {
  if (!props.isBookingsOpen) {
    router.push({ 
      query: { 
        ...router.currentRoute.value.query, 
        bookings: 'true' 
      }
    });
  } else {
    const query = { ...router.currentRoute.value.query };
    delete query.bookings;
    router.push({
      path: router.currentRoute.value.path,
      query,
      hash: router.currentRoute.value.hash,
    });
  }
  emit('update:isBookingsOpen', !props.isBookingsOpen)
}

// Cancel booking
const cancelBooking = (bookingId) => {
  store.dispatch('module2/cancelBooking', bookingId)
}

// Close booking
const closeBooking = (bookingId) => {
  store.dispatch('module2/closeBooking', bookingId)
}

// Open review modal
const openReviewModal = (booking) => {
  currentBooking.value = booking
  reviewData.value = {
    rating: booking.review_details.rating || 1,
    comment: booking.review_details.review || ''
  }
  isReviewModalOpen.value = true
}

// Submit review
const submitReview = (reviewData) => {
  store.dispatch('module2/submitReview', {
    bookingId: currentBooking.value.id,
    ...reviewData
  })
  isReviewModalOpen.value = false
}

// Professional service actions
const acceptService = (serviceId) => {
  store.dispatch('module2/acceptService', serviceId)
}

const rejectService = (serviceId) => {
  store.dispatch('module2/rejectService', serviceId)
}

watch (
  () => route.query.bookings,
  (newValue) => {
    if (newValue === "true") {
      store.dispatch('module2/fetchBookings')
      toggleBookings();
    }
  }
)

// Determine if review is readonly based on user role
const isReviewReadOnly = computed(() => 
  store.getters['module1/userRole'] === 'professional'
)
</script>

<template>
  <div class="bookings-container">
    <button @click="toggleBookings" class="nav-icon" aria-label="Bookings">
      <i class="ri-calendar-line" aria-hidden="true"></i>
    </button>

    <Transition name="fade">
      <div v-if="isBookingsOpen" class="bookings-overlay" @click.self="toggleBookings">
        <div class="bookings-dialog">
          <div class="bookings-header">
            <h2 class="bookings-title">My Bookings</h2>
            <button class="bookings-close" @click="toggleBookings">
              <i class="ri-close-line" />
            </button>
          </div>

          <div class="bookings-content">
            <div v-if="bookings.length === 0" class="bookings-empty">
              <i class="ri-file-list-line bookings-empty-icon"></i>
              <p>No bookings found</p>
            </div>
            
            <div v-else class="bookings-list">
              <div v-for="booking in bookings" :key="booking.id" class="booking-item">
                <img :src="booking.service?.img" :alt="booking.service.name" class="booking-item-image">
                
                <div class="booking-item-details">
                  <div class="booking-item-header">
                    <div class="booking-item-text">
                      <h3 class="booking-item-title">{{ booking.service.name }} (₹{{ booking.total_amount? booking.total_amount : booking.service.base_price+"/hr" }})</h3>
                      <template v-if="store.getters['module1/userRole'] === 'user'"> 
                        <template v-if="booking.status !== 'pending'"> 
                          <p class="booking-professional">Professional: {{ booking.professional_details?.name || "NA"}}</p>
                          <p class="booking-professional">Request time: {{ booking.date_of_request.toLocaleString('en-US', { timeZone: 'Asia/Kolkata' })|| "NA"}}</p>
                          <p class="booking-hours">Contact: {{ booking.professional_details?.phone }}</p>
                        </template>
                          <p class="booking-status" :class="booking.status.toLowerCase()">
                            Status: {{ booking.status }}
                          </p>
                      </template>
                      <template v-else> 
                        <p class="booking-professional"> Customer: {{ booking.customer_details?.name || "NA"}}</p>
                          <p class="booking-hours"> Contact: {{ booking.customer_details?.phone }}</p>
                          <p class="booking-status"> Address: {{ booking.address.street + " , "+ booking.address.city }} 
                          </p>
                      </template>
                    </div>
                    <div class="booking-actions">
                      <!-- User Actions -->
                      <template v-if="store.getters['module1/userRole'] === 'user'">
                        <button 
                          v-if="booking.status === 'pending'" 
                          class="cancel-btn" 
                          @click="cancelBooking(booking.id)"
                        >
                          Cancel Booking
                        </button>
                        <button 
                          v-if="booking.status === 'accepted'" 
                          class="close-btn" 
                          @click="closeBooking(booking.id)"
                        >
                          Close Booking
                        </button>
                        <button 
                          v-if="booking.status === 'completed'" 
                          class="review-btn" 
                          @click="openReviewModal(booking)"
                        >
                          Submit Review
                        </button>
                      </template>

                      <!-- Professional Actions -->
                      <template v-if="store.getters['module1/userRole'] === 'professional'">
                        <template v-if="booking.status === 'pending'">
                          <button 
                            class="accept-btn" 
                            @click="acceptService(booking.service.id)"
                          >
                            Accept
                          </button>
                          <button 
                            class="reject-btn" 
                            @click="rejectService(booking.service.id)"
                          >
                            Reject
                          </button>
                        </template>
                        <template v-if="booking.status === 'accepted'">
                          <button 
                            class="close-btn" 
                            @click="closeBooking(booking.id)"
                          >
                            Close Booking
                          </button>
                          <button 
                            class="cancel-btn" 
                            @click="cancelBooking(booking.id)"
                          >
                            Cancel Booking
                          </button>
                        </template>
                        <template v-if="booking.status === 'completed'">
                          <button 
                            class="review-btn" 
                            @click="openReviewModal(booking)"
                          >
                            View Review
                          </button>
                        </template>
                      </template>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Review Modal -->
    <div v-if="isReviewModalOpen" class="review-modal">
      <div class="review-modal-content">
        <h3>Submit Review for {{ currentBooking.service.name }}</h3>
        <form @submit.prevent="submitReview(reviewData)">
          <div class="rating">
            <label>Rating:</label>
            <select 
              v-model="reviewData.rating" 
              required 
              :disabled="isReviewReadOnly"
            >
              <option v-for="n in 5" :key="n" :value="n">{{ n }} Stars</option>
            </select>
          </div>
          <div class="review-text">
            <label>Comments:</label>
            <textarea 
              v-model="reviewData.comment" 
              rows="4" 
              required
              :readonly="isReviewReadOnly"
            ></textarea>
          </div>
          <div class="review-actions">
            <button 
              v-if="store.getters['module1/userRole'] === 'user'"
              type="submit" 
              class="submit-review-btn"
            >
              Submit Review
            </button>
            <button 
              type="button" 
              @click="isReviewModalOpen = false" 
              class="cancel-review-btn"
            >
              {{ store.getters['module1/userRole'] === 'user' ? 'Cancel' : 'Close' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>

.nav-icon {
  background: transparent;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  position: relative;
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
  font-size: 1.25rem;
}

.bookings-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: var(--background-color-blur);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  padding: 2rem 1.5rem;
}

.bookings-dialog {
  position: relative;
  width: 100%;
  max-width: 600px;
  background: var(--container-color);
  border-radius: 1rem;
  box-shadow: 0 12px 24px var(--background-color-blur);
  animation: slideUp 0.3s ease-out;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 4rem);
}

.bookings-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bookings-title {
  font-size: var(--h2-font-size);
  color: var(--text-color);
  margin: 0;
}

.bookings-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: var(--text-color);
  cursor: pointer;
  padding: 0.5rem;
  transition: color 0.2s;
}

.bookings-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.bookings-empty {
  text-align: center;
  padding: 2rem;
  color: var(--text-color-light);
}

.booking-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: var(--surface-color);
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  position: relative;
}

.booking-item-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 0.5rem;
}

.booking-item-details {
  flex: 1;
}

.booking-item-title {
  margin: 0 0 0.5rem;
  font-size: 1.25rem;
  color: var(--text-color);
}

.booking-professional {
  color: var(--text-color-light);
  margin: 0.25rem 0;
}

.booking-hours {
  color: var(--primary-color);
  margin: 0.25rem 0;
}

.booking-status {
  font-weight: 600;
  margin: 0.25rem 0;
}

.booking-status.pending {
  color: var(--warning-color);
}

.booking-status.accepted {
  color: var(--success-color);
}

.booking-status.rejected {
  color: var(--error-color);
}

.booking-status.completed {
  color: var(--primary-color);
}

.booking-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.cancel-btn, .close-btn, .review-btn,
.accept-btn, .reject-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.2s, transform 0.2s;
}

.cancel-btn {
  background-color: var(--error-color);
  color: white;
}

.close-btn {
  background-color: var(--primary-color);
  color: white;
}

.review-btn {
  background-color: var(--accent-color);
  color: white;
}

.accept-btn {
  background-color: var(--accent-color);
  color: white;
}

.reject-btn {
  background-color: var(--error-color);
  color: white;
}
/* Review Modal Styles */
.review-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--background-color-blur);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2100;
  padding: 1rem;
}

.review-modal-content {
  background: var(--container-color);
  border-radius: 1rem;
  padding: 2rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.1);
  animation: modalSlideUp 0.4s ease-out;
  position: relative;
}

@keyframes modalSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.review-modal-content h3 {
  color: var(--text-color);
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.25rem;
  font-weight: var(--font-semi-bold);
}

.rating, .review-text {
  margin-bottom: 1.5rem;
}

.rating label, .review-text label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-color-light);
  font-weight: var(--font-medium);
}

.rating select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid hsla(34, 52%, 53%, 0.2);
  border-radius: 0.5rem;
  background-color: var(--bg-color);
  color: var(--text-color);
  font-size: var(--normal-font-size);
  transition: border-color var(--transition-speed);
}

.rating select:focus {
  outline: none;
  border-color: var(--primary-color);
}

.review-text textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid hsla(34, 52%, 53%, 0.2);
  border-radius: 0.5rem;
  resize: vertical;
  min-height: 120px;
  background-color: var(--bg-color);
  color: var(--text-color);
  font-size: var(--normal-font-size);
  transition: border-color var(--transition-speed);
}

.review-text textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.review-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 1.5rem;
}

.submit-review-btn, .cancel-review-btn {
  flex: 1;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: var(--font-semi-bold);
  font-size: var(--normal-font-size);
  transition: 
    background-color var(--transition-speed),
    transform var(--transition-speed);
}

.submit-review-btn {
  background-color: var(--accent-color);
  color: var(--white);
}

.submit-review-btn:hover {
  background-color: var(--secondary-color);
}

.cancel-review-btn {
  background-color: var(--container-color);
  color: var(--text-color);
  border: 1px solid hsla(34, 52%, 53%, 0.2);
}

.cancel-review-btn:hover {
  background-color: var(--secondary-color-blur);
}

.submit-review-btn:active, 
.cancel-review-btn:active {
  transform: scale(0.98);
}

.booking-item-header {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.booking-item-text {
  flex-grow: 1;
}

.booking-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-self: flex-start;
}

/* Ensure rating is disabled for professional */
.rating select:disabled,
.review-text textarea:read-only {
  background-color: var(--surface-color);
  color: var(--text-color-light);
  cursor: not-allowed;
  opacity: 0.7;
}

@media (max-width: 480px) {
  .review-modal-content {
    padding: 1.5rem;
    margin: 0 0.5rem;
  }

  .review-actions {
    flex-direction: column;
  }

  .submit-review-btn, .cancel-review-btn {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .booking-item-header {
    flex-direction: column;
  }
  
  .booking-actions {
    align-self: stretch;
    margin-top: 0.5rem;
  }
}
</style>