# Deploy Saideo Surabaya

Deploy baru dilakukan setelah klien memilih satu arah desain. Tiga arah saat ini
berbagi satu build, jadi yang diunggah tetap satu proyek.

## Sebelum deploy

1. Klien memilih arah. Hapus dua arah lain dari `build.py` dan `dist`, atau
   biarkan pemilih di beranda kalau memang ingin ditunjukkan sebagai pilihan.
2. Isi `url` di `data/site.json` setelah alamat Pages diketahui.
3. Ganti nomor WhatsApp di `data/site.json` (kolom `wa`).
4. Konfirmasi harga dan paket mitra.
5. Jalankan build bersih:

```bash
pip install -r requirements.txt
python build.py
python tools/audit.py
```

`tools/audit.py` harus berakhir `masalah: 0` dan `dist/` berisi 17 halaman.

## Urutan: repo dulu, Pages belakangan

Proyek Pages yang dibuat lewat Upload assets tidak bisa dihubungkan ke GitHub
setelahnya. Jadi:

1. Buat repo publik `alifvir/umkm-saideo-surabaya` (satu klien satu repo).
2. Push seluruh isi proyek, termasuk `assets-src/` dan `data/`. Jangan push
   `dist/`.
3. Di Cloudflare: Workers & Pages, Create, Pages, Connect to Git.
4. Setelan build:
   - Framework preset: None
   - Build command: `pip install -r requirements.txt && python build.py`
   - Build output directory: `dist`
   - Root directory: kosong
5. Nama proyek menentukan subdomain, misalnya `saideo-surabaya` menjadi
   `https://saideo-surabaya.pages.dev`. Putuskan sebelum klik pertama.

## Setelah live

1. Isi `url` di `data/site.json` tanpa garis miring di akhir, build ulang, push.
   Dengan `url` terisi, canonical, `og:url`, `sitemap.xml`, dan baris `Sitemap:`
   di `robots.txt` ikut dibuat.
2. Uji alamat produksi:

```bash
for n in 1 2 3; do
  for p in "" produk/ mitra/ tentang/ kontak/; do
    printf "%s " "/arah-$n/$p"
    curl -s -o /dev/null -w "%{http_code}\n" "https://DOMAIN.pages.dev/arah-$n/$p"
  done
done
curl -s -o /dev/null -w "%{http_code}\n" "https://DOMAIN.pages.dev/"
curl -s -o /dev/null -w "%{http_code}\n" "https://DOMAIN.pages.dev/halaman-ngawur"
```

Semua harus 200, kecuali path ngawur yang harus 404 dengan halaman sendiri.
Cloudflare mengalihkan `/404.html` ke `/404` (308), jadi uji juga `/404`.

3. Cek satu tombol WhatsApp di HP: harus membuka tautan WhatsApp dengan pesan
   pembuka yang menyebut produk.
4. Cek thumbnail WhatsApp: kirim tautan ke diri sendiri. Kalau gambar tidak
   muncul, pastikan `og:image` memakai JPEG 1200x630 (`assets/img/og.jpg`) dan
   `url` sudah terisi.

## Catatan teknis

- `_headers` sudah ada: gambar di `/assets/img/*` cache 7 hari, CSS dan JS
  dimuat ulang setiap kunjungan selama fase pratinjau, halaman 1 jam. Nama aset
  tanpa hash, jadi ganti nama berkas setiap ganti gambar.
- Semua path aset absolut (`/assets/...`). Pratinjau lokal wajib lewat server.
- Halaman 404 memakai `404.html` di akar `dist/`.
- Kalau hanya satu arah yang dipakai, hapus dua folder `arah-*` dari `dist` dan
  entri terkait di `main()`.

## Update setelah live

1. Ubah `data/*.json` atau teks di `build.py`.
2. `python build.py` lalu `python tools/audit.py`.
3. `git add -A`, commit, push. Cloudflare membangun ulang otomatis.

Harga tidak berubah sendiri di halaman yang sudah terbit: harus lewat build dan
push.
