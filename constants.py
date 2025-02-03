import cv2
import os
import time
import string
import random as rd
import numpy as np
import pandas as pd
from PIL import Image
import qrcode
from pyzbar.pyzbar import decode
from datetime import datetime
from num2words import num2words
import logging

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