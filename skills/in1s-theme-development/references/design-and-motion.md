# Design, motion and accessibility

For a redesign, a new theme, or a request such as "make it modern". The person's brand, the existing theme and any
references they give come first. Everything below is a default for when they do not decide.

## 1. Choose a direction before building

Read the site's type and profile (`get_settings` `websiteType`, `profileData`; they may be empty) and its content.
Then propose, in a few lines, and wait for the person's OK on a new site or a redesign:

- who visits, and the **one** main action (book, call, buy, download, sign up, enquire, donate, read);
- the mood, the type pairing, the colours, and the motion level (below).

Five questions work for any kind of site:

1. Who visits, and what must they decide or do?
2. What is the main action, and the second one?
3. What earns trust in this field (credentials, real work, reviews, licences, guarantees, press)?
4. What must a visitor know before acting (prices, hours, place, process, availability, requirements)?
5. How serious are the stakes? Health, money, law, children, safety and government call for a calmer design, less
   motion and stricter honesty.

What each kind usually needs:

| Kind | Leads with |
|---|---|
| App | One-line value, store badges, device screenshots, features, privacy and support links |
| SaaS, software, agency | A clear promise, product visuals, proof (logos, cases), pricing or process, demo or contact |
| Company, organisation | Who, what, proof, team, places, careers, contact |
| Local service | Services and area, hours, quote or booking request, click-to-call, map |
| Health | Calm and readable; booking, hours, place, specialties, credentials; an emergency notice; minimal motion |
| Portfolio | The work: large images, case studies, a filterable grid; a quiet interface |
| Restaurant, hospitality | Photos, menu, booking, hours, map |
| Shop, catalogue | Products with photos, prices and availability; categories; delivery and returns |
| Events | Date, place, programme, speakers, tickets or registration |
| Education | Programmes, schedule and fees, teachers, admissions |
| Legal, finance | Calm and precise; services, credentials, process, consultation request; no promised outcomes |
| Blog, media | Reading comfort (60–75 characters a line), categories, related posts |
| Government, public | Task-first navigation, plain language, documents, maximum accessibility |

If the site needs something the platform cannot do (online payment, a live booking calendar, member login), say so
and offer the honest nearest option: a form, an enquiry, a link to an outside service. Never fake it.

## 2. What modern sites share

- **Type leads.** One characterful family (or a pairing), a strong scale: large, tight headings (about 44–90px on
  desktop, line-height near 1, letter-spacing near −0.03em for Latin), body 17–20px in a softer colour, small labels
  for structure. Each script gets a font that covers it.
- **Restraint.** One accent colour used sparingly, generous space, one corner radius and one spacing scale, hairline
  dividers rather than heavy borders and shadows. One darker section can give rhythm.
- **Real content is the visual**: the work, the people, the place, the product, real numbers. A number shown large
  (a count, a year, a rating) must come from the person or their content.
- **The main action is always within reach**: the header button, repeated at the end of pages, click-to-call on
  phones for local businesses.
- **Each page tells a story**: a promise, proof, detail, answers to doubts, an action.

Section patterns to choose from, only where they fit: a hero with proof (a stat, rating, credential, badge); a
scrolling band of logos or services with faded edges; framed image cards; a bento grid; sticky stacking cards for a
process; a stats card; a statement that lights up as it scrolls; a filterable gallery; pricing cards; an FAQ; a
call-to-action panel; a large wordmark in the footer. Look in the theme for each before writing one.

## 3. Motion

Pick a level for the audience and keep to it:

| Level | For | What moves |
|---|---|---|
| Expressive | Apps, SaaS, agencies, portfolios | Everything below |
| Subtle | Companies, services, restaurants, NGOs | Blocks rising into view, hover states |
| Minimal | Health, legal, finance, government, blogs | Hover and focus states only |

Typical values: one easing everywhere (for example `cubic-bezier(.22,1,.36,1)`); blocks rise 24–40px and fade in over
about 0.8s, once, when they enter the screen; headings may reveal word by word (a small blur and rise, about 70–80ms
between words); a header may turn into a floating frosted bar after a little scrolling; buttons may roll their label
on hover; scrolling bands move about 40–60px a second and pause on hover. Count-up numbers only for real figures, and
never for years.

### Motion must never hide content

A section is shown with **no** animation in four situations: without JavaScript, in the theme editor, with
`prefers-reduced-motion: reduce`, and when printed. So never hide anything in plain CSS. Hide it only under a class
that a script adds after checking all of that:

```liquid
<script>
  (function () {
    var d = document.documentElement;
    if ({{ request.design_mode | json }} || !window.IntersectionObserver ||
        matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    d.classList.add('motion');
  })();
</script>
```

```css
.motion [data-reveal]:not(.is-in) { opacity: 0; transform: translateY(32px); }
[data-reveal] { transition: opacity .8s var(--ease), transform .8s var(--ease); }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; transition: none !important; } }
@media print { .motion [data-reveal] { opacity: 1 !important; transform: none !important; } }
```

Put the first script in the layout's `<head>` so the class is set before the first paint. The script that adds
`is-in` must also run on `in1s:section:load` and clean up on `in1s:section:unload`, or an edited section stays
invisible in the editor (`section_load_unhandled`). Use the theme's existing setup helper if it has one.

When a script splits a heading into words, keep the setting's `data-setting-id` on the element the setting prints
into, keep the words in order for screen readers (`aria-label` on the heading, or leave the text whole and animate a
clip), and do not split Arabic or other joined scripts into letters.

Smooth-scroll libraries change how wheel scrolling feels and how anchors jump. Use one only when the person wants that
feel, skip it for touch devices and reduced motion, and keep `scroll-padding-top` for a sticky header.

## 4. Accessibility (WCAG 2.2 AA)

- **Contrast**: 4.5:1 for body text, 3:1 for large text and for controls. Check text over photos and on the accent
  colour; a light accent such as lime needs dark text on it.
- **Focus**: a visible focus style on every link, button and field (`:focus-visible`), never removed.
- **The current page** is marked in every menu (`aria-current="page"`): the bar, the phone menu and the footer.
- **Images** have alt text that says what they show; purely decorative ones have empty alt.
- **Language**: `lang` and `dir` on `<html>`, and `lang` on a phrase in another language.
- **Headings** keep their real levels: one `<h1>` per page, then `<h2>`, `<h3>`. A shared heading snippet takes the
  level as a parameter.
- **Targets** at least 24×24px; the phone menu opens and closes with the keyboard and traps nothing.
- **Motion** respects reduced motion (above); nothing flashes more than three times a second.

## 5. Checking

`validate_theme` and `render_page` (every language), then look at the preview in a browser at about 1440 and 390
pixels and in each right-to-left language, scrolling the whole page. Report what you looked at, at which widths and
languages, and what you could not check.
