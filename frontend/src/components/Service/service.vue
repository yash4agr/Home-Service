<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const props = defineProps({
  serviceToEdit: {
    type: Object,
    default: () => null
  },
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close'])

const store = useStore()
const router = useRouter()

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
  } else {
    handleDialogClose()
  }
})

// Cleanup
onUnmounted(() => {
  handleDialogClose()
})

// Fetch categories on mount
onMounted(async () => {
  await store.dispatch('admin/fetchCategories')
})

// Access categories from store
const categories = computed(() => store.getters['admin/serviceCategories'])
const isLoading = computed(() => store.getters['admin/isServicesLoading'])

// Reactive form data
const serviceForm = reactive({
  name: '',
  description: '',
  base_price: null,
  img: '',
  time_required: 1,
  category_id: '',
  new_category: '',
  tags: [],
})

// New category handling
const isNewCategory = ref(false)

// Tags handling
const newTag = ref('')
const addTag = () => {
  const tag = newTag.value.trim()
  if (tag && !serviceForm.tags.includes(tag)) {
    serviceForm.tags.push(tag)
  }
  newTag.value = ''
}
const removeTag = (index) => {
  serviceForm.tags.splice(index, 1)
}

// Populate form if editing existing service
watch(() => props.serviceToEdit, (newService) => {
  if (newService) {
    Object.assign(serviceForm, newService)
  } else {
    // Reset form when creating new service
    Object.assign(serviceForm, {
      name: '',
      description: '',
      base_price: null,
      img: '',
      time_required: 1,
      category_id: '',
      new_category: '',
      tags: [],
    })
  }
}, { immediate: true })

// Image upload handling
const imageFile = ref(null)
const imagePreview = ref(null)

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
    const maxSize = 5 * 1024 * 1024 // 5MB

    if (!allowedTypes.includes(file.type)) {
      errors.img = 'Invalid file type. Please upload JPG, PNG, or GIF.'
      return
    }

    if (file.size > maxSize) {
      errors.img = 'File size exceeds 5MB limit.'
      return
    }

    imageFile.value = file || null
    errors.img = ''
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// Form validation
const errors = reactive({
  name: '',
  description: '',
  base_price: '',
  category: '',
  img: ''
})

const validateForm = () => {
  Object.keys(errors).forEach(key => errors[key] = '')
  let isValid = true
  
  if (!serviceForm.name.trim()) {
    errors.name = 'Service name is required'
    isValid = false
  }

  if (!serviceForm.description.trim()) {
    errors.description = 'Description is required'
    isValid = false
  }

  if (!serviceForm.base_price || serviceForm.base_price <= 0) {
    errors.base_price = 'Valid price is required'
    isValid = false
  }

  if (isNewCategory.value && !serviceForm.new_category.trim()) {
    errors.category = 'Category name is required'
    isValid = false
  } else if (!isNewCategory.value && !serviceForm.category_id) {
    errors.category = 'Please select a category'
    isValid = false
  }

  return isValid
}

// Submit handling
const submitError = ref('')

const handleSubmit = async () => {
  if (isLoading.value) return
  
  if (!validateForm()) {
    submitError.value = 'Please complete all required fields correctly.'
    return
  }

  try {
    submitError.value = ''
    
    const formData = new FormData()
    
    // Handle category
    if (isNewCategory.value) {
      formData.append('new_category', serviceForm.new_category)
    } else {
      formData.append('category_id', serviceForm.category_id)
    }

    // Append other form data
    Object.keys(serviceForm).forEach(key => {
      if (key === 'tags') {
        formData.append('tags', JSON.stringify(serviceForm.tags))
      } else if (key !== 'new_category') {
        formData.append(key, serviceForm[key])
      }
    })

    if (imageFile.value) {
      formData.append('img', imageFile.value)
    }

    await store.dispatch('admin/upsertService', {
      serviceData: formData,
      serviceId: props.serviceToEdit?.id
    })

    store.dispatch('admin/closeServiceDialog')
    router.go(0)
  } catch (error) {
    submitError.value = error.response?.data?.message || 'Failed to save service. Please try again.'
  }
}

const isEditing = computed(() => !!props.serviceToEdit)
</script>

