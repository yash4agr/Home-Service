const isAdmin = state => state.userRole === 'admin' || true;

// Dialogs
const serviceDialogState = state => state.dialogs.serviceDialog;
const serviceManagementDialogState = state => state.dialogs.serviceManagementDialog;
const userManagementDialogState = state => state.dialogs.UserManagementDialog;

// stats
const dashboardStats = state => state.dashboard.stats;
const dashboardChartData = state => state.dashboard.chartData;

// services
const servicesList = state => state.services.list;
const serviceCategories = state => state.services.categories;
const isServicesLoading = state => state.services.isLoading;

export default {
    isAdmin,

    serviceDialogState,
    serviceManagementDialogState,
    userManagementDialogState,

    dashboardStats,
    dashboardChartData,

    servicesList,
    serviceCategories,
    isServicesLoading,
    };