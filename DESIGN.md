# DESIGN.md - Saideo Surabaya (tiga mockup)

Dokumen ini menjelaskan tiga arah desain yang dibangun untuk calon klien Saideo
Surabaya. Isi dan harga sama di ketiganya, yang berbeda arah visual, susunan
bagian, dan cara menonjolkan jalur mitra.

Berkas acuan: skill `situs-klien` dan `antislop` mode `during`.

## Kebutuhan klien

Dua jenis pengunjung dalam satu situs:

1. Pembeli satuan: ingin tahu harga, bedanya kemasan, dan cara pesan.
2. Calon mitra: ingin tahu modal awal, apa yang didapat, dan cara mulai.

Karena itu setiap arah dibangun lima halaman: beranda, produk, mitra, tentang,
dan kontak. Jalur mitra punya halaman sendiri supaya bisa dijelaskan panjang,
sementara beranda tetap memuat ringkasannya.

## Struktur lima halaman

| Halaman | Tugas |
|---|---|
| Beranda | Menjawab "ini apa dan harganya berapa" lalu mengarahkan ke dua jalur |
| Produk | Etalase foto, tiga kemasan, harga, cara pesan |
| Mitra | Panel ajakan, alasan, paket, langkah, pertanyaan umum |
| Tentang | Profil agen, fakta produk, poster agen, testimoni |
| Kontak | WhatsApp, Shopee, Instagram, COD, jam layanan |

Halaman dalam ketiga arah memakai kerangka kelas yang sama (`d-kepala`, `d-dua`,
`d-kartu`, `d-faq`, `d-fakta`). Yang berubah per arah hanya token warna,
tipografi, sudut, dan bingkai. Beranda tetap paling khas karena susunan
bagiannya memang berbeda di tiap arah.

## Arah 1 - Bersih Klinis

Dial ENERGY 1 / RHYTHM 2 / MOTION 1.

Design read: halaman produk perawatan harian yang dijual agen resmi, terasa
seperti apotek modern, bukan iklan ramai.

| Token | Nilai | Dipakai untuk |
|---|---|---|
| kertas | #F5F8F6 | latar halaman |
| kartu | #FFFFFF | panel, baris produk |
| tinta | #12231E | teks utama |
| redup | #4E615B | teks penjelas |
| hijau | #0C4A3A | tombol, tautan, pita mitra |
| mint | #DCEBE3 | bagian alasan, ajakan akhir |
| tembaga | #A6431F | harga, nomor bagian |
| garis | #D3E0DA | garis rambut |

Judul memakai Bricolage Grotesque, teks Plus Jakarta Sans. Susunan: hero belah
dua, daftar produk bergaris, empat alasan berkolom, pita hijau untuk mitra,
kutipan dengan tangkapan layar, langkah bernomor.

## Arah 2 - Kota Malam

Dial ENERGY 4 / RHYTHM 3 / MOTION 2.

Design read: poster jalanan Surabaya. Huruf besar dan rapat, latar hampir hitam,
hijau limau sebagai penanda. Paling berani dari ketiganya.

| Token | Nilai | Dipakai untuk |
|---|---|---|
| malam | #0C0D10 | latar halaman |
| panel | #16181D | kartu dan panel |
| garis | #2A2D35 | pemisah |
| kertas | #F2F4F1 | teks utama |
| redup | #A9AFBB | teks penjelas |
| limau | #D8F25A | tombol, harga, aksen |
| biru | #1F49D6 | hanya di palet contoh, belum dipakai |

Judul memakai Anton, teks Plus Jakarta Sans. Susunan: judul raksasa, panggung
foto penuh lebar, pita fakta, tiga kartu produk, blok mitra berlatar limau,
kutipan, tiga jalur order.

## Arah 3 - Hangat Personal

Dial ENERGY 2 / RHYTHM 3 / MOTION 1.

Design read: surat dari agen, bukan katalog. Krem dan tanah liat, serif lembut,
dua jalur langsung di bawah pembuka.

