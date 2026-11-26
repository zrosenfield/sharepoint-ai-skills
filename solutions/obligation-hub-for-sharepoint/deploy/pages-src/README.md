# Page sources

The sources for the 7 hub pages in [`../pages/`](../pages/). Each page is one self-contained HTML file: its CSS and JavaScript, the icon sprite and a fictional sample snapshot (built from [`../../sample-data/`](../../sample-data/)) are inlined. On a site, the page reads live list data through its `ka-livedata-manifest`. It shows the sample snapshot, labelled as sample, until live data arrives.

```
python3 build.py
```

This rebuilds `../pages/<Name>.template.html` and `../pages/tokens.json` from `src/`. It checks that each inline script parses in Node, that every JSON block parses, that each page is under 300 KB with no external URLs or forbidden APIs, and that every `{{TOKEN}}` is documented. You need Python 3 and Node.

| Folder | Holds |
|---|---|
| `src/shared/` | `base.css`, `core.js` (live-data and snapshot loading, formatting, helpers), the icon sprite, the hub mark and the footer |
| `src/pages/` | `<Name>.body.html`, `<Name>.css` and `<Name>.js` for each page |
| `src/data/` | The sample snapshots, written by `snapshots.py` |

The pages have no navigation of their own. The SharePoint site navigation is the hub's only navigation, and the deploy script adds its links. Tokens such as `{{SITE_URL}}`, `{{LISTID_OBLIGATIONS}}` and `{{WORKFLOW_PROMPT_CAPTURE_NEW}}` are filled at install time by `../deploy-obligation-hub.js` or `../cowork/fill_pages.py`. See `../pages/tokens.json`.
