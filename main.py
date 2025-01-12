import time
import pandas as pd
import qrcode
from PIL import Image, ImageDraw
import string
import random as rd
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import os
import numpy as np

def open_image(image_path):
  try:
    img = Image.open(image_path)
    return img
  except FileNotFoundError:
    print(f"Error: Image file '{image_path}' not found.")
    return None
  except Exception as e:
    print(f"Error opening image: {e}")
    return None

def create_parking_ticket_jpg(kodParking,kodeTiket,qr_file_path, tgl_masuk, output_file):
    img = np.zeros((400, 400, 3), np.uint8)
    img[:] = 255

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    color = (0, 0, 0)
    now = datetime.now()
    tanggal = now.strftime("%d %B %Y") 
    waktu = now.strftime("%H:%M:%S")

   
    cv2.putText(img, 'TANDA MASUK - UNIVERSITAS IPWIJA', (50, 50), font, font_scale, color, 2)
    cv2.putText(img,f"="*23,(50, 70), font, font_scale, color, 2)
    cv2.putText(img,f"Nomor Tiket    : {kodeTiket}", (50, 100), font, font_scale, color, 2)
    cv2.putText(img, f"Tanggal Masuk : {tanggal}", (50, 120), font, font_scale, color, 2)
    cv2.putText(img, f"Waktu Masuk   : {waktu}", (50, 140), font, font_scale, color, 2)
    cv2.putText(img, f"           {kodParking}", (50, 320), font, font_scale, color, 2)
    cv2.putText(img,f"="*23,(50, 360), font, font_scale, color, 2)
    cv2.putText(img, "Terima kasih ", (50, 380), font, font_scale, color, 2)

    try:
        qr_img = cv2.imread(qr_file_path)
    except (FileNotFoundError, cv2.error):
        print(f"Error: QR code image '{qr_file_path}' not found or invalid.")
        return 
    
    img_width = 350 
    qr_img = cv2.resize(qr_img, (150, 150))
    qr_x = (img_width - 100) // 2
    qr_y = 150

    img[qr_y:qr_y+150, qr_x:qr_x+150] = qr_img

    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

  
    draw = ImageDraw.Draw(pil_img)
    pil_img.save(output_file)

