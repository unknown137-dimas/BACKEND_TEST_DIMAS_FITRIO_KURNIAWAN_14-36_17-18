# Buatlah sebuah program yang menanyakan nama dan usia kepada user. Program kemudian memunculkan kapan user bersangkutan berusia 50 tahun.
from datetime import date

nama = input('Siapa nama anda: ')
umur = input('Berapa usia anda saat ini: ')
year = date.today().year
year50 = int(year) + (50 - int(umur))

print(f'{nama} akan berusia 50 tahun pada tahun {year50}')