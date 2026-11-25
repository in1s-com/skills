# Rendering data lists, entries, forms and search

How a theme shows a data list's listing page and entry pages, other lists anywhere on the site, form submissions
such as comments, and search. Field ids in the examples are illustrative: read the real ones with `get_data_list`.

## Which template renders which page

| URL | Template | Exists when |
|---|---|---|
| `/<list slug>` | `data-list.<handle>.json` | the list's `pageConfig` is `both` or `listing_only` |
| `/<list slug>/<entry slug>` | `entry.<handle>.json`, or `entry.<handle>.<suffix>.json` when the entry has a `templateSuffix` | `pageConfig` is `both` or `entry_only`, and the entry is published |
| `/<page path>` | `route.<path>.json` with each `/` as `-` (`legal/privacy` → `route.legal-privacy.json`), or `route.<path>.<variant>.json` | the route is published |
| `/search` | `search.json` | always |

A missing template falls back by dropping its last dot-segment:

- `entry.blog-posts.featured.json` → `entry.blog-posts.json` → `entry.json`
- `data-list.<handle>.json` → `data-list.json`
- `route.<path>.json` → `route.json`

The gallery themes ship the generic `data-list.json`, `entry.json` and `route.json`, so a new list renders at once.
Check with `list_theme_files` `prefix: "templates/"`. Give
it its own look by adding `data-list.<handle>.json` / `entry.<handle>.json` (`write_theme_file`), or an alternate
layout with `create_template`.

A template file names its sections:

```json
{"sections": {"main": {"type": "main-blog-listing", "settings": {}}}, "order": ["main"]}
```

The page's title, description, share image, canonical link, language alternates and noindex come from the list's or
entry's SEO. The theme does not print them itself.

## Three ways to reach a list

