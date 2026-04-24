<div align="center">
  <a href="https://frappe.io">
    <img src=".github/logo.svg" height="80" width="80" alt="Frappe Box Logo">
  </a>
  <h2>Frappe Box</h2>

**Plug and Play Decentralized Frappe Bench**

</div>

> [!Warning]  
> Frappe Box is in beta. It is strongly advised to take backups in production use.

## Frappe Box

Frappe Box is a Decentralized platform to host Frappe Bench and Frappe Apps, allowing the users to store their data in their own storage solutions.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app box
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/box
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

<div align="center" style="padding-top: 0.75rem;">
	<a href="https://frappe.io" target="_blank">
		<picture>
			<source media="(prefers-color-scheme: dark)" srcset="https://frappe.io/files/Frappe-white.png">
			<img src="https://frappe.io/files/Frappe-black.png" alt="Frappe Technologies" height="28"/>
		</picture>
	</a>
</div>
