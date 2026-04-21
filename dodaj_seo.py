#!/usr/bin/env python3
"""
Kondyss SEO / Open Graph Patcher
=================================
Uruchom ten skrypt w folderze z plikami HTML (tam gdzie są index.html, subathon.html itp.)
Skrypt doda tagi SEO i Open Graph do każdej strony (embedy na Discordzie itp.)

Użycie:
    python3 dodaj_seo.py
"""

import os
import re

# ── KONFIGURACJA META TAGÓW DLA KAŻDEJ STRONY ─────────────────
PAGES = {
    'index.html': {
        'title':       'Kondyss — Polski Świat aRPG | YouTube & Twitch',
        'description': 'Kondyss — twórca YouTube i streamer Twitch. Polskie poradniki, buildy i livestreamy z Diablo 4, Path of Exile 2, Path of Exile i Last Epoch.',
        'url':         'https://kondyss.pl/',
        'image':       'https://kondyss.pl/img/og/kondyss.jpg',
        'keywords':    'Kondyss, Diablo 4, Path of Exile, Last Epoch, aRPG, poradniki, buildy, Twitch, YouTube, polska',
    },
    'subathon.html': {
        'title':       'Subathon Nienawiści — Kondyss',
        'description': 'Największe wydarzenie w historii kanału! Sprawdź zasady, nagrody i cele Subathonu Nienawiści. Każda sub i donacja dodaje czas do timera.',
        'url':         'https://kondyss.pl/subathon.html',
        'image':       'https://kondyss.pl/img/og/subathon.jpg',
        'keywords':    'Subathon, Kondyss, Twitch, subskrypcja, livestream, event',
    },
    'diablo4.html': {
        'title':       'Diablo IV — Polskie Poradniki i Buildy | Kondyss',
        'description': 'Najlepsze polskie poradniki do Diablo 4. Buildy postaci, taktyki farmienia i startery sezonowe — Sezon Rzezi i kolejne na kanale Kondyssa.',
        'url':         'https://kondyss.pl/diablo4.html',
        'image':       'https://kondyss.pl/img/og/diablo4.jpg',
        'keywords':    'Diablo 4, Diablo IV, build, poradnik, sezon, aRPG, Kondyss, Paladyn, Barbarzyńca, Nekromanta',
    },
    'poe.html': {
        'title':       'Path of Exile — Polskie Poradniki i Buildy | Kondyss',
        'description': 'Polskie poradniki do Path of Exile. Buildy, mechaniki ligowe i startery sezonowe — liga Mirage 3.28 i więcej na kanale Kondyssa.',
        'url':         'https://kondyss.pl/poe.html',
        'image':       'https://kondyss.pl/img/og/poe.jpg',
        'keywords':    'Path of Exile, PoE, build, liga, poradnik, aRPG, Kondyss, Juggernaut, Berserker',
    },
    'poe2.html': {
        'title':       'Path of Exile 2 — Polskie Poradniki i Buildy | Kondyss',
        'description': 'Polskie poradniki do Path of Exile 2 Early Access. Buildy, startery i taktyki farmienia — liga Fate of the Vaal 0.4 na kanale Kondyssa.',
        'url':         'https://kondyss.pl/poe2.html',
        'image':       'https://kondyss.pl/img/og/poe2.jpg',
        'keywords':    'Path of Exile 2, PoE2, Early Access, build, liga, poradnik, aRPG, Kondyss',
    },
    'lastepoch.html': {
        'title':       'Last Epoch — Polskie Poradniki i Buildy | Kondyss',
        'description': 'Polskie poradniki do Last Epoch. Buildy, crafting i postacie sezonowe — Cykl 4 i więcej na kanale Kondyssa.',
        'url':         'https://kondyss.pl/lastepoch.html',
        'image':       'https://kondyss.pl/img/og/lastepoch.jpg',
        'keywords':    'Last Epoch, build, cykl, sezon, crafting, poradnik, aRPG, Kondyss',
    },
}

