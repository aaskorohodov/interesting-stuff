import time


def is_prime(initial_number: int) -> bool:
    if initial_number <= 1:
        return False

    for numb in range(2, int(initial_number**0.5) + 1):
        if not initial_number % numb:
            if numb != initial_number:
                return False

        if not numb % 100_000_0:
            print(f'Current iteration {numb}\n'
                  f'Overall iteration {int(initial_number**0.5)}')

    return True


prime_numbers = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
    109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
    233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293
]
not_prime_numbers = [
    1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42,
    44, 45, 46, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 60, 62, 63
]

all_good = []
for n in prime_numbers:
    all_good.append(is_prime(n))

print(all(all_good))
all_good_too = []
for n in not_prime_numbers:
    all_good_too.append(is_prime(n) is False)

print(all(all_good_too))
start_time = time.perf_counter()
print(is_prime(9223372036854775783))
print(time.perf_counter() - start_time)

# print(is_prime(170141183460469231731687303715884105727))