<template>
  <Transition name="fade">
    <div
      v-if="isOpen"
      class="service-container"
      @click.self="$emit('close')"
    >
      <div class="service-overlay">
        <form @submit.prevent="handleSubmit" class="service-form">
          <button 
            type="button"
            class="service-close" 
            @click="$emit('close')"
            aria-label="Close"
          >
            <i class="ri-close-line" />
          </button>

          <h2 class="service-title">
            {{ isEditing ? 'Edit Service' : 'Create New Service' }}
          </h2>

          <div class="form-group">
            <!-- Service Name -->
            <div class="form-item">
              <label for="name" class="form-label">Service Name</label>
              <input
                id="name"
                v-model="serviceForm.name"
                type="text"
                :class="['form-input', { error: errors.name }]"
                placeholder="Enter service name"
                required
              />
              <span v-if="errors.name" class="error-text">
                {{ errors.name }}
              </span>
            </div>

            <!-- Description -->
            <div class="form-item">
              <label for="description" class="form-label">Description</label>
              <textarea
                id="description"
                v-model="serviceForm.description"
                :class="['form-input', { error: errors.description }]"
                placeholder="Describe your service"
                rows="4"
                required
              />
              <span v-if="errors.description" class="error-text">
                {{ errors.description }}
              </span>
            </div>

            <!-- Price and Time Required -->
            <div class="form-row">
              <div class="form-item">
                <label for="base_price" class="form-label">Base Price (₹)</label>
                <input
                  id="base_price"
                  v-model.number="serviceForm.base_price"
                  type="number"
                  step="0.01"
                  :class="['form-input', { error: errors.base_price }]"
                  placeholder="Enter base price"
                  required
                />
                <span v-if="errors.base_price" class="error-text">
                  {{ errors.base_price }}
                </span>
              </div>
              <div class="form-item">
                <label for="time_required" class="form-label">Time Required (hours)</label>
                <input
                  id="time_required"
                  v-model.number="serviceForm.time_required"
                  type="number"
                  min="0.5"
                  step="0.5"
                  class="form-input"
                  placeholder="Enter time required"
                />
              </div>
            </div>

            <!-- Category Selection -->
            <div class="form-item">
              <label class="form-label">Category</label>
              <div class="category-selection">
                <select
                  v-if="!isNewCategory"
                  v-model="serviceForm.category_id"
                  :class="['form-input', { error: errors.category }]"
                >
                  <option value="">Select a category</option>
                  <option 
                    v-for="category in categories"
                    :key="category.id"
                    :value="category.id"
                  >
                    {{ category.name }}
                  </option>
                </select>
                <input
                  v-else
                  v-model="serviceForm.new_category"
                  type="text"
                  :class="['form-input', { error: errors.category }]"
                  placeholder="Enter new category name"
                />
                <button 
                  type="button"
                  class="category-toggle"
                  @click="isNewCategory = !isNewCategory"
                >
                  {{ isNewCategory ? 'Select Existing' : 'Create New' }}
                </button>
              </div>
              <span v-if="errors.category" class="error-text">
                {{ errors.category }}
              </span>
            </div>

            <!-- Tags -->
            <div class="form-item">
              <label class="form-label">Tags</label>
              <div class="tags-input">
                <input
                  v-model="newTag"
                  type="text"
                  class="form-input"
                  placeholder="Enter tag and press Enter"
                  @keyup.enter.prevent="addTag"
                />
                <button 
                  type="button"
                  class="tag-add-btn"
                  @click="addTag"
                >
                  Add
                </button>
              </div>
              <div class="tags-container">
                <span 
                  v-for="(tag, index) in serviceForm.tags"
                  :key="index"
                  class="tag"
                >
                  {{ tag }}
                  <button 
                    type="button"
                    class="tag-remove"
                    @click="removeTag(index)"
                  >
                    ×
                  </button>
                </span>
              </div>
            </div>

            <!-- Image Upload -->
            <div class="form-item">
              <label for="image" class="form-label">Service Image</label>
              <input
                id="image"
                type="file"
                accept="image/*"
                :class="['form-input', { error: errors.img }]"
                @change="handleImageUpload"
              />
              <span v-if="errors.img" class="error-text">
                {{ errors.img }}
              </span>
              <div v-if="imagePreview" class="image-preview">
                <img :src="imagePreview" alt="Service preview" />
              </div>
            </div>
          </div>

          <!-- Submit Error Message -->
          <div v-if="submitError" class="error-container">
            <p class="error-text" role="alert">
              {{ submitError }}
            </p>
          </div>

          <!-- Submit Button -->
          <div class="service-actions">
            <button
              type="button"
              class="service-button secondary"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="service-button"
              :disabled="isLoading"
            >
              {{ isLoading ? 'Saving...' : (isEditing ? 'Update Service' : 'Create Service') }}
            </button>
          </div>
        </form>
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
  width: 100%;
  max-width: var(--auth-max-width);
  background-color: var(--container-color);
  padding: var(--auth-padding);
  border-radius: var(--auth-border-radius);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  animation: slideUp 0.3s ease-out;
  margin: auto;
  max-height: calc(100vh - 4rem);
  overflow-y: auto;
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

