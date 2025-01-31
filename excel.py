import pandas as pd

# Data laporan parkir
data = {
    "Kode_Parking": ["K510UVQEVTDI", "760YXKX0VP1G", "HSOZWOJ32MD8"],
    "Jenis_Kendaraan": ["Motor", "Motor", "Mobil"],
    "Waktu_Masuk": ["2024-12-31 22:16:51", "2025-01-01 16:09:08", "2025-01-04 12:00:11"],
    "Waktu_Keluar": ["2024-12-31 22:17:58", "2025-01-01 16:10:27", "2025-01-04 12:01:51"],
    "Durasi": ["0.0 jam 1.0 menit 7.0 detik", "0.0 jam 1.0 menit 19.0 detik", "0.0 jam 1.0 menit 40.0 detik"],
    "Biaya": [2000, 2000, 4000],
    "Uang_Pembayaran": [4000, 3000, 5000]
}

# Konversi ke DataFrame
df = pd.DataFrame(data)

# Menambahkan total pemasukan dan keterangan lainnya
total_pemasukan = df["Biaya"].sum()
kembalian = df["Uang_Pembayaran"].sum() - total_pemasukan
uang_setoran = total_pemasukan

# Fungsi untuk konversi angka ke terbilang
from num2words import num2words

def angka_ke_terbilang(angka):
    return num2words(angka, lang='id').replace("dan ", "").capitalize() + " Rupiah"

terbilang_setoran = angka_ke_terbilang(uang_setoran)

# Data tambahan sebagai ringkasan laporan
summary = {
    "Total Pemasukan": [f"= Rp. {total_pemasukan}"],
    "Kembalian": [f"= Rp. {kembalian}"],
    "Uang Yang Perlu di Setorkan": [f"= Rp. {uang_setoran}"],
    "Terbilang": [f": {terbilang_setoran}"]
}

# Konversi ringkasan ke DataFrame
df_summary = pd.DataFrame.from_dict(summary, orient='index', columns=["Keterangan"])

# Simpan ke file Excel
with pd.ExcelWriter("Laporan_Parkir.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Data Parkir", index=False)
    df_summary.to_excel(writer, sheet_name="Ringkasan", index=True)

print("File Excel berhasil dibuat: 'Laporan_Parkir.xlsx'")
