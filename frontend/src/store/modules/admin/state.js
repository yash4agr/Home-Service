export default {
  dialogs: {
    serviceDialog: {
      isOpen: false,
      serviceToEdit: null
    },
    serviceManagementDialog: {
      isOpen: false
    },
    UserManagementDialog: {
      isOpen: true
    }
  },
  
  // Dashboard data
  dashboard: {
    stats: {
      totalRequests: 0,
      activeServices: 0,
      completionRate: 0
    },
    chartData: {
      serviceData: [],
      revenueData: []
    }
  },
  
  // Services data
  services: {
    list: [],
    categories: [],
    isLoading: false,
    error: null
  }
}