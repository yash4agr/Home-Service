<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { Chart } from 'chart.js/auto'

import RequestsDialog from '../components/Professionals/Requests.vue'

// Store
const store = useStore()


// Refs for charts
const serviceChartRef = ref(null)
const revenueChartRef = ref(null)
const serviceChart = ref(null)
const revenueChart = ref(null)


// Computed properties from store
const isApproved = computed(() => store.getters['professional/isApproved'])
const stats = computed(() => store.getters['professional/dashboardStats'])


// Method to fetch dashboard data
const fetchDashboardData = async () => {
    try {
        const response = await store.dispatch('professional/fetchDashboardData')
        updateCharts(response.chartData)
    } catch (error) {
        console.error('Error fetching dashboard data:', error)
    }
}

const isRequestsOpen = ref(false)
const title = ref('')
const requests = ref([])

const updateRequestsOpen = (value) => {
    isRequestsOpen.value = value
}

const handleNewRequests = async() => {
    title.value = "New Requests"
    isRequestsOpen.value = true
    try {
        const response = await store.dispatch('professional/get_bookings', 'pending_request')
        requests.value = response.pending_request
    } catch (error) {
        console.error('Error fetching new requests:', error)
        requests.value = []
    }
}

const handlePendingServices = async() => {
    title.value = "Pending Services"
    isRequestsOpen.value = true
    try {
        const response = await store.dispatch('professional/get_bookings', 'accepted_request')
        requests.value = response.accepted_request
    } catch (error) {
        console.error('Error fetching pending services:', error)
        requests.value = []
    }
}

const handlePastServices = async() => {
    title.value = "Past Services"
    isRequestsOpen.value = true
    try {
        const response = await store.dispatch('professional/get_bookings', 'past_request')
        requests.value = response.past_request
    } catch (error) {
        console.error('Error fetching past services:', error)
        requests.value = []
    }
}


// Initialize Charts
const initializeCharts = () => {
    if (!serviceChartRef.value || !revenueChartRef.value) return
    const chartData = store.getters['professional/dashboardChartData']
    // Service Requests Chart
    const serviceCtx = serviceChartRef.value.getContext('2d')
    serviceChart.value = new Chart(serviceCtx, {
        type: 'line',
        data: {
            labels: chartData.days || ['1', '2', '3', '4', '5', '6', '7'],
            datasets: [{
                label: 'Service Requests',
                data: chartData.serviceData || [],
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
            labels: chartData.days || ['1', '2', '3', '4', '5', '6', '7'],
            datasets: [{
                label: 'Ratings',
                data: chartData.revenueData || [],
                backgroundColor: '#dfbc90'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Last 7 Days Ratings'
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

// Lifecycle Hook
onMounted(async () => {
    await store.dispatch('professional/status')
    initializeCharts()
    try {
        const dashboardData = await store.dispatch('professional/fetchDashboardData')
        updateCharts(dashboardData.chartData)
    } catch (error) {
        console.error('Error initializing dashboard:', error)
    }

    const refreshInterval = setInterval(() => {
        store.dispatch('professional/fetchDashboardData')
            .then(data => updateCharts(data.chartData))
            .catch(error => console.error('Error refreshing dashboard:', error))
    }, 5 * 60 * 1000)

    // Clean up interval on component unmount
    return () => clearInterval(refreshInterval)
})

</script>

<!-- Dashboard.vue -->
<template>
    <div class="dashboard">
        <template v-if="!isApproved">
            <div class="not_approved">
                <h2>You are not approved yet</h2>
            </div>
        </template>
        <template v-else>
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
                        <button class="action-btn" @click="handleNewRequests">
                            View Requests
                        </button>
                        <button class="action-btn" @click="handlePendingServices">
                            Pending Services
                        </button>
                        <button class="action-btn" @click="handlePastServices">
                            Past Services
                        </button>
                        <RequestsDialog :is-bookings-open="isRequestsOpen" :bookings-data="requests" :title="title"
                            @update:is-bookings-open="updateRequestsOpen" />
                    </div>

                    <!-- Stats Cards -->
                    <div class="stats-cards">
                        <div class="stat-card">
                            <h3>Average Rating</h3>
                            <p>{{ stats.avg_rating }}</p>
                        </div>
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
        </template>
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

.not_approved {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    background-color: var(--container-color);
    padding: 1.5rem;
    border-radius: var(--auth-border-radius);
    height: 90vh;
    width: 100%;
    align-items: center;
    justify-content: center;
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