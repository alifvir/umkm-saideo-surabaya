"""Build tiga arah situs Saideo Surabaya, masing-masing lima halaman.

Sumber:
  data/site.json     identitas, tautan, catatan
  data/produk.json   produk dan harga
  data/mitra.json    isi program mitra
  data/arah.json     palet dan keterangan tiap arah desain
  assets-src/*.jpeg  foto dari pemilik akun

Halaman per arah: beranda, produk, mitra, tentang, kontak.
Hasil: dist/ siap diunggah ke Cloudflare Pages.

Jalankan: python build.py
"""

import json
import os
import shutil
from html import escape
from urllib.parse import quote

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "assets-src")
DIST = os.path.join(ROOT, "dist")
IMG = os.path.join(DIST, "assets", "img")

SITE = json.load(open(os.path.join(ROOT, "data", "site.json"), encoding="utf-8-sig"))
PRODUK = json.load(open(os.path.join(ROOT, "data", "produk.json"), encoding="utf-8-sig"))
MITRA = json.load(open(os.path.join(ROOT, "data", "mitra.json"), encoding="utf-8-sig"))
ARAH = json.load(open(os.path.join(ROOT, "data", "arah.json"), encoding="utf-8-sig"))

MAPS = "https://www.google.com/maps/search/?api=1&query=Perak+Utara+Surabaya"

FAQ = [
    ("Berapa jumlah minimal untuk jadi mitra?",
     "Paket mulai 10 pcs. Jumlah untuk paket toko dan grosir masih disiapkan, tanyakan lewat WhatsApp."),
    ("Bagaimana cara mengambil barang?",
     "Bisa diambil atau COD di Perak Utara, Surabaya. Pengiriman juga bisa dari Surabaya."),
    ("Apakah harga paket ditampilkan di situs?",
     "Belum. Harga paket dikirim lewat WhatsApp karena bergantung jumlah dan isi paket."),
    ("Apakah produk sudah BPOM?",
     "Merek mencantumkan keterangan BPOM pada produk. Nomor izin edar menyusul di halaman ini."),
]

IKON_WA = (
    '<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" focusable="false">'
    '<path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38c1.45.79 '
    '3.08 1.21 4.79 1.21h.01c5.46 0 9.91-4.45 9.91-9.91C21.96 6.45 17.5 2 12.04 2Zm5.8 14.13c-.24.68-1.4 1.3-1.93 '
    '1.35-.53.05-1.02.24-3.44-.72-2.93-1.15-4.75-4.2-4.9-4.4-.14-.2-1.16-1.55-1.16-2.96 0-1.4.73-2.09 1-2.38.26-.29.58-.36.77-.36l.56.01c.18 '
    '0 .42-.07.65.5.24.58.82 2 .89 2.14.07.14.12.31.02.5-.1.2-.15.32-.29.49-.15.17-.31.38-.44.51-.15.14-.3.3-.13.59.17.29.75 '
    '1.24 1.62 2.01 1.11.99 2.05 1.3 2.34 1.44.29.15.46.12.63-.07.17-.2.73-.85.93-1.14.19-.29.39-.24.65-.14.26.09 1.66.78 1.94.93.29.14.48.22.55.34.07.13.07.73-.17 1.41Z"/></svg>'
)

FONTS_1 = "family=Bricolage+Grotesque:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600"
FONTS_2 = "family=Anton&family=Plus+Jakarta+Sans:wght@400;500;700"
FONTS_3 = "family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Plus+Jakarta+Sans:wght@400;500;600"


def rupiah(n):
    return "Rp" + format(n, ",d").replace(",", ".")


def tautan_wa(pesan=None):
    nomor = (SITE.get("wa") or "").strip()
    if nomor:
        bersih = nomor.replace("+", "").replace(" ", "").replace("-", "")
        if bersih.startswith("0"):
            bersih = "62" + bersih[1:]
        return "https://wa.me/%s?text=%s" % (bersih, quote(pesan or SITE["wa_pesan"]))
    return SITE["wa_cadangan"]


def wa(kelas, teks, pesan=None):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s</a>' % (
        kelas, escape(tautan_wa(pesan)), teks)


def shopee(kelas, teks):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s</a>' % (
        kelas, escape(SITE["shopee"]), teks)


def kepala(judul, deskripsi, css, tema, fonts, kanonikal):
    kanon = og_url = ""
    if SITE.get("url"):
        kanon = '<link rel="canonical" href="%s%s">' % (SITE["url"], kanonikal)
        og_url = '<meta property="og:url" content="%s%s">' % (SITE["url"], kanonikal)
    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="{tema}">
<title>{escape(judul)}</title>
<meta name="description" content="{escape(deskripsi)}">
{kanon}
<meta property="og:type" content="website">
<meta property="og:locale" content="id_ID">
<meta property="og:site_name" content="Saideo Surabaya">
<meta property="og:title" content="{escape(judul)}">
<meta property="og:description" content="{escape(deskripsi)}">
<meta property="og:image" content="/assets/img/og.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
{og_url}
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">
<link rel="stylesheet" href="/assets/css/{css}">
</head>
<body>
<a class="lewati" href="#utama">Lewati ke isi utama</a>
"""


def tutup():
    return f"""
<a class="wa-melayang" href="{escape(tautan_wa())}" target="_blank" rel="noopener" aria-label="Chat WhatsApp Saideo Surabaya">{IKON_WA}</a>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


def blok_produk(kelas_kartu, kelas_harga, kelas_tombol):
    kartu = []
    for p in PRODUK:
        fakta = "".join("<li>%s</li>" % escape(f) for f in p["fakta"])
        pesan = "Halo Saideo Surabaya, saya mau pesan %s (%s)." % (p["nama"], rupiah(p["harga"]))
        kartu.append(f"""
      <article class="{kelas_kartu}">
        <div class="produk__isi">
          <p class="label-kecil">{escape(p['label'])}</p>
          <h3>{escape(p['nama'])}</h3>
          <p class="catatan-produk">{escape(p['catatan'])}</p>
          <ul class="tag">{fakta}</ul>
        </div>
        <div class="produk__beli">
          <p class="{kelas_harga}">{rupiah(p['harga'])}</p>
          {wa(kelas_tombol, "Pesan", pesan)}
        </div>
      </article>""")
    return "".join(kartu)


def blok_paket(kelas):
    return "".join(f"""
        <li class="{kelas}">
          <div>
            <strong>{escape(nama)}</strong>
            <span>{escape(catatan)}</span>
          </div>
          <span class="paket__jumlah">{escape(jumlah)}</span>
        </li>""" for nama, jumlah, catatan in MITRA["paket"])


def blok_langkah_mitra(kelas):
    return "".join(f"""
        <li>
          <span class="langkah__no">{i:02d}</span>
          <div>
            <h3>{escape(j)}</h3>
            <p>{escape(t)}</p>
          </div>
        </li>""" for i, (j, t) in enumerate(MITRA["langkah"], 1))


