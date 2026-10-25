# Shared look for every scene: tokens, HUD panels, planets, chips.
# Each scene gets its own prefixed copy so ids/classes stay unique in the assembled page.
def css(p):
    return f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: "Inter", sans-serif; color: #eaf2f8; }}
    .{p}-hud {{ position: absolute; top: 200px; height: 128px; padding: 18px 26px; border-radius: 18px;
      background: rgba(16, 30, 42, 0.82); border: 2px solid rgba(160, 200, 230, 0.18); }}
    .{p}-hud-l {{ font-weight: 700; font-size: 28px; letter-spacing: 0.12em; color: #8fa5b5; line-height: 1; }}
    .{p}-hud-v {{ margin-top: 12px; font-weight: 900; font-size: 64px; line-height: 1; font-variant-numeric: tabular-nums; white-space: nowrap; }}
    .{p}-hud-v small {{ font-size: 30px; font-weight: 700; color: #8fa5b5; margin-left: 8px; }}
    .{p}-title {{ position: absolute; left: 0; width: 100%; text-align: center; font-weight: 900; line-height: 0.98; letter-spacing: -0.01em; }}
    .{p}-label {{ position: absolute; left: 0; width: 100%; text-align: center; font-weight: 700; font-size: 32px; letter-spacing: 0.14em; color: #8fa5b5; }}
    .{p}-chip {{ position: absolute; padding: 12px 24px; border-radius: 999px; font-weight: 900; font-size: 34px; letter-spacing: 0.04em; white-space: nowrap; line-height: 1; }}
    .{p}-sun {{ position: absolute; border-radius: 50%;
      background: radial-gradient(circle at 40% 38%, #ffe6a8 0%, #ffb648 48%, #f08a24 100%);
      box-shadow: 0 0 50px 8px rgba(255, 170, 60, 0.35), 0 0 140px 40px rgba(255, 150, 40, 0.12); }}
    .{p}-planet {{ position: absolute; border-radius: 50%; }}
    .{p}-surf {{ position: absolute; inset: 0; border-radius: 50%; overflow: visible; }}
    .{p}-surf-fill {{ position: absolute; inset: 0; border-radius: 50%; overflow: hidden; }}
    .{p}-venus .{p}-surf-fill {{ background: repeating-linear-gradient(-14deg, #e9b46c 0 11%, #d39448 11% 19%, #efc584 19% 30%, #dca159 30% 37%); }}
    .{p}-earth .{p}-surf-fill {{ background: #2a7fd0; }}
    .{p}-earth .{p}-surf-fill svg {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    .{p}-pin {{ position: absolute; left: 50%; top: -6%; width: 7%; height: 17%; margin-left: -3.5%; border-radius: 999px; background: #ffffff;
      box-shadow: 0 0 0 4px rgba(13, 24, 34, 0.55); }}
    .{p}-night {{ position: absolute; inset: 0; border-radius: 50%;
      background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 50%, rgba(6, 12, 22, 0.66) 50%); }}
    .{p}-rim {{ position: absolute; inset: 0; border-radius: 50%; box-shadow: inset 0 0 0 3px rgba(255, 255, 255, 0.10); }}
    """

EARTH_LAND = ('<svg viewBox="0 0 100 100" preserveAspectRatio="none">'
    '<path d="M18 22 C28 12 44 14 46 26 C48 36 38 40 40 52 C42 62 30 66 24 58 C18 50 10 44 12 34 Z" fill="#4cb86a"/>'
    '<path d="M60 18 C70 14 84 22 86 34 C88 44 78 46 72 42 C66 38 58 30 60 18 Z" fill="#4cb86a"/>'
    '<path d="M58 58 C66 52 78 56 80 66 C82 78 70 88 62 84 C56 80 52 66 58 58 Z" fill="#4cb86a"/>'
    '<path d="M20 74 C26 70 34 74 32 82 C30 88 22 88 20 82 Z" fill="#4cb86a"/>'
    '<ellipse cx="50" cy="4" rx="30" ry="6" fill="#e8f2fa"/><ellipse cx="50" cy="97" rx="30" ry="6" fill="#e8f2fa"/></svg>')

def planet(p, kind, pid, size, left, top, night=True, pin=True):
    """A planet: outer box (positioned), rotating surface with pin, fixed night overlay."""
    land = EARTH_LAND if kind == "earth" else ""
    return (f'<div id="{pid}" class="{p}-planet {p}-{kind}" style="left:{left}px;top:{top}px;width:{size}px;height:{size}px">'
            f'<div id="{pid}-surf" class="{p}-surf"><div class="{p}-surf-fill">{land}</div>'
            + (f'<div class="{p}-pin"></div>' if pin else "") + '</div>'
            + (f'<div id="{pid}-night" class="{p}-night"></div>' if night else "")
            + f'<div class="{p}-rim"></div></div>')

def scene(cid, css_extra, body, script):
    return f"""<template>
  <style>{css(cid)}{css_extra}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const lerp = (a, b, u) => a + (b - a) * u;
      const clamp = (u) => Math.max(0, Math.min(1, u));
      const sm = (u) => {{ u = clamp(u); return u * u * (3 - 2 * u); }};
      // piecewise keyframes [[t, v], ...] with smoothstep between keys
      const keys = (k, t) => {{
        if (t <= k[0][0]) return k[0][1];
        for (let i = 1; i < k.length; i++) if (t <= k[i][0]) return lerp(k[i - 1][1], k[i][1], sm((t - k[i - 1][0]) / (k[i][0] - k[i - 1][0])));
        return k[k.length - 1][1];
      }};
{script}
      window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
"""
