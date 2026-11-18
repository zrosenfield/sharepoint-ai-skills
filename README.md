# SharePoint AI Experiments and Demo Lab

Experimental AI skills, prototypes, automated demo scripts, sample data, and presentation assets for AI in Microsoft 365 SharePoint.

> **Repository status:** This is an incubation and demonstration repository. For maintained community skills, use the official [PnP SharePoint Skills repository](https://github.com/pnp/sharepoint-skills).

## What Is Here

| Path | Purpose |
|---|---|
| [`Skills/`](./Skills/) | Experimental skills that have not graduated to the PnP repository |
| [`demos/`](./demos/) | Demo documentation, sample data, golden outputs, and presentation assets |
| [`tools/scripts/`](./tools/scripts/) | Automated browser demo scripts |
| [`tools/`](./tools/) | The Playwright-based demo runner and local configuration examples |

## Skill Lifecycle

Skills in this repository are prototypes. They may change quickly and should be reviewed before production use.

1. New ideas are developed and demonstrated here.
2. Mature skills are contributed to [`pnp/sharepoint-skills`](https://github.com/pnp/sharepoint-skills).
3. After graduation, the local copy is removed and [`Skills/README.md`](./Skills/README.md) links to the maintained PnP version.

Do not submit updates for graduated skills here. Open issues and pull requests against the official repository instead.

## Running Demos

Demo scripts use site-agnostic defaults. Put real SharePoint URLs in the gitignored `tools/demo.vars.json`; never edit a `.demo` file to insert a tenant or site URL.

```powershell
npm install
npm run demo -- tools/scripts/23-program-portfolio-review/23-program-portfolio-review.demo
```

Most scripts support `--setup`, the default demo section, and `--reset`.

## Prerequisites

- Microsoft 365 tenant with a Copilot license
- SharePoint contributor permissions for setup and skill installation
- Node.js for the automated demo runner

## Contributing

Contributions are welcome for experimental skills, demo scenarios, runner improvements, and sample assets. Stable reusable skills should be proposed to [PnP SharePoint Skills](https://github.com/pnp/sharepoint-skills).

## License

[MIT](./LICENSE) © 2026 [zrosenfield](https://github.com/zrosenfield)

## Disclaimer

This repository is provided as-is for learning and experimentation. It is not official Microsoft documentation. Verify behavior against current Microsoft Learn documentation before production deployment.
