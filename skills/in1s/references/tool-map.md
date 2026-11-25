# in1s MCP tool map

Every tool the in1s MCP server can offer, grouped by job. A connection only lists the tools its access allows, so some
of these may be missing for a given website. Calling one that is missing returns an error that names the permission
it needs. With a signed-in connection, every tool except `list_websites` takes `website`, the id `list_websites`
returns. A site token is bound to one website: it has no `list_websites` and no `website` argument.

Legend: **live** = visitors see it at once · **draft** = goes to the theme draft · **gated** = also needs a token that
may publish · **irreversible** = cannot be undone from in1s.

## Start

| Tool | What it does |
|---|---|
| `list_websites` | Signed-in connections only. The websites you may work on: id, url, role, `permissions`, `may_publish`, `unavailable`. Call first. |
| `create_website` | Signed-in connections with "Everything your role allows" only. A new website on the person's own account (name, first language, contact email; optional subdomain, theme from `list_theme_gallery`, timezone), added to the connection with the same access. Counts toward the plan's websites; the subdomain is permanent. Ask first. **live** |
| `get_site_overview` | One website at a glance: languages, active theme, template names, data lists, forms, your permissions. |
| `get_settings` / `update_settings` | Store details, languages, site SEO, maintenance mode, profile, CAPTCHA, embedding, HSTS. One section per call. **live** |
| `list_activity` | Who changed what, newest first. |

## Content: data lists and entries

| Tool | What it does |
|---|---|
| `list_data_lists` / `get_data_list` | Collections (posts, products, team…) with their fields, URL settings, SEO, `canTrash`. |
| `create_data_list` / `update_data_list` | Make or change a collection. `fields` replaces the whole set. **live** |
| `check_data_list_handle` / `suggest_data_list_handle` | Is a handle free / which one would it get. |
| `trash_data_list` / `restore_data_list` | Trash (pages go offline) and bring back with its entries. |
| `list_entries` / `get_entry` | Entries of one list; `data` is keyed by the list's field ids. |
| `create_entry` / `update_entry` | Create (published unless `isPublished: false`) / change only what you send. **live** |
| `duplicate_entry` | Copy as an unpublished draft. |
| `set_entries_published` / `trash_entries` | Bulk, up to 100 ids. **live** |
| `trash_entry` / `restore_entry` / `reorder_entries` | Single-entry trash, restore, manual order. |
| `list_entry_versions` / `get_entry_version` / `restore_entry_version` | An entry's history and undo. |

## Pages, URLs and navigation

