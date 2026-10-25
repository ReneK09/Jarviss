from shared import scene, planet

def orbit_svg(pid, size, r, color, circ):
    return (f'<svg id="{pid}" viewBox="0 0 {size} {size}">'
            f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="rgba(160,200,230,.28)" stroke-width="3" stroke-dasharray="10 12"/>'
            f'<circle id="{pid}-trail" cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="{color}" stroke-width="6" stroke-linecap="round" '
            f'stroke-dasharray="{circ}" stroke-dashoffset="{circ}" transform="translate({size},0) scale(-1,1) rotate(90 {size/2} {size/2})"/></svg>')

def race():
    p = "r"
    css = """
    #r-hud1 { left: 70px; width: 420px; }
    #r-pill { position: absolute; right: 70px; top: 238px; padding: 14px 22px; border-radius: 999px; font-weight: 800; font-size: 28px; letter-spacing: 0.12em;
      background: rgba(16, 30, 42, 0.82); border: 2px solid rgba(160, 200, 230, 0.18); color: #8fa5b5; white-space: nowrap; }
    #r-path { position: absolute; left: 310px; top: 410px; width: 460px; height: 460px; overflow: visible; }
    #r-sun { left: 470px; top: 570px; width: 140px; height: 140px; }
    #r-ring { position: absolute; left: -22px; top: -22px; width: 164px; height: 164px; overflow: visible; }
    .r-row { position: absolute; left: 70px; width: 940px; height: 60px; }
    .r-name { position: absolute; left: 0; top: 10px; font-weight: 900; font-size: 32px; letter-spacing: 0.08em; }
    .r-track { position: absolute; left: 250px; top: 16px; width: 520px; height: 28px; border-radius: 14px; background: rgba(255, 255, 255, 0.08); overflow: hidden; }
    .r-fill { position: absolute; left: 0; top: 0; height: 100%; width: 100%; border-radius: 14px; transform-origin: 0 50%; }
    .r-pct { position: absolute; right: 0; top: 4px; font-weight: 900; font-size: 44px; font-variant-numeric: tabular-nums; }
    #r-row1 { top: 1022px; } #r-row2 { top: 1096px; }
    #r-row1 .r-name, #r-row1 .r-pct { color: #ff6b5b; } #r-row1 .r-fill { background: #ff6b5b; }
    #r-row2 .r-name, #r-row2 .r-pct { color: #3dd6c6; } #r-row2 .r-fill { background: #3dd6c6; }
    .r-note { left: 0; width: 1080px; top: 962px; text-align: center; background: none; font-size: 38px; }
    #r-n1, #r-n3, #r-n4 { color: #3dd6c6; } #r-n2 { color: #ff6b5b; }
    """
    body = f"""
    <div id="r-stage" data-layout-allow-overflow>
      {orbit_svg("r-path", 460, 230, "#ff6b5b", 1445)}
      <div id="r-sun" class="r-sun"></div>
      <div id="r-vbox" style="position:absolute;left:480px;top:810px;width:120px;height:120px">
        <svg id="r-ring" viewBox="0 0 164 164"><circle id="r-ring-arc" cx="82" cy="82" r="76" fill="none" stroke="#3dd6c6" stroke-width="6" stroke-linecap="round"
          stroke-dasharray="477.5" stroke-dashoffset="477.5" transform="rotate(-90 82 82)"/></svg>
        {planet(p, "venus", "r-venus", 120, 0, 0)}
      </div>
      <div id="r-hud1" class="r-hud"><div class="r-hud-l">ZEIT · VENUS</div><div class="r-hud-v"><span id="r-d">0</span><small>Erdtage</small></div></div>
      <div id="r-pill">❚❚ PAUSE</div>
      <div id="r-row1" class="r-row"><div class="r-name">UMLAUF</div><div class="r-track"><div id="r-f1" class="r-fill"></div></div><div id="r-p1" class="r-pct">0 %</div></div>
      <div id="r-row2" class="r-row"><div class="r-name">DREHUNG</div><div class="r-track"><div id="r-f2" class="r-fill"></div></div><div id="r-p2" class="r-pct">0 %</div></div>
      <div id="r-n1" class="r-chip r-note">NICHT MAL HALB GEDREHT</div>
      <div id="r-n2" class="r-chip r-note">✓ 1 JAHR VORBEI</div>
      <div id="r-n3" class="r-chip r-note">DREHUNG: NOCH NICHT FERTIG</div>
      <div id="r-n4" class="r-chip r-note">✓ 1 DREHUNG = 243 TAGE</div>
    </div>"""
    js = """
      const DUR = 16.05, P = { t: 0 }, R = 230, CX = 540, CY = 640;
      const K = [[1.6, 0], [2.62, 100], [4.8, 100], [6.7, 225], [12.4, 225], [14.0, 243]];
      const runs = [[1.6, 2.62], [4.8, 6.7], [12.4, 14.0]];
      const dEl = document.getElementById("r-d"), p1 = document.getElementById("r-p1"), p2 = document.getElementById("r-p2"), pill = document.getElementById("r-pill");
      const render = (t) => {
        const d = keys(K, t);
        const a = 180 - 360 * d / 224.7, ar = a * Math.PI / 180;
        gsap.set("#r-vbox", { x: R * Math.sin(ar), y: -R * Math.cos(ar) - R });
        gsap.set("#r-venus-surf", { rotation: 270 + 360 * d / 243 });
        gsap.set("#r-venus-night", { rotation: a + 180 });
        const u = Math.min(1, d / 224.7), s = Math.min(1, d / 243);
        gsap.set("#r-path-trail", { strokeDashoffset: 1445 * (1 - u) });
        gsap.set("#r-ring-arc", { strokeDashoffset: 477.5 * (1 - s) });
        gsap.set("#r-f1", { scaleX: u }); gsap.set("#r-f2", { scaleX: s });
        dEl.textContent = Math.round(d);
        p1.textContent = Math.round(u * 100) + " %"; p2.textContent = Math.round(s * 100) + " %";
        const running = runs.some(([a0, a1]) => t > a0 && t < a1);
        pill.textContent = running ? "▶ ZEITRAFFER" : "❚❚ PAUSE";
        pill.style.color = running ? "#ffb648" : "#8fa5b5";
      };
      render(0);
      tl.fromTo(P, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => render(P.t) }, 0);
      tl.fromTo("#r-stage", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power2.out" }, 0);
      tl.fromTo(["#r-row1", "#r-row2"], { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.4, ease: "expo.out", stagger: 0.08 }, 0.9);
      const note = (id, a, b) => {
        tl.fromTo(id, { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }, a);
        tl.to(id, { opacity: 0, duration: 0.18, ease: "power2.in" }, b);
      };
      note("#r-n1", 4.36, 6.05);
      note("#r-n2", 9.21, 10.6);
      note("#r-n3", 11.31, 12.95);
      note("#r-n4", 14.1, 15.8);
      // the year finishing flashes the Umlauf row, the slow spin highlights Drehung
      tl.fromTo("#r-row1", { scale: 1 }, { scale: 1.04, duration: 0.12, ease: "power2.out" }, 6.7);
      tl.to("#r-row1", { scale: 1, duration: 0.3, ease: "expo.out" }, 6.82);
      tl.fromTo("#r-row2", { scale: 1 }, { scale: 1.04, duration: 0.12, ease: "power2.out" }, 10.67);
      tl.to("#r-row2", { scale: 1, duration: 0.3, ease: "expo.out" }, 10.79);
      tl.to("#r-stage", { opacity: 0, filter: "blur(10px)", duration: 0.22, ease: "power2.in" }, 15.83);
    """
    return scene(p, css, body, js)

