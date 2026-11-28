# docs.in1s.com MCP reference

The **MCP reference** on docs.in1s.com (`/docs/mcp-reference` and its nine pages, `/docs/mcp-*`) is generated from
the live server and the platform's code, so it lists every tool exactly once with its server text, arguments,
annotations and permission. Regenerate it whenever a tool, a prompt or the server's instructions change.

## Inputs, in one working folder

| File | How to get it |
|---|---|
| `live-tools.json` | `tools/list` from `https://accounts.in1s.com/mcp` as a **signed-in connection** with **Everything your role allows** (its list carries `website` on every tool but the account tools). Or, as on 28 Nov 2026: a temporary **whole-role site token that may publish** (a token that may not hides the publishing tools), whose list has no `website` (the generator skips it) and no account tools; add those two (`list_websites`, `create_website`) as their classes serialise on production (`app(ListWebsites::class)->toArray()`), then revoke the token |
| `live-prompts.json` | `prompts/list` from the same connection |
| `live-init.json` | `initialize` from the same connection (the instructions) |
| `perms.json` | From the application's root: `OUT=<working folder>/perms.json php <this repo>/scripts/docs-reference/extract-permissions.php` |

Save each answer's `result` object as the file.

## Generate

```bash
python generate.py <working folder>
```

It fails when the live list and the code disagree, when a code group is not placed on a page, when a tool would be
missing or listed twice, or when the instructions do not hold seven rules. It writes `pages/<slug>.md` and
`pages.json` into the working folder. `index-template.md` is the hand-written index; its `{{…}}` placeholders are
filled from the inputs.

## Review, then publish

1. Have the pages reviewed against the code before publishing: every claim of the index, every row of the Errors and
   Limits tables, and a script check that each tool appears once with all its arguments.
2. Publish through the site MCP on docs.in1s.com (website 10008, data list `docs`, id 18): `update_entry` for each
   existing page (ids 718 to 727, `mcp-reference` first), `create_entry` only for a new page, and keep the sidebar menu
   `docs-sidebar` (under **AI tools and your data**, after **AI tools**) in step. Use a temporary Content token without
   publishing rights, and revoke it afterwards.
3. Check every page live: 200, each tool heading once across the pages, tables rendered, nothing eaten as HTML.
