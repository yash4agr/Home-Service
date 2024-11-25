<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { Chart } from 'chart.js/auto'

import ServiceDialog from '@/components/Service/service.vue'
import ServiceManagementDialog from '@/components/Service/ServiceManagementDialog.vue'
import UserManagementDialog from '@/components/User/UserDialog.vue'
import VerifyProfessionalDialog from '@/components/User/VerifyProfessional.vue'

// Store
const store = useStore()


// Refs for charts
const serviceChartRef = ref(null)
const revenueChartRef = ref(null)
const serviceChart = ref(null)
const revenueChart = ref(null)

// Dialog state management
const isServiceDialogOpen = ref(false)
const isManageDialogOpen = ref(false)
const selectedService = ref(null)

// Timer
const isDisabled = ref(false)
const timeLeft = ref(0)

// Computed properties from store
const isAdmin = computed(() => store.getters['admin/isAdmin'])
const stats = computed(() => store.getters['admin/dashboardStats'])
const serviceDialogState = computed(() => store.getters['admin/serviceDialogState'])
const serviceManagementDialogState = computed(() => store.getters['admin/serviceManagementDialogState'])
const userManagementDialogState = computed(() => store.getters['admin/userManagementDialogState'])
const VerifyProfessionalDialogDialogState = computed(() => store.getters['admin/verifyProfessionalDialogState'])


// Computed Properties
// const isAdmin = computed(() => true) // Replace with actual admin check from store
const userData = computed(() => store.getters['module1/currentUser'])


// Method to fetch dashboard data
const fetchDashboardData = async () => {
  try {
    const response = await store.dispatch('dashboard/fetchData')
    stats.value = response.stats
    updateCharts(response.chartData)
  } catch (error) {
    console.error('Error fetching dashboard data:', error)

  }
}

const startTimer = () => {
  timeLeft.value = 30
  const timer = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      clearInterval(timer)
      isDisabled.value = false
    }
  }, 1000)
}

const buttonText = computed(() => {
  return timeLeft.value > 0 
    ? `Export Monthly Report in ${timeLeft.value}s` 
    : 'Export Monthly Report'
})

// Initialize Charts
const initializeCharts = () => {
  if (!serviceChartRef.value || !revenueChartRef.value) return

  // Service Requests Chart
  const serviceCtx = serviceChartRef.value.getContext('2d')
  serviceChart.value = new Chart(serviceCtx, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'Service Requests',
        data: [12, 19, 3, 5, 2, 3],
        borderColor: '#dfbc90',
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: 'Service Requests Over Time'
        }
      }
    }
  })

  // Revenue/Rating Chart
  const revenueCtx = revenueChartRef.value.getContext('2d')
  revenueChart.value = new Chart(revenueCtx, {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: isAdmin.value ? 'Revenue' : 'Ratings',
        data: [65, 59, 80, 81, 56, 55],
        backgroundColor: '#dfbc90'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: isAdmin.value ? 'Monthly Revenue' : 'Monthly Ratings'
        }
      }
    }
  })
}

// Update Charts with New Data
const updateCharts = (data) => {
  if (serviceChart.value && data?.serviceData) {
    serviceChart.value.data.datasets[0].data = data.serviceData
    serviceChart.value.update()
  }
  
  if (revenueChart.value && data?.revenueData) {
    revenueChart.value.data.datasets[0].data = data.revenueData
    revenueChart.value.update()
  }
}

// Quick Action Handlers
const handleCreateService = () => {
  store.dispatch('admin/openServiceDialog')
}

const closeServiceDialog = () => {
  isServiceDialogOpen.value = false
  selectedService.value = null
}


const handleManageService = () => {
  store.dispatch('admin/toggleServiceManagementDialog', true)
}

const handleServiceEdit = (service) => {
  store.dispatch('admin/toggleServiceManagementDialog', false)
  store.dispatch('admin/openServiceDialog', service)
}

const handleManageUsers = () => {
  store.dispatch('admin/toggleUserManagementDialog', true)
}

const handleUserProfile = (user) => {
  store.commit('admin/SET_USER_PROFILE_DIALOG', { isOpen: true, user });
}
const handleCloseUserProfile = () => {
  store.commit('admin/SET_USER_PROFILE_DIALOG', { isOpen: false, user: null });
}

const handleExportReport = async () => {
  try {
    isDisabled.value = true
    
    await store.dispatch('admin/exportMonthlyReport')
    alert('Monthly report will be sent to your email within the next 24 hours')
    
    startTimer()
  } catch (error) {
    console.error('Error generating report:', error)
    isDisabled.value = false
  }
}

const handleVerifyProfessionals = () => {
  store.dispatch('admin/toggleVerifyProfessionalDialog', true)
}

