# KERNHALL – Nicht veröffentlichter Website-Entwurf (10.10.2026)
Branch: `draft/international-site-2026-10-10`. **main bleibt unverändert.**

## Implementiert im Entwurf
- 19 eindeutige Spotify-Tracklinks, zugehörige Albumlinks und UPCs aus der vom Projektinhaber bereitgestellten DistroKid-Liste. Spotify-Buttons werden nur für laut Website-Datum veröffentlichte Songs gezeigt. Für noch nicht veröffentlichte Songs bleiben HyperFollow-Pre-Saves.
- Startseiten-Button leitet unmittelbar zum neuesten laut vorhandener Website-Daten veröffentlichten Spotify-Track; Fallback: Künstlerprofil.
- Aktueller Release statt kommender Release prominent dargestellt, nächste Veröffentlichung kleiner darunter.
- Deutsche und englische Beschriftungen und transparente Erläuterung des Ein-Mann-Projekts mit KI-produzierter Musik/Vocals.
- Internationale Meta-Texte, lesbarerer Footer, Datumsstand der Sitemap vorbereitet.
- Bekannter KERNHALL-Amazon-Music-Künstlerlink ergänzt; Apple-Music-Künstlerlink bleibt aus, da nicht verlässlich identifiziert.

## Nicht verändert / zu bestätigen
- **Keine Veröffentlichung**: Staging-Branch, keine Änderungen an main.
- **Alle 19 Website-Songtitel und Daten unverändert**; teils abweichende DistroKid-Schreibweisen und Termine sind vor Übernahme ausdrücklich abzugleichen.
- Hinweise auf Abweichungen: VORARBEITER (Website 22.01.2027 vs. vormals geplant 20.11.2026), DER WACHOLDERBAUM/WACHOLDERBAUM, DER GEVATTER TOD/GEVATTER TOD, DIE SCHWARZE SPINNE/SCHWARZE SPINNE; weitere einzelne Titel mit Transliteration und abweichende Märchen-Releasetermine.
- Open Graph / Social Preview: vorhandenes Symbol bleibt bestehen, Bildgestaltung optional zu prüfen.
- Cover-Optimierung: 19 PNGs teils ca. 1,8–2,7 MB, WebP-Varianten sind **noch nicht erzeugt**, da der GitHub-Connector für Dateiänderungen nur UTF-8-Text unterstützt. Originale unangetastet. Nach Freigabe binäre Bilder separat optimieren und unter anderem Pfad bereitstellen.
- Datenschutzseite und GoatCounter-Konfiguration unverändert; rechtliche Prüfung der konkreten Cookie-/Tracking-Konfiguration empfohlen.
- Original-Songcover unverändert; Spotify-URLs wurden aus den vom Projektinhaber gelieferten Daten übernommen, öffentliche Freischaltung zukünftiger Tracklinks kann je Plattform verzögert sein.

## Tests vor Veröffentlichung
1. Responsives Layout (iPhone/Mobil, Desktop), Barrierefreiheit der zweisprachigen Labels.
2. Release-Gating mit Datum 09.10.2026, 10.10.2026 sowie nach letztem eingetragenen Release.
3. Spotify-Tracklinks nur nach Termin anzeigen, HyperFollow auf bevorstehende Releases.
4. DistroKid-Releasetermine und exakte Titelschreibweisen gesondert vom Projektinhaber bestätigen lassen.
5. Amazon-Music-Profil im Browser öffnen, Apple Music URL nachreichen.
6. Datenschutz/GoatCounter, Footer-Kontrast und externe Links prüfen.
