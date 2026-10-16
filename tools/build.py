#!/usr/bin/env python3
"""Builds the static Attelkom site (attelkom.net) from the page bodies below.

    python3 tools/build.py

Every page shares the same header, notice strip, footer, chat widget and cookie banner.
Pages in subfolders get a relative prefix so the site works both at attelkom.net/ and
at a GitHub Pages project path.
"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAV = [("internet.html", "Home Internet"), ("mobile.html", "Mobile"), ("business.html", "Business"),
       ("pay.html", "Attelkom Pay"), ("news/index.html", "News"), ("about.html", "About")]

NOTICE = ("Dear subscribers! Planned technical works on the Talas–Nurzhan backbone on the night of 18 October from 01:00 to 05:00. "
          "Short interruptions of service are possible. We apologise for the inconvenience. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
          "New tariff «Burkut 100» — now in central Talas! &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
          "Pay for Attelkom services by SMS with Attelkom Pay — send PAY to 5050.")

SITE = "https://attelkom.net/"
# One description per page for search results and link previews (news pages use their first paragraph).
DESCS = {
    "index.html": "Attelkom, Irad's largest internet and mobile operator: home internet, 4G mobile, Attelkom Pay and business services in Talas, Nurzhan and Iyık Janyl.",
    "internet.html": "Attelkom home internet tariffs: fibre and ADSL plans for Talas, Nurzhan and Iyık Janyl, with prices in som and free installation offers.",
    "mobile.html": "Attelkom mobile tariffs: 4G/LTE plans, prepaid packages and USIM replacement. Coverage across the ISEZ district centres.",
    "business.html": "Attelkom for business: dedicated internet channels, corporate mobile plans, data centre hosting in Nurzhan and solutions for state organisations.",
    "pay.html": "Attelkom Pay: pay for mobile, utilities, veterinary services and more from your phone balance by SMS to 5050, together with Talasbank.",
    "coverage.html": "Attelkom coverage map: where 2G, 3G and 4G/LTE mobile service and home internet are available in the Irad Special Economic Zone.",
    "about.html": "About OJSC Attelkom: founded in 1994, Irad's national telecom operator, with its head office on Communications Square in Talas.",
    "support.html": "Attelkom help: service centres in Talas, Nurzhan and Iyık Janyl, the 105 hotline, frequently asked questions and how to pay.",
    "blocked.html": "Restricted resources: information on websites restricted in the Irad Special Economic Zone under the 2008 security directives.",
    "docs.html": "Attelkom documents: public offer, privacy policy, tariff regulations and licences of OJSC Attelkom.",
    "news/index.html": "Attelkom news: network expansion, tariff changes, technical works and new services from Irad's national operator.",
}
NOINDEX = {"login.html", "lang/index.html", "404.html"}   # mock-ups and the error page stay out of search
PAGES = []

def page(path, title, body, active=None, desc=None, base=False, img="img/hero_tower.jpg"):
    desc = desc or DESCS.get(path, "Attelkom, Irad's largest internet and mobile operator.")
    url = SITE + (path[:-10] if path.endswith("index.html") else path)
    if path not in NOINDEX: PAGES.append(url)
    full_title = f"{title} | ATTELKOM"
    seo = (f'<link rel="canonical" href="{url}">\n'
           + ('<meta name="robots" content="noindex">\n' if path in NOINDEX else '')
           + f'<meta property="og:type" content="{"article" if path.startswith("news/") and path != "news/index.html" else "website"}">\n'
           f'<meta property="og:site_name" content="Attelkom">\n'
           f'<meta property="og:title" content="{html.escape(full_title)}">\n'
           f'<meta property="og:description" content="{html.escape(desc)}">\n'
           f'<meta property="og:url" content="{url}">\n'
           f'<meta property="og:image" content="{SITE}{img}">\n'
           f'<meta name="twitter:card" content="summary_large_image">\n')
    depth = path.count("/")
    p = "../" * depth
    nav = "".join(f'<a href="{p}{h}"{" class=\"on\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
{BASE if base else ""}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | ATTELKOM</title>
<meta name="description" content="{html.escape(desc)}">
{seo}<meta name="keywords" content="attelkom, internet, irad, talas, nurzhan, 4g, lte, provider, mobile, tariffs, интернет, провайдер">
<link rel="icon" href="{p}img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{p}css/style.css?v=2.3.8">
</head>
<body>
<div class="topbar"><div class="wrap">
  <span>Hotline: <span class="hot">105</span> (free from Attelkom numbers) &nbsp;|&nbsp; +996 39 312 10 50</span>
  <span><a href="https://maps.attelkom.net/">Attelkom Maps</a><a href="https://ads.attelkom.net/">Advertising</a><a href="{p}coverage.html">Coverage map</a><a href="{p}support.html">Service centres</a><a href="{p}support.html">Help</a></span>
</div></div>
<header class="main"><div class="wrap">
  <a class="logo" href="{p}index.html"><img src="{p}img/logo-2019.svg" alt="attelkom — Connecting Irad"></a>
  <nav class="menu">{nav}</nav>
  <div class="langs"><a class="on" href="#">EN</a>|<a href="{p}lang/index.html">IRD</a>|<a href="{p}lang/index.html">РУС</a></div>
  <a class="btn-login" href="{p}login.html">&#128100; Personal account</a>
  <button class="burger" aria-label="Menu">&#9776;</button>
</div></header>
<div class="notice"><marquee scrollamount="4">{NOTICE}</marquee></div>
{body.replace("{p}", p)}
<footer class="main"><div class="wrap">
  <div class="cols">
    <div>
      <img class="logo-f" src="{p}img/logo-2019-white.svg" alt="attelkom">
      <p>OJSC «Attelkom» is the leading provider of telecommunication services in Irad since 1994. Fibre, 4G/LTE, satellite, hosting and data centre services for citizens, business and the state.</p>
      <div class="soc"><a href="#" title="Tulpar">T</a><a href="#" title="Facebook">f</a><a href="#" title="Instagram">in</a><a href="#" title="YouTube">&#9654;</a></div>
    </div>
    <div><h4>For you</h4><a href="{p}internet.html">Home Internet</a><a href="{p}mobile.html">Mobile tariffs</a><a href="{p}pay.html">Attelkom Pay</a><a href="{p}coverage.html">Coverage</a><a href="{p}login.html">Personal account</a></div>
    <div><h4>Company</h4><a href="{p}about.html">About Attelkom</a><a href="{p}news/index.html">News</a><a href="{p}about.html#tenders">Tenders</a><a href="{p}about.html#jobs">Vacancies</a><a href="https://ads.attelkom.net/">Attelkom Jarnama (advertising)</a><a href="https://maps.attelkom.net/">Attelkom Maps</a></div>
    <div><h4>Useful links</h4><a href="{p}support.html">Service centres</a><a href="{p}support.html#faq">FAQ</a><a href="{p}docs.html">Public offer</a><a href="{p}docs.html">Privacy policy</a><a href="{p}blocked.html">Restricted resources</a></div>
  </div>
  <div class="bottom"><span>© 2019–2024 OJSC «Attelkom». All rights reserved. Licence of the Communications Regulator No. 0014/08.</span><span>Site by WebStudio Talas</span></div>
</div></footer>
<button class="chat" title="Online consultant">&#128172;</button>
<div class="chatbox"><div class="h">Online consultant</div><div class="b"><div class="msg">Hello! How can we help you?</div></div><input placeholder="Type your message..."></div>
<div class="cookies">This site uses cookies to improve your experience. By continuing to use the site you agree to our cookie policy. <button>OK</button></div>
<div style="display:none">counter</div>
<script src="{p}js/main.js"></script>
<script src="https://ads.attelkom.net/serve.js" data-theme="current local state" defer></script>
</body>
</html>
"""
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(out)

