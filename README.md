# SharePoint AI Demos

A curated library of AI skills, site-generation plans, and end-to-end demo setups for the latest AI features in Microsoft 365 SharePoint.

> **Status:** Active — new content added regularly.

---

## What's Inside

| Folder | Purpose | Intended use |
|---|---|---|
| [`skills/`](./skills/) | AI skills for use in SharePoint — ready-made instructions you can drop into Copilot or an agent | Download and reuse in your own tenant |
| [`site-plans/`](./site-plans/) | `plan.md` files describing SharePoint site structures, pages, and content — feed them to an AI to generate a new site | Download and adapt for your scenario |
| [`demos/`](./demos/) | End-to-end demo setups with sample content, configuration steps, and screenshots | Reference and walkthrough — not intended for direct reuse |

---

## Getting Started

Each item has its own `README.md` (or is self-contained as a `plan.md`) with:
- What the skill or plan does
- Prerequisites (licenses, permissions, tenant config)
- How to use or adapt it

No special tooling required — everything is Markdown, readable directly on GitHub.

---

## Prerequisites (general)

- Microsoft 365 tenant with **Copilot licenses** (where noted per item)
- SharePoint admin or site owner permissions
- Familiarity with the [Microsoft 365 admin center](https://admin.microsoft.com) and [SharePoint admin center](https://admin.sharepoint.com)

---

## Contributing

Contributions and corrections are welcome!

1. Fork the repo and create a branch: `git checkout -b demo/your-demo-name`
2. Add your demo in the appropriate subfolder, following the existing `README.md` structure
3. Open a pull request with a short description of what the demo covers

Please keep demos focused, concise, and free of tenant-specific credentials or internal URLs.

---

## License

[MIT](./LICENSE) © 2026 [zrosenfield](https://github.com/zrosenfield)

---

## Disclaimer

These demos are provided as-is for learning and experimentation. They are not official Microsoft documentation. Always verify against the latest [Microsoft Learn](https://learn.microsoft.com) docs before deploying to production.