def blok_langkah_pesan():
    langkah = [
        ("Chat atau buka Shopee", "Tanya stok, pilih kemasan, lalu sebutkan alamat kirim atau rencana ambil sendiri."),
        ("Konfirmasi dan bayar", "Transfer untuk pengiriman, atau bayar di tempat untuk COD di Perak Utara."),
        ("Terima barang", "Ambil di Perak Utara, atau terima kiriman dari Surabaya."),
    ]
    return "".join(f"""
        <li>
          <span class="langkah__no">{i:02d}</span>
          <div>
            <h3>{escape(j)}</h3>
            <p>{escape(t)}</p>
          </div>
        </li>""" for i, (j, t) in enumerate(langkah, 1))


def blok_faq():
    return "".join(f"""
        <details>
          <summary>{escape(tanya)}</summary>
          <p>{escape(jawab)}</p>
        </details>""" for tanya, jawab in FAQ)


def blok_fakta():
    fakta = [
        ("Agen resmi", "Menjual Saideo Deodorant Fresh langsung dari Surabaya."),
        ("Non alkohol", "Keterangan produk resmi menyebut formulanya tanpa alkohol."),
        ("BPOM", "Keterangan BPOM dari merek. Nomor izin edar menyusul."),
        ("COD Perak Utara", "Bisa diambil atau dibayar di tempat, atau dikirim dari Surabaya."),
    ]
    return "".join(f"""
        <li><strong>{escape(j)}</strong><span>{escape(t)}</span></li>""" for j, t in fakta)


def kepala_dalam(nomor, label, h1, intro):
    return f"""
<section class="d-kepala">
  <div class="wrap">
    <p class="label"><span>{nomor}</span> {escape(label)}</p>
    <h1>{escape(h1)}</h1>
    <p class="d-intro">{escape(intro)}</p>
  </div>
</section>"""


# ------------------------------------------------------------------ gambar
def potong_rasio(im, rasio):
    w, h = im.size
    if w / h > rasio:
        baru = int(h * rasio)
        kiri = (w - baru) // 2
        return im.crop((kiri, 0, kiri + baru, h))
    baru = int(w / rasio)
    atas = (h - baru) // 2
    return im.crop((0, atas, w, atas + baru))


def simpan_webp(im, nama, mutu=84):
    im.save(os.path.join(IMG, nama), "WEBP", quality=mutu, method=6)
    return {"berkas": "assets/img/" + nama, "w": im.width, "h": im.height}


def siapkan_gambar():
    if os.path.isdir(IMG):
        shutil.rmtree(IMG)
    os.makedirs(IMG, exist_ok=True)
    hasil = {}

    dinding = Image.open(os.path.join(SRC, "dinding-botol.jpeg")).convert("RGB")
    dinding = dinding.resize((1600, round(dinding.height * 1600 / dinding.width)), Image.LANCZOS)
    hasil["dinding"] = simpan_webp(dinding, "dinding.webp", 82)

    og = potong_rasio(dinding, 1200 / 630).resize((1200, 630), Image.LANCZOS)
    og.save(os.path.join(IMG, "og.jpg"), "JPEG", quality=82, optimize=True, progressive=True)

    agen = Image.open(os.path.join(SRC, "poster-agen.jpeg")).convert("RGB")
    agen.thumbnail((860, 860), Image.LANCZOS)
    hasil["agen"] = simpan_webp(agen, "poster-agen.webp", 85)

    mitra = Image.open(os.path.join(SRC, "poster-mitra.jpeg")).convert("RGB")
    mitra = mitra.resize((760, round(mitra.height * 760 / mitra.width)), Image.LANCZOS)
    hasil["mitra"] = simpan_webp(mitra, "poster-mitra.webp", 85)

    chat = Image.open(os.path.join(SRC, "testimoni.jpeg")).convert("RGB")
    chat = chat.resize((960, round(chat.height * 960 / chat.width)), Image.LANCZOS)
    hasil["testimoni"] = simpan_webp(chat, "testimoni.webp", 86)

    produk = Image.open(os.path.join(SRC, "produk-desk.jpeg")).convert("RGB")
    hasil["produk"] = simpan_webp(produk, "produk-100ml.webp", 86)

    ikon = Image.new("RGB", (128, 128), (12, 74, 58))
    gambar = ImageDraw.Draw(ikon)
    try:
        font = ImageFont.truetype("arialbd.ttf", 92)
    except OSError:
        font = ImageFont.load_default()
    kotak = gambar.textbbox((0, 0), "S", font=font)
    gambar.text(
        ((128 - (kotak[2] - kotak[0])) / 2 - kotak[0], (128 - (kotak[3] - kotak[1])) / 2 - kotak[1]),
        "S", font=font, fill=(245, 248, 246),
    )
    ikon.save(os.path.join(DIST, "assets", "favicon.png"), "PNG")
    return hasil


# ------------------------------------------------------------------ navigasi
def nav_1(aktif):
    def item(kunci, href, teks):
        tanda = ' aria-current="page"' if aktif == kunci else ""
        return '<li><a href="%s"%s>%s</a></li>' % (href, tanda, teks)
    return f"""
<header class="kepala">
  <div class="wrap kepala__bar">
    <a class="merek" href="/arah-1/">
      <span class="merek__tanda" aria-hidden="true">S</span>
      <span class="merek__teks"><strong>Saideo</strong><small>Deodorant Fresh, Surabaya</small></span>
    </a>
    <button class="menu-tombol" type="button" data-nav-tombol aria-expanded="false" aria-controls="nav-utama">
      <span class="menu-tombol__garis" aria-hidden="true"></span>Menu
    </button>
    <nav class="nav" id="nav-utama" data-nav data-terbuka="false" aria-label="Navigasi utama">
      <ul>
        {item("produk", "/arah-1/produk/", "Produk")}
        {item("mitra", "/arah-1/mitra/", "Buka mitra")}
        {item("tentang", "/arah-1/tentang/", "Tentang")}
        {item("kontak", "/arah-1/kontak/", "Kontak")}
        <li>{wa("nav__cta", "WhatsApp")}</li>
      </ul>
    </nav>
  </div>
</header>"""


