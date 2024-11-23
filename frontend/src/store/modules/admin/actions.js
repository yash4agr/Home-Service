import axios from 'axios';
// Dialogs actions
const openServiceDialog = ({ commit }, service = null) => {
  commit('SET_SERVICE_DIALOG', { isOpen: true, serviceToEdit: service });
  }
    
const closeServiceDialog = ({ commit }) => {
  commit('SET_SERVICE_DIALOG', { isOpen: false, serviceToEdit: null });
  }
    
const toggleServiceManagementDialog = ({ commit }, value) => {
  commit('SET_SERVICE_MANAGEMENT_DIALOG', value);
  }

// Dashboard data actions
const fetchDashboardData = async ({ commit }) => {
  try {
    // Replace with actual API call
    const response = await fetch('/api/dashboard/data')
    const data = await response.json()
    
    commit('SET_DASHBOARD_STATS', data.stats)
    commit('SET_DASHBOARD_CHART_DATA', data.chartData)
    return data
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    throw error
  }
}

// Service actions
const fetchServices = async ({ commit }) => {
  try {
    commit('SET_SERVICES_LOADING', true)

    const response = await axios.get('/api/services')
    const data = await response.data
    
    commit('SET_SERVICES_LIST', data)
    return data
  } catch (error) {
    commit('SET_SERVICES_ERROR', error.message)
    throw error
  } finally {
    commit('SET_SERVICES_LOADING', false)
  }
}
const fetchCategories = async ({ commit }) => {
  try {
    // Replace with actual API call
    const response = await axios.get('/api/services/categories')
    const data = await response.data
    
    commit('SET_SERVICES_CATEGORIES', data)
    return data
  } catch (error) {
    console.error('Error fetching categories:', error)
    throw error
  }
}

const upsertService = async ({ dispatch }, { serviceData, serviceId }) => {
  try {
    const method = serviceId ? 'PUT' : 'POST';

    // Construct the endpoint dynamically
    const endpoint = serviceId ? `/api/services?service_id=${serviceId}` : '/api/services';

    const response = await axios({
      method,
      url: endpoint,
      data: serviceData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    // Refresh services list after update
    await dispatch('fetchServices');
    return response.data;
  } catch (error) {
    console.error('Error upserting service:', error);
    throw error;
  }
};

const deleteService = async ({ dispatch }, serviceId) => {
  try {
    // Replace with actual API call
    await axios.delete(`/api/services/${serviceId}`)
    
    // Refresh services list after deletion
    await dispatch('fetchServices');
    return;
  } catch (error) {
    console.error('Error deleting service:', error)
    throw error
  }
}
    


export default {
  openServiceDialog,
  closeServiceDialog,
  toggleServiceManagementDialog,

  fetchDashboardData,

  fetchServices,
  fetchCategories,
  upsertService,
  deleteService
    }