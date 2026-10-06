import base64
import datetime
import html
import json
import math
import os
import pathlib
import re
import urllib.request

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "hud"
LOGIN = "Thaskow"
KUMA = "https://kuma.thaskow.fr/api/status-page"
SLUG = "cstonx"
RELEASES = "https://api.github.com/repos/CStonx/download/releases?per_page=3"
STACK = ["cpp", "ts", "js", "vue", "react", "html", "css", "php", "laravel", "symfony", "python", "cmake"]
HOSTED = ["linux", "debian", "docker", "nginx", "githubactions", "git"]
SERVICES = {
    "Site Web - CStonx": "cstonx.thaskow.fr",
    "Ntfy": "ntfy",
    "Bezsel": "beszel",
    "Beszel": "beszel",
    "GlitchTip": "glitchtip",
    "Umami": "umami",
}
LINKS = [
    ("CStonx", "cstonx.thaskow.fr"),
    ("Download", "windows · latest"),
    ("X", "@thaskow"),
    ("Status", "kuma.thaskow.fr"),
]

W, G = 900, 24
P0, P1 = 20, 880
C0, C1 = 56, 844
OUTER, PANEL, GRID, BORDER = "#0a0912", "#0f0d1c", "#19162e", "#2c2650"
ACCENT, ACCENT2, TEXT, MUTED = "#7b6cff", "#c58bff", "#e8e6f5", "#8a86a8"
PROMPT, UP, DOWN = "#3fb950", "#3fb950", "#f85149"
LEVELS = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
HEAT = [(GRID, "1"), (ACCENT, ".35"), (ACCENT, ".6"), (ACCENT, "1"), (ACCENT2, "1")]
MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', 'Cascadia Mono', Menlo, Consolas, 'Liberation Mono', monospace"

