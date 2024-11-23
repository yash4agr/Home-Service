<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

const props = defineProps({
  user: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

const store = useStore()
const isLoading = ref(true)
const userDetails = ref(null)
const reviews = ref([])
const userAddress = ref(null)

// Computed properties for user type checks
const isProfessional = computed(() => props.user.role === 'professional')

// Computed properties for professional stats
const professionalStats = computed(() => ({
  totalServices: store.getters['admin/professionalTotalServices'](props.user.id) || 0,
  pendingServices: store.getters['admin/professionalPendingServices'](props.user.id) || 0,
  averageRating: store.getters['admin/professionalAverageRating'](props.user.id) || 0,
}))

// Format date helper
const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Handle blocking/unblocking user
const handleToggleBlock = async () => {
  const action = props.user.is_banned ? 'unblock' : 'block'
  if (!confirm(`Are you sure you want to ${action} this user?`)) return
  
  try {
    await store.dispatch('admin/toggleUserBan', {
      userId: props.user.id,
      isBanned: !props.user.is_banned
    })
  } catch (error) {
    console.error('Failed to update user status:', error)
    alert(`Failed to ${action} user. Please try again.`)
  }
}

// Fetch user details including address and reviews if professional
const fetchUserDetails = async () => {
  isLoading.value = true
  try {
    // Fetch user address
    const address = await store.dispatch('admin/fetchUserAddress', props.user.id)
    userAddress.value = address

    if (isProfessional.value) {
      // Fetch professional details and reviews
      const [professionalData, reviewsData] = await Promise.all([
        store.dispatch('admin/fetchProfessionalDetails', props.user.id),
        store.dispatch('admin/fetchProfessionalReviews', props.user.id)
      ])
      userDetails.value = professionalData
      reviews.value = reviewsData
    }
  } catch (error) {
    console.error('Error fetching user details:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchUserDetails)
</script>

<template>
  <div class="user-profile-overlay" @click.self="$emit('close')">
    <div class="user-profile-container">
      <button 
        type="button"
        class="user-close" 
        @click="$emit('close')"
        aria-label="Close"
      >
        <i class="ri-close-line" />
      </button>

      <div v-if="isLoading" class="loading-state">
        Loading user details...
      </div>
      
      <div v-else class="user-profile-content">
        <!-- User Header -->
        <div class="user-header">
          <div class="user-avatar">
            <img 
              :src="user.avatar || '/src/assets/pfp.jpg'" 
              :alt="user.name"
            >
          </div>
          <div class="user-header-info">
            <h2>{{ user.name }}</h2>
            <p class="user-email">{{ user.email }}</p>
            <div class="user-meta">
              <span 
                class="user-role"
                :class="user.role"
              >
                {{ user.role }}
              </span>
              <span 
                v-if="user.is_banned" 
                class="user-banned"
              >
                Banned
              </span>
            </div>
          </div>
        </div>

        <!-- User Details -->
        <div class="user-details-section">
          <div class="detail-group">
            <h3>Contact Information</h3>
            <p><strong>Phone:</strong> {{ user.phone_number || 'Not provided' }}</p>
            <p><strong>Email Verified:</strong> {{ user.is_email_verified ? 'Yes' : 'No' }}</p>
            <p><strong>Joined:</strong> {{ formatDate(user.created_at) }}</p>
          </div>

          <!-- Address Information -->
          <div v-if="userAddress" class="detail-group">
            <h3>Address</h3>
            <p>{{ userAddress.street }}</p>
            <p>{{ userAddress.city }}, {{ userAddress.state }} {{ userAddress.zip_code }}</p>
            <p>{{ userAddress.country }}</p>
          </div>

          <!-- Professional Specific Information -->
          <template v-if="isProfessional && userDetails">
            <div class="detail-group">
              <h3>Professional Details</h3>
              <div class="stats-grid">
                <div class="stat-item">
                  <span class="stat-label">Total Services</span>
                  <span class="stat-value">{{ professionalStats.totalServices }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Pending Services</span>
                  <span class="stat-value">{{ professionalStats.pendingServices }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Average Rating</span>
                  <span class="stat-value">{{ professionalStats.averageRating.toFixed(1) }}/5</span>
                </div>
              </div>
            </div>

            <!-- Reviews Section -->
            <div v-if="reviews.length > 0" class="detail-group">
              <h3>Recent Reviews</h3>
              <div class="reviews-list">
                <div 
                  v-for="review in reviews" 
                  :key="review.id" 
                  class="review-item"
                >
                  <div class="review-header">
                    <div class="review-rating">
                      ★ {{ review.rating }}/5
                    </div>
                    <div class="review-date">
                      {{ formatDate(review.created_at) }}
                    </div>
                  </div>
                  <p class="review-comment">{{ review.comment }}</p>
                </div>
              </div>
            </div>
          </template>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button
            class="action-button toggle-ban"
            :class="{ 'banned': user.is_banned }"
            @click="handleToggleBlock"
          >
            {{ user.is_banned ? 'Unblock' : 'Block' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.user-profile-overlay {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100vh;
  background-color: var(--background-color-blur);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  z-index: 1200;
}

.user-profile-container {
  position: relative;
  width: 100%;
  max-width: 40rem;
  background-color: var(--container-color);
  padding: var(--auth-padding);
  border-radius: var(--auth-border-radius);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  animation: slideUp 0.3s ease-out;
  max-height: calc(100vh - 4rem);
  overflow-y: auto;
}

.user-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.5rem;
  color: var(--text-color);
  background-color: transparent;
  border: none;
  cursor: pointer;
  transition: color var(--transition-speed);
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.user-header {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-header-info h2 {
  font-size: var(--h3-font-size);
  margin-bottom: 0.25rem;
}

.user-details-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-group {
  padding: 1rem;
  background-color: var(--accent-color);
  border-radius: 0.5rem;
}

.detail-group h3 {
  font-size: var(--normal-font-size);
  margin-bottom: 1rem;
  color: var(--text-color);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
}

.stat-item {
  background-color: var(--container-color);
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 0.875rem;
  color: var(--text-color-light);
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-color);
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.review-item {
  background-color: var(--container-color);
  padding: 1rem;
  border-radius: 0.5rem;
}

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.review-rating {
  color: #fbbf24;
  font-weight: 600;
}

.review-date {
  font-size: 0.875rem;
  color: var(--text-color-light);
}

.action-buttons {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 640px) {
  .user-profile-overlay {
    padding: 1rem;
  }

  .user-profile-container {
    margin: 1rem;
    max-height: calc(100vh - 2rem);
  }

  .user-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>