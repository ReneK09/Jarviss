from shared import scene, planet
from scenes_b import orbit_svg

ARROW = lambda pid, color, cw: (
    f'<svg id="{pid}" viewBox="0 0 400 400" style="position:absolute;overflow:visible">'
    + (f'<path d="M 200 14 A 186 186 0 0 1 386 200" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round"/>'
       f'<path d="M 362 176 L 386 212 L 410 176" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
       if cw else
       f'<path d="M 200 14 A 186 186 0 0 0 14 200" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round"/>'
       f'<path d="M -10 176 L 14 212 L 38 176" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')
    + '</svg>')

def twist():
    p = "w"
    css = """
    #w-a { position: absolute; inset: 0; }
    #w-aber { top: 640px; font-size: 64px; color: #8fa5b5; }
    #w-moment { top: 715px; font-size: 150px; color: #ffb648; }
    #w-b { position: absolute; inset: 0; }
    #w-b-lbl { top: 228px; }
    #w-back { top: 290px; font-size: 128px; color: #ff6b5b; }
    #w-arr-e { left: 140px; top: 610px; width: 300px; height: 300px; }
    #w-arr-v { left: 640px; top: 610px; width: 300px; height: 300px; }
    .w-name { position: absolute; top: 960px; width: 400px; text-align: center; font-weight: 900; font-size: 40px; letter-spacing: 0.08em; }
    #w-name-e { left: 90px; color: #3dd6c6; } #w-name-v { left: 590px; color: #ff6b5b; }
    #w-c { position: absolute; inset: 0; }
    #w-sky { position: absolute; left: 0; top: 0; width: 1080px; height: 1000px; background: linear-gradient(to bottom, rgba(13, 24, 34, 0) 40%, rgba(240, 138, 36, 0.28) 100%); }
    #w-sun { left: 130px; top: 1000px; width: 200px; height: 200px; }
    #w-ground { position: absolute; left: 0; top: 1000px; width: 1080px; height: 920px; background: #3b2618; border-top: 3px solid #a8683a; }
    .w-dir { position: absolute; top: 1030px; font-weight: 900; font-size: 56px; line-height: 1; }
    #w-dir-w { left: 212px; color: #ffb648; } #w-dir-o { left: 828px; color: rgba(234, 242, 248, 0.6); }
    #w-c-lbl { top: 228px; }
    #w-west { top: 290px; font-size: 150px; color: #ffb648; }
    """
    body = f"""
    <div id="w-a"><div id="w-aber" class="w-title">ABER</div><div id="w-moment" class="w-title">MOMENT.</div></div>
    <div id="w-b" data-layout-allow-overflow>
      <div id="w-b-lbl" class="w-label">DIE VENUS DREHT SICH</div>
      <div id="w-back" class="w-title">RÜCKWÄRTS</div>
      {ARROW("w-arr-e", "#3dd6c6", False)}
      {ARROW("w-arr-v", "#ff6b5b", True)}
      {planet(p, "earth", "w-earth", 250, 165, 635)}
      {planet(p, "venus", "w-venus", 250, 665, 635)}
      <div id="w-name-e" class="w-name">ERDE ↺</div>
      <div id="w-name-v" class="w-name">VENUS ↻</div>
    </div>
    <div id="w-c" data-layout-allow-overflow>
      <div id="w-sky"></div>
      <div id="w-sun" class="w-sun"></div>
      <div id="w-ground"></div>
      <div id="w-dir-w" class="w-dir">W</div>
      <div id="w-dir-o" class="w-dir">O</div>
      <div id="w-c-lbl" class="w-label">DIE SONNE GEHT AUF IM</div>
      <div id="w-west" class="w-title">WESTEN</div>
    </div>"""
    js = """
      const DUR = 6.5, P = { t: 0 };
      const render = (t) => {
        gsap.set("#w-earth-surf", { rotation: -t * 140 });
        gsap.set("#w-venus-surf", { rotation: t * 60 });
        gsap.set("#w-earth-night", { rotation: -90 }); gsap.set("#w-venus-night", { rotation: -90 });
      };
      render(0);
      tl.fromTo(P, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => render(P.t) }, 0);
      // A: "Aber Moment." slams in
      tl.fromTo("#w-aber", { opacity: 0 }, { opacity: 1, duration: 0.12, ease: "power2.out" }, 0.05);
      tl.fromTo("#w-moment", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }, 0.33);
      tl.to("#w-a", { opacity: 0, filter: "blur(10px)", duration: 0.18, ease: "power2.in" }, 0.8);
      // B: spin directions
      tl.fromTo("#w-b", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.out" }, 0.95);
      tl.fromTo("#w-back", { opacity: 0, x: 140, filter: "blur(10px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }, 2.05);
      tl.fromTo("#w-arr-e", { rotation: 0 }, { rotation: -150, duration: 3.3, ease: "none" }, 0.95);
      tl.fromTo("#w-arr-v", { rotation: 0 }, { rotation: 150, duration: 3.3, ease: "none" }, 0.95);
      tl.to("#w-b", { opacity: 0, filter: "blur(10px)", duration: 0.2, ease: "power2.in" }, 4.1);
      // C: sunrise in the west
      tl.fromTo("#w-c", { opacity: 0 }, { opacity: 1, duration: 0.25, ease: "power2.out" }, 4.25);
      tl.fromTo("#w-c-lbl", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.out" }, 4.4);
      tl.fromTo("#w-sun", { y: 0 }, { y: -300, duration: 1.3, ease: "power2.out" }, 5.0);
      tl.fromTo("#w-sky", { opacity: 0 }, { opacity: 1, duration: 1.3, ease: "power2.out" }, 5.0);
      tl.fromTo("#w-west", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.35, ease: "expo.out" }, 5.8);
      tl.fromTo("#w-dir-w", { scale: 1 }, { scale: 1.4, duration: 0.12, ease: "power2.out" }, 5.8);
      tl.to("#w-dir-w", { scale: 1, duration: 0.3, ease: "expo.out" }, 5.92);
      tl.to("#w-c", { opacity: 0, filter: "blur(10px)", duration: 0.2, ease: "power2.in" }, 6.3);
    """
    return scene(p, css, body, js)

