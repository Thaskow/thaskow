import base64
import html
import pathlib
import re
import urllib.request

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(
        bg1="#0d1117", bg2="#18132e", panel="#161b22", border="#30363d",
        text="#e6edf3", muted="#8b949e", dim="#30363d", grid="#21262d",
        glow1="#7b6cff", glow2="#c58bff", glowop="0.38", bar="#30363d", backdrop="#100d1d",
        yellow="#ffc800", green="#1ce400",
    ),
    "light": dict(
        bg1="#ffffff", bg2="#f3efff", panel="#f6f8fa", border="#d1d9e0",
        text="#1f2328", muted="#59636e", dim="#d1d9e0", grid="#e5e7eb",
        glow1="#6a5af9", glow2="#b57bff", glowop="0.40", bar="#d1d9e0", backdrop="#f4f1fe",
        yellow="#c79500", green="#1a9a00",
    ),
}

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def header(t):
    roles = ["Fullstack developer", "Building CStonx for CS2 players", "Self-hosting all the things"]
    role_nodes = "\n".join(
        f'<text class="role r{i}" x="64" y="205">{r}</text>' for i, r in enumerate(roles)
    )
    term = [
        ("whoami", "thaskow (Lucas)"),
        ("location", "Dole, France"),
        ("now", "shipping CStonx v1"),
        ("stack", "C++ · Vue · Python · Docker"),
    ]
    term_nodes = []
    for i, (cmd, out) in enumerate(term):
        y = 100 + i * 40
        term_nodes.append(
            '<g>'
            f'<text class="mono prompt" x="560" y="{y}">$ <tspan class="cmd">{cmd}</tspan></text>'
            f'<text class="mono out" x="560" y="{y + 20}">{out}</text></g>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="290" viewBox="0 0 900 290" role="img" aria-label="Thaskow aka Lucas, fullstack developer from Dole, France">
<style>
  text {{ font-family: {FONT}; }}
  .mono {{ font-family: {MONO}; }}
  .hey {{ font-size: 13px; font-weight: 600; letter-spacing: 3px; fill: {t["glow1"]}; }}
  .name {{ font-size: 64px; font-weight: 800; letter-spacing: -2px; }}
  .aka {{ font-size: 20px; font-weight: 500; fill: {t["muted"]}; }}
  .chev {{ font-family: {MONO}; font-size: 18px; fill: {t["glow2"]}; }}
  .role {{ font-family: {MONO}; font-size: 18px; fill: {t["text"]}; opacity: 0; animation: role 9s infinite; }}
  .r0 {{ opacity: 1; }}
  .r1 {{ animation-delay: 3s; }}
  .r2 {{ animation-delay: 6s; }}
  @keyframes role {{
    0%, 28% {{ opacity: 1; transform: none; }}
    33%, 95% {{ opacity: 0; transform: translateY(-8px); }}
    100% {{ opacity: 1; transform: none; }}
  }}
  .orb {{ animation: drift 14s ease-in-out infinite alternate; }}
  .orb2 {{ animation-duration: 18s; animation-direction: alternate-reverse; }}
  @keyframes drift {{ from {{ transform: translate(0, 0); }} to {{ transform: translate(60px, 25px); }} }}
  .prompt {{ font-size: 13px; fill: {t["glow2"]}; }}
  .cmd {{ fill: {t["text"]}; }}
  .out {{ font-size: 13px; fill: {t["muted"]}; }}
  .title {{ font-size: 12px; fill: {t["muted"]}; }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/>
  </linearGradient>
  <linearGradient id="ink" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t["glow1"]}"/><stop offset="1" stop-color="{t["glow2"]}"/>
  </linearGradient>
  <radialGradient id="g1"><stop offset="0" stop-color="{t["glow1"]}" stop-opacity="{t["glowop"]}"/><stop offset="1" stop-color="{t["glow1"]}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2"><stop offset="0" stop-color="{t["glow2"]}" stop-opacity="{t["glowop"]}"/><stop offset="1" stop-color="{t["glow2"]}" stop-opacity="0"/></radialGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t["grid"]}"/></pattern>
  <clipPath id="frame"><rect width="900" height="290" rx="16"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="900" height="290" fill="url(#bg)"/>
  <rect width="900" height="290" fill="url(#dots)"/>
  <circle class="orb" cx="180" cy="40" r="220" fill="url(#g1)"/>
  <circle class="orb orb2" cx="720" cy="260" r="250" fill="url(#g2)"/>
