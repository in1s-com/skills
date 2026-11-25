# Data list fields and entry values

What `create_data_list` / `update_data_list` take as `fields`, and what `create_entry` / `update_entry` take as
`data`. Read the list's fields with `get_data_list` first; `data` is keyed by those field ids.

## Writing an entry

- `data` holds one value per field id. A key that is not a field of the list is refused, and the error names the
  valid ids (on an update, a key the entry already stores is kept).
- **Reference fields do not go in `data`.** They go in the separate `references` argument:
  `{"author": [12]}` or `{"author": [{"id": 12}]}`. A reference key put in `data` is stored without a check, and
  the site never shows it.
- On `update_entry`, `data` is merged one level deep: fields you leave out keep their values. Inside a translatable
  value only the languages you send change, and a language sent as `null` is removed. A structure's rows are replaced
  as a whole.
- Strings are trimmed, and `""` becomes `null`. To remove one language, send it as `null`, not `""`.
- A non-required field accepts `null` (empty). A required field counts as missing when it is `null`, `""`, `[]`, or a
  translatable map with every language empty. `false` counts as a value.
- No field has a length limit of its own; only the request size (16 MB) bounds it.

## Translatable values

Only `text`, `textarea` and `richtext` can be translatable (the default for those three). Their value is either a plain
value or a language map:

```json
{"l10n": true, "en": "Blue mug", "ar": "كوب أزرق"}
```

**Language keys must be exactly two letters** (`en`, `ar`, `fr`). A key such as `pt-BR` refuses the whole value. Use
the codes `get_settings` lists for the site.

Setting `translatable: true` on any other type does not fail: it is stored as `false` and reported under `warnings`.

## Value per type

| Type | Value | Rules |
|---|---|---|
| `text` | `"Blue mug"` or an `l10n` map | String. The field's `pattern`, if set, applies. |
| `textarea` | `"Line 1\nLine 2"` or an `l10n` map | String. **Not sanitised**: themes print it as written. |
| `richtext` | `"<p>Text with <a href=\"in1s://routes/12\">a link</a></p>"` or an `l10n` map | Sanitised on save, see below. |
| `number` | `12.5` | Numeric, finite, within `min`/`max`. `step` is not enforced. |
| `range` | `40` | Within `min`/`max`, **and on the `step` grid** counted from `min`. |
| `select`, `radio` | `"small"` | One option's `value`, **same JSON type**: `7` does not match `"7"`. |
| `checkbox` | `true` | A real boolean. `"true"` and `1` are refused. |
| `checkbox_group` | `["red", "blue"]` | A list of distinct option values, same JSON type. |
| `color` | `"#1a2b3c"` | `#rgb`, `#rgba`, `#rrggbb` or `#rrggbbaa`. |
| `url` | `"https://example.com"`, `"/about"`, `"#top"`, `"mailto:…"`, `"tel:…"`, `"in1s://routes/handle:about"` | http, https, mailto, tel, a path or anchor, or an `in1s://` site link. `javascript:` and `data:` are refused. Syntax only: the target is not looked up. |
| `video_url` | `"https://youtu.be/abc"` | http or https only. |
| `date` | `"2026-11-25"` | Exactly `YYYY-MM-DD`, a real calendar date. No time. |
| `image_picker` | `"<media uuid>"` | The uuid of an **image** in the site's media library. A URL or numeric id is refused. |
| `video` | `"<media uuid>"` | The uuid of a **video** in the media library. |
| `font_picker` | `"inter_n4"` | Any string. |
| `html` | `"<div>…</div>"` | Not validated and not sanitised. Stored as sent. |
| `liquid` | `"{{ x }}"` | Not validated, and not rendered as a template in entries. |
| `reference` | (in `references`) `[12, 15]` | See "Reference fields". |
| `structure` | `[{"name": "A", "photo": "<uuid>"}]` | See "Structure fields". |

### Reference fields

- Each id is an integer naming a live entry of the list the field's `reference_list` names. An id from another list
  is refused, not dropped.