def kaki_1():
    return f"""
<footer class="kaki">
  <div class="wrap kaki__grid">
    <div>
      <p class="kaki__merek">Saideo</p>
      <p>Deodorant Fresh dari agen resmi Surabaya. Dijual eceran dan untuk mitra mulai 10 pcs.</p>
    </div>
    <div>
      <h2>Halaman</h2>
      <ul>
        <li><a href="/arah-1/produk/">Produk dan harga</a></li>
        <li><a href="/arah-1/mitra/">Buka mitra</a></li>
        <li><a href="/arah-1/tentang/">Tentang</a></li>
        <li><a href="/arah-1/kontak/">Kontak</a></li>
      </ul>
    </div>
    <div>
      <h2>Kontak</h2>
      <ul>
        <li><a href="{escape(SITE['instagram'])}" target="_blank" rel="noopener">Instagram {escape(SITE['handle'])}</a></li>
        <li><a href="{escape(SITE['shopee'])}" target="_blank" rel="noopener">Toko resmi di Shopee</a></li>
        <li><a href="{escape(tautan_wa())}" target="_blank" rel="noopener">WhatsApp</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap kaki__bawah">
    <span>&copy; 2026 Saideo Surabaya.</span>
    <span>{escape(SITE['catatan_pratinjau'])}</span>
  </div>
</footer>"""


def nav_2(aktif):
    def item(kunci, href, teks):
        tanda = ' aria-current="page"' if aktif == kunci else ""
        return '<li><a href="%s"%s>%s</a></li>' % (href, tanda, teks)
    return f"""
<header class="kepala">
  <div class="wrap kepala__bar">
    <a class="merek" href="/arah-2/">SAIDEO<span>/SBY</span></a>
    <button class="menu-tombol" type="button" data-nav-tombol aria-expanded="false" aria-controls="nav-utama">
      <span class="menu-tombol__garis" aria-hidden="true"></span>Menu
    </button>
    <nav class="nav" id="nav-utama" data-nav data-terbuka="false" aria-label="Navigasi utama">
      <ul>
        {item("produk", "/arah-2/produk/", "Produk")}
        {item("mitra", "/arah-2/mitra/", "Mitra")}
        {item("tentang", "/arah-2/tentang/", "Tentang")}
        {item("kontak", "/arah-2/kontak/", "Kontak")}
        <li>{wa("nav__cta", "WA", "Halo Saideo Surabaya, saya mau pesan.")}</li>
      </ul>
    </nav>
  </div>
</header>"""


def kaki_2():
    return f"""
<footer class="kaki">
  <div class="wrap kaki__isi">
    <div>
      <p class="kaki__merek">SAIDEO<span>/SBY</span></p>
      <p>{escape(SITE['catatan_pratinjau'])}</p>
    </div>
    <div class="kaki__tautan">
      <a href="/arah-2/produk/">Produk</a>
      <a href="/arah-2/mitra/">Mitra</a>
      <a href="/arah-2/tentang/">Tentang</a>
      <a href="/arah-2/kontak/">Kontak</a>
      <a href="{escape(SITE['instagram'])}" target="_blank" rel="noopener">Instagram {escape(SITE['handle'])}</a>
      {shopee("", "Shopee resmi")}
      {wa("", "WhatsApp")}
    </div>
  </div>
</footer>"""


def nav_3(aktif):
    def item(kunci, href, teks):
        tanda = ' aria-current="page"' if aktif == kunci else ""
        return '<li><a href="%s"%s>%s</a></li>' % (href, tanda, teks)
    return f"""
<header class="kepala">
  <div class="wrap kepala__bar">
    <a class="merek" href="/arah-3/">Saideo <span>Surabaya</span></a>
    <button class="menu-tombol" type="button" data-nav-tombol aria-expanded="false" aria-controls="nav-utama">
      <span class="menu-tombol__garis" aria-hidden="true"></span>Menu
    </button>
    <nav class="nav" id="nav-utama" data-nav data-terbuka="false" aria-label="Navigasi utama">
      <ul>
        {item("produk", "/arah-3/produk/", "Produk")}
        {item("mitra", "/arah-3/mitra/", "Mitra")}
        {item("tentang", "/arah-3/tentang/", "Tentang")}
        {item("kontak", "/arah-3/kontak/", "Kontak")}
        <li>{wa("", "WhatsApp")}</li>
      </ul>
    </nav>
  </div>
</header>"""


def kaki_3():
    return f"""
<footer class="kaki">
  <div class="wrap kaki__isi">
    <div>
      <p class="kaki__merek">Saideo Surabaya</p>
      <p>Deodorant Fresh dari agen resmi Surabaya. Eceran dan mitra mulai 10 pcs.</p>
    </div>
    <div class="kaki__tautan">
      <a href="/arah-3/produk/">Produk</a>
      <a href="/arah-3/mitra/">Mitra</a>
      <a href="/arah-3/tentang/">Tentang</a>
      <a href="/arah-3/kontak/">Kontak</a>
      <a href="{escape(SITE['instagram'])}" target="_blank" rel="noopener">Instagram {escape(SITE['handle'])}</a>
      {shopee("", "Shopee resmi")}
      {wa("", "WhatsApp")}
    </div>
  </div>
  <div class="wrap kaki__bawah"><p>{escape(SITE['catatan_pratinjau'])}</p></div>
</footer>"""


# ------------------------------------------------------------------ blok bersama
def produk_1(img):
    d = img["produk"]
    return f"""
    <div class="etalase-grid">
      <figure class="etalase">
        <img src="/{d['berkas']}" alt="Botol Saideo Deodorant Spray 100 ml di atas meja kerja" width="{d['w']}" height="{d['h']}" loading="lazy" decoding="async">
        <figcaption>Botol 100 ml di meja kerja. Foto dari pemilik akun.</figcaption>
      </figure>
      <div class="produk-lis">{blok_produk("produk", "produk__harga", "tombol tombol--kecil tombol--garis")}</div>
    </div>
    <p class="sumber">Harga mengikuti toko resmi Saideo. Pembelian juga bisa lewat Shopee.</p>"""


def produk_2(img):
    d = img["produk"]
    return f"""
    <figure class="etalase">
      <img src="/{d['berkas']}" alt="Botol Saideo Deodorant Spray 100 ml di atas meja kerja dengan laptop dan ponsel" width="{d['w']}" height="{d['h']}" loading="lazy" decoding="async">
      <figcaption>Botol 100 ml di meja kerja. Foto dari pemilik akun.</figcaption>
    </figure>
    <div class="kartu-grid">{blok_produk("kartu", "kartu__harga", "tombol tombol--penuh")}</div>
    <p class="sumber">Harga mengikuti toko resmi Saideo. Stok wangi tanyakan sebelum memesan.</p>"""


def produk_3(img):
    d = img["produk"]
    return f"""
    <figure class="etalase">
      <img src="/{d['berkas']}" alt="Botol Saideo Deodorant Spray 100 ml di atas meja kerja" width="{d['w']}" height="{d['h']}" loading="lazy" decoding="async">
      <figcaption>
        <span class="etalase__label">Etalase</span>
        <p>Botol spray 100 ml, cukup untuk pemakaian harian.</p>
        <ul class="tag"><li>Non alkohol</li><li>BPOM</li></ul>
      </figcaption>
    </figure>
    <div class="produk-lis">{blok_produk("produk", "produk__harga", "tombol tombol--kecil tombol--garis")}</div>
    <p class="sumber">Harga mengikuti toko resmi Saideo. Bisa juga membeli lewat Shopee.</p>"""


