# STATUS - ringkasan kerja sesi 18 November 2026

Dokumen ini untuk melanjutkan pekerjaan tanpa perlu membaca ulang riwayat chat.
Kalau ada yang bertentangan, `data/*.json` dan `build.py` yang berlaku.

## Keadaan sekarang

| Hal | Nilai |
|---|---|
| Live | https://mockup-saideo-surabaya.pages.dev |
| Repo | `alifvir/umkm-saideo-surabaya`, publik, branch `main` |
| Commit terakhir | `297dc0e` |
| Build | 17 halaman, 31 berkas, sekitar 571 KB |
| Audit | 0 masalah, 20 pasangan kontras lolos |
| Deploy | Cloudflare Pages, `<project>` otomatis build dari `main` |

Proyek ini mockup untuk calon klien, bukan situs final. Jangan deploy ke domain
klien sebelum arah desain dipilih.

## Tiga arah

| Arah | Nama | Tipografi | Ciri |
|---|---|---|---|
| 1 | Bersih Klinis | Bricolage Grotesque | latar Cloud Blue, kartu putih, garis tipis |
| 2 | Kota Malam | Anton | latar Midnight Blue, huruf besar, aksen Powder Sky |
| 3 | Lembut Personal | Fraunces | kartu membulat, dua jalur di bawah pembuka |

Lima halaman per arah: beranda, produk, mitra, tentang, kontak. Plus halaman
pemilih di `/` dan `404.html`.

## Palet (permintaan klien)

Cloud Blue `#EDF4FA`, Powder Sky `#CFE3F1`, Calm Ocean `#8FB6D8`,
Dusty Denim `#5F86A6`, Midnight Blue `#243A5E`.

Dua turunan untuk teks: `#4A627D` (redup) dan `#46688C` (harga/label).
Dusty Denim hanya untuk bingkai foto dan hover karena 3.47:1 di atas Cloud Blue.

## Yang dikerjakan di sesi ini

1. Palet lama (hijau, krem, kuning) diganti seluruhnya ke palet biru klien.
2. `arah-3` berganti nama dari Hangat Personal menjadi Lembut Personal.
3. Sisa `rgba()` lama di header arah 1 dan 3 diperbaiki (penyebab header krem).
4. Bayangan dan hover coklat di arah 3 diganti biru. Satu garis krem di chip tag.
5. Nama merek arah 3 diberi jarak; sebelumnya menempel karena `inline-flex`.
6. Cache: gambar 7 hari, CSS dan JS `must-revalidate`. Aturan `/*` dihapus agar
   header tidak ganda.

## Aturan kerja yang wajib dipegang

- Jangan menjalankan server lokal atau pratinjau di foreground. Pratinjau hanya
  kalau user memintanya, lewat background tersembunyi dan dimatikan setelahnya.
- Verifikasi default tanpa server: `python build.py`, `python tools/audit.py`,
  lalu cek URL live.
- Jangan ubah `data/produk.json` tanpa angka dari klien atau toko resmi.

## Menunggu klien

1. Nomor WhatsApp khusus website. Sekarang memakai tautan bio Instagram.
2. Konfirmasi harga Rp30.000 kemasan eksklusif (Rp25.000 dan Rp42.000 dari Shopee).
3. Nomor BPOM.
4. Nama varian wangi.
5. Jumlah paket mitra tingkat toko dan grosir.
6. Alamat lengkap Perak Utara dan jam layanan.
7. Izin memakai tangkapan layar chat sebagai testimoni.
8. Foto kemasan eksklusif dan bundling.

Daftar lengkap ada di `README.md` bagian "Yang menunggu klien".

## Langkah berikutnya

1. Klien memilih satu arah. Setelah itu hapus dua folder `arah-*` lain dari
   `build.py` dan `dist`, atau arahkan `/` langsung ke arah terpilih.
2. Isi `wa` di `data/site.json`, lalu build ulang. Semua tombol ikut berubah.
3. `pratinjau/` masih tangkapan layar palet lama. Regenerasi hanya kalau diminta,
   karena butuh server lokal sementara.
4. Setelah domain klien ada, isi `url` di `data/site.json` agar canonical dan
   sitemap aktif.
