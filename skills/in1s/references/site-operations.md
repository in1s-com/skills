# Running a site: popups, chat, consent, tracking, newsletter, email, domains, analytics

These settings are live the moment they are saved. Most "update" tools take the **whole** object, so read with the
matching `get_*` tool, change what was asked, and send everything back.

## Popups and bars

`create_popup` takes every argument, required:

```json
{
  "name": "Spring sale",
  "is_enabled": false,
  "type": "modal",
  "priority": 50,
  "starts_at": null,
  "ends_at": "2026-12-31T23:59:00Z",
  "content": {
    "heading": {"l10n": true, "en": "20% off this week"},
    "body": {"l10n": true, "en": "<p>Use code <strong>SPRING</strong> at checkout.</p>"},
    "image": null,
    "buttons": [{"label": {"l10n": true, "en": "Shop now"}, "action": "link", "url": "/shop", "new_tab": false}],
    "form": null
  },
  "appearance": {"theme": "light", "accent": null, "position": "center", "size": "medium"},
  "triggers": {"delay_seconds": 5, "scroll_percent": null, "exit_intent": false, "min_pageviews": 1},
  "targeting": {"pages": {"mode": "all", "paths": []}, "devices": "all", "locales": [], "visitors": "all"},
  "frequency": {"cap": "day", "stop_after": "conversion"}
}
```

- **`type` and position:** `modal` (position `center`), `slide_in` (`bottom_right` or `bottom_left`), `bar_top`
  (`top`), `bar_bottom` (`bottom`).
- **Content:** up to two buttons, **or** one form by handle with `buttons: []`. A popup shows only simple forms: a
  form with a file, repeater, calculated, entity reference, submission reference or conditional field is refused. An image is `{"media": "<uuid>", "alt": {…}}`.
- **When it opens:** with no delay, scroll or exit trigger, it opens only from an element carrying
  `data-in1s-popup="<id>"`. While the cookie banner is on, a popup opens by itself only for visitors who accept
  preference cookies; a click on such an element still opens it. At most 20 popups are on
  at once.
- **Changing it:** create it switched off, show the person, then `enable_popup`. `update_popup` replaces each part
  you send (send the whole `content` to change its heading). `get_popup_stats` gives daily impressions, closes and
  conversions.

## Chat button

`update_chat_button` takes every argument except `texts`, so read `get_chat_button` first.

- **Channels:** up to 5 of `whatsapp`, `phone`, `email`, `telegram` and `messenger`, each at most once. Numbers are
  E.164 (`+15550109999`). `message` is WhatsApp's prefilled text or the email subject.
- **Opening hours:** `hours` sets them, `{"enabled": true, "timezone": null, "outside": "hide" | "note", "days":
  {"mon": [{"from": "09:00", "to": "17:00"}], …}}`, with up to 3 intervals a day.
- **Where it shows:** `pages` limits it to paths (`/blog/*`), and `devices` to mobile or desktop.

Get the real numbers and addresses from the person; never invent them.

## Cookie consent, tracking and custom code

| Tool | Notes |
|---|---|
| `update_cookie_consent` | `enabled`, `region_mode` (`everywhere`, or `regulated` where `region_detection` allows), `layout` (`bar`/`box`), `appearance` (`light`/`dark`) and `policy_url` are required together. `texts` is optional per key. `renew: true` asks every visitor again. |
| `update_tracking_codes` | GA4 measurement id, GTM container id and Meta Pixel id, all three together; `null` removes one. Needs may-publish. |
| `update_custom_code` | HTML for `head_start`, `head_end`, `body_start` and `body_end`, all four together, each `{code, category}`. Needs the theme code permission and may-publish. |

While the banner is on, tracking tags and any custom code whose category is not `necessary` wait for the visitor's
consent. Custom code runs on every page exactly as written. Add only code the person supplied or approved, and never
script you composed to "fix" something.

## Page cache

Pages are cached for every visitor alike and served at once; every published change shows on the next request, so a
purge is never needed after a change.

