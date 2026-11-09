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
| **Ligen** | Bundesliga, 2. Bundesliga, DFB-Pokal, Premier League, LaLiga, Serie A, Ligue 1, Champions/Europa/Conference League, Eredivisie, Primeira Liga, Süper Lig, Österreich, Schweiz, Schottland, Belgien, MLS |
| **Liga** | Tabelle mit Europapokal- und Abstiegszonen, Spieltage mit Datumsauswahl, alle Teams |
| **Team** | Platzierung und Bilanz, nächste Spiele, Ergebnisse, Kader nach Positionen, Spielerprofil als Sheet |
| **Spiel** | Ergebnis, Verlauf (Tore, Karten, Wechsel), Statistik-Balken, Aufstellungen mit Formation; aktualisiert sich bei Live-Spielen alle 30 s |
| **Spiele** | Alle Ligen für einen Tag (−4 bis +4 Tage), Live-Zähler, deine Favoriten zuerst |
| **Suche** | Teams (deutsch oder englisch) und Ligen |
| **Favoriten** | Teams mit ★ markieren (wird lokal im Browser gespeichert) |

## Start-Ablauf

1. **Intro-Video:** `assets/intro.mp4` (optional zusätzlich `assets/intro.webm`) wird beim Start stumm und im Vollbild abgespielt und lässt sich überspringen. Solange es noch kein Video gibt, erscheint stattdessen das animierte Logo.
2. **Registrierung:** Name, E-Mail und Passwort, mit Prüfung der Eingaben.
3. **Lieblingsverein:** Auswahl über Liga-Chips oder Suche. Die App übernimmt sofort die Vereinsfarben als Live-Vorschau.
4. **Nationalmannschaft:** über 200 Länder, die beliebtesten oben, mit Suche.
5. **Fertig:** Verein und Nationalteam landen unter „Meine Teams“. Im Tab **Profil** lassen sich beide ändern und man kann sich abmelden.

### Vereinsfarben

Die Farben kommen aus ESPNs Vereinsfarbe, sofern sie eine echte Farbe ist (nicht nur Weiß), und aus den dominanten Farben des Wappens, die per Canvas ausgelesen werden. Ein Beispiel: Dortmund wird Gelb/Schwarz, Frankfurt Rot/Dunkelrot, Real Madrid Gold/Blau. Die Akzentfarbe wird für Hell- und Dunkelmodus automatisch so angepasst, dass sie lesbar bleibt.

### Konten mit Supabase

Arenly nutzt **Supabase** für Registrierung, Anmeldung und das Profil (Verein, Nationalteam, Farben und Favoriten werden geräteübergreifend gespeichert). Solange `config.js` leer ist, läuft die App im **lokalen Modus**, d. h. das Profil liegt nur auf dem Gerät.

**Einrichtung (ca. 10 Minuten):**

1. Auf [supabase.com](https://supabase.com) kostenlos ein Projekt anlegen, als Region **Frankfurt (eu-central-1)** wählen.
2. **SQL Editor:** Inhalt von [`supabase/schema.sql`](supabase/schema.sql) einfügen und ausführen. Das legt die Tabelle `profiles` mit Row Level Security an: Jeder sieht nur sein eigenes Profil.
3. **Authentication → URL Configuration:** als *Site URL* die Adresse der App eintragen (z. B. `https://<name>.github.io/Jarviss/football/`) und unter *Redirect URLs* zusätzlich `http://localhost:8000/**` für lokale Tests.
4. **Authentication → Emails** (optional): die Bestätigungs- und Passwort-Mails ins Deutsche übersetzen.
5. **Project Settings → API:** *Project URL* und den *anon public* Key in [`config.js`](config.js) eintragen. Dieser Key ist für den Browser gedacht und darf öffentlich sein. Den *service_role* Key niemals eintragen.

**Funktionen:** Registrierung mit E-Mail-Bestätigung (inkl. „Erneut senden“), Anmeldung, „Passwort vergessen“ mit Link zum Festlegen eines neuen Passworts, Abmelden, Synchronisierung des Profils und deutsche Fehlermeldungen.

**Mit Apple anmelden** (optional, erfordert einen Apple-Developer-Account, 99 $/Jahr): in Supabase unter *Authentication → Providers → Apple* einrichten, dann in `config.js` `appleSignIn: true` setzen.

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