- Ids are distinct. A field without `multiple: true` takes one link.
- The list you send replaces the field's links, in that order.
- `get_entry` answers them as `references: {"author": [{"id": 12, "title": …, "slug": …}]}`.

### Structure fields (repeating rows)

- A **list** of row objects, each keyed by the structure's sub-field ids. A row key that is not a sub-field is refused.
- Rows get an `_id` when stored. Send rows back with their `_id` to keep them stable.
- `max` on the field caps the number of rows; `min` is not enforced on values.
- Sub-field types: `text`, `textarea`, `url`, `select`, `checkbox`, `number`, `range`, `color`, `date`,
  `image_picker`, `video`, `video_url`. Each takes the same value as above.

### Richtext sanitising

Text without `<` is stored as written. Otherwise:

- **Kept tags:** p, br, strong, em, b, i, u, s, a, ul, ol, li, h1–h6, blockquote, pre, code, img, table, thead, tbody,
  tr, td, th, hr, div, span, figure, figcaption, sup, sub, mark, small, abbr, del, ins, strike, video, source.
- **Removed with their content:** `script`, `style`, `iframe`, `object`, `embed`, `template`, `noscript` and similar.
  Embed a video with a `video_url` field instead of an iframe.
- **Attributes:**
  - Every kept tag may carry `class`, `id`, `title`, `dir` and `lang`.
  - `a` also takes `href`, `target` and `rel`.
  - `img` also takes `src`, `alt`, `width`, `height` and `loading`.
  - Table cells take `colspan` and `rowspan`.
  - Links must be http, https, mailto, tel or `in1s://`.
- **Size:** over 100 KB of HTML, all markup is stripped to plain text. Split long content across fields or entries.

Disallowed markup is dropped without an error, so read the entry back when exact markup matters.

## Defining fields

```json
{
  "id": "price",
  "type": "number",
  "label": {"l10n": true, "en": "Price"},
  "required": true,
  "filterable": true,
  "min": 0
}
```

| Key | Rules |
|---|---|
| `id` | Lowercase letter first, then lowercase letters, digits, `_`. Unique in the list. |
| Reserved ids | `id`, `title`, `slug`, `handle`, `url`, `published_at`, `created_at`, `updated_at`, `seo_title`, `seo_description`, `template_suffix`, `object_type`, `data_list`, `referenced_by`, `popularity`, `first`, `last`, `object`. A filterable field also may not be `page`, `sort` or `direction`, nor `<x>_min` / `<x>_max` where `<x>` is a filterable number field. |
| `type` | text, textarea, richtext, number, range, select, radio, checkbox, color, url, image_picker, video, video_url, date, font_picker, html, liquid, checkbox_group, reference, structure |
| `label` | Required. A string or an `l10n` map. `placeholder`, `info` and option labels work the same way. |
| `translatable` | Text, textarea and richtext only (on by default). |
| `required` | Default `false`. |
| `filterable` | Only `reference`, `select`, `checkbox`, `checkbox_group`, `number` (not `radio`). Makes the field a filter on the list's page. |
| `options` | `select`, `radio`, `checkbox_group`: at least one `{"value": "small", "label": {"l10n": true, "en": "Small"}}`, values unique. |
| `min`, `max`, `step` | `number`, `range` (`range` needs both `min` and `max`; `step` > 0). On `structure`, the row count. |
| `pattern` | A regular expression for text-like values. |
| `reference_list`, `multiple` | `reference`: the handle of the target data list, and whether it takes several links. |
| `fields` | `structure`: its sub-fields `{id, type, label}`, at least one, at most 50. |

Limits: 200 fields per list, 300 options per field, 3,000 options per list.

- **`update_data_list` replaces the whole `fields` set**: send every field you keep.
- **Changing a field's type** to richtext, html or textarea is refused while entries hold `<` in it.
- **`defaultSortField`** may be `title`, `created_at`, or a field that is not structure, richtext, image_picker,
  video, html, liquid, reference or font_picker.
- **A list handle** starts with a lowercase letter, then lowercase letters, digits or `-`, and does not end in `-`; at
  most 100 characters; unique per site, and set only when the list is created. It may not be `index`, `404`,
  `password` or `up`.
