# ⚽ Fußball – Liquid Glass

Eine Fußball-Web-App im Stil von Apples *Liquid Glass*: alle großen Ligen, Tabellen, Teams, Kader und Spiele, live und ohne API-Key.

## Starten

Es ist eine einzige Datei, es muss nichts gebaut werden:

```bash
cd football
python3 -m http.server 8000
# → http://localhost:8000
```

Oder einfach über GitHub Pages bzw. jeden anderen statischen Host ausliefern. Auf dem iPhone in Safari öffnen, dann über **Teilen → Zum Home-Bildschirm** wie eine native App nutzen.

## Funktionen

| Bereich | Inhalt |
|---|---|
| **Ligen** | Bundesliga, 2. Bundesliga, DFB-Pokal, Premier League, LaLiga, Serie A, Ligue 1, Champions/Europa/Conference League, Eredivisie, Primeira Liga, Süper Lig, Österreich, Schweiz, Schottland, Belgien, MLS |
| **Liga** | Tabelle mit Europapokal- und Abstiegszonen, Spieltage mit Datumsauswahl, alle Teams |
| **Team** | Platzierung und Bilanz, nächste Spiele, Ergebnisse, Kader nach Positionen, Spielerprofil als Sheet |
| **Spiel** | Ergebnis, Verlauf (Tore, Karten, Wechsel), Statistik-Balken, Aufstellungen mit Formation; aktualisiert sich bei Live-Spielen alle 30 s |
| **Spiele** | Alle Ligen für einen Tag (−4 bis +4 Tage), Live-Zähler, deine Favoriten zuerst |
| **Suche** | Teams (deutsch oder englisch) und Ligen |
| **Favoriten** | Teams mit ★ markieren (wird lokal im Browser gespeichert) |

## Design

- Glasflächen aus `backdrop-filter: blur() saturate()`, einem spiegelnden Verlaufsrand und einem inneren Glanz
- Farbige, langsam treibende Lichtflächen im Hintergrund, die die Glasflächen brechen. Sie färben sich in den Vereinsfarben des geöffneten Teams.
- Schwebende Tab-Bar mit federnder „Linse“ und segmentierte Steuerelemente mit gleitendem Glas-Daumen
- Große Titel nach iOS-Vorbild, die beim Scrollen in eine Glas-Navigationsleiste übergehen
- Hell- und Dunkelmodus folgen automatisch dem System; `prefers-reduced-motion` wird respektiert

## Daten

Die Daten kommen von der öffentlichen ESPN-Fußball-API (`site.api.espn.com`). Sie braucht keinen Key und erlaubt CORS. Es ist eine inoffizielle Schnittstelle, Endpunkte können sich also ohne Ankündigung ändern.
