---
name: in1s-theme-development
description: Use when changing how an in1s website looks or is built - adding, moving or editing sections and blocks, theme settings, colors, fonts, storefront translations, or writing Liquid theme files (sections, blocks, snippets, templates, CSS, JS, assets) through the in1s MCP tools such as get_theme_catalog, get_template, upsert_section, write_theme_file and validate_theme. Also when porting a Shopify-style section or making a theme work right-to-left.
license: MIT
metadata:
  author: in1s
  version: "1.7.0"
  homepage: https://in1s.com
---

# in1s theme development

in1s themes are Shopify-style Liquid themes (`layout/`, `templates/`, `sections/`, `blocks/`, `snippets/`, `config/`,
`locales/`, `assets/`) running on in1s's own engine, which differs from Shopify in places. Every theme write lands in the
theme's **shared draft**. Visitors see it only after `publish_draft`. Read the **in1s** skill first for connecting,
permissions and what is live.

**Core principle:** compose before you code. Most requests are met by the sections the theme already has, placed and
configured. Write a new file only when nothing in the catalog can do the job.

## Choose the level

| Request | Level | Tools |
|---|---|---|
| Change a text, image, link or option in a section | Configure | `get_template` → `upsert_section` |
| Add, move or remove a section on a page | Compose | `get_theme_catalog` → `get_template` → `upsert_section` (with `position` / `remove`) |
| Colors, fonts, spacing across the site | Theme settings | `get_theme_settings` → `update_theme_settings` (fonts from `list_fonts`) |
| A storefront label (button, heading, message) | Translations | `get_translations` → `update_translations` |
| A section type the theme does not have | Code | `get_liquid_reference` → read a similar section → `write_theme_file` |
| A list's listing or entry pages, comments, search | Code | [references/data-list-templates.md](references/data-list-templates.md) |
| A redesign, or "make it modern" | Design, then code | Ask first: see "Building another theme" below, then [references/design-and-motion.md](references/design-and-motion.md) |

Before writing a new section, look for what already exists:

- `get_theme_catalog` lists the section types a template may hold.
- `list_theme_files` with `prefix: "sections/"` lists every file, including types only rendered by code.
- `snippets/` holds the theme's reusable parts: cards, buttons, signup forms, icons, section intros.
- `search_theme_code` finds related work by keyword.

A theme often already has a pricing, FAQ, testimonial or gallery section under another name. Reuse it rather than
write a duplicate. Build a new section out of the theme's snippets, CSS classes and color schemes, so it matches the
rest of the site.

Every theme tool works on the **active** theme. An installed theme that is not live cannot be read, edited, rendered or
previewed through the MCP; `set_active_theme` must make it live first.

### Building another theme

`duplicate_theme` (a copy of what visitors see) or `create_blank_theme` adds a theme without making it live. To build
it, it has to become the active theme, which shows it to visitors at once. Before doing that, get the person's
explicit go-ahead, and agree on one of these:

- Build it in place on the live theme instead, as draft edits, so visitors keep the published version until
  `publish_draft`.
- Switch while the site is in maintenance mode (`update_settings` `maintenanceMode`), then switch back
  (`list_installed_themes` → `set_active_theme`).

## The loop

