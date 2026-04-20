import { createRouter, createWebHistory } from 'vue-router'

const base = import.meta.env.BASE_URL || '/frontend/setup/'
console.log('Router base:', base) // confirm in browser console

let router = createRouter({
	history: createWebHistory('/frontend/'),
	routes: [
		// { path: '/setup', name: 'Welcome', component: () => import('@/pages/Welcome.vue') },
		{ path: '/setup/scan', name: 'SSDScan', component: () => import('@/pages/SSDScan.vue') },
		// {
		// 	path: '/setup/config',
		// 	name: 'SSDConfig',
		// 	component: () => import('@/pages/SSDConfig.vue'),
		// },
		// {
		// 	path: '/setup/complete',
		// 	name: 'SetupComplete',
		// 	component: () => import('@/pages/SetupComplete.vue'),
		// },
	],
})

export default router
