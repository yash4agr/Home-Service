<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const props = defineProps({
  isBookingsOpen: {
    type: Boolean,
    required: true,
    // default: true
  }
})
// var props;
// const props.isBookingsOpen = ref(true)
// const isBookingsOpen = ref(true)
const emit = defineEmits(['update:isBookingsOpen'])

// Bookings data from store
// const bookings = computed(() => store.getters['module2/bookings'])
const bookings = computed(() => [])

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
</script>

<template>
  <div class="bookings-container">
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
                <img :src="booking.service.image" :alt="booking.service.name" class="booking-item-image">
                
                <div class="booking-item-details">
                  <h3 class="booking-item-title">{{ booking.service.name }}</h3>
                  <p class="booking-professional">Professional: {{ booking.professional.name }}</p>
                  <p class="booking-hours">Hours: {{ booking.hours }}</p>
                  <p class="booking-status" :class="booking.status.toLowerCase()">
                    Status: {{ booking.status }}
                  </p>
                  
                  <div class="booking-actions">
                    <!-- Client Actions -->
                    <template v-if="booking.role === 'client'">
                      <button 
                        v-if="booking.status === 'Pending'" 
                        class="cancel-btn" 
                        @click="cancelBooking(booking.id)"
                      >
                        Cancel Booking
                      </button>
                      <button 
                        v-if="booking.status === 'Accepted'" 
                        class="close-btn" 
                        @click="closeBooking(booking.id)"
                      >
                        Close Booking
                      </button>
                      <button 
                        v-if="booking.status === 'Completed'" 
                        class="review-btn" 
                        @click="openReviewModal(booking)"
                      >
                        Submit Review
                      </button>
                    </template>

                    <!-- Professional Actions -->
                    <template v-if="booking.role === 'professional'">
                      <button 
                        v-if="booking.status === 'Pending'" 
                        class="accept-btn" 
                        @click="acceptService(booking.service.id)"
                      >
                        Accept
                      </button>
                      <button 
                        v-if="booking.status === 'Pending'" 
                        class="reject-btn" 
                        @click="rejectService(booking.service.id)"
                      >
                        Reject
                      </button>
                    </template>
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
        <form @submit.prevent="submitReview">
          <div class="rating">
            <label>Rating:</label>
            <select v-model="reviewData.rating" required>
              <option v-for="n in 5" :key="n" :value="n">{{ n }} Stars</option>
            </select>
          </div>
          <div class="review-text">
            <label>Comments:</label>
            <textarea v-model="reviewData.comment" rows="4" required></textarea>
          </div>
          <div class="review-actions">
            <button type="submit" class="submit-review-btn">Submit Review</button>
            <button type="button" @click="isReviewModalOpen = false" class="cancel-review-btn">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Reusing most of the cart styles with modifications */
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
  box-shadow: 0 8px 32px var(--background-color-blur);
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
  background-color: var(--success-color);
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
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1200;
}

.review-modal-content {
  background: var(--container-color);
  border-radius: 1rem;
  padding: 2rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 8px 32px var(--background-color-blur);
}

.rating, .review-text {
  margin-bottom: 1rem;
}

.review-actions {
  display: flex;
  justify-content: space-between;
}

.submit-review-btn, .cancel-review-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s, transform 0.2s;
}

.submit-review-btn {
  background-color: var(--accent-color);
  color: white;
}

.cancel-review-btn {
  background-color: var(--surface-hover);
  color: var(--text-color);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .booking-item {
    flex-direction: column;
  }
  
  .booking-item-image {
    width: 100%;
    height: 200px;
  }
}
</style>