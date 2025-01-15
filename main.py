import os
import time
import string
import random as rd
import numpy as np
import pandas as pd
import cv2
from PIL import Image
import qrcode
from pyzbar.pyzbar import decode
from datetime import datetime
import logging
from constants import FONT, FONT_SCALE, COLOR, IMAGE_SIZE, QR_SIZE, TICKET_PATH, QR_PATH, CAPTURE_PATH_IN, CAPTURE_PATH_OUT, DATABASE_PATH

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_database():
    """Ensure the database directory and file exist."""
    if not os.path.exists("./database"):
        os.makedirs("./database")
        logging.info("Database directory created.")

    if not os.path.exists(DATABASE_PATH):
        empty_df = pd.DataFrame(columns=['Kode_Parking', 'No_Kendaraan', 'Jenis_Kendaraan', 
                                          'Waktu_Masuk', 'Waktu_Keluar', 'Durasi', 
                                          'Biaya', 'Nama_Petugas', 'Foto_Masuk', 
                                          'Foto_Keluar'])
        empty_df.to_excel(DATABASE_PATH, index=False, sheet_name="Data_Parking")
        logging.info(f"Database file '{DATABASE_PATH}' created.")
    else:
        logging.info("Database file already exists.")

def open_image(image_path: str) -> Image:
    """Open an image file and return the image object."""
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        logging.error(f"Image file '{image_path}' not found.")
    except Exception as e:
        logging.error(f"Error opening image: {e}")
    return None

def create_parking_ticket_jpg(kodParking: str, kodeTiket: str, qr_file_path: str, tgl_masuk: str, output_file: str):
    """Create a parking ticket image with QR code."""
    img = np.ones((*IMAGE_SIZE, 3), dtype=np.uint8) * 255
    now = datetime.now()
    tanggal = now.strftime("%d %B %Y")
    waktu = now.strftime("%H:%M:%S")

# Add text to the image
    cv2.putText(img, 'TANDA MASUK - UNIVERSITAS IPWIJA', (50, 50), FONT, FONT_SCALE, COLOR, 2)
    cv2.putText(img, "=" * 23, (50, 70), FONT, FONT_SCALE, COLOR, 2)
    cv2.putText(img, f"Nomor Tiket    : {kodeTiket}", (50, 100), FONT, FONT_SCALE, COLOR, 2)
    cv2.putText(img, f"Tanggal Masuk : {tanggal}", (50, 120), FONT, FONT_SCALE, COLOR, 2)
    cv2.putText(img, f"Waktu Masuk   : {waktu}", (50, 140), FONT, FONT_SCALE, COLOR, 2)
    cv2.putText(img, f"           {kodParking}", (50, 320), FONT, FONT_SCALE, COLOR, 2)
    cv2.putText(img, "=" * 23, (50, 360), FONT, FONT_SCALE, COLOR, 2)
    cv2.putText(img, "Terima kasih ", (50, 380), FONT, FONT_SCALE, COLOR, 2)

    # Load and place the QR code
    try:
        qr_img = cv2.imread(qr_file_path)
        qr_img = cv2.resize(qr_img, QR_SIZE)
        img[150:300, 125:275] = qr_img
    except (FileNotFoundError, cv2.error):
        logging.error(f"QR code image '{qr_file_path}' not found or invalid.")
        return 

    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    pil_img.save(output_file)

def capture_image(filename: str) -> bool:
    """Capture an image from the camera and save it."""
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        logging.error("Tidak dapat membuka kamera")
        return False

    ret, frame = cap.read()
    if ret:
        cv2.putText(frame, datetime.now().strftime("%Y/%m/%d %H:%M:%S"), (20, 30), FONT, 1, (0, 255, 0), 2, cv2.LINE_AA)
        if cv2.imwrite(filename, frame):
            return True
        else:
            logging.error("Gagal menyimpan foto")
    cap.release()
    return False

