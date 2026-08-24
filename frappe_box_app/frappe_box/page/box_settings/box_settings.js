// Box identity/IP (for SSH) and saved WiFi networks (Flutter's Phase 7),
// available from Desk instead of the phone.
frappe.pages["box-settings"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Box Settings"),
		single_column: true,
	});

	page.add_inner_button(__("Dashboard"), () => frappe.set_route("box-dashboard"));
	page.add_inner_button(__("Add Network"), () => show_add_network_dialog(page));

	page.$box_info = $('<div class="box-info-section mt-2"></div>').appendTo(page.body);
	page.$wifi_networks = $('<div class="wifi-networks-section mt-4"></div>').appendTo(page.body);

	load_box_info(page);
	load_wifi_networks(page);
};

function load_box_info(page) {
	frappe.call({
		method: "frappe_box_app.api.box_info",
		callback: (r) => render_box_info(page, r.message),
	});
}

function render_box_info(page, info) {
	page.$box_info.html(`
		<h5>${__("Box Info")}</h5>
		${info_row(__("Box name"), frappe.utils.escape_html(info.box_name || "—"))}
		${info_row(__("Serial number"), frappe.utils.escape_html(info.serial_number || "—"))}
		${info_row(__("IP address"), frappe.utils.escape_html(info.ip_address))}
		${info_row(
			__("Provisioning"),
			info.provisioning_complete ? __("Complete") : __("Incomplete")
		)}
		<p class="text-muted small mt-2">
			${__("SSH into your box with")}: <code>ssh &lt;user&gt;@${frappe.utils.escape_html(info.ip_address)}</code>
		</p>
	`);
}

function info_row(label, value) {
	return `
		<div class="d-flex justify-content-between align-items-center py-2 border-bottom">
			<span class="text-muted">${label}</span>
			<span class="font-weight-bold">${value}</span>
		</div>
	`;
}

function load_wifi_networks(page) {
	frappe.call({
		method: "frappe_box_app.api.list_wifi_networks",
		callback: (r) => render_wifi_networks(page, r.message.networks),
		error: () => render_wifi_networks_error(page),
	});
}

function render_wifi_networks_error(page) {
	page.$wifi_networks.html(`
		<h5>${__("WiFi Networks")}</h5>
		<p class="text-muted">${__("Couldn't reach the box's WiFi daemon.")}</p>
	`);
}

function render_wifi_networks(page, networks) {
	const rows = networks.length
		? networks.map(wifi_network_row).join("")
		: `<p class="text-muted">${__("No saved networks yet.")}</p>`;
	page.$wifi_networks.html(`<h5>${__("WiFi Networks")}</h5>${rows}`);
	page.$wifi_networks.find(".forget-network-btn").on("click", function () {
		forget_network(page, $(this).attr("data-ssid"));
	});
}

function wifi_network_row(ssid) {
	const escaped_ssid = frappe.utils.escape_html(ssid);
	return `
		<div class="d-flex justify-content-between align-items-center py-2 border-bottom">
			<span><i class="fa fa-wifi text-muted mr-2"></i>${escaped_ssid}</span>
			<button class="btn btn-xs btn-default forget-network-btn" data-ssid="${escaped_ssid}">
				${__("Forget")}
			</button>
		</div>
	`;
}

function forget_network(page, ssid) {
	frappe.confirm(__("Forget network {0}?", [ssid]), () => {
		frappe.call({
			method: "frappe_box_app.api.remove_wifi_network",
			args: { ssid },
			callback: () => load_wifi_networks(page),
		});
	});
}

function show_add_network_dialog(page) {
	const dialog = new frappe.ui.Dialog({
		title: __("Add WiFi Network"),
		fields: [
			{ fieldname: "ssid", label: __("Network name"), fieldtype: "Data", reqd: 1 },
			{ fieldname: "password", label: __("Password"), fieldtype: "Password", reqd: 1 },
		],
		primary_action_label: __("Add"),
		primary_action(values) {
			frappe.call({
				method: "frappe_box_app.api.add_wifi_network",
				args: values,
				callback: () => {
					dialog.hide();
					load_wifi_networks(page);
				},
			});
		},
	});
	dialog.show();
}