BASE = """<script>document.write('<base href="' + (location.pathname.indexOf('/attelkom-new/') === 0 ? '/attelkom-new/' : '/') + '">');</script>
"""

def head(title, crumbs):
    c = ' / '.join(f'<a href="{{p}}{h}">{t}</a>' for h, t in crumbs)
    return f'<div class="pagehead"><div class="wrap"><div class="crumbs"><a href="{{p}}index.html">Main</a> / {c}</div><h1>{title}</h1></div></div>'

# ---------------------------------------------------------------- news
NEWS = [
 ("international-exchange", "18.08.2026", "Attelkom connects to one of the largest internet traffic exchange points in the region",
  "img/hero_backbone.jpg",
  """<p>OJSC «Attelkom» informs that on 15 August 2026 the company completed the connection of its international gateway to a major regional internet traffic exchange platform via the northern fibre route through Kazakhstan.</p>
<p>The connection allows Attelkom to exchange traffic directly with the largest content providers, search engines, video platforms and cloud services, without passing through intermediate operators. As a result, subscribers will notice a faster loading of popular resources and a lower delay (ping) for online services.</p>
<p>«This is an important step in the development of the digital infrastructure of Irad,» said the Director-General of Attelkom Samat Kasymov. «Our task is to provide every family and every business with fast, reliable and affordable internet.»</p>
<p>The project was implemented within the framework of the Programme for the Development of Telecommunications 2024–2028. Total capacity of the new channel is 100 Gbit/s with possibility of expansion.</p>
<p>All traffic is processed in accordance with the legislation of the Irad Special Economic Zone.</p>"""),
 ("4g-kara-buura", "02.10.2026", "4G/LTE network now available in all district centres of Kara-Buura",
  "img/hero_4g.jpg",
  """<p>Attelkom continues the expansion of its 4G/LTE network. From 1 October, high-speed mobile internet is available in all district centres of Kara-Buura District, including Kyzyl-Adyr and Aulie-Ata.</p>
<p>To use 4G, a subscriber needs a 4G-compatible phone and a USIM card. Old SIM cards can be replaced free of charge at any Attelkom service centre on presentation of a passport.</p>
<p>In 2027 the company plans to extend 4G coverage along the Trans-Talas Highway.</p>"""),
 ("technical-works", "11.09.2026", "On technical works in the central district of Talas",
  "img/hero_tower.jpg",
  """<p>Dear subscribers!</p>
<p>In connection with technical works on the network equipment, on 11–12 September interruptions in the operation of mobile internet in the central district of Talas were possible. Voice services and SMS operated normally.</p>
<p>At present all services have been fully restored. Attelkom apologises to subscribers for the temporary inconvenience.</p>
<p>The company reminds that the works were carried out in accordance with the requirements of the regulator.</p>"""),
 ("attelkom-pay-vet", "01.09.2026", "Attelkom Pay: now you can pay for veterinary services by SMS",
  "img/hero_pay.jpg",
  """<p>Together with Talasbank, Attelkom has added veterinary services to the list of payments available through Attelkom Pay. Herders and farmers can now pay licensed veterinarians and feed suppliers directly from their mobile balance, without travelling to a bank branch.</p>
<p>To pay, send an SMS with the text <b>VET [code of the vet] [amount]</b> to the short number <b>5050</b>. The commission is 2.5% (minimum 10 som).</p>
<p>The service works in all areas of Attelkom coverage.</p>"""),
 ("attelkom-park", "20.07.2026", "Attelkom Park stadium receives new lighting and free Wi-Fi",
  "img/hq.jpg",
  """<p>At Attelkom Park, the home stadium of FC Attelkom Talas, the installation of new LED floodlights and a public Wi-Fi network was completed before the second half of the season.</p>
<p>Spectators can connect to the network «Attelkom_Park_FREE» and use the internet free of charge for 30 minutes after authorisation by SMS.</p>
<p>Attelkom wishes the team successful games!</p>"""),
 ("tariffs-april", "12.03.2026", "On changes of tariffs from 1 April 2026",
  "img/hero_backbone.jpg",
  """<p>In connection with the growth of costs for international channels and equipment, and to further improve the quality of services, from 1 April 2026 the cost of some tariff plans for home internet and mobile communication will be changed.</p>
<p>Detailed information on new prices is available in the section <a href="../internet.html">Home Internet</a> and at service centres. Subscribers on archive tariffs will be transferred to the nearest current tariff automatically.</p>
<p>Attelkom thanks you for your understanding and for choosing us.</p>"""),
]