def sunday():
    p = "s"
    css = """
    #s-hud1 { left: 70px; width: 430px; }
    #s-hud2 { right: 70px; width: 440px; }
    #s-path { position: absolute; left: 320px; top: 420px; width: 440px; height: 440px; overflow: visible; }
    #s-sun { left: 470px; top: 570px; width: 140px; height: 140px; }
    #s-ray { position: absolute; left: 540px; top: 640px; width: 0; height: 0; }
    #s-ray i { position: absolute; left: -2px; top: 0; width: 4px; height: 220px; background: linear-gradient(to bottom, rgba(255, 182, 72, 0.7), rgba(255, 182, 72, 0)); }
    .s-tag { position: absolute; top: 960px; width: 540px; text-align: center; font-weight: 900; font-size: 38px; letter-spacing: 0.06em; }
    #s-tag1 { left: 0; color: #3dd6c6; } #s-tag2 { left: 540px; color: #ff6b5b; }
    #s-vs { position: absolute; left: 490px; top: 952px; width: 100px; text-align: center; font-weight: 900; font-size: 46px; color: #ffb648; }
    #s-line { position: absolute; left: 90px; top: 960px; width: 900px; height: 200px; }
    #s-line-lbl { position: absolute; left: 0; top: 0; font-weight: 700; font-size: 28px; letter-spacing: 0.12em; color: #8fa5b5; }
    #s-track { position: absolute; left: 0; top: 92px; width: 900px; height: 18px; border-radius: 9px; background: rgba(255, 107, 91, 0.35); }
    #s-track-f { position: absolute; inset: 0; border-radius: 9px; background: #ff6b5b; transform-origin: 0 50%; }
    .s-mk { position: absolute; top: 48px; width: 34px; height: 34px; margin-left: -17px; border-radius: 50%; background: #ffb648; box-shadow: 0 0 18px rgba(255, 182, 72, 0.6); }
    .s-mk::after { content: ""; position: absolute; left: 15px; top: 34px; width: 4px; height: 12px; background: #ffb648; }
    #s-mk1 { left: 0; } #s-mk2 { left: 468px; }
    #s-two { position: absolute; left: 0; width: 900px; top: 130px; text-align: center; font-weight: 900; font-size: 40px; color: #ffb648; }
    """
    body = f"""
    <div id="s-stage" data-layout-allow-overflow>
      {orbit_svg("s-path", 440, 220, "#ff6b5b", 1382)}
      <div id="s-ray"><i></i></div>
      <div id="s-sun" class="s-sun"></div>
      <div id="s-vbox" style="position:absolute;left:460px;top:780px;width:160px;height:160px">{planet(p, "venus", "s-venus", 160, 0, 0)}</div>
      <div id="s-hud1" class="s-hud"><div class="s-hud-l">SONNENTAG</div><div class="s-hud-v"><span id="s-d">0</span><small>Erdtage</small></div></div>
      <div id="s-hud2" class="s-hud"><div class="s-hud-l">SONNENAUFGÄNGE</div><div class="s-hud-v"><span id="s-n">0</span></div></div>
      <div id="s-tag1" class="s-tag">DREHUNG ↻</div>
      <div id="s-vs">⇄</div>
      <div id="s-tag2" class="s-tag">UMLAUF ↺</div>
      <div id="s-line">
        <div id="s-line-lbl">1 VENUS-JAHR = 225 TAGE</div>
        <div id="s-mk1" class="s-mk"></div><div id="s-mk2" class="s-mk"></div>
        <div id="s-track"><div id="s-track-f"></div></div>
        <div id="s-two">≈ 2 SONNENAUFGÄNGE PRO JAHR</div>
      </div>
    </div>"""
    js = """
      const DUR = 10.4, P = { t: 0 }, R = 220;
      const K = [[2.0, 0], [7.6, 116.75]];
      const dEl = document.getElementById("s-d"), nEl = document.getElementById("s-n");
      const pin = () => document.querySelector("#s-venus .s-pin");
      const render = (t) => {
        const d = keys(K, t);
        const a = 180 - 360 * d / 224.7, ar = a * Math.PI / 180;
        gsap.set("#s-vbox", { x: R * Math.sin(ar), y: -R * Math.cos(ar) - R });
        gsap.set("#s-ray", { rotation: a + 180 });
        // the observer pin starts exactly on the sunrise line (a + 90) and turns clockwise
        const b = 270 + 360 * d / 243;
        gsap.set("#s-venus-surf", { rotation: b });
        gsap.set("#s-venus-night", { rotation: a + 180 });
        gsap.set("#s-path-trail", { strokeDashoffset: 1382 * (1 - d / 224.7) });
        let diff = ((b - (a + 180)) % 360 + 540) % 360 - 180;
        const lit = Math.abs(diff) <= 90.5 && t >= 2.0;
        const el = pin(); if (el) el.style.background = lit ? "#ffb648" : "#ffffff";
        dEl.textContent = Math.round(d);
        nEl.textContent = t < 2.0 ? 0 : d >= 116.7 ? 2 : 1;
      };
      render(0);
      tl.fromTo(P, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => render(P.t) }, 0);
      tl.fromTo("#s-stage", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power2.out" }, 0);
      tl.fromTo("#s-tag1", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }, 0.54);
      tl.fromTo("#s-tag2", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }, 1.17);
      tl.fromTo("#s-vs", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }, 1.54);
      tl.fromTo("#s-hud2", { scale: 1 }, { scale: 1.06, duration: 0.12, ease: "power2.out" }, 2.0);
      tl.to("#s-hud2", { scale: 1, duration: 0.3, ease: "expo.out" }, 2.12);
      tl.fromTo("#s-hud2", { scale: 1 }, { scale: 1.06, duration: 0.12, ease: "power2.out", immediateRender: false }, 7.6);
      tl.to("#s-hud2", { scale: 1, duration: 0.3, ease: "expo.out" }, 7.72);
      tl.to(["#s-tag1", "#s-tag2", "#s-vs"], { opacity: 0, duration: 0.2, ease: "power2.in" }, 7.9);
      tl.fromTo("#s-line", { opacity: 0 }, { opacity: 1, duration: 0.25, ease: "power2.out" }, 8.15);
      tl.fromTo("#s-track-f", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power2.out" }, 8.2);
      tl.fromTo("#s-mk1", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }, 8.3);
      tl.fromTo("#s-mk2", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }, 8.6);
      tl.fromTo("#s-two", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }, 8.88);
      tl.to("#s-stage", { opacity: 0, filter: "blur(10px)", duration: 0.22, ease: "power2.in" }, 10.15);
    """
    return scene(p, css, body, js)