def panel_mitra_1():
    return f"""
<section class="mitra" id="mitra">
  <div class="wrap mitra__grid">
    <div class="mitra__kiri">
      <p class="label label--terang"><span class="label__no">03</span> Buka mitra</p>
      <h2>{escape(MITRA['pembuka'])}</h2>
      <p class="mitra__p">{escape(MITRA['ringkas'])}</p>
      <ul class="mitra__alasan">
        {''.join('<li><strong>%s</strong><span>%s</span></li>' % (escape(j), escape(t)) for j, t in MITRA['alasan'][:3])}
      </ul>
      {wa("tombol tombol--terang", "Tanya paket mitra", SITE["wa_pesan_mitra"])}
    </div>
    <div class="paket">
      <h3 class="paket__judul">Pilihan paket</h3>
      <ul class="paket__list">{blok_paket("paket__baris")}</ul>
      <p class="paket__catatan">Harga paket dikirim lewat WhatsApp karena bergantung jumlah dan isi paket.</p>
    </div>
  </div>
</section>"""


def panel_mitra_2():
    return f"""
<section class="mitra" id="mitra">
  <div class="wrap">
    <div class="mitra__kepala">
      <p class="label label--gelap"><span>02</span> Peluang</p>
      <h2>Buka mitra.<br>Mulai 10 pcs.</h2>
      <p>{escape(MITRA['ringkas'])}</p>
    </div>
    <div class="mitra__grid">
      <ul class="mitra__alasan">
        {''.join('<li><strong>%s</strong><span>%s</span></li>' % (escape(j), escape(t)) for j, t in MITRA['alasan'])}
      </ul>
      <div class="paket">
        <h3 class="paket__judul">Pilihan paket</h3>
        <ul class="paket__list">{blok_paket("paket__baris")}</ul>
        <p class="paket__catatan">Harga paket dikirim lewat WhatsApp karena bergantung jumlah dan isi paket.</p>
        {wa("tombol tombol--gelap", "Chat paket mitra", SITE["wa_pesan_mitra"])}
      </div>
    </div>
    <ol class="langkah langkah--terang">{blok_langkah_mitra("langkah")}</ol>
  </div>
</section>"""


def panel_mitra_3(img):
    paket = "".join(f"""
        <li class="paket__kartu">
          <p class="paket__nama">{escape(n)}</p>
          <p class="paket__jumlah">{escape(j)}</p>
          <p class="paket__catatan">{escape(c)}</p>
        </li>""" for n, j, c in MITRA["paket"])
    return f"""
<section class="mitra" id="mitra">
  <div class="wrap mitra__isi">
    <div class="mitra__teks">
      <p class="label"><span>02</span> Surat dari Surabaya</p>
      <h2>Kalau kamu mau ikut menjual, mulai dari 10 pcs.</h2>
      <p>{escape(MITRA['ringkas'])}</p>
      <ul class="mitra__alasan">
        {''.join('<li><strong>%s</strong><span>%s</span></li>' % (escape(j), escape(t)) for j, t in MITRA['alasan'])}
      </ul>
      {wa("tombol", "Tanya paket mitra", SITE["wa_pesan_mitra"])}
      <p class="mitra__tanda">Agen Saideo Surabaya<br><span>{escape(SITE['handle'])}</span></p>
    </div>
    <div class="mitra__sisi">
      <ul class="paket__grid">{paket}</ul>
      <figure class="mitra__poster">
        <img src="/{img['mitra']['berkas']}" alt="Poster peluang usaha Saideo yang menawarkan kemitraan" width="{img['mitra']['w']}" height="{img['mitra']['h']}" loading="lazy" decoding="async">
        <figcaption>Poster mitra dari pemilik akun.</figcaption>
      </figure>
    </div>
  </div>
</section>"""


def testimoni_1(img):
    return f"""
<section class="bagian" id="testimoni">
  <div class="wrap testimoni">
    <blockquote class="kutipan">
      <p>&ldquo;Biarpun sirkulasi keringat sekali, tidak sampai basah ketiak karena pakai Saideo. Tadi panas sekali dari posyandu pulang jalan kaki, ketiak tidak basah sama sekali.&rdquo;</p>
      <footer>Pesan pembeli lewat WhatsApp</footer>
    </blockquote>
    <figure class="kutipan__foto">
      <img src="/assets/img/testimoni.webp" alt="Tangkapan layar percakapan WhatsApp berisi pujian pembeli terhadap Saideo" width="{img['testimoni']['w']}" height="{img['testimoni']['h']}" loading="lazy" decoding="async">
      <figcaption>Tangkapan layar chat yang dikirim pemilik akun.</figcaption>
    </figure>
  </div>
</section>"""


def testimoni_2(img):
    return f"""
<section class="bagian" id="suara">
  <div class="wrap suara">
    <blockquote>
      <p>&ldquo;Biarpun sirkulasi keringat sekali, tidak sampai basah ketiak karena pakai Saideo. Tadi panas sekali dari posyandu pulang jalan kaki, ketiak tidak basah sama sekali.&rdquo;</p>
      <footer>Pesan pembeli lewat WhatsApp</footer>
    </blockquote>
    <figure>
      <img src="/assets/img/testimoni.webp" alt="Tangkapan layar percakapan WhatsApp berisi pujian pembeli terhadap Saideo" width="{img['testimoni']['w']}" height="{img['testimoni']['h']}" loading="lazy" decoding="async">
    </figure>
  </div>
</section>"""


def testimoni_3(img):
    return f"""
<section class="bagian" id="suara">
  <div class="wrap suara">
    <blockquote>
      <p>&ldquo;Biarpun sirkulasi keringat sekali, tidak sampai basah ketiak karena pakai Saideo. Tadi panas sekali dari posyandu pulang jalan kaki, ketiak tidak basah sama sekali.&rdquo;</p>
      <footer>Pesan pembeli lewat WhatsApp</footer>
    </blockquote>
    <figure>
      <img src="/assets/img/testimoni.webp" alt="Tangkapan layar percakapan WhatsApp berisi pujian pembeli terhadap Saideo" width="{img['testimoni']['w']}" height="{img['testimoni']['h']}" loading="lazy" decoding="async">
    </figure>
  </div>
</section>"""


