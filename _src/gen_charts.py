"""Generates the pace chart SEO pages. Run: python3 _src/gen_charts.py (from repo root)."""
import json, os
BASE = "https://dwalver.github.io/paceplanner"
MI = 1.609344
ETSY = {"5k":"https://www.etsy.com/listing/4621569947","10k":"https://www.etsy.com/listing/4621556280",
        "half":"https://www.etsy.com/listing/4621555304","marathon":"https://www.etsy.com/listing/4621547981",
        "bundle":"https://www.etsy.com/listing/4621577122"}

def fmt(sec, hours=None):
    sec = int(round(sec)); h, r = divmod(sec, 3600); m, s = divmod(r, 60)
    if h or hours: return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

RACES = [
 dict(slug="5k", key="5k", name="5K", km=5, lo=15*60, hi=45*60, step=60,
      splits=[(1,"1 km"),(MI,"1 mile"),(3,"3 km")], weeks=8,
      intro="Use this 5K pace chart to see the pace per kilometre and per mile you need to hold for every finish time from 15 to 45 minutes, plus your 1 km, 1 mile and 3 km split times.",
      faq=[("What is a good 5K time?","For most recreational runners, finishing under 30 minutes is a solid goal, which is about 6:00 per km or 9:39 per mile. Under 25 minutes (5:00/km) puts you well ahead of the average parkrun field, and sub-20 (4:00/km) is a strong club-level time."),
           ("How do I run a faster 5K?","Combine one interval session a week (for example 5 × 1 km at goal pace with short recoveries) with mostly easy running. Most improvement for beginners comes from running more often at an easy, conversational pace."),
           ("What pace is a 25 minute 5K?","A 25:00 5K is 5:00 per kilometre or 8:03 per mile.")]),
 dict(slug="10k", key="10k", name="10K", km=10, lo=32*60, hi=80*60, step=120,
      splits=[(1,"1 km"),(MI,"1 mile"),(5,"5 km")], weeks=10,
      intro="This 10K pace chart shows the pace per kilometre and per mile for every finish time from 32 minutes to 1 hour 20, with the 5 km split you need to be on target at halfway.",
      faq=[("What is a good 10K time?","Under one hour is the classic first goal for a 10K, which means 6:00 per km or 9:39 per mile. Sub-50 (5:00/km) is a strong recreational time and sub-40 (4:00/km) is competitive at most local races."),
           ("What pace is a 50 minute 10K?","A 50:00 10K is 5:00 per kilometre or 8:03 per mile, with a 25:00 split at 5 km."),
           ("Should I run even splits in a 10K?","Yes. Aim to pass 5 km within a few seconds of half your goal time. Starting too fast is the most common reason runners miss their target.")]),
 dict(slug="half-marathon", key="half", name="Half marathon", km=21.0975, lo=75*60, hi=180*60, step=300,
      splits=[(1,"1 km"),(MI,"1 mile"),(5,"5 km"),(10,"10 km"),(15,"15 km")], weeks=12,
      intro="This half marathon pace chart lists the pace per kilometre and per mile for every finish time from 1:15 to 3:00, plus the 5 km, 10 km and 15 km split times to check during the race.",
      faq=[("What pace is a 2 hour half marathon?","A 2:00:00 half marathon is 5:41 per kilometre or 9:09 per mile. You should pass 10 km in about 56:53."),
           ("What is a good half marathon time?","Breaking two hours is the most popular half marathon goal. Around 1:45 is a strong recreational time, and sub-1:30 (4:16/km) is a competitive club-level result."),
           ("How long should I train for a half marathon?","About 12 weeks if you can already run 30 to 45 minutes comfortably. Build your long run gradually to around 18 to 20 km.")]),
 dict(slug="marathon", key="marathon", name="Marathon", km=42.195, lo=150*60, hi=390*60, step=300,
      splits=[(1,"1 km"),(MI,"1 mile"),(10,"10 km"),(21.0975,"Half"),(30,"30 km")], weeks=16,
      intro="This marathon pace chart shows the pace per kilometre and per mile for every finish time from 2:30 to 6:30, plus the 10 km, halfway and 30 km split times you need to be on track.",
      faq=[("What pace is a 4 hour marathon?","A 4:00:00 marathon is 5:41 per kilometre or 9:09 per mile, with a halfway split of 2:00:00."),
           ("What pace do I need for a sub-3 marathon?","A 2:59:59 marathon needs 4:15 per kilometre or 6:51 per mile, with a halfway split just under 1:30:00."),
           ("Should I run a negative split in a marathon?","Aim for even pacing, or a halfway split one to two minutes faster than half your goal at most. Runners who go out too fast usually slow dramatically after 30 km.")]),
]

