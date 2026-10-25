# Review: Ist ein Tag auf der Venus länger als ihr Jahr? (Simulations-Stil)

- Stil nach den drei Referenzclips des Nutzers: dunkles Navy mit Raster, HUD-Kästen mit laufenden Zahlen, Türkis/Koralle/Orange, Umfrage mit 3-2-1, Simulation, Wendung, Schlusswort.
- Stimme: Piper `de_DE-thorsten-high` (lokal, kostenlos), Satz für Satz erzeugt; Wortzeiten aus den Satzlängen verteilt (keine Whisper-Transkription).
- Musik: MusicGen-small, 29-s-Seed, per Crossfade auf 68 s geloopt, 0.15 unter der Stimme. SFX: mitgelieferte Pixabay-Sounds.
- Fakten: Drehung 243 d (siderisch, rückläufig), Umlauf 224,7 d, Sonnentag ≈ 116,75 d; Simulation rechnet genau damit.
- Gemessen: `check` ok (nur Hinweis: captions.html ist lang, generiert). Mix −14,6 LUFS, True Peak −1,4 dBTP, kein Clipping. Ton gemessen, nicht gehört.
- Neu bauen: `python3 tools/build.py` (Szenen, Untertitel, Root) – Texte/Timings dort ändern.
- Schwächste Stelle: "ALSO JA?"-Karte (36–39 s) ist statisch und unten leer.
