from shared import scene, planet

def hook():
    p = "h"
    css = """
    #h-lbl { top: 228px; }
    #h-title { top: 284px; font-size: 118px; }
    #h-title em { font-style: normal; color: #ffb648; }
    #h-poll { position: absolute; left: 0; top: 1040px; width: 1080px; height: 170px; }
    #h-ask { top: 0; font-size: 28px; }
    #h-ja { left: 170px; top: 62px; color: #3dd6c6; background: rgba(61, 214, 198, 0.14); border: 3px solid #3dd6c6; width: 230px; text-align: center; }
    #h-nein { left: 680px; top: 62px; color: #ff6b5b; background: rgba(255, 107, 91, 0.14); border: 3px solid #ff6b5b; width: 230px; text-align: center; }
    #h-count { position: absolute; left: 490px; top: 48px; width: 100px; height: 100px; }
    #h-count svg { position: absolute; inset: 0; overflow: visible; }
    #h-num { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 50px; font-variant-numeric: tabular-nums; }
    """
    body = f"""
    <div id="h-stage" data-layout-allow-overflow>
      {planet(p, "venus", "h-venus", 440, 320, 580)}
      <div id="h-lbl" class="h-label">EIN TAG AUF DER VENUS</div>
      <div id="h-title" class="h-title">LÄNGER ALS<br><em>EIN JAHR?</em></div>
      <div id="h-poll">
        <div id="h-ask" class="h-label">WAS MEINST DU?</div>
        <div id="h-ja" class="h-chip">JA</div>
        <div id="h-count"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="rgba(16,30,42,.9)" stroke="rgba(160,200,230,.25)" stroke-width="5"/>
          <circle id="h-arc" cx="50" cy="50" r="46" fill="none" stroke="#ffb648" stroke-width="6" stroke-linecap="round" stroke-dasharray="289" stroke-dashoffset="289" transform="rotate(-90 50 50)"/></svg>
          <div id="h-num">3</div></div>
        <div id="h-nein" class="h-chip">NEIN</div>
      </div>
    </div>"""
    js = """
      const DUR = 8.6, P = { t: 0 };
      const num = document.getElementById("h-num");
      const render = (t) => {
        gsap.set("#h-venus-surf", { rotation: 30 + t * 4 });
        gsap.set("#h-venus-night", { rotation: 135 });
        num.textContent = t < 6.6 ? "3" : t < 7.3 ? "2" : t < 8.0 ? "1" : "?";
      };
      render(0);
      tl.fromTo(P, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => render(P.t) }, 0);
      // poll on "Ja oder nein?"
      tl.fromTo("#h-poll", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }, 3.9);
      tl.fromTo("#h-arc", { strokeDashoffset: 289 }, { strokeDashoffset: 0, duration: 2.1, ease: "none" }, 5.9);
      tl.fromTo("#h-num", { scale: 1.5 }, { scale: 1, duration: 0.3, ease: "expo.out" }, 5.9);
      tl.fromTo("#h-num", { scale: 1.5 }, { scale: 1, duration: 0.3, ease: "expo.out", immediateRender: false }, 6.6);
      tl.fromTo("#h-num", { scale: 1.5 }, { scale: 1, duration: 0.3, ease: "expo.out", immediateRender: false }, 7.3);
      tl.to("#h-stage", { opacity: 0, filter: "blur(10px)", duration: 0.22, ease: "power2.in" }, 8.36);
    """
    return scene(p, css, body, js)

def earth():
    p = "e"
    css = """
    #e-hud1 { left: 70px; width: 400px; }
    #e-hud2 { right: 70px; width: 440px; }
    #e-path { position: absolute; left: 240px; top: 420px; width: 600px; height: 600px; overflow: visible; }
    #e-sunwrap { position: absolute; left: 465px; top: 645px; width: 150px; height: 150px; }
    #e-sun { left: 0; top: 0; width: 150px; height: 150px; }
    #e-chip1 { left: 0; width: 1080px; top: 1070px; text-align: center; background: none; color: #3dd6c6; font-size: 46px; }
    #e-chip2 { left: 0; width: 1080px; top: 1110px; text-align: center; background: none; color: #ff6b5b; font-size: 46px; }
    """
    body = f"""
    <div id="e-stage" data-layout-allow-overflow>
      <svg id="e-path" viewBox="0 0 600 600">
        <circle cx="300" cy="300" r="300" fill="none" stroke="rgba(160,200,230,.28)" stroke-width="3" stroke-dasharray="10 12"/>
        <circle id="e-trail" cx="300" cy="300" r="300" fill="none" stroke="#3dd6c6" stroke-width="6" stroke-linecap="round"
          stroke-dasharray="1885" stroke-dashoffset="1885" transform="translate(600,0) scale(-1,1) rotate(90 300 300)"/>
      </svg>
      <div id="e-sunwrap"><div id="e-sun" class="e-sun"></div></div>
      {planet(p, "earth", "e-earth", 520, 280, 500)}
      <div id="e-hud1" class="e-hud"><div class="e-hud-l">DREHUNG</div><div class="e-hud-v"><span id="e-h">0</span><small>Stunden</small></div></div>
      <div id="e-hud2" class="e-hud"><div class="e-hud-l">UMLAUF</div><div class="e-hud-v"><span id="e-d">0</span><small>Tage</small></div></div>
      <div id="e-chip1" class="e-chip">= 1 TAG</div>
      <div id="e-chip2" class="e-chip">= 1 JAHR</div>
    </div>"""
    js = """
      const DUR = 11.6, P = { t: 0 }, R = 300, CX = 540, CY = 720;
      const hEl = document.getElementById("e-h"), dEl = document.getElementById("e-d");
      const render = (t) => {
        const h = keys([[1.8, 0], [3.4, 24]], t);
        const d = keys([[7.3, 0], [9.67, 365]], t);
        const pull = keys([[6.3, 0], [7.1, 1]], t);
        const a = 180 - 360 * d / 365, ar = a * Math.PI / 180;
        const ox = CX + R * Math.sin(ar), oy = CY - R * Math.cos(ar);
        const x = lerp(540, ox, pull) - 540, y = lerp(760, oy, pull) - 760;
        gsap.set("#e-earth", { x: x, y: y, scale: lerp(1, 110 / 520, pull) });
        gsap.set("#e-earth-surf", { rotation: -360 * h / 24 - 360 * 12 * d / 365 });
        gsap.set("#e-earth-night", { rotation: lerp(-60, a + 180, pull) });
        gsap.set("#e-trail", { strokeDashoffset: 1885 * (1 - d / 365) });
        hEl.textContent = Math.round(h);
        dEl.textContent = Math.round(d);
      };
      render(0);
      tl.fromTo(P, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => render(P.t) }, 0);
      tl.fromTo("#e-stage", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power2.out" }, 0);
      tl.fromTo("#e-hud1", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, 1.4);
      tl.fromTo("#e-chip1", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.35, ease: "expo.out" }, 5.94);
      tl.to("#e-chip1", { opacity: 0, duration: 0.2, ease: "power2.in" }, 6.3);
      tl.fromTo(["#e-path", "#e-sunwrap"], { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.7, ease: "expo.out" }, 6.4);
      tl.fromTo("#e-hud2", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, 6.9);
      tl.fromTo("#e-chip2", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.35, ease: "expo.out" }, 10.76);
      tl.to("#e-stage", { opacity: 0, filter: "blur(10px)", duration: 0.22, ease: "power2.in" }, 11.36);
    """
    return scene(p, css, body, js)
