<script setup>
import BaseAuth from "@/components/Auth/BaseAuth.vue";
import { ref, computed, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";

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

const STATES = [
  "Maharashtra", "Karnataka", "Tamil Nadu", "Delhi", "Gujarat"
];

const COUNTRIES = ["India"];

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
    country: "India"
  },
  yearsOfExperience: null,
  resume: null
});

const errorMessages = ref({
  fullName: "",
  phoneNumber: "",
  "address.locality": "",
  "address.city": "",
  "address.pincode": "",
  "address.state": "",
  serviceCategory: "",
  yearsOfExperience: "",
  resume: ""
});

const currentStep = ref(1);
const isLoading = ref(false);
const submitError = ref("");
const availableStates = ref(STATES);
const hasAttemptedStepOne = ref(false);
const hasAttemptedStepTwo = ref(false);

const isOpen = computed(() => store.getters["module1/professionalSignupDialogVisible"]);

// Validation Methods
const validateStepOne = () => {
  let isValid = true;
  
  if (!hasAttemptedStepOne.value) {
    return true;
  }

  errorMessages.value = { ...errorMessages.value };

  // Name Validation
  if (!professionalData.value.fullName.trim()) {
    errorMessages.value.fullName = "Name is required";
    isValid = false;
  } else {
    errorMessages.value.fullName = "";
  }

  // Phone Number Validation
  const phoneRegex = /^(?!0)(?!(\+91))[6-9]\d{9}$/;
  if (!phoneRegex.test(professionalData.value.phoneNumber)) {
    errorMessages.value.phoneNumber = "Enter valid 10-digit phone number";
    isValid = false;
  } else {
    errorMessages.value.phoneNumber = "";
  }

  // Address Validations
  const addressFields = ['locality', 'city', 'pincode', 'state'];
  addressFields.forEach(field => {
    if (!professionalData.value.address[field]?.trim()) {
      errorMessages.value[`address.${field}`] = `${field} is required`;
      isValid = false;
    } else {
      errorMessages.value[`address.${field}`] = "";
    }
  });

  return isValid;
};

const validateStepTwo = () => {
  let isValid = true;

  if (!hasAttemptedStepTwo.value) {
    return true;
  }
  
  // Service Category Validation
  if (!professionalData.value.serviceCategory) {
    errorMessages.value.serviceCategory = "Please select a service category";
    isValid = false;
  } else {
    errorMessages.value.serviceCategory = "";
  }

  // Years of Experience Validation
  if (!professionalData.value.yearsOfExperience) {
    errorMessages.value.yearsOfExperience = "Experience is required";
    isValid = false;
  } else {
    errorMessages.value.yearsOfExperience = "";
  }

  // Resume Validation
  if (!professionalData.value.resume) {
    errorMessages.value.resume = "Resume is required";
    isValid = false;
  } else {
    errorMessages.value.resume = "";
  }

  return isValid;
};

// Computed Properties
const isStepOneValid = computed(() => validateStepOne());
const isStepTwoValid = computed(() => validateStepTwo());
const isFormValid = computed(() => ({
  stepOne: isStepOneValid.value,
  stepTwo: isStepTwoValid.value
}));

// File Upload Handler
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const maxSize = 5 * 1024 * 1024; // 5MB

    if (!allowedTypes.includes(file.type)) {
      errorMessages.value.resume = "Invalid file type. Please upload PDF or DOC.";
      return;
    }

    if (file.size > maxSize) {
      errorMessages.value.resume = "File size exceeds 5MB limit.";
      return;
    }

    professionalData.value.resume = file;
    if (hasAttemptedStepTwo.value) {
      errorMessages.value.resume = "";
    }
  }
};

const updateStates = () => {
  if (professionalData.value.address.country === "India") {
    availableStates.value = STATES;
  } else {
    availableStates.value = [];
  }
};

// Navigate between steps
const nextStep = () => {
  hasAttemptedStepOne.value = true;
  if (currentStep.value === 1 && isStepOneValid.value) {
    currentStep.value = 2;
    submitError.value = "";
  }
};

const prevStep = () => {
  if (currentStep.value === 2) {
    currentStep.value = 1;
    submitError.value = "";
    hasAttemptedStepTwo.value = false; // Reset step two validation
  }
};

// Submit Handler
const handleProfessionalSignup = async () => {
  if (isLoading.value) return;

  hasAttemptedStepTwo.value = true;

  // Ensure user is authenticated and email verified
  if (!store.getters['module1/isAuthenticated']) {
    router.push('/?login=true');
    return;
  }

  if (!store.getters['module1/isEmailVerified']) {
    closeDialog();
    router.push({
      query: {
        "verify-password": "true",
        email: store.getters['module1/currentUser']?.email,
      },
    });
    return;
  }

  if (!isStepOneValid.value || !isStepTwoValid.value) {
    submitError.value = "Please complete all required fields correctly.";
    return;
  }

  try {
    isLoading.value = true;
    submitError.value = "";
    const response = await store.dispatch('module1/registerProfessional', professionalData.value);
    router.push('/professional-dashboard');
  } catch (error) {
    submitError.value = error.response?.data?.message || "Signup failed. Please try again.";
  } finally {
    isLoading.value = false;
  }
};

const handleSubmit = () => {
  if (currentStep.value === 1) {
    nextStep();
  } else {
    handleProfessionalSignup();
  }
}

const closeDialog = () => {
  const query = { ...route.query };
  delete query.professionalSignup;
  
  router.push({
    path: route.path,
    query,
    hash: route.hash,
  });
  
  store.dispatch("module1/toggleProfessionalSignupDialog", false);
  // Reset all validation states
  hasAttemptedStepOne.value = false;
  hasAttemptedStepTwo.value = false;
  errorMessages.value = {
    fullName: "",
    phoneNumber: "",
    "address.locality": "",
    "address.city": "",
    "address.pincode": "",
    "address.state": "",
    serviceCategory: "",
    yearsOfExperience: "",
    resume: ""
  };
};

