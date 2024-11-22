import { createApp } from 'vue'
import '@/style.css'
import App from '@/App.vue'
import store from '@/store'
import router from '@/plugins/router'
import '@/plugins/axios'
import vue3GoogleLogin from 'vue3-google-login'

const CLIENT_ID = "254167476653-3oa77013v6spbelqcbtusbehl4pv5kbc.apps.googleusercontent.com"

createApp(App).use(vue3GoogleLogin, {clientId: CLIENT_ID}).use(store).use(router).mount('#app')

