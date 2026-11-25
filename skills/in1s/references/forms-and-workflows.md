# Forms and workflows

What `create_form` / `update_form` and `create_workflow` / `update_workflow` take. Read an existing form or workflow
with `get_form` / `get_workflow` first: on an update, `fields`, `statuses`, `actions` and `trigger` each replace the
whole set.

## The form

| Setting | Rules |
|---|---|
| `name` | Required, 1–100 characters, translatable. |
| `handle` | A lowercase letter first, then lowercase letters, digits or `-`, not ending in `-`; at most 100; unique per site; **cannot change later**. Reserved: `index`, `404`, `password`, `storefront_password`, `localization`. Use `suggest_form_handle`. |
| `description`, `success_message` | Up to 500 characters, translatable. |
| `submit_label` | Up to 100 characters, translatable. |
| `captcha_enabled` | Default `true`. The provider is set per site (`update_settings` `captchaConfig`). |
| `stores_visitor_metadata` | Default `true`: keeps each submitter's IP address and browser. |
| `notification_emails` | Up to 20 addresses emailed on every submission. Needs the submissions edit permission. |
| `notification_subject` / `notification_intro` | Liquid over the submission, up to 200 / 2,000 characters: `New booking {{ reference_number }} from {{ name }}`. |
| `retention_days` | 1–3650: submissions older than this are **deleted for good**, daily. Needs submissions delete and may-publish. Ask first. |

Translatable values are `{"l10n": true, "en": "…"}`; the language keys are two letters.

## Fields

Every field has `id` (a lowercase letter, then lowercase letters, digits or `_`; unique), `type` and `label`. It may
also have `required`, `placeholder`, `info` (help text), `default` and `conditions`. A top-level field may set
`"unique": true`, which refuses a repeat value; `unique_window_minutes` limits that to a time window.

Reserved ids: `form_type`, `utf8`, `_honeypot`, `_captcha_token`, `_token`, `_method`. Limits: 200 fields, 300
options per field, 50 repeater sub-fields. Any text answer is at most 65,535 characters, and a submission at most
1 MB.

| Type | Extra settings |
|---|---|
| `text`, `textarea`, `email`, `tel`, `url` | `min_length`, `max_length`, `pattern` (a regular expression, text types only). |
| `number` | `min`, `max`, `step`. |
| `select`, `radio`, `checkbox_group` | `options`: `[{"value": "s", "label": {"l10n": true, "en": "Small"}}]`, values unique. |
| `checkbox` | A required checkbox must be ticked: use it for consent. |
| `date`, `datetime`, `time` | None. |
| `file` | `allowed_types` (extensions, such as `["pdf", "jpg"]`; empty allows any safe type) and `max_file_size` (MB, up to 50, default 10). One file per field. Executables are refused. Files are private and never shown publicly. |
| `hidden` | `value_from`, a Liquid path the theme fills in when it draws the form: under `entry`, `data_list`, `route`, `site`, `section` or `form` (`entry.id`, `route.title`), or exactly `request.path` or `request.host`. A visitor can change it, so treat it as visitor data. |
| `repeater` | `sub_fields` (any type but file, hidden, repeater, calculated), `min_rows` (default 1), `max_rows` (default 50). |
| `calculated` | `formula` and `precision` (0–10, default 2). Computed on the server at submit. |
| `entity_reference` | `reference_list`: a data list handle (optional). The answer is a published entry's id: "which product", "which event". |
| `submission_reference` | `reference_form`: a form handle. The answer is a submission's id: replies, threads. |
| `header`, `paragraph` | Display only. A header shows its `label`; a paragraph shows its `info`. |

### Calculated formulas

- **Operators:** numbers, `+ - * /` and parentheses. `%` is refused. Division by zero gives no value.
- **Functions:** `SUM`, `MIN`, `MAX`, `AVG`, `COUNT`, `ROUND`.
- **What a formula can name:**
  - other top-level fields by id: `guests * 25`;
  - a repeater column inside an aggregate: `SUM(items.price)`;
  - a repeater's row count: `COUNT(items)`.
- **Not allowed:** a repeater column inside `ROUND`, and loops between calculated fields.
- A calculated field cannot drive a condition.

### Conditions (show a field only when…)

```json
{"match": "all", "rules": [{"field": "extras", "operator": "contains", "value": "cake"}]}
```

- **`match`:** `all` or `any`. A rule names a field at the same level; a calculated, header or paragraph field cannot
  be a source.
