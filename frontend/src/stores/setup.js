import { defineStore } from 'pinia'
import { ref } from 'vue'
import { call } from 'frappe-ui'

export const useSetupStore = defineStore('setup', () => {
	const disks = ref([])
	const selectedDisks = ref([])
	const poolName = ref('tank')
	const loading = ref(false)
	const error = ref('')

	async function scanDisks() {
		loading.value = true
		error.value = ''
		try {
			const result = await call('box.api.disk.scan_disks')
			console.log('result from scan_disk', result)
			disks.value = result.disks || []
		} catch (e) {
			error.value = e.message || 'Failed to scan disks'
		} finally {
			loading.value = false
		}
	}

	async function configureZFS() {
		loading.value = true
		error.value = ''
		try {
			await call('box.api.disk.configure_zfs', {
				pool_name: poolName.value,
				devices: JSON.stringify(selectedDisks.value),
			})
		} catch (e) {
			error.value = e.message || 'ZFS configuration failed'
			throw e
		} finally {
			loading.value = false
		}
	}

	async function completeSetup() {
		await call('box.api.system.complete_setup')
	}

	return {
		disks,
		selectedDisks,
		poolName,
		loading,
		error,
		scanDisks,
		configureZFS,
		completeSetup,
	}
})