STYLE = """:root{--bg:#f6f8fb;--card:#fff;--ink:#1b2733;--muted:#5b6b7b;--brand:#1f3a5f;--accent:#f26b3a;--line:#dde4ec;--soft:#eef3f8}
@media (prefers-color-scheme:dark){:root{--bg:#0f1720;--card:#17212c;--ink:#e6edf3;--muted:#9fb0c0;--brand:#8db4e2;--accent:#ff8a5c;--line:#2a3846;--soft:#1d2a37}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
header{background:var(--brand);color:#fff;padding:28px 16px 36px}@media (prefers-color-scheme:dark){header{background:#13263d}}
.wrap{max-width:880px;margin:0 auto;padding:0 16px}header h1{margin:0 0 6px;font-size:clamp(1.6rem,4vw,2.2rem)}header p{margin:0;opacity:.9}
nav{display:flex;gap:14px;flex-wrap:wrap;margin-top:14px;font-size:.95rem}nav a{color:#fff;opacity:.9}main{margin-top:-18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px;margin:0 0 20px}
h2{margin:0 0 8px;font-size:1.3rem;color:var(--brand)}h3{margin:16px 0 4px;font-size:1.05rem}a{color:var(--brand)}
.tbl{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:.95rem;font-variant-numeric:tabular-nums}
th,td{text-align:right;padding:7px 8px;border-bottom:1px solid var(--line);white-space:nowrap}th:first-child,td:first-child{text-align:left}
th{color:var(--muted);font-weight:600;font-size:.85rem;position:sticky;top:0;background:var(--card)}tr:nth-child(even) td{background:var(--soft)}
.btn{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;padding:11px 18px;border-radius:9px;font-weight:600;margin:6px 8px 0 0}
.btn.alt{background:var(--brand)}@media (prefers-color-scheme:dark){.btn.alt{color:#0f1720}}
.cta{border:2px solid var(--accent)}footer{color:var(--muted);font-size:.85rem;text-align:center;padding:24px 16px 40px}"""

def page(path, title, desc, h1, lead, body, jsonld):
    url = f"{BASE}/{path}"
    depth = path.count("/")
    up = "../" * depth
    nav = (f'<nav><a href="{up}">Pace calculator</a><a href="{up}plan/"><b>Free plan generator</b></a>'
           f'<a href="{up}pace-chart/">Pace charts</a>'
           + "".join(f'<a href="{up}pace-chart/{r["slug"]}/">{r["name"]}</a>' for r in RACES) + "</nav>")
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>\n' for j in jsonld)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{h1}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="PacePlanner">
{ld}<style>{STYLE}</style>
</head>
<body>
<header><div class="wrap">
<h1>{h1}</h1>
<p>{lead}</p>
{nav}
</div></header>
<main class="wrap">
{body}
</main>
<footer>© 2026 PacePlanner · <a href="{up}">Running pace calculator</a> · <a href="{up}plan/">Training plan generator</a></footer>
</body>
</html>
"""

def cta(r, up):
    return f"""<section class="card cta">
<h2>Turn your goal time into a training plan</h2>
<p>The free PacePlanner generator builds a {r['weeks']}-week {r['name'].lower()} plan from your race date and goal time, with the target pace for every run. Prefer a spreadsheet you keep? The {r['name']} plan on Etsy fills in your dates and paces automatically in Excel or Google Sheets.</p>
<a class="btn" href="{up}plan/">Build my free {r['name'].lower()} plan</a><a class="btn alt" href="{ETSY[r['key']]}" rel="noopener">{r['name']} spreadsheet plan</a>
</section>"""

def breadcrumb(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}

out = []
for r in RACES:
    path = f"pace-chart/{r['slug']}/"
    rows = []
    t = r["lo"]
    while t <= r["hi"]:
        pk = t / r["km"]
        cells = [f"<td><b>{fmt(t, hours=r['km']>15)}</b></td>", f"<td>{fmt(pk)}</td>", f"<td>{fmt(pk*MI)}</td>",
                 f"<td>{60/(pk/60):.1f}</td>"]
        cells += [f"<td>{fmt(pk*d, hours=d>15)}</td>" for d, _ in r["splits"][2:]]
        rows.append("<tr>" + "".join(cells) + "</tr>")
        t += r["step"]
    heads = ["Finish time","Pace /km","Pace /mile","km/h"] + [f"{n} split" for _, n in r["splits"][2:]]
    table = "<div class=\"tbl\"><table><thead><tr>" + "".join(f"<th>{h}</th>" for h in heads) + "</tr></thead><tbody>" + "\n".join(rows) + "</tbody></table></div>"
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in r["faq"])
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in r["faq"]]}
    body = f"""<section class="card">