- **Operators:**
  - Every theme supports `equals`, `not_equals`, `contains` (also membership in a checkbox group), `is_empty` and
    `is_not_empty`.
  - `starts_with`, `ends_with`, `not_contains`, `greater_than`, `less_than`, `between` (with `value_to`, inclusive)
    and `in_list` (`value` is a list of up to 100 items) work only when the active theme supports them. `get_form`
    answers `condition_operators`, the set that will be accepted.
  - `greater_than`, `less_than` and `between` compare a number, a date (`YYYY-MM-DD`, optionally `THH:MM`) or a time
    (`HH:MM`).
- **Where it applies:** both in the browser and on the server. A hidden field's answer is not stored.

## Statuses and transitions

```json
{
  "statuses": [
    {"key": "new", "label": {"l10n": true, "en": "New"}, "color": "blue"},
    {"key": "confirmed", "label": {"l10n": true, "en": "Confirmed"}, "color": "green"},
    {"key": "cancelled", "label": {"l10n": true, "en": "Cancelled"}, "color": "red"}
  ],
  "default_status": "new",
  "status_transitions": {"new": ["confirmed", "cancelled"], "confirmed": ["cancelled"]}
}
```

- A form has no statuses until you give them. Keys are at most 50 characters and distinct ignoring case and accents.
- Removing a status that submissions still hold, or that `public_listing` shows, is refused.
- `status_transitions`: a status listed as a key may move only to its targets. A status not listed may move anywhere.
  It applies to `set_submission_status`, bulk moves, workflows and the public callback.
- Every real status change runs the form's `form.status_changed` workflows and its webhooks. Setting the same status
  again runs nothing.

## Other form settings

| Setting | Shape | What it does |
|---|---|---|
| `capacity` | `{"limit": 40, "count_statuses": ["confirmed"], "per_fields": ["day"], "count_field": "guests"}` | Refuses submissions past the limit. It counts only `count_statuses` (empty means all), per value of `per_fields` (for example per day), or sums `count_field` instead of counting. A half-filled session holds a place for 30 minutes. |
| `waitlist_config` | `{"status": "waitlist", "reference_field": "<entity_reference field>", "capacity_field": "<number field of that list>", "max_notify": 5}` | When the referenced entry's capacity rises above 0, up to `max_notify` waiting submissions fire `form.waitlist_available`. |
| `submission_expiry` | `[{"when_status": "new", "after_hours": 48, "set_status": "cancelled"}]` | Moves stale submissions on, checked hourly. |
| `session_config` | `{"enabled": true}` | Keeps a visitor's answers between visits (multi-step forms, carts). |
| `lookup_config` | `{"enabled": true, "verify_field": "email"}` | Lets a visitor look up their own submission by reference number plus that field. Pair it with a `generate_reference` workflow. Needs the submissions edit permission. |
| `public_listing` | `{"statuses": ["approved"], "fields": ["name", "message"]}` | Shows those submissions on the entry they reference (comments, reviews). A theme reads them with `submissions_for`. File, email and phone fields can never be listed. Moderate with `set_submission_status`. |
| `newsletter_config` | `{"enabled": true, "email_field": "email", "consent_field": "<checkbox id>"}` | Adds submitters to the newsletter, after a confirmation email under double opt-in. With a consent checkbox, only those who tick it join. |
| `redirect` | `{"type": "http_link", "value": "/thanks?ref={reference_number}"}` | Where the visitor goes after submitting. Types are `frontpage_link` (no value), `http_link` (a URL or `/path`; `{submission_id}` and `{reference_number}` are filled in), and `route_link`, `data_list_link`, `data_list_entry_link` (an id). |

## Workflows

```json
{
  "name": {"l10n": true, "en": "Confirm booking"},
  "is_enabled": false,
  "trigger": {"event": "form.status_changed", "resource": {"type": "form", "form_id": 12}, "conditions": {"status": "confirmed"}},
  "actions": [
    {"type": "send_email", "to": "{{ email }}", "subject": {"l10n": true, "en": "Booking {{ reference_number }} confirmed"}, "body": {"l10n": true, "en": "See you on {{ day }}."}},
    {"type": "delay", "amount": 1, "unit": "days"},
    {"type": "send_email", "to": "{{ email }}", "subject": {"l10n": true, "en": "Reminder: booking {{ reference_number }}"}, "body": {"l10n": true, "en": "A reminder of your booking on {{ day }}."}}
  ]
}
```

Limits: 10 workflows per form, 10 per data list, 10 scheduled per website. A workflow is live when created unless
`is_enabled` is `false`. Create it disabled, show the person what it will send, and enable it with `update_workflow`
when they agree.

### Triggers

