# DESIGN.md - Saideo Surabaya (tiga arah, palet biru klien)

Dokumen ini menjelaskan tiga arah desain untuk calon klien Saideo Surabaya.
Isi dan harga sama di ketiganya, yang berbeda arah visual, susunan bagian, dan
cara menonjolkan jalur mitra.

Palet mengikuti permintaan klien. Versi sebelumnya memakai hijau, krem, dan
kuning; seluruhnya sudah diganti.

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
tipografi, sudut, dan bingkai.

## Palet klien

| Nama | Nilai | Peran |
|---|---|---|
| Cloud Blue | #EDF4FA | latar terang, teks di atas biru tua |
| Powder Sky | #CFE3F1 | panel lembut, tombol terang, penanda |
| Calm Ocean | #8FB6D8 | aksen dekoratif di latar gelap |
| Dusty Denim | #5F86A6 | bingkai foto dan hover, bukan teks |
| Midnight Blue | #243A5E | teks utama, tombol, latar gelap |

Dua turunan dibuat karena batas kontras, bukan selera:

| Turunan | Nilai | Alasan |
|---|---|---|
| Redup | #4A627D | teks penjelas. Dusty Denim hanya 3.47:1 di atas Cloud Blue |
| Denim tua | #46688C | harga dan label. 5.23:1 di atas Cloud Blue, 5.80:1 di atas putih |

Dusty Denim tidak dipakai untuk teks kecil. Di atas Cloud Blue hanya 3.47:1,
gagal AA. Perannya tinggal bingkai foto dan garis hover.

## Arah 1 - Bersih Klinis

Dial ENERGY 1 / RHYTHM 2 / MOTION 1.

Design read: halaman produk perawatan harian yang dijual agen resmi, terasa
seperti apotek modern, bukan iklan ramai. Latar biru awan hampir putih, kartu
putih, dan tinta biru tengah malam.

| Token | Nilai | Dipakai untuk |
|---|---|---|
| kertas | #EDF4FA | latar halaman |
| kartu | #FFFFFF | panel, baris produk |
| tinta | #243A5E | teks utama |
| redup | #4A627D | teks penjelas |
| utama | #243A5E | tombol, tautan, pita mitra |
| aksen | #CFE3F1 | bagian alasan, chip, ajakan akhir |
| harga | #46688C | harga, nomor bagian |
| garis | #C9DCEB | garis rambut |

Judul memakai Bricolage Grotesque, teks Plus Jakarta Sans. Susunan: hero belah
dua, etalase foto dengan daftar produk bergaris, empat alasan berkolom, pita biru
tua untuk mitra, kutipan dengan tangkapan layar, langkah bernomor.

## Arah 2 - Kota Malam

Dial ENERGY 4 / RHYTHM 3 / MOTION 2.

Design read: poster jalanan Surabaya. Biru tengah malam sebagai latar, huruf
besar dan rapat, biru langit sebagai penanda. Paling berani dari ketiganya.

| Token | Nilai | Dipakai untuk |
|---|---|---|
| malam | #243A5E | latar halaman |
| panel | #2C466E | kartu dan panel |
| garis | #3E587C | pemisah |
| kertas | #EDF4FA | teks utama |
| redup | #B9CDE0 | teks penjelas |
| aksen | #CFE3F1 | tombol, harga, penanda |
| laut | #8FB6D8 | hover dan aksen kecil |

Judul memakai Anton, teks Plus Jakarta Sans. Susunan: judul raksasa, panggung
foto penuh lebar, pita fakta, etalase dan tiga kartu produk, blok mitra berlatar
biru langit, kutipan, tiga jalur order.

## Arah 3 - Lembut Personal

Dial ENERGY 2 / RHYTHM 3 / MOTION 1.

Design read: surat dari agen, bukan katalog. Biru awan, serif lembut, kartu
membulat. Dua jalur langsung di bawah pembuka.

| Token | Nilai | Dipakai untuk |
|---|---|---|
| kertas | #EDF4FA | latar halaman |
| kartu | #FFFFFF | kartu produk |
| tinta | #243A5E | teks utama, panel mitra |
| redup | #4A627D | teks penjelas |
| utama | #243A5E | tombol dan harga |
| label | #46688C | label kecil, tautan |
| panel | #CFE3F1 | bagian mitra, kartu paket |
| garis | #C9DCEB | pemisah |

Judul memakai Fraunces, teks Plus Jakarta Sans. Susunan: hero tengah, dua kartu
jalur (beli satuan dan jadi mitra), etalase foto persegi, daftar produk berpanel,
surat mitra dengan tanda tangan, kutipan, langkah, ajakan biru tua.

## Kontras yang diukur

Dihitung, bukan dikira. Semua pasangan di bawah ini lolos AA 4.5:1 dan diperiksa
ulang oleh `tools/audit.py`.

| Arah | Pasangan | Rasio |
|---|---|---|
| 1 | tinta di awan | 10.27:1 |
| 1 | redup di awan | 5.67:1 |
| 1 | putih di biru tua | 11.40:1 |
| 1 | denim tua di awan | 5.23:1 |
| 1 | tinta di langit | 8.64:1 |
| 2 | awan di malam | 10.27:1 |
| 2 | redup di malam | 6.99:1 |
| 2 | langit di malam | 8.64:1 |
| 2 | malam di langit | 8.64:1 |
| 2 | putih di panel | 9.51:1 |
| 2 | redup di panel | 5.83:1 |
| 3 | tinta di awan | 10.27:1 |
| 3 | redup di awan | 5.67:1 |
| 3 | putih di biru tua | 11.40:1 |
| 3 | denim tua di awan | 5.23:1 |
| 3 | tinta di langit | 8.64:1 |
| 3 | redup di langit | 4.77:1 |
| pemilih | tinta di awan | 10.27:1 |
| pemilih | redup di awan | 5.67:1 |
| pemilih | putih di biru tua | 11.40:1 |

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
| poster-agen.jpeg | poster-agen.webp | hero arah 2 dan halaman tentang |
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