# ------------------------------------------------------------------ halaman dalam
def isi_produk(blok):
    return kepala_dalam(
        "01", "Produk",
        "Tiga kemasan Saideo, harga tertulis.",
        "Semua deodorant spray untuk pemakaian harian. Stok wangi bisa berbeda tiap kiriman, tanyakan yang tersedia sebelum memesan.",
    ) + f"""
<section class="bagian">
  <div class="wrap">
    {blok}
    <div class="d-dua d-dua--jarak">
      <div>
        <p class="label"><span>02</span> Cara pesan</p>
        <h2>Tiga langkah, tanpa aplikasi baru.</h2>
        <p class="d-intro">Semua pesanan dicatat lewat chat atau Shopee, lalu dikirim dari Surabaya. Sebutkan kemasan dan jumlah supaya balasannya langsung berisi total.</p>
      </div>
      <ol class="langkah">{blok_langkah_pesan()}</ol>
    </div>
    <div class="d-catatan">
      <p>COD dan pengambilan di <strong>Perak Utara, Surabaya</strong>.</p>
      {shopee("tautan", "Buka toko resmi di Shopee")}
    </div>
  </div>
</section>"""


def isi_mitra(panel):
    return kepala_dalam(
        "01", "Buka mitra",
        MITRA["pembuka"],
        MITRA["ringkas"],
    ) + panel + f"""
<section class="bagian">
  <div class="wrap">
    <div class="bagian__kepala">
      <div>
        <p class="label"><span>03</span> Pertanyaan</p>
        <h2>Yang sering ditanya calon mitra.</h2>
      </div>
      <p>Kalau ada yang belum terjawab, tanyakan lewat WhatsApp. Kami balas dengan rincian paket yang tersedia.</p>
    </div>
    <div class="d-faq">{blok_faq()}</div>
  </div>
</section>"""


def isi_tentang(img, testimoni):
    return kepala_dalam(
        "01", "Tentang",
        "Agen Saideo di Surabaya.",
        "Saideo Surabaya menjual Saideo Deodorant Fresh langsung dari Surabaya. Barang bisa diambil atau COD di Perak Utara, atau dikirim lewat kurir.",
    ) + f"""
<section class="bagian">
  <div class="wrap">
    <div class="d-dua">
      <div>
        <p class="label"><span>02</span> Kenapa lewat agen</p>
        <h2>Barang dari Surabaya, bisa diambil langsung.</h2>
        <p class="d-intro">Semua produk berasal dari merek Saideo. Keterangan yang dipakai di situs ini mengikuti label dan toko resmi: non alkohol, aktif seharian, dan mencantumkan BPOM. Foto berasal dari pemilik akun.</p>
        <ul class="d-fakta">{blok_fakta()}</ul>
      </div>
      <figure class="d-foto">
        <img src="/{img['agen']['berkas']}" alt="Poster Saideo Authorized Surabaya dengan botol produk" width="{img['agen']['w']}" height="{img['agen']['h']}" loading="lazy" decoding="async">
        <figcaption>Poster agen resmi dari pemilik akun.</figcaption>
      </figure>
    </div>
  </div>
</section>
{testimoni}"""


def isi_kontak():
    return kepala_dalam(
        "01", "Kontak",
        "Pesan, bayar, lalu ambil atau kirim.",
        "Semua pesanan diproses lewat WhatsApp atau Shopee. Untuk COD dan pengambilan, barang disiapkan di Perak Utara, Surabaya.",
    ) + f"""
<section class="bagian">
  <div class="wrap">
    <div class="d-grid3">
      <div class="d-kartu">
        <h2>WhatsApp</h2>
        <p>Tanya stok, pilih kemasan, lalu atur COD atau kirim.</p>
        <p class="d-kecil">Nomor khusus website menyusul. Tombol ini mengarah ke tautan yang tercantum di bio Instagram.</p>
        {wa("tombol tombol--kecil", "Chat WhatsApp")}
      </div>
      <div class="d-kartu">
        <h2>Shopee</h2>
        <p>Beli lewat toko resmi kalau lebih nyaman memakai marketplace.</p>
        <p class="d-kecil">Toko resmi Saideo, bukan lapak lain.</p>
        {shopee("tautan", "Buka toko resmi")}
      </div>
      <div class="d-kartu">
        <h2>Instagram</h2>
        <p>Foto produk dan info stok kadang diunggah di akun agen.</p>
        <p class="d-kecil">{escape(SITE['handle'])}</p>
        <a class="tautan" href="{escape(SITE['instagram'])}" target="_blank" rel="noopener">Buka Instagram</a>
      </div>
    </div>
    <div class="d-dua d-dua--jarak">
      <div class="d-kartu">
        <h2>COD dan pengambilan</h2>
        <p>Perak Utara, Surabaya. Bayar di tempat atau ambil setelah pesanan dikonfirmasi lewat chat.</p>
        <a class="tautan" href="{escape(MAPS)}" target="_blank" rel="noopener">Buka Google Maps</a>
      </div>
      <div class="d-kartu">
        <h2>Jam layanan</h2>
        <p>Jam layanan menyusul dari pemilik akun.</p>
        <p class="d-kecil">Sementara ini balasan mengikuti jam operasional agen di Instagram.</p>
      </div>
    </div>
  </div>
</section>"""


