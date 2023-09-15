# Buatlah function yang menghitung jumlah huruf kapital dalam sebuah file


def countCapital(file):
    file_buffer = []
    count = 0
    with open(file, 'r') as file:
        file_buffer = file.readlines()

    for line in file_buffer:
        for char in line:
            if char.isupper():
                count += 1
    return count

print(countCapital('file.txt'))