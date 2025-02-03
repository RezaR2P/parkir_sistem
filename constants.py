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