# ------------------------------------------------------------------ arah 1
def arah_1(img):
    mitra = panel_mitra_1()
    testimoni = testimoni_1(img)
    return kepala(
        "Saideo Surabaya, deodorant spray non alkohol",
        "Saideo Deodorant Fresh dari agen resmi Surabaya. Harga mulai Rp25.000 untuk botol 100 ml, non alkohol, bisa COD di Perak Utara atau kirim dari Surabaya. Buka mitra mulai 10 pcs.",
        "arah-1.css", "#F5F8F6", FONTS_1, "/arah-1/",
    ) + nav_1("beranda") + f"""
<main id="utama">
<section class="hero">
  <div class="wrap hero__grid">
    <div class="hero__teks">
      <p class="kicker">Agen resmi Saideo Surabaya</p>
      <h1>Ketiak kering dan wangi seharian, tanpa alkohol.</h1>
      <p class="hero__p">Saideo Deodorant Fresh untuk pemakaian harian. Dijual langsung oleh agen Surabaya, mulai Rp25.000 per botol 100 ml. Bisa COD di Perak Utara atau dikirim dari Surabaya.</p>
      <div class="aksi">
        {wa("tombol", "Pesan lewat WhatsApp")}
        <a class="tombol tombol--garis" href="/arah-1/produk/">Lihat produk</a>
      </div>
      <ul class="poin">
        <li>Non alkohol</li>
        <li>BPOM</li>
        <li>COD Perak Utara</li>
      </ul>
    </div>
    <figure class="hero__foto">
      <img src="/{img['dinding']['berkas']}" alt="Deretan botol Saideo 100 ml berjejer di atas latar kayu" width="{img['dinding']['w']}" height="{img['dinding']['h']}" fetchpriority="high" decoding="async">
      <figcaption>Botol Saideo 100 ml. Foto dari agen Surabaya.</figcaption>
    </figure>
  </div>
</section>

<section class="bagian" id="produk">
  <div class="wrap">
    <div class="bagian__kepala">
      <div>
        <p class="label"><span class="label__no">01</span> Produk dan harga</p>
        <h2>Tiga pilihan, harga tertulis.</h2>
      </div>
      <p>Semua untuk pemakaian harian. Stok wangi bisa berbeda tiap kiriman, jadi tanyakan yang tersedia sebelum memesan.</p>
    </div>
    {produk_1(img)}
    <p class="d-lanjut"><a class="tautan" href="/arah-1/produk/">Lihat halaman produk dan cara pesan</a></p>
  </div>
</section>

<section class="bagian bagian--alasan">
  <div class="wrap">
    <div class="bagian__kepala">
      <div>
        <p class="label"><span class="label__no">02</span> Alasan memilih</p>
        <h2>Yang tercatat di produknya.</h2>
      </div>
    </div>
    <ul class="alasan-grid">
      <li><h3>Non alkohol</h3><p>Keterangan produk resmi menyebut formulanya tanpa alkohol, jadi tetap nyaman untuk pemakaian harian.</p></li>
      <li><h3>BPOM</h3><p>Merek mencantumkan keterangan BPOM pada produknya. Nomor izin edar menyusul di halaman ini.</p></li>
      <li><h3>Dari agen Surabaya</h3><p>Barang dikirim dari Surabaya, bisa diambil atau COD di Perak Utara.</p></li>
      <li><h3>Bisa ecer atau mitra</h3><p>Beli satu botol untuk mencoba, atau ambil 10 pcs untuk dijual lagi.</p></li>
    </ul>
  </div>
</section>

{mitra}

{testimoni}

<section class="bagian" id="cara">
  <div class="wrap">
    <div class="bagian__kepala">
      <div>
        <p class="label"><span class="label__no">04</span> Cara pesan</p>
        <h2>Tiga langkah, tanpa aplikasi baru.</h2>
      </div>
      <p>Semua pesanan dicatat lewat chat atau Shopee, lalu dikirim dari Surabaya.</p>
    </div>
    <ol class="langkah">{blok_langkah_pesan()}</ol>
    <div class="info-cod">
      <p>COD dan pengambilan di <strong>Perak Utara, Surabaya</strong>.</p>
      {shopee("tautan", "Buka toko resmi di Shopee")}
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap cta__isi">
    <div>
      <h2>Mau coba satu botol atau langsung 10 pcs?</h2>
      <p>Sebutkan kemasan dan jumlahnya. Untuk paket mitra, sebutkan juga area pengiriman.</p>
    </div>
    <div class="cta__aksi">
      {wa("tombol", "Chat WhatsApp")}
      {wa("tombol tombol--garis", "Tanya paket mitra", SITE["wa_pesan_mitra"])}
    </div>
  </div>
</section>
</main>
""" + kaki_1() + tutup()


def halaman_1(aktif, judul, deskripsi, path, isi):
    return kepala(judul, deskripsi, "arah-1.css", "#F5F8F6", FONTS_1, path) + nav_1(aktif) + \
        '<main id="utama">' + isi + "</main>" + kaki_1() + tutup()


# ------------------------------------------------------------------ arah 2
def arah_2(img):
    mitra = panel_mitra_2()
    return kepala(
        "Saideo Surabaya, sai goodbye bau badan",
        "Deodorant spray Saideo dari agen resmi Surabaya. Non alkohol, BPOM, aktif seharian. Mulai Rp25.000, COD Perak Utara, buka mitra mulai 10 pcs.",
        "arah-2.css", "#0C0D10", FONTS_2, "/arah-2/",
    ) + nav_2("beranda") + f"""
<main id="utama">
<section class="hero">
  <div class="wrap">
    <p class="kicker">Agen resmi / Surabaya</p>
    <h1>Sai goodbye <span>bau badan.</span></h1>
    <div class="hero__bawah">
      <div>
        <p class="hero__p">Deodorant spray non alkohol untuk pemakaian harian. Dijual langsung dari Surabaya, bisa COD di Perak Utara atau dikirim lewat kurir.</p>
        <div class="aksi">
          {wa("tombol", "Pesan sekarang")}
          <a class="tombol tombol--garis" href="/arah-2/mitra/">Buka mitra</a>
        </div>
      </div>
      <div class="hero__sisi">
        <div class="hero__angka">
          <strong>10 pcs</strong>
          <span>jumlah awal untuk mulai jadi mitra</span>
        </div>
        <figure class="hero__poster">
          <img src="/{img['agen']['berkas']}" alt="Poster Saideo Authorized Surabaya dengan botol produk" width="{img['agen']['w']}" height="{img['agen']['h']}" loading="lazy" decoding="async">
          <figcaption>Poster agen resmi dari pemilik akun.</figcaption>
        </figure>
      </div>
    </div>
  </div>
</section>

<figure class="panggung">
  <img src="/{img['dinding']['berkas']}" alt="Puluhan botol Saideo 100 ml tersusun dalam panel di latar kayu" width="{img['dinding']['w']}" height="{img['dinding']['h']}" fetchpriority="high" decoding="async">
  <figcaption>Botol 100 ml, stok agen Surabaya.</figcaption>
</figure>

<div class="pita">
  <div class="wrap">
    <ul>
      <li>Non alkohol</li>
      <li>BPOM</li>
      <li>COD Perak Utara</li>
      <li>Kirim dari Surabaya</li>
      <li>Mitra mulai 10 pcs</li>
    </ul>
  </div>
</div>

<section class="bagian" id="produk">
  <div class="wrap">
    <div class="bagian__kepala">
      <p class="label"><span>01</span> Harga</p>
      <h2>Pilih botolnya.</h2>
    </div>
    {produk_2(img)}
    <p class="d-lanjut"><a class="tautan" href="/arah-2/produk/">Lihat halaman produk</a></p>
  </div>
</section>

{mitra}

{testimoni_2(img)}

<section class="bagian" id="cara">
  <div class="wrap">
    <div class="bagian__kepala">
      <p class="label"><span>03</span> Order</p>
      <h2>Tiga jalur, satu barang.</h2>
    </div>
    <div class="kanal">
      <div class="kanal__kartu">
        <h3>WhatsApp</h3>
        <p>Tanya stok, pilih kemasan, lalu atur COD atau kirim.</p>
        {wa("tautan", "Chat sekarang")}
      </div>
      <div class="kanal__kartu">
        <h3>Shopee</h3>
        <p>Beli lewat toko resmi kalau lebih nyaman memakai marketplace.</p>
        {shopee("tautan", "Buka Shopee")}
      </div>
      <div class="kanal__kartu">
        <h3>COD Perak Utara</h3>
        <p>Ambil langsung di Perak Utara, Surabaya. Bayar di tempat.</p>
        {wa("tautan", "Atur waktu ambil")}
      </div>
    </div>
  </div>
</section>
</main>
""" + kaki_2() + tutup()