CSS = f"""
  text {{ font-family: {MONO}; fill: {TEXT}; }}
  .muted {{ fill: {MUTED}; }}
  .accent {{ fill: {ACCENT}; }}
  .accent2 {{ fill: {ACCENT2}; }}
  .prompt {{ fill: {PROMPT}; }}
  .sys {{ font-size: 13px; letter-spacing: 1.5px; fill: {ACCENT}; }}
  .cmd {{ font-size: 15px; fill: {MUTED}; }}
  .line {{ font-size: 15px; }}
  .h {{ font-size: 22px; font-weight: 700; }}
  .num {{ font-size: 13px; fill: {MUTED}; }}
  .small {{ font-size: 11.5px; fill: {MUTED}; }}
  .label {{ font-size: 10.5px; letter-spacing: 1.5px; fill: {MUTED}; }}
  .value {{ font-size: 32px; font-weight: 800; fill: {ACCENT2}; font-variant-numeric: tabular-nums; }}
  .pulse {{ animation: pulse 2.4s ease-in-out infinite; }}
  .blink {{ animation: blink 1.1s steps(1) infinite; }}
  .glitch-a {{ animation: glitch 7s infinite; }}
  .glitch-b {{ animation: glitch 7s infinite reverse; }}
  @keyframes pulse {{ 50% {{ opacity: .3; }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @keyframes glitch {{
    0%, 91%, 100% {{ transform: none; }}
    92% {{ transform: translate(-5px, 1px); }}
    94% {{ transform: translate(4px, -1px); }}
    96% {{ transform: translate(-2px, 0); }}
  }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""


def get(url, token=None, data=None):
    headers = {"User-Agent": "thaskow-profile", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"bearer {token}"
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    return urllib.request.urlopen(req, timeout=30).read()


def esc(s):
    return html.escape(str(s))


def svg(width, height, label, body, x_offset=0, top=False, bottom=False, left=True, right=True):
    py0 = G if top else 0
    py1 = height - G if bottom else height
    pl = max(P0 - x_offset, 0)
    pr = min(P1 - x_offset, width)
    frame = []
    if left:
        frame.append(f'<line x1="10.5" y1="{10.5 if top else 0}" x2="10.5" y2="{height - 10.5 if bottom else height}" stroke="{ACCENT}" stroke-opacity=".35"/>')
        frame.append(f'<line x1="{P0 + .5}" y1="{py0}" x2="{P0 + .5}" y2="{py1}" stroke="{BORDER}"/>')
    if right:
        rx = width - 10.5
        frame.append(f'<line x1="{rx}" y1="{10.5 if top else 0}" x2="{rx}" y2="{height - 10.5 if bottom else height}" stroke="{ACCENT}" stroke-opacity=".35"/>')
        frame.append(f'<line x1="{pr - .5}" y1="{py0}" x2="{pr - .5}" y2="{py1}" stroke="{BORDER}"/>')
    for edge, y_out, y_in, d in ((top, 10.5, py0 + .5, 1), (bottom, height - 10.5, py1 - .5, -1)):
        if not edge:
            continue
        frame.append(f'<line x1="10" y1="{y_out}" x2="{width - 10}" y2="{y_out}" stroke="{ACCENT}" stroke-opacity=".35"/>')
        frame.append(f'<line x1="{P0}" y1="{y_in}" x2="{P1}" y2="{y_in}" stroke="{BORDER}"/>')
        for x, dx in ((10.5, 1), (width - 10.5, -1)):
            frame.append(f'<path d="M{x} {y_out + 22 * d} V{y_out} H{x + 22 * dx}" fill="none" stroke="{ACCENT}" stroke-width="2.5"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(label)}">
<style>{CSS}</style>
<defs><pattern id="grid" x="{(P0 - x_offset) % G}" y="0" width="{G}" height="{G}" patternUnits="userSpaceOnUse"><path d="M{G} 0H0V{G}" fill="none" stroke="{GRID}"/></pattern></defs>
<rect width="{width}" height="{height}" fill="{OUTER}"/>
<rect x="{pl}" y="{py0}" width="{pr - pl}" height="{py1 - py0}" fill="{PANEL}"/>
<rect x="{pl}" y="{py0}" width="{pr - pl}" height="{py1 - py0}" fill="url(#grid)"/>
{"".join(frame)}
{body}
</svg>
'''


def snap(h):
    return math.ceil(h / G) * G


def section(y, title, number):
    return (
        f'<text class="h" x="{C0}" y="{y}"><tspan class="accent">~/</tspan>{esc(title)}</text>'
        f'<text class="num" x="{C1}" y="{y}" text-anchor="end">// {number:02d}</text>'
        f'<line x1="{C0}" y1="{y + 14.5}" x2="{C1}" y2="{y + 14.5}" stroke="{BORDER}"/>'
        f'<line x1="{C0}" y1="{y + 14.5}" x2="{C0 + 112}" y2="{y + 14.5}" stroke="{ACCENT}" stroke-width="2"/>'
    )


def cmd(y, text, x=C0):
    return f'<text class="cmd" x="{x}" y="{y}"><tspan class="prompt">$</tspan> {esc(text)}</text>'


def box(x, y, w, h, notch=10):
    return (
        f'<path d="M{x} {y}H{x + w - notch}L{x + w} {y + notch}V{y + h}H{x}Z" fill="{OUTER}" fill-opacity=".55" stroke="{ACCENT}" stroke-opacity=".45"/>'
        f'<path d="M{x} {y + 14}V{y}H{x + 14}" fill="none" stroke="{ACCENT}" stroke-width="2"/>'
    )


def top(svc):
    down = sum(not s["up"] for s in svc)
    state = ("ONLINE · ALL SYSTEMS NOMINAL", UP) if not down else (
        f"DEGRADED · {down} SERVICE{'S' if down > 1 else ''} DOWN", DOWN)
    name = "THASKOW"
    lines = [
        ("fullstack developer · Dole, France", None),
        ("C++ · Vue · TypeScript · Python · Docker", None),
        ("building ", "CStonx", " · CS2 stats in the Steam overlay"),
    ]
    rows = []
    for i, parts in enumerate(lines):
        y = 262 + i * 28
        text = esc(parts[0]) if parts[1] is None else (
            f'{esc(parts[0])}<tspan class="accent2" font-weight="700">{esc(parts[1])}</tspan>{esc(parts[2])}')
        rows.append(f'<text class="line" x="{C0}" y="{y}"><tspan class="accent">&gt;&gt;</tspan> {text}</text>')
    body = f'''
<line x1="{P0}" y1="72.5" x2="{P1}" y2="72.5" stroke="{BORDER}"/>
<text class="sys" x="{C0 - 8}" y="53">SYS://THASKOW // NODE:DOLE-FR</text>
<circle class="pulse" cx="{C1 + 8 - len(state[0]) * 9.3 - 10:.0f}" cy="48.5" r="4" fill="{state[1]}"/>
<text class="sys" x="{C1 + 8}" y="53" text-anchor="end" style="fill:{MUTED}">{state[0]}</text>
{cmd(126, "whoami")}
<g font-size="80" font-weight="800" letter-spacing="6">
  <text class="glitch-a" x="{C0 - 3}" y="214" style="fill:{ACCENT2}" fill-opacity=".85">{name}</text>
  <text class="glitch-b" x="{C0 + 3}" y="214" style="fill:{ACCENT}" fill-opacity=".9">{name}</text>
  <text x="{C0}" y="214">{name}</text>
</g>
{"".join(rows)}
<text class="cmd" x="{C0}" y="362"><tspan class="prompt">$</tspan></text>
<rect class="blink" x="{C0 + 18}" y="348" width="9" height="17" fill="{ACCENT2}"/>
{section(420, "links", 1)}
{cmd(474, "ping thaskow --all-channels")}
'''
    return svg(W, 504, "Thaskow aka Lucas, fullstack developer from Dole, France. " + state[0].title(), body, top=True)


TILE_W, TILE_GAP = 185, 16
TILE_EDGES = [0] + [C0 + i * (TILE_W + TILE_GAP) + TILE_W + TILE_GAP // 2 for i in range(len(LINKS) - 1)] + [W]


def tile(i, title, sub):
    tw = TILE_W
    offset = TILE_EDGES[i]
    width = TILE_EDGES[i + 1] - offset
    x = C0 + i * (TILE_W + TILE_GAP) - offset
    body = (
        box(x, 10, tw, 60)
        + f'<text x="{x + 16}" y="37" font-size="15" font-weight="700" style="fill:{ACCENT2}">{esc(title)} <tspan class="muted" font-weight="400">↗</tspan></text>'
        + f'<text class="small" x="{x + 16}" y="58">{esc(sub)}</text>'
    )
    return svg(width, 96, f"{title}: {sub}", body, x_offset=offset, left=i == 0, right=i == len(LINKS) - 1)


def cstonx(rel):
    lv = [(10, "#fe1f00"), (8, "#ff6309"), (9, "#ff6309"), (6, "#ffc800"), (7, "#ffc800"),
          (5, "#ffc800"), (10, "#fe1f00"), (3, "#1ce400"), (8, "#ff6309"), (4, "#ffc800")]
    ratings = ["+3.1", "+1.8", "+2.4", "-0.6", "+0.9", "+0.2", "+4.0", "-1.7", "+1.2", "-0.3"]
    widths = [74, 58, 66, 50, 70, 62, 54, 76, 60, 68]
    rows = []
    for i in range(10):
        team = 0 if i < 5 else 1
        y = 146 + i * 20 + team * 12
        rows.append(
            f'<rect x="548" y="{y - 10}" width="3" height="13" rx="1.5" fill="{"#5b9bd5" if team == 0 else "#e8b04b"}"/>'
            f'<rect x="562" y="{y - 8}" width="{widths[i]}" height="9" rx="2" fill="{BORDER}"/>'
            f'<text x="760" y="{y}" text-anchor="end" font-size="12" font-weight="700" style="fill:{UP if ratings[i][0] == "+" else DOWN}">{ratings[i]}</text>'
            f'<circle cx="812" cy="{y - 3.5}" r="8.5" fill="none" stroke="{lv[i][1]}" stroke-width="2"/>'
            f'<text x="812" y="{y}" text-anchor="middle" font-size="8" font-weight="700" style="fill:{lv[i][1]}">{lv[i][0]}</text>'
        )
    chips, x = [], C0
    for c in ["C++ Windows app", "Vue + TypeScript", "Steam overlay"]:
        w = 20 + len(c) * 7.4
        chips.append(
            f'<rect x="{x}" y="270" width="{w:.0f}" height="26" fill="{OUTER}" fill-opacity=".55" stroke="{ACCENT}" stroke-opacity=".45"/>'
            f'<text x="{x + w / 2:.0f}" y="287" text-anchor="middle" font-size="12" style="fill:{ACCENT2}">{esc(c)}</text>'
        )
        x += w + 10
    latest = rel[0]["tag"] if rel else ""
    body = f'''
{section(44, "cstonx", 2)}
{cmd(98, "cat projects/cstonx.md")}
<text x="{C0}" y="162" font-size="44" font-weight="800">CStonx</text>
<text class="line" x="{C0}" y="204" style="fill:{MUTED}">Leetify and FACEIT stats for all 10</text>
<text class="line" x="{C0}" y="226" style="fill:{MUTED}">players in your CS2 match, right in</text>
<text class="line" x="{C0}" y="248" style="fill:{MUTED}">the Steam overlay (Shift+Tab).</text>
{"".join(chips)}
<text class="small" x="{C0}" y="338"><tspan class="accent">→</tspan> cstonx.thaskow.fr · latest {esc(latest)} · Windows 10/11</text>
{box(532, 92, 312, 264)}
<circle class="pulse" cx="550" cy="114" r="4" fill="{DOWN}"/>
<text class="label" x="562" y="118">LIVE MATCH</text>
<text class="label" x="760" y="118" text-anchor="end">LEETIFY</text>
<text class="label" x="812" y="118" text-anchor="middle">FACEIT</text>
{"".join(rows)}
'''
    return svg(W, 384, "CStonx: Leetify and FACEIT stats for all 10 players in your CS2 match, right in the Steam overlay", body)


def wrap(text, width, lines):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > width:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    out.append(cur)
    if len(out) > lines:
        out = out[:lines]
        out[-1] = out[-1][: width - 1].rstrip(" ,.:;") + "…"
    return out


def status(svc, rel, now):
    rows = []
    for i, s in enumerate(svc):
        y = 140 + i * 30
        color = UP if s["up"] else DOWN
        strip = "".join(
            f'<rect x="{262 + j * 5}" y="{y - 12}" width="3" height="15" fill="{UP if b else DOWN}" fill-opacity="{0.3 + 0.7 * (j + 1) / 30:.2f}"/>'
            for j, b in enumerate(s["beats"][-30:])
        )
        uptime = "  –" if s["uptime"] is None else f'{s["uptime"] * 100:.1f}%'.replace("100.0%", "100%")
        rows.append(
            f'<circle class="pulse" cx="{C0 + 4}" cy="{y - 4.5}" r="4" fill="{color}"/>'
            f'<text class="line" x="{C0 + 18}" y="{y}" font-size="14">{esc(s["name"])}</text>'
            f'{strip}<text x="460" y="{y}" text-anchor="end" font-size="13">{uptime}</text>'
        )
    items = []
    for i, r in enumerate(rel):
        y = 140 + i * 76
        notes = "".join(
            f'<text x="500" y="{y + 22 + k * 18}" font-size="12.5" style="fill:{MUTED}">{esc(line)}</text>'
            for k, line in enumerate(wrap(r["note"], 44, 2))
        )
        items.append(
            f'<text x="500" y="{y}" font-size="14" font-weight="700" style="fill:{ACCENT2}">{esc(r["tag"])}'
            f'<tspan class="muted" font-weight="400" font-size="12">  {r["date"].day} {r["date"]:%b %Y}</tspan></text>{notes}'
        )
    bottom = max(140 + len(svc) * 30, 140 + len(rel) * 76)
    height = snap(bottom + 24)
    body = f'''
{section(44, "status", 3)}
{cmd(98, "curl kuma.thaskow.fr/status")}
<text class="small" x="460" y="98" text-anchor="end">24h · {now:%H:%M} UTC</text>
{"".join(rows)}
<line x1="476.5" y1="80" x2="476.5" y2="{height - 20}" stroke="{BORDER}"/>
{cmd(98, "git tag --sort=-v:refname", x=500)}
{"".join(items)}
'''
    return svg(W, height, "Live status of my self-hosted services and latest CStonx releases", body)


def icons(names, x, y, per_line, cache):
    out = []
    for i, n in enumerate(names):
        col, row = i % per_line, i // per_line
        out.append(f'<image x="{x + col * 54}" y="{y + row * 56}" width="46" height="46" href="{cache[n]}"/>')
    return "".join(out)


def stack():
    cache = {
        n: "data:image/svg+xml;base64," + base64.b64encode(get(f"https://skillicons.dev/icons?i={n}")).decode()
        for n in STACK + HOSTED
    }
    text = ("One VPS, rebuilt from code in a single command: Docker Compose services behind Nginx "
            "and Authelia SSO, monitored with Uptime Kuma and Beszel, nightly backups and restore tests.")
    lines = "".join(
        f'<text x="500" y="{196 + i * 20}" font-size="12.5" style="fill:{MUTED}">{esc(l)}</text>'
        for i, l in enumerate(wrap(text, 44, 6))
    )
    body = f'''
{section(44, "stack", 4)}
{cmd(98, "ls ~/code")}
{icons(STACK, C0, 116, 7, cache)}
<line x1="476.5" y1="80" x2="476.5" y2="268" stroke="{BORDER}"/>
{cmd(98, "ls ~/vps", x=500)}
{icons(HOSTED, 500, 116, 6, cache)}
{lines}
'''
    return svg(W, 312, "Stack: C++, TypeScript, JavaScript, Vue, React, HTML, CSS, PHP, Laravel, Symfony, Python, CMake. Self-hosted on Linux with Docker and Nginx", body)


def streaks(days):
    counts = [d["contributionCount"] for d in days]
    best = run = 0
    for c in counts:
        run = run + 1 if c else 0
        best = max(best, run)
    if counts and not counts[-1]:
        counts = counts[:-1]
    current = 0
    for c in reversed(counts):
        if not c:
            break
        current += 1
    return current, best


def activity(data):
    weeks = data["contributionCalendar"]["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    current, best = streaks(days)
    top_day = max(days, key=lambda d: d["contributionCount"])
    top_date = datetime.date.fromisoformat(top_day["date"])
    stats = [
        ("CONTRIBUTIONS", f'{data["contributionCalendar"]["totalContributions"]:,}', "last 12 months"),
        ("ACTIVE DAYS", f'{sum(1 for d in days if d["contributionCount"])}', f"out of {len(days)} days"),
        ("BEST DAY", f'{top_day["contributionCount"]}', f"{top_date.day} {top_date:%b %Y}"),
        ("CURRENT STREAK", f"{current}d", f"longest: {best} days"),
    ]
    bw, gap = 185, 16
    boxes = "".join(
        box(C0 + i * (bw + gap), 116, bw, 92)
        + f'<text class="label" x="{C0 + i * (bw + gap) + 16}" y="140">{label}</text>'
        + f'<text class="value" x="{C0 + i * (bw + gap) + 16}" y="178">{esc(v)}</text>'
        + f'<text class="small" x="{C0 + i * (bw + gap) + 16}" y="198">{esc(sub)}</text>'
        for i, (label, v, sub) in enumerate(stats)
    )
    step, cell = 14, 11
    x0 = C0 + (C1 - C0 - len(weeks) * step) // 2
    cells, months, last = [], [], None
    for wi, w in enumerate(weeks):
        first = datetime.date.fromisoformat(w["contributionDays"][0]["date"])
        if first.month != last:
            if wi < len(weeks) - 2 and (not months or wi - months[-1][0] > 2):
                months.append((wi, first.strftime("%b")))
            last = first.month
        for d in w["contributionDays"]:
            dow = (datetime.date.fromisoformat(d["date"]).weekday() + 1) % 7
            color, op = HEAT[LEVELS.index(d["contributionLevel"])]
            extra = f' class="pulse" stroke="{ACCENT2}"' if d["date"] == days[-1]["date"] else ""
            cells.append(
                f'<rect{extra} x="{x0 + wi * step}" y="{254 + dow * step}" width="{cell}" height="{cell}" '
                f'fill="{color}" fill-opacity="{op}"/>'
            )
    month_nodes = "".join(f'<text class="small" x="{x0 + wi * step}" y="244">{m}</text>' for wi, m in months)
    lx = C1 - 5 * step - 34
    legend = "".join(
        f'<rect x="{lx + i * step}" y="362" width="{cell}" height="{cell}" fill="{c}" fill-opacity="{o}"/>'
        for i, (c, o) in enumerate(HEAT)
    )
    body = f'''
{section(44, "activity", 5)}
{cmd(98, "gh stats --user thaskow")}
{boxes}
{month_nodes}
{"".join(cells)}
<text class="small" x="{lx - 8}" y="372" text-anchor="end">less</text>{legend}<text class="small" x="{lx + 5 * step + 2}" y="372">more</text>
'''
    return svg(W, 408, f'GitHub activity over the last 12 months: {stats[0][1]} contributions', body)


def bottom(now):
    body = f'''
{cmd(44, "exit")}
<text class="small" x="{C0}" y="70">logout · connection to thaskow closed · refreshed {now.day} {now:%b %Y} {now:%H:%M} UTC</text>
'''
    return svg(W, 120, "", body, bottom=True)


def fetch_services():
    page = json.loads(get(f"{KUMA}/{SLUG}"))
    beats = json.loads(get(f"{KUMA}/heartbeat/{SLUG}"))
    rows = []
    for group in reversed(page["publicGroupList"]):
        for m in group["monitorList"]:
            hb = beats["heartbeatList"].get(str(m["id"]), [])
            rows.append(dict(
                name=SERVICES.get(m["name"], m["name"]),
                up=bool(hb) and hb[-1]["status"] == 1,
                beats=[b["status"] == 1 for b in hb],
                uptime=beats["uptimeList"].get(f'{m["id"]}_24'),
            ))
    return rows


def fetch_releases():
    out = []
    for r in json.loads(get(RELEASES)):
        notes = r["body"].split("## Télécharger")[0]
        bullet = next((l[2:] for l in notes.splitlines() if l.startswith("- ")), r["name"])
        out.append(dict(
            tag=r["tag_name"],
            date=datetime.date.fromisoformat(r["published_at"][:10]),
            note=re.sub(r"[*`]", "", bullet),
        ))
    return out


def fetch_activity():
    query = """query($login: String!) { user(login: $login) { contributionsCollection { contributionCalendar {
      totalContributions weeks { contributionDays { date contributionCount contributionLevel } } } } } }"""
    body = json.loads(get(
        "https://api.github.com/graphql", token=os.environ["GITHUB_TOKEN"],
        data=json.dumps({"query": query, "variables": {"login": LOGIN}}).encode(),
    ))
    if "errors" in body:
        raise SystemExit(body["errors"])
    return body["data"]["user"]["contributionsCollection"]


if __name__ == "__main__":
    now = datetime.datetime.now(datetime.timezone.utc)
    svc, rel = fetch_services(), fetch_releases()
    pieces = {
        "01-top": top(svc),
        "03-cstonx": cstonx(rel),
        "04-status": status(svc, rel, now),
        "05-stack": stack(),
        "06-activity": activity(fetch_activity()),
        "07-bottom": bottom(now),
    }
    pieces.update({f"02-link-{i}": tile(i, *link) for i, link in enumerate(LINKS)})
    OUT.mkdir(parents=True, exist_ok=True)
    for name, content in pieces.items():
        (OUT / f"{name}.svg").write_text(content, encoding="utf-8", newline="\n")
