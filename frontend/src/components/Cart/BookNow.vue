<script setup>
import BaseAuth from "@/components/Auth/BaseAuth.vue";
import { ref, computed, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";

const router = useRouter();
const route = useRoute();
const store = useStore();

// Constants for time slots
const TIME_SLOTS = Array.from({ length: 13 }, (_, i) => {
    const hour = i + 9; // 9 AM to 9 PM
    return `${hour}:00`;
});

const STATES = {
    "India": [
        "Chhattisgarh"
    ]
};

// Form State
const bookingData = ref({
    fullName: "",
    phoneNumber: "",
    address: {
        locality: "",
        city: "",
        pincode: "",
        state: "",
    },
    serviceDate: "",
    serviceTime: "",
    paymentMethod: "cash",
});

const PAYMENT_METHODS = [{
    id: 'cash',
    label: 'Pay by Cash',
    description: 'Pay in cash after service completion',
    icon: '💵'
}];

const currentStep = ref(1);
const errorMessage = ref("");
const isFormValid = ref({
    stepOne: false,
    stepTwo: false
});
const availableStates = ref(STATES["India"] || []);

// Computed
const isOpen = computed(() => store.getters['module2/isBookingDialogOpen']);
const minDate = computed(() => {
    const date = new Date();
    date.setDate(date.getDate());
    return date.toISOString().split('T')[0];
});

// Validation
const validateStepOne = () => {
    const { fullName, phoneNumber } = bookingData.value;
    const { locality, city, pincode, state } = bookingData.value.address;

    isFormValid.value.stepOne = !!(
        fullName.trim() &&
        phoneNumber.trim() &&
        locality.trim() &&
        city.trim() &&
        pincode.trim() &&
        state.trim()
    );
};

const validateStepTwo = () => {
    isFormValid.value.stepTwo = !!(
        bookingData.value.serviceDate &&
        bookingData.value.serviceTime &&
        bookingData.value.paymentMethod
    );
};

// Navigation
const nextStep = async () => {
    if (currentStep.value === 1 && isFormValid.value.stepOne) {
        // Check if we serve at this location
        try {
            // Get cart items to pass along with pincode
            const cartItems = store.getters['module2/cartItems'];
            const serviceIds = cartItems.map(item => item.id);
            console.log(cartItems, serviceIds)
            // Dispatch serviceability check with service IDs and pincode
            const isServiceable = await store.dispatch(
                'module2/checkServiceability', 
                {
                    pincode: bookingData.value.address.pincode,
                    serviceIds: serviceIds
                }
            );

            if (!isServiceable) {
                errorMessage.value = "Sorry, we don't serve these services at your location yet.";
                return;
            }

            currentStep.value = 2;
            errorMessage.value = "";
        } catch (error) {
            errorMessage.value = "Unable to verify serviceability. Please try again.";
        }
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
    if (!isFormValid.value.stepTwo) {
        errorMessage.value = "Please select service date and time.";
        return;
    }
    try {
        // Create booking with all necessary data
        const bookingResponse = await store.dispatch('module2/createBooking', {
            ...bookingData.value,
            services: store.getters['module2/cartItems'],
            paymentMethod: 'cash'
        });

        closeDialog();
        cartItems.value = [];
        cartItems.value.update()
        router.push('/?bookings=true');
    } catch (error) {
        errorMessage.value = error.response?.data?.message || "Booking failed. Please try again.";
    }
};

// Dialog Controls
const closeDialog = () => {
    // const query = { ...route.query };
    // delete query.booking;
    // router.push({
    //     path: route.path,
    //     query,
    //     hash: route.hash,
    // });
    store.dispatch("module2/toggleBookingDialog", false);
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

// Lifecycle
watch(
    () => route.query.booking,
    async (newValue) => {
        if (newValue === "true") {
            if (await checkAuthAndProceed()) {
                store.dispatch("module2/toggleBookingDialog", true);
            }
        }
    },
    { immediate: true }
);
</script>

<template>
    <BaseAuth :title="currentStep === 1 ? 'Booking Details' : 'Schedule Service'" :is-open="isOpen"
        :on-close="closeDialog" @submit="currentStep === 1 ? nextStep() : handleSubmit">
        <!-- Step One: Personal Information and Address -->
        <div v-if="currentStep === 1" class="form-group">
            <!-- Basic Info -->
            <div class="form-row">
                <div class="form-item">
                    <label for="fullName" class="form-label">Full Name</label>
                    <input id="fullName" v-model="bookingData.fullName" type="text" class="form-input"
                        placeholder="Enter your full name" required @input="validateStepOne" />
                </div>
                <div class="form-item">
                    <label for="phoneNumber" class="form-label">Phone Number</label>
                    <input id="phoneNumber" v-model="bookingData.phoneNumber" type="tel" class="form-input"
                        placeholder="Enter phone number" required @input="validateStepOne" />
                </div>
            </div>

            <!-- Address -->
            <div class="form-item">
                <label for="locality" class="form-label">Locality/Street</label>
                <input id="locality" v-model="bookingData.address.locality" type="text" class="form-input"
                    placeholder="Enter locality or street" required @input="validateStepOne" />
            </div>

            <div class="form-row">
                <div class="form-item">
                    <label for="city" class="form-label">City</label>
                    <input id="city" v-model="bookingData.address.city" type="text" class="form-input"
                        placeholder="Enter city" required @input="validateStepOne" />
                </div>
                <div class="form-item">
                    <label for="pincode" class="form-label">Pincode</label>
                    <input id="pincode" v-model="bookingData.address.pincode" type="text" class="form-input"
                        placeholder="Enter pincode" required @input="validateStepOne" />
                </div>
            </div>

            <div class="form-item">
                <label for="state" class="form-label">State</label>
                <select id="state" v-model="bookingData.address.state" class="form-input" required
                    @change="validateStepOne">
                    <option value="" disabled>Select State</option>
                    <option v-for="state in availableStates" :key="state" :value="state">
                        {{ state }}
                    </option>
                </select>
            </div>
        </div>

        <!-- Step Two: Schedule -->
        <div v-else class="form-group">
            <div class="form-item">
                <label for="serviceDate" class="form-label">Service Date</label>
                <input id="serviceDate" v-model="bookingData.serviceDate" type="date" class="form-input" :min="minDate"
                    required @input="validateStepTwo" />
            </div>

            <div class="form-item">
                <label for="serviceTime" class="form-label">Service Time</label>
                <select id="serviceTime" v-model="bookingData.serviceTime" class="form-input" required
                    @change="validateStepTwo">
                    <option value="" disabled>Select time</option>
                    <option v-for="time in TIME_SLOTS" :key="time" :value="time">
                        {{ time }}
                    </option>
                </select>
            </div>

            <div class="payment-section">
                <h3 class="payment-title">Payment Method</h3>
                <div class="payment-info">
                    <span class="payment-icon">💵</span>
                    <div class="payment-details">
                        <span class="payment-label">Pay by Cash</span>
                        <span class="payment-description">Pay in cash after service completion</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="error-message" role="alert">
            {{ errorMessage }}
        </p>

        <!-- Navigation Buttons -->
        <div class="auth-actions">
            <button v-if="currentStep === 1" class="auth-button" type="button" :disabled="!isFormValid.stepOne"
                @click="nextStep">
                Next: Schedule Service
            </button>

            <template v-else>
                <button class="auth-button secondary" type="button" @click="prevStep">
                    Previous
                </button>
                <button class="auth-button" type="submit" :disabled="!isFormValid.stepTwo" @click="handleSubmit">
                    Confirm Booking
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
    background-color: var(--surface-color);
    color: var(--text-color);
    border: 1px solid var(--border-color);
}

.payment-section {
  /* padding: 1.25rem; */
  border-radius: 0.75rem;
  /* margin-top: 1.5rem; */
}

.payment-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--text-color);
}

.payment-info {
  display: flex;
  align-items: center;
  padding: 0.875rem;
  background: var(--secondary-color);
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
}

.payment-icon {
  font-size: 1.25rem;
  margin-right: 0.75rem;
  display: flex;
  align-items: center;
}

.payment-details {
  flex: 1;
}

.payment-label {
  display: block;
  font-weight: 500;
  color: var(--text-color);
  margin-bottom: 0.25rem;
}

.payment-description {
  font-size: 0.875rem;
  color: var(--text-secondary-color);
}

@media (max-width: 600px) {
    .form-row {
    grid-template-columns: 1fr;
  }
  
  .payment-section {
    padding: 1rem;
  }
  
  .payment-info {
    padding: 0.75rem;
  }
}
</style>