| Access | `.entries` holds | Use for |
|---|---|---|
| `data_list` on its own listing or entry page | **one page** (`page_size`, the list's `entriesPerPage`, 12 by default) | The listing itself |
| A section setting of type `data_source` | **one page**, and it follows the page's `?page=`, filter and sort parameters | "Latest posts" on another page |
| `data_lists['handle']` | **every published entry**, not paged; the page's own filter and sort parameters still apply to it | Small lists you need whole: plans, team, FAQ |

`{% for entry in data_list.entries limit: 6 %}` slices the current page only; it cannot return more than
`page_size`. To page any of them: `{% paginate X.entries by N %}`, with N from 1 to 250.

## The `data_list` object

- **Basics:** `id`, `title`, `handle`, `url` (in the visitor's language; blank when the list has no listing page),
  `seo_title`, `seo_description`.
- **Entries and paging:** `entries`, `entries_count` / `total_entries` (after filters), `current_page`, `total_pages`,
  `page_size`.
- **Fields:** `fields`, the list's fields in order, as `{id, label, type}`; a structure carries its sub-fields as
  `fields`.
- **Filtering and sorting:** `filters`, `sort_options`, `active_sort`, `active_direction`, and the query strings
  `filter_query` and `listing_query` (each starts with `&`; `listing_query` includes the sort).
- **`facet`:** set when the listing is filtered to exactly one value of a select, checkbox group or reference field
  (a tag page, an author page): `{field_id, field_label, value, label, url}`.
- **`feed_url`:** the Atom feed, when enabled.

### Filters and sorting in the URL

Only fields marked `filterable` are filters, and the parameter is the field id itself:

| Field type | Parameter |
|---|---|
| select | `?category=news` |
| checkbox | `?featured=1` (or `0`) |
| reference | `?author=<entry slug>` |
| checkbox_group | `?tags[]=a&tags[]=b`, or `?tags=a` |
| number | `?price_min=10&price_max=50` |

Sorting is `?sort=<title|created_at|popularity|field id>&direction=asc|desc`, and paging is `?page=N`.

Each item of `data_list.filters` is `{id, param, label, type, active_value, options}`:

- **Options:** each is `{label, value, url, active, count}`. `url` toggles that value and keeps the other parameters,
  so a theme never builds filter URLs by hand. A checkbox group option also has `only_url`.
- **Counts:** they respect the other active filters, and empty options are left out unless active.
- **Number filters:** `options` is `{type: "range", min, max}`, plus `min_value`, `max_value`, `form_action` and
  `form_fields` for a GET form.

## The `entry` object

`id`, `title`, `slug` (also `handle`), `url`, `published_at`, `created_at`, `updated_at`, `seo_title`,
`seo_description`, `template_suffix`, `data_list`, `referenced_by`. Each field is `entry.<field id>`; a built-in name
wins over a field with the same id unless the built-in is blank. `published_at` is the creation time; give the list a
`date` field for a publication date an editor controls.

| Field type | Print it with |
|---|---|
| text, select value, url | `{{ entry.x \| escape }}` (a url inside `href="…"`) |
| richtext, html, textarea | `{{ entry.x \| field_html: entry, 'x' }}`: raw for those types, escaped for any other |
| number, range | `{{ entry.x \| times: 1 }}` |
| date | `{{ entry.x \| date: '%B %d, %Y' }}` |
| image_picker | `{{ entry.x \| image_url: width: 1200 \| image_tag: width: entry.x.width, height: entry.x.height, widths: '400,800,1200', alt: entry.title }}` |
| video | `{{ entry.x \| media_tag }}` |
| video_url | `{{ entry.x \| external_video_tag }}` |
| select, radio, checkbox_group **labels** | `{{ entry.x \| option_label: entry, 'x' }}` (the stored value is the option's `value`) |
| reference, single | an entry object, or blank: `entry.author.url`, `entry.author.title` |
| reference, multiple | a list of entry objects: `{% for post in entry.related %}` |
| structure | a list of rows: `{% for row in entry.faq %}{{ row.question \| escape }}{% endfor %}` |

**Reverse references:** `entry.referenced_by['<list handle>']` lists the entries of another list that reference this
one, such as an author's posts.

- **On the entry's own page** it is a full list object, so use `.entries` and `{% paginate %}`.
- **Anywhere else**, inside a loop for example, it is a plain list of entries.

**Draw every field of any entry** without knowing the schema:
`{% for field in entry.data_list.fields %}…{% endfor %}`. Shipped themes do this in a `snippets/entry-field.liquid`;
reuse it where it exists.

## Section settings that point at content

| Setting type | Value in Liquid |
|---|---|
| `data_source` | a list object (paginated, as above) |
| `entry_picker` (with `"data_source": "<setting id>"`) | one entry, or blank when unpublished or deleted |
| `field_mapping` (with `"data_source"` and `"field_types"`) | a field id: read it with `entry[section.settings.x]` |
| `url` | a link; it takes `in1s://routes/<id>`, `in1s://routes/handle:<handle>`, `in1s://data-lists/<handle>`, `in1s://data-lists/<handle>/<slug>` and `in1s://data-lists/<handle>/id:<id>` |

## Forms and submissions

- **Rendering a form:** `{% assign handle = section.settings.form | default: 'contact' %}{% form handle, section-id: section.id %}…{% endform %}`.
  A tag argument takes no filters, so assign first. An unknown form renders nothing (a notice in the editor).
  Reuse the theme's `snippets/form-fields.liquid`.
- **The `form` object:** `handle`, `name`, `fields`, `submit_label`, `success_message`, `errors`,
  `posted_successfully?`, `submission`, `captcha_required?`, `captcha_script`, `session`.
- **Each field:** `id`, `type`, `label`, `name`, `value`, `error`, `options`, `required?`, `visible?`, `conditions`,
  `sub_fields`.
- **`form.session`** is what a visitor typed. It is hostile: `| escape` text, `| times: 1` numbers, and a link only
  through a `safe-relative-url` snippet. Few themes ship one, so check `snippets/`, and print no visitor-written link
  where it is missing.
- **Comments and reviews:** `{% assign comments = entry | submissions_for: 'comments', 200 %}` returns, oldest
  first, up to 200 submissions that point at this entry. Only the statuses and answers the form's `public_listing`
  allows are returned. A form without it returns nothing. The answers are visitor data: escape them.
- **Totals:** `{{ 'orders' | submissions_sum: 'amount' }}` adds a number answer over every submitted submission,
  whatever its status (drafts and trashed ones excluded).

## Search

- **The search page:** `/search?q=…&data_list=<handle>&page=N` renders `search.json`.
- **The `search` object:** `terms`, `performed`, `results` (entries), `results_count`, `current_page`,
  `total_pages`, `page_size` (12).
- **Paging and the form:** page with `{% paginate search.results by search.page_size %}`. The form's action is
  `{{ routes.search_url }}`.
- **Predictive search:** `GET {{ routes.predictive_search_url }}?q=…&limit=8&data_list=<handle>` answers
  `{"results": [{"title", "url", "image", "type"}]}` (`type` is the list's name). A query under 2 characters
  answers no results; the limit is at most 20, at 120 requests a minute per visitor.

## Example: a listing section with filters, sorting and paging

```liquid
<section class="section list-page" {{ section.in1s_attributes }}>
  <div class="page-width">
    <h1>{{ data_list.title | escape }}</h1>
    {%- for filter in data_list.filters -%}
      {%- unless filter.type == 'number' -%}
        <nav class="list-page__filter" aria-label="{{ filter.label | escape }}">
          {%- for option in filter.options -%}
            <a href="{{ option.url | escape }}"{% if option.active %} aria-current="true"{% endif %}>{{ option.label | escape }} ({{ option.count }})</a>
          {%- endfor -%}
        </nav>
      {%- endunless -%}
    {%- endfor -%}
    {%- paginate data_list.entries by data_list.page_size -%}
      <div class="list-page__grid">
        {%- for entry in data_list.entries -%}
          <article class="list-page__card">
            {%- if entry.featured_image != blank -%}
              {{ entry.featured_image | image_url: width: 800 | image_tag: width: entry.featured_image.width, height: entry.featured_image.height, widths: '400,600,800', loading: 'lazy', alt: entry.title }}
            {%- endif -%}
            <h2><a href="{{ entry.url | escape }}">{{ entry.title | escape }}</a></h2>
          </article>
        {%- else -%}
          <p>{{ 'sections.list-page.empty' | t }}</p>
        {%- endfor -%}
      </div>
      {%- if paginate.pages > 1 -%}{{ paginate | default_pagination }}{%- endif -%}
    {%- endpaginate -%}
  </div>
</section>

{% schema %}
{ "name": "t:sections.list-page.name", "settings": [] }
{% endschema %}
```

## Example: an entry section with an image, richtext, references, an option label and rows

```liquid
<article class="section entry-page" {{ section.in1s_attributes }}>
  <div class="page-width">
    <h1>{{ entry.title | escape }}</h1>
    <time datetime="{{ entry.created_at | date: '%Y-%m-%d' }}">{{ entry.created_at | date: '%B %d, %Y' }}</time>
    {%- if entry.category != blank -%}<span>{{ entry.category | option_label: entry, 'category' | escape }}</span>{%- endif -%}
    {%- if entry.featured_image != blank -%}
      {{ entry.featured_image | image_url: width: 1600 | image_tag: width: entry.featured_image.width, height: entry.featured_image.height, widths: '600,900,1200,1600', sizes: '100vw', alt: entry.title }}
    {%- endif -%}
    {%- assign author = entry.author_profile -%}
    {%- if author != blank -%}<a href="{{ author.url | escape }}">{{ author.title | escape }}</a>{%- endif -%}
    {%- if entry.content != blank -%}<div class="rte">{{ entry.content | field_html: entry, 'content' }}</div>{%- endif -%}
    {%- for row in entry.faq -%}
      <details><summary>{{ row.question | escape }}</summary>{{ row.answer | escape | newline_to_br }}</details>
    {%- endfor -%}
    {%- for post in entry.related_posts -%}<a href="{{ post.url | escape }}">{{ post.title | escape }}</a>{%- endfor -%}
    {%- if data_list.url != blank -%}<a href="{{ data_list.url | escape }}">{{ 'sections.entry-page.back' | t }}</a>{%- endif -%}
  </div>
</article>

{% schema %}
{ "name": "t:sections.entry-page.name", "settings": [] }
{% endschema %}
```

Both examples print no settings, so they need no `data-setting-id` markers. Add `sections.list-page.name` /
`sections.entry-page.name` to `locales/en.default.schema.json`, and `sections.list-page.empty` /
`sections.entry-page.back` to every storefront locale.
