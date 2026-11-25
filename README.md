# SharePoint AI Experiments and Demo Lab

<!-- yarkr:badges:start -->
[![Indexed on Yarkr](https://api.yarkr.com/functions/v1/api/api/v1/badges/repos/zrosenfield/sharepoint-ai-skills/version.svg)](https://yarkr.com/arks/zrosenfield/sharepoint-ai-skills)
<!-- yarkr:badges:end -->

Experimental AI skills, prototypes, automated demo scripts, sample data, and presentation assets for AI in Microsoft 365 SharePoint.

> **Repository status:** This is an incubation and demonstration repository. For maintained community skills, use the official [PnP SharePoint Skills repository](https://github.com/pnp/sharepoint-skills).

## What Is Here

| Path | Purpose |
|---|---|
| [`Skills/`](./Skills/) | Experimental skills that have not graduated to the PnP repository |
| [`solutions/`](./solutions/) | Complete experimental solution kits with setup, deployment assets, sample data, and linked skills |
| [`demos/`](./demos/) | Demo documentation, sample data, golden outputs, and presentation assets |
| [`tools/scripts/`](./tools/scripts/) | Automated browser demo scripts |
| [`tools/`](./tools/) | The Playwright-based demo runner and local configuration examples |

## Skill Lifecycle

Skills in this repository are prototypes. They may change quickly and should be reviewed before production use.

1. New ideas are developed and demonstrated here.
2. Mature skills are contributed to [`pnp/sharepoint-skills`](https://github.com/pnp/sharepoint-skills).
3. After graduation, the local copy is removed and [`Skills/README.md`](./Skills/README.md) links to the maintained PnP version.

Do not submit updates for graduated skills here. Open issues and pull requests against the official repository instead.

## Experimental Solutions

Solutions are complete samples to try on a test site, not production-ready or supported products. Their installable skills remain in `Skills/`; each kit links to those canonical sources.

Start with [Client Hub for SharePoint](./solutions/client-hub-for-sharepoint/): three related lists for clients, projects, and activity, with deployment/removal scripts, formatting, fictional sample data, an optional dashboard, and five Copilot skills. Its [manual setup guide](./solutions/client-hub-for-sharepoint/SETUP.md) is an alternative to running the browser script.

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

<!-- yarkr:install:start -->
## Install with Yarkr

This repo is indexed on [Yarkr](https://yarkr.com/arks/zrosenfield/sharepoint-ai-skills) as the ark [zrosenfield/sharepoint-ai-skills](https://yarkr.com/arks/zrosenfield/sharepoint-ai-skills), so its skills install into Claude Code, Codex, Cursor and other agent harnesses with one command.

### CLI

Install the whole ark, which Yarkr keeps equal to this repo:

```bash
npx yarkr-cli sync zrosenfield/sharepoint-ai-skills
```

Or add individual skills:

```bash
npx yarkr-cli add skill:zrosenfield/sharepoint-ai-skills/authoring-sharepoint-markdown
npx yarkr-cli add skill:zrosenfield/sharepoint-ai-skills/autoresearch
npx yarkr-cli add skill:zrosenfield/sharepoint-ai-skills/brainstorming-design-docs
```

No Node.js? `curl -fsSL https://yarkr.com/install.sh | sh` (macOS, Linux) or `irm https://yarkr.com/install.ps1 | iex` (Windows PowerShell) installs `yarkr` as a standalone binary; then type `yarkr` in place of `npx yarkr-cli`.

### MCP

Connect your agent to the ark over MCP:

```bash
npx yarkr-cli mcp add zrosenfield/sharepoint-ai-skills
```

Or point any MCP client at `https://api.yarkr.com/functions/v1/api/mcp/o/zrosenfield/sharepoint-ai-skills`.
<!-- yarkr:install:end -->

## Contributing

Contributions are welcome for experimental skills, solution kits, demo scenarios, runner improvements, and sample assets. Stable reusable skills should be proposed to [PnP SharePoint Skills](https://github.com/pnp/sharepoint-skills).

## License

[MIT](./LICENSE) © 2026 [zrosenfield](https://github.com/zrosenfield)

## Disclaimer

This repository is provided as-is for learning and experimentation. It is not official Microsoft documentation. Verify behavior against current Microsoft Learn documentation before production deployment.