def halaman_2(aktif, judul, deskripsi, path, isi):
    return kepala(judul, deskripsi, "arah-2.css", "#0C0D10", FONTS_2, path) + nav_2(aktif) + \
        '<main id="utama">' + isi + "</main>" + kaki_2() + tutup()


# ------------------------------------------------------------------ arah 3
def arah_3(img):
    mitra = panel_mitra_3(img)
    testimoni = testimoni_3(img)
    return kepala(
        "Saideo Surabaya, deodorant untuk dipakai dan dijual",
        "Saideo Deodorant Fresh dari agen resmi Surabaya. Beli satuan mulai Rp25.000, atau buka mitra mulai 10 pcs. COD Perak Utara, kirim dari Surabaya.",
        "arah-3.css", "#FBF3E7", FONTS_3, "/arah-3/",
    ) + nav_3("beranda") + f"""
<main id="utama">
<section class="hero">
  <div class="wrap hero__isi">
    <p class="kicker">Agen resmi Saideo Surabaya</p>
    <h1>Wangi yang menemanimu seharian.</h1>
    <p class="hero__p">Deodorant spray non alkohol dalam botol 100 ml. Dijual satuan mulai Rp25.000, dan terbuka untuk kamu yang mau ikut menjualnya mulai 10 pcs.</p>
    <figure class="hero__foto">
      <img src="/{img['dinding']['berkas']}" alt="Deretan botol Saideo 100 ml berjejer di atas latar kayu" width="{img['dinding']['w']}" height="{img['dinding']['h']}" fetchpriority="high" decoding="async">
      <figcaption>Botol Saideo 100 ml, stok agen Surabaya.</figcaption>
    </figure>
  </div>
</section>

<section class="jalur">
  <div class="wrap jalur__grid">
    <a class="jalur__kartu" href="/arah-3/produk/">
      <span class="jalur__label">Untuk pemakai</span>
      <h2>Beli satuan</h2>
      <p>Satu botol untuk dicoba, atau bundling dua botol dengan harga lebih ringan.</p>
      <span class="jalur__panah">Lihat produk</span>
    </a>
    <a class="jalur__kartu jalur__kartu--mitra" href="/arah-3/mitra/">
      <span class="jalur__label">Untuk penjual</span>
      <h2>Jadi mitra</h2>
      <p>Mulai 10 pcs, diambil atau dikirim dari Perak Utara, Surabaya.</p>
      <span class="jalur__panah">Lihat paket</span>
    </a>
  </div>
</section>

<section class="bagian" id="produk">
  <div class="wrap">
    <div class="bagian__kepala">
      <div>
        <p class="label"><span>01</span> Produk</p>
        <h2>Tiga cara membeli.</h2>
      </div>
      <p>Harga tertulis, tanpa perlu tanya dulu. Stok wangi bisa berbeda tiap kiriman.</p>
    </div>
    {produk_3(img)}
    <p class="d-lanjut"><a class="tautan" href="/arah-3/produk/">Lihat halaman produk dan cara pesan</a></p>
  </div>
</section>

{mitra}

{testimoni}

<section class="bagian" id="cara">
  <div class="wrap">
    <div class="bagian__kepala">
      <div>
        <p class="label"><span>03</span> Cara pesan</p>
        <h2>Dari chat sampai barang di tangan.</h2>
      </div>
      <p>COD dan pengambilan di <strong>Perak Utara, Surabaya</strong>, atau kirim lewat kurir.</p>
    </div>
    <ol class="langkah">{blok_langkah_pesan()}</ol>
  </div>
</section>

<section class="cta">
  <div class="wrap cta__isi">
    <div>
      <h2>Mau beli satu, atau mulai jualan?</h2>
      <p>Sebutkan kemasan dan jumlahnya. Untuk paket mitra, sebutkan juga area pengiriman.</p>
    </div>
    <div class="cta__aksi">
      {wa("tombol", "Chat WhatsApp")}
      {shopee("tombol tombol--garis", "Buka Shopee")}
    </div>
  </div>
</section>
</main>
""" + kaki_3() + tutup()


def halaman_3(aktif, judul, deskripsi, path, isi):
    return kepala(judul, deskripsi, "arah-3.css", "#FBF3E7", FONTS_3, path) + nav_3(aktif) + \
        '<main id="utama">' + isi + "</main>" + kaki_3() + tutup()


# ------------------------------------------------------------------ pemilih
def halaman_pemilih():
    kartu = []
    for a in ARAH["arah"]:
        swatch = "".join(
            '<li><span class="contoh" style="background:%s" aria-hidden="true"></span>%s<code>%s</code></li>'
            % (escape(w), escape(n), escape(w)) for n, w in a["palet"]
        )
        kartu.append(f"""
      <article class="kartu">
        <div class="kartu__kepala">
          <p class="kartu__nomor">{escape(a['slug'].split('-')[1])}</p>
          <h2>{escape(a['nama'])}</h2>
          <p class="kartu__dial">{escape(a['dial'])}</p>
        </div>
        <p class="kartu__ringkas">{escape(a['ringkas'])}</p>
        <p class="kartu__cocok">{escape(a['cocok'])}</p>
        <ul class="palet">{swatch}</ul>
        <a class="tombol" href="/{escape(a['slug'])}/">Buka mockup {escape(a['nama'])}</a>
      </article>""")
    return kepala(
        "Tiga arah desain untuk Saideo Surabaya",
        "Pratinjau tiga arah desain situs Saideo Surabaya: Bersih Klinis, Kota Malam, dan Hangat Personal. Setiap arah lima halaman, dengan jalur pembelian dan jalur mitra.",
        "pemilih.css", "#F2EFE9", "family=Plus+Jakarta+Sans:wght@400;500;600;700", "/",
    ) + f"""
<main id="utama" class="pilih">
  <div class="wrap">
    <p class="kicker">Pratinjau desain</p>
    <h1>{escape(ARAH['judul'])}</h1>
    <p class="pilih__intro">{escape(ARAH['intro'])}</p>
    <div class="pilih__grid">{''.join(kartu)}</div>
    <div class="pilih__catatan">
      <h2>Yang sama di ketiganya</h2>
      <ul>
        <li>Lima halaman: beranda, produk, mitra, tentang, kontak.</li>
        <li>Harga, produk, dan isi program mitra berasal dari data yang sama.</li>
        <li>Tombol WhatsApp memakai tautan yang tercantum di bio Instagram.</li>
        <li>Foto memakai berkas yang dikirim pemilik akun, tanpa stok foto.</li>
      </ul>
      <p>{escape(SITE['catatan_pratinjau'])}</p>
    </div>
  </div>
</main>
<footer class="kaki">
  <div class="wrap kaki__isi">
    <p>Saideo Surabaya / pratinjau desain</p>
    <p><a href="{escape(SITE['instagram'])}" target="_blank" rel="noopener">Instagram {escape(SITE['handle'])}</a></p>
  </div>
</footer>
""" + tutup()


