<script setup>
import BaseAuth from "@/components/Auth/BaseAuth.vue";
import { ref, computed, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";
import axios from "axios";

// Service Categories Dropdown
const SERVICE_CATEGORIES = [
  "Web Development",
  "Graphic Design", 
  "Digital Marketing",
  "IT Consulting",
  "Content Writing",
  "Software Engineering",
  "Cloud Services",
  "Cybersecurity",
  "UX/UI Design",
  "Data Analysis"
];

// Country and State Lists (example data)
const COUNTRIES = [
  "United States", 
  "Canada", 
  "United Kingdom", 
  "India", 
  "Australia", 
  "Germany", 
  "France"
];

const STATES = {
  "United States": [
    "California", "New York", "Texas", "Florida", "Illinois"
  ],
  "India": [
    "Maharashtra", "Karnataka", "Tamil Nadu", "Delhi", "Gujarat"
  ],
  "Canada": [
    "Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba"
  ]
};

// Composables
const router = useRouter();
const route = useRoute();
const store = useStore();

// Form State
const professionalData = ref({
  fullName: "",
  phoneNumber: "",
  serviceCategory: "",
  address: {
    locality: "",
    city: "",
    pincode: "",
    state: "",
    country: ""
  },
  yearsOfExperience: null,
  resume: null
});
const errorMessage = ref("");
const currentStep = ref(1);
const isFormValid = ref({
  stepOne: false,
  stepTwo: false
});
const availableStates = ref([]);

const isOpen = computed(() => store.getters["module1/professionalSignupDialogVisible"]);
// Validation for Step One
const validateStepOne = () => {
  const { fullName, phoneNumber } = professionalData.value;
  const { locality, city, pincode, state, country } = professionalData.value.address;
  
  isFormValid.value.stepOne = !!(
    fullName.trim() && 
    phoneNumber.trim() && 
    locality.trim() && 
    city.trim() && 
    pincode.trim() && 
    state.trim() && 
    country.trim()
  );
};

// Validation for Step Two
const validateStepTwo = () => {
  const { serviceCategory, yearsOfExperience, resume } = professionalData.value;
  
  isFormValid.value.stepTwo = !!(
    serviceCategory && 
    yearsOfExperience !== null && 
    resume
  );
};

// Update available states based on selected country
const updateStates = () => {
  const selectedCountry = professionalData.value.address.country;
  availableStates.value = STATES[selectedCountry] || [];
  
  // Reset state when country changes
  professionalData.value.address.state = "";
};

// File Upload Handler
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    // Validate file type and size
    const allowedTypes = ['application/pdf', 'application/doc', 'application/docx'];
    const maxSize = 5 * 1024 * 1024; // 5MB

    if (!allowedTypes.includes(file.type)) {
      errorMessage.value = "Invalid file type. Please upload PDF or DOC.";
      return;
    }

    if (file.size > maxSize) {
      errorMessage.value = "File size exceeds 5MB limit.";
      return;
    }

    professionalData.value.resume = file;
    validateStepTwo();
  }
};

// Navigate between steps
const nextStep = () => {
  if (currentStep.value === 1 && isFormValid.value.stepOne) {
    currentStep.value = 2;
    errorMessage.value = "";
  }
};

const prevStep = () => {
  if (currentStep.value === 2) {
    currentStep.value = 1;
    errorMessage.value = "";
  }
};

