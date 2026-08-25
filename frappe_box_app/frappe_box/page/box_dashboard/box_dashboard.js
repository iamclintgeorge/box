// Live CPU/memory/storage stats, mirroring the Flutter app's dashboard
// (specs/phase-6-sign-in-and-dashboard.md) for whoever is on Desk instead.
frappe.pages["box-dashboard"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Box Dashboard"),
		single_column: true,
	});

	page.add_inner_button(__("Refresh"), () => load_stats(page));
	page.add_inner_button(__("Settings"), () => frappe.set_route("box-settings"));

	page.$stats = $('<div class="box-dashboard-stats mt-2"></div>').appendTo(page.body);

	load_stats(page);
	setInterval(() => load_stats(page), 5000);
};

function load_stats(page) {
	frappe.call({
		method: "frappe_box_app.api.system_stats",
		callback: (r) => render_stats(page, r.message),
		error: () => render_stats_error(page),
	});
}

function render_stats(page, stats) {
	page.$stats.html(
		[
			stat_row(__("CPU temperature"), format_temperature(stats.cpu_temperature_celsius)),
			stat_row(__("Memory"), format_usage(stats.memory)),
			stat_row(__("Storage"), format_usage(stats.storage)),
		].join("")
	);
}

function render_stats_error(page) {
	page.$stats.html(`<p class="text-muted">${__("Couldn't reach your Frappe Box.")}</p>`);
}

function stat_row(label, value) {
	return `
		<div class="d-flex justify-content-between align-items-center py-2 border-bottom">
			<span class="text-muted">${label}</span>
			<span class="font-weight-bold">${value}</span>
		</div>
	`;
}

function format_temperature(celsius) {
	return celsius == null ? "—" : `${celsius.toFixed(1)} °C`;
}

function format_usage(usage) {
	return `${format_bytes(usage.used_bytes)} / ${format_bytes(usage.total_bytes)}`;
}

function format_bytes(bytes) {
	return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
}
