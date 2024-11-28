export default {
  isApproved: false,
  profile: null,
  dashboard: {
    stats: {
      totalRequests: 0,
      avg_rating: 0,
      activeServices: 0,
      completionRate: 0
    },
    chartData: {
      serviceData: [],
      revenueData: [],
      days: []
    }
  },
  bookings: {
    pending_request: [],
    accepted_request: [],
    past_request: []
  }
}