.form-group {
  display: grid;
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  color: var(--text-color);
  font-weight: 500;
  font-size: 0.875rem;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid var(--accent-color);
  border-radius: 0.5rem;
  background-color: var(--container-color);
  color: var(--text-color);
  transition: border-color var(--transition-speed);
  font-size: 0.875rem;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.form-input.error {
  border-color: var(--error-color);
}

textarea.form-input {
  resize: vertical;
  min-height: 100px;
}

.error-container {
  background-color: rgba(220, 38, 38, 0.1);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
}

.error-text {
  color: var(--error-color);
  font-size: 0.875rem;
}

.service-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.service-button {
  min-width: 120px;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-speed);
  font-size: 0.875rem;
}

.service-button:not(.secondary) {
  background-color: var(--accent-color);
  /* color: white; */
}

.service-button:not(.secondary):hover {
  background-color: var(--secondary-color);
}

.service-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.service-button.secondary {
  background-color: transparent;
  color: var(--text-color);
  border: 1px solid var(--accent-color);
}

.service-button.secondary:hover {
  background-color: var(--accent-color);
}

.category-selection {
  display: flex;
  gap: 0.75rem;
}

.category-selection select,
.category-selection input {
  flex: 1;
}

.category-toggle {
  padding: 0.75rem 1rem;
  background-color: var(--container-color);
  border: 1px solid var(--accent-color);
  border-radius: 0.5rem;
  color: var(--text-color);
  cursor: pointer;
  font-size: 0.875rem;
  transition: all var(--transition-speed);
}

.category-toggle:hover {
  background-color: var(--accent-color);
}

.tags-input {
  display: flex;
  gap: 0.75rem;
}

.tags-input input {
  flex: 1;
}

.tag-add-btn {
  padding: 0.75rem 1rem;
  background-color: var(--container-color);
  border: 1px solid var(--accent-color);
  border-radius: 0.5rem;
  color: var(--text-color);
  cursor: pointer;
  font-size: 0.875rem;
  transition: all var(--transition-speed);
}

.tag-add-btn:hover {
  background-color: var(--accent-color);
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
  min-height: 38px;
  padding: 0.5rem;
  border: 1px solid var(--accent-color);
  border-radius: 0.5rem;
}

.tags-container:empty { 
    grid-area: tags-container; 
    display: none;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  background-color: var(--accent-color);
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.tag-remove {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.25rem;
  height: 1.25rem;
  border: none;
  background: rgba(0, 0, 0, 0.1);
  color: var(--text-color);
  cursor: pointer;
  padding: 0;
  font-size: 1rem;
  border-radius: 50%;
  transition: all var(--transition-speed);
}

.tag-remove:hover {
  background-color: rgba(0, 0, 0, 0.2);
}

.image-preview {
  margin-top: 0.75rem;
  border-radius: 0.5rem;
  overflow: hidden;
  border: 1px solid var(--accent-color);
}

.image-preview img {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  display: block;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive Styles */
@media (max-width: 640px) {
  :root {
    --service-padding: 1.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
  
  .service-overlay {
    padding: 1rem;
  }
  
  .service-form {
    margin: 1rem;
    max-height: calc(100vh - 2rem);
  }

  .service-actions {
    flex-direction: column-reverse;
  }

  .service-button {
    width: 100%;
  }

  .category-selection {
    flex-direction: column;
  }

  .tags-input {
    flex-direction: column;
  }
}
</style>