def news_card(slug, date, title, img, body, p="{p}"):
    first = body.split("</p>")[0].replace("<p>", "")
    import re
    first = re.sub("<[^>]+>", "", first)
    if len(first) > 120: first = first[:117].rsplit(" ", 1)[0] + "..."
    return f'''<div class="card"><a href="{p}news/{slug}.html"><img src="{p}{img}" alt=""></a><div class="in"><div class="d">{date}</div><a href="{p}news/{slug}.html"><h3>{title}</h3></a><p>{first}</p></div></div>'''

def lead_text(body, n=158):
    import re
    t = re.sub("<[^>]+>", "", body.split("</p>")[0]).strip()
    if t.startswith("Dear subscribers") and "</p>" in body: t = re.sub("<[^>]+>", "", body.split("</p>")[1]).strip()
    return t if len(t) <= n else t[:n - 1].rsplit(" ", 1)[0] + "…"

for slug, date, title, img, body in NEWS:
    page(f"news/{slug}.html", title, desc=lead_text(body), img=img, body=f'''
{head("News", [("news/index.html", "News")])}
<div class="wrap"><div class="content article">
<img class="hero-img" src="{{p}}{img}" alt="">
<h1 style="font-size:26px;margin:20px 0 4px">{title}</h1>
<div class="meta">{date} &nbsp;·&nbsp; Press service of OJSC «Attelkom»</div>
{body}
<div class="share">Share: <a href="#">Tulpar</a><a href="#">Facebook</a><a href="#">WhatsApp</a><a href="#">Telegram</a></div>
<p style="margin-top:20px"><a href="{{p}}news/index.html">&larr; Back to news</a></p>
</div></div>''', active="news/index.html")

