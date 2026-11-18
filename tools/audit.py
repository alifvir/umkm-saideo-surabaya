"""Audit hasil build: struktur HTML, tautan, gambar, palet, dan format harga.

Jalankan setelah build: python tools/audit.py
Berakhir "masalah: 0" kalau semua lolos.
"""

import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
ARAH = json.load(open(os.path.join(ROOT, "data", "arah.json"), encoding="utf-8-sig"))

masalah = []
halaman = []
for akar, _dirs, berkas in os.walk(DIST):
    for b in berkas:
        if b.endswith(".html"):
            halaman.append(os.path.join(akar, b))


def rel(p):
    return os.path.relpath(p, DIST).replace("\\", "/")


def luminansi(warna):
    warna = warna.lstrip("#")
    r, g, b = (int(warna[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def kanal(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = kanal(r), kanal(g), kanal(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kontras(depan, belakang):
    a, b = luminansi(depan), luminansi(belakang)
    atas, bawah = max(a, b), min(a, b)
    return (atas + 0.05) / (bawah + 0.05)


# ---------------------------------------------------------------- html
for p in sorted(halaman):
    html = open(p, encoding="utf-8").read()
    nama = rel(p)

    if len(re.findall(r"<h1[ >]", html)) != 1:
        masalah.append("%s: jumlah h1 bukan 1" % nama)
    if 'lang="id"' not in html:
        masalah.append("%s: tidak ada lang=id" % nama)
    if 'name="viewport"' not in html:
        masalah.append("%s: tidak ada meta viewport" % nama)
    if "<title>" not in html or re.search(r"<title>\s*</title>", html):
        masalah.append("%s: title kosong" % nama)
    if 'name="description"' not in html:
        masalah.append("%s: meta description kosong" % nama)
    for wajib in ("og:title", "og:description", "og:image", "twitter:card"):
        if wajib not in html:
            masalah.append("%s: tidak ada %s" % (nama, wajib))

    if "\u2014" in html:
        masalah.append("%s: ada em dash" % nama)
    if re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", html):
        masalah.append("%s: ada emoji" % nama)

    for href in re.findall(r'href="(/[^"#?]*)"', html):
        target = os.path.join(DIST, href.lstrip("/"))
        if href.endswith("/"):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            masalah.append("%s: tautan mati %s" % (nama, href))

    for frag in re.findall(r'href="#([^"]+)"', html):
        if 'id="%s"' % frag not in html:
            masalah.append("%s: anchor #%s tidak ada" % (nama, frag))

    for tag in re.findall(r"<img [^>]*>", html):
        if 'alt="' not in tag:
            masalah.append("%s: img tanpa alt" % nama)
        if "width=" not in tag or "height=" not in tag:
            masalah.append("%s: img tanpa width/height" % nama)
        src = re.search(r'src="(/[^"]+)"', tag)
        if src and not os.path.exists(os.path.join(DIST, src.group(1).lstrip("/"))):
            masalah.append("%s: gambar hilang %s" % (nama, src.group(1)))

    for aset in re.findall(r'(?:href|src)="(/assets/[^"]+)"', html):
        if not os.path.exists(os.path.join(DIST, aset.lstrip("/"))):
            masalah.append("%s: aset hilang %s" % (nama, aset))

    for tag in re.findall(r"<a [^>]*>", html):
        if 'href="#"' in tag or "href=''" in tag:
            masalah.append("%s: tautan kosong" % nama)
        if 'target="_blank"' in tag and "noopener" not in tag:
            masalah.append("%s: target blank tanpa noopener" % nama)

    for angka in re.findall(r"Rp\d[\d.]*", html):
        if not re.match(r"^Rp\d{1,3}(\.\d{3})*$", angka):
            masalah.append("%s: format harga aneh: %s" % (nama, angka))

    if "Lorem" in html or "lorem" in html:
        masalah.append("%s: masih ada teks lorem" % nama)

# ---------------------------------------------------------------- palet
pasangan = []
for a in ARAH["arah"]:
    for depan, belakang in a["pasangan"]:
        pasangan.append((a["nama"], depan, belakang))
for depan, belakang in ARAH["pemilih_pasangan"]:
    pasangan.append(("Pemilih", depan, belakang))

for nama, depan, belakang in pasangan:
    rasio = kontras(depan, belakang)
    if rasio < 4.5:
        masalah.append("%s: kontras %s di %s hanya %.2f:1" % (nama, depan, belakang, rasio))

# ---------------------------------------------------------------- ukuran
ukuran = Counter()
for akar, _dirs, berkas in os.walk(DIST):
    for b in berkas:
        ext = os.path.splitext(b)[1].lower()
        ukuran[ext] += os.path.getsize(os.path.join(akar, b))

print("halaman diperiksa:", len(halaman))
for ext, total in ukuran.most_common():
    print("  %-6s %7.1f KB" % (ext, total / 1024))
print("pasangan kontras diperiksa:", len(pasangan))
print("masalah:", len(masalah))
for m in masalah:
    print("  -", m)
sys.exit(1 if masalah else 0)