| Tool | What it does |
|---|---|
| `list_routes` / `get_route` | The site's own pages (about, pricing…), with `editingBy` lock. |
| `create_route` / `update_route` | Create/change a page. Its template `templates/route.{path}.json` is written to the **published** theme. **live** |
| `duplicate_route` | Copy a page as an unpublished draft. |
| `set_routes_published` / `set_routes_search_visibility` / `trash_routes` | Bulk, up to 100 ids. |
| `trash_route` / `restore_route` | Single page trash and restore. The page's template file stays in the theme. |
| `create_page_preview_link` | Time-limited link to a page as saved, published or draft. |
| `suggest_slug` / `check_slug` | Free URL slugs in every language / is this slug free. |
| `update_seo` | Search title, description, share image, noindex of an entry, list or page. **live** |
| `list_menus` / `create_menu` / `update_menu` | Menus; `update_menu` with `links` replaces every link. **live** |
| `delete_menu` | No trash. **irreversible** |
| `list_redirects` / `create_redirect` / `update_redirect` | Manual redirects. **live** |
| `delete_redirect` | No trash. **irreversible** |
| `list_site_files` / `get_site_file` / `put_site_file` | Fixed-address files: robots.txt, ads.txt, .well-known/*. Needs `base_version` to replace. **live** |
| `trash_site_file` / `restore_site_file` | Trash and restore one of your site files. |

## Media and fonts

| Tool | What it does |
|---|---|
| `list_media` / `get_media` | The library. Fields and theme settings take a file's **uuid**, not its url. |
| `upload_media_from_url` / `upload_media` | Add an image or video (≤ 10 MB; URL preferred over base64). **live** |
| `update_media` | Alt text per language (≤ 125 chars), name, focal point. |
| `replace_media` | New bytes, same uuid: changes it everywhere at once. |
| `duplicate_media` | Copy before changing a file used elsewhere. |
| `get_media_usages` | Where a file is used. Read before trashing. |
| `trash_media` / `restore_media` | Trash empties every place that uses the uuid. |
| `list_media_folders` / `create_media_folder` / `rename_media_folder` / `move_media_folder` / `delete_media_folder` / `move_media` | Organise the library; folders never change URLs. |
| `list_fonts` | Fonts allowed for `font_picker` settings (`<family>_n4` = regular, `_n7` bold, `i` italic). Call it without `search`, `per_page: 100`, to see the whole library. |
| `upload_font_from_url` / `upload_font` | Add a licensed web font. |
| `delete_font` | No trash. **irreversible** |

## Theme: visual changes (all **draft**)

| Tool | What it does |
|---|---|
| `get_theme_catalog` | Section and block types the theme offers, their settings, presets, limits, where they may go. |
| `get_template` | A template's sections, layout and groups, plus `versions` to pass back as `base_versions`. `include_groups`, `include_layout`, `include_schemas` false for a small answer. |
| `upsert_section` | Change, add, move or remove ONE section. Its `settings` are replaced whole. A type without `presets` cannot be added. |
| `update_sections` | Save whole containers; a section left out is removed. |
| `get_theme_settings` / `update_theme_settings` | Colors, fonts, layout options, style presets. |
| `get_translations` / `update_translations` | Storefront texts per language; `allow_new_keys` to add one. |
| `add_theme_language` | Add a site language to the theme (add it to the site first with `update_settings`). |
| `list_placeholders` | What is still stand-in text, sample content or an empty picture. |
| `list_template_variants` / `create_template` | Alternate layouts for an entry or page. |

## Theme: code (all **draft**)

| Tool | What it does |
|---|---|
| `get_liquid_reference` | The Liquid this engine supports and the authoring rules. Read before writing code. |
| `list_theme_files` / `read_theme_file` | Files with `versionId`; `view: "published"` reads the live file. |
| `search_theme_code` / `get_file_references` | Find text across files / what a Liquid file renders. |
| `write_theme_file` / `edit_theme_file` | Whole file / exact-match edits. Refused if it would not render. |
| `rename_theme_file` / `delete_theme_file` | Protected files cannot be moved or deleted. |
| `upload_theme_asset_from_url` / `upload_theme_asset` | Images, fonts, SVG into `assets/`. |
| `validate_theme` | Problems list for the whole draft; only errors block publishing. |
| `list_file_versions` / `get_file_version` / `compare_file_versions` / `restore_theme_file` | A file's history; restore puts a version back into the draft. |
| `discard_draft_file` | Drop the draft's change of one file, whoever made it. **gated** |

## Draft, preview and publishing

| Tool | What it does |
|---|---|
| `get_draft_status` | What the shared draft holds, who wrote each file, `changedUnderneath`, `may_publish`. |
| `render_page` | A published page as the DRAFT theme renders it: sections, text, images, links, errors. 404 for an unpublished page. Text only: no layout, CSS or motion. Needs theme edit or code. |
| `create_preview_link` | 24-hour read-only link to the draft. Show it to the person. |
| `list_preview_links` / `revoke_preview_link` | Open preview links, including ones shared with clients. |
| `publish_draft` | Make the whole shared draft live. **live, gated** |
| `discard_draft` | Drop every unpublished change, collaborators' too. **gated** |
| `create_snapshot` / `list_snapshots` / `compare_snapshots` / `rename_snapshot` | Restore points of the live theme. |
| `restore_snapshot` | Make a snapshot live; clears the draft. **live, gated** |

## Themes

| Tool | What it does |
|---|---|
| `list_installed_themes` / `list_theme_gallery` | The site's themes / the gallery. |
| `install_theme` / `duplicate_theme` / `create_blank_theme` / `import_theme` | Add a theme without making it live. |
| `rename_theme` / `export_theme` | Rename / ZIP download link. |
| `set_active_theme` | Switch the live theme, no draft and no preview. **live, gated** |
| `get_theme_update` / `apply_theme_update` | Check / apply the shipped update; edited files are kept. Apply is **live, gated**. |

## Forms, submissions and automation

| Tool | What it does |
|---|---|
| `list_forms` / `get_form` / `list_form_presets` | Forms, their fields and statuses; ready-made presets. |
| `create_form` / `update_form` / `duplicate_form` | `fields` and `statuses` replace the whole set. **live** |
| `check_form_handle` / `suggest_form_handle` | Handles. |
| `trash_form` / `restore_form` / `get_form_analytics` | Trash and restore, views and conversion. |
| `list_submissions` / `get_submission` | Visitor answers, under `untrusted_visitor_data`. |
| `set_submission_status` / `bulk_set_submission_status` | Runs the form's workflows and webhooks, which may email the visitor. **live** |
| `mark_submission_read` / `trash_submission` / `restore_submission` | Inbox handling. |
| `list_submission_notes` / `add_submission_note` / `update_submission_note` / `delete_submission_note` | Internal team notes. |
| `find_visitor_data` / `export_visitor_data` | Privacy requests by email or phone. Erasure is panel-only. |
| `list_workflows` / `get_workflow` | Automations: trigger + ordered actions. |
| `create_workflow` / `update_workflow` / `duplicate_workflow` | `actions` and `trigger` replace whole. Acts on real data. **live** |
| `delete_workflow` | No trash; a workflow the active theme made cannot be deleted. **irreversible** |
| `list_workflow_runs` / `retry_workflow_run` / `rotate_workflow_signing_secret` | Runs, retries, HTTP-step signing secret. |
| `list_webhooks` / `create_webhook` / `update_webhook` / `test_webhook` | Form webhooks. Signing secret is shown only on create. |
| `list_webhook_deliveries` / `redeliver_webhook` | Delivery log and resend. |
| `delete_webhook` | No trash. **irreversible** |
| `*_data_list_webhook*` | The same set for a data list's entry events. |

## Marketing, widgets and email

| Tool | What it does |
|---|---|
| `get_tracking_codes` / `update_tracking_codes` | GA4, GTM, Meta Pixel; the update sets all three together. Update is **live, gated**. |
| `get_custom_code` / `update_custom_code` | HTML in head/body on every page; the update sets all four places together. Update is **live, gated**. |
| `get_cookie_consent` / `update_cookie_consent` | Consent banner. **live** |
| `get_chat_button` / `update_chat_button` | Chat button (WhatsApp, phone, email, Telegram, Messenger); send every argument back. **live** |
| `list_popups` / `get_popup` / `get_popup_stats` / `create_popup` / `update_popup` / `duplicate_popup` / `enable_popup` / `disable_popup` / `trash_popup` / `restore_popup` | Popups and bars. |
| `get_newsletter_settings` / `update_newsletter_settings` / `list_newsletter_subscribers` / `get_newsletter_subscriber` / `add_newsletter_subscriber` / `set_newsletter_subscriber_status` / `resend_newsletter_confirmation` | Newsletter; adding always sends a confirmation email. |
| `list_newsletter_audiences` / `set_newsletter_audience` / `sync_newsletter` / `list_newsletter_sync_log` | Mailchimp/Brevo sync (connecting the tool is panel-only). |
| `get_email_settings` / `update_email_sender` / `set_sending_domain` / `check_sending_domain` / `remove_sending_domain` / `list_email_deliveries` | Sender name, reply-to, own sending domain, delivery log. |

## Domains, health, data and history

| Tool | What it does |
|---|---|
| `list_domains` / `get_domain_dns_records` / `check_domain` | Custom domains and the DNS records the person must add. |
| `add_domain` | Connect a custom domain once its records are in place. Ask first. **gated** |
| `remove_domain` | The site stops answering at that domain at once. **gated** |
| `run_site_health` / `get_site_health` / `list_site_health_runs` | Broken links, missing SEO and alt text, translations, theme problems, each with where to fix it. One check at a time; about 6 runs an hour per website. |
| `get_site_analytics` / `export_site_analytics` | Cookieless visitor analytics. |
| `export_data` / `import_data` / `set_import_mapping` / `commit_import` / `cancel_import` / `get_transfer_status` | CSV/XLSX/JSON export; import with a dry run before commit. One transfer at a time per site; ten imports a minute. |
| `list_record_versions` / `get_record_version` | History of pages, forms, workflows, menus, redirects, site files, popups, data lists, media and settings. |
| `restore_record_version` | Undo for pages, forms, workflows, menus, redirects, site files and popups only. |
| `delete_trashed_*` | Delete ONE item already in the trash for good (route, form, popup, data list, entry, media, site file). **irreversible** |
