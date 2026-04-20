import './index.css'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
// import router from './router'
import router from './router/index'
import App from './App.vue'

import { Button, setConfig, frappeRequest, resourcesPlugin } from 'frappe-ui'

let app = createApp(App)

setConfig('resourceFetcher', frappeRequest)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(resourcesPlugin)

app.component('Button', Button)
app.mount('#app')

router.beforeEach((to, from) => {
	console.log('Router navigating to:', to.fullPath)
})