// Lifecycle Hook
onMounted(async () => {
  initializeCharts()
  
  try {
    const dashboardData = await store.dispatch('admin/fetchDashboardData')
    updateCharts(dashboardData.chartData)
  } catch (error) {
    console.error('Error initializing dashboard:', error)
  }

  const refreshInterval = setInterval(() => {
    store.dispatch('admin/fetchDashboardData')
      .then(data => updateCharts(data.chartData))
      .catch(error => console.error('Error refreshing dashboard:', error))
  }, 5 * 60 * 1000)

  // Clean up interval on component unmount
  return () => clearInterval(refreshInterval)
})

// Expose methods if needed for template or parent components
defineExpose({
  fetchDashboardData,
  initializeCharts,
  updateCharts,
  handleCreateService,
  handleManageUsers,
  handleExportReport,
  handleVerifyProfessionals
})
</script>

<!-- Dashboard.vue -->
<template>
  <div class="dashboard">
    <div class="dashboard__container">
      <!-- Chart Section -->
      <div class="dashboard__charts">
        <div class="chart-container">
          <canvas ref="serviceChartRef"></canvas>
        </div>
        <div class="chart-container">
          <canvas ref="revenueChartRef"></canvas>
        </div>
      </div>

      <!-- Actions Section -->
      <div class="dashboard__actions">
        <div class="actions__header">
          <h2>Quick Actions</h2>
        </div>
        <div class="actions__buttons">
          <!-- Admin Buttons -->
          <template v-if="isAdmin">
            <button class="action-btn" @click="handleCreateService">
              Create Service
            </button>
            <button class="action-btn" @click="handleManageService">
              Manage Service
            </button>
            <button class="action-btn" @click="handleManageUsers">
              Manage Users
            </button>
            <button class="action-btn" @click="handleExportReport" :disabled="isDisabled">
              {{ buttonText }}
            </button>
            <button class="action-btn" @click="handleVerifyProfessionals">
              Verify Professionals
            </button>
            <ServiceDialog 
              :is-open="serviceDialogState.isOpen"
              :serviceToEdit="serviceDialogState.serviceToEdit"
              @close="store.dispatch('admin/closeServiceDialog')"
            />
            <ServiceManagementDialog
              :is-open="serviceManagementDialogState.isOpen"
              @close="store.dispatch('admin/toggleServiceManagementDialog', false)"
              @edit="handleServiceEdit"
            />
            <UserManagementDialog
              :is-open="userManagementDialogState.isOpen"
              @close="store.dispatch('admin/toggleUserManagementDialog', false)"
              @show-profile="handleUserProfile"
            />
            <VerifyProfessionalDialog
              :is-open="VerifyProfessionalDialogDialogState.isOpen"
              @close="store.dispatch('admin/toggleVerifyProfessionalDialog', false)"
              @show-profile="handleUserProfile"
            />
          </template>

          <!-- Professional Buttons -->
          <template v-else>
            <button class="action-btn" @click="handleViewRequests">
              View Requests
            </button>
            <button class="action-btn" @click="handlePendingServices">
              Pending Services
            </button>
            <button class="action-btn" @click="handleUpdateProfile">
              Update Profile
            </button>
            <button class="action-btn" @click="handleViewReviews">
              View Reviews
            </button>
          </template>
        </div>

        <!-- Stats Cards -->
        <div class="stats-cards">
          <div class="stat-card">
            <h3>Total Requests</h3>
            <p>{{ stats.totalRequests }}</p>
          </div>
          <div class="stat-card">
            <h3>Active Services</h3>
            <p>{{ stats.activeServices }}</p>
          </div>
          <div class="stat-card">
            <h3>Completion Rate</h3>
            <p>{{ stats.completionRate }}%</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  padding: 2rem;
  padding-top: 5rem;
  background-color: var(--bg-color);
  min-height: calc(100vh - var(--header-height));
}

.dashboard__container {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard__charts {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  background-color: var(--container-color);
  padding: 1.5rem;
  border-radius: var(--auth-border-radius);
}

.chart-container {
  width: 100%;
  height: 300px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.dashboard__actions {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.actions__header h2 {
  font-size: var(--h2-font-size);
  color: var(--text-color);
  margin-bottom: 1rem;
}

.actions__buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-btn {
  width: 100%;
  padding: 1rem;
  background-color: var(--accent-color);
  color: var(--white);
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color var(--transition-speed);
  font-weight: var(--font-medium);
}

.action-btn:hover {
  background-color: var(--secondary-color);
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.stat-card {
  background-color: var(--container-color);
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: center;
}

.stat-card h3 {
  font-size: 0.875rem;
  color: var(--text-color-light);
  margin-bottom: 0.5rem;
}

.stat-card p {
  font-size: 1.25rem;
  font-weight: var(--font-semi-bold);
  color: var(--primary-color);
}

@media screen and (max-width: 1023px) {
  .dashboard__container {
    grid-template-columns: 1fr;
  }
  
  .dashboard__charts {
    order: 2;
  }
  
  .dashboard__actions {
    order: 1;
  }
}

@media screen and (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }
  
  .chart-container {
    height: 250px;
  }
}
</style>