# Changelog

## 1.1.0 — 2026-11-25

- New references: data list field definitions and the value each type takes (`field-values.md`), forms and
  workflows with every field type, condition, setting, trigger and action (`forms-and-workflows.md`), and running a
  site: popups, chat, consent, tracking, newsletter, email, domains and analytics (`site-operations.md`).
- Theme skill: rendering data lists, entries, filters, sorting, comments and search (`data-list-templates.md`).
- The example sections were run through the in1s theme validator and give no diagnostics.
- Fixed: a site token has no `list_websites` and no `website` argument; a session with one starts at
  `get_site_overview`.
- Fixed: reference fields are written through `references`, not `data`.
- Theme skill: add new storefront keys to every language the theme ships; reuse snippets and the theme's script setup
  helper; a section that cannot work without a fact renders nothing until it is set.
- `scripts/check-tool-map.mjs` checks the tool map against the live server.

## 1.0.0 — 2026-11-25

- `in1s` skill: connecting the MCP server (sign-in and site tokens, every client), the start of a session, which
  changes go live and which go to the draft, the value shapes that trip agents up, what to confirm before acting,
  visitor-written data, checking work, and errors. References: connect, tool map, recipes.
- `in1s-theme-development` skill: compose before code, the read-write-check-show loop, a section that passes the
  validator, the engine rules that differ from Shopify, languages and right-to-left, assets.
- Claude Code plugin and marketplace that install both skills together with the MCP server.
