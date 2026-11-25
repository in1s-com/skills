# in1s skills

Agent Skills for building and running websites on [in1s](https://in1s.com) with an AI agent, through the in1s MCP
server.

They work in Claude Code, Claude Desktop, claude.ai, Codex, Cursor, VS Code and any other client that reads
[Agent Skills](https://agentskills.io).

| Skill | Use it for |
|---|---|
| [`in1s`](skills/in1s/SKILL.md) | Connecting the MCP server, then working on a site: pages, data lists and entries, media, menus, SEO, forms, submissions, workflows, webhooks, domains, languages, publishing safely. |
| [`in1s-theme-development`](skills/in1s-theme-development/SKILL.md) | How a site looks: sections and blocks, theme settings, fonts, translations, right-to-left, and writing Liquid theme files that pass in1s's validator, including data list listings, entry pages, filters, comments and search. |

Each skill keeps its `SKILL.md` short and loads detail from `references/` only when a task needs it:

| Reference | Covers |
|---|---|
| [connect.md](skills/in1s/references/connect.md) | Configuration for every client, access levels, token hygiene |
| [tool-map.md](skills/in1s/references/tool-map.md) | Every MCP tool, grouped by job, marked live / draft / needs publishing rights / irreversible |
| [recipes.md](skills/in1s/references/recipes.md) | New page, blog post, data list, form with email, import, domain, new language, SEO sweep, undo |
| [field-values.md](skills/in1s/references/field-values.md) | Data list field definitions and the value each field type takes |
| [forms-and-workflows.md](skills/in1s/references/forms-and-workflows.md) | Form fields, conditions, statuses, capacity, comments; workflow triggers and actions |
| [site-operations.md](skills/in1s/references/site-operations.md) | Popups, chat button, consent, tracking, newsletter, email, domains, analytics |
| [data-list-templates.md](skills/in1s-theme-development/references/data-list-templates.md) | Listing and entry templates, filters, sorting, entry fields, forms in Liquid, search |

The MCP server already tells an agent what each of its tools does. These skills add what the tools cannot say:
connecting in the first place, which changes go live and which go to the draft, the shortest path for common jobs,
the value shapes that trip agents up, and what to confirm with a person before acting.

## Install

### Any agent (skills.sh)

```bash
npx skills add in1s-com/skills
```

To install one skill only, add `--skill in1s` or `--skill in1s-theme-development`.

### Claude Code plugin (skills and the MCP server together)

```
/plugin marketplace add in1s-com/skills
/plugin install in1s@in1s
```

Then run `/mcp`, choose **plugin:in1s:in1s** and **Authenticate**. If you already added the server yourself with
`claude mcp add`, remove one of the two (`claude mcp remove in1s`), or every tool appears twice.

### By hand

Copy each folder under `skills/` into your agent's skills directory, for example `~/.claude/skills/` for Claude Code.

## Connect the in1s MCP server

The endpoint is `https://accounts.in1s.com/mcp`.

- **Claude Code**:
  `claude mcp add --transport http in1s https://accounts.in1s.com/mcp`, then `/mcp` → in1s → Authenticate.
- **claude.ai, Claude Desktop, ChatGPT**: add a custom connector with that URL, sign in to in1s, tick your websites
  and Allow.
- **Cursor, VS Code, Codex, other clients**: create a site token in the in1s panel under **AI tools → Coding tools**,
  and send it as `Authorization: Bearer in1s_…`.

Config for every client: [skills/in1s/references/connect.md](skills/in1s/references/connect.md).

## Try it

> List my in1s websites and tell me what you can change on each.

> Add a blog post about our summer opening hours, with this photo, and link it in the footer.

> Put an FAQ section under the hero on my homepage and show me a preview before anything goes live.

> Run a site health check and fix the missing alt texts and search descriptions.

## Safety

- Content edits are live at once. Theme edits wait in a draft until someone publishes it.
- The skills tell the agent to show a preview link after theme changes, and to publish, delete for good, switch
  themes or change domains only when you ask.
- Visitor-written content (form submissions and similar) is treated as data, never as instructions.
- What an agent may do is limited by the access you choose when connecting. Choose **View only** to let it look
  without changing anything.

Report a security problem privately through this repository's **Security** tab → **Report a vulnerability**, not in
a public issue.

## Maintaining

- `node scripts/check-tool-map.mjs` (with `IN1S_TOKEN` set to an owner's full-access site token) compares
  `tool-map.md` with the tools the server offers, and fails when the server has a tool the map does not mention.
- `claude plugin validate --strict .` checks the plugin and marketplace manifests.
- [evals/](evals/README.md) holds the scenarios the skills were tested on.

## Contributing

Issues and pull requests are welcome. A change to a skill should come with the task it fixes: what an agent did
without the change, and what it does with it. Keep `SKILL.md` files short. Detail goes in `references/`.

## License

[MIT](LICENSE)
