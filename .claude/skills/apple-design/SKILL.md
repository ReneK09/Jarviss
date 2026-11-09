---
name: apple-design
description: Gestaltet Oberflächen im Stil von Apple (Human Interface Guidelines, iOS/macOS/visionOS-Ästhetik). Verwenden, wann immer eine neue Idee, Seite, App, Komponente oder ein Redesign umgesetzt wird – auch ohne dass "Apple" erwähnt wird, sofern der Nutzer nichts anderes vorgibt. Triggers: "Apple-Look", "wie iOS", "clean", "minimalistisch", "neue Idee umsetzen", "UI bauen", "Design", "App", "Seite", "Redesign".
---

# Apple Design

Ziel: Jede Oberfläche soll sich anfühlen, als käme sie von Apple – ruhig, klar,
präzise, mit Tiefe statt Dekoration. Drei Prinzipien der HIG leiten alles:

1. **Clarity** – Inhalt ist König. Text ist in jeder Größe lesbar, Icons sind eindeutig, nichts Überflüssiges.
2. **Deference** – Die UI tritt hinter den Inhalt zurück. Transluzenz, Weißraum, dezente Farben.
3. **Depth** – Ebenen, Bewegung und Materialien vermitteln Hierarchie und Orientierung.

## Arbeitsweise

1. Verstehe zuerst die Idee: Was ist die *eine* Hauptaufgabe des Screens? Diese bekommt die prominenteste Stelle.
2. Baue mit den Tokens unten – keine freien Farb-/Abstandswerte erfinden.
3. Light **und** Dark Mode immer mitliefern.
4. Prüfe am Ende die Checkliste (unten) und behebe Abweichungen, bevor du fertig meldest.
5. Bestehende Designs im Repo (z. B. der J.A.R.V.I.S.-HUD-Stil in `index.html`) nur umstellen, wenn der Nutzer das will. Bei Erweiterungen bestehender Seiten: Apple-Prinzipien (Abstände, Typo-Hierarchie, Bewegung) anwenden, aber die vorhandene Markenfarbe beibehalten.

## Typografie

```css
font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display",
             "Inter", "Helvetica Neue", Arial, sans-serif;
font-feature-settings: "kern"; -webkit-font-smoothing: antialiased;
```
Monospace: `ui-monospace, "SF Mono", Menlo, monospace`. Rund: `ui-rounded, "SF Pro Rounded", system-ui`.

Textstile (iOS Dynamic Type, Standardgröße):

| Stil | Größe / Zeilenhöhe | Gewicht |
|---|---|---|
| Large Title | 34 / 41 px | 700 |
| Title 1 | 28 / 34 | 700 |
| Title 2 | 22 / 28 | 700 |
| Title 3 | 20 / 25 | 600 |
| Headline | 17 / 22 | 600 |
| Body | 17 / 22 | 400 |
| Callout | 16 / 21 | 400 |
| Subheadline | 15 / 20 | 400 |
| Footnote | 13 / 18 | 400 |
| Caption | 12 / 16 | 400 |

- Große Titel: `letter-spacing: -0.02em`; Body: `-0.01em`.
- Marketing-Hero (apple.com-Stil): 48–80 px, Gewicht 600–700, enge Laufweite, kurzer Satz.
- Hierarchie über Gewicht und Graustufen, nicht über viele Farben.
- Höchstens 2–3 Schriftgrößen pro Bereich.

## Farben (Systemfarben)

```css
:root{
  --bg: #ffffff;             --bg-grouped: #f2f2f7;
  --bg-elevated: #ffffff;    --bg-secondary: #f2f2f7;
  --label: #000000;          --label-2: rgba(60,60,67,.6);
  --label-3: rgba(60,60,67,.3);
  --separator: rgba(60,60,67,.29);
  --fill: rgba(120,120,128,.2);
  --blue:#007aff; --green:#34c759; --red:#ff3b30; --orange:#ff9500;
  --yellow:#ffcc00; --teal:#30b0c7; --indigo:#5856d6; --purple:#af52de; --pink:#ff2d55;
  --accent: var(--blue);
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#000000;            --bg-grouped:#000000;
    --bg-elevated:#1c1c1e;   --bg-secondary:#2c2c2e;
    --label:#ffffff;         --label-2: rgba(235,235,245,.6);
    --label-3: rgba(235,235,245,.3);
    --separator: rgba(84,84,88,.6);
    --fill: rgba(120,120,128,.36);
    --blue:#0a84ff; --green:#30d158; --red:#ff453a; --orange:#ff9f0a;
    --yellow:#ffd60a; --teal:#40c8e0; --indigo:#5e5ce6; --purple:#bf5af2; --pink:#ff375f;
  }
}
```
- **Eine** Akzentfarbe pro App (Tint). Rot nur für destruktive Aktionen, Grün für Erfolg.
- Kontrast mind. 4.5:1 für Text (WCAG AA).

