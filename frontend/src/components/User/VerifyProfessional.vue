<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { useStore } from 'vuex'
import UserProfileDialog from './UserProfile.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close', 'showProfile'])

const store = useStore()
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedUser = ref(null)
let searchTimeout = null

// Get users from store
const users = computed(() => store.getters['admin/ProfessionalsList'] || [])
const userProfileDialogState = computed(() => store.getters['admin/userProfileDialogState'])
const isLoading = computed(() => store.getters['admin/isUsersLoading'])
const categories = computed(() => store.getters['admin/serviceCategories'])

const debounce = (callback, wait) => {
  return (...args) => {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => callback(...args), wait)
  }
}

// Search and filter functionality with null checks
const filteredUsers = computed(() => {
  const query = searchQuery.value?.toLowerCase().trim() || ''
  const categoryId = selectedCategory.value
  return users.value.filter(user => {
    const matchesSearch = !query || 
      user?.name?.toLowerCase().includes(query) ||
      user?.email?.toLowerCase().includes(query)

    const matchesCategory = !categoryId || user.category_id === categoryId

    return matchesSearch && matchesCategory
  }) || []
})

// Debounced search handler
const handleSearch = debounce((value) => {
  searchQuery.value = value || ''
}, 300)


// View profile handler
const handleUserProfile = (user) => {
  if (!user) return
  store.commit('admin/SET_USER_PROFILE_DIALOG', { isOpen: true, user });
}

const handleCloseUserProfile = () => {
  store.commit('admin/SET_USER_PROFILE_DIALOG', { isOpen: false, user: null });
}

// Scroll management with cleanup
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

// Watch dialog state and fetch users only when opening
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    store.dispatch('admin/fetchProfessionalUsers')
    store.dispatch('admin/fetchCategories')
    handleDialogOpen()
  } else {
    handleDialogClose()
  }
}, { immediate: true })

watch(() => userProfileDialogState.value.isOpen, (newValue) => {
  if (!newValue) {
    store.commit('admin/SET_USER_PROFILE_DIALOG', { isOpen: false, user: null });
  }
});

// Reset filters when dialog closes
watch(() => props.isOpen, (newValue) => {
  if (!newValue) {
    searchQuery.value = ''
    selectedCategory.value = ''
    selectedUser.value = null
  }
})

// Cleanup on component unmount
onUnmounted(() => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  handleDialogClose()
  // Reset body styles
  document.body.style.position = ''
  document.body.style.top = ''
  document.body.style.width = ''
  document.body.classList.remove('dialog-open')
})
</script>

<template>
  <Transition name="fade">
    <div
      v-if="isOpen"
      class="user-container"
      @click.self="$emit('close')"
    >
      <div class="user-overlay">
        <div class="user-form">
          <button 
            type="button"
            class="user-close" 
            @click="$emit('close')"
            aria-label="Close"
          >
            <i class="ri-close-line" />
          </button>

          <h2 class="user-title">Verify Professionals</h2>

          <!-- Search and Filter Section -->
          <div class="search-filter-container">
            <div class="search-box">
              <input
                type="text"
                class="form-input"
                placeholder="Search users..."
                :value="searchQuery"
                @input="e => handleSearch(e.target.value)"
              >
            </div>
            <div class="role-filter">
              <select
                v-model="selectedCategory"
                class="form-input"
              >
                <option value="">All Categories</option>
                <option 
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- Users List -->
          <div class="users-list">
            <div 
              v-if="isLoading"
              class="loading-state"
            >
              Loading users...
            </div>
            <div 
              v-else-if="users.value?.length" 
              class="no-users"
            >
              No users available
            </div>
            <div 
              v-else-if="filteredUsers.length === 0" 
              class="no-users"
            >
              No users found matching your search
            </div>
            <div
              v-else
              v-for="user in filteredUsers"
              :key="user.id"
              class="user-item"
            >
              <div class="user-info">
                <div class="user-avatar">
                  <img 
                    :src="'/src/assets/pfp.jpg'" 
                    :alt="user.name"
                    @error="$event.target.src = '/src/assets/default-avatar.jpg'"
                  >
                </div>
                <div class="user-details">
                  <h3>{{ user.name }}</h3>
                  <p class="user-email">{{ user.email }}</p>
                  <div class="user-meta">
                  </div>
                </div>
              </div>
              <div class="user-actions">
                <button
                  class="action-button view"
                  @click="handleUserProfile(user)"
                >
                  View Profile
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Profile Dialog -->
      <UserProfileDialog
      v-if="userProfileDialogState.isOpen"
      :is-open="userProfileDialogState.isOpen"
      v-model:user="userProfileDialogState.user"
      @close="store.commit('admin/SET_USER_PROFILE_DIALOG', { isOpen: false, user: null })"
    />
    </div>
  </Transition>
</template>

<style scoped>
.user-container {
  position: fixed;
  z-index: 1100;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.user-overlay {
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
  z-index: 1100;
}

.user-form {
  position: relative;
  width: auto;
  background-color: var(--container-color);
  padding: var(--auth-padding);
  border-radius: var(--auth-border-radius);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  animation: slideUp 0.3s ease-out;
  margin: auto;
  max-height: calc(100vh - 4rem);
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

.user-close:hover {
  color: var(--primary-color);
  background-color: var(--accent-color);
}

.user-title {
  font-size: var(--h2-font-size);
  color: var(--text-color);
  text-align: center;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.search-filter-container {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.users-list {
  max-height: calc(100vh - 250px);
  max-width: 35rem;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid var(--accent-color);
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  background-color: var(--container-color);
}

.user-info {
  display: flex;
  gap: 1rem;
  flex: 1;
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-details {
  flex: 1;
}

.user-email {
  color: var(--text-color);
  opacity: 0.7;
  font-size: 0.875rem;
}

.user-meta {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.user-role {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.user-role.admin {
  background-color: #818cf8;
  color: white;
}

.user-role.professional {
  background-color: #10b981;
  color: white;
}

.user-role.user {
  background-color: #6b7280;
  color: white;
}

.user-banned {
  background-color: #ef4444;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.user-actions {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.action-button.view {
  background-color: var(--accent-color);
  color: var(--text-color);
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
  .user-overlay {
    padding: 1rem;
  }

  .user-form {
    margin: 1rem;
    max-height: calc(100vh - 2rem);
  }

  .search-filter-container {
    grid-template-columns: 1fr;
  }

  .user-item {
    flex-direction: column;
    align-items: stretch;
  }

  .user-actions {
    margin-top: 1rem;
    justify-content: flex-end;
  }
}
</style>