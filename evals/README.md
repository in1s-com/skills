# Skill evaluations

The scenarios these skills were written and tested against. Run each one as a fresh agent session twice: once without
the skills and once with them. Keep a change to a skill only when it moves a run from failing to passing, or closes a
gap a run exposed.

**Run them read-only.** Tell the agent it may call only tools whose names start with `get_`, `list_`, `search_`,
`check_` or `suggest_`, plus `read_theme_file`, `render_page` and `validate_theme`. Every write must be written out as
the call it would make, with full arguments. Use a test website you own.

## 1. Not connected yet

> I have a website on in1s. Connect it to you here in Claude Code so you can edit it, then tell me what you can and
> can't do on it.

No in1s tools are available in this session.

Pass when the agent:

- gives `https://accounts.in1s.com/mcp` and the `claude mcp add --transport http …` command;
- uses the sign-in flow (`/mcp` → Authenticate) rather than asking for a token;
- names the access levels and the separate "may publish" choice;
- never asks for a token to be pasted into the chat.

## 2. Change one text and make it live

> Change the main heading of my homepage hero to "…" and make it live right away, I'm in a hurry.

Pass when the agent:

- reads the template and sends the whole section back with one setting changed;
- passes `base_version`;
- checks `get_draft_status` and names anyone else's unpublished changes before publishing;
- publishes only because the person asked.

## 3. A blog post with a photo and a menu link

> Publish a new blog post titled "…" (about three short paragraphs), use this cover photo <url>, and add a link to it
> in the footer menu.

Pass when the agent:

- uploads the photo to the media library and puts the **uuid** in the image field and the **url** in `ogImage`;
- uses `l10n` maps for translatable values;
- sends every existing menu link back with the new one;
- works out which menu the footer actually shows before choosing one.

## 4. A section the theme may already have

> Build me a new pricing table section (three plans with name, price, features and a button to the download page)
> and put it on the homepage just before the footer.

Pass when the agent:

- finds an existing pricing section, if the theme has one, and uses it rather than writing a duplicate;
- links with `in1s://routes/handle:…`;
- never writes invented prices into the section, and asks for the real ones;
- ends with a preview link, not a publish.

## 5. A new section the theme does not have

> Add a launch countdown section to the homepage under the hero: a big countdown to our release, a heading, the
> release perks and a notify-me button. Arabic is coming soon, so make it ready.

Pass when the agent:

- reuses the theme's snippets and its script setup helper;
- has `in1s_attributes` on the root and setting markers on printed text;
- uses `t:` schema labels and `| t` storefront words, with keys added to both locale files;
- uses logical CSS and checks the theme's fonts for Arabic;
- leaves the date and perks for the person to supply;
- runs `validate_theme` and `render_page`, then gives a preview link.

## What the baselines showed

With the MCP server connected, agents without the skills already handled scenarios 2 to 4 well: the server's tool
descriptions carry most of the operational rules. Scenario 1 failed without the skills, because the agent could not
know the endpoint or the sign-in flow. Scenario 4 put invented prices into the section. The skills target those gaps,
and the edge cases scenario 5 exposed.
