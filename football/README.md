# Arenly

<img src="assets/icon-rounded-256.png" width="96" alt="Arenly App-Icon">

Eine Sport-Web-App (aktuell: Fußball) im Stil von Apples *Liquid Glass*: alle großen Ligen, Tabellen, Teams, Kader und Spiele, live und ohne API-Key.

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
| **Übersicht** | Start-Tab mit Lieblingsverein, Lieblingsliga und Nationalteam auf einen Blick: letztes und nächstes Spiel (inkl. Pokal und Europapokal) mit TV-Sender, Countdown bis zum Anpfiff und „In Kalender“ (Termin mit Erinnerung 30 Min. vorher), Tabellenplatz, Tabellenausschnitt der Liga, **Transfers** (Gerüchte und offizielle Wechsel, nur wenn es welche gibt) und aktuelle **News** |
| **Ligen** | Bundesliga, 2. Bundesliga, DFB-Pokal, Premier League, LaLiga, Serie A, Ligue 1, Champions/Europa/Conference League, Eredivisie, Primeira Liga, Süper Lig, Österreich, Schweiz, Schottland, Belgien, MLS |
| **Liga** | Tabelle mit Europapokal- und Abstiegszonen und **Formkurve** (letzte 5 Spiele), Spieltage mit Datumsauswahl, **Torjäger** (Tore und Vorlagen, mit Spielerfotos), alle Teams |
| **Team** | Platzierung und Bilanz, nächste Spiele, Ergebnisse, Kader nach Positionen, Spielerprofil als Sheet |
| **Spiel** | Ergebnis, Verlauf (Tore, Karten, Wechsel), Statistik-Balken, **Aufstellung auf dem Spielfeld**: beide Teams stehen sich in ihrer echten Formation gegenüber, mit Spielerfotos, Rückennummer, Toren, Karten und Auswechslungen, darunter die Bank; aktualisiert sich bei Live-Spielen alle 30 s |
| **Spiele** | Alle Ligen für einen Tag (−4 bis +4 Tage), Live-Zähler, deine Favoriten zuerst |
| **Suche** | Teams (deutsch oder englisch) und Ligen |
| **Favoriten** | Teams mit ★ markieren (wird lokal im Browser gespeichert) |

## Start-Ablauf

1. **Intro-Video:** `assets/intro.mp4` (1080×1920, 5,2 s): Bälle verschiedener Sportarten verschmelzen zum Arenly-„A“. Es läuft beim Start im Vollbild. Hat ein Video eine Tonspur, erscheint oben links **„Ton an“**, da Browser nur stumm automatisch abspielen. Bei sehr langsamer Verbindung oder im Stromsparmodus erscheint nach 4 s das animierte Logo. Ein neues Video einfach als `assets/intro.mp4` ablegen (H.264, Hochformat).
2. **Registrierung:** Name, E-Mail und Passwort, mit Prüfung der Eingaben.
3. **Lieblingsverein:** Auswahl über Liga-Chips oder Suche. Die App übernimmt sofort die Vereinsfarben als Live-Vorschau.
4. **Lieblingsliga:** vorausgewählt ist die Liga des Vereins.
5. **Nationalmannschaft:** über 200 Länder, die beliebtesten oben, mit Suche.
6. **Fertig:** Verein und Nationalteam landen unter „Meine Teams“. Im Tab **Profil** lassen sich beide ändern und man kann sich abmelden.

### Vereinsfarben

Die Farben kommen aus ESPNs Vereinsfarbe, sofern sie eine echte Farbe ist (nicht nur Weiß), und aus den dominanten Farben des Wappens, die per Canvas ausgelesen werden. Ein Beispiel: Dortmund wird Gelb/Schwarz, Frankfurt Rot/Dunkelrot, Real Madrid Gold/Blau. Die Akzentfarbe wird für Hell- und Dunkelmodus automatisch so angepasst, dass sie lesbar bleibt.

### Konten mit Supabase

Arenly nutzt **Supabase** für Registrierung, Anmeldung und das Profil (Verein, Nationalteam, Farben und Favoriten werden geräteübergreifend gespeichert). Solange `config.js` leer ist, läuft die App im **lokalen Modus**, d. h. das Profil liegt nur auf dem Gerät.

**Einrichtung (ca. 10 Minuten):**