</g>
<rect x=".5" y=".5" width="899" height="289" rx="16" fill="none" stroke="{t["border"]}"/>

<text class="hey" x="66" y="85">HEY, I'M</text>
<text class="name" x="62" y="149" fill="url(#ink)">Thaskow</text>
<text class="aka" x="342" y="149">aka Lucas</text>
<text class="chev" x="64" y="205" dx="-22">›</text>
{role_nodes}

<rect x="540" y="40" width="320" height="214" rx="10" fill="{t["panel"]}" fill-opacity=".85" stroke="{t["border"]}"/>
<circle cx="560" cy="58" r="5" fill="#ff5f57"/><circle cx="578" cy="58" r="5" fill="#febc2e"/><circle cx="596" cy="58" r="5" fill="#28c840"/>
<text class="title mono" x="700" y="62" text-anchor="middle">~/thaskow</text>
<line x1="540" y1="74" x2="860" y2="74" stroke="{t["border"]}"/>
{"".join(term_nodes)}
</svg>
'''


def cstonx(t):
    lv = [(10, "#fe1f00"), (8, "#ff6309"), (9, "#ff6309"), (6, t["yellow"]), (7, t["yellow"]),
          (5, t["yellow"]), (10, "#fe1f00"), (3, t["green"]), (8, "#ff6309"), (4, t["yellow"])]
    ratings = ["+3.1", "+1.8", "+2.4", "-0.6", "+0.9", "+0.2", "+4.0", "-1.7", "+1.2", "-0.3"]
    widths = [74, 58, 66, 50, 70, 62, 54, 76, 60, 68]
    rows = []
    for i in range(10):
        team = 0 if i < 5 else 1
        y = 88 + i * 22 + team * 14
        col = "#5b9bd5" if team == 0 else "#e8b04b"
        good = not ratings[i].startswith("-")
        rows.append(
            '<g>'
            f'<rect x="538" y="{y - 10}" width="3" height="13" rx="1.5" fill="{col}"/>'
            f'<circle cx="558" cy="{y - 3.5}" r="6" fill="{t["bar"]}"/>'
            f'<rect x="572" y="{y - 8}" width="{widths[i]}" height="9" rx="4.5" fill="{t["bar"]}"/>'
            f'<text class="mono rating" x="760" y="{y}" text-anchor="end" fill="{"#3fb950" if good else "#f85149"}">{ratings[i]}</text>'
            f'<circle cx="826" cy="{y - 3.5}" r="8.5" fill="none" stroke="{lv[i][1]}" stroke-width="2"/>'
            f'<text class="lvl" x="826" y="{y}" text-anchor="middle" fill="{lv[i][1]}">{lv[i][0]}</text>'
            f'</g>'
        )
    chips = ["C++ Windows app", "Vue + TypeScript", "Steam overlay"]
    chip_nodes, x = [], 48
    for c in chips:
        w = 18 + len(c) * 7.2
        chip_nodes.append(
            f'<rect x="{x}" y="244" width="{w:.0f}" height="26" rx="13" fill="{t["panel"]}" stroke="{t["border"]}"/>'
            f'<text class="chip" x="{x + w / 2:.0f}" y="261" text-anchor="middle">{c}</text>'
        )
        x += w + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="340" viewBox="0 0 900 340" role="img" aria-label="CStonx: Leetify and FACEIT stats for all 10 players in your CS2 match, right in the Steam overlay">
<style>
  text {{ font-family: {FONT}; }}
  .mono {{ font-family: {MONO}; }}
  .label {{ font-size: 12px; font-weight: 600; letter-spacing: 3px; fill: {t["glow1"]}; }}
  .brand {{ font-size: 46px; font-weight: 800; letter-spacing: -1.5px; fill: {t["text"]}; }}
  .tag {{ font-size: 17px; fill: {t["muted"]}; }}
  .chip {{ font-size: 12px; font-weight: 500; fill: {t["text"]}; }}
  .head {{ font-size: 10px; font-weight: 600; letter-spacing: 1.5px; fill: {t["muted"]}; }}
  .rating {{ font-size: 12px; font-weight: 600; }}
  .lvl {{ font-size: 8px; letter-spacing: -.3px; font-weight: 700; }}
  .live {{ animation: pulse 1.6s ease-in-out infinite; }}
  @keyframes pulse {{ 50% {{ opacity: .25; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/>
  </linearGradient>
  <radialGradient id="g1"><stop offset="0" stop-color="{t["glow1"]}" stop-opacity="{t["glowop"]}"/><stop offset="1" stop-color="{t["glow1"]}" stop-opacity="0"/></radialGradient>
  <clipPath id="frame"><rect width="900" height="340" rx="16"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="900" height="340" fill="url(#bg)"/>
  <circle cx="700" cy="170" r="280" fill="url(#g1)"/>
</g>
<rect x=".5" y=".5" width="899" height="339" rx="16" fill="none" stroke="{t["border"]}"/>

<text class="label" x="50" y="94">WHAT I'M BUILDING</text>
<text class="brand" x="48" y="146">CStonx</text>
<text class="tag" x="50" y="184">Leetify and FACEIT stats for all 10 players</text>
<text class="tag" x="50" y="208">in your CS2 match, right in the Steam overlay.</text>
{"".join(chip_nodes)}

<rect x="520" y="30" width="340" height="290" rx="10" fill="{t["panel"]}" fill-opacity=".9" stroke="{t["border"]}"/>
<circle class="live" cx="540" cy="52" r="4" fill="#f85149"/>
<text class="head" x="552" y="56">LIVE MATCH</text>
<text class="head" x="760" y="56" text-anchor="end">LEETIFY</text>
<text class="head" x="826" y="56" text-anchor="middle">FACEIT</text>
{"".join(rows)}
</svg>
'''