page("news/index.html", "News", f'''
{head("News", [("news/index.html", "News")])}
<div class="wrap" style="padding:30px 15px 46px">
<div class="cards">{"".join(news_card(*n) for n in NEWS)}</div>
<p style="text-align:center;margin-top:26px"><a class="btn" href="#">Load more</a></p>
</div>''', active="news/index.html")

# ---------------------------------------------------------------- home
slides = [
 ("img/hero_backbone.jpg", "18.08.2026", "Attelkom connects to one of the largest internet traffic exchange points in the region", "news/international-exchange.html"),
 ("img/hero_4g.jpg", "02.10.2026", "4G/LTE now in all district centres of Kara-Buura", "news/4g-kara-buura.html"),
 ("img/hero_pay.jpg", "", "Attelkom Pay — pay for anything from your phone, even on the jailoo", "pay.html"),
 ("img/hero_tower.jpg", "", "Burkut 100 — the fastest home internet in Irad*", "internet.html"),
]
slides_html = "".join(f'''<div class="slide{" on" if i == 0 else ""}"><img src="{{p}}{s[0]}" alt=""><div class="cap"><div class="date">{s[1]}</div><h1>{s[2]}</h1><a class="more" href="{{p}}{s[3]}">Learn more</a></div></div>''' for i, s in enumerate(slides))

PLANS = [
 ("Dala", "10", "1 150", ["Unlimited traffic*", "Wi-Fi router for rent — 90 som/month", "Connection: 1 500 som"], False),
 ("Kök", "25", "1 890", ["Unlimited traffic*", "Wi-Fi router for rent — 90 som/month", "IPTV «Basic» (40 channels)"], True),
 ("Burkut", "50", "3 200", ["Unlimited traffic*", "Wi-Fi router included", "IPTV «Basic» (40 channels)", "Static IP — 300 som"], False),
 ("Burkut 100", "100", "5 400", ["Unlimited traffic*", "Wi-Fi router included", "IPTV «Extended» (85 channels)", "Only in central Talas"], False),
]
def plans_html():
    out = ""
    for nm, sp, pr, feats, hit in PLANS:
        li = "".join(f"<li>{f}</li>" for f in feats)
        out += f'''<div class="plan{" hit" if hit else ""}">{'<div class="badge">Popular</div>' if hit else ""}<div class="nm">{nm}</div><div class="sp">{sp} <small>Mbit/s</small></div><div class="pr">{pr} <small>som/month</small></div><ul>{li}</ul><a class="btn" href="{{p}}login.html">Connect</a></div>'''
    return out

page("index.html", "Main", f'''
<div class="promo-pop" id="promopop"><div class="pp">
  <button class="pp-x" aria-label="Close">&times;</button>
  <img src="{{p}}img/hero_4g.jpg" alt="">
  <div class="pp-in">
    <div class="pp-tag">Only until 31 October!</div>
    <h3>Switch to «Joguru» and get <span>+20 GB</span> for FREE!*</h3>
    <p>Connect the tariff «Joguru» and receive an additional 20 GB of 4G internet every month for the first 3 months. Hurry, the offer is limited!</p>
    <div class="pp-timer">Offer ends in: <b id="pptimer">00:14:59</b></div>
    <a class="btn o pp-go" href="{{p}}mobile.html">CONNECT NOW</a>
    <label class="pp-no"><input type="checkbox"> Do not show again</label>
    <div class="pp-fine">* Bonus gigabytes are valid in the home region only, from 01:00 to 07:00. Connection of the tariff is paid (150 som). The offer does not apply to subscribers who used other promotions in 2026.</div>
  </div>
</div></div>
<div class="hero">{slides_html}<button class="arrow prev">&#8249;</button><button class="arrow next">&#8250;</button><div class="dots"></div></div>
<div class="wrap">
  <div class="tiles">
    <a class="tile" href="{{p}}internet.html"><span class="ic">&#127968;</span><b>Home Internet</b>Fibre and ADSL up to 100 Mbit/s</a>
    <a class="tile" href="{{p}}mobile.html"><span class="ic">&#128241;</span><b>Mobile</b>4G/LTE in all three cities</a>
    <a class="tile" href="{{p}}pay.html"><span class="ic">&#128176;</span><b>Attelkom Pay</b>Payments by SMS — 5050</a>
    <a class="tile" href="{{p}}login.html"><span class="ic">&#128179;</span><b>Top up balance</b>Online, by card or in terminals</a>
  </div>
</div>
<section class="block"><div class="wrap">
  <h2>News</h2>
  <div class="cards">{"".join(news_card(*n) for n in NEWS[:3])}</div>
  <p style="text-align:right;margin-top:14px"><a href="{{p}}news/index.html">All news &raquo;</a></p>
</div></section>
<section class="block white"><div class="wrap">
  <h2>Home internet tariffs</h2>
  <div class="plans">{plans_html()}</div>
  <p class="fine">* Unlimited traffic is subject to the Fair Use Policy. After 300 GB per month the speed may be reduced to 2 Mbit/s until the end of the billing period. Prices include VAT. Tariffs valid from 01.04.2026.</p>
</div></section>
<section class="block"><div class="wrap">
  <div class="promo"><img src="{{p}}img/hero_pay.jpg" alt=""><div class="tx"><h2>Attelkom Pay</h2>
  <p>Pay for mobile, internet, utilities, feed and veterinary services directly from your mobile balance. Send money to relatives in any city of Irad. No bank card needed!</p>
  <p><b>Send PAY to 5050</b> to register.</p><a class="btn o" href="{{p}}pay.html">More details</a></div></div>
</div></section>
<div class="wrap adrow"><div class="jarnama" data-size="728x90"></div></div>
<section class="block"><div class="wrap">
  <h2>Why Attelkom?</h2>
  <div class="cards">
    <div class="card"><div class="in"><h3>&#127760; Largest network</h3><p>1 800 km of fibre backbone and more than 600 base stations across the ISEZ.</p></div></div>
    <div class="card"><div class="in"><h3>&#128737; Reliability</h3><p>Our own data centre in Nurzhan and three independent international channels.</p></div></div>
    <div class="card"><div class="in"><h3>&#128506; Attelkom Maps</h3><p>Maps and directions for every city and road of Irad at <a href="https://maps.attelkom.net/">maps.attelkom.net</a>.</p></div></div>
    <div class="card"><div class="in"><h3>&#128226; Advertise with us</h3><p>Banner advertising on the leading sites of Irad with <a href="https://ads.attelkom.net/">Attelkom Jarnama</a>.</p></div></div>
    <div class="card"><div class="in"><h3>&#128222; Support 24/7</h3><p>Call 105 or visit one of our 46 service centres. Online consultant on the site.</p></div></div>
  </div>
</div></section>
''', desc="Attelkom — Irad's #1 ISP. Home internet, 4G mobile, Attelkom Pay and business solutions in Talas, Nurzhan and Iyık Janyl.")

