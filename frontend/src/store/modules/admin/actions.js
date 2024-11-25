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
const toggleUserManagementDialog = ({ commit }, value) => {
  commit('SET_USER_MANAGEMENT_DIALOG', value);
  }
const toggleUserProfileDialog = ({ commit }, { isOpen, user = null }) => {
  commit('SET_USER_PROFILE_DIALOG', { isOpen, user });
}
const toggleVerifyProfessionalDialog = ({ commit }, value) => {
  commit('SET_PROFESSINAL_VERIFY_DIALOG', value);
  }
  
// Dashboard data actions
const fetchDashboardData = async ({ commit }) => {
  try {
    // Replace with actual API call
    const response = await axios.get('/api/admin/dashboard')
    const data = await response.data
    
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
    const response = await axios.get('/api/services/categories')
    const data = await response.data
    
    commit('SET_SERVICES_CATEGORIES', data)
    return data
  } catch (error) {
    console.error('Error fetching categories:', error.message)
    throw error
  }
}

const upsertService = async ({ dispatch }, { serviceData, serviceId }) => {
  try {
    const method = serviceId ? 'PUT' : 'POST';
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
    console.error('Error upserting service:', error.message);
    throw error;
  }
};

const deleteService = async ({ dispatch }, serviceId) => {
  try {
    await axios.delete(`/api/services/${serviceId}`)
    
    // Refresh services list after deletion
    await dispatch('fetchServices');
    return;
  } catch (error) {
    console.error('Error deleting service:', error.message)
    throw error
  }
}
    
// User Actions
const fetchUsers = async ({ commit }) => {
  try {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    
    const response = await axios.get('/api/admin/users')
    commit('SET_USERS', response.data)
  } catch (error) {
    commit('SET_ERROR', 'Failed to fetch users')
    console.error('Error fetching users:', error.message)
  } finally {
    commit('SET_LOADING', false)
  }
}

const fetchUser = async ({ commit }, user) => {
  try {
    commit('SET_LOADING', true)
    const response = await axios.get(`/api/admin/users?user_id=${user.id}`)
    commit('UPDATE_USER', response.data)
  } catch (error) {
    console.error('Error fetching user:', error.message)
  } finally {
    commit('SET_LOADING', false)
  }
}

const toggleUserBan = async ({ commit, dispatch }, { userId, isBanned }) => {
  try {
    commit('SET_ERROR', null)
    
    const response = await axios.patch(`/api/admin/users/${userId}/ban-status`, {
      is_banned: isBanned
    })
    
    commit('UPDATE_USER', response.data)
    dispatch('fetchUsers')
  } catch (error) {
    commit('SET_ERROR', 'Failed to update user ban status')
    console.error('Error updating user ban status:', error.message)
    throw error
  }
}
const fetchUserAddress = async ({ commit }, userId) => {
  try {
    const response = await axios.get(`/api/admin/users/${userId}/address`)
    commit('SET_USER_ADDRESS', response.data)
    return response.data
  } catch (error) {
    console.error('Error fetching user address:', error.message)
    return null
  }
}
const fetchProfessionalDetails = async ({ commit }, userId) => {
  try {
    const response = await axios.get(`/api/admin/professionals/${userId}/details`)
    commit('SET_PROFESSIONAL_DETAILS', response.data)
    return response.data
  } catch (error) {
    console.error('Error fetching professional details:', error.message)
    return null
  }
}
const fetchProfessionalReviews = async ({ commit }, userId) => {
  try {
    const response = await axios.get(`/api/admin/professionals/${userId}/reviews`)
    commit('SET_PROFESSIONAL_REVIEWS', response.data)
    return response.data
  } catch (error) {
    console.error('Error fetching professional reviews:', error.message)
    return []
  }
}

// Export Monthly Report
const exportMonthlyReport = async ({ commit }) => {
  try {
    const response = await axios.get(`/api/admin/exportMonthlyReport`)
    if (response.data) {
      return response.data
    }
    return false
  } catch (error) {
    console.error('Error exporting monthly report:', error.message)
    throw error
  }
}

const fetchProfessionalUsers = async ({ commit }) => {
  try {
    commit('SET_LOADING', true)
    const response = await axios.get('/api/admin/professionals-pending')
    commit('SET_PROFESSIONALS', response.data)
  } catch (error) {
    commit('SET_ERROR', error.message)
    console.error('Error fetching professionals:', error)
  } finally {
    commit('SET_LOADING', false)
  }
}

const updateProfessionalStatus = async ({ commit, dispatch  }, {professionalId, isApproved}) => {
  try {
    commit('SET_LOADING', true)
    await axios.put(`/api/admin/verify?user_id=${professionalId}&approved=${isApproved}`)
    await dispatch('fetchProfessionalUsers')
  } catch (error) {
    commit('SET_ERROR', error.message)
    console.error('Error updating user profile:', error)
  } finally {
    commit('SET_LOADING', false)
  }
}

const downloadProfessionalResume = async ({ commit }, professionalId) => {
  try {
    const response = await axios.get(`/api/admin/professionals/${professionalId}/resume`, {
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    
    // Get filename from response headers or use default
    const contentDisposition = response.headers['content-disposition']
    const fileName = contentDisposition
      ? contentDisposition.split('filename=')[1].replace(/['"]/g, '')
      : `resume-${professionalId}.pdf`
    
    link.setAttribute('download', fileName)
    document.body.appendChild(link)
    link.click()
    
    // Cleanup
    link.remove()
    window.URL.revokeObjectURL(url)
    
  } catch (error) {
    commit('SET_ERROR', error.message)
    throw error
  }
}



export default {
  openServiceDialog,
  closeServiceDialog,
  toggleServiceManagementDialog,
  toggleUserManagementDialog,
  toggleUserProfileDialog,
  toggleVerifyProfessionalDialog,


  fetchDashboardData,

  fetchServices,
  fetchCategories,
  upsertService,
  deleteService,

  fetchUsers,
  fetchUser,
  toggleUserBan,
  fetchUserAddress,
  fetchProfessionalDetails,
  fetchProfessionalReviews,
  exportMonthlyReport,
  fetchProfessionalUsers,
  updateProfessionalStatus,
  downloadProfessionalResume,

    }