1. Auf [supabase.com](https://supabase.com) kostenlos ein Projekt anlegen, als Region **Frankfurt (eu-central-1)** wählen.
2. **SQL Editor:** Inhalt von [`supabase/schema.sql`](supabase/schema.sql) einfügen und ausführen. Das legt die Tabelle `profiles` mit Row Level Security an: Jeder sieht nur sein eigenes Profil.
3. **Authentication → URL Configuration:** als *Site URL* die Adresse der App eintragen (z. B. `https://<name>.github.io/Jarviss/football/`) und unter *Redirect URLs* zusätzlich `http://localhost:8000/**` für lokale Tests.
4. **Authentication → Emails:** die deutschen Vorlagen aus [`supabase/email-templates/`](supabase/email-templates/) einfügen (Betreff und HTML, siehe [Anleitung](supabase/email-templates/README.md)).
5. **Project Settings → API:** *Project URL* und den *anon public* Key in [`config.js`](config.js) eintragen. Dieser Key ist für den Browser gedacht und darf öffentlich sein. Den *service_role* Key niemals eintragen.

**Funktionen:** Registrierung mit E-Mail-Bestätigung (inkl. „Erneut senden“), Anmeldung, „Passwort vergessen“ mit Link zum Festlegen eines neuen Passworts, Abmelden, Synchronisierung des Profils und deutsche Fehlermeldungen.

**Mit Apple anmelden** (optional, erfordert einen Apple-Developer-Account, 99 $/Jahr): in Supabase unter *Authentication → Providers → Apple* einrichten, dann in `config.js` `appleSignIn: true` setzen.

### News & Transfers

- **kicker** (deutsch): eigener Feed für alle Vereine der 1. und 2. Bundesliga, für Bundesliga, 2. Bundesliga, DFB-Pokal, Champions League, Europa League und die deutsche Nationalmannschaft
- **Transfermarkt** (deutsch): Meldungen, die den Verein in der Überschrift nennen
- **ESPN** (englisch, mit „EN“ markiert): für Vereine und Ligen ohne kicker-Feed sowie als Quelle für Transfergerüchte
- Transfers werden an der Überschrift erkannt (z. B. „verpflichtet“, „ist perfekt“, „im Visier“, „transfer rumors“) und als **Gerücht** oder **Offiziell** markiert. Angezeigt werden Meldungen der letzten 21 Tage, Doppelte werden zusammengefasst. Ein Tipp öffnet den Artikel beim Anbieter.

### Spielerfotos

Freigestellte Fotos von [TheSportsDB](https://www.thesportsdb.com) (kostenlose API, ca. 30 Anfragen pro Minute):

- Suche nach vollem Namen; der Treffer wird gegen den Spielernamen geprüft (auch ß/Akzente), damit nie ein falsches Foto erscheint.
- Bei abweichender Schreibweise wird nach dem Nachnamen gesucht und der Spieler über den Verein zugeordnet.
- Als Reserve dient das ESPN-Foto, sonst die Rückennummer in den Vereinsfarben.
- Abdeckung im Test: rund 92–100 % je nach Liga (Bundesliga 100 %). Die Startelf lädt zuerst, die Bank wegen des Limits innerhalb von 1–2 Minuten. Danach ist jedes Foto im Gerät gespeichert.

### Spielfeld ohne Überlappung

Fotogröße, Namensbreite und Reihenabstände werden pro Formation berechnet: Der Reihenabstand ist immer größer als Foto plus Name, der Spaltenabstand größer als die Namensbreite. Reicht der Platz nicht, wird das Feld höher, statt die Fotos zu verkleinern. Geprüft automatisch für 9 Formationen (u. a. 4-2-3-1, 4-3-3, 3-5-2, 5-3-2, 4-1-2-1-2) auf 320, 390 und 430 px Breite.

### TV-Sender (Deutschland)

Auf der Spielseite steht bei anstehenden und laufenden Spielen, wo sie in Deutschland live laufen. Abgeleitet aus der Rechtevergabe 2026/27 nach Wettbewerb, Wochentag und Anstoßzeit:

| Wettbewerb | Sender |
|---|---|
| Bundesliga | Freitag & Samstag Sky (Sa 15:30 zusätzlich DAZN-Konferenz), Sonntag DAZN |
| 2. Bundesliga | Sky, Samstag 20:30 zusätzlich RTL |
| DFB-Pokal | Sky, ausgewählte Spiele ARD/ZDF/RTL |
| Champions League | DAZN, Dienstags-Topspiel Prime Video |
| Europa & Conference League | RTL+, ein Spiel pro Spieltag frei bei RTL/NITRO |
| Premier League | Sky |
| LaLiga, Serie A | DAZN |
| Deutschland (Nations League, Quali) | auswärts RTL, daheim ARD oder ZDF; Testspiele ARD/ZDF/RTL |

Für andere Wettbewerbe wird nichts angezeigt. Die Regeln stehen in `tvGermany()` in `index.html` und müssen bei neuen Rechteperioden angepasst werden (z. B. Champions League ab 2027/28 bei Paramount+, Europa/Conference League bei DAZN).

### Push-Mitteilungen

Tore (mit Torschütze), Anpfiff & Abpfiff und Aufstellung für Lieblingsverein und Nationalteam – einzeln schaltbar unter **Profil → Benachrichtigungen**. Auf dem iPhone nur, wenn Arenly auf dem Home-Bildschirm liegt (ab iOS 16.4).

- `sw.js`: Service Worker, zeigt Mitteilungen an und öffnet beim Antippen das Spiel
- `supabase/push.sql`: Tabellen `push_subscriptions` (Geräte, nur eigene Zeilen) und `push_state` (was schon gemeldet wurde) plus pg_cron-Job, der jede Minute die Edge Function aufruft
- `supabase/functions/push-watch/`: Edge Function – liest die Spiele des Tages bei ESPN, entscheidet in `logic.ts`, was neu ist, und verschickt Web Push (VAPID). Schon gefallene Tore werden beim ersten Blick auf ein laufendes Spiel nicht nachträglich gemeldet.
- Secrets der Edge Function: `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `VAPID_SUBJECT`, `CRON_SECRET` (der private Schlüssel gehört nur dorthin, nie ins Repository); `verify_jwt` ist aus, geschützt wird über `CRON_SECRET`.

## Updates

Die App prüft beim Start und bei jeder Rückkehr, ob online eine neuere Version liegt (`APP_BUILD` in `index.html`), und lädt sich dann einmal selbst neu. So bleiben auch App-Icons auf dem Home-Bildschirm aktuell. Vor jedem Veröffentlichen `tools/release.sh` ausführen, das setzt eine neue Build-Kennung.

## Weitere Sportarten

Auf der Ligen-Seite oben die Sportart wählen: ⚽ Fußball · 🏀 Basketball (NBA, WNBA) · 🏒 Eishockey (NHL) · 🏈 Football (NFL) · ⚾ Baseball (MLB) · 🏎️ Formel 1.

- Tabellen mit passenden Spalten (Siege/Niederlagen/Quote/Serie, beim Eishockey OT und Punkte), Spiele, Teams, Teamseiten mit Kader und Fotos
- Spielseite: Ergebnis pro Viertel/Drittel/Inning, Team-Statistik, Top-Spieler
- Formel 1: Fahrer-WM, Konstrukteurs-WM, Rennkalender; pro Grand Prix Training, Qualifying, Sprint und Rennen
- Ligen anderer Sportarten haben Kennungen wie `basketball:nba`; deutsche Ligen (BBL, DEL, Handball) bietet die Datenquelle nicht an

## Marke & Icon

- **Name:** Arenly (von *Arena*): international aussprechbar und an keine Sportart gebunden
- **Icon** (`assets/icon.svg`): ein Glas-„A“ als Arena-Bogen, umkreist von einem Stadion-Oval mit leuchtendem Ball. Das Oval steht für Stadion und Laufbahn, der Ball für jede Sportart und für „live“.
- **Exporte** in `assets/`: `icon-1024.png` (App Store), `icon-512/192.png`, `icon-maskable-512.png` (Android), `apple-touch-icon.png` (iOS-Home-Bildschirm), `favicon-64.png`, `icon-rounded-256.png` (in der App)
- **In der App:** Favicon, Home-Bildschirm-Icon (`manifest.webmanifest`), Start-Splash, Marke auf der Startseite und im Footer

## Design

- Glasflächen aus `backdrop-filter: blur() saturate()`, einem spiegelnden Verlaufsrand und einem inneren Glanz
- Farbige, langsam treibende Lichtflächen im Hintergrund, die die Glasflächen brechen. Sie färben sich in den Vereinsfarben des geöffneten Teams.
- Schwebende Tab-Bar mit federnder „Linse“ und segmentierte Steuerelemente mit gleitendem Glas-Daumen
- Große Titel nach iOS-Vorbild, die beim Scrollen in eine Glas-Navigationsleiste übergehen
- Hell- und Dunkelmodus folgen automatisch dem System; `prefers-reduced-motion` wird respektiert

## Daten

Die Daten kommen von der öffentlichen ESPN-Fußball-API (`site.api.espn.com`). Sie braucht keinen Key und erlaubt CORS. Es ist eine inoffizielle Schnittstelle, Endpunkte können sich also ohne Ankündigung ändern.