def result():
    p = "x"
    css = """
    #x-lbl { top: 228px; }
    .x-row { position: absolute; left: 90px; width: 900px; height: 110px; }
    .x-name { font-weight: 900; font-size: 32px; letter-spacing: 0.08em; }
    .x-bar { position: absolute; left: 0; top: 46px; height: 56px; border-radius: 12px; transform-origin: 0 50%; }
    .x-val { position: absolute; top: 50px; font-weight: 900; font-size: 44px; font-variant-numeric: tabular-nums; white-space: nowrap; }
    #x-r1 { top: 300px; } #x-r1 .x-name, #x-r1 .x-val { color: #3dd6c6; } #x-r1 .x-bar { background: #3dd6c6; width: 700px; } #x-r1 .x-val { left: 720px; }
    #x-r2 { top: 440px; } #x-r2 .x-name, #x-r2 .x-val { color: #ff6b5b; } #x-r2 .x-bar { background: #ff6b5b; width: 648px; } #x-r2 .x-val { left: 668px; }
    #x-r3 { top: 580px; } #x-r3 .x-name, #x-r3 .x-val { color: #ffb648; } #x-r3 .x-bar { background: #ffb648; width: 337px; } #x-r3 .x-val { left: 357px; }
    #x-q { top: 790px; font-size: 96px; }
    #x-end1 { top: 790px; font-size: 100px; color: #ffb648; white-space: nowrap; }
    #x-end2 { top: 930px; font-size: 64px; }
    """
    body = """
    <div id="x-lbl" class="x-label">VENUS · IN ERDTAGEN</div>
    <div id="x-r1" class="x-row"><div class="x-name">1 DREHUNG</div><div class="x-bar"></div><div class="x-val">243 Tage</div></div>
    <div id="x-r2" class="x-row"><div class="x-name">1 JAHR</div><div class="x-bar"></div><div class="x-val">225 Tage</div></div>
    <div id="x-r3" class="x-row"><div class="x-name">1 SONNENTAG</div><div class="x-bar"></div><div class="x-val">117 Tage</div></div>
    <div id="x-q" class="x-title">TAG &gt; JAHR?</div>
    <div id="x-end1" class="x-title">KOMMT DRAUF AN,</div>
    <div id="x-end2" class="x-title">wie man zählt.</div>"""
    js = """
      tl.fromTo("#x-lbl", { opacity: 0 }, { opacity: 1, duration: 0.25, ease: "power2.out" }, 0.1);
      [["#x-r1", 1.1], ["#x-r2", 2.1], ["#x-r3", 2.96]].forEach(([id, at]) => {
        tl.fromTo(id, { opacity: 0 }, { opacity: 1, duration: 0.15, ease: "power2.out" }, at);
        tl.fromTo(id + " .x-bar", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "expo.out" }, at);
        tl.fromTo(id + " .x-val", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.4, ease: "expo.out" }, at + 0.35);
      });
      tl.fromTo("#x-q", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.18, ease: "power4.out" }, 4.28);
      tl.to("#x-q", { opacity: 0, filter: "blur(8px)", duration: 0.18, ease: "power2.in" }, 6.8);
      tl.fromTo("#x-end1", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "expo.out" }, 6.99);
      tl.fromTo("#x-end2", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.18, ease: "power4.out" }, 7.8);
    """
    return scene(p, css, body, js)
