# Sistem Parkir Universitas IPWIJA

Sistem Parkir Universitas IPWIJA adalah sebuah aplikasi berbasis Python untuk mengelola parkir kendaraan di lingkungan kampus. Aplikasi ini mencakup fitur-fitur seperti:

## Fitur Utama

### Manajemen Parkir

- Mencatat kendaraan masuk dan keluar.
- Menghasilkan QR code dan tiket parkir.
- Menghitung biaya parkir berdasarkan durasi dan jenis kendaraan.

### Laporan Keuangan

- Menghasilkan laporan keuangan harian, bulanan, atau tahunan.
- Menyertakan ringkasan pemasukan, pengeluaran, dan terbilang.

### Manajemen Data

- Menghapus data parkir beserta file terkait.
- Menyimpan data parkir dalam format Excel.

### Integrasi Kamera

- Mengambil foto kendaraan saat masuk dan keluar.
- Membaca QR code untuk proses parkir keluar.

## Instalasi

### Persyaratan Sistem

- **Python** 3.8 atau lebih baru.
- Library yang diperlukan (lihat `requirements.txt`).

### Langkah Instalasi

1. **Clone Repository**:

   ```bash
   git clone https://github.com/username/parking_system.git
   cd parking_system
   ```

2. **Buat Virtual Environment (opsional)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   venv\Scripts\activate     # Untuk Windows
   ```

3. **Instal Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Aplikasi**:
   ```bash
   python main.py
   ```

## Cara Penggunaan

### Parkir Masuk

1. Pilih opsi "Parkir Masuk" dari menu utama.
2. Masukkan nomor kendaraan.
3. Sistem akan menghasilkan tiket parkir dan menyimpan data.

### Parkir Keluar

1. Pilih opsi "Parkir Keluar" dari menu utama.
2. Arahkan kamera ke QR code pada tiket parkir.
3. Sistem akan menghitung biaya parkir dan mengupdate data.

### Laporan Keuangan

1. Pilih opsi "Buat Laporan Keuangan" dari menu utama.
2. Pilih periode laporan (harian, bulanan, atau tahunan).
3. Sistem akan menghasilkan laporan dalam format Excel.

### Hapus Data Parkir

1. Pilih opsi "Hapus Data Parkir" dari menu utama.
2. Masukkan kriteria penghapusan (kode parkir atau nomor kendaraan).
3. Sistem akan menghapus data dan file terkait.

## Struktur Direktori

```
parking_system/
│
├── constants.py          # File konstanta
├── main.py               # Entry point aplikasi
├── database/             # Penyimpanan database
│   └── Data_Parking.xlsx # File database parkir
├── capture/              # Penyimpanan foto kendaraan
│   ├── masuk/            # Foto kendaraan masuk
│   └── keluar/           # Foto kendaraan keluar
├── karcis/               # Penyimpanan tiket parkir
├── qr_code/              # Penyimpanan QR code
└── laporan/              # Penyimpanan laporan keuangan
```

## Dependencies

Berikut adalah daftar library yang digunakan dalam proyek ini:

- **opencv-python (cv2)**: Untuk manipulasi gambar dan kamera.
- **Pillow (PIL)**: Untuk pengolahan gambar.
- **pandas**: Untuk manajemen data dalam format Excel.
- **qrcode**: Untuk pembuatan QR code.
- **pyzbar**: Untuk membaca QR code.
- **num2words**: Untuk mengkonversi angka ke kata-kata.

Untuk menginstal semua dependencies, jalankan:

```bash
pip install -r requirements.txt
```

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan ikuti langkah-langkah berikut:

1. Fork repository ini.
2. Buat branch baru (git checkout -b fitur-baru).
3. Commit perubahan Anda (git commit -m 'Tambahkan fitur baru').
4. Push ke branch (git push origin fitur-baru).
5. Buat Pull Request.

## Catatan

- Pastikan untuk mengganti username pada langkah instalasi dengan username GitHub Anda.
- Sesuaikan deskripsi dan instruksi sesuai dengan kebutuhan proyek Anda.
