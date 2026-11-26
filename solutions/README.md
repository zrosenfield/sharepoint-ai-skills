# Experimental Solutions

Complete, reusable sample kits for trying SharePoint scenarios on a test site. "Complete" describes the supplied components, not production readiness: these are experiments, provided as-is and unsupported.

| Solution | What it explores | Status |
|---|---|---|
| [Client Hub for SharePoint](./client-hub-for-sharepoint/) | A lightweight client tracker built from related lists, formatting, and optional Copilot skills and a dashboard | Experimental; tenant validation required |
| [Obligation Hub for SharePoint](./obligation-hub-for-sharepoint/) | Turns signed contracts into a tracked register of obligations, owners, due dates, evidence, digests, and recurring work | Experimental; tenant validation required |

## Where things belong

Use `solutions/<solution-name>/` when the deliverable is a working scenario kit rather than an individual skill or a presentation walkthrough. Keep setup/removal instructions, deployment assets, formatting, and fictional sample data together.

Installable skills live in the repository's top-level [`Skills/`](../Skills/), with links from the solution. Do not maintain a second skill copy in the kit. Browser demo-runner scripts still belong in [`tools/scripts/`](../tools/scripts/), and recordings or walkthrough assets belong in [`demos/`](../demos/).

Each solution README must explain prerequisites, experimental limitations, setup, and removal. Keep tenant-specific configuration and real client data out of the repository. Validate a solution on a disposable site before considering any production use.