1. **Read**: `get_draft_status` (the draft is shared; note other people's changes), then `get_template` or
   `read_theme_file`. Keep the `versions` / `versionId` the read returns. When you only change the template, pass
   `get_template` `include_groups: false`, `include_layout: false` and `include_schemas: false`: the answer is a
   fraction of the size.
2. **Write**: send the `base_version` / `base_versions` you read. A conflict means someone saved in between: read
   again, merge, retry. Change an existing file with `edit_theme_file` (exact `old` → `new` pieces), and one section
   with `upsert_section`. Keep `write_theme_file` for new files: resending a whole stylesheet or template to change a
   line wastes the person's tokens and risks overwriting a collaborator's edit.
3. **Check**: `validate_theme` (errors block publishing), then `render_page` on an affected page in **every**
   language: `errors`, the section order, the text, the links (an Arabic page's links should be Arabic URLs).
4. **Look**: `render_page` is text only. It cannot show layout, CSS, overflow, contrast or motion. See "Look at
   the page" below.
5. **Show**: `create_preview_link` and give the person the link. Each call ends the previous link this token made.
   The link lets anyone who has it see the draft until it expires: give it to the person in your reply and nowhere
   else (never in a file, commit, issue, log or message to anyone else), and `revoke_preview_link` it once they
   have looked.
6. **Publish** only when the person asks, and only with `may_publish`. Tell them whose changes are in the draft first.

Settings in `upsert_section` are **replaced, not merged**: send every setting and block you keep, exactly as
`get_template` returned them, with only your change applied. `update_sections` replaces whole containers: a section
left out of a template's `sections` is removed. A section type whose schema has no `presets` cannot be added to a
template: `upsert_section` answers "it has no presets". Give a new section a preset before placing it.

## Look at the page

No MCP tool shows what a page looks like. Bugs that only a screenshot reveals: a sticky header that scrolls away, a
strip of the wrong background, text that overflows on a phone, a heading that came out as a `<div>`, content left
invisible by a reveal animation, poor contrast over a photo.

- **If you can run a browser** (Playwright, Chrome tools): open the `create_preview_link` URL at about 1440 and 390
  pixels wide, and once in each right-to-left language. Scroll the whole page with real wheel events, since scroll
  animations only start then. Check the console for errors, that `document.documentElement.scrollWidth` is not wider
  than the window, that nothing is still hidden, that menus and the language switch work, and that it still reads
  with `prefers-reduced-motion: reduce`. Fix what you find before you report.
- **If you cannot**, say so plainly in your report ("checked the text and links, not the layout") and ask the person
  to look at the preview on a phone and a computer.

A preview link opens the draft for the browser session it is opened in. Switching language on the previewed site
keeps the preview.

## Content in settings

- **Links** to the site's own pages use references, which follow the visitor's language:
  `in1s://routes/handle:download`, `in1s://data-lists/blog-posts`, `in1s://data-lists/blog-posts/{slug}`. This works
  in `url` settings **and** inside `richtext` settings (`<a href="in1s://data-lists/services/seo">`): on an Arabic page
  both print the Arabic URL. A typed `/services/seo` gets only the `/ar` prefix, and an entry whose Arabic slug differs
  then answers through a redirect at best. `{slug}` may be the entry's slug in any language.
- **Image and video settings** take a media library **uuid** (`list_media`, `upload_media_from_url`). An address there
  is kept but shows nothing; the answer's `normalized` reports it as `media_external`.
- **Real facts only**: prices, plan features, dates, phone numbers, addresses, testimonials and statistics come from
  the person. If they are missing, keep the theme's preset text (`list_placeholders` tracks it) and list what you need.
  Never write invented figures into a section, even "as stand-ins". For a new section that cannot work without one
  fact (a countdown without its date, a map without its address), render nothing on the site until that setting is set,
  and show a short hint only in the editor: `{% if section.settings.launch_at != blank or is_editing %}`.

## Writing a section file

Call `get_liquid_reference` once per session. Its `rules` are the authoring guide, and `validate_theme` reports each
rule's `code`. Use only the tags and filters it lists: an unknown filter passes its input through unchanged, without
an error. Then read one similar section in the theme and match its structure, class names, CSS variables and color
schemes.

A minimal section that passes every check. It was run through the in1s theme validator in a shipped theme with its
locale keys added, and gave no diagnostics:

```liquid
<section class="section feature-list" {{ section.in1s_attributes }}>
  <div class="page-width">
    {%- if section.settings.heading != blank -%}
      <h2 data-setting-id="heading" data-setting-type="text">{{ section.settings.heading | escape }}</h2>
    {%- endif -%}
    <ul class="feature-list__items">
      {%- for block in section.blocks -%}
        <li class="feature-list__item" {{ block.in1s_attributes }}>
          <h3 data-setting-id="title" data-setting-type="text">{{ block.settings.title | escape }}</h3>
          <div class="rte" data-setting-id="text" data-setting-type="richtext">{{ block.settings.text }}</div>
          {%- if block.settings.link != blank -%}
            <a href="{{ block.settings.link | escape }}">{{ 'sections.feature-list.learn_more' | t }}</a>
          {%- endif -%}
        </li>
      {%- endfor -%}
    </ul>
  </div>
</section>

{% schema %}
{
  "name": "t:sections.feature-list.name",
  "tag": "div",
  "class": "section-wrap",
  "max_blocks": 12,
  "settings": [
    { "type": "text", "id": "heading", "label": "t:sections.feature-list.settings.heading.label" }
  ],
  "blocks": [
    {
      "type": "item",
      "name": "t:sections.feature-list.blocks.item.name",
      "settings": [
        { "type": "text", "id": "title", "label": "t:sections.feature-list.blocks.item.settings.title.label" },
        { "type": "richtext", "id": "text", "label": "t:sections.feature-list.blocks.item.settings.text.label" },
        { "type": "url", "id": "link", "label": "t:sections.feature-list.blocks.item.settings.link.label" }
      ]
    }
  ],
  "presets": [
    {
      "name": "t:sections.feature-list.presets.preset_1",
      "settings": { "heading": "Why people choose us" },
      "blocks": [
        { "type": "item", "settings": { "title": "First reason", "text": "<p>One or two sentences.</p>" } },
        { "type": "item", "settings": { "title": "Second reason", "text": "<p>One or two sentences.</p>" } }
      ]
    }
  ]
}
{% endschema %}
```

Why each part is there:

- `{{ section.in1s_attributes }}` on the **first** element and `{{ block.in1s_attributes }}` on each block's root let
  the editor select them. Without them you get `missing_root_attributes`.
- `data-setting-id` / `data-setting-type` on the element that prints exactly one setting makes it editable in place
  (`missing_setting_marker`). Text goes through `| escape`; richtext prints raw.
- Every schema `name` and `label` is a `t:` key. Visitor-facing words come through `| t`. Both need their keys
  (next section).
- `presets` puts the section in the editor's **Add section** list.
- The theme's shared settings (color scheme, spacing, alignment) are left out here because their keys differ between
  themes. Copy those settings, their `t:` labels and their markup from a sibling section in the same theme, so the
  labels exist and the defaults (such as a color scheme id) are ones the theme defines.

Then add the keys:

- **Storefront words** (`| t`): `update_translations` with `allow_new_keys: true`, for example
  `{"sections.feature-list.learn_more": "Learn more"}`. Do it for **every** language `get_translations` lists in
  `locales`, not only the default one. A key missing from another language raises `partial_locale_file`, and that
  language's visitors see the default text.
- **Editor labels** (`t:` in the schema): `edit_theme_file` on `locales/en.default.schema.json`. It is a large
  protected file, which can be edited but not moved or deleted. Find a unique anchor at the right depth with
  `search_theme_code` (for example the line that opens a neighbouring section's object), and insert the new
  `"feature-list": { "name": …, "settings": …, "blocks": …, "presets": … }` object there, matching the file's
  indentation.

Then run `validate_theme`. Only `error`s block a publish: broken Liquid or JSON, a missing snippet or section file.
`missing_root_attributes`, `missing_setting_marker`, `missing_translation` and `missing_schema_translation` are
**warnings**. They do not stop a publish, but each one breaks the editor or a language for the person, so clear every
warning your change introduced.

## Engine rules that differ from Shopify

These come from `get_liquid_reference`; read its full list for the rest.

- **Pages are cached for every visitor alike.** A published change shows on the next request. Output that moves with
  the clock alone (`'now' | date` with minutes, a countdown) can be up to 10 minutes old, and live counts
  (`form.submissions_count`, the `submissions_*` filters) up to 5 seconds. A visitor with a cart or a session always gets
  their own page, but never print per-visitor or per-moment values into the HTML for everyone: read them in the browser.
- **A filter argument takes no filters, and neither does a tag argument.** Use `{% assign %}` first:
  `{% assign handle = section.settings.form | default: 'contact' %}{% form handle %}…{% endform %}`. A filter inside a
  `{% for %}` expression is ignored.
- **`{% render %}` is isolated**: pass everything the snippet needs as a parameter. `{% include %}` shares scope.
- **Paths go through `route_url`**: `{{ '/contact' | route_url }}`. A literal `href="/contact"` sends visitors of
  another language to the default one.
- **`data_list.entries` is one page** (`page_size`, 12 unless set). Wrap the loop in
  `{% paginate data_list.entries by data_list.page_size %}`. `data_lists['handle'].entries` is the first 50, and
  `entry.previous` / `entry.next` are the neighbours (never loop a list for them). Templates,
  filters, sorting, entry fields and comments: [references/data-list-templates.md](references/data-list-templates.md).
- **The engine wraps each section** in `<div id="in1s-section-{id}" class="in1s-section …">` exactly as tall as the
  section, so `position: sticky` goes on the **wrapper**: set the schema's `"class"` and style that class.
- **Scripts must survive editor re-renders**: set up again on `in1s:section:load`, and clean up timers and observers on
  `in1s:section:unload`. Never hide content until a script reveals it unless that handler exists, or the section turns
  blank in the editor (`section_load_unhandled`). Most themes already have one setup helper in their main script that
  handles both events (search `assets/` for `in1s:section:load`). Register with it rather than adding listeners.
- **Text a script writes** cannot go through `| t` at that moment. Render the translated words into the markup
  (`data-*` attributes or hidden elements) and let the script pick them. Format numbers and dates with `Intl` in the
  page's `lang`.
- **Visitor values are hostile**: `form.session.*` and submission data print through `| escape`, numbers through
  `| times: 1`, and links only through a `safe-relative-url` snippet where the theme has one (never print a visitor-written link without it).
- **Plurals and parameters** go through `t`: `{{ 'sections.reviews.count' | t: count: reviews.size }}`. Never build a
  sentence from fragments.

## Languages and right-to-left

- `<html lang="{{ request.locale.iso_code }}" dir="{{ request.locale.text_direction }}">` in the layout.
- Use logical CSS (`margin-inline-start`, `inset-inline-end`, `text-align: start`) rather than left and right.
- A language switcher links `language.url | default: language.root_url` for each of
  `localization.available_languages`.
- Fonts must cover the script. Check the theme's current fonts (`get_theme_settings`) before calling a theme ready
  for a new script. Many Latin fonts have no Arabic letters. For Arabic, `list_fonts` offers `ibm_plex_sans_arabic`,
  `noto_kufi_arabic`, `cairo`, `tajawal` and `alexandria`. Call `list_fonts` **without** `search` (and with
  `per_page: 100`) to see the whole library; a search narrows it, and a family missing from a filtered answer may
  still be there.
- A family the library does not have: `upload_font_from_url` with the font file's own address (a `.woff2`, not a
  stylesheet URL) so the site serves it itself. Loading it from Google Fonts or another CDN in the layout also works,
  but it is a third-party request on every page: tell the person.
- Arabic text: `letter-spacing: 0` (tracking breaks joined letters), a taller `line-height` than Latin, and no
  word-by-word splitting that separates letters of one word. Wrap phone numbers and Latin codes in `<span dir="ltr">`.
- A new storefront language: the site gets it first (`update_settings` `locale`), then the theme
  (`add_theme_language`, then `update_translations`).

## Assets

`upload_theme_asset_from_url` with a path such as `assets/hero.webp` (images, fonts, SVG; SVG is cleaned of scripts).
Reference it with `{{ 'hero.webp' | asset_url }}`. CSS and JS are text files: use `write_theme_file` or
`edit_theme_file`. Content images belong in the media library, not in `assets/`.

## Common mistakes

| Mistake | Result | Instead |
|---|---|---|
| Sending only the changed setting to `upsert_section` | Every other setting is wiped | Send the section as read, with one change |
| Writing a new section when the theme has one | A duplicate to maintain | Check the catalog and `sections/` first |
| Typing `/about` in a link setting | Wrong language, breaks on slug change | `in1s://routes/handle:about` |
| An image URL in an image setting | Nothing shows (`media_external`) | Upload to the media library, use the uuid |
| `| default:` after a filter with arguments | Defaults the whole chain | `{% assign %}` first |
| A Shopify-only filter or object | Passes through silently | Only what `get_liquid_reference` lists |
| Publishing to "see it" | Everyone's draft goes live | `render_page` and `create_preview_link` |
| Placeholder prices or quotes | Invented facts on a live site after publish | Ask, or keep the preset text |
| `write_theme_file` with the whole file to change a line | Large resend; a collaborator's edit can be lost | `edit_theme_file` |
| A reveal animation that starts with `opacity: 0` in plain CSS | Blank page without JavaScript, in the editor, or for reduced motion | Hide only under a class the script adds ([design-and-motion.md](references/design-and-motion.md)) |
| Calling the work done after `render_page` | Layout bugs nobody saw | Look at the preview in a browser, or say you could not |
| A typed `/ar/...` URL in an Arabic text | Breaks when a slug changes | `in1s://` reference; it prints the right URL per language |

## When something breaks

- **Write refused, "would not render"**: the error names the line. Fix the Liquid or JSON and resend; nothing was saved.
- **Publish refused**: `validate_theme` errors, or a file marked `changedUnderneath`. For the latter,
  `read_theme_file` with `view: "published"`, merge, then `write_theme_file` with that `versionId`.
- **A page renders a blank section**: `render_page` `errors` names it. Check `get_file_references` for a missing
  snippet.
- **Undo one file**: `list_file_versions`, then `restore_theme_file`. `discard_draft_file` drops the draft's change of
  that file whoever made it, and needs may-publish.
- **Undo a whole publish**: `list_snapshots`, then `restore_snapshot`, only when the person asks.
