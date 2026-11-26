# Changelog

## 1.5.1 — 2026-11-26

- Preview links (draft and page): anyone who has one can see what it opens until it expires, so the agent gives it to the person
  in its reply only, never writes it anywhere else, and revokes it once they have looked (both skills; Snyk W007).

## 1.5.0 — 2026-11-26

- `list_domains` / `check_domain` / `add_domain`: a domain's `oldAddress` (it still points at an old in1s address,
  keeps working, and the person should change its address record to the value in `records`), in site-operations.md
  (liquid-things 4cabf2619).

## 1.4.1 — 2026-11-26

- A website scheduled for deletion: `list_websites` shows it unavailable and every call on it answers 403
  `website_scheduled_for_deletion` (SKILL.md errors, connect.md, the docs reference's errors table).

## 1.4.0 — 2026-11-25

- The server's three MCP prompts, `build-website`, `redesign` and `seo-sweep` (liquid-things d2e4428d1, live since
  25 Nov 2026): what they are and that their steps agree with this skill.

## 1.3.0 — 2026-11-25

- `create_website`: a signed-in connection with "Everything your role allows" can make a new website on the person's
  account, which joins the connection. In the session start, "Ask first", the tool map, connect.md, and as step 2 of
  the "whole website" recipe.

## 1.2.1 — 2026-11-25

- design-and-motion.md: how each modern pattern works (reveal on view, word-by-word headings, highlighted words, the
  header that becomes a pill, rolling button labels, rolling numbers, scrolling bands, statements that fill in on
  scroll, sticky stacking cards, framed image cards, the footer wordmark, smooth scrolling), the small finishing
  details, the mistakes a real build made that only a browser shows, and how to study reference sites.

## 1.2.0 — 2026-11-25

From an agent's full build of a bilingual (English and Arabic) site through the MCP, and a re-test of each point
against the live server.

- Theme skill: a design, motion and accessibility reference (`design-and-motion.md`): choosing a direction for any
  kind of site, what modern sites share, motion levels, motion that never hides content (no JavaScript, editor,
  reduced motion, print; checked with the theme validator), WCAG 2.2 AA.
- Theme skill: "Look at the page": `render_page` is text only, so check the preview in a browser at desktop and phone
  width and in right-to-left, or say it was not checked.
- Theme skill: change files with `edit_theme_file` and one section with `upsert_section`; small `get_template`
  answers; a section without `presets` cannot be placed; `in1s://` links work inside richtext settings; the whole
  font library is listed only without `search`; self-host fonts with `upload_font_from_url`; Arabic typography.
- in1s skill: don't create throwaway records to learn how a tool behaves (a page's template stays in the published
  theme after the page is trashed); a stale tool description means reconnecting; menu links to pages rather than
  typed paths; a "whole website" recipe.
- connect.md: tools listed twice, stale descriptions, and a new server missing from `/mcp` until restart.
- Two new eval scenarios: bilingual links, and "make it modern".

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