def halaman_404():
    return kepala(
        "Halaman tidak ditemukan, Saideo Surabaya",
        "Halaman yang dicari tidak ada. Kembali ke pratinjau tiga arah desain.",
        "pemilih.css", "#F2EFE9", "family=Plus+Jakarta+Sans:wght@400;500;600;700", "/404.html",
    ) + """
<main id="utama" class="pilih">
  <div class="wrap">
    <p class="kicker">404</p>
    <h1>Halaman ini tidak ada.</h1>
    <p class="pilih__intro">Mungkin tautannya salah ketik. Pratinjau desain ada di halaman depan.</p>
    <p><a class="tombol" href="/">Kembali ke pratinjau</a></p>
  </div>
</main>
""" + tutup()


def tulis(path, isi):
    tujuan = os.path.join(DIST, path)
    os.makedirs(os.path.dirname(tujuan) or DIST, exist_ok=True)
    with open(tujuan, "w", encoding="utf-8", newline="\n") as f:
        f.write(isi)


def salin_aset():
    for nama in ("arah-1.css", "arah-2.css", "arah-3.css", "pemilih.css"):
        shutil.copy(os.path.join(ROOT, "assets", "css", nama), os.path.join(DIST, "assets", "css", nama))
    shutil.copy(os.path.join(ROOT, "assets", "js", "site.js"), os.path.join(DIST, "assets", "js", "site.js"))


def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(IMG, exist_ok=True)
    os.makedirs(os.path.join(DIST, "assets", "css"), exist_ok=True)
    os.makedirs(os.path.join(DIST, "assets", "js"), exist_ok=True)

    img = siapkan_gambar()

    tulis("index.html", halaman_pemilih())
    tulis("404.html", halaman_404())

    tulis("arah-1/index.html", arah_1(img))
    tulis("arah-1/produk/index.html", halaman_1(
        "produk", "Produk dan harga Saideo Surabaya",
        "Tiga kemasan Saideo Deodorant Fresh 100 ml dengan harga tertulis. Non alkohol, BPOM, bisa COD di Perak Utara atau kirim dari Surabaya.",
        "/arah-1/produk/", isi_produk(produk_1(img))))
    tulis("arah-1/mitra/index.html", halaman_1(
        "mitra", "Buka mitra Saideo Surabaya mulai 10 pcs",
        "Kemitraan Saideo Surabaya mulai 10 pcs. Harga mitra, bisa diambil atau COD di Perak Utara, atau dikirim dari Surabaya.",
        "/arah-1/mitra/", isi_mitra(panel_mitra_1())))
    tulis("arah-1/tentang/index.html", halaman_1(
        "tentang", "Tentang Saideo Surabaya, agen resmi",
        "Agen resmi Saideo Deodorant Fresh di Surabaya. Non alkohol, keterangan BPOM, COD Perak Utara, dan kirim dari Surabaya.",
        "/arah-1/tentang/", isi_tentang(img, testimoni_1(img))))
    tulis("arah-1/kontak/index.html", halaman_1(
        "kontak", "Kontak Saideo Surabaya",
        "WhatsApp, Shopee, Instagram, dan lokasi COD Saideo Surabaya di Perak Utara.",
        "/arah-1/kontak/", isi_kontak()))

    tulis("arah-2/index.html", arah_2(img))
    tulis("arah-2/produk/index.html", halaman_2(
        "produk", "Produk dan harga Saideo Surabaya",
        "Tiga kemasan Saideo Deodorant Fresh 100 ml dengan harga tertulis. Non alkohol, BPOM, bisa COD di Perak Utara.",
        "/arah-2/produk/", isi_produk(produk_2(img))))
    tulis("arah-2/mitra/index.html", halaman_2(
        "mitra", "Buka mitra Saideo Surabaya mulai 10 pcs",
        "Kemitraan Saideo Surabaya mulai 10 pcs. Harga mitra, bisa diambil atau COD di Perak Utara, atau dikirim dari Surabaya.",
        "/arah-2/mitra/", isi_mitra(panel_mitra_2())))
    tulis("arah-2/tentang/index.html", halaman_2(
        "tentang", "Tentang Saideo Surabaya, agen resmi",
        "Agen resmi Saideo Deodorant Fresh di Surabaya. Non alkohol, keterangan BPOM, COD Perak Utara, dan kirim dari Surabaya.",
        "/arah-2/tentang/", isi_tentang(img, testimoni_2(img))))
    tulis("arah-2/kontak/index.html", halaman_2(
        "kontak", "Kontak Saideo Surabaya",
        "WhatsApp, Shopee, Instagram, dan lokasi COD Saideo Surabaya di Perak Utara.",
        "/arah-2/kontak/", isi_kontak()))

    tulis("arah-3/index.html", arah_3(img))
    tulis("arah-3/produk/index.html", halaman_3(
        "produk", "Produk dan harga Saideo Surabaya",
        "Tiga kemasan Saideo Deodorant Fresh 100 ml dengan harga tertulis. Non alkohol, BPOM, bisa COD di Perak Utara.",
        "/arah-3/produk/", isi_produk(produk_3(img))))
    tulis("arah-3/mitra/index.html", halaman_3(
        "mitra", "Buka mitra Saideo Surabaya mulai 10 pcs",
        "Kemitraan Saideo Surabaya mulai 10 pcs. Harga mitra, bisa diambil atau COD di Perak Utara, atau dikirim dari Surabaya.",
        "/arah-3/mitra/", isi_mitra(panel_mitra_3(img))))
    tulis("arah-3/tentang/index.html", halaman_3(
        "tentang", "Tentang Saideo Surabaya, agen resmi",
        "Agen resmi Saideo Deodorant Fresh di Surabaya. Non alkohol, keterangan BPOM, COD Perak Utara, dan kirim dari Surabaya.",
        "/arah-3/tentang/", isi_tentang(img, testimoni_3(img))))
    tulis("arah-3/kontak/index.html", halaman_3(
        "kontak", "Kontak Saideo Surabaya",
        "WhatsApp, Shopee, Instagram, dan lokasi COD Saideo Surabaya di Perak Utara.",
        "/arah-3/kontak/", isi_kontak()))

    salin_aset()

    tulis("robots.txt", "User-agent: *\nAllow: /\n")
    tulis("_headers", "/assets/*\n  Cache-Control: public, max-age=604800\n/*\n  Cache-Control: public, max-age=3600\n")

    ukuran = 0
    jumlah = 0
    halaman = 0
    for akar, _d, berkas in os.walk(DIST):
        for b in berkas:
            jumlah += 1
            ukuran += os.path.getsize(os.path.join(akar, b))
            if b.endswith(".html"):
                halaman += 1
    print("halaman: %d" % halaman)
    print("berkas: %d, total %.1f KB" % (jumlah, ukuran / 1024))


if __name__ == "__main__":
    main()
