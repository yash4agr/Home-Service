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
      isOpen: false
    },
    UserProfileDialog: {
      isOpen: false,
      user: null
    },
    VerifyProfessionalDialog: {
      isOpen: false
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
      revenueData: [],
      days: []
    }
  },
  
  // Services data
  services: {
    list: [],
    categories: [],
    isLoading: false,
    error: null
  },

  // User data
  users: [],
  isLoading: false,
  error: null,
  selectedUser: null,
  userDetails: {
    address: null,
    professionalDetails: null,
    reviews: [],
    stats: {
      totalServices: 0,
      pendingServices: 0,
      averageRating: 0
    }
  },

  // Professionals
  professionals: [],
}