| Token | Nilai | Dipakai untuk |
|---|---|---|
| krem | #FBF3E7 | latar halaman |
| kartu | #FFFBF3 | kartu produk |
| tinta | #33241E | teks utama, panel mitra |
| redup | #6B564B | teks penjelas |
| tanah | #A6472A | tombol, harga, nomor |
| zaitun | #5E6E52 | label kecil |
| sage | #E7E9DC | bagian mitra |
| garis | #E6D6C3 | pemisah |

Judul memakai Fraunces, teks Plus Jakarta Sans. Susunan: hero tengah, dua kartu
jalur (beli satuan dan jadi mitra), daftar produk berpanel, surat mitra dengan
tanda tangan, kutipan, langkah, ajakan gelap.

## Kontras yang diukur

Dihitung, bukan dikira. Semua pasangan di bawah ini lolos AA 4.5:1 dan diperiksa
ulang oleh `tools/audit.py`.

| Arah | Pasangan | Rasio |
|---|---|---|
| 1 | tinta di kertas | 15.29:1 |
| 1 | redup di kertas | 6.17:1 |
| 1 | putih di hijau | 10.21:1 |
| 1 | tembaga di kertas | 5.70:1 |
| 1 | tinta di mint | 13.26:1 |
| 2 | kertas di malam | 17.57:1 |
| 2 | redup di malam | 8.82:1 |
| 2 | limau di malam | 15.52:1 |
| 2 | malam di limau | 15.52:1 |
| 2 | putih di biru | 7.04:1 |
| 2 | redup di panel | 8.06:1 |
| 3 | tinta di krem | 13.51:1 |
| 3 | redup di krem | 6.24:1 |
| 3 | putih di tanah liat | 5.91:1 |
| 3 | tanah liat di krem | 5.36:1 |
| 3 | zaitun di krem | 4.98:1 |
| 3 | tinta di sage | 12.10:1 |
| pemilih | tinta di kertas | 14.85:1 |
| pemilih | redup di kertas | 6.25:1 |
| pemilih | kertas di tinta | 17.04:1 |

## Aturan isi yang dipegang ketiganya

- Satu `h1` per halaman, landmark jelas, tautan lewati isi tersedia.
- Tanpa em dash, tanpa emoji, tanpa ikon set. Ikon hanya tombol WhatsApp karena
  itu penanda fungsi, bukan hiasan.
- Placeholder ditulis apa adanya: jumlah paket yang belum diputuskan memakai
  "menyusul", bukan angka karangan.
- Tidak ada statistik, jumlah pembeli, atau testimoni karangan. Satu kutipan yang
  dipakai berasal dari tangkapan layar chat yang dikirim pemilik akun.
- Klaim produk hanya yang tercatat di akun resmi: non alkohol, BPOM, aktif
  seharian. Nomor izin edar belum ada, jadi tidak dicantumkan.
- Harga satu sumber untuk semua halaman, diambil dari toko resmi Saideo di
  Shopee per 18 November 2026.
- Tidak ada tautan mati dan tidak ada `href="#"`.
- Foto memakai berkas asli dari pemilik akun. Tidak ada stok foto.

## Foto yang dipakai

| Berkas sumber | Dipakai jadi | Letak |
|---|---|---|
| dinding-botol.jpeg | dinding.webp dan og.jpg | hero arah 1 dan 3, panggung arah 2, gambar pratinjau WhatsApp |
| produk-desk.jpeg | produk-100ml.webp | etalase bagian produk di ketiga arah |
| poster-agen.jpeg | poster-agen.webp | hero arah 2 |
| poster-mitra.jpeg | poster-mitra.webp | bagian mitra arah 3 |
| testimoni.jpeg | testimoni.webp | kutipan di ketiga arah |

Foto produk memakai satu sumber yang sama, tetapi dipotong berbeda: 4:5 di arah 1,
3:2 di arah 2, dan 1:1 di arah 3. Tujuannya satu botol terlihat utuh di semua
potongan, bukan mengarang foto kemasan lain.

## Yang sengaja tidak dilakukan

- Tidak membuat keranjang atau checkout. Semua pesanan lewat WhatsApp atau Shopee.
- Tidak menampilkan angka keuntungan mitra. Belum ada data dari klien.
- Tidak memakai animasi scroll, gradien, glass, atau bayangan selain tombol
  WhatsApp melayang.
