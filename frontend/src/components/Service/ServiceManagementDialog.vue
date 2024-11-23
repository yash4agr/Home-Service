<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { useStore } from 'vuex'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close', 'edit'])

const store = useStore()
const searchQuery = ref('')
const selectedCategory = ref('')
let searchTimeout = null

// Get services and categories from store
const services = computed(() => store.getters['admin/servicesList'])
const categories = computed(() => store.getters['admin/serviceCategories'])
const isLoading = computed(() => store.getters['admin/isServicesLoading'])

const debounce = (callback, wait) => {
  return (...args) => {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => callback(...args), wait)
  }
}

// Search and filter functionality
const filteredServices = computed(() => {
  const query = searchQuery.value.toLowerCase().trim()
  const categoryId = selectedCategory.value

  return services.value.filter(service => {
    const matchesSearch = !query || 
      service.name.toLowerCase().includes(query) ||
      service.description.toLowerCase().includes(query)
    
    const matchesCategory = !categoryId || service.category_id === categoryId

    return matchesSearch && matchesCategory
  })
})

// Debounced search handler
const handleSearch = debounce((value) => {
  searchQuery.value = value
}, 300)

// Delete service handler
const handleDelete = async (serviceId) => {
  if (!confirm('Are you sure you want to delete this service?')) return
  
  try {
    await store.dispatch('admin/deleteService', serviceId)
  } catch (error) {
    console.error('Failed to delete service:', error)
    alert('Failed to delete service. Please try again.')
  }
}

// Edit service handler
const handleEdit = (service) => {
  emit('edit', service)
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

// Watch dialog state to handle body scroll
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    handleDialogOpen()
    store.dispatch('admin/fetchServices')
    store.dispatch('admin/fetchCategories')
  } else {
    handleDialogClose()
  }
})

// Reset filters when dialog closes
watch(() => props.isOpen, (newValue) => {
  if (!newValue) {
    searchQuery.value = ''
    selectedCategory.value = ''
  }
})

onUnmounted(() => {
    if (searchTimeout) {
        clearTimeout(searchTimeout)
    }
    handleDialogClose()
})
</script>

<template>
  <Transition name="fade">
    <div
      v-if="isOpen"
      class="service-container"
      @click.self="$emit('close')"
    >
      <div class="service-overlay">
        <div class="service-form">
          <button 
            type="button"
            class="service-close" 
            @click="$emit('close')"
            aria-label="Close"
          >
            <i class="ri-close-line" />
          </button>

          <h2 class="service-title">Manage Services</h2>

          <!-- Search and Filter Section -->
          <div class="search-filter-container">
            <div class="search-box">
              <input
                type="text"
                class="form-input"
                placeholder="Search services..."
                @input="e => handleSearch(e.target.value)"
              >
            </div>
            <div class="category-filter">
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

          <!-- Services List -->
          <div class="services-list">
            <div 
              v-if="isLoading"
              class="loading-state"
            >
              Loading services...
            </div>
            <div 
              v-else-if="filteredServices.length === 0" 
              class="no-services"
            >
              No services found
            </div>
            <div
              v-else
              v-for="service in filteredServices"
              :key="service.id"
              class="service-item"
            >
              <div class="service-info">
                <div class="service-image">
                  <img 
                    :src="service.img || '/placeholder-image.jpg'" 
                    :alt="service.name"
                  >
                </div>
                <div class="service-details">
                  <h3>{{ service.name }}</h3>
                  <p class="service-description">{{ service.description }}</p>
                  <div class="service-meta">
                    <span class="service-price">₹ {{ service.base_price }}</span>
                    <span class="service-category">{{ 
                      categories.find(c => c.id === service.category_id)?.name ||'Uncategorized'
                    }}</span>
                  </div>
                </div>
              </div>
              <div class="service-actions">
                <button
                  class="action-button edit"
                  @click="handleEdit(service)"
                >
                  Edit
                </button>
                <button
                  class="action-button delete"
                  @click="handleDelete(service.id)"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>

.service-container {
  position: fixed;
  z-index: 1100;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.service-overlay {
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

.service-form {
  position: relative;
  width: auto;
  background-color: var(--container-color);
  padding: var(--auth-padding);
  border-radius: var(--auth-border-radius);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  animation: slideUp 0.3s ease-out;
  margin: auto;
  max-height: calc(100vh - 4rem);
  /* overflow-y: auto; */
}

.service-form::-webkit-scrollbar {
  width: 8px;
}

.service-form::-webkit-scrollbar-track {
  background: transparent;
}

.service-form::-webkit-scrollbar-thumb {
  background-color: var(--accent-color);
  border-radius: 4px;
}

.service-close {
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

.service-close:hover {
  color: var(--primary-color);
  background-color: var(--accent-color);
}

.service-title {
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

.services-list {
  max-height: calc(100vh - 250px);
  max-width: 35rem;
  overflow-y: auto;
  padding-right: 0.5rem;
  padding-top: 0.5rem;
}

.services-list::-webkit-scrollbar {
  width: 8px;
}

.services-list::-webkit-scrollbar-track {
  background: transparent;
}

.services-list::-webkit-scrollbar-thumb {
  background-color: var(--accent-color);
  border-radius: 4px;
}

.no-services {
  text-align: center;
  padding: 2rem;
  color: var(--text-color);
  background-color: var(--accent-color);
  border-radius: 0.5rem;
}

.service-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid var(--accent-color);
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  background-color: var(--container-color);
  transition: transform 0.2s, box-shadow 0.2s;
}

.service-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.service-info {
  display: flex;
  gap: 1rem;
  flex: 1;
}

.service-image {
  width: 80px;
  height: 80px;
  border-radius: 0.5rem;
  overflow: hidden;
  flex-shrink: 0;
}

.service-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.service-details {
  flex: 1;
  min-width: 0;
}

.service-details h3 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-color);
}

.service-description {
  font-size: 0.875rem;
  color: var(--text-color);
  opacity: 0.8;
  margin: 0 0 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.service-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
}

.service-price {
  font-weight: 500;
  color: var(--primary-color);
}

.service-category {
  color: var(--text-color);
  opacity: 0.7;
}

.service-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: 1rem;
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

.action-button.edit {
  background-color: var(--accent-color);
  color: white;
}

.action-button.edit:hover {
  background-color: var(--secondary-color);
}

.action-button.delete {
  background-color: #fee2e2;
  color: #dc2626;
}

.action-button.delete:hover {
  background-color: #fecaca;
}

@media (max-width: 640px) {
  .service-overlay {
    padding: 1rem;
  }

  .service-form {
    margin: 1rem;
    max-height: calc(100vh - 2rem);
  }
  .search-filter-container {
    grid-template-columns: 1fr;
  }

  .service-item {
    flex-direction: column;
    align-items: stretch;
  }

  .service-actions {
    margin-left: 0;
    margin-top: 1rem;
    justify-content: flex-end;
  }

  .service-info {
    flex-direction: column;
  }

  .service-image {
    width: 100%;
    height: 160px;
  }
}
</style>