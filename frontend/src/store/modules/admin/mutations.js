
const SET_SERVICE_DIALOG = (state, { isOpen, serviceToEdit }) => {
  state.dialogs.serviceDialog.isOpen = isOpen
  state.dialogs.serviceDialog.serviceToEdit = serviceToEdit
  }
    
const SET_SERVICE_MANAGEMENT_DIALOG = (state, isOpen) => {
  state.dialogs.serviceManagementDialog.isOpen = isOpen
  }
const SET_USER_MANAGEMENT_DIALOG = (state, isOpen) => {
  state.dialogs.UserManagementDialog.isOpen = isOpen
  }
const SET_USER_PROFILE_DIALOG = (state, { isOpen, user = null }) => {
  state.dialogs.UserProfileDialog.isOpen = isOpen
  state.dialogs.UserProfileDialog.user = user
  }
const SET_PROFESSINAL_VERIFY_DIALOG = (state, isOpen) => {
  state.dialogs.VerifyProfessionalDialog.isOpen = isOpen
  }

const SET_DASHBOARD_STATS = (state, stats) => {
  state.dashboard.stats = stats
  }
    
const SET_DASHBOARD_CHART_DATA = (state, chartData) => {
  state.dashboard.chartData = chartData
  }


const SET_SERVICES_LIST = (state, services) => {
  state.services.list = services
  }
    
const SET_SERVICES_CATEGORIES = (state, categories) => {
  state.services.categories = categories
  }
    
const SET_SERVICES_LOADING = (state, isLoading) => {
  state.services.isLoading = isLoading
  }
    
const SET_SERVICES_ERROR = (state, error) => {
  state.services.error = error
  }

// User Mutations
const SET_USERS = (state, users) => {
  state.users = users
  }
const SET_SELECTED_USERS = (state, user) => {
  state.selectedUser = user
  }
const SET_LOADING = (state, isLoading) => {
  state.isLoading = isLoading
  }
const SET_ERROR = (state, error) => {
  state.error = error
  }
const UPDATE_USER = (state, updatedUser) => {
  const index = state.users.findIndex(user => user.id === updatedUser.id)
    if (index !== -1) {
      state.users.splice(index, 1, updatedUser)
    }
  }
const SET_USER_ADDRESS = (state, address) => {
  state.userDetails.address = address
  }

const SET_PROFESSIONAL_DETAILS = (state, details) => {
  state.userDetails.professionalDetails = details
  }
const SET_PROFESSIONAL_REVIEWS = (state, reviews) => {
  state.userDetails.reviews = reviews
  }
const SET_PROFESSIONAL_STATS = (state, stats) => {
  state.userDetails.stats = {
    ...state.userDetails.stats,
    ...stats
  }
}
const SET_PROFESSIONALS = (state, professionals) => {
  state.professionals = professionals
}




export default {
  SET_SERVICE_DIALOG,
  SET_SERVICE_MANAGEMENT_DIALOG,
  SET_USER_MANAGEMENT_DIALOG,
  SET_USER_PROFILE_DIALOG,
  SET_PROFESSINAL_VERIFY_DIALOG,
  SET_DASHBOARD_STATS,
  SET_DASHBOARD_CHART_DATA,
  SET_SERVICES_LIST,
  SET_SERVICES_CATEGORIES,
  SET_SERVICES_LOADING,
  SET_SERVICES_ERROR,

  SET_USERS,
  SET_LOADING,
  SET_ERROR,
  UPDATE_USER,
  SET_SELECTED_USERS,
  SET_USER_ADDRESS,
  SET_PROFESSIONAL_DETAILS,
  SET_PROFESSIONAL_REVIEWS,
  SET_PROFESSIONAL_STATS,
  SET_PROFESSIONALS,
    }