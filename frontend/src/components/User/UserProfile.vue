<script setup>
import { ref, computed, watch } from 'vue'
import { useStore } from 'vuex'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  user: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'update:user'])

const store = useStore()
const isLoading = computed(() => store.getters['admin/isUserLoading'])
const currentUser = computed(() => store.getters['admin/getUserById'](props.user?.id) || props.user)
const userAddress = computed(() => store.state.admin.userDetails?.address || null)
const professionalDetails = computed(() => store.state.admin.userDetails?.professionalDetails || null)
const reviews = computed(() => store.state.admin.userDetails?.reviews || [])

const isProfessional = computed(() => props.user?.role === 'professional')
const isAdmin = computed(() => props.user?.role === 'admin')

const professionalStats = computed(() => ({
  totalServices: store.state.admin.userDetails?.stats?.totalServices || 0,
  pendingServices: store.state.admin.userDetails?.stats?.pendingServices || 0,
  completedServices: store.state.admin.userDetails?.stats?.completedServices || 0,
  averageRating: store.state.admin.userDetails?.stats?.averageRating || 0,
}))

const formatDate = (date) => {
  if (!date) return 'N/A'
  try {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (error) {
    console.error('Error formatting date:', error)
    return 'Invalid date'
  }
}

const updateParentUser = () => {
  const updatedUser = store.getters['admin/getUserById'](props.user?.id)
  if (updatedUser) {
    emit('update:user', updatedUser)
  }
}

const refreshUserData = async (userId) => {
  if (!userId) return
  try {
    await store.dispatch('admin/fetchUser', { id: userId })
    await Promise.all([
      store.dispatch('admin/fetchUserAddress', userId),
      isProfessional.value && store.dispatch('admin/fetchProfessionalDetails', userId),
      isProfessional.value && store.dispatch('admin/fetchProfessionalReviews', userId)
    ])
    
    const updatedUser = store.getters['admin/getUserById'](userId)
    if (updatedUser) {
      emit('update:user', updatedUser)
    }
  } catch (error) {
    console.error('Failed to refresh user data:', error)
  }
}

// Actions handlers
const handleToggleBan = async (userId, isBanned) => {
  if (!userId) return
  
  const action = isBanned ? 'unban' : 'ban'
  if (!confirm(`Are you sure you want to ${action} this user?`)) return
  
  try {
    await store.dispatch('admin/toggleUserBan', { userId, isBanned: !isBanned })
    updateParentUser()
  } catch (error) {
    console.error('Failed to update user status:', error)
    alert(`Failed to ${action} user. Please try again.`)
  }
}

const handleProfessionalApproval = async (isApproved) => {
  if (!professionalDetails.value?.id) return
  
  const action = isApproved ? 'approve' : 'reject'
  if (!confirm(`Are you sure you want to ${action} this professional?`)) return
  
  try {
    await store.dispatch('admin/updateProfessionalStatus', {
      professionalId: professionalDetails.value.id,
      isApproved
    })
    await refreshUserData(currentUser.value.id)
    updateParentUser()
  } catch (error) {
    console.error('Failed to update professional status:', error)
    alert(`Failed to ${action} professional. Please try again.`)
  }
}

const downloadResume = async () => {
  if (!professionalDetails.value?.id) return
  try {
    await store.dispatch('admin/downloadProfessionalResume', professionalDetails.value.id)
  } catch (error) {
    console.error('Failed to download resume:', error)
    alert('Failed to download resume. Please try again.')
  }
}

// Scroll management
const scrollPosition = ref(0)

const handleDialogOpen = () => {
  scrollPosition.value = window.scrollY
  document.body.classList.add('dialog-open')
  document.body.style.position = 'fixed'
  document.body.style.top = `-${scrollPosition.value}px`
  document.body.style.width = '100%'
}

const handleDialogClose = () => {
  document.body.style.position = ''
  document.body.style.top = ''
  document.body.style.width = ''
  document.body.classList.remove('dialog-open')
  window.scrollTo(0, scrollPosition.value)
}

const handleClose = () => {
  handleDialogClose()
  emit('close')
}

// Watch dialog state and fetch data
watch(() => props.isOpen, (newValue) => {
  if (newValue && props.user?.id) {
    handleDialogOpen()
    refreshUserData(props.user.id)
  } else {
    handleDialogClose()
  }
}, { immediate: true })

watch(() => props.user?.id, (newId) => {
  if (props.isOpen && newId) {
    refreshUserData(newId)
  }
})
</script>

<template>
  <div 
    v-if="isOpen"
    class="user-profile-overlay" 
    @click.self="handleClose"
  >
    <div class="user-profile-container">
      <button 
        type="button"
        class="user-close" 
        @click="handleClose"
        aria-label="Close"
      >
        <i class="ri-close-line" />
      </button>

      <div v-if="isLoading" class="loading-state">
        Loading user details...
      </div>
      
      <div v-else-if="user" class="user-profile-content">
        <!-- User Header -->
        <div class="user-header">
          <div class="user-avatar">
            <img 
              :src="'/src/assets/pfp.jpg'" 
              :alt="currentUser.name"
            >
          </div>
          <div class="user-header-info">
            <h2>{{ currentUser.name }}</h2>
            <p class="user-email">{{ currentUser.email }}</p>
            <div class="user-meta">
              <span 
                class="user-role"
                :class="currentUser.role"
              >
                {{ currentUser.role }}
              </span>
              <span 
                v-if="currentUser.is_banned" 
                class="user-banned"
              >
                Banned
              </span>
            </div>
          </div>
        </div>

        <!-- Basic User Details -->
        <div class="user-details-section">
          <div class="detail-group">
            <h3>Contact Information</h3>
            <p><strong>Phone:</strong> {{ currentUser.phone_number || 'Not provided' }}</p>
            <p><strong>Email Verified:</strong> {{ currentUser.is_email_verified ? 'Yes' : 'No' }}</p>
            <p><strong>Joined:</strong> {{ formatDate(currentUser.created_at) }}</p>
          </div>

          <!-- Address Information -->
          <div v-if="userAddress" class="detail-group">
            <h3>Address</h3>
            <p>{{ userAddress.street }}</p>
            <p>{{ userAddress.city }}, {{ userAddress.state }} {{ userAddress.zip_code }}</p>
            <p>{{ userAddress.country }}</p>
          </div>

          <!-- Professional Specific Information -->
          <template v-if="isProfessional">
            <div v-if="professionalDetails" class="detail-group">
              <h3>Professional Details</h3>
              <p><strong>Experience:</strong> {{ professionalDetails.experience }} years</p>
              <p><strong>Status:</strong> {{ professionalDetails.is_approved ? 'Approved' : 'Pending Approval' }}</p>
              
              <div class="stats-grid">
                <div class="stat-item">
                  <span class="stat-label">Total Services</span>
                  <span class="stat-value">{{ professionalStats.totalServices }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Pending</span>
                  <span class="stat-value">{{ professionalStats.pendingServices }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Completed</span>
                  <span class="stat-value">{{ professionalStats.completedServices }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Rating</span>
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

        <!-- Action Buttons (Not shown for admins) -->
        <div v-if="!isAdmin" class="action-buttons">
          <!-- Professional specific actions -->
          <template v-if="isProfessional && professionalDetails">
            <button
              v-if="!professionalDetails.is_approved"
              class="action-button approve"
              @click="handleProfessionalApproval(true)"
            >
              Approve Professional
            </button>
            <button
              v-if="!professionalDetails.is_approved"
              class="action-button reject"
              @click="handleProfessionalApproval(false)"
            >
              Reject Professional
            </button>
            <button
              class="action-button download"
              @click="downloadResume"
            >
              Download Resume
            </button>
          </template>

          <!-- Block/Unblock button for all non-admin users -->
          <button
            class="action-button toggle-ban"
            :class="{ 'banned': currentUser.is_banned }"
            @click="handleToggleBan(currentUser.id, currentUser.is_banned)"
          >
            {{ currentUser.is_banned ? 'Unblock' : 'Block' }}
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

.user-details-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-group {
  padding: 1.5rem;
  background-color: var(--accent-color);
  border-radius: 0.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.stat-item {
  background-color: var(--container-color);
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: center;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.review-item {
  background-color: var(--container-color);
  padding: 1rem;
  border-radius: 0.5rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.action-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.action-button.approve {
  background-color: #10b981;
  color: white;
}

.action-button.reject {
  background-color: #ef4444;
  color: white;
}

.action-button.download {
  background-color: #6366f1;
  color: white;
}

.action-button.toggle-ban {
  background-color: #fee2e2;
  color: #dc2626;
}

.action-button.toggle-ban.banned {
  background-color: #f3f4f6;
  color: #374151;
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
    grid-template-columns: 1fr 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-button {
    width: 100%;
  }
}
</style>