# ── TEMPLATE BLOKÓW META ───────────────────────────────────────
def make_meta_block(m):
    return f"""
  <!-- ══ SEO ══════════════════════════════════════════════════ -->
  <meta name="description" content="{m['description']}" />
  <meta name="keywords" content="{m['keywords']}" />
  <meta name="author" content="Kondyss" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{m['url']}" />

  <!-- ══ Open Graph — Discord / Facebook / Messenger ══════════ -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Kondyss.pl" />
  <meta property="og:url" content="{m['url']}" />
  <meta property="og:title" content="{m['title']}" />
  <meta property="og:description" content="{m['description']}" />
  <meta property="og:image" content="{m['image']}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{m['title']}" />
  <meta property="og:locale" content="pl_PL" />

  <!-- ══ Twitter Card ══════════════════════════════════════════ -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@kondyss" />
  <meta name="twitter:creator" content="@kondyss" />
  <meta name="twitter:title" content="{m['title']}" />
  <meta name="twitter:description" content="{m['description']}" />
  <meta name="twitter:image" content="{m['image']}" />"""

# ── PATCHER ───────────────────────────────────────────────────
def patch_file(filename, meta):
    if not os.path.exists(filename):
        print(f"  ⚠  Plik nie znaleziony: {filename} — pomijam")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # Sprawdź czy już wstrzyknięte
    if 'og:title' in html:
        print(f"  ✓  {filename} — już ma tagi OG, pomijam (usuń ręcznie jeśli chcesz odświeżyć)")
        return

    # Podmień <title>
    new_title = f'<title>{meta["title"]}</title>'
    html = re.sub(r'<title>[^<]*</title>', new_title, html)

    # Wstaw blok meta po viewport tagu
    meta_block = make_meta_block(meta)
    viewport_pattern = r'(<meta name="viewport"[^/]*/\s*>)'
    if re.search(viewport_pattern, html):
        html = re.sub(viewport_pattern, r'\1' + meta_block, html)
    else:
        # fallback: po <meta charset=...>
        html = re.sub(r'(<meta charset[^/]*/\s*>)', r'\1' + meta_block, html)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✅  {filename} — zaktualizowany pomyślnie")

# ── JSON-LD dla strony głównej ─────────────────────────────────
JSONLD_INDEX = """
  <!-- ══ Structured Data (Google) ══════════════════════════════ -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Kondyss",
    "url": "https://kondyss.pl",
    "sameAs": [
      "https://www.youtube.com/@kondyss",
      "https://www.twitch.tv/kondyss",
      "https://discord.gg/kondyss",
      "https://www.instagram.com/kondyss_"
    ],
    "jobTitle": "Streamer & YouTuber",
    "description": "Kondyss — twórca YouTube i streamer Twitch specjalizujący się w grach aRPG.",
    "knowsAbout": ["Diablo 4", "Path of Exile", "Path of Exile 2", "Last Epoch"]
  }
  </script>"""

def patch_index_jsonld(filename):
    if not os.path.exists(filename):
        return
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    if 'application/ld+json' in html:
        return
    html = html.replace('</head>', JSONLD_INDEX + '\n</head>', 1)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  ✅  {filename} — dodano JSON-LD structured data")

# ── MAIN ──────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n🔍 Kondyss SEO Patcher\n" + "─" * 40)
    for fname, meta in PAGES.items():
        patch_file(fname, meta)
    patch_index_jsonld('index.html')
    print("\n─" * 40)
    print("✅ Gotowe!\n")
    print("📌 WAŻNE — Zdjęcia OG Image:")
    print("   Stwórz folder /img/og/ i wrzuć tam obrazki 1200×630 px:")
    print("   kondyss.jpg, subathon.jpg, diablo4.jpg, poe.jpg, poe2.jpg, lastepoch.jpg")
    print("\n   Do czasu stworzenia dedykowanych obrazków Discord użyje")
    print("   tego co ma dostępne (logo gry / zdjęcie profilowe).\n")
