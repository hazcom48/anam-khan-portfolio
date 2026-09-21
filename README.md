# Anam Khan — journalist portfolio

A portable static website with four content pages, 130 reporting records (76 original, 54 additional publisher-verified articles), two demo reels, and a custom 404 page. All biography and reporting content is based on https://anamaylakhan.com/, retrieved September 21, 2026. Contact address confirmed by the user: anamlaylakhan@gmail.com.

## Build and preview

Run `python3 build.py`, then `python3 verify.py`. Serve `dist` with any static web server. No package installation or application framework is needed.

`SITE_ORIGIN` controls canonical URLs, structured-data IDs and the sitemap. The default is the intended public address, https://anam.josta.club. This domain is not yet connected. When moving the site to the original domain, rebuild with `SITE_ORIGIN=https://anamaylakhan.com python3 build.py` and revalidate before publishing.

The existing public website and its DNS have not been modified. The Sites copy is private by default. Search engines cannot index an owner-private site. Public-domain rollout, Search Console verification, sitemap submission and indexing checks remain separate launch steps.

## Content and SEO

- Four unique page titles, descriptions and self-referencing canonical URLs.
- All primary copy and all 130 stories are delivered as HTML, without requiring JavaScript.
- One H1 per page, descriptive section headings, semantic landmarks, focus styles and a skip link.
- Person, WebSite, ProfilePage, CollectionPage and ContactPage structured data, without invented credentials, employment claims or awards.
- Sitemap and robots.txt; index.html redirect declaration; canonical root linking.
- Original article destinations preserved; local copies of all 37 story thumbnails, the supplied portrait, and 14 available radio clips.
- Broadcast videos load only when a visitor opens a report. Links to the original YouTube pages work without JavaScript.
- Social title and description metadata included. No bespoke social-sharing image was requested or generated.
- Generated artwork is decorative and is not represented as documentary reporting photography.

## Source-media limitations

Six radio URLs on the original website return HTTP 404. Their titles and descriptions are retained, but no broken players are shown:

- Nick Nurse and student musicians (`radio/nurse.mp3`)
- Greenbelt reversal (`radio/greenbelt.mp3`)
- Louis March (`radio/louismarch.mp3`)
- Toronto Island arborist (`radio/tyler.mp3`)
- Air quality warnings (`radio/airquality.mp3`)
- Peter Cripps and East York fastpitch (`radio/baseball.mp3`)

Replace these recordings when the original files become available, update `source-content/asset-report.json`, and rebuild. Third-party publishers and YouTube control availability of external stories and videos. No search-ranking, traffic or Core Web Vitals result is claimed.

## Visual direction

The latest direction is inspired by Suleika Jaouad’s site: blush-pink navigation, deep-blue serif type, spacious editorial sections and a watercolour portrait against a blue-grey background. Earlier references were Steph Spector, Joshua Davis and Donald Boström. Original photographs are preserved. Generated artwork prompts are recorded in `source-content/watercolour-provenance.md` and `source-content/art-provenance.md`.

## Added reporting

54 additional articles were verified on BNN Bloomberg’s official Anam Khan author archive and on each linked article page. Visible publication dates are used; the publisher’s metadata dates sometimes differ. Details and verification dates are retained in `source-content/additional-articles.json`. This is a verified addition set, not a claim that every article she has ever published has been found.


## Deployment

Publish the `dist` folder using a static host such as Netlify or Cloudflare Pages. Optional build command: `python3 build.py`. Validate with `python3 verify.py`. The Sites hosting configuration is retained for reference; Sites publication has not succeeded. This repository alone does not activate website hosting or DNS.
