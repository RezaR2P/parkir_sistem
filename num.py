from num2words import num2words
def angka_ke_terbilang(angka):
    return num2words(angka, lang='id').replace("dan ", "").capitalize() + " Rupiah"

uang = 20000
terbilang = angka_ke_terbilang(uang)
print(f"Uang yang perlu disetorkan = Rp. {uang}")
print(f"Terbilang: {terbilang}")
