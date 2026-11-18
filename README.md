# Saideo Surabaya - tiga arah desain, lima halaman per arah

Pratinjau desain untuk calon klien Saideo Surabaya (@agensaideo.sby). Tiga arah
visual, isi dan harga sama, semuanya memuat jalur pembelian dan jalur mitra.

Bukan situs final. Harga, nomor WhatsApp, dan beberapa keterangan masih menunggu
konfirmasi pemilik (lihat bagian "Yang menunggu klien").

## Halaman

| Rute | Isi |
|---|---|
| `/` | Pemilih arah desain, alasan tiap arah, contoh palet |
| `/arah-N/` | Beranda: hero, produk ringkas, alasan, mitra, testimoni, cara pesan |
| `/arah-N/produk/` | Etalase, tiga kemasan, harga, cara pesan |
| `/arah-N/mitra/` | Panel mitra, paket, langkah, pertanyaan yang sering diajukan |
| `/arah-N/tentang/` | Profil agen, fakta produk, poster agen, testimoni |
| `/arah-N/kontak/` | WhatsApp, Shopee, Instagram, COD Perak Utara, jam layanan |
| `/404.html` | Halaman tidak ditemukan |

`N` adalah 1, 2, atau 3. Jadi total 17 halaman.

`pratinjau/` berisi tangkapan layar untuk dikirim ke klien: lima halaman desktop
per arah di `pratinjau/arah-N/`, beranda versi HP, dan halaman pemilih.

## Struktur

```
build.py              generator 17 halaman + potong gambar + favicon + OG
data/site.json        identitas, tautan, catatan pratinjau
data/produk.json      produk dan harga
data/mitra.json       isi program mitra
data/arah.json        palet, dial, dan pasangan kontras yang diaudit
assets/css/           arah-1.css, arah-2.css, arah-3.css, pemilih.css
assets/js/site.js     menu mobile saja
assets-src/           foto asli dari pemilik akun
tools/audit.py        pemeriksaan hasil build
pratinjau/            tangkapan layar
dist/                 hasil build, diabaikan git
```

Halaman dalam ketiga arah memakai kerangka kelas yang sama (`d-kepala`, `d-dua`,
`d-kartu`, `d-faq`, `d-fakta`) tetapi gayanya ditulis ulang per arah, jadi
tipografi, warna, dan sudut mengikuti arah masing-masing.

## Perintah

```bash
pip install -r requirements.txt
python build.py
python tools/audit.py
```

`tools/audit.py` harus berakhir `masalah: 0`. Yang diperiksa: satu `h1`, `lang`,
title, description, OG, em dash, emoji, tautan mati, anchor, aset hilang, alt dan
ukuran gambar, tautan kosong, `noopener`, format harga, dan 20 pasangan kontras.

Pratinjau lokal memakai server, bukan `file://`:

```bash
cd dist
python -m http.server 8899
```

Lalu buka `http://127.0.0.1:8899/`.

Catatan: hentikan server sebelum menjalankan `python build.py`. Windows tidak
mengizinkan folder `dist` dihapus saat masih dipakai server.

## Cara mengubah isi

- Harga: `data/produk.json`, lalu `python build.py`. Angka tampil di semua halaman
  karena semua membaca data yang sama.
- Isi program mitra: `data/mitra.json`.
- Nomor WhatsApp: isi `wa` di `data/site.json`. Selama kosong, semua tombol
  mengarah ke `wa_cadangan` (`https://bit.ly/talk-wa`, tautan dari bio Instagram).
- Alamat, Instagram, Shopee: `data/site.json`.
- Teks per arah ada di `build.py`: `nav_1` sampai `nav_3` untuk kepala halaman,
  `isi_produk`, `isi_mitra`, `isi_tentang`, `isi_kontak` untuk isi halaman dalam,
  lalu `arah_1` sampai `arah_3` untuk beranda.
- Foto: ganti berkas di `assets-src/`, lalu build. Nama berkas webp sengaja
  berubah kalau sumbernya berubah, agar pengunjung lama tidak melihat foto lama.

## Hasil uji 18 November 2026

- Build bersih, 17 halaman, total sekitar 571 KB.
- Audit 0 masalah.
- 68 kombinasi halaman dan lebar layar (17 halaman x 320, 390, 768, 1440 px):
  nol overflow, semua gambar termuat, tidak ada target sentuh di bawah 44 px,
  satu `h1` per halaman, font termuat.
- Console bersih di beranda, produk, mitra, tentang, dan kontak.
- Menu mobile arah 1, 2, dan 3: terbuka, tertutup lewat Escape, dan tertutup
  setelah tautan diklik.
- Tombol WhatsApp membuka `https://bit.ly/talk-wa` sesuai bio Instagram klien.

## Yang menunggu klien

1. Nomor WhatsApp khusus website. Sekarang memakai tautan bio.
2. Konfirmasi harga: Rp25.000 (ekonomis 100 ml) dan Rp42.000 (bundling 2 pcs)
   diambil dari toko resmi Saideo di Shopee. Rp30.000 untuk kemasan eksklusif
   berasal dari lapak Shopee lain, perlu dipastikan.
3. Nomor izin edar BPOM. Sekarang hanya ditulis "BPOM".
4. Nama wangi atau varian yang tersedia. Sekarang ditulis "stok wangi bisa
   berbeda, tanyakan lewat WhatsApp".
5. Jumlah paket mitra untuk tingkat toko dan grosir. Sekarang "menyusul".
6. Alamat lengkap pengambilan di Perak Utara dan jam layanan.
7. Izin memakai tangkapan layar chat sebagai testimoni, dan apakah nama perlu
   disensor.
8. Foto produk per kemasan. Sekarang satu foto botol 100 ml dipakai sebagai
   etalase di ketiga arah, dengan potongan berbeda. Foto kemasan eksklusif dan
   bundling belum ada.

## Deploy

Lihat `DEPLOY.md`. Jangan deploy sebelum klien memilih arah desain.