# ---------------------------------------------------------------- internet
page("internet.html", "Home Internet", f'''
{head("Home Internet", [("internet.html", "Home Internet")])}
<section class="block"><div class="wrap">
  <h2>Tariffs for fibre (GPON)</h2>
  <div class="plans">{plans_html()}</div>
  <p class="fine">* Unlimited traffic is subject to the Fair Use Policy. After 300 GB per month the speed may be reduced to 2 Mbit/s until the end of the billing period. The speed is indicated as «up to» and is not guaranteed. «Burkut 100» is available only in the central district of Talas. Prices include VAT.</p>
</div></section>
<div class="wrap"><div class="content">
  <h2>ADSL tariffs</h2>
  <p>For subscribers in buildings without fibre. ADSL speed depends on the length and condition of the telephone line.</p>
  <table class="t"><tr><th>Tariff</th><th>Speed</th><th>Price, som/month</th><th>Traffic</th></tr>
  <tr><td>ADSL Start</td><td>up to 2 Mbit/s</td><td>690</td><td>Unlimited</td></tr>
  <tr><td>ADSL Optimal</td><td>up to 6 Mbit/s</td><td>990</td><td>Unlimited</td></tr>
  <tr><td>ADSL Maximum</td><td>up to 12 Mbit/s</td><td>1 390</td><td>Unlimited*</td></tr></table>
  <h2 style="margin-top:30px">How to connect</h2>
  <ol><li>Check the possibility of connection at your address on the <a href="{{p}}coverage.html">coverage page</a> or by calling 105.</li>
  <li>Come to a service centre with your passport and a document confirming your address (or the owner's permission).</li>
  <li>Sign the contract and pay for the connection.</li><li>Our technician will visit you within 3–14 working days.</li></ol>
  <p class="fine">Archive tariffs «Internet 512», «Internet 1024» and «Family» are no longer available for new connections.</p>
</div></div>''', active="internet.html")

