# Buatlah function dengan Python untuk memeriksa suatu bilangan prima

# Output:
# False

def isPrime(n):
    prime = True
    for i in range(2, int(n / 2) + 1):
        if n % i == 0:
            prime = False
            break
    return prime

print(isPrime(9))