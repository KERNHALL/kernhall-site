#!/usr/bin/env python3
"""Generate static song pages and sitemap from index.html's release catalogue.

Run after changing the catalogue: python scripts/generate_song_pages.py
No external dependencies. Existing release links and dates remain authoritative.
"""
from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://kernhall.de'
source = (ROOT / 'index.html').read_text()
catalogue = re.search(r'const releases = \[([\s\S]*?)\n    \];', source).group(1)
releases = []
for block in re.findall(r'\{[\s\S]*?\}', catalogue):
    data = dict(re.findall(r"(\w+): '([^']*)'", block))
    data['slug'] = data['hyperfollow'].rstrip('/').split('/')[-1]
    if data['slug'] == 'trgerwelle':
        data['slug'] = 'traegerwelle'
    releases.append(data)
assert len({r['slug'] for r in releases}) == len(releases)

def esc(value):
    return html.escape(value, quote=True)

def date(value):
    return '.'.join(reversed(value.split('-')))

for release in releases:
    title = release['title']
    path = '/songs/' + release['slug'] + '/'
    url = BASE + path
    description = f"{title} von KERNHALL: Veröffentlichung am {date(release['date'])}. Offizielles Cover, Songinformationen und Streaminglinks."
    recording = {
        '@context': 'https://schema.org', '@type': 'MusicRecording',
        '@id': url + '#recording', 'name': title, 'url': url,
        'datePublished': release['date'], 'inLanguage': 'de',
        'image': BASE + release['cover'],
        'byArtist': {'@type': 'MusicGroup', '@id': BASE + '/#artist', 'name': 'KERNHALL', 'url': BASE + '/'},
        'sameAs': [release['hyperfollow'], release['spotify']],
    }
    series = (f"<p class=\"song-series\">Aus der Reihe <strong>{esc(release['series'])}</strong> / From the series DARK FAIRY TALES</p>" if 'series' in release else '')
    index = releases.index(release)
    neighbours = releases[max(0, index-1):index] + releases[index+1:index+2]
    links = ''.join(f'<li><a href="/songs/{esc(r["slug"])}/">{esc(r["title"])}</a></li>' for r in neighbours)
    schema_json = json.dumps(recording, ensure_ascii=False).replace('<', r'\u003c')
    content = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} – KERNHALL | Song &amp; Streaminglinks</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/styles.css">
<meta property="og:type" content="music.song">
<meta property="og:site_name" content="KERNHALL">
<meta property="og:title" content="{esc(title)} – KERNHALL">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}{release['cover']}">
<meta property="og:image:alt" content="{esc(title)} – offizielles KERNHALL-Cover">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)} – KERNHALL">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{BASE}{release['cover']}">
<script type="application/ld+json">{schema_json}</script>
<script async src="https://gc.zgo.at/count.js" data-goatcounter="https://kernhall.goatcounter.com/count" data-goatcounter-settings='{{"no_events":true}}'></script>
</head>
<body>
<header class="site-header"><a class="brand" href="/" aria-label="KERNHALL Startseite"><img src="/wordmark-transparent.png" alt="KERNHALL"></a><nav aria-label="Navigation"><a href="/#music">MUSIK / MUSIC</a><a href="/#links">PLATTFORMEN / PLATFORMS</a></nav></header>
<main class="song-page">
<p class="song-breadcrumb"><a href="/">KERNHALL</a> / <a href="/#song-catalogue">Songs</a></p>
<article class="song-layout">
<img class="song-cover" src="{release['cover']}" alt="{esc(title)} – offizielles KERNHALL-Cover" width="1254" height="1254" fetchpriority="high">
<div class="song-content"><p class="eyebrow">KERNHALL · SINGLE</p><h1>{esc(title)}</h1>
<p class="song-date">Release: <time datetime="{release['date']}">{date(release['date'])}</time></p>
{series}
<p>Hier findest du das offizielle Cover und die Streaminglinks zu <strong>{esc(title)}</strong> von KERNHALL.</p>
<p lang="en">The official cover, release date and streaming links for <strong>{esc(title)}</strong> by KERNHALL.</p>
<div class="button-row"><a class="button primary" href="{release['hyperfollow']}" target="_blank" rel="noopener">HYPERFOLLOW / STREAMING &amp; PRE-SAVE</a><a class="button ghost" id="song-spotify" data-release-date="{release['date']}" href="{release['spotify']}" target="_blank" rel="noopener" hidden>SPOTIFY ANHÖREN / LISTEN</a></div>
<p class="song-status" id="song-status">Streaming-Verfügbarkeit siehe HyperFollow. / See HyperFollow for availability.</p>
</div></article>
<section class="song-about"><h2>Über KERNHALL / About</h2><p>KERNHALL ist ein Ein-Mann-Musikprojekt für deutschsprachigen Industrial Metal und Metalcore. Texte, Konzepte und künstlerische Leitung stammen vom Gründer; Musik und Gesang werden mithilfe von KI produziert.</p><p lang="en">KERNHALL is a one-person project for German-language Industrial Metal and Metalcore. The founder writes the lyrics and develops the concepts; music and vocals are produced using AI.</p></section>
<section class="song-related"><h2>Weitere Songs / More songs</h2><ul>{links}</ul><a href="/#song-catalogue">Alle Songs / All songs</a></section>
</main>
<footer><span>© KERNHALL</span><div class="footer-links"><a href="/impressum.html">Impressum / Legal notice</a><a href="/datenschutz.html">Datenschutz / Privacy</a></div></footer>
<script src="/scripts/song-page.js" defer></script>
</body></html>
'''
    target = ROOT / path.lstrip('/') / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)

rows = ''.join(f'<li><a href="/songs/{esc(r["slug"])}/">{esc(r["title"])}</a><time datetime="{r["date"]}">{date(r["date"])}</time></li>\n' for r in releases)
catalogue_html = '<!-- SONG-CATALOGUE:START -->\n<details class="song-catalogue" id="song-catalogue"><summary>Alle Songs &amp; Termine / All songs &amp; release dates</summary><ol>\n' + rows + '</ol></details>\n<!-- SONG-CATALOGUE:END -->'
source = re.sub(r'<!-- SONG-CATALOGUE:START -->[\s\S]*?<!-- SONG-CATALOGUE:END -->', lambda m: catalogue_html, source)
(ROOT / 'index.html').write_text(source)
namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', namespace)
root = ET.Element('{' + namespace + '}urlset')
for path in ['/'] + ['/songs/' + r['slug'] + '/' for r in releases]:
    item = ET.SubElement(root, '{' + namespace + '}url')
    ET.SubElement(item, '{' + namespace + '}loc').text = BASE + path
ET.indent(root)
ET.ElementTree(root).write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
print(f'Generated {len(releases)} song pages, static catalogue and sitemap.')