def capture(nama_file):
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # V4L2 backend

    if not cap.isOpened():
        print("Tidak dapat membuka kamera")
        return False
    ret, frame = cap.read()
    waktu_sekarang = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, waktu_sekarang, (20, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    if cv2.imwrite(nama_file, frame):
        return True
    else:
        print("Gagal menyimpan foto")
        return False
    cap.release()


def gen_kode_parking(panjang):
    """Fungsi ini digunakan untuk mengenerate Kode String dan Angka Secara otomatis sepanjang 10 karakter"""
    karakter = string.ascii_uppercase + string.digits
    kode = ''.join(rd.choice(karakter) for _ in range(panjang))
    return kode

    
def check_file(file_path):
    return os.path.exists(file_path)



def save_parking(parking):
    # Path direktori dan file
    path = "./database"
    fileName = "Data_Parking.xlsx"
    
    # Pastikan direktori ada
    if not os.path.exists(path):
        os.makedirs(path)

    # Konversi data parkir menjadi DataFrame
    dfParking = pd.DataFrame(parking)

    try:
        # Cek jika file sudah ada, lalu gabungkan data baru
        file_path = os.path.join(path, fileName)
        if os.path.exists(file_path):
            dfEx = pd.read_excel(file_path)
            dfParking = pd.concat([dfEx, dfParking], ignore_index=True)
        
        # Simpan data ke file Excel
        dfParking.to_excel(file_path, index=False, sheet_name="Data_Parking")
        print(f"Data berhasil disimpan ke file: {file_path}")
    
    except PermissionError as e:
        print(f"PermissionError: {e}")
        print("Pastikan file tidak sedang dibuka oleh program lain.")
    
    except Exception as e:
        print(f"Error saat menyimpan file: {e}")




def gen_QRcode(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    imgQR = qr.make_image(fill_color="black", back_color="white")
    imgQR.save(filename)


def validate_nomor_kendaraan(nomor_kendaraan):
    if len(nomor_kendaraan.strip()) == 0:
        print("Error: Nomor kendaraan tidak boleh kosong.")
        return False

    plats = nomor_kendaraan.split()
    if len(plats) != 3:
        print("Error: Format nomor kendaraan harus 'A 1234 XYZ'.")
        return False

    kode_wilayah, nomor_urut, kode_seri = plats
    if not kode_wilayah.isalpha() or len(kode_wilayah) != 1:
        print("Error: Kode wilayah harus berupa satu huruf.")
        return False

    if not nomor_urut.isdigit() or len(nomor_urut) != 4:
        print("Error: Nomor urut harus berupa 4 digit angka.")
        return False

    if not kode_seri.isalpha() or len(kode_seri) != 3:
        print("Error: Kode seri harus berupa 3 huruf.")
        return False

    return True



def masuk(tgl_masuk, nama_petugas):
    kodParking = gen_kode_parking(12)
    kodeTiket = gen_kode_parking(4)
    NoKendaraan = input("Masukan Nomor Kendaraan: ")
    if validate_nomor_kendaraan(NoKendaraan):
        pathCapture = "./capture/masuk"
        nameQr = kodParking + ".png"
        path = "./qr_code"
        pathTiket = "./karcis"
        namaTiket = kodeTiket + '.jpg'
        FileTiket = os.path.join(pathTiket, namaTiket)
        nameFile = os.path.join(path, nameQr)
        nameCapture = os.path.join(pathCapture, nameQr)
        if check_file(path):
            print("Silahkan Masuk...")
        else:
            print("File QR Tidak berhasil disimpan")
        
        parking = {
            'Kode_Parking':[kodParking],
            'No_Kendaraan':[NoKendaraan],
            'Jenis_Kendaraan':[" "],
            'Waktu_Masuk':[tgl_masuk],
            'Waktu_Keluar':[" "],
            'Durasi':[" "],
            'Biaya':[" "],
            'Nama_Petugas':[nama_petugas],
            'Foto_Masuk':[nameCapture],
            'Foto_Keluar':[" "]
                }
        save_parking(parking)
        gen_QRcode(data=kodParking, filename=nameFile)
        capture(nameCapture)
        create_parking_ticket_jpg(kodParking, kodeTiket, nameFile, tgl_masuk, FileTiket)
        img = open_image(FileTiket)
        if img:
            img.show()
            time.sleep(5)
            img.close()
    else:
        print("\n")
        print("+"*100)
        print("\t\t\tFormat nomor kendaraan salah.")
        print("\t\t\tSilahkan Masukan Nomor Kendaraan Yang Benar")
        print("+"*100)
        print("\n")

    

def update_data_parkir(fileExcel, id_parkir, jenis_kendaraan, waktu_keluar, durasi, biaya, foto_keluar):
    dfParkir = pd.read_excel(fileExcel, sheet_name="Data_Parking")
    dfParkir['Jenis_Kendaraan'] = dfParkir['Jenis_Kendaraan'].astype('object')

    # Cari data berdasarkan ID parkir
    index = dfParkir[dfParkir['Kode_Parking'] == id_parkir].index
    if index.empty:
        print("\n")
        print("+"*100)
        print("Data parkir tidak ditemukan.")
        print("+"*100)
        print("\n")
        return

    dfParkir.loc[index, 'Jenis_Kendaraan'] = jenis_kendaraan
    dfParkir.loc[index, 'Waktu_Keluar'] = waktu_keluar
    dfParkir.loc[index, 'Durasi'] = durasi
    dfParkir.loc[index, 'Biaya'] = biaya
    dfParkir.loc[index, 'Foto_Keluar'] = foto_keluar
    dfParkir.to_excel(fileExcel, sheet_name="Data_Parking", index=False)



def keluar_parkir(qrCode):
    path = "./database"
    fileExcel = "Data_Parking.xlsx"
    pathCapture = "./capture/keluar"
    nameExcel = os.path.join(path, fileExcel)
    nameQr = qrCode + ".png"
    nameCapture = os.path.join(pathCapture, nameQr)
    dfProduk = pd.read_excel(f"{path}/{fileExcel}", sheet_name="Data_Parking")
    resultProduk = dfProduk[dfProduk['Kode_Parking'] == qrCode]
    capture(nameCapture)

    if resultProduk.empty:
        print("\n")
        print("+"*100)
        print("Data Parkir tidak ditemukan.")
        print("+"*100)
        print("\n")
    else:
        print("TANDA KELUAR - UNIVERSITAS IPWIJA")
        print("="*50)

        # Ambil data kendaraan dari DataFrame
        data_kendaraan = resultProduk.iloc[0]  # Ambil baris pertama (asumsi hanya ada satu data)
        print("="*50)
        print(f"Kode Parking: {data_kendaraan['Kode_Parking']}")
        print("="*50)
        print("Jenis Kendaraan:")
        print("1. Mobil")
        print("2. Motor")
        jenisKendaraan = int(input("Pilih Jenis Kendaraan: "))  # Asumsikan ada kolom 'Jenis_Kendaraan'
        if jenisKendaraan == 1:
            jenisKendaraan = "Mobil"
        else:
            jenisKendaraan = "Motor"
        waktu_masuk = pd.to_datetime(data_kendaraan['Waktu_Masuk'])

        # Ambil waktu keluar saat ini
        waktu_keluar = datetime.now()
        tgl_Keluar = waktu_keluar.strftime("%Y-%m-%d %H:%M:%S")
        waktu_keluar = pd.to_datetime(tgl_Keluar)

        # Hitung durasi parkir dan tarif
        estimasi = (waktu_keluar - waktu_masuk).total_seconds()
        jam, menit, detik = estimasi // 3600, (estimasi % 3600) // 60, estimasi % 60
        tarif_per_jam = 2000 if jenisKendaraan == "Motor" else 4000
        if jam == 0 and menit < 60:  # Jika durasi kurang dari 1 jam
            total_tarif = tarif_per_jam
        else:
            # Hitung tarif normal jika durasi lebih dari atau sama dengan 1 jam
            total_tarif = (jam * tarif_per_jam) + tarif_per_jam
            total_tarif = round(total_tarif, -3)
        update_data_parkir(fileExcel=nameExcel, id_parkir=qrCode, jenis_kendaraan=jenisKendaraan, 
                        waktu_keluar=tgl_Keluar, durasi=f"{jam} jam {menit} menit {detik} detik", 
                        biaya=total_tarif, foto_keluar=nameCapture)
        print(f"Jenis Kendaraan : {jenisKendaraan}")
        print(f"Waktu Masuk : {waktu_masuk}")
        print(f"Waktu Keluar : {waktu_keluar}")
        print(f"Durasi Parkir : {jam} jam {menit} menit {detik} detik")
        print(f"Total Tarif : Rp {total_tarif:,}")
        while True:
            try:
                uang_bayar = float(input("Masukkan jumlah uang pembayaran: Rp "))
                if uang_bayar >= total_tarif:
                    break
                else:
                    print("Uang pembayaran kurang. Silakan ulangi.")
            except ValueError:
                print("Input tidak valid. Masukkan angka.")


        kembalian = uang_bayar - total_tarif
        # Tampilkan informasi kendaraan
        print("="*50)
        print(f"Uang Bayar : Rp {uang_bayar}")
        print(f"Kembalian : Rp {kembalian}")
        print("="*50)
        foto_Masuk = data_kendaraan['Foto_Masuk']
        img_masuk = cv2.imread(foto_Masuk)
        img_keluar = cv2.imread(nameCapture)
        if img_masuk is None or img_keluar is None:
            print("Salah satu atau kedua gambar tidak dapat dimuat.")
        else:
            # Resize gambar agar memiliki tinggi yang sama (opsional)
            height = min(img_masuk.shape[0], img_keluar.shape[0])
            img_masuk_resized = cv2.resize(img_masuk, (int(img_masuk.shape[1] * height / img_masuk.shape[0]), height))
            img_keluar_resized = cv2.resize(img_keluar, (int(img_keluar.shape[1] * height / img_keluar.shape[0]), height))
            
            # Gabungkan gambar secara horizontal
            img_combined = cv2.hconcat([img_masuk_resized, img_keluar_resized])
            
            # Tampilkan gambar gabungan
            cv2.imshow('Foto Masuk dan Keluar', img_combined)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        print("="*50)

def baca_qr_code():
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Error: Kamera tidak dapat diakses.")
        return

    print("Membaca QR Code...")
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Tidak dapat membaca frame dari kamera.")
            break

        decoded_objects = decode(frame)
        if decoded_objects:
            for obj in decoded_objects:
                qr_data = obj.data.decode("utf-8")
                print(f"QR Code ditemukan: {qr_data}")
                # Lepaskan kamera dan tutup window sebelum masuk ke `keluar_parkir`
                cap.release()
                cv2.destroyAllWindows()
                keluar_parkir(qr_data)  # Panggil fungsi setelah sumber daya dilepas
                return

        elapsed_time = time.time() - start_time
        if elapsed_time > 10:
            print("Waktu habis. Tidak ada QR Code yang ditemukan.")
            break

        cv2.imshow("QR Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def menu_utama():
    while True:
        print("*" * 100)
        print("Ujian Akhir Semester - Dasar Pemrograman")
        print("*" * 100)
        print("Nama : Reza Ramdan Permana")
        print("Kelas : IK241")
        print("*" * 100, "\n")
        print("*" * 100)
        print("Sistem Parking Universitas IPWIJA")
        print("*" * 100)
        tanggal_waktu = datetime.now()
        tgl_masuk = tanggal_waktu.strftime("%Y-%m-%d %H:%M:%S")
        print("Nama Petugas: Reza Ramdan Permana")
        nama_petugas = "Reza Ramdan Permana"
        print("Tanggal Operation: ", tgl_masuk)
        print("*" * 100)
        print("1. Parkir Masuk")
        print("2. Parkir Keluar")
        print("3. Keluar Program")

        try:
            pilihan = int(input("Masukkan Pilihan: "))
            print("*" * 100)
            if pilihan == 1:
                masuk(tgl_masuk, nama_petugas)
            elif pilihan == 2:
                baca_qr_code()
            elif pilihan == 3:
                print("Keluar dari sistem. Terima kasih.")
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
        except ValueError:
            print("Input tidak valid. Masukkan angka.")

menu_utama()