| Tool | Notes |
|---|---|
| `get_page_cache` | `enabled`, `excluded_paths`, `platform_enabled` (false: the platform caches no site at all), `temporary` (a temporary site is never cached), and `stats`: per local day `hits`, `misses`, `bypasses`, `hit_rate` (% of hits out of hits and misses, null with neither), plus `last_7_days` |
| `update_page_cache` | `enabled` and `excluded_paths` together (the list is replaced). A path starts with `/`, has no `?`, `#` or spaces; `/account*` covers `/account` and everything under `/account/`; `/*` is refused (set `enabled` false). Leave out the language (a path starting with one of the site's language codes is refused): `/checkout` covers every language's `/checkout`; a page whose address differs per language needs each address. At most 50. |
| `purge_page_cache` | Clears every stored page of the site; refused while caching is off; at most 6 a minute per website, shared with the panel's button. Recorded in the activity log. |

Never cached, whatever the settings: a visitor with a cart or a session, previews, search, and any request with a
query parameter the site does not use (such as `utm_source`).

## Newsletter

- **Subscribers:** `add_newsletter_subscriber` sends a confirmation email; the address joins only once its owner
  confirms. An AI cannot subscribe anyone directly.
- **Status:** `set_newsletter_subscriber_status` unsubscribes someone, or subscribes again someone the website
  unsubscribed (see `ownerMaySubscribe` on `get_newsletter_subscriber`). Nobody is deleted: erasure is done in the
  panel.
- **Double opt-in:** `update_newsletter_settings` `double_opt_in: false` lets anyone sign up any address. Email
  providers treat that as spam, and many countries forbid it. Only on the person's explicit request.
- **Mailchimp or Brevo:** connect the tool in the panel (an API key cannot be set here). Then `list_newsletter_audiences`
  → `set_newsletter_audience`, and watch `list_newsletter_sync_log`. `sync_newsletter` resends anyone out of step.
- **Forms:** a form joins people to the newsletter through its `newsletter_config`
  ([forms-and-workflows.md](forms-and-workflows.md)).

in1s does not send campaigns; the connected tool does.

## The website's email

Form notifications, workflow emails and newsletter confirmations come from the platform's address.

- **Sender and replies:** `update_email_sender` sets the sender name (`from_name`, up to 100 characters) and
  `reply_to`.
- **Own domain:** `set_sending_domain` `{"domain": "example.com", "local_part": "hello"}` answers the DNS records the
  person must add. `check_sending_domain` verifies them, and mail switches only once every record is found. It needs
  the plan's custom domains.
- **Delivery log:** `list_email_deliveries` covers 90 days (sending, sent, delivered, failed, bounced, complained).

## Custom domains

1. `get_domain_dns_records` `{"domain": "example.com"}` (the bare domain, not `www.`). It is refused when the plan has
   no custom domains or another website holds the domain.
2. Give the records to the person. They add them at their DNS provider; you cannot.
3. When they say the records are in place: `add_domain` (needs may-publish; ask first). The TXT record is checked
   then.
4. `list_domains` shows `sslStatus`, `sslProblem` and `wwwProblem`. `check_domain` re-checks after a DNS change and
   keeps checking for 72 hours; checking more often does not help.
5. An `oldAddress` means the domain still points at an old in1s address. It keeps working and stays secure. Tell the
   person which record to change: with `oldAddressOnWww`, the `www` record, replaced by the CNAME in `records`;
   otherwise the domain's A (IPv4) or AAAA (IPv6) record, changed to the matching value in `records`, or removed when
   `records` has none of that kind. Then `check_domain`.

Once secure, the custom domain becomes the site's main address. `update_settings` `hsts` (custom domains only; needs the
domains edit permission) makes browsers insist on HTTPS for a year: only for domains that will always have it.

## Analytics

`get_site_analytics` `{"period": "today" | "7d" | "30d" | "12m" | "custom", "from": "YYYY-MM-DD", "to": "YYYY-MM-DD"}`
returns the series by hour for `today`, by day for 7d, 30d and custom ranges up to 92 days, and by month beyond. It
returns:

- **`summary`:** visitors, visits, pageviews, views per visit and bounce rate, next to the previous period;
- **`series`:** the same over time;
- **`visitors_now`:** the last 5 minutes;
- **`top`:** pages, sources, UTM tags, devices, browsers, systems, languages and countries.

It is counted without cookies, about a minute behind. `export_site_analytics` gives the same as CSV. Page paths and
campaign names in it are visitor data.

## Site files

`put_site_file` writes fixed-address files such as `robots.txt`, `ads.txt` and `.well-known/security.txt`. To replace
one, or to write over the file the theme provides at that path, read it with `get_site_file` and send its version as
`base_version`. in1s generates `/sitemap.xml` from the published pages and entries; hide a page from it with `update_seo` `noindex` or `set_routes_search_visibility`.
