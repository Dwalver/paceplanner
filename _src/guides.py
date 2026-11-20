"""Guide pages for PacePlanner. Each weekly run may append ONE new dict to GUIDES.
Keys: slug, title (<60ch ideally), desc, h1, lead, body (HTML cards; links relative to guides/<slug>/), faq [(q,a)]."""
MI = 1.609344
ETSY_BUNDLE = "https://www.etsy.com/listing/4621577122"

def _fmt(sec):
    sec = int(round(sec)); h, r = divmod(sec, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def _riegel(t, d1, d2, k=1.06):
    return t * (d2 / d1) ** k

_rows = "".join(
    f"<tr><td><b>{_fmt(t)}</b></td><td>{_fmt(_riegel(t,5,10))}</td><td>{_fmt(_riegel(t,5,21.0975))}</td>"
    f"<td>{_fmt(_riegel(t,5,42.195))}</td><td>{_fmt(_riegel(t,5,42.195)/42.195)}</td></tr>"
    for t in range(17*60, 40*60+1, 60))

_calc = """<section class="card">
<h2>Race time predictor</h2>
<p>Enter a recent race result and the distance you want to predict.</p>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;align-items:end">
<label>Your race<br><select id="d1" style="width:100%;padding:8px"><option value="5">5K</option><option value="10">10K</option><option value="21.0975">Half marathon</option><option value="42.195">Marathon</option></select></label>
<label>Your time (h:mm:ss or mm:ss)<br><input id="t1" value="25:00" style="width:100%;padding:8px"></label>
<label>Predict<br><select id="d2" style="width:100%;padding:8px"><option value="5">5K</option><option value="10">10K</option><option value="21.0975" selected>Half marathon</option><option value="42.195">Marathon</option></select></label>
</div>
<p id="out" style="font-size:1.15rem;margin-top:14px"></p>
<script>
(function(){
 const $=id=>document.getElementById(id);
 const parse=s=>{const p=s.trim().split(':').map(Number);if(p.some(isNaN))return NaN;return p.reduce((a,b)=>a*60+b,0)};
 const fmt=x=>{x=Math.round(x);const h=Math.floor(x/3600),m=Math.floor(x%3600/60),s=x%60;return (h?h+':'+String(m).padStart(2,'0'):m)+':'+String(s).padStart(2,'0')};
 function go(){const t=parse($('t1').value),d1=+$('d1').value,d2=+$('d2').value;
  if(!(t>0)){$('out').textContent='Enter a time like 25:00 or 1:52:30.';return}
  const p=t*Math.pow(d2/d1,1.06);
  $('out').innerHTML='Predicted time: <b>'+fmt(p)+'</b> &middot; pace '+fmt(p/d2)+' /km &middot; '+fmt(p/d2*1.609344)+' /mile';}
 ['d1','t1','d2'].forEach(i=>$(i).addEventListener('input',go));go();
})();
</script>
</section>"""

GUIDES = [
 dict(
  slug="race-time-predictor",
  title="Race Time Predictor: 5K to 10K, Half & Marathon Times | PacePlanner",
  desc="Predict your 10K, half marathon and marathon time from a 5K or 10K result, with a free calculator and a 5K conversion chart.",
  h1="Race time predictor: convert your 5K time to 10K, half and marathon",
  lead="Use one recent race to estimate what you can run at any other distance, and how much to trust the number.",
  body=_calc + f"""
<section class="card">
<h2>5K to 10K, half marathon and marathon conversion chart</h2>
<p>Predicted equivalent times for every 5K result from 17:00 to 40:00, using Riegel's formula (T2 = T1 × (D2 / D1)<sup>1.06</sup>). The last column is the marathon pace per kilometre.</p>
<div class="tbl"><table><thead><tr><th>5K time</th><th>10K</th><th>Half marathon</th><th>Marathon</th><th>Marathon /km</th></tr></thead><tbody>{_rows}</tbody></table></div>
</section>
<section class="card">
<h2>How accurate are race time predictions?</h2>
<p>Riegel's formula works well between 5K and half marathon if you have trained for the longer distance. For the marathon it is usually optimistic: most recreational runners finish 5 to 10 percent slower than the prediction unless they have run 50+ km a week and long runs of 30 km or more.</p>
<ul>
<li><b>Use a recent result.</b> A race from the last 6 to 8 weeks, run flat out on a flat course.</li>
<li><b>Predict from the closest distance.</b> A half marathon predicts a marathon far better than a 5K does.</li>
<li><b>Treat the marathon number as a ceiling.</b> Start at the predicted pace plus 5 to 10 seconds per km and speed up after 30 km if you feel good.</li>
</ul>
</section>
<section class="card cta">
<h2>Got your goal time? Train for it</h2>
<p>The free PacePlanner generator turns your race date and predicted time into a week-by-week plan with the target pace for every run. Prefer a spreadsheet? The Etsy plans fill in dates and paces automatically.</p>
<a class="btn" href="../../plan/">Build my free plan</a><a class="btn alt" href="{ETSY_BUNDLE}" rel="noopener">Spreadsheet plans (5K to marathon)</a>
<p style="margin-top:12px">Need the pace per km or mile for a time? See the <a href="../../pace-chart/">pace charts</a> or the <a href="../../">pace calculator</a>.</p>
</section>""",
  faq=[("What marathon time does a 25 minute 5K predict?", f"Riegel's formula predicts about {_fmt(_riegel(1500,5,42.195))} for the marathon and {_fmt(_riegel(1500,5,21.0975))} for the half. Most runners without high mileage should expect a marathon 5 to 10 percent slower."),
       ("What half marathon time does a 50 minute 10K predict?", f"About {_fmt(_riegel(3000,10,21.0975))}, which is {_fmt(_riegel(3000,10,21.0975)/21.0975)} per kilometre."),
       ("What is Riegel's formula?", "It is a race time prediction published by Peter Riegel in 1977: T2 = T1 × (D2 / D1)^1.06. The exponent 1.06 reflects how much a runner slows down as the distance increases."),
       ("Can I run a sub-4 marathon?", f"A 4:00:00 marathon roughly matches a {_fmt(14400/(42.195/5)**1.06)} 5K or a {_fmt(14400/(42.195/21.0975)**1.06)} half marathon by Riegel's formula, but you also need the endurance from several months of consistent training.")]),
]
