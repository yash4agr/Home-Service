import { createRouter, createWebHistory } from "vue-router";

const routes = [
    {path : '', name: 'home', component: () => import('@/views/Home.vue')},
    {path: '/login', name: 'login', component: () => import('@/views/Login.vue')},
    {path: '/register', name: 'register', component: () => import('@/views/RegisterUser.vue')},
    {path: '/forgot-password', name: 'forgot-password', component: () => import('@/views/Forgotpass.vue')}
]


const router = createRouter({
    routes,
    history: createWebHistory(),
})


export default router