# Connecting the in1s MCP server

Endpoint: `https://accounts.in1s.com/mcp`. It is streamable HTTP, takes `POST` only, and keeps no session. A browser
page cannot call it: requests carrying an `Origin` header are refused.

There are two ways to authorise it.

| | Sign in (OAuth) | Site token |
|---|---|---|
| Clients | Claude Code, claude.ai, Claude Desktop, ChatGPT | Cursor, VS Code, Codex, any other MCP client |
| Websites | Every website the person ticks on the Allow page | One website per token |
| Made in | The client's connect flow | in1s panel → **AI tools** → **Coding tools** |
| Removed in | in1s panel → **AI tools** → **Apps** → Disconnect | Same page → **Your tokens** → Revoke |
| Expiry | Renewed by the client | 30 days, 90 days, 1 year or never |

Both carry an **access level** chosen when they are made:

- **Everything your role allows**: follows the person's role as it changes.
- **Content**: data lists, entries, media, navigation, pages and redirects; the theme is view-only.
- **View only**: reads only.
- **Custom**: tick each permission; only what the person holds can be given.

**May publish theme changes** is a separate tick. Without it the agent cannot publish, discard or restore the draft,
drop a draft file's change, apply a theme update, switch the theme, write tracking codes or custom code, or add or
remove a custom domain.

## Claude Code

```bash
claude mcp add --transport http in1s https://accounts.in1s.com/mcp
```

Run it in a terminal, not inside a Claude Code session. Then start Claude Code, run `/mcp`, choose **in1s**, choose
**Authenticate**, and complete the in1s Allow page in the browser. Add `--scope user` to make it available in every
project; the sign-in is kept by Claude Code, so it is asked once.

With a site token instead:

```bash
claude mcp add --transport http in1s-mysite "https://accounts.in1s.com/mcp" \
  --header "Authorization: Bearer in1s_…"
```

## claude.ai and Claude Desktop

Settings → Connectors → **Add custom connector** → URL `https://accounts.in1s.com/mcp` → Connect, sign in to in1s,
tick the websites and choose the access, then Allow.

## ChatGPT

Add a custom connector (MCP app) with the URL `https://accounts.in1s.com/mcp`, then sign in and Allow as above. The
exact menu names in ChatGPT depend on its plan and current interface.

## Cursor (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "in1s-mysite": {
      "url": "https://accounts.in1s.com/mcp",
      "headers": { "Authorization": "Bearer in1s_…" }
    }
  }
}
```

## VS Code (`.vscode/mcp.json`)

VS Code prompts for the token, so it never sits in the file:

```json
{
  "inputs": [
    { "type": "promptString", "id": "in1s-token", "description": "in1s token", "password": true }
  ],
  "servers": {
    "in1s-mysite": {
      "type": "http",
      "url": "https://accounts.in1s.com/mcp",
      "headers": { "Authorization": "Bearer ${input:in1s-token}" }
    }
  }
}
```

## Codex (`~/.codex/config.toml`)

```toml
[mcp_servers.in1s-mysite]
url = "https://accounts.in1s.com/mcp"
bearer_token_env_var = "IN1S_TOKEN"
```

Then, in the shell that starts Codex: `export IN1S_TOKEN=in1s_…`

## Any other client

```
URL:    https://accounts.in1s.com/mcp
Header: Authorization: Bearer in1s_…
```

## Check it works

Call `list_websites`. One entry per website the access covers means it is connected. Common failures:

- **401**: the token is wrong, revoked or expired, or the sign-in was disconnected. Make a new one.
- **403** naming the request origin: the client is a browser page. Use an MCP client instead.
- **A website listed with `unavailable`**: the owner's plan is paused, the site is suspended, or the person's access
  ended. The reason is given.
- **Fewer tools than expected**: the access level leaves them out. Make the token or connection again with more access.

## Token hygiene

- A site token is shown **once**, when it is made. It starts with `in1s_`.
- Keep it in the client's config or an environment variable. Never commit it, and never paste it into a chat.
- A person may hold up to 10 live tokens per website. Revoke the ones no longer used.
- Changing or resetting a password, signing out other devices, or "this wasn't me" revokes every token the person holds
  and disconnects every connected app. Reconnect afterwards.