<h2>{r['name']} pace chart ({fmt(r['lo'], hours=r['km']>15)} to {fmt(r['hi'], hours=r['km']>15)})</h2>
<p>{r['intro']} Times are for even pacing over {r['km']:g} km ({r['km']/MI:.2f} miles). For a time between two rows, use the <a href="../../">pace calculator</a>.</p>
{table}
</section>
{cta(r, '../../')}
<section class="card">
<h2>Common questions</h2>
{faq_html}
<p>See also: {' · '.join(f'<a href="../{o["slug"]}/">{o["name"]} pace chart</a>' for o in RACES if o is not r)}.</p>
</section>"""
    html = page(path, f"{r['name']} Pace Chart: Pace per km & mile for Every Finish Time | PacePlanner",
                f"{r['name']} pace chart with the pace per km and per mile for every finish time, plus split times. Free, printable and mobile friendly.",
                f"{r['name']} pace chart", f"The pace per km and per mile for every {r['name'].lower()} finish time, with split times.",
                body, [faq_ld, breadcrumb([("PacePlanner", BASE+"/"),("Pace charts", BASE+"/pace-chart/"),(r['name'], BASE+"/"+path)])])
    os.makedirs(path, exist_ok=True); open(path+"index.html","w").write(html); out.append(path)

# hub page: km <-> mile conversion
rows = []
for s in range(180, 601, 10):
    rows.append(f"<tr><td><b>{fmt(s)}</b></td><td>{fmt(s*MI)}</td><td>{3600/s:.1f}</td>" +
                "".join(f"<td>{fmt(s*r['km'], hours=r['km']>15)}</td>" for r in RACES) + "</tr>")
heads = ["Pace /km","Pace /mile","km/h"] + [r["name"] for r in RACES]
table = "<div class=\"tbl\"><table><thead><tr>" + "".join(f"<th>{h}</th>" for h in heads) + "</tr></thead><tbody>" + "\n".join(rows) + "</tbody></table></div>"
body = f"""<section class="card">
<h2>Pick your race</h2>
<p>{' · '.join(f'<a href="{r["slug"]}/"><b>{r["name"]} pace chart</b></a>' for r in RACES)}</p>
</section>
<section class="card">
<h2>Pace conversion chart: min/km to min/mile and finish times</h2>
<p>Every pace from 3:00 to 10:00 per kilometre, converted to minutes per mile and kilometres per hour, with the finish time it gives at 5K, 10K, half marathon and marathon.</p>
{table}
</section>
<section class="card cta">
<h2>Know your pace? Get a plan built around it</h2>
<p>The free generator turns a race date and goal time into a week-by-week plan with target paces for every run.</p>
<a class="btn" href="../plan/">Build my free plan</a><a class="btn alt" href="{ETSY['bundle']}" rel="noopener">All four spreadsheet plans</a>
</section>"""
faq = [("How do I convert pace per km to pace per mile?","Multiply the pace per kilometre by 1.609. For example, 5:00 per km × 1.609 = 8:03 per mile."),
       ("How do I convert pace to speed?","Divide 60 by the pace in minutes. A pace of 5:00 per km is 60 / 5 = 12 km/h.")]
html = page("pace-chart/", "Running Pace Chart: min/km to min/mile with 5K–Marathon Times | PacePlanner",
            "Running pace chart converting min/km to min/mile and km/h, with finish times for 5K, 10K, half marathon and marathon at every pace.",
            "Running pace charts", "Convert min/km to min/mile and see your finish time at every distance.",
            body, [{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]},
                   breadcrumb([("PacePlanner", BASE+"/"),("Pace charts", BASE+"/pace-chart/")])])
os.makedirs("pace-chart", exist_ok=True); open("pace-chart/index.html","w").write(html); out.insert(0,"pace-chart/")

urls = ["", "plan/"] + out
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{BASE}/{u}</loc><lastmod>2026-11-20</lastmod></url>\n" for u in urls) + "</urlset>\n")
print("wrote", out)
