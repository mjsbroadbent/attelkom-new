"""Builds the 2019 "modernized" Attelkom site logo (img/logo-2019.svg, img/logo-2019-white.svg).

In-world: WebStudio Talas's rebrand for the 2019 site. The old horse-and-globe emblem
(img/favicon.svg, still used on letterheads and as the favicon) is dropped whole into a
glossy app-icon tile, next to a lowercase Poppins wordmark with Wi-Fi arcs over the "o"
and a tagline in the site's orange. Deliberately middling: stock font, gradient + gloss,
an emblem too detailed for the tile, arcs a little off-centre, colours that don't agree.

    python3 tools/make_logo_2019.py
"""
import re
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path("/usr/share/fonts/truetype/google-fonts")


def text_path(text, font_file, size, x, y, tracking=0.0):
    """SVG path data for `text` set in `font_file` at `size` px, baseline at (x, y)."""
    font = TTFont(FONTS / font_file)
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    scale = size / upm
    pen = SVGPathPen(gs)
    cx = x
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            continue
        tp = TransformPen(pen, (scale, 0, 0, -scale, cx, y))
        gs[name].draw(tp)
        cx += gs[name].width * scale + tracking
    return pen.getCommands(), cx


def emblem_group():
    """The old emblem's <g> (one compound path), from img/favicon.svg."""
    s = (ROOT / "img/favicon.svg").read_text(encoding="utf-8")
    g = re.search(r"<g\b.*</g>", s, re.S).group(0)
    return re.sub(r"fill:#[0-9a-fA-F]{6}", "fill:#ffffff", g)


def build(white=False):
    word_fill = "#ffffff" if white else "#145c1d"
    tag_fill = "#ffb347" if white else "#ff8a00"
    word, word_end = text_path("attelkom", "Poppins-Bold.ttf", 86, 168, 100, tracking=-1.5)
    tag, _ = text_path("Connecting Irad", "Poppins-LightItalic.ttf", 25, 172, 134, tracking=1.2)
    # Wi-Fi arcs over the "o" (the cliche of the day), centred on the letter but a touch high
    _, o_left = text_path("attelk", "Poppins-Bold.ttf", 86, 168, 100, tracking=-1.5)
    _, o_right = text_path("attelko", "Poppins-Bold.ttf", 86, 168, 100, tracking=-1.5)
    kx, cy = (o_left + o_right) / 2 + 1.5, 44
    import math
    sx, sy = math.sin(math.radians(48)), math.cos(math.radians(48))
    arcs = "".join(
        f'<path d="M{kx - r * sx:.1f},{cy - r * sy:.1f} A{r},{r} 0 0 1 {kx + r * sx:.1f},{cy - r * sy:.1f}" '
        f'fill="none" stroke="{tag_fill}" stroke-width="4.5" stroke-linecap="round"/>'
        for r in (10, 18, 26))
    dot = f'<circle cx="{kx:.1f}" cy="{cy - 1:.1f}" r="3.8" fill="{tag_fill}"/>'
    width = int(word_end + 20)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 150" width="{width}" height="150">
<title>attelkom</title>
<defs>
  <linearGradient id="tile" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#8fd14f"/><stop offset=".55" stop-color="#2fa33c"/><stop offset="1" stop-color="#14661e"/>
  </linearGradient>
  <linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff" stop-opacity=".55"/><stop offset="1" stop-color="#ffffff" stop-opacity=".05"/>
  </linearGradient>
  <clipPath id="tileclip"><rect x="8" y="8" width="134" height="134" rx="30"/></clipPath>
  <filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="2" dy="4" stdDeviation="3" flood-color="#000" flood-opacity=".28"/></filter>
</defs>
<g filter="url(#sh)">
  <rect x="8" y="8" width="134" height="134" rx="30" fill="url(#tile)"/>
  <svg x="20" y="20" width="110" height="110" viewBox="3 3 176 176">{emblem_group()}</svg>
  <ellipse cx="62" cy="22" rx="92" ry="52" fill="url(#gloss)" clip-path="url(#tileclip)"/>
</g>
<path d="{word}" fill="{word_fill}"/>
{arcs}{dot}
<path d="{tag}" fill="{tag_fill}"/>
</svg>
"""


if __name__ == "__main__":
    (ROOT / "img/logo-2019.svg").write_text(build(False), encoding="utf-8")
    (ROOT / "img/logo-2019-white.svg").write_text(build(True), encoding="utf-8")
    print("img/logo-2019.svg, img/logo-2019-white.svg")