| Trigger | Shape |
|---|---|
| A form is submitted | `{"event": "form.submitted", "resource": {"type": "form", "form_id": 12}}` |
| A submission's status changes | `{"event": "form.status_changed", "resource": {…}, "conditions": {"status": "confirmed"}}`. Without `conditions` it runs on every change. |
| A waitlist place opens | `{"event": "form.waitlist_available", "resource": {…}}` |
| An entry changes | `{"event": "entry.created" \| "entry.updated" \| "entry.published" \| "entry.deleted", "resource": {"type": "data_list", "data_list_id": 7}}`. Imports do not trigger it. |
| A schedule | `{"event": "schedule.tick", "schedule": {"every": "hourly" \| "daily" \| "weekly", "at": "09:00", "weekday": 1, "timezone": "Europe/Berlin"}}`. `timezone` is required (an IANA zone). `weekday` is weekly only, with 0 = Sunday. |

`generate_reference`, `set_status`, `set_field` and `update_entry` need a submission, so they are refused under an
entry or schedule trigger.

### Values in templates

`{{ … }}` in actions reads:

- **A submission:** each answer by field id (`{{ email }}`), `{{ reference_number }}`, `{{ form.name }}`,
  `{{ form.handle }}`, and `{{ submission.id }}` / `status` / `created_at`. An `entity_reference` answer reads as its
  entry: `{{ product.title }}`.
- **An entry trigger:** its field values, `{{ entry.title }}`, `{{ data_list.handle }}`.
- **A schedule:** `{{ schedule.date }}`, `{{ schedule.time }}`.
- **After a `find_submission` step:** `{{ found.<output_as>.<field> }}`.

Email subjects and bodies are Liquid with a safe set of tags (`if`, `unless`, `case`, `for`, `assign`, `capture`).

### Actions

Settings sit directly on the action. Any action may add `"continue_on_failure": true`.

| Action | Settings | Notes |
|---|---|---|
| `generate_reference` | `prefix` (required), `pad_length` (default 5) | Gives the submission `BK-00042`. Runs within the submit. |
| `send_email` | `to` (required; addresses or `{{ field }}`, comma-separated, at most 5: more is refused when the workflow is saved), `reply_to`, `subject`, `body` (required; text or `l10n` map, Liquid) | Newlines in the body become line breaks. 100 a minute per site. A blank optional recipient skips the step. |
| `create_entry` | `data_list` (handle, required), `title` (template), `field_mapping` `{"<entry field>": "{{ answer }}"}`, `is_published` (default `true`) | Values a field refuses are left out and logged as warnings. Fires `entry.created`. |
| `update_entry` | `reference_field` (the form field holding the entry id, or rows holding it), `operations` `[{"field": "stock", "operation": "decrement", "value_field": "qty", "min_value": 0}]` (`increment`, `decrement`, or `set` with `value_field` or `value`), `validate_before_submit` | Stock, seats, counters. `validate_before_submit: true` refuses the submission when the step would fail (sold out). |
| `set_status` | `status` (required), `conditions` (the field-condition shape, every operator allowed) | Skips when the conditions don't match. Follows `status_transitions`. |
| `set_field` | `field` (not calculated), `value` (literal or template) | Runs within the submit. |
| `find_submission` | `form_handle`, `filters` `{"status": "paid", "data.email": "{{ email }}"}`, `order`, `direction`, `output_as` | Makes `{{ found.<output_as>.<field> }}` available to later steps. |
| `delay` | `amount`, `unit` (`minutes`, `hours`, `days`) | 1 minute to 30 days. The steps after it run later. |
| `http_request` | `method`, `url` (starts with a literal `https://` or `http://` host; values may fill the path and query), `headers` (up to 20), `body` (JSON text for POST/PUT/PATCH, values inside quotes), `sign` | 10-second timeout, no redirects, up to 3 attempts, 120 a minute per site. Private addresses are refused. `sign: true` adds an HMAC signature with the workflow's secret (`rotate_workflow_signing_secret`). Sends data outside: ask first. |

### Runs

`list_workflow_runs` shows each run's status and steps. A failed run with no `retry_blocked_reason` can be retried
with `retry_workflow_run`, which re-runs only the failed steps; a failed `send_email` sends then. A status change made
by a workflow runs that status's workflows once per chain, so loops stop on their own.

## Putting a form on the site

A theme section with a `form` setting renders it: set that setting to the form's handle with `upsert_section`. Theme
authors: [the theme skill's data-list templates reference](../../in1s-theme-development/references/data-list-templates.md)
covers `{% form %}`, `form.session` and `submissions_for`.