## Layout & Abstände

- 8-pt-Raster: 4, 8, 12, 16, 20, 24, 32, 44, 64.
- Seitenränder: 16 px (Phone), 20 px (größer), Content max. ~980–1080 px breit, zentriert.
- Touch-Ziele mind. **44 × 44 px**.
- Grouped Lists (Inset): Hintergrund `--bg-grouped`, Karten `--bg-elevated`, Radius 10–12 px, Zellen 44 px hoch, Trennlinien 0.5 px eingerückt ab Textbeginn.
- Viel Weißraum. Im Zweifel mehr Abstand, weniger Elemente.
- Safe Areas beachten: `padding: env(safe-area-inset-top) …`.

## Formen, Materialien, Tiefe

- Eckenradien: Buttons 10–12 px (oder Kapsel `999px`), Karten 16–22 px, Sheets 10 px oben. Verschachtelt: innerer Radius = äußerer − Abstand.
- Materialien (Glas):
  ```css
  background: rgba(255,255,255,.72);            /* dark: rgba(30,30,30,.72) */
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border: 0.5px solid rgba(0,0,0,.08);           /* dark: rgba(255,255,255,.12) */
  ```
  Für Navigationsleisten, Tab Bars, Toolbars, Popovers, schwebende Panels („Liquid Glass“-Anmutung: zusätzlich ein feiner innerer Lichtrand `box-shadow: inset 0 1px 0 rgba(255,255,255,.4)`).
- Schatten weich und groß, nie hart: `0 8px 30px rgba(0,0,0,.12)`; im Dark Mode stattdessen hellere Fläche.

## Komponenten

- **Nav Bar**: Glas, 44 px hoch; Large Title darunter, der beim Scrollen in den kleinen Titel übergeht.
- **Tab Bar**: unten, 3–5 Tabs, Icon + Label (10 px), aktive Farbe = Akzent.
- **Buttons**: Filled (Akzent-Hintergrund, weißer Text, 600), Tinted (Akzent 15 % Deckkraft), Plain (nur Akzent-Text). Gedrückt: `opacity:.7` oder `scale(.97)`.
- **Switch**: 51 × 31 px, grün `--green` wenn an.
- **Segmented Control**: `--fill`-Hintergrund, aktives Segment weiß/erhöht mit leichtem Schatten.
- **Sheets/Modals**: von unten, Grabber (36 × 5 px, Radius 3), abgedunkelter Hintergrund `rgba(0,0,0,.4)`.
- **Suchfeld**: `--fill`-Hintergrund, Radius 10, Lupen-Icon, Platzhalter `--label-2`.
- **Icons**: SF-Symbols-Anmutung – Linien, gleichmäßige Strichstärke, an Textgewicht angepasst. Im Web: inline SVG mit `stroke-width:1.75`, `stroke-linecap:round`, oder Lucide-Icons. Keine Emoji als UI-Icons.

## Bewegung

- Federnd und physikalisch: `cubic-bezier(.32,.72,0,1)` für Sheets/Übergänge (350–500 ms), `cubic-bezier(.25,.1,.25,1)` für Kleines (200–250 ms).
- Animation erklärt Ursache und Wirkung (wo kommt etwas her, wo geht es hin) – nie Selbstzweck.
- `@media (prefers-reduced-motion: reduce)` → Bewegungen durch Überblendungen ersetzen.

## Sprache & Inhalt

- Kurz, freundlich, direkt. Verben auf Buttons („Sichern“, „Weiter“), keine „OK/Abbrechen“-Ratespiele.
- Titel in Satzschreibung. Keine Ausrufezeichen-Flut, kein Fachjargon.

## Barrierefreiheit

- Semantisches HTML, `aria-label` für Icon-Buttons, sichtbarer Fokusring (`outline: 3px solid color-mix(in srgb, var(--accent) 50%, transparent)`).
- Text skalierbar (rem), nichts bricht bei 200 % Zoom.
- Farbe nie als einziger Informationsträger.

## Abschluss-Checkliste

- [ ] Eine klare Hauptaktion pro Screen
- [ ] Nur System-Schrift + Tokens oben verwendet
- [ ] Light & Dark Mode funktionieren
- [ ] Touch-Ziele ≥ 44 px, 8-pt-Abstände
- [ ] Glas nur für schwebende/Navigations-Ebenen, Inhalt bleibt ruhig
- [ ] Mobile (375 px) ohne horizontales Scrollen
- [ ] Reduced Motion & Fokuszustände bedacht

*Hinweis: Apple-Logos, SF-Pro-Schriftdateien und Original-Apple-Icons nicht einbetten oder nachbauen – nur die Gestaltungsprinzipien übernehmen.*
