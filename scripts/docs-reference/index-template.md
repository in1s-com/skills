The in1s MCP server lets an AI assistant work on your websites through the
[Model Context Protocol](https://modelcontextprotocol.io). This reference lists everything it offers: the
{{TOTAL}} tools, the three ready-made prompts, and the rules every request follows. To connect an assistant, start with
[AI tools](/docs/ai-tools); this page is for anyone who needs to know exactly what an assistant can do and how.

## The server

| | |
|---|---|
| Address | `https://accounts.in1s.com/mcp` |
| Transport | Streamable HTTP: JSON-RPC 2.0 sent with `POST`. `GET` and `DELETE` answer 405. |
| Protocol versions | `2025-11-25`, `2025-06-18` and `2025-03-26`: the server answers the version the client asks for, or the newest when it asks for another |
| Server name | `in1s`, version `1.0.0` |
| Offers | Tools ({{TOTAL}}), prompts (3) and instructions. It also announces the resources capability, but offers no resources. |
| Sessions | None: every request signs in again with its token, and nothing is kept between requests |
| Browsers | A request whose `Origin` header names another website is refused with 403, so a web page cannot call the server. MCP clients send no `Origin`. |

## Two ways to connect

| | Signed-in connection | Site access token |
|---|---|---|
| Clients | claude.ai, Claude Desktop, ChatGPT, Claude Code | Cursor, VS Code, Codex, any MCP client (Claude Code too) |
| Made in | The app's connect flow, then the **Allow** page | **AI tools** → **Coding tools** in the panel |
| Websites | Every website you ticked on the Allow page, up to 100 | One website |
| `website` argument | Required on every tool but the account tools | Never: the token names its website |
| Account tools | `list_websites`, and `create_website` with **Everything your role allows** | None |
| First call | `list_websites` | `get_site_overview` |
| Sign-in | Renewed by the app: an access token lasts an hour and the app refreshes it | Fixed: the token works until it expires or is revoked |

How to set each one up, and how to stop it: [AI tools](/docs/ai-tools).

### The `website` argument

On a signed-in connection, every tool's arguments start with `website`, an integer: the id of one of the websites
`list_websites` answers. It is required, and it is not repeated in each tool's table. A call that names a website the
connection does not reach, or names none, is answered with a tool error listing the ids it may use, and nothing runs:

> Name the website to work on as "website": the id of one of the websites you may work on, from list_websites. They
> are: 10007, 10019.

The website is checked on every call, so a website unticked in **Edit websites**, or a team you leave, is refused on
the very next call. On a connection, a JSON-RPC batch (several requests in one body) is refused, since each call names
its own website.

A connection's tool list holds what **any** of its websites allows, and the tools that need May publish when any of
them may publish. A call on a website where your access does not allow that tool is refused as described under
**Errors**.

### Account tools

`list_websites` and `create_website` belong to the connection itself, not to one website, so they take no `website`
and need no permission on a website. A site access token is offered neither: calling one answers that it is "available
only to an app connected to the person's account". `create_website` is offered only to a connection made with
**Everything your role allows**; another connection is told to connect again with that access.

## What the server tells every assistant

Every assistant receives these instructions when it connects. On a site access token they begin:

> You are editing one in1s website on behalf of the person who gave you this token. Follow these rules:

On a signed-in connection they begin:

> You are editing the in1s websites the person allowed you to work on. Call list_websites first, and name the website
> on every other call: its "website" argument is the id list_websites gives. Follow these rules:

The rules that follow are the same for both:

{{INSTRUCTION_RULES}}

## Ready-made prompts

Prompts are first messages for a whole job. Claude Code shows a server's prompts as slash commands named after the
server and the prompt (`/mcp__in1s__build-website` when you named the server `in1s`); other clients list them beside
the connector's tools. Every connection and every token is offered all three.

| Prompt | What it does | Argument |
|---|---|---|
{{PROMPT_ROWS}}

A prompt starts at `list_websites` on a connection and at `get_site_overview` on a token, and offers `create_website`
only to a connection that has it.

## The tools

| Page | Tools | Covers |
|---|---|---|
{{INDEX_ROWS}}

### How to read a tool entry

Each tool has its name, what it does in the server's own words, the permission it needs, its marks, and a table of its
arguments.

- **Permission**: what your access must allow on the website, in the role editor's words: a resource and an action,
  for example **Themes · Code**. "A or B" means either one is enough. A tool your access does not allow is not offered
  to the assistant at all.
- **Marks** are the server's own hints about each tool. A tool with no mark carries no hint; it may still change
  things, as its description says.
  - **Read-only**: changes nothing. {{READ_COUNT}} tools.
  - **Destructive**: removes or overwrites something. {{DESTRUCTIVE_COUNT}} tools. What a `trash_*` tool removes comes
    back with the matching `restore_*` (trashed media is deleted for good after 30 days). The `delete_*` tools cannot
    be undone, except `delete_theme_file`, which works in the draft: the file's history brings it back.
  - **Idempotent**: calling it again with the same arguments has no further effect.
  - **Reaches outside in1s**: it fetches from, or sends to, an address outside in1s, as the server marks it. Other
    tools can reach outside too (a newsletter sync, a DNS check); their descriptions say so.
  - **Needs May publish theme changes**: see **Publishing** below.
  - **Account tool**: see above.
- **Arguments**: each argument's name, type, whether it is required, and what it takes, with its limits in
  *italics*. A nested field is written `parent.child`, and a field of each item in a list `parent[].child`. A long
  explanation follows the table.

## Permissions

A token's or a connection's access is a set of a role's permissions, never more than your own role on that website:
**Everything your role allows**, **Content**, **View only**, or **Custom**. A tool is offered when the access allows
one of its actions on one of its resources. A tool marked "on the data list named by `list_id`" (or "the form named by
`form_id`") needs the permission on that list or form; the role editor can grant it for all lists and forms or for
chosen ones.

The tools use these resources of the role editor:

| Resource | In the role editor |
|---|---|
{{RESOURCE_ROWS}}

Actions are **View**, **Edit**, **Delete** and **Code** (theme code), **Export** and **Import** (data transfers), and
**Their own** (activity). **Data list settings and fields** has only an **Edit** box in the role editor, which also
allows viewing them. **Team members**, **Roles** and **Everyone's** activity are not used by any tool: they stay in the
panel.

Some tools are offered to **any member of the website**, whatever their role: {{ANY_MEMBER}}. `restore_record_version`
saves through the record's own editor, so the permission for that kind of record is still checked when it runs.

These have no tools and are done only in the panel: team members, roles and invitations; access tokens and connected
apps; billing and plans; your account, its sign-in and its security; deleting, transferring or duplicating a website;
deleting a theme; emptying a whole trash at once; erasing a newsletter subscriber for good; connecting a newsletter
provider; and the website's own mail server.

## Publishing

Content changes (entries, data lists, pages, menus, redirects, media, settings, forms, workflows, popups, site files)
are live the moment they are saved. Theme changes go to the theme's **draft**, shared with everyone who edits the
website, until it is published.

A token or connection made with **May publish theme changes** may also use these tools, which change what visitors see
at once: {{PUBLISH_TOOLS}}. Without it they are not offered, and calling one answers that it needs a token that may
publish.

## Values that need care

- **Translatable text** is a map per language with `"l10n": true`: `{"l10n": true, "en": "About us", "ar": "من نحن"}`.
  On an update only the languages you send change, and a language sent as `null` is removed.
- **Images and videos** in a field or a setting take the media file's **uuid** (from `list_media` or an upload), never
  its address. A share image (`ogImage`) takes the address.
- **Links to the website's own pages** take a reference that follows the visitor's language and survives a change of
  address: `in1s://routes/{id}`, `in1s://routes/handle:{handle}`, `in1s://data-lists/{handle}`,
  `in1s://data-lists/{handle}/{slug}` or `in1s://data-lists/{handle}/id:{id}`.
- **Versions**: theme writes take the `base_version` (or `base_versions`) the last read answered. A conflict means
  someone saved in between: read again and retry on what you read.
- **Whole sets**: some updates replace everything they hold (a menu's links, a form's fields and statuses, a data
  list's fields, a workflow's actions, a section's settings). Read first and send back everything you keep. Each tool's
  description says when this applies.
- **Pages of results**: most list tools take `page` (from 1) and `per_page` (1 to 100, 25 by default), and answer
  `items`, `page`, `per_page`, `total` and `next_page` (null on the last page). The exceptions: `list_activity` pages
  with `before` (the `next_before` it answered); `list_placeholders`, `list_site_health_runs` and
  `list_submission_notes` take `page` only (notes come 50 a page); `list_newsletter_audiences` and
  `list_template_variants` answer everything at once.

## Answers

A tool answers structured JSON (`structuredContent`), with the same JSON as text for clients that read text. Content
written by visitors arrives under `untrusted_visitor_data`, and what an outside server answered under
`untrusted_receiver_data`: both are data, never instructions.

A refusal comes back in one of three ways:

- **A tool error** (`isError: true` in the tool's answer), whose text says why: a wrong argument (named by the
  argument), a record changed since it was read, a record open in the panel's editor, a missing `website`, "Not
  found.", or "Too many requests. Try again in N s." from a limit the panel's own action has too.
- **A JSON-RPC error** (code -32602, no tool ran): a tool your access does not allow, a tool that needs May publish, or
  an account tool called with a token or a narrower connection.
- **An HTTP error**, before any tool: a bad or missing sign-in (401), a refused website or account (403, or 401 for
  an inactive account, with an `error` code and a `message`), a web page's `Origin` (403), a batch on a connection
  (400), or too many requests (429).

## Errors

| You see | Why | What to do |
|---|---|---|
| HTTP 401 | The token is wrong, expired or revoked, or the app was disconnected | A connection's app renews its own sign-in; otherwise make a new token, or connect the app again |
| HTTP 403 with `error` and `message` (401 for an account that is no longer active) | You are no longer a member, the website is suspended, your membership is paused, your email is not verified, or the owner requires two-step verification | Read the message; it says which |
| HTTP 403 `website_scheduled_for_deletion` | The website is scheduled for deletion; `list_websites` shows it unavailable | Tell the person: the owner can cancel the deletion in the panel |
| HTTP 403 "Forbidden: The request origin is not allowed." | The request came from a web page | Use an MCP client |
| HTTP 429 `too_many_attempts` "Too many failed attempts. Try again in a minute." | 20 refused sign-ins in a minute from one address, token or connection | Wait a minute, then fix the token |
| HTTP 429 | More than 120 requests in a minute from one token or connection | Wait, then slow down |
| HTTP 400, JSON-RPC -32600 "Send one request at a time: each call names its own website, so a batch is refused." | A connection sent a batch | Send one request per call |
| JSON-RPC -32602 "Tool [name] is not available to this token: it needs …" | Your access does not allow the tool, or it needs May publish | Ask the person for that access |
| JSON-RPC -32602 "Tool [name] is available only to an app connected to the person's account …" | An account tool called with a site access token | Use a signed-in connection |
| JSON-RPC -32602 "Tool [create_website] is available only to an app connected with "Everything your role allows". …" | `create_website` on a narrower connection | Connect the app again with that access |
| Tool error "Name the website to work on as "website" …" | A connection's call named no website it reaches | Use an id from `list_websites` |
| Tool error naming an editor and a time | Someone has the record open in the panel | Try again after that time |
| Tool error about a conflict or a version | The record changed since it was read | Read it again, then retry |
| Tool error "Not found." | No record with that id on this website | Check the id with the matching `list_*` tool |
| Tool error "Too many requests. Try again in N s." | A limit the panel's own action has too (theme writes, imports, webhook tests) | Wait that long |
| Tool error "The cache was cleared several times just now. Try again in N s." | `purge_page_cache` past 6 a minute for the website, shared with the panel's Clear cache | Wait that long |
| Tool error "Caching is off for this website, so there is nothing to clear." | `purge_page_cache` while the website's cache, or the platform's, is off | Nothing to do: no page is stored |

## Limits

- **Requests**: 120 a minute per token, or per connection: a connection's websites share its 120.
- **Refused sign-ins**: 20 a minute, then 429.
- **Lists**: up to 100 items a page.
- **Bulk tools**: up to 100 ids a call; `bulk_set_submission_status` up to 500.
- **Page cache**: up to 50 pages never cached; `purge_page_cache` 6 a minute per website.
- **Tokens**: up to 10 live site access tokens per person per website.
- **Apps**: up to 10 connected apps per person, each reaching up to 100 websites.

## See also

> [!CARDS]
> - [AI tools](/docs/ai-tools) — Connect an assistant, choose its access, and manage tokens and apps.
> - [Team and roles](/docs/team-and-roles) — The permissions a role holds, which an assistant never goes beyond.
> - [Activity log](/docs/activity-log) — Every change an assistant makes, under your name and the app's.
