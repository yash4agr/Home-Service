<script setup>
import { ref, reactive, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const props = defineProps({
  serviceToEdit: {
    type: Object,
    default: () => null
  }
})

const emit = defineEmits(['close'])

// Reactive form data
const serviceForm = reactive({
  name: '',
  description: '',
  base_price: null,
  img: '',
  time_required: 1,
  available: ''
})

// Populate form if editing existing service
if (props.serviceToEdit) {
  Object.assign(serviceForm, props.serviceToEdit)
}

// Image upload handling
const imageFile = ref(null)
const imagePreview = ref(null)

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    imageFile.value = file
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
  available: ''
})

const validateForm = () => {
  // Reset errors
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

  if (!serviceForm.available.trim()) {
    errors.available = 'Availability information is required'
    isValid = false
  }

  return isValid
}

// Submit form
const submitService = async () => {
  if (!validateForm()) return

  try {
    const formData = new FormData()
    
    // Append form fields
    Object.keys(serviceForm).forEach(key => {
      formData.append(key, serviceForm[key])
    })

    // Append image if uploaded
    if (imageFile.value) {
      formData.append('img', imageFile.value)
    }

    // Dispatch Vuex action for service creation/update
    await store.dispatch('services/upsertService', {
      serviceData: formData,
      serviceId: props.serviceToEdit?.id
    })

    // Close dialog and potentially refresh service list
    emit('close')
    router.go(0) // Optional: hard refresh to update service list
  } catch (error) {
    console.error('Service submission error:', error)
    // Handle error (e.g., show error toast)
  }
}

// Computed properties for form submission state
const isEditing = computed(() => !!props.serviceToEdit)
const submitButtonText = computed(() => 
  isEditing.value ? 'Update Service' : 'Create Service'
)
</script>

<template>
  <div class="service-dialog">
    <div class="service-dialog-content">
      <h2>{{ isEditing ? 'Edit Service' : 'Create New Service' }}</h2>
      
      <form @submit.prevent="submitService" class="service-form">
        <div class="form-group">
          <label for="name">Service Name</label>
          <input 
            id="name" 
            v-model="serviceForm.name" 
            type="text" 
            placeholder="Enter service name"
          />
          <span v-if="errors.name" class="error-message">{{ errors.name }}</span>
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea 
            id="description" 
            v-model="serviceForm.description"
            placeholder="Describe the service"
          ></textarea>
          <span v-if="errors.description" class="error-message">{{ errors.description }}</span>
        </div>

        <div class="form-group">
          <label for="base_price">Base Price</label>
          <input 
            id="base_price" 
            v-model.number="serviceForm.base_price" 
            type="number" 
            step="0.01" 
            placeholder="Enter base price"
          />
          <span v-if="errors.base_price" class="error-message">{{ errors.base_price }}</span>
        </div>

        <div class="form-group">
          <label for="available">Availability</label>
          <input 
            id="available" 
            v-model="serviceForm.available" 
            type="text" 
            placeholder="Enter availability details"
          />
          <span v-if="errors.available" class="error-message">{{ errors.available }}</span>
        </div>

        <div class="form-group">
          <label for="image">Service Image</label>
          <input 
            id="image" 
            type="file" 
            accept="image/*"
            @change="handleImageUpload"
          />
          <div v-if="imagePreview" class="image-preview">
            <img :src="imagePreview" alt="Image Preview" />
          </div>
        </div>

        <div class="form-actions">
          <button type="button" @click="$emit('close')" class="btn-cancel">
            Cancel
          </button>
          <button type="submit" class="btn-submit">
            {{ submitButtonText }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.service-dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.service-dialog-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.service-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.error-message {
  color: red;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.image-preview img {
  max-width: 200px;
  max-height: 200px;
  object-fit: cover;
  margin-top: 0.5rem;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.btn-submit,
.btn-cancel {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-submit {
  background-color: #4CAF50;
  color: white;
}

.btn-cancel {
  background-color: #f44336;
  color: white;
}
</style>