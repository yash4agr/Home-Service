const SET_APPROVAL_STATUS = (state, status) => {
  state.isApproved = status
}
    
const SET_PROFILE = (state, profile) => {
  state.profile = profile
}
    
const SET_DASHBOARD_STATS = (state, stats) => {
  state.dashboard.stats = stats
  }

const SET_DASHBOARD_CHART_DATA = (state, chartData) => {
  state.dashboard.chartData = chartData
  }
    
const SET_BOOKINGS = (state, { type, bookings }) => {
  state.bookings[type] = bookings
}

export default {
  SET_APPROVAL_STATUS,
  SET_PROFILE,
  SET_DASHBOARD_STATS,
  SET_DASHBOARD_CHART_DATA,
  SET_BOOKINGS,
    }