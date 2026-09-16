# KERNHALL – Website

Fertige statische Website für **https://kernhall.de**.

## Inhalt
- `index.html` – Startseite
- `styles.css` – Design
- `kernhall-*.png`, `kern-cover.png`, `favicon.png` – Bilder direkt im Hauptverzeichnis
- `CNAME` – Custom Domain `kernhall.de`
- `robots.txt` + `sitemap.xml` – Google/SEO
- `impressum.html` – **muss vor Veröffentlichung ergänzt werden**
- `datenschutz.html` – schlanke Datenschutzseite ohne Tracking

## GitHub Pages – iPhone / Safari

1. Repository `kernhall-site` öffnen.
2. Dateien aus diesem ZIP **in die oberste Ebene des Repositories** hochladen.
3. GitHub → Repository → **Settings** → **Pages**.
4. Unter **Build and deployment**:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/ (root)`
   - Save
5. Unter **Custom domain**: `kernhall.de` eintragen und speichern.
6. Nach erfolgreicher DNS-Auflösung **Enforce HTTPS** aktivieren.

## DNS bei netcup für kernhall.de

Für die Apex-Domain `kernhall.de` vier A-Records auf GitHub Pages setzen:

- `@` → `185.199.108.153`
- `@` → `185.199.109.153`
- `@` → `185.199.110.153`
- `@` → `185.199.111.153`

Optional zusätzlich IPv6/AAAA:

- `@` → `2606:50c0:8000::153`
- `@` → `2606:50c0:8001::153`
- `@` → `2606:50c0:8002::153`
- `@` → `2606:50c0:8003::153`

Für `www.kernhall.de`:
- `www` → CNAME auf `<DEIN-GITHUB-BENUTZERNAME>.github.io`

GitHub empfiehlt bei einer Apex-Domain zusätzlich die `www`-Variante. GitHub leitet bei korrekter Konfiguration zwischen beiden Varianten um.

**Wichtig:** Bestehende kollidierende A/AAAA/CNAME-Einträge für dieselben Hosts vorher prüfen. DNS kann bis zu 24 Stunden benötigen.

## Google Search Console

Nach Veröffentlichung:
1. https://search.google.com/search-console öffnen
2. Property `https://kernhall.de/` hinzufügen
3. Verifikation per HTML-Meta-Tag auswählen
4. Den von Google ausgegebenen Token in `index.html` an der markierten Stelle einfügen
5. Änderungen committen
6. In Search Console `https://kernhall.de/` prüfen und **Indexierung beantragen**
7. Sitemap einreichen: `https://kernhall.de/sitemap.xml`

## Release-Automatik

Die Website wechselt am **18.09.2026 um 00:00 MESZ** automatisch:
- von `KERN VORMERKEN` zu `KERN AUF SPOTIFY`
- auf den direkten Track-Link
- HyperFollow bleibt als Link zu allen Streamingdiensten erhalten.

## Vor Veröffentlichung zwingend

`impressum.html` enthält absichtlich Platzhalter für Name und ladungsfähige Anschrift. Diese Daten müssen korrekt ergänzt werden.