def generate_parking_code(length: int = 10) -> str:
    """Generate a random parking code of specified length."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(rd.choice(characters) for _ in range(length))

def file_exists(file_path: str) -> bool:
    """Check if a file exists."""
    return os.path.exists(file_path)

def save_parking_data(parking: dict):
    """Save parking data to an Excel file."""
    dfParking = pd.DataFrame(parking)
    
  # Ensure the database directory exists
if not os.path.exists("./database"):
    os.makedirs("./database")
    logging.info("Database directory created.")

# Ensure the capture directories exist
if not os.path.exists(CAPTURE_PATH_IN):
    os.makedirs(CAPTURE_PATH_IN)
    logging.info("Capture directory for incoming photos created.")
if not os.path.exists(CAPTURE_PATH_OUT):
    os.makedirs(CAPTURE_PATH_OUT)
    logging.info("Capture directory for outgoing photos created.")

# Ensure the ticket and QR code directories exist
if not os.path.exists(TICKET_PATH):
    os.makedirs(TICKET_PATH)
    logging.info("Karcis (ticket) directory created.")
if not os.path.exists(QR_PATH):
    os.makedirs(QR_PATH)
    logging.info("QR Code directory created.")

    try:
        # Check if the database file exists
        if not file_exists(DATABASE_PATH):
            # Create an empty DataFrame with the required columns
            empty_df = pd.DataFrame(columns=['Kode_Parking', 'No_Kendaraan', 'Jenis_Kendaraan', 
                                              'Waktu_Masuk', 'Waktu_Keluar', 'Durasi', 
                                              'Biaya', 'Nama_Petugas', 'Foto_Masuk', 
                                              'Foto_Keluar'])
            empty_df.to_excel(DATABASE_PATH, index=False, sheet_name="Data_Parking")
            logging.info(f"Database file '{DATABASE_PATH}' created.")

        if file_exists(DATABASE_PATH):
            dfEx = pd.read_excel(DATABASE_PATH)
            dfParking = pd.concat([dfEx, dfParking], ignore_index=True)
        
        dfParking.to_excel(DATABASE_PATH, index=False, sheet_name="Data_Parking")
        logging.info(f"Data berhasil disimpan ke file: {DATABASE_PATH}")
    except PermissionError:
        logging.error("PermissionError: File sedang dibuka oleh program lain.")
    except Exception as e:
        logging.error(f"Error saat menyimpan file: {e}")

def generate_qr_code(data: str, filename: str):
    """Generate a QR code and save it to a file."""
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    imgQR = qr.make_image(fill_color="black", back_color="white")
    imgQR.save(filename)

def validate_vehicle_number() -> str:
    """Validate the vehicle registration number format and return it if valid."""
    dfParkir = pd.read_excel(DATABASE_PATH, sheet_name="Data_Parking")
    while True:
        vehicle_number = input("Masukkan Nomor Kendaraan: ").strip()
        if not vehicle_number:
            logging.error("Nomor kendaraan tidak boleh kosong.")
            continue  
        if not validate_format(vehicle_number):
            continue
        if is_vehicle_parked(dfParkir, vehicle_number):
            logging.error("Kendaraan dengan nomor ini sudah ada di parkir.")
            continue
        return vehicle_number.upper()

def validate_format(vehicle_number: str) -> bool:
    """Check the format of the vehicle registration number."""
    parts = vehicle_number.split()
    if len(parts) != 3:
        logging.error("Format nomor kendaraan harus 'A 1234 XYZ'.")
        return False  
    kode_wilayah, nomor_urut, kode_seri = parts
    if not (kode_wilayah.isalpha() and len(kode_wilayah) <= 2):
        logging.error("Kode wilayah tidak boleh lebih dari dua huruf.")
        return False  
    if not (nomor_urut.isdigit() and len(nomor_urut) <= 4):
        logging.error("Nomor urut tidak boleh lebih dari 4 digit angka.")
        return False  
    if not (kode_seri.isalpha() and len(kode_seri) <= 3):
        logging.error("Kode seri tidak boleh lebih dari 3 huruf.")
        return False 
    return True

def is_vehicle_parked(dfParkir: pd.DataFrame, vehicle_number: str) -> bool:
    """Check if the vehicle is already parked."""
    parked_vehicle = dfParkir[(dfParkir['No_Kendaraan'] == vehicle_number) & 
                               (dfParkir['Waktu_Keluar'].isna() | (dfParkir['Waktu_Keluar'] == " "))]
    return not parked_vehicle.empty

def park_in(tgl_masuk: str, nama_petugas: str):
    """Handle parking entry."""
    kodParking = generate_parking_code(12)
    kodeTiket = generate_parking_code(4)

    vehicle_number = validate_vehicle_number()  # Get valid vehicle number

    qr_code_filename = os.path.join(QR_PATH, f"{kodParking}.png")
    ticket_filename = os.path.join(TICKET_PATH, f"{kodeTiket}.jpg")
    capture_filename = os.path.join(CAPTURE_PATH_IN, f"{kodParking}.png")

    parking_data = {
        'Kode_Parking': [kodParking],
        'No_Kendaraan': [vehicle_number],
        'Jenis_Kendaraan': [" "],
        'Waktu_Masuk': [tgl_masuk],
        'Waktu_Keluar': [" "],
        'Durasi': [" "],
        'Biaya': [" "],
        'Nama_Petugas': [nama_petugas],
        'Foto_Masuk': [capture_filename],
        'Foto_Keluar': [" "]
    }

    save_parking_data(parking_data)
    generate_qr_code(data=kodParking, filename=qr_code_filename)
    capture_image(capture_filename)
    create_parking_ticket_jpg(kodParking, kodeTiket, qr_code_filename, tgl_masuk, ticket_filename)

    img = open_image(ticket_filename)
    if img:
        img.show()
        time.sleep(5)
        img.close()
    else:
        logging.error("Format nomor kendaraan salah. Silahkan Masukan Nomor Kendaraan Yang Benar.")

def update_parking_data(fileExcel: str, id_parkir: str, jenis_kendaraan: str, waktu_keluar: str, durasi: str, biaya: float, foto_keluar: str):
    """Update parking data in the Excel file."""
    dfParkir = pd.read_excel(fileExcel, sheet_name="Data_Parking")
    index = dfParkir[dfParkir['Kode_Parking'] == id_parkir].index

    if index.empty:
        logging.error("Data parkir tidak ditemukan.")
        return

    dfParkir.loc[index, ['Jenis_Kendaraan', 'Waktu_Keluar', 'Durasi', 'Biaya', 'Foto_Keluar']] = \
        [jenis_kendaraan, waktu_keluar, durasi, biaya, foto_keluar]
    dfParkir.to_excel(fileExcel, sheet_name="Data_Parking", index=False)

def park_out(qr_code: str):
    """Handle parking exit."""
    dfProduk = pd.read_excel(DATABASE_PATH, sheet_name="Data_Parking")
    resultProduk = dfProduk[dfProduk['Kode_Parking'] == qr_code]
    capture_filename = os.path.join(CAPTURE_PATH_OUT, f"{qr_code}.png")
    capture_image(capture_filename)

    if resultProduk.empty:
        logging.error("Data Parkir tidak ditemukan.")
        return

    logging.info("TANDA KELUAR UNIVERSITAS IPWIJA")
    logging.info("=" * 50)

    data_kendaraan = resultProduk.iloc[0]
    logging.info("=" * 50)
    logging.info(f"Kode Parking: {data_kendaraan['Kode_Parking']}")
    logging.info("=" * 50)
    logging.info("Jenis Kendaraan:")
    logging.info("1. Mobil")
    logging.info("2. Motor")
    jenisKendaraan = int(input("Pilih Jenis Kendaraan: "))
    jenisKendaraan = "Mobil" if jenisKendaraan == 1 else "Motor"

    waktu_masuk = pd.to_datetime(data_kendaraan['Waktu_Masuk'])
    waktu_keluar = datetime.now()
    tgl_Keluar = waktu_keluar.strftime("%Y-%m-%d %H:%M:%S")

    estimasi = (waktu_keluar - waktu_masuk).total_seconds()
    jam = int(estimasi // 3600)  # Menghitung jam
    menit = int((estimasi % 3600) // 60)  # Menghitung menit
    detik = int(estimasi % 60)  # Menghitung detik
    tarif_per_jam = 2000 if jenisKendaraan == "Motor" else 4000
    total_tarif = tarif_per_jam if jam == 0 and menit < 60 else (jam * tarif_per_jam) + tarif_per_jam
    total_tarif = round(total_tarif, -3)

    update_parking_data(fileExcel=DATABASE_PATH, id_parkir=qr_code, jenis_kendaraan=jenisKendaraan, 
                        waktu_keluar=tgl_Keluar, durasi=f"{jam:02}:{menit:02}:{detik:02}", 
                        biaya=total_tarif, foto_keluar=capture_filename)

    logging.info(f"Jenis Kendaraan : {jenisKendaraan}")
    logging.info(f"Waktu Masuk : {waktu_masuk.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Waktu Keluar : {waktu_keluar.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Durasi Parkir : {jam:02}:{menit:02}:{detik:02}")
    logging.info(f"Total Tarif : Rp {total_tarif:,}")

    while True:
        try:
            uang_bayar = float(input("Masukkan jumlah uang pembayaran: Rp "))
            if uang_bayar >= total_tarif:
                break
            logging.warning("Uang pembayaran kurang. Silakan ulangi.")
        except ValueError:
            logging.warning("Input tidak valid. Masukkan angka.")

    kembalian = uang_bayar - total_tarif
    logging.info("=" * 50)
    logging.info(f"Uang Bayar : Rp {uang_bayar}")
    logging.info(f"Kembalian : Rp {kembalian}")
    logging.info("=" * 50)

    # Display the entry and exit images
    img_masuk = cv2.imread(data_kendaraan['Foto_Masuk'])
    img_keluar = cv2.imread(capture_filename)
    if img_masuk is not None and img_keluar is not None:
        height = min(img_masuk.shape[0], img_keluar.shape[0])
        img_masuk_resized = cv2.resize(img_masuk, (int(img_masuk.shape[1] * height / img_masuk.shape[0]), height))
        img_keluar_resized = cv2.resize(img_keluar, (int(img_keluar.shape[1] * height / img_keluar.shape[0]), height))
        img_combined = cv2.hconcat([img_masuk_resized, img_keluar_resized])
        cv2.imshow('Foto Masuk dan Keluar', img_combined)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        logging.error("Salah satu atau kedua gambar tidak dapat dimuat.")

def read_qr_code():
    """Read QR code from camera."""
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        logging.error("Error: Kamera tidak dapat diakses.")
        return

    logging.info("Membaca QR Code...")
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.error("Error: Tidak dapat membaca frame dari kamera.")
            break

        decoded_objects = decode(frame)
        if decoded_objects:
            for obj in decoded_objects:
                qr_data = obj.data.decode("utf-8")
                logging.info(f"QR Code ditemukan: {qr_data}")
                cap.release()
                cv2.destroyAllWindows()
                park_out(qr_data)
                return

        if time.time() - start_time > 10:
            logging.warning("Waktu habis. Tidak ada QR Code yang ditemukan.")
            break

        cv2.imshow("QR Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def lihat_data_parkir():
    """Display parking data."""
    df_parkir = pd.read_excel(DATABASE_PATH, sheet_name='Data_Parking')
    kolom_dipilih = [
        'Kode_Parking', 'No_Kendaraan', 'Jenis_Kendaraan', 'Durasi', 'Biaya'
    ]
    dfFiltered = df_parkir[kolom_dipilih]
    pd.set_option('display.max_columns', None)  # Menampilkan semua kolom
    pd.set_option('display.width', 500)        # Lebar tampilan maksimal
    pd.set_option('display.max_colwidth', None) # Menampilkan seluruh isi kolom
    print(dfFiltered.tail(10))

def main_menu():
    """Display the main menu and handle user input."""
    initialize_database()  # Ensure database is initialized

    while True:
        print("*" * 50)
        print("Ujian Akhir Semester - Dasar Pemrograman")
        print("*" * 50)
        print("Nama : Reza Ramdan Permana")
        print("Kelas : IK241")
        print("*" * 50, "\n")
        print("*" * 50)
        print("Sistem Parking Universitas IPWIJA")
        print("*" * 50)

        tgl_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Nama Petugas: Reza Ramdan Permana")
        print("Tanggal Operation: ", tgl_masuk)
        print("*" * 50)
        print("1. Parkir Masuk")
        print("2. Parkir Keluar")
        print("3. Lihat Data Parkir")
        print("4. Keluar Program")

        try:
            pilihan = int(input("Masukkan Pilihan: "))
            print("*" * 50)
            if pilihan == 1:
                park_in(tgl_masuk, "Reza Ramdan Permana")
            elif pilihan == 2:
                read_qr_code()
            elif pilihan == 3:
                lihat_data_parkir()
            elif pilihan == 4:
                logging.info("Keluar dari sistem. Terima kasih.")
                break
            else:
                logging.warning("Pilihan tidak valid. Silakan coba lagi.")
        except ValueError:
            logging.warning("Input tidak valid. Masukkan angka.")

if __name__ == "__main__":
    main_menu()