# ---------------------------------------------------------------- mobile
page("mobile.html", "Mobile", f'''
{head("Mobile", [("mobile.html", "Mobile")])}
<section class="block"><div class="wrap">
  <h2>Prepaid tariffs</h2>
  <div class="plans">
    <div class="plan"><div class="nm">Salam</div><div class="sp">5 <small>GB</small></div><div class="pr">290 <small>som/month</small></div><ul><li>100 minutes in network</li><li>50 SMS</li><li>Tulpar messenger without traffic</li></ul><a class="btn" href="{{p}}support.html">Buy SIM</a></div>
    <div class="plan hit"><div class="badge">Popular</div><div class="nm">Jakshı</div><div class="sp">15 <small>GB</small></div><div class="pr">490 <small>som/month</small></div><ul><li>Unlimited calls in network</li><li>150 minutes to other operators</li><li>Tulpar messenger without traffic</li></ul><a class="btn" href="{{p}}support.html">Buy SIM</a></div>
    <div class="plan"><div class="nm">Joguru</div><div class="sp">40 <small>GB</small></div><div class="pr">890 <small>som/month</small></div><ul><li>Unlimited calls in network</li><li>400 minutes to other operators</li><li>Night internet free (01:00–07:00)</li></ul><a class="btn" href="{{p}}support.html">Buy SIM</a></div>
    <div class="plan"><div class="nm">Jailoo</div><div class="sp">2 <small>GB</small></div><div class="pr">150 <small>som/month</small></div><ul><li>For herders and seasonal workers</li><li>Attelkom Pay without commission</li><li>Works on 2G/3G</li></ul><a class="btn" href="{{p}}support.html">Buy SIM</a></div>
  </div>
  <p class="fine">Prices include VAT. Unused minutes and gigabytes do not carry over to the next month. Roaming in Kazakhstan, Kyrgyzstan and Uzbekistan — see the <a href="{{p}}docs.html">full list of prices</a>. The «Tulpar messenger without traffic» option does not include voice and video calls.</p>
</div></section>
<div class="wrap"><div class="content">
  <h2>USSD commands</h2>
  <table class="t"><tr><th>Command</th><th>Action</th></tr>
  <tr><td>*100#</td><td>Check balance</td></tr><tr><td>*102#</td><td>Remaining minutes and traffic</td></tr>
  <tr><td>*110*code#</td><td>Top up with a scratch card</td></tr><tr><td>*505#</td><td>Attelkom Pay menu</td></tr>
  <tr><td>*111#</td><td>Change tariff</td></tr><tr><td>*121#</td><td>«Call me back» request (free)</td></tr></table>
</div></div>''', active="mobile.html")

# ---------------------------------------------------------------- business
page("business.html", "Business", f'''
{head("For business", [("business.html", "Business")])}
<div class="wrap"><div class="content">
  <img src="{{p}}img/hq.jpg" alt="" style="width:100%;display:block;margin-bottom:20px">
  <h2>Solutions for business and the state</h2>
  <p>Attelkom offers a full range of telecommunication services for enterprises, banks and state organisations of Irad.</p>
  <table class="t"><tr><th>Service</th><th>Description</th></tr>
  <tr><td>Dedicated internet access</td><td>Symmetric channels from 10 Mbit/s to 10 Gbit/s with SLA</td></tr>
  <tr><td>VPN / L2 channels</td><td>Connection of branches in Talas, Nurzhan, Iyık Janyl and district centres</td></tr>
  <tr><td>Data centre (colocation)</td><td>Racks and units in the Attelkom Data Center, Nurzhan. Tier III*. Diesel backup.</td></tr>
  <tr><td>Hosting and domains</td><td>Registration of <b>.com</b>, <b>.net</b> and <b>.org</b> domains, virtual hosting, VPS</td></tr>
  <tr><td>Microwave and satellite</td><td>Connection of remote industrial sites, mines and border posts</td></tr>
  <tr><td>Corporate mobile</td><td>Group tariffs from 10 SIM cards, single invoice</td></tr>
  <tr><td>Advertising</td><td>Banner advertising on the <a href="https://ads.attelkom.net/">Attelkom Jarnama</a> network (ads.attelkom.net)</td></tr></table>
  <p class="fine">* Certification in process.</p>
  <p>For commercial offers please write to <b>b2b@attelkom.net</b> or call +996 39 312 10 77 (working days 9:00–18:00).</p>
</div></div>''', active="business.html")

# ---------------------------------------------------------------- pay
page("pay.html", "Attelkom Pay", f'''
{head("Attelkom Pay", [("pay.html", "Attelkom Pay")])}
<div class="wrap"><div class="content">
  <img src="{{p}}img/hero_pay.jpg" alt="" style="width:100%;display:block;margin-bottom:20px">
  <h2>Payments from your mobile balance</h2>
  <p>Attelkom Pay is a service of OJSC «Attelkom» together with Talasbank. Pay for services and send money from your mobile balance by SMS or USSD, in any place where there is an Attelkom signal.</p>
  <table class="t"><tr><th>Payment</th><th>SMS to 5050</th><th>Commission</th></tr>
  <tr><td>Registration</td><td>PAY</td><td>free</td></tr>
  <tr><td>Transfer to another Attelkom number</td><td>SEND [number] [amount]</td><td>1%</td></tr>
  <tr><td>Home internet</td><td>NET [contract] [amount]</td><td>free</td></tr>
  <tr><td>Electricity (Talas, Nurzhan)</td><td>ELEC [account] [amount]</td><td>1.5%</td></tr>
  <tr><td>Veterinary services, feed</td><td>VET [code] [amount]</td><td>2.5% (min. 10 som)</td></tr>
  <tr><td>Withdrawal at Talasbank</td><td>CASH [amount]</td><td>2%</td></tr></table>
  <p>Limits: up to 15 000 som per transaction, up to 60 000 som per month. To increase the limit, visit a Talasbank branch with your passport.</p>
  <p class="fine">Attelkom Pay is not connected with any cryptocurrency or third-party payment applications.</p>
</div></div>''', active="pay.html")

