import datetime
import html
import json
import re
import urllib.request

from banners import FONT, MONO, stamp_readme, write, write_links

KUMA = "https://kuma.thaskow.fr/api/status-page"
SLUG = "cstonx"
RELEASES = "https://api.github.com/repos/CStonx/download/releases?per_page=3"
SERVICES = {
    "Site Web - CStonx": ("cstonx.thaskow.fr", "CS2 stats website"),
    "Ntfy": ("ntfy", "Push notifications"),
    "Bezsel": ("Beszel", "Server monitoring"),
    "Beszel": ("Beszel", "Server monitoring"),
    "GlitchTip": ("GlitchTip", "Error tracking"),
    "Umami": ("Umami", "Web analytics"),
}
BEATS = 30
UP, DOWN = "#3fb950", "#f85149"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "thaskow-profile", "Accept": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def services():
    page = get(f"{KUMA}/{SLUG}")
    beats = get(f"{KUMA}/heartbeat/{SLUG}")
    rows = []
    for group in reversed(page["publicGroupList"]):
        for m in group["monitorList"]:
            hb = beats["heartbeatList"].get(str(m["id"]), [])[-BEATS:]
            name, role = SERVICES.get(m["name"], (m["name"], ""))
            rows.append(dict(
                name=name, role=role,
                up=bool(hb) and hb[-1]["status"] == 1,
                beats=[b["status"] == 1 for b in hb],
                uptime=beats["uptimeList"].get(f'{m["id"]}_24'),
            ))
    return rows


def releases():
    out = []
    for r in get(RELEASES):
        notes = r["body"].split("## Télécharger")[0]
        bullet = next((l[2:] for l in notes.splitlines() if l.startswith("- ")), r["name"])
        out.append(dict(
            tag=r["tag_name"],
            date=datetime.date.fromisoformat(r["published_at"][:10]),
            note=re.sub(r"[*`]", "", bullet),
        ))
    return out


def wrap(text, width=50, lines=2):
    words, out, cur = text.split(), [], ""
    for w in words:
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


def card(svc, rel, now):
    down = sum(not s["up"] for s in svc)
    summary = "All systems operational" if not down else f"{down} service{'s' if down > 1 else ''} down"

    def render(t):
        rows = []
        for i, s in enumerate(svc):
            y = 128 + i * 38
            strip = "".join(
                f'<rect x="{240 + j * 5}" y="{y - 12}" width="3" height="16" rx="1.5" fill="{UP if b else DOWN}" fill-opacity="{0.35 + 0.65 * (j + 1) / BEATS:.2f}"/>'
                for j, b in enumerate(s["beats"][-BEATS:])
            )
            uptime = "–" if s["uptime"] is None else f'{s["uptime"] * 100:.1f}%'.replace("100.0%", "100%")
            rows.append(
                f'<circle class="{"dot" if s["up"] else "dot down"}" cx="56" cy="{y - 4}" r="4.5" fill="{UP if s["up"] else DOWN}"/>'
                f'<text class="svc" x="72" y="{y - 4}">{html.escape(s["name"])}</text>'
                f'<text class="role" x="72" y="{y + 11}">{html.escape(s["role"])}</text>'
                f'{strip}'
                f'<text class="pct" x="440" y="{y}" text-anchor="end">{uptime}</text>'
            )
        items = []
        for i, r in enumerate(rel):
            y = 128 + i * 74
            w = 14 + len(r["tag"]) * 7.4
            note = "".join(
                f'<text class="note" x="500" y="{y + 22 + k * 17}">{html.escape(line)}</text>'
                for k, line in enumerate(wrap(r["note"]))
            )
            items.append(
                f'<rect x="500" y="{y - 14}" width="{w:.0f}" height="20" rx="10" fill="{t["glow1"]}" fill-opacity=".16" stroke="{t["glow1"]}" stroke-opacity=".5"/>'
                f'<text class="tag" x="{500 + w / 2:.0f}" y="{y}" text-anchor="middle">{html.escape(r["tag"])}</text>'
                f'<text class="date" x="{500 + w + 10:.0f}" y="{y}">{r["date"].day} {r["date"]:%b %Y}</text>'
                f'{note}'
            )
        height = max(128 + len(svc) * 38, 128 + len(rel) * 74) + 26
        status_color = UP if not down else DOWN
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img" aria-label="Live status of my self-hosted services and latest CStonx releases: {summary}">
<style>
  text {{ font-family: {FONT}; }}
  .label {{ font-size: 12px; font-weight: 600; letter-spacing: 3px; fill: {t["glow1"]}; }}
  .title {{ font-size: 22px; font-weight: 800; letter-spacing: -.5px; fill: {t["text"]}; }}
  .summary {{ font-size: 12px; font-weight: 600; }}
  .checked {{ font-family: {MONO}; font-size: 11px; fill: {t["muted"]}; }}
  .svc {{ font-size: 14px; font-weight: 600; fill: {t["text"]}; }}
  .role, .date {{ font-size: 11.5px; fill: {t["muted"]}; }}
  .pct {{ font-family: {MONO}; font-size: 12.5px; fill: {t["text"]}; font-variant-numeric: tabular-nums; }}
  .tag {{ font-family: {MONO}; font-size: 11.5px; font-weight: 700; fill: {t["text"]}; }}
  .note {{ font-size: 13px; fill: {t["text"]}; }}
  .dot {{ animation: pulse 2.4s ease-in-out infinite; }}
  .down {{ animation-duration: .8s; }}
  @keyframes pulse {{ 50% {{ opacity: .35; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/>
  </linearGradient>
  <radialGradient id="g2"><stop offset="0" stop-color="{t["glow2"]}" stop-opacity="{t["glowop"]}"/><stop offset="1" stop-color="{t["glow2"]}" stop-opacity="0"/></radialGradient>
  <clipPath id="frame"><rect width="900" height="{height}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="900" height="{height}" fill="url(#bg)"/>
  <circle cx="820" cy="40" r="240" fill="url(#g2)"/>
</g>
<rect x=".5" y=".5" width="899" height="{height - 1}" rx="16" fill="none" stroke="{t["border"]}"/>

<text class="label" x="50" y="50">LIVE FROM MY VPS</text>
<text class="title" x="48" y="80">Status</text>
<circle cx="132" cy="73" r="4" fill="{status_color}"/>
<text class="summary" x="142" y="77" fill="{status_color}">{summary}</text>
<text class="checked" x="440" y="50" text-anchor="end">last 24h · {now:%H:%M} UTC</text>
{"".join(rows)}

<line x1="470" y1="40" x2="470" y2="{height - 40}" stroke="{t["border"]}"/>
<text class="label" x="500" y="50">RECENTLY SHIPPED</text>
<text class="title" x="500" y="80">CStonx releases</text>
{"".join(items)}
</svg>
'''

    return render


if __name__ == "__main__":
    svc, rel = services(), releases()
    down = sum(not s["up"] for s in svc)
    write("live", card(svc, rel, datetime.datetime.now(datetime.timezone.utc)))
    write_links([
        ("cstonx", "CStonx"),
        ("download", f"Windows · {rel[0]['tag']}" if rel else "Windows"),
        ("x", "@thaskow"),
        ("status", f"{down} service{'s' if down > 1 else ''} down" if down else "All systems up", DOWN if down else UP),
    ])
    stamp_readme()
