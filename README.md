# HHMI Web Redesign

Working files for the HHMI / Janelia website redesign.

## What's here

| Path | What it is |
| --- | --- |
| `prototype/HHMI_Janelia_Prototype_9.27.html` | The 9.27 clickable prototype (single-page app, hash routes like `#/janelia/science`). Open it in a browser. |
| `studies/sitemap.html` | Sitemap: both menu bars, every page under its section, cross-section links, and issues to review. |
| `studies/menu.html` | Full site menu: a black mega menu containing every page, over a full-screen hero image. |
| `studies/footer.html` | The menu page plus a mega footer built from the menu, and a particle HHMI wordmark revealed as the page lifts away like a curtain. |
| `data/pages.json` | Every page found by crawling the prototype: title, heading, breadcrumb, menus, and outbound links. |
| `data/open-questions.json` | The 36 Janelia open questions with their field and theme. |
| `tools/` | Scripts that crawl the prototype and generate the sitemap and menu pages. |

## Site at a glance

- About 159 unique pages, no broken links.
- **HHMI header (every page):** Programs · Our scientists · Janelia · Shaping science · Science for everyone
- **Janelia campus bar (Janelia pages only):** About Janelia · Science · People · Resources · Join Janelia
- **Footer:** Find a program · About HHMI · Shaping science · Education & engagement · Prototype guide
- Janelia's 36 open questions each have a question page and a technical statement page (72 pages).

**Ethos in three words:** Questions, People, Openness.

## Issues found in the prototype

- Orphan pages that nothing links to: `#/janelia/join/opportunities`, `#/janelia/prototype-guide`.
- "Explore your path" (careers quiz, 6 pages) and About HHMI have no header menu home.
- Two "Other roles" pages (HHMI and Janelia).
- Five people have both a Leadership profile and a Lab page.
- The fly connectome story is reachable at two URLs (`#/discoveries/…` alias).
- `#/janelia/about` sets the browser tab title to "Prototype guide".

## Regenerating

Requires Python and Playwright (Chromium). Run from `tools/`:

```sh
python3 crawl.py /path/to/slim-prototype.html   # writes crawl.json
python3 gen.py                                   # sitemap
python3 gen2.py                                  # menu
```

The crawl works on a copy of the prototype with embedded images stripped, which makes it much faster.
