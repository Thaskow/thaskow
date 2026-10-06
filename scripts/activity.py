import datetime
import json
import os
import urllib.request

from banners import FONT, MONO, write

LOGIN = "Thaskow"
QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""
LEVELS = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
CELL, STEP, X0, Y0 = 12, 15, 54, 130


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    body = json.load(urllib.request.urlopen(req, timeout=30))
    if "errors" in body:
        raise SystemExit(body["errors"])
    return body["data"]["user"]["contributionsCollection"]


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


def card(data, today):
    weeks = data["contributionCalendar"]["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    current, best = streaks(days)
    stats = [
        (data["contributionCalendar"]["totalContributions"], "contributions"),
        (sum(1 for d in days if d["contributionCount"]), "active days"),
        (max(d["contributionCount"] for d in days), "best day"),
        (current, "day streak" if current == 1 else "days streak"),
        (best, "best streak"),
    ]

    def render(t):
        fills = [
            (t["dim"], "1"), (t["glow1"], ".35"), (t["glow1"], ".6"), (t["glow1"], "1"), (t["glow2"], "1"),
        ]
        cells, months, last_month = [], [], None
        for wi, w in enumerate(weeks):
            first = datetime.date.fromisoformat(w["contributionDays"][0]["date"])
            if first.month != last_month:
                if wi < len(weeks) - 2 and (not months or wi - months[-1][0] > 2):
                    months.append((wi, first.strftime("%b")))
                last_month = first.month
            for d in w["contributionDays"]:
                dow = (datetime.date.fromisoformat(d["date"]).weekday() + 1) % 7
                color, op = fills[LEVELS.index(d["contributionLevel"])]
                cls = ' class="today"' if d["date"] == days[-1]["date"] else ""
                cells.append(
                    f'<rect{cls} x="{X0 + wi * STEP}" y="{Y0 + dow * STEP}" width="{CELL}" height="{CELL}" rx="3" '
                    f'fill="{color}" fill-opacity="{op}"><title>{d["date"]}: {d["contributionCount"]}</title></rect>'
                )
        month_nodes = "".join(
            f'<text class="month" x="{X0 + wi * STEP}" y="{Y0 - 10}">{m}</text>' for wi, m in months
        )
        legend_x = 852 - 5 * STEP
        legend = "".join(
            f'<rect x="{legend_x + i * STEP}" y="248" width="{CELL}" height="{CELL}" rx="3" fill="{c}" fill-opacity="{o}"/>'
            for i, (c, o) in enumerate(fills)
        )
        col = 804 / len(stats)
        stat_nodes = "".join(
            f'<text class="num" x="{48 + col * i + col / 2:.0f}" y="312" text-anchor="middle">{v:,}</text>'
            f'<text class="lbl" x="{48 + col * i + col / 2:.0f}" y="334" text-anchor="middle">{label.upper()}</text>'
            for i, (v, label) in enumerate(stats)
        )
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="370" viewBox="0 0 900 370" role="img" aria-label="GitHub activity over the last 12 months: {stats[0][0]} contributions">
<style>
  text {{ font-family: {FONT}; }}
  .label {{ font-size: 12px; font-weight: 600; letter-spacing: 3px; fill: {t["glow1"]}; }}
  .title {{ font-size: 24px; font-weight: 800; letter-spacing: -.5px; fill: {t["text"]}; }}
  .updated {{ font-family: {MONO}; font-size: 12px; fill: {t["muted"]}; }}
  .month, .legend {{ font-size: 11px; fill: {t["muted"]}; }}
  .num {{ font-size: 28px; font-weight: 800; fill: {t["text"]}; font-variant-numeric: tabular-nums; }}
  .lbl {{ font-size: 10px; font-weight: 600; letter-spacing: 1.5px; fill: {t["muted"]}; }}
  .today {{ stroke: {t["glow2"]}; stroke-width: 1.5; animation: pulse 2s ease-in-out infinite; }}
  @keyframes pulse {{ 50% {{ stroke-opacity: .2; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/>
  </linearGradient>
  <radialGradient id="g1"><stop offset="0" stop-color="{t["glow1"]}" stop-opacity="{t["glowop"]}"/><stop offset="1" stop-color="{t["glow1"]}" stop-opacity="0"/></radialGradient>
  <clipPath id="frame"><rect width="900" height="370" rx="16"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="900" height="370" fill="url(#bg)"/>
  <circle cx="120" cy="330" r="260" fill="url(#g1)"/>
</g>
<rect x=".5" y=".5" width="899" height="369" rx="16" fill="none" stroke="{t["border"]}"/>

<text class="label" x="50" y="56">ACTIVITY</text>
<text class="title" x="48" y="88">Last 12 months on GitHub</text>
<text class="updated" x="852" y="56" text-anchor="end">updated {today.day} {today:%b %Y}</text>
{month_nodes}
{"".join(cells)}
<text class="legend" x="{legend_x - 8}" y="258" text-anchor="end">Less</text>
{legend}
<text class="legend" x="{legend_x + 5 * STEP + 4}" y="258">More</text>
<line x1="48" y1="276" x2="852" y2="276" stroke="{t["border"]}"/>
{stat_nodes}
</svg>
'''

    return render


if __name__ == "__main__":
    write("activity", card(fetch(), datetime.datetime.now(datetime.timezone.utc).date()))