# ---------------------------------------------------------------- coverage
page("coverage.html", "Coverage", f'''
{head("Coverage map", [("coverage.html", "Coverage")])}
<div class="wrap"><div class="content">
  <h2>Check coverage</h2>
  <form id="covform" class="form"><label>Settlement</label><select>
    <option value="">— select —</option><option value="talas">Talas</option><option value="nurzhan">Nurzhan</option><option value="iyik">Iyık Janyl</option>
    <option value="district">District centre</option><option value="village">Village / other</option><option value="atr">Autonomous Tribal Regions</option></select>
    <p><button class="btn" type="submit">Check</button></p></form>
  <div id="covres"></div>
  <h2 style="margin-top:30px">Map</h2>
  <div style="background:#dfe8df url({{p}}img/hero_tower.jpg) center/cover;height:360px;display:flex;align-items:center;justify-content:center">
    <div style="background:rgba(255,255,255,.9);padding:16px 22px;font-size:13px">The interactive coverage map is temporarily unavailable. Please use the form above. Street maps: <a href="https://maps.attelkom.net/">maps.attelkom.net</a></div></div>
</div></div>''')

# ---------------------------------------------------------------- about
page("about.html", "About", f'''
{head("About the company", [("about.html", "About")])}
<div class="wrap"><div class="content">
  <img src="{{p}}img/hq.jpg" alt="Attelkom headquarters, Communications Square, Talas" style="width:100%;display:block;margin-bottom:20px">
  <h2>OJSC «Attelkom»</h2>
  <p>Attelkom is the largest telecommunications company of Irad. Since 1994 we connect people, business and the state. Today Attelkom serves more than 2.6 million mobile subscribers and operates the main fibre backbone, international gateways and the national data centre.</p>
  <h3>History</h3>
  <table class="t">
  <tr><td>1994</td><td>Foundation of the company. Modernisation of telephone exchanges of Talas.</td></tr>
  <tr><td>1996</td><td>First dial-up internet in Irad. Registration of the domain zone .ir.ad.</td></tr>
  <tr><td>1997</td><td>Launch of the first GSM mobile network in Talas.</td></tr>
  <tr><td>1999</td><td>Transformation into an open joint-stock company.</td></tr>
  <tr><td>2002</td><td>Opening of the new headquarters and network operations centre on Communications Square.</td></tr>
  <tr><td>2005</td><td>Fibre backbone reaches Nurzhan and Iyık Janyl.</td></tr>
  <tr><td>2010</td><td>Launch of 3G.</td></tr><tr><td>2016</td><td>Launch of 4G/LTE in three cities.</td></tr>
  <tr><td>2026</td><td>Connection to a regional traffic exchange point. 4G in all district centres of Kara-Buura.</td></tr></table>
  <h3>Management</h3>
  <p><b>Samat Kasymov</b> — Director-General</p>
  <h3>Mission</h3>
  <p>To provide every citizen of Irad with reliable and modern communication services, supporting the development of the national economy and the security of the information space.</p>
  <h3 id="tenders">Tenders</h3><p>There are no active tenders at the moment.</p>
  <h3 id="jobs">Vacancies</h3><p>Send your CV to <b>hr@attelkom.net</b>. Current vacancies: network engineer (Nurzhan), sales manager (Iyık Janyl), installer (Talas, 3 positions).</p>
  <h3>Contacts</h3><p>Communications Square 1, Talas<br>Phone: +996 39 312 10 50<br>E-mail: info@attelkom.net</p>
</div></div>''', active="about.html")

