import json, sys
proj = sys.argv[1]
OFF = 0.3  # narration starts at 0.3 s on the root
words = json.load(open(f"{proj}/assets/transcript.json"))
words = [dict(w, start=w["start"] + OFF, end=w["end"] + OFF) for w in words if w["text"].strip()]
# groups of up to 3 words; break after sentence punctuation or a pause >= 0.15 s
groups, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    brk = w["text"][-1] in ".,?!" or len(cur) == 3 or (nxt and nxt["start"] - w["end"] >= 0.35) or not nxt
    if brk:
        groups.append(cur); cur = []
html, js = [], []
for gi, g in enumerate(groups):
    start = max(g[0]["start"] - 0.05, 0.2)
    nxt = groups[gi + 1][0]["start"] - 0.05 if gi + 1 < len(groups) else g[-1]["end"] + 0.4
    end = min(g[-1]["end"] + 0.35, nxt)
    spans = "".join(
        f'<span class="cap-word" id="cap-w{gi}-{wi}"><span class="cap-bg" id="cap-bg{gi}-{wi}"></span><span class="cap-text">{w["text"].strip(".,").upper()}</span></span>'
        for wi, w in enumerate(g))
    html.append(f'    <div class="cap-group" id="cap-g{gi}">{spans}</div>')
    js.append(f'      tl.set("#cap-g{gi}", {{ visibility: "visible" }}, {start:.2f});')
    js.append(f'      tl.fromTo("#cap-g{gi}", {{ opacity: 0, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.12, ease: "power2.out" }}, {start:.2f});')
    for wi, w in enumerate(g):
        js.append(f'      tl.fromTo("#cap-bg{gi}-{wi}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.12, ease: "power2.out" }}, {w["start"]:.2f});')
        js.append(f'      tl.to("#cap-bg{gi}-{wi}", {{ opacity: 0, duration: 0.08, ease: "power2.in" }}, {max(w["end"], w["start"] + 0.15):.2f});')
    js.append(f'      tl.to("#cap-g{gi}", {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, {end - 0.1:.2f});')
    js.append(f'      tl.set("#cap-g{gi}", {{ opacity: 0, visibility: "hidden" }}, {end:.2f});')
out = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cap-group {{ position: absolute; left: 0; width: 100%; bottom: 610px; padding: 0 80px; display: flex; flex-wrap: wrap; justify-content: center; gap: 6px 10px; opacity: 0; visibility: hidden; overflow: visible; }}
    .cap-word {{ position: relative; display: inline-block; padding: 4px 14px 8px; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 72px; line-height: 1; color: #ffffff; letter-spacing: 0.01em; }}
    .cap-text {{ position: relative; z-index: 1; -webkit-text-stroke: 10px #16110b; paint-order: stroke fill; }}
    .cap-bg {{ position: absolute; inset: 0; background: #d42f1a; border-radius: 6px; transform-origin: 0% 50%; transform: scaleX(0); z-index: 0; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(html)}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
'''
open(f"{proj}/compositions/captions.html", "w").write(out)
print(len(groups), "groups:", [" ".join(w["text"] for w in g) for g in groups])
