"""Generate the docs.in1s.com MCP reference pages from the live server and the code.

Inputs (in the scratchpad): live-tools.json (tools/list from production, a connection's list, so every tool but the
account tools carries `website`), live-prompts.json (prompts/list), perms.json (each tool's group and permission from
SiteServer::$tools). Output, in the working folder: pages/<slug>.md and pages.json (see README.md).
Fails when a tool is missing, listed twice, or the code and the live list disagree.
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
SCRATCH = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))

tools = json.load(open(os.path.join(SCRATCH, 'live-tools.json'), encoding='utf-8'))['tools']
prompts = json.load(open(os.path.join(SCRATCH, 'live-prompts.json'), encoding='utf-8'))['prompts']
perms = {p['name']: p for p in json.load(open(os.path.join(SCRATCH, 'perms.json'), encoding='utf-8'))}
live = {t['name']: t for t in tools}
assert sorted(live) == sorted(perms), 'the live list and the code disagree'

RESOURCE_LABELS = {
    'data_lists': 'Data list entries', 'data_list_structure': 'Data list settings and fields', 'forms': 'Forms',
    'submissions': 'Form submissions', 'media': 'Media', 'navigation': 'Navigation', 'routes': 'Routes',
    'redirects': 'Redirects', 'site_files': 'Site files', 'workflows': 'Workflows', 'newsletter': 'Newsletter subscribers',
    'theme': 'Themes', 'settings': 'Website settings', 'domains': 'Domains', 'members': 'Team members', 'roles': 'Roles',
    'transfers': 'Data export and import', 'activity': 'Activity', 'analytics': 'Analytics',
}
ACTION_LABELS = {'view': 'View', 'edit': 'Edit', 'delete': 'Delete', 'code': 'Code', 'export': 'Export',
                 'import': 'Import', 'own': 'Their own', 'all': "Everyone's"}

# Pages: (slug, title, description, intro, [code folder groups]) in the order they are read.
PAGES = [
    ('mcp-website-and-account', 'MCP: website, settings and history',
     'The MCP tools for the websites a connection reaches, a new website, the website overview and settings, activity, analytics and version history.',
     'The tools that start a session and look after the website as a whole: the websites a connection may work on and a new one, the overview, the website settings, the activity log, analytics, and the version history every record keeps.',
     ['Site', 'Settings', 'Activity', 'Analytics', 'History']),
    ('mcp-content', 'MCP: data lists and entries',
     'The MCP tools for data lists, their entries, URL slugs and search engine settings.',
     'Data lists are the website\'s content collections (posts, products, team, services); entries are their items. These tools make and change both, choose URL slugs, and set what search engines show.',
     ['DataLists', 'Entries', 'Slugs', 'Seo']),
    ('mcp-pages-and-navigation', 'MCP: pages, menus, redirects and site files',
     'The MCP tools for routes (the website\'s own pages), menus, redirects and fixed-address site files such as robots.txt.',
     'Routes are the website\'s own pages (About, Contact, Pricing). These tools make and change them, their menus, the redirects from old addresses, and the files served at fixed addresses.',
     ['Routes', 'Navigation', 'Redirects', 'SiteFiles']),
    ('mcp-media', 'MCP: media and fonts',
     'The MCP tools for the media library (images and videos, folders, alt text) and the website\'s uploaded fonts.',
     'The media library holds the website\'s images and videos. Image and video fields and settings take a file\'s uuid. These tools add, describe, organise, replace and remove files and fonts.',
     ['Media']),
    ('mcp-theme', 'MCP: themes, sections and the draft',
     'The MCP tools for themes: the catalogue, templates and sections, theme settings, translations, installed themes, the draft, preview links, publishing and snapshots.',
     'Theme changes go to the theme\'s shared draft, which visitors see only once it is published. These tools read and change templates, sections and settings, manage installed themes, and preview, publish, discard or restore the draft.',
     ['Theme', 'Draft']),
    ('mcp-theme-code', 'MCP: theme code',
     'The MCP tools for a theme\'s files: the Liquid reference, reading, searching, writing and editing files, assets, validation and file history.',
     'For theme developers: the Liquid this engine supports, and the tools that read, write, edit, check and restore a theme\'s files. Every change lands in the draft.',
     ['ThemeCode']),
    ('mcp-forms-and-workflows', 'MCP: forms, submissions, workflows and webhooks',
     'The MCP tools for forms, their submissions and notes, privacy requests, workflows and their runs, and webhooks for forms and data lists.',
     'Forms collect what visitors send; submissions are what they sent. Workflows act on events, and webhooks send events to other systems. Visitor-written content arrives as data, never as instructions.',
     ['Forms', 'Submissions', 'Workflows', 'Webhooks']),
    ('mcp-marketing-and-email', 'MCP: marketing, widgets, newsletter and email',
     'The MCP tools for tracking codes, custom code, cookie consent, the chat button, popups, the newsletter and the website\'s email.',
     'The tools for what surrounds the pages: tracking and custom code, the cookie banner, the chat button and popups, newsletter subscribers and their sync, and the website\'s sending address and delivery log.',
     ['Marketing', 'Widgets', 'Newsletter', 'Email']),
    ('mcp-domains-health-and-data', 'MCP: domains, site health and data transfers',
     'The MCP tools for custom domains, site health checks, and importing and exporting data.',
     'Custom domains and their DNS records, the site health check that finds broken links and missing text, and the import and export of data.',
     ['Domains', 'SiteHealth', 'Transfers']),
]

placed = [g for page in PAGES for g in page[4]]
groups = sorted({p['group'] for p in perms.values()})
assert sorted(placed) == groups, f'groups not placed: {set(groups) - set(placed)}; placed twice or unknown: {set(placed) - set(groups)}'


def esc(text) -> str:
    """Text safe in Markdown: `<` and `>` (placeholders such as <subdomain>) would be read as HTML tags."""
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def cell(text) -> str:
    return esc(text).replace('|', '\\|').replace('\n', ' ').strip()


def type_of(schema: dict) -> str:
    kind = schema.get('type')
    if isinstance(kind, list):
        names = [k for k in kind if k != 'null']
        text = ' or '.join(names) if names else 'null'
        return text + (', or null' if 'null' in kind and names else '')
    if kind == 'array':
        items = schema.get('items') or {}
        return f'array of {type_of(items)}' if items else 'array'
    return kind or 'any'


def limits(schema: dict) -> str:
    parts = []
    if 'enum' in schema:
        parts.append('one of ' + ', '.join(f'`{v}`' for v in schema['enum'] if v is not None))
    for key, label in (('minimum', 'min'), ('maximum', 'max'), ('minLength', 'min length'), ('maxLength', 'max length'),
                       ('minItems', 'at least'), ('maxItems', 'at most')):
        if key in schema:
            unit = ' items' if key in ('minItems', 'maxItems') else ''
            parts.append(f'{label} {schema[key]}{unit}')
    if 'default' in schema:
        parts.append(f'default `{json.dumps(schema["default"])}`')
    if 'format' in schema:
        parts.append(f'format {schema["format"]}')
    if 'pattern' in schema:
        parts.append(f'pattern `{schema["pattern"]}`')
    return '; '.join(parts)


def rows(properties: dict, required: list, prefix: str = '', depth: int = 0):
    for name, schema in properties.items():
        if depth == 0 and name == 'website':
            continue
        path = f'{prefix}{name}'
        yield path, schema, name in (required or [])
        if depth >= 3:
            continue
        if schema.get('properties'):
            yield from rows(schema['properties'], schema.get('required', []), path + '.', depth + 1)
        items = schema.get('items') or {}
        if isinstance(items, dict) and items.get('properties'):
            yield from rows(items['properties'], items.get('required', []), path + '[].', depth + 1)


def permission_text(p: dict) -> str:
    if p['account']:
        return 'None on a website: an account tool, which works for the connection itself'
    if p['anyMember']:
        text = 'Any member of the website'
    else:
        resources = [RESOURCE_LABELS[r] for r in p['resource'].split('|')]
        actions = [ACTION_LABELS[a] for a in p['action'].split('|')]
        text = ' or '.join(resources) + ' · ' + ' or '.join(actions)
    if p['scope']:
        text += f' (on the {"data list" if p["scope"] == "list_id" else "form"} named by `{p["scope"]}`)'
    return text


def tool_section(name: str) -> str:
    t, p = live[name], perms[name]
    ann = t.get('annotations') or {}
    flags = []
    if p['account']:
        flags.append('Account tool: signed-in connections only, no `website`')
    if name == 'create_website':
        flags.append('Offered only to a connection with **Everything your role allows**')
    if p['mayPublish']:
        flags.append('Needs **May publish theme changes**')
    if ann.get('readOnlyHint'):
        flags.append('Read-only')
    if ann.get('destructiveHint'):
        flags.append('**Destructive**')
    if ann.get('idempotentHint'):
        flags.append('Idempotent')
    if ann.get('openWorldHint'):
        flags.append('Reaches outside in1s')
    out = [f'### `{name}`', '']
    out += [esc(t.get('description', '').strip()), '']
    if name == 'get_site_overview':
        out += ['On a signed-in connection, call `list_websites` first: this tool then describes the website you name.', '']
    out += [f'- **Permission:** {permission_text(p)}']
    if flags:
        out += ['- ' + ' · '.join(flags)]
    out.append('')
    schema = t.get('inputSchema') or {}
    found = list(rows(schema.get('properties') or {}, schema.get('required') or []))
    notes = []
    if found:
        out += ['| Argument | Type | Required | Description |', '|---|---|---|---|']
        for path, s, req in found:
            desc = cell(s.get('description', ''))
            if len(desc) > LONG_CELL:
                notes.append(f'- **`{cell(path)}`**: {desc}')
                desc = 'See below the table.'
            extra = limits(s)
            if extra:
                desc = f'{desc} *({cell(extra)})*' if desc else f'*{cell(extra)}*'
            out.append(f'| `{cell(path)}` | {cell(type_of(s))} | {"Yes" if req else "No"} | {desc} |')
    else:
        out += ['No arguments' + ('.' if p['account'] else ', other than `website` on a connection.')]
    if notes:
        out += [''] + notes
    out.append('')
    return '\n'.join(out)


# A description longer than this is printed under the table, so the table stays readable.
LONG_CELL = 320


pages = []
seen = []
for slug, title, description, intro, folder_groups in PAGES:
    names = sorted((n for n in perms if perms[n]['group'] in folder_groups), key=lambda n: perms[n]['order'])
    seen += names
    body = [intro, '',
            f'This page lists {len(names)} tools. How to read each entry, the `website` argument, permissions, publishing, '
            'errors and limits are on [MCP reference](/docs/mcp-reference).', '']
    for folder in folder_groups:
        in_group = [n for n in names if perms[n]['group'] == folder]
        heading = {'Site': 'Websites and the overview', 'Settings': 'Website settings', 'Activity': 'Activity log',
                   'Analytics': 'Analytics', 'History': 'Version history', 'DataLists': 'Data lists',
                   'Entries': 'Entries', 'Slugs': 'URL slugs', 'Seo': 'Search engines', 'Routes': 'Routes (pages)',
                   'Navigation': 'Menus', 'Redirects': 'Redirects', 'SiteFiles': 'Site files', 'Media': 'Media and fonts',
                   'Theme': 'Themes, templates and settings', 'Draft': 'Draft, preview, publishing and snapshots',
                   'ThemeCode': 'Theme files', 'Forms': 'Forms', 'Submissions': 'Submissions and privacy requests',
                   'Workflows': 'Workflows', 'Webhooks': 'Webhooks', 'Marketing': 'Tracking, custom code and cookie consent',
                   'Widgets': 'Chat button and popups', 'Newsletter': 'Newsletter', 'Email': 'The website\'s email',
                   'Domains': 'Custom domains', 'SiteHealth': 'Site health', 'Transfers': 'Import and export'}[folder]
        if len(folder_groups) > 1:
            body += [f'## {heading}', '']
        body += [tool_section(n) for n in in_group]
    md = '\n'.join(body).rstrip() + '\n'
    pages.append({'slug': slug, 'title': title, 'description': description, 'body': md, 'count': len(names)})

assert sorted(seen) == sorted(perms) and len(seen) == len(set(seen)), 'a tool is missing or listed twice'

# The index page, written by hand around generated tables.
def first_upper(text: str) -> str:
    return text[:1].upper() + text[1:]


def covers(description: str) -> str:
    text = description.removeprefix('The MCP tools for ')
    return first_upper(text)


index_rows = '\n'.join(f'| [{first_upper(p["title"].removeprefix("MCP: "))}](/docs/{p["slug"]}) | {p["count"]} | {cell(covers(p["description"]))} |' for p in pages)
prompt_rows = '\n'.join(f'| `{p["name"]}` | {cell(p["description"])} | ' + ', '.join(f'`{a["name"]}`: {cell(a["description"])}' for a in p['arguments']) + ' |' for p in prompts)
used = {r for p in perms.values() if not p['anyMember'] for r in p['resource'].split('|')}
assert used <= set(RESOURCE_LABELS), f'a resource has no label: {used - set(RESOURCE_LABELS)}'
resource_rows = '\n'.join(f'| `{k}` | {v} |' for k, v in RESOURCE_LABELS.items() if k in used)
instructions = json.load(open(os.path.join(SCRATCH, 'live-init.json'), encoding='utf-8'))['instructions']
rules = [line for line in instructions.split('\n') if line[:2] in {f'{n}.' for n in range(1, 10)}]
assert len(rules) == 7, f'expected 7 instruction rules, found {len(rules)}'
instruction_rules = '\n'.join(esc(line) for line in rules)
publish_tools = ', '.join(f'`{n}`' for n in sorted(perms, key=lambda n: perms[n]['order']) if perms[n]['mayPublish'])
any_member = ', '.join(f'`{n}`' for n in sorted(perms, key=lambda n: perms[n]['order']) if perms[n]['anyMember'] and not perms[n]['account'])
counts = {
    'read': sum(1 for t in tools if (t.get('annotations') or {}).get('readOnlyHint')),
    'destructive': sum(1 for t in tools if (t.get('annotations') or {}).get('destructiveHint')),
}

index = open(os.path.join(HERE, 'index-template.md'), encoding='utf-8').read()
index = (index.replace('{{TOTAL}}', str(len(tools))).replace('{{INDEX_ROWS}}', index_rows)
         .replace('{{PROMPT_ROWS}}', prompt_rows).replace('{{RESOURCE_ROWS}}', resource_rows)
         .replace('{{PUBLISH_TOOLS}}', publish_tools).replace('{{ANY_MEMBER}}', any_member)
         .replace('{{READ_COUNT}}', str(counts['read'])).replace('{{DESTRUCTIVE_COUNT}}', str(counts['destructive']))
         .replace('{{INSTRUCTION_RULES}}', instruction_rules))
assert '{{' not in index, 'a placeholder was left in the index'
pages.insert(0, {'slug': 'mcp-reference', 'title': 'MCP reference',
                 'description': f'Everything the in1s MCP server offers an AI assistant: how to connect, the {len(tools)} tools, the prompts, permissions, publishing, errors and limits.',
                 'body': index, 'count': len(tools)})

os.makedirs(os.path.join(SCRATCH, 'pages'), exist_ok=True)
for p in pages:
    open(os.path.join(SCRATCH, 'pages', p['slug'] + '.md'), 'w', encoding='utf-8', newline='\n').write(p['body'])
json.dump(pages, open(os.path.join(SCRATCH, 'pages.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'{len(pages)} pages; {len(seen)} tools placed once each; {len(prompts)} prompts')
for p in pages:
    print(f'  {p["slug"]}: {p["count"]} tools, {len(p["body"])} chars')