// Submit Handler
const handleSubmit = async () => {
  // Ensure user is authenticated and email verified
  if (!store.getters['module1/isAuthenticated']) {
    router.push('/?login=true');
    return;
  }

  if (!store.getters['module1/isEmailVerified']) {
    router.push('/verify-email');
    return;
  }

  if (!isFormValid.value.stepOne || !isFormValid.value.stepTwo) {
    errorMessage.value = "Please complete all required fields.";
    return;
  }

  const formData = new FormData();
  
  // Append basic data
  formData.append('fullName', professionalData.value.fullName);
  formData.append('phoneNumber', professionalData.value.phoneNumber);
  formData.append('serviceCategory', professionalData.value.serviceCategory);
  formData.append('yearsOfExperience', professionalData.value.yearsOfExperience);
  
  // Append address details
  Object.entries(professionalData.value.address).forEach(([key, value]) => {
    formData.append(`address.${key}`, value);
  });

  // Append resume
  if (professionalData.value.resume) {
    formData.append('resume', professionalData.value.resume);
  }

  try {
    const response = await axios.post("/api/professionals/signup", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    // Handle successful signup
    store.dispatch('professionals/registerProfessional', response.data);
    router.push('/professional-dashboard');
  } catch (error) {
    errorMessage.value = error.response?.data?.message || "Signup failed. Please try again.";
  }
};

const closeDialog = () => {
  if (route.query.login === "true") {
    // Remove login query parameter while preserving others
    const query = { ...route.query };
    delete query.login;
    router.push({
      path: route.path,
      query,
      hash: route.hash,
    });
  }
  store.dispatch("module1/toggleProfessionalSignupDialog", false);
};

watch(
  () => route.query.professionalSignup,
  (newValue) => {
    // Only update store if the value actually changed
    if (newValue === "true" && !isOpen.value) {
      store.dispatch("module1/toggleProfessionalSignupDialog", true);
    } else if (!newValue && isOpen.value) {
      store.dispatch("module1/toggleProfessionalSignupDialog", false);
    }
  },
  { immediate: true }
);

// Lifecycle
onMounted(() => {
  validateStepOne();
  validateStepTwo();

  // Check URL on mount and open dialog if needed
  if (route.query.professionalSignup === "true" && isOpen.value) {
    store.dispatch("module1/toggleProfessionalSignupDialog", true);
  }
});
</script>

<template>
    <BaseAuth
      :title="currentStep === 1 ? 'Professional Signup - Personal & Address Info' : 'Professional Signup - Service Details'"
      :is-open="isOpen"
      :on-close="closeDialog"
      @submit="currentStep === 1 ? nextStep() : handleSubmit"
    >
      <!-- Step One: Personal Information and Address -->
      <div v-if="currentStep === 1" class="form-group">
        <!-- Full Name -->
        <div class="form-item">
          <label for="fullName" class="form-label">Full Name</label>
          <input
            id="fullName"
            v-model="professionalData.fullName"
            type="text"
            class="form-input"
            placeholder="Enter your full name"
            required
            @input="validateStepOne"
          />
        </div>
  
        <!-- Phone Number -->
        <div class="form-item">
          <label for="phoneNumber" class="form-label">Phone Number</label>
          <input
            id="phoneNumber"
            v-model="professionalData.phoneNumber"
            type="tel"
            class="form-input"
            placeholder="Enter your phone number"
            required
            @input="validateStepOne"
          />
        </div>
  
        <!-- Locality -->
        <div class="form-item">
          <label for="locality" class="form-label">Locality/Street Address</label>
          <input
            id="locality"
            v-model="professionalData.address.locality"
            type="text"
            class="form-input"
            placeholder="Enter locality or street address"
            required
            @input="validateStepOne"
          />
        </div>
  
        <!-- City and Pincode Side by Side -->
        <div class="form-row">
          <div class="form-item">
            <label for="city" class="form-label">City</label>
            <input
              id="city"
              v-model="professionalData.address.city"
              type="text"
              class="form-input"
              placeholder="Enter city"
              required
              @input="validateStepOne"
            />
          </div>
          <div class="form-item">
            <label for="pincode" class="form-label">Pincode/Zip Code</label>
            <input
              id="pincode"
              v-model="professionalData.address.pincode"
              type="text"
              class="form-input"
              placeholder="Enter pincode or zip code"
              required
              @input="validateStepOne"
            />
          </div>
        </div>
  
        <!-- Country and State Side by Side -->
        <div class="form-row">
          <div class="form-item">
            <label for="country" class="form-label">Country</label>
            <select
              id="country"
              v-model="professionalData.address.country"
              class="form-input"
              required
              @change="updateStates(); validateStepOne()"
            >
              <option value="" disabled>Select Country</option>
              <option 
                v-for="country in COUNTRIES" 
                :key="country" 
                :value="country"
              >
                {{ country }}
              </option>
            </select>
          </div>
          <div class="form-item">
            <label for="state" class="form-label">State/Province</label>
            <select
              id="state"
              v-model="professionalData.address.state"
              class="form-input"
              :disabled="!professionalData.address.country"
              required
              @change="validateStepOne"
            >
              <option value="" disabled>Select State</option>
              <option 
                v-for="state in availableStates" 
                :key="state" 
                :value="state"
              >
                {{ state }}
              </option>
            </select>
          </div>
        </div>
      </div>

    <!-- Step Two: Service Details -->
    <div v-else-if="currentStep === 2" class="form-group">
      <!-- Service Category -->
      <div class="form-item">
        <label for="serviceCategory" class="form-label">Service Category</label>
        <select
          id="serviceCategory"
          v-model="professionalData.serviceCategory"
          class="form-input"
          required
          @change="validateStepTwo"
        >
          <option value="" disabled>Select a service category</option>
          <option 
            v-for="category in SERVICE_CATEGORIES" 
            :key="category" 
            :value="category"
          >
            {{ category }}
          </option>
        </select>
      </div>

      <!-- Years of Experience -->
      <div class="form-item">
        <label for="yearsOfExperience" class="form-label">Years of Experience</label>
        <input
          id="yearsOfExperience"
          v-model.number="professionalData.yearsOfExperience"
          type="number"
          min="0"
          max="50"
          class="form-input"
          placeholder="Enter years of experience"
          required
          @input="validateStepTwo"
        />
      </div>

      <!-- Resume Upload -->
      <div class="form-item">
        <label for="resume" class="form-label">Upload Resume (PDF/DOC)</label>
        <input
          id="resume"
          type="file"
          accept=".pdf,.doc,.docx"
          class="form-input"
          @change="handleFileUpload"
        />
      </div>
    </div>

    <!-- Error Message -->
    <p v-if="errorMessage" class="error-message" role="alert">
      {{ errorMessage }}
    </p>

    <!-- Navigation Buttons -->
    <div class="auth-actions">
      <!-- Step One Next Button -->
      <button 
        v-if="currentStep === 1"
        class="auth-button" 
        type="button"
        :disabled="!isFormValid.stepOne"
        @click="nextStep"
      >
        Next: Service Details
      </button>

      <!-- Step Two Previous and Submit Buttons -->
      <template v-else-if="currentStep === 2">
        <button 
          class="auth-button secondary" 
          type="button"
          @click="prevStep"
        >
          Previous
        </button>
        <button 
          class="auth-button" 
          type="submit"
          :disabled="!isFormValid.stepTwo"
        >
          Submit
        </button>
      </template>
    </div>
  </BaseAuth>
</template>

<style scoped>
.form-group {
  display: grid;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-item {
  display: flex;
  flex-direction: column;
}

.auth-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.auth-button.secondary {
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #ccc;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>