def ja():
    p = "j"
    css = """
    #j-title { top: 330px; font-size: 140px; color: #3dd6c6; }
    .j-box { position: absolute; top: 600px; width: 380px; height: 250px; border-radius: 22px; background: rgba(16, 30, 42, 0.82); border: 2px solid rgba(160, 200, 230, 0.18); text-align: center; padding-top: 34px; }
    .j-box b { display: block; font-weight: 900; font-size: 110px; line-height: 1; font-variant-numeric: tabular-nums; }
    .j-box span { display: block; margin-top: 16px; font-weight: 700; font-size: 30px; letter-spacing: 0.14em; color: #8fa5b5; }
    #j-a { left: 70px; } #j-a b { color: #3dd6c6; }
    #j-b { left: 630px; } #j-b b { color: #ff6b5b; }
    #j-gt { position: absolute; left: 450px; top: 640px; width: 180px; text-align: center; font-weight: 900; font-size: 140px; color: #ffb648; line-height: 1; }
    """
    body = """
    <div id="j-stage">
      <div id="j-title" class="j-title">ALSO JA?</div>
      <div id="j-a" class="j-box"><b>243</b><span>TAGE DREHUNG</span></div>
      <div id="j-gt">&gt;</div>
      <div id="j-b" class="j-box"><b>225</b><span>TAGE = 1 JAHR</span></div>
    </div>"""
    js = """
      tl.fromTo("#j-title", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.18, ease: "power4.out" }, 0.05);
      tl.fromTo(["#j-a", "#j-b"], { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: "expo.out", stagger: 0.1 }, 0.9);
      tl.fromTo("#j-gt", { opacity: 0, scale: 2.5 }, { opacity: 1, scale: 1, duration: 0.35, ease: "expo.out" }, 1.9);
      // the claim cracks: a quick shake before "Aber Moment"
      tl.to("#j-stage", { keyframes: { x: [0, -14, 12, -8, 0] }, duration: 0.28, ease: "none" }, 2.62);
    """
    return scene(p, css, body, js)
