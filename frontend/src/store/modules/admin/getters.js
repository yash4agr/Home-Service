const isAdmin = state => state.userRole === 'admin' || true;

// Dialogs
const serviceDialogState = state => state.dialogs.serviceDialog;
const serviceManagementDialogState = state => state.dialogs.serviceManagementDialog;
const userManagementDialogState = state => state.dialogs.UserManagementDialog;
const userProfileDialogState = state => state.dialogs.UserProfileDialog;
const verifyProfessionalDialogState = state => state.dialogs.VerifyProfessionalDialog;

// stats
const dashboardStats = state => state.dashboard.stats;
const dashboardChartData = state => state.dashboard.chartData;

// services
const servicesList = state => state.services.list;
const serviceCategories = state => state.services.categories;
const isServicesLoading = state => state.services.isLoading;

// user
const usersList = state => state.users;
const isUsersLoading = state => state.isLoading;
const isUserLoading = state => state.isLoading;
const getUserById = state => id => state.users.find(user => user.id === id);
const getError = state => state.error;

const ProfessionalsList = state => state.professionals;
const professionalTotalServices = state => userId => state.userDetails.stats.totalServices;
const professionalPendingServices = state => userId => state.userDetails.stats.pendingServices;
const professionalAverageRating = state => userId => state.userDetails.stats.averageRating;

export default {
    isAdmin,

    serviceDialogState,
    serviceManagementDialogState,
    userManagementDialogState,
    userProfileDialogState,
    verifyProfessionalDialogState,

    dashboardStats,
    dashboardChartData,

    servicesList,
    serviceCategories,
    isServicesLoading,

    usersList,
    isUsersLoading,
    isUserLoading,
    getUserById,
    getError,
    professionalTotalServices,
    professionalPendingServices,
    professionalAverageRating,
    ProfessionalsList,
    };