def footer(t):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="60" viewBox="0 0 900 60" role="img" aria-label="">
<style>
  .w {{ animation: wave 8s ease-in-out infinite alternate; }}
  .w2 {{ animation-duration: 11s; }}
  @keyframes wave {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-120px); }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<defs>
  <linearGradient id="ink" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t["glow1"]}"/><stop offset="1" stop-color="{t["glow2"]}"/>
  </linearGradient>
</defs>
<path class="w" d="M0 34 C 120 14, 240 54, 360 34 S 600 14, 720 34 S 960 54, 1080 34 L 1080 60 L 0 60 Z" fill="url(#ink)" opacity=".25"/>
<path class="w w2" d="M0 42 C 150 26, 300 58, 450 42 S 750 26, 900 42 S 1050 58, 1080 42 L 1080 60 L 0 60 Z" fill="url(#ink)" opacity=".5"/>
</svg>
'''


STACK = ["cpp", "ts", "js", "vue", "react", "html", "css", "php", "laravel", "symfony", "python", "cmake"]
HOSTED = ["linux", "debian", "docker", "nginx", "githubactions", "git"]
SELF_HOST = ("One VPS, rebuilt from code in a single command: Docker Compose services behind Nginx "
             "and Authelia SSO, monitored with Uptime Kuma and Beszel, with nightly backups and restore tests.")
INSET, PAD, CAP = 20, 10, 28
LINK_EDGES = [0, 230, 450, 670, 900]


def fetch_icon(name):
    req = urllib.request.Request(f"https://skillicons.dev/icons?i={name}", headers={"User-Agent": "thaskow-profile"})
    return "data:image/svg+xml;base64," + base64.b64encode(urllib.request.urlopen(req, timeout=30).read()).decode()


def stack(icons):
    def icon_row(names, x, y, per_line):
        return "".join(
            f'<image x="{x + (i % per_line) * 56}" y="{y + (i // per_line) * 56}" width="48" height="48" href="{icons[n]}"/>'
            for i, n in enumerate(names)
        )

    def render(t):
        words, lines, cur = SELF_HOST.split(), [], ""
        for w in words:
            if len(cur) + len(w) + 1 > 50:
                lines.append(cur)
                cur = w
            else:
                cur = f"{cur} {w}".strip()
        lines.append(cur)
        text = "".join(f'<text class="body" x="484" y="{160 + i * 21}">{html.escape(l)}</text>' for i, l in enumerate(lines))
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="260" viewBox="0 0 900 260" role="img" aria-label="Stack: C++, TypeScript, JavaScript, Vue, React, HTML, CSS, PHP, Laravel, Symfony, Python, CMake. Self-hosted on Linux, Debian, Docker, Nginx">
<style>
  text {{ font-family: {FONT}; }}
  .label {{ font-size: 12px; font-weight: 600; letter-spacing: 3px; fill: {t["glow1"]}; }}
  .body {{ font-size: 14px; fill: {t["muted"]}; }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/>
  </linearGradient>
  <radialGradient id="g1"><stop offset="0" stop-color="{t["glow1"]}" stop-opacity="{t["glowop"]}"/><stop offset="1" stop-color="{t["glow1"]}" stop-opacity="0"/></radialGradient>
  <clipPath id="frame"><rect width="900" height="260" rx="16"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="900" height="260" fill="url(#bg)"/>
  <circle cx="60" cy="250" r="220" fill="url(#g1)"/>
</g>
<rect x=".5" y=".5" width="899" height="259" rx="16" fill="none" stroke="{t["border"]}"/>
<text class="label" x="50" y="56">THINGS I CODE WITH</text>
{icon_row(STACK, 48, 76, 7)}
<line x1="450" y1="40" x2="450" y2="220" stroke="{t["border"]}"/>
<text class="label" x="484" y="56">WHAT I SELF-HOST</text>
{icon_row(HOSTED, 482, 76, 6)}
{text}
</svg>
'''

    return render


