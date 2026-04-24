<template>
	<div class="min-h-screen flex flex-col items-center justify-center p-8">
		<!-- <StepIndicator :current="2" :total="4" /> -->

		<h1 class="text-3xl font-bold mt-6 mb-2">Scanning for drives</h1>
		<p class="text-gray-500 mb-8">We found the following block devices on your system.</p>

		<!-- Scan trigger -->
		<Button
			v-if="!store.disks.length && !store.loading"
			variant="solid"
			size="lg"
			@click="store.scanDisks()"
		>
			Scan now
		</Button>

		<!-- <LoadingIndicator v-if="store.loading" class="w-10 h-10 mt-6" /> -->

		<!-- <ErrorMessage v-if="store.error" :message="store.error" class="mt-4" /> -->

		<!-- Disk list -->
		<div v-if="store.disks.length" class="w-full max-w-2xl mt-6 space-y-3">
			<!-- <DiskCard
				v-for="disk in store.disks"
				:key="disk.name"
				:disk="disk"
				:selected="store.selectedDisks.includes('/dev/' + disk.name)"
				@toggle="toggleDisk(disk)"
			/> -->
		</div>

		<!-- Navigation -->
		<div class="flex gap-4 mt-8" v-if="store.disks.length">
			<Button variant="outline" @click="$router.push('/')">← Back</Button>
			<Button
				variant="solid"
				:disabled="!store.selectedDisks.length"
				@click="$router.push('/config')"
			>
				Configure selected ({{ store.selectedDisks.length }}) →
			</Button>
		</div>
	</div>
</template>

<script setup>
import { useSetupStore } from '@/stores/setup'
// import StepIndicator from '@/components/StepIndicator.vue'
// import DiskCard from '@/components/DiskCard.vue'

const store = useSetupStore()

// Auto-scan on mount
import { onMounted } from 'vue'
onMounted(() => {
	if (!store.disks.length) store.scanDisks()
})

function toggleDisk(disk) {
	const path = '/dev/' + disk.name
	const idx = store.selectedDisks.indexOf(path)
	if (idx === -1) store.selectedDisks.push(path)
	else store.selectedDisks.splice(idx, 1)
}
</script>
