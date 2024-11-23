
const SET_SERVICE_DIALOG = (state, { isOpen, serviceToEdit }) => {
  state.dialogs.serviceDialog.isOpen = isOpen
  state.dialogs.serviceDialog.serviceToEdit = serviceToEdit
  }
    
const SET_SERVICE_MANAGEMENT_DIALOG = (state, isOpen) => {
  state.dialogs.serviceManagementDialog.isOpen = isOpen
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


export default {
  SET_SERVICE_DIALOG,
  SET_SERVICE_MANAGEMENT_DIALOG,
  SET_DASHBOARD_STATS,
  SET_DASHBOARD_CHART_DATA,
  SET_SERVICES_LIST,
  SET_SERVICES_CATEGORIES,
  SET_SERVICES_LOADING,
  SET_SERVICES_ERROR
    }