def link(i, text):
    def render(t):
        width = LINK_EDGES[i + 1] - LINK_EDGES[i]
        x = INSET + i * 220 - LINK_EDGES[i]
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="56" viewBox="0 0 {width} 56" role="img" aria-label="{html.escape(text)}">
<style>text {{ font-family: {FONT}; }}</style>
<rect x="{x + .5}" y="10.5" width="199" height="35" rx="17.5" fill="{t["panel"]}" stroke="{t["border"]}"/>
<text x="{x + 100}" y="33" text-anchor="middle" font-size="13" font-weight="600" fill="{t["text"]}">{html.escape(text)} <tspan fill="{t["glow1"]}">↗</tspan></text>
</svg>
'''

    return render


def backdrop(card, t, top=False, bottom=False, inset=True, left=True, right=True):
    head = re.match(r'<svg xmlns="http://www.w3.org/2000/svg" width="(\d+)" height="(\d+)" viewBox="[^"]*" role="img" aria-label="([^"]*)">', card)
    w, h, label = int(head[1]), int(head[2]), head[3]
    pt, pb = (CAP if top else PAD), (CAP if bottom else PAD)
    if inset:
        ch = h * (900 - 2 * INSET) / 900
        inner = card.replace(head[0], f'<svg x="{INSET}" y="{pt}" width="{900 - 2 * INSET}" height="{ch:.2f}" viewBox="0 0 900 {h}">', 1)
        height = round(pt + ch + pb)
    else:
        inner = card.replace(head[0], f'<svg x="0" y="0" width="{w}" height="{h}" viewBox="0 0 {w} {h}">', 1)
        height = h
    r = 20
    y0 = r if top else 0
    y1 = height - r if bottom else height
    shape = [f"M0 {y0}"]
    shape.append(f"Q0 0 {r} 0H{w - r}Q{w} 0 {w} {r}" if top else f"H{w}")
    shape.append(f"V{y1}")
    shape.append(f"Q{w} {height} {w - r} {height}H{r}Q0 {height} 0 {y1}" if bottom else f"V{height}H0")
    shape.append("Z")
    edges = []
    if left:
        edges.append(f'<line x1=".5" y1="{y0}" x2=".5" y2="{y1}"/>')
    if right:
        edges.append(f'<line x1="{w - .5}" y1="{y0}" x2="{w - .5}" y2="{y1}"/>')
    if top:
        edges.append(f'<path d="M.5 {y0}Q.5 .5 {r} .5H{w - r}Q{w - .5} .5 {w - .5} {y0}"/>')
    if bottom:
        edges.append(f'<path d="M.5 {y1}Q.5 {height - .5} {r} {height - .5}H{w - r}Q{w - .5} {height - .5} {w - .5} {y1}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{height}" viewBox="0 0 {w} {height}" role="img" aria-label="{label}">
<defs><clipPath id="bdclip"><path d="{"".join(shape)}"/></clipPath></defs>
<path d="{"".join(shape)}" fill="{t["backdrop"]}"/>
<g clip-path="url(#bdclip)">{inner}</g>
<g fill="none" stroke="{t["glow1"]}" stroke-opacity=".35">{"".join(edges)}</g>
</svg>
'''


def write(name, fn, **frame):
    ASSETS.mkdir(exist_ok=True)
    for theme, t in THEMES.items():
        (ASSETS / f"{name}-{theme}.svg").write_text(backdrop(fn(t), t, **frame), encoding="utf-8", newline="\n")


def write_links(texts):
    for i, text in enumerate(texts):
        write(f"link-{i}", link(i, text), inset=False, left=i == 0, right=i == len(texts) - 1)


if __name__ == "__main__":
    write("header", header, top=True)
    write("cstonx", cstonx)
    write("footer", footer, bottom=True, inset=False)
    icons = {n: fetch_icon(n) for n in STACK + HOSTED}
    write("stack", stack(icons))
