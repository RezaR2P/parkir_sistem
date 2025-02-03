# constants.py

import cv2

# Constants
TARIF_MOTOR = 2000
TARIF_MOBIL = 4000
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
COLOR = (0, 0, 0)
IMAGE_SIZE = (400, 400)
QR_SIZE = (150, 150)
TICKET_PATH = "./karcis"
QR_PATH = "./qr_code"
CAPTURE_PATH_IN = "./capture/masuk"
CAPTURE_PATH_OUT = "./capture/keluar"
DATABASE_PATH = "./database"
DATAPARKING_PATH = "./database/Data_Parking.xlsx"
LAPORAN_PATH = "./laporan"

REPORT_FILENAME_FORMAT = {
    'hari': 'laporan_keuangan_{tanggal}.xlsx',
    'bulan': 'laporan_keuangan_{bulan}_{tahun}.xlsx',
    'tahun': 'laporan_keuangan_{tahun}.xlsx'
}