// Services
const isApproved = state => state.isApproved;
const profile = state => state.profile;

// stats
const dashboardStats = state => state.dashboard.stats;
const dashboardChartData = state => state.dashboard.chartData;

const pendingRequests = state => state.bookings.pending_request;

const acceptedRequests = state => state.bookings.accepted_request;
const pastRequests = state => state.bookings.past_request;

export default {
    isApproved,
    profile,
    dashboardStats,
    dashboardChartData,
    pendingRequests,
    acceptedRequests,
    pastRequests,
    }