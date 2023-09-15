# Buatlah function untuk mengimplementasikan algoritma pengurutan daftar(array)
# sample array 	: [“1”,“4”,“0”,“6”,“9”] 
# hasil		: ["0","1","4","6","9"]

def sortArray(list):
    list.sort()
    return list

print(sortArray(['1', '4', '0', '6', '9']))