# ---------------------------------------------------------------- support
page("support.html", "Help and service centres", f'''
{head("Help", [("support.html", "Help")])}
<div class="wrap"><div class="content">
  <h2>Service centres</h2>
  <table class="t"><tr><th>City</th><th>Address</th><th>Hours</th></tr>
  <tr><td>Talas</td><td>Communications Square 1 (head office)</td><td>Mon–Sat 8:30–19:00</td></tr>
  <tr><td>Talas</td><td>Bazar-i Kalan, pavilion 14</td><td>Mon–Sun 9:00–18:00</td></tr>
  <tr><td>Talas</td><td>Semiz, near the parish of St. Yusup</td><td>Mon–Fri 9:00–18:00</td></tr>
  <tr><td>Nurzhan</td><td>Central square, House of Communications</td><td>Mon–Sat 8:30–19:00</td></tr>
  <tr><td>Iyık Janyl</td><td>Cathedral Hill road, 3</td><td>Mon–Sat 9:00–18:00</td></tr>
  <tr><td>Kyzyl-Adyr</td><td>Main street, 22</td><td>Mon–Fri 9:00–17:00 (lunch 12–13)</td></tr></table>
  <h2 id="faq" style="margin-top:30px">FAQ</h2>
  <p><b>The internet is slow. What to do?</b><br>Restart the router. If the problem continues, call 105.</p>
  <p><b>Some sites do not open.</b><br>Access to certain resources may be restricted in accordance with legislation. See <a href="{{p}}blocked.html">Restricted resources</a>.</p>
  <p><b>How to recover my personal account password?</b><br>Visit a service centre with your passport.</p>
  <p><b>Lorem ipsum dolor sit amet?</b><br>Consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.</p>
</div></div>''')

# ---------------------------------------------------------------- login
page("login.html", "Personal account", f'''
{head("Personal account", [("login.html", "Personal account")])}
<div class="wrap"><div class="content">
  <h2>Log in</h2>
  <form id="loginform" class="form">
    <label>Phone number or contract number</label><input placeholder="+996 39 ___ __ __" required>
    <label>Password</label><input type="password" required>
    <div class="err" id="loginerr"></div>
    <p><button class="btn" type="submit">Log in</button> &nbsp; <a href="{{p}}support.html#faq">Forgot password?</a></p>
  </form>
  <p class="fine">New personal account is coming soon! The old personal account (my.attelkom.net) no longer works.</p>
</div></div>''')

# ---------------------------------------------------------------- restricted
page("blocked.html", "Restricted resources", f'''
{head("Restricted resources", [("blocked.html", "Restricted resources")])}
<div class="wrap"><div class="content">
  <h2>Access to the resource is restricted</h2>
  <p>In accordance with the security directives of 2008 and decisions of the competent authorities of the Irad Special Economic Zone, access to certain internet resources is restricted on the networks of all operators.</p>
  <p>If you see this page instead of the site you requested, the resource is included in the list of restricted resources. Attelkom does not decide which resources are restricted and cannot provide the list.</p>
  <p>Questions about restrictions should be addressed to the Department of Public Information.</p>
  <p class="fine">Use of tools for bypassing restrictions may violate the terms of your contract.</p>
</div></div>''')

# ---------------------------------------------------------------- docs
page("docs.html", "Documents", f'''
{head("Documents", [("docs.html", "Documents")])}
<div class="wrap"><div class="content">
  <h2>Documents</h2>
  <p>&#128196; <a href="#">Public offer for communication services (PDF, 2.1 MB)</a></p>
  <p>&#128196; <a href="#">Full list of prices, valid from 01.04.2026 (PDF, 4.8 MB)</a></p>
  <p>&#128196; <a href="#">Privacy policy (PDF)</a></p>
  <p>&#128196; <a href="#">Fair Use Policy (PDF)</a></p>
  <p>&#128196; <a href="#">Annual report 2023 (PDF, 12 MB)</a></p>
  <p class="fine">Documents are being updated. Please request the current versions at a service centre.</p>
</div></div>''')

# ---------------------------------------------------------------- lang placeholder
page("lang/index.html", "Language", f'''
<div class="wrap"><div class="content" style="text-align:center;padding:60px 20px">
  <h2 style="display:inline-block">Бул бет даярдалууда</h2>
  <p>Страница находится в разработке.</p><p>This page is under construction.</p>
  <p><a class="btn" href="{{p}}index.html">&larr; EN</a></p>
</div></div>''')

# ---------------------------------------------------------------- 404
page("404.html", "Page not found", f'''
<div class="wrap"><div class="content" style="text-align:center;padding:60px 20px">
  <div style="font-size:90px;font-weight:900;color:#1f8a2b;font-family:Montserrat">404</div>
  <h2 style="display:inline-block">Page not found</h2>
  <p>The page you requested does not exist or has been moved.</p>
  <p><a class="btn" href="index.html">To main page</a></p>
</div></div>''', base=True)
print("built")

# ---------------------------------------------------------------- sitemap, robots
with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    f.write("".join(f"  <url><loc>{u}</loc></url>\n" for u in PAGES))
    f.write("</urlset>\n")
with open(os.path.join(ROOT, "robots.txt"), "w") as f:
    f.write("User-agent: *\nAllow: /\n\nSitemap: https://attelkom.net/sitemap.xml\n")
print(len(PAGES), "pages in sitemap.xml")
