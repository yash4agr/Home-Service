import axios from 'axios';

const status = async ({ commit }) => {
  try {
    const response = await axios.get('/api/professionals/status')
    commit('SET_APPROVAL_STATUS', response.data.is_approved)
    return response.data.is_approved
  } catch (error) {
    console.error('Error checking professional status:', error)
    return false
  }
}
const fetchProfile = async ({ commit }) => {
  try {
    const response = await axios.get('/api/professionals/profile')
    commit('SET_PROFILE', response.data)
    return response.data
  } catch (error) {
    console.error('Error fetching professional profile:', error)
    throw error
  }
}

const fetchDashboardData = async ({ commit }) => {
  try {
    const response = await axios.get('/api/professionals/dashboard')
    const data = {
      stats: response.data.stats,
      chartData: {
        serviceData: response.data.serviceData,
        revenueData: response.data.revenueData,
        days: response.data.days
      }
    }
    commit('SET_DASHBOARD_STATS', data.stats)
    commit('SET_DASHBOARD_CHART_DATA', data.chartData)
    return data
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    throw error
  }
}

const get_bookings = async ({ commit }, type = 'pending_request') => {
  try {
    const response = await axios.get(`/api/professionals/bookings?type=${type}`)
    commit('SET_BOOKINGS', { 
      type, 
      bookings: response.data[type] 
    })
    return response.data
  } catch (error) {
    console.error(`Error fetching ${type} bookings:`, error)
    throw error
  }
}

export default {
  status,
  fetchProfile,
  fetchDashboardData,
  get_bookings,
}