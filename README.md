# attelkom.net — the current Attelkom site

The working corporate site of **OJSC «Attelkom»**, Irad's largest telecom and ISP, meant for **attelkom.net**. (The deprecated late-90s site with the user pages lives in `mjsbroadbent/attelkom` and is meant for www.attelkom.net.)

In-world brief: Attelkom has no real competition, so the site is a mid-budget agency template from 2019 that nobody has cared about since — stock "theme v2.3" by "WebStudio Talas", a marquee notice strip, a cookie banner that never remembers you, a slider of over-shiny AI-generated news images with text baked in (like a lot of Central Asian telecom sites), lorem ipsum left in the FAQ, an unfinished mobile menu, a language switcher that leads to an under-construction page, a personal account login that always fails with a billing error, an "online consultant" that only ever puts you in a queue, and a "Restricted resources" page for blocked sites.

## Files
- `tools/build.py` builds every page (shared header/footer) — edit content there and run `python3 tools/build.py`.
- `css/style.css`, `js/main.js` — template styles and scripts.
- `img/logo.svg`, `img/logo-white.svg`, `img/favicon.svg` — made from the owner's logo SVG (`tools/attelkom_logo_original.svg`), recoloured.
- `img/*.jpg` — AI news/hero images (FLUX.1 Krea, owner's PC).
- Links to the subdomains ads.attelkom.net (Jarnama, repo mjsbroadbent/jarnama) and maps.attelkom.net (Kartalar, repo mjsbroadbent/kartalar). Ads come from [Attelkom Jarnama](https://github.com/mjsbroadbent/jarnama) (`serve.js`, theme `current local state`).

## Lore used
Founded 1994 (US defense contract), privatized 1999, HQ on Communications Square, Talas (2002); Director-General Samat Kasymov; .ir.ad zone 1996–2019 (lapsed; the site no longer offers it); GSM 1997, 3G 2010, 4G 2016; ~2.6 million mobile subscriptions; 1,800 km fibre backbone; data centre in Nurzhan; Attelkom Pay with Talasbank (SMS payments for herders); no service in the ATR; 2008 security directives and blocking; "technical works" during the 2023 protests. Prices are in som (8.40/USD).

## Hosting
Works from GitHub Pages at `/attelkom-new/` or from the root of attelkom.net. `build.py` also writes each page's description, canonical address and share tags (`DESCS` at the top), `sitemap.xml` and `robots.txt`; the login and language mock-ups are `noindex`. Served at attelkom.net (`CNAME`); www.attelkom.net is deliberately still the old site (repo attelkom).

## Logos

- `img/logo.svg`, `img/logo-white.svg`, `img/favicon.svg` — the original horse-and-globe emblem with the serif "ATTELKOM" wordmark. In-world it's still on letterheads, bills and shop signs; here it's the favicon.
- `img/logo-2019.svg`, `img/logo-2019-white.svg` — WebStudio Talas's 2019 "modernized" version used in the site header and footer: the old emblem crammed into a glossy app-icon tile, lowercase Poppins wordmark, Wi-Fi arcs over the "o", "Connecting Irad" tagline. Deliberately middling. Regenerate with `python3 tools/make_logo_2019.py`.
