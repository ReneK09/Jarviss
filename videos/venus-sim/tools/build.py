import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from scenes_a import hook, earth
from scenes_b import race, ja
from scenes_c import twist, sunday, result
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFF = 0.3  # voice starts at 0.3 s on the root

SCENES = [("h", hook, 0, 8.6), ("e", earth, 8.6, 11.6), ("r", race, 20.2, 16.05), ("j", ja, 36.25, 2.95),
          ("w", twist, 39.2, 6.5), ("s", sunday, 45.7, 10.4), ("x", result, 56.1, 11.9)]
TOTAL = 68.0
for cid, fn, _, _ in SCENES:
    open(f"{ROOT}/compositions/{cid}.html", "w").write(fn())

# captions: 2-4 words, one line, numbers as amber digits
NUM = {"vierundzwanzig": "24", "dreihundertfünfundsechzig": "365", "hundert": "100", "zweihundertfünfundzwanzig": "225",
       "zweihundertdreiundvierzig": "243", "hundertsiebzehn": "117", "zwei": "2"}
words = json.load(open(f"{ROOT}/assets/words.json"))
groups, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    chars = sum(len(x["text"]) for x in cur)
    if w["text"][-1] in ".,?!:" or len(cur) == 4 or chars > 20 or not nxt or nxt["sent"] != w["sent"]:
        groups.append(cur); cur = []
html, js = [], []
for gi, g in enumerate(groups):
    start = g[0]["start"] + OFF - 0.04
    nxt = groups[gi + 1][0]["start"] + OFF - 0.06 if gi + 1 < len(groups) else TOTAL - 0.5
    end = min(g[-1]["end"] + OFF + 0.3, nxt)
    parts = []
    for w in g:
        core = w["text"].rstrip(".,?!:"); tail = w["text"][len(core):]
        if core.lower() in NUM:
            parts.append(f'<em>{NUM[core.lower()]}</em>{tail}')
        else:
            parts.append(w["text"])
    html.append(f'    <div class="cap" id="cap-{gi}"><span>{" ".join(parts)}</span></div>')
    js.append(f'      tl.set("#cap-{gi}", {{ visibility: "visible" }}, {start:.2f});')
    js.append(f'      tl.fromTo("#cap-{gi}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, ease: "none" }}, {start:.2f});')
    js.append(f'      tl.to("#cap-{gi}", {{ opacity: 0, duration: 0.08, ease: "none" }}, {end - 0.08:.2f});')
    js.append(f'      tl.set("#cap-{gi}", {{ opacity: 0, visibility: "hidden" }}, {end:.2f});')
open(f"{ROOT}/compositions/captions.html", "w").write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cap {{ position: absolute; left: 0; width: 100%; top: 1206px; text-align: center; opacity: 0; visibility: hidden; }}
    .cap span {{ display: inline-block; padding: 12px 22px 14px; border-radius: 12px; background: rgba(8, 16, 24, 0.8);
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 42px; line-height: 1.1; color: #ffffff; white-space: nowrap; }}
    .cap em {{ font-style: normal; color: #ffb648; }}
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
''')

hosts = "\n".join(
    f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{s}" data-duration="{d}" '
    f'data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 2"></div>'
    for cid, _, s, d in SCENES)
sfx = json.load(open(f"{ROOT}/tools/sfx.json"))
audio = "\n".join(
    f'      <audio id="{a["id"]}" class="clip" src="assets/sfx/{a["f"]}" data-start="{a["s"]}" data-duration="{a["d"]}"'
    + (f' data-media-start="{a["ms"]}"' if a.get("ms") else "") + f' data-track-index="{(8 if a["id"] == "sfx-riser" else 5 + i % 3)}" data-volume="{a["v"]}"></audio>'
    for i, a in enumerate(sfx))
music = os.path.exists(f"{ROOT}/assets/bgm/track.wav")
open(f"{ROOT}/index.html", "w").write(f'''<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0d1822; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      #bg {{ position: absolute; inset: 0; background-color: #0d1822;
        background-image: linear-gradient(rgba(160, 200, 230, 0.04) 2px, transparent 2px), linear-gradient(90deg, rgba(160, 200, 230, 0.04) 2px, transparent 2px);
        background-size: 48px 48px; }}
      #stars {{ position: absolute; inset: 0; background: url("assets/stars.svg") no-repeat; background-size: 1080px 1920px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="bg" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="0" style="z-index: 1"></div>
      <div id="stars" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="0" style="z-index: 1"></div>
{hosts}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}"
        data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 5"></div>
      <audio id="voice" class="clip" src="assets/voice.wav" data-start="{OFF}" data-duration="64.6" data-track-index="3" data-volume="1"></audio>
''' + (f'      <audio id="music" class="clip" src="assets/bgm/track.wav" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-volume="0.15"></audio>\n' if music else "") + f'''{audio}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
''')
print("built", len(groups), "caption groups, music:", music)
