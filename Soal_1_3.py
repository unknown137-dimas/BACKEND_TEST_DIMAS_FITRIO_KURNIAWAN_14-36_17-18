# Buatlah function dengan Python untuk menghasilkan Bintang segitiga

# Output:
# *
# **
# ***
# ****
# *****

def bintang_segitiga(x):
    for i in range(1, x + 1):
        print('*' * i)

bintang_segitiga(5)