// Authentication Check
const checkAuthAndProceed = async () => {
    if (!store.getters['module1/isAuthenticated']) {
        router.push('/?login=true');
        return false;
    }

    if (!store.getters['module1/isEmailVerified']) {
        const email = store.getters['module1/currentUser']?.email;
        router.push(`/?verify-email=true&email=${email}`);
        return false;
    }

    return true;
};

watch(
  () => route.query.professionalSignup,
  async (newValue) => {
        if (newValue === "true") {
            if (await checkAuthAndProceed()){
              if (newValue === "true" && !isOpen.value) {
                store.dispatch("module1/toggleProfessionalSignupDialog", true);
              } else if (!newValue && isOpen.value) {
                store.dispatch("module1/toggleProfessionalSignupDialog", false);
              }
            }
  }
},
  { immediate: true }
);

// Lifecycle
onMounted(() => {
  if (route.query.professionalSignup === "true" && !isOpen.value) {
    store.dispatch("module1/toggleProfessionalSignupDialog", true);
  }
});
</script>

<template>
  <BaseAuth
    :title="currentStep === 1 ? 'Professional Signup - Personal & Address Info' : 'Professional Signup - Service Details'"
    :is-open="isOpen"
    :on-close="closeDialog"
    @submit="handleSubmit"
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
          :class="['form-input', { error: errorMessages.fullName }]"
          placeholder="Enter your full name"
          required
          @input="validateStepOne"
        />
        <span v-if="errorMessages.fullName" class="error-text">
          {{ errorMessages.fullName }}
        </span>
      </div>

      <!-- Phone Number -->
      <div class="form-item">
        <label for="phoneNumber" class="form-label">Phone Number</label>
        <input
          id="phoneNumber"
          v-model="professionalData.phoneNumber"
          type="tel"
          :class="['form-input', { error: errorMessages.phoneNumber }]"
          placeholder="Enter your phone number"
          required
          @input="validateStepOne"
        />
        <span v-if="errorMessages.phoneNumber" class="error-text">
          {{ errorMessages.phoneNumber }}
        </span>
      </div>

      <!-- Locality -->
      <div class="form-item">
        <label for="locality" class="form-label">Locality/Street Address</label>
        <input
          id="locality"
          v-model="professionalData.address.locality"
          type="text"
          :class="['form-input', { error: errorMessages['address.locality'] }]"
          placeholder="Enter locality or street address"
          required
          @input="validateStepOne"
        />
        <span v-if="errorMessages['address.locality']" class="error-text">
          {{ errorMessages['address.locality'] }}
        </span>
      </div>

      <!-- City and Pincode Side by Side -->
      <div class="form-row">
        <div class="form-item">
          <label for="city" class="form-label">City</label>
          <input
            id="city"
            v-model="professionalData.address.city"
            type="text"
            :class="['form-input', { error: errorMessages['address.city'] }]"
            placeholder="Enter city"
            required
            @input="validateStepOne"
          />
          <span v-if="errorMessages['address.city']" class="error-text">
            {{ errorMessages['address.city'] }}
          </span>
        </div>
        <div class="form-item">
          <label for="pincode" class="form-label">Pincode/Zip Code</label>
          <input
            id="pincode"
            v-model="professionalData.address.pincode"
            type="text"
            :class="['form-input', { error: errorMessages['address.pincode'] }]"
            placeholder="Enter pincode or zip code"
            required
            @input="validateStepOne"
          />
          <span v-if="errorMessages['address.pincode']" class="error-text">
            {{ errorMessages['address.pincode'] }}
          </span>
        </div>
      </div>

      <!-- Country and State Side by Side -->
      <div class="form-row">
        <div class="form-item">
          <label for="country" class="form-label">Country</label>
          <select
            id="country"
            v-model="professionalData.address.country"
            :class="['form-input', { error: errorMessages['address.country'] }]"
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
            :class="['form-input', { error: errorMessages['address.state'] }]"
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
          <span v-if="errorMessages['address.state']" class="error-text">
            {{ errorMessages['address.state'] }}
          </span>
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
          :class="['form-input', { error: errorMessages.serviceCategory }]"
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
        <span v-if="errorMessages.serviceCategory" class="error-text">
          {{ errorMessages.serviceCategory }}
        </span>
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
          :class="['form-input', { error: errorMessages.yearsOfExperience }]"
          placeholder="Enter years of experience"
          required
          @input="validateStepTwo"
        />
        <span v-if="errorMessages.yearsOfExperience" class="error-text">
          {{ errorMessages.yearsOfExperience }}
        </span>
      </div>

      <!-- Resume Upload -->
      <div class="form-item">
        <label for="resume" class="form-label">Upload Resume (PDF/DOC)</label>
        <input
          id="resume"
          type="file"
          accept=".pdf,.doc,.docx"
          :class="['form-input', { error: errorMessages.resume }]"
          @change="handleFileUpload"
        />
        <span v-if="errorMessages.resume" class="error-text">
          {{ errorMessages.resume }}
        </span>
      </div>
    </div>

    <!-- Submit Error Message -->
    <div v-if="submitError" class="error-container">
      <p class="error-text" role="alert">
        {{ submitError }}
      </p>
    </div>

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
          :disabled="!isFormValid.stepTwo || isLoading"
        >
        {{ isLoading ? 'Submitting...' : 'Submit' }}
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

.error-container {
  min-height: 4rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-text {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.form-input.error {